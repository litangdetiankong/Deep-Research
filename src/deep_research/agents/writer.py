from __future__ import annotations

import re
import sys
from pathlib import Path

SRC=Path(__file__).resolve().parents[2]
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from deep_research.llm import chat
from deep_research.schemas import Evidence,Plan,ResearchState
REPORT_OUTLINE="""
请严格按以下Markdown结构输出（不要省略标题）:

#研究报告标题

## 1.结论摘要
-用3~5条要点概况
-每条要点末尾必须带引用,格式如[04_mcp_overview::0]

## 2.分节论证
### 2.1 ...
### 2.2 ...
(按研究子问题组织；段落中关键论断都要带[evidence_id])

## 3.不确定与局限
-说明证据不足或冲突之处
-没有证据支撑时，明确写[现有资料不足]，不要编造

## 4.参考来源
-列表列出用到的evidence:id、title、source
""".strip()

def _format_evidence(evidence:list[Evidence],max_items:int=8)->str:
    lines=[]
    for e in evidence[:max_items]:
        snippet=(e.snippet or "").replace("\n","")
        if len(snippet)>800:
            snippet=snippet[:800]+"..."
        lines.append(
            f"- id:{e.id}\n"
            f"  title:{e.title}\n"
            f"  source:{e.source}\n"
            f"  snippet:{snippet}\n"
        )
    return "\n".join(lines) if lines else "(无证据)"

def _format_plan(plan:Plan | None)->str:
    if plan is None:
        return "(无计划)"
    subs="\n".join(f"- {q}" for q in plan.sub_questions) or "- (无)"
    crit="\n".join(f"- {c}" for c in plan.success_criteria) or "- (无)"
    return f"子问题:\n{subs}\n\n成功标准:\n{crit}\nmax_steps: {plan.max_steps}"

SYSTEM_PROMPT=f"""
你是技术知识研报Writer。
只能基于给定证据写作，禁止编造证据中不存在的事实。
引用格式必须使用方括号evidence_id,例如[04_mcp_overview::0]。
不要输出json，只输出Markdown正文。

{REPORT_OUTLINE}
""".strip()

def run_writer(state:ResearchState,max_evidence:int=8)->ResearchState:
    user_prompt=(
        f"研究问题:\n{state.question}\n\n"
        f"研究计划:\n{_format_plan(state.plan)}\n\n"
        f"证据列表:\n{_format_evidence(state.evidence,max_items=max_evidence)}\n\n"
    )
    report=chat(
        messages=[
            {
                "role":"system","content":SYSTEM_PROMPT
            },
            {"role":"user","content":user_prompt},
        ],
        temperature=0.3,
    )
    state.report_md=(report or "").strip()
    return state

def save_report(state:ResearchState)->Path:
    root=Path(__file__).resolve().parents[3]
    out_dir=root / "outputs" / "reports"
    out_dir.mkdir(parents=True,exist_ok=True)
    path=out_dir / f"report_{state.research_id}.md"
    path.write_text(state.report_md,encoding="utf-8")
    return path

def find_citations(report_md:str)->list[str]:
    raw=re.findall(r"\[([^\[\]]+)\]",report_md)
    return [c for c in raw if "::" in c]