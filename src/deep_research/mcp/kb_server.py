from __future__ import annotations

import sys
from pathlib import Path

SRC = Path(__file__).resolve().parents[2]  # .../src
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mcp.server.mcpserver import MCPServer
from deep_research.tools.rag import vector_search
from deep_research.tools.search import web_search
from deep_research.tools.fetch import fetch_url as _fetch_url

mcp = MCPServer("deep-research-tools")


@mcp.tool()
def rag_search(query: str, top_k: int = 4) -> list[dict]:
    """Search local Chroma knowledge base and return Evidence dicts."""
    hits = vector_search(query, top_k=top_k)
    return [h.model_dump() for h in hits]


@mcp.tool()
def tavily_search(query: str, max_results: int = 5) -> list[dict]:
    """Search the web via Tavily and return Evidence dicts."""
    hits = web_search(query, max_results=max_results)
    return [h.model_dump() for h in hits]


@mcp.tool()
def fetch_url(url: str, max_chars: int = 2000) -> str:
    """Fetch a web page and return extracted plain text."""
    return _fetch_url(url, max_chars=max_chars)


if __name__ == "__main__":
    mcp.run(transport="stdio")