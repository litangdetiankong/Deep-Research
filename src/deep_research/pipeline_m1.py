from __future__ import annotations

import sys
import uuid
from pathlib import Path
from typing import Callable

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
from deep_research.tools.fetch import fetch_url
from deep_research.config import USE_MCP

ProgressFn = Callable[[str, str], None] | None


def _emit(on_progress: ProgressFn, stage: str, message: str) -> None:
    print(f"[progress] {stage}: {message}")
    if on_progress:
        on_progress(stage, message)


def _upgrade_top_web(state: ResearchState) -> int:
    web_items = [e for e in state.evidence if (e.source or "").startswith("http")]
    web_items.sort(key=lambda e: e.score, reverse=True)
    fetched = 0
    for e in web_items[:2]:
        body = fetch_url(e.source)
        if not body:
            continue
        e.snippet = body
        fetched += 1
        state.metrics.tool_calls += 1
    print(f"[fetch_url] upgraded={fetched}")
    return fetched


def run_plan_and_search(question: str, on_progress: ProgressFn = None) -> ResearchState:
    _emit(on_progress, "planner", "正在拆解研究计划…")
    plan = run_planner(question)

    if USE_MCP:
        _emit(on_progress, "mcp", "经 MCP 检索中（本地 + 联网 + 深读）…")
        from deep_research.tools.mcp_bridge import search_via_mcp
        hits = search_via_mcp(question, plan.sub_questions)
        state = ResearchState(
            research_id=str(uuid.uuid4()),
            question=question,
            plan=plan,
        )
        state.evidence = hits
        state.metrics.tool_calls = 1
        _emit(on_progress, "search_done", f"证据已收集 {len(state.evidence)} 条")
        return state

    _emit(on_progress, "rag", "正在检索本地知识库…")
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
    _emit(on_progress, "web", "正在联网搜索…")
    web_added = _merge(web_search(question, max_results=5))
    if web_added:
        state.metrics.tool_calls += 1
    for sq in plan.sub_questions:
        local_added = _merge(vector_search(sq, top_k=2))
        if local_added:
            state.metrics.tool_calls += 1
        w_added = _merge(web_search(sq, max_results=2))
        if w_added:
            state.metrics.tool_calls += 1
    _emit(on_progress, "fetch", "正在深读高分网页…")
    _upgrade_top_web(state)
    _emit(on_progress, "search_done", f"证据已收集 {len(state.evidence)} 条")
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
