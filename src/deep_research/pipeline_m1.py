from __future__ import annotations

import sys
import uuid
from pathlib import Path

SRC=Path(__file__).resolve().parents[1]
if str(SRC) not in sys.path:
    sys.path.insert(0,str(SRC))

from deep_research.agents.planner import run_planner
from deep_research.agents.searcher import run_searcher,save_evidence_pack
from deep_research.schemas import ResearchState
from deep_research.tools.rag import vector_search
from deep_research.agents.writer import run_writer, save_report, find_citations
from deep_research.agents.critic import apply_critic_loop, run_critic
from deep_research.tools.search import web_search

def run_plan_and_search(question: str) -> ResearchState:
    plan = run_planner(question)
    # 1) 本地 RAG：原问题
    state = run_searcher(question, top_k=4)
    state.plan = plan
    seen_ids = {e.id for e in state.evidence}
    seen_sources = {e.source for e in state.evidence}
    def _merge(extra: list) -> int:
        """把新证据合并进 state.evidence，返回新增条数"""
        added = 0
        for e in extra:
            if e.id in seen_ids or (e.source and e.source in seen_sources):
                continue
            state.evidence.append(e)
            seen_ids.add(e.id)
            if e.source:
                seen_sources.add(e.source)
            added += 1
        return added
    # 2) 联网搜索：先对原问题搜一次（控成本）
    web_added = _merge(web_search(question, max_results=5))
    if web_added:
        state.metrics.tool_calls += 1
    # 3) 子问题：本地补检 + 联网补检
    for sq in plan.sub_questions:
        local_added = _merge(vector_search(sq, top_k=2))
        if local_added:
            state.metrics.tool_calls += 1
        # 子问题也联网的话打开下面两行；想省额度可先注释掉
        w_added = _merge(web_search(sq, max_results=2))
        if w_added:
            state.metrics.tool_calls += 1
    return state



if __name__=="__main__":

    q=input("请输入研究问题:").strip()
    if not q:
        print("问题不能未空")
        raise SystemExit(1)
    # 1) 规划 + 检索
    state = run_plan_and_search(q)
    # 2) Critic 闭环（内部会：检查 → 不通过则补检 → 重写 Writer）
    state = apply_critic_loop(state)
    # 3) 落盘
    evidence_path = save_evidence_pack(state)
    report_path = save_report(state)
    # 4) 最终再检查一次，打印结果
    final = run_critic(state)
    print("research_id:", state.research_id)
    print("plan.sub_questions:")
    for i, sq in enumerate(state.plan.sub_questions, 1):
        print(f"  {i}. {sq}")
    print("evidence_count:", len(state.evidence))
    print("retry_count:", state.metrics.retry_count)
    print("final_passed:", final.passed)
    print("final_issues:", final.issues)
    print("unknown_citations:", final.unknown_citations)
    print("evidence_saved:", evidence_path)
    print("report_saved:", report_path)
    print("----- report preview -----")
    print(state.report_md[:500])