from __future__ import annotations

import asyncio
import json
import os
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from deep_research.schemas import Evidence

ROOT = Path(__file__).resolve().parents[3]
SERVER = ROOT / "src" / "deep_research" / "mcp" / "kb_server.py"
PYTHON = ROOT / ".venv" / "Scripts" / "python.exe"


def _parse_tool_result(result) -> object:
    if getattr(result, "isError", False):
        print(f"[mcp] tool error: {result}")
        return []
    structured = getattr(result, "structuredContent", None)
    if structured is not None:
        if isinstance(structured, dict) and "result" in structured and len(structured) == 1:
            return structured["result"]
        return structured
    texts: list[str] = []
    for block in getattr(result, "content", None) or []:
        text = getattr(block, "text", None)
        if text:
            texts.append(text)
    if not texts:
        return []
    try:
        return json.loads(texts[0])
    except json.JSONDecodeError:
        return texts[0]


def _to_evidence_list(raw) -> list[Evidence]:
    if isinstance(raw, dict) and "result" in raw:
        raw = raw["result"]
    if not isinstance(raw, list):
        return []
    out: list[Evidence] = []
    for item in raw:
        if isinstance(item, dict):
            try:
                out.append(Evidence.model_validate(item))
            except Exception as e:
                print(f"[mcp] skip evidence: {e}")
    return out


def _merge(evidence: list[Evidence], extra: list[Evidence], seen_ids: set[str], seen_sources: set[str]) -> None:
    for e in extra:
        if e.id in seen_ids or (e.source and e.source in seen_sources):
            continue
        evidence.append(e)
        seen_ids.add(e.id)
        if e.source:
            seen_sources.add(e.source)


async def _call_tool(session: ClientSession, name: str, arguments: dict) -> object:
    result = await session.call_tool(name, arguments)
    return _parse_tool_result(result)


async def _search_once(question: str, sub_questions: list[str]) -> list[Evidence]:
    params = StdioServerParameters(
        command=str(PYTHON),
        args=[str(SERVER)],
        cwd=str(ROOT),
        env=os.environ.copy(),
    )
    evidence: list[Evidence] = []
    seen_ids: set[str] = set()
    seen_sources: set[str] = set()

    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            _merge(
                evidence,
                _to_evidence_list(await _call_tool(session, "rag_search", {"query": question, "top_k": 4})),
                seen_ids,
                seen_sources,
            )
            _merge(
                evidence,
                _to_evidence_list(await _call_tool(session, "tavily_search", {"query": question, "max_results": 5})),
                seen_ids,
                seen_sources,
            )
            for sq in sub_questions:
                _merge(
                    evidence,
                    _to_evidence_list(await _call_tool(session, "rag_search", {"query": sq, "top_k": 2})),
                    seen_ids,
                    seen_sources,
                )
                _merge(
                    evidence,
                    _to_evidence_list(await _call_tool(session, "tavily_search", {"query": sq, "max_results": 2})),
                    seen_ids,
                    seen_sources,
                )

            web_items = [e for e in evidence if (e.source or "").startswith("http")]
            web_items.sort(key=lambda e: e.score, reverse=True)
            for e in web_items[:2]:
                body = await _call_tool(session, "fetch_url", {"url": e.source, "max_chars": 2000})
                if isinstance(body, str) and len(body) >= 80:
                    e.snippet = body[:2000]
                    print(f"[mcp fetch_url] upgraded {e.source[:80]}")

    return evidence


def search_via_mcp(question: str, sub_questions: list[str]) -> list[Evidence]:
    if not PYTHON.exists():
        raise FileNotFoundError(f"MCP python not found: {PYTHON}")
    if not SERVER.exists():
        raise FileNotFoundError(f"MCP server not found: {SERVER}")
    return asyncio.run(_search_once(question, sub_questions or []))
