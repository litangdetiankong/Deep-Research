from __future__ import annotations

import re
import sys
from dataclasses import dataclass,field
from pathlib import Path

SRC = Path(__file__).resolve().parents[2]
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from typing import Callable

from deep_research.config import MAX_CRITIC_ROUNDS
from deep_research.schemas import ResearchState
from deep_research.tools.rag import vector_search
from deep_research.agents.writer import run_writer,find_citations

ProgressFn = Callable[[str, str], None] | None

@dataclass
class CriticResult:
    passed:bool
    issues:list[str]=field(default_factory=list)
    citations:list[str]=field(default_factory=list)
    unknown_citations:list[str]=field(default_factory=list)

def run_critic(state:ResearchState)->CriticResult:
    report=state.report_md or ""
    issues:list[str]=[]

    if not report.strip():
        return CriticResult(passed=False,issues=["报告未空"])

    #1.基本结构标题
    required_headers=["结论摘要","分节论证","不确定与局限","参考来源"]
    for h in required_headers:
        if h not in report:
            issues.append(f"缺少章节:{h}")

    #2.引用提取
    citations=find_citations(report)
    valid_ids={e.id for e in state.evidence}
    unknown=[c for c in citations if c not in valid_ids]

    if not citations:
        issues.append("报告中没有任何[evidence_id]引用")

    if unknown:
        issues.append(f"存在未知引用:{unknown}")

    #3.结论摘要里至少要有引用
    m=re.search(r"##\s*1\.? ?结论摘要(.*?)(?:\n##\s*|\Z)",report,flags=re.S)
    if m:
        summary=m.group(1)
        summary_cites=find_citations(summary)
        if len(summary_cites)<2:
            issues.append("结论摘要引用过少(少于2个)")
    else:
        issues.append("未找到结论摘要段落,无法检查摘要引用")

    passed=len(issues)==0
    return CriticResult(
        passed=passed,
        issues=issues,
        citations=citations,
        unknown_citations=unknown,
    )

def _build_repair_queries(state:ResearchState,result:CriticResult)->list[str]:
    queries=[]

    #永远用原问题补一轮
    queries.append(state.question)

    #若有计划，用子问题再补
    if state.plan:
        queries.extend(state.plan.sub_questions[:3])

    #针对"引用过少/未知引用"再加一句约束型查询
    if any("引用" in x for x in result.issues):
        queries.append(state.question+"关键证据与来源")

    #去重保序
    seen=set()
    uniq=[]
    for q in queries:
        q=q.strip()
        if q and q not in seen:
            seen.add(q)
            uniq.append(q)
    return uniq

def _supplement_evidence(state:ResearchState,queries:list[str],top_k:int=2)->int:
    seen={e.id for e in state.evidence}
    added=0
    for q in queries:
        for e in vector_search(q,top_k=top_k):
            if e.id not in seen:
                state.evidence.append(e)
                seen.add(e.id)
                added+=1
                state.metrics.tool_calls+=1
    return added

def apply_critic_loop(state:ResearchState,max_rounds:int | None=None,on_progress:ProgressFn=None)->ResearchState:
    if max_rounds is None:
        max_rounds=MAX_CRITIC_ROUNDS

    def emit(stage:str,message:str)->None:
        print(f"[progress] {stage}: {message}")
        if on_progress:
            on_progress(stage,message)

    for round_idx in range(max_rounds):
        #第一轮先检查现有报告；若还没有报告，先写一次
        if not (state.report_md or "").strip():
            emit("writer","正在撰写报告…")
            state=run_writer(state)

        emit("critic",f"质量检查 round={round_idx}…")
        result=run_critic(state)
        print(f"[critic] round={round_idx},passed{result.passed},issues={result.issues}")

        if result.passed:
            state.metrics.retry_count=round_idx
            emit("critic","质量检查通过")
            return state

        #最后一轮失败:保留报告，但不再重写
        if round_idx==max_rounds-1:
            state.metrics.retry_count=round_idx
            note= "\n\n---\n## Critic 审查未完全通过\n" + "\n".join(f"- {x}" for x in result.issues)
            state.report_md+=note
            emit("critic","质量检查未完全通过，已写入说明")
            return state

        emit("repair","检查未通过，正在补检并重写…")
        queries=_build_repair_queries(state,result)
        added=_supplement_evidence(state,queries,top_k=2)
        print(f"[critic] supplemented_evidence={added}")
        emit("writer","正在重写报告…")
        state=run_writer(state)

    return state
