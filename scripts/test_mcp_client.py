from __future__ import annotations

import asyncio
import json
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

ROOT = Path(__file__).resolve().parents[1]
SERVER = ROOT / "src" / "deep_research" / "mcp" / "kb_server.py"
PYTHON = ROOT / ".venv" / "Scripts" / "python.exe"


async def main() -> None:
    if not SERVER.exists():
        raise FileNotFoundError(SERVER)

    server_params = StdioServerParameters(
        command=str(PYTHON),
        args=[str(SERVER)],
        # 把项目 src 环境带给子进程
        cwd=str(ROOT),
        env=None,
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            tools = await session.list_tools()
            print("tools:")
            for t in tools.tools:
                print("-", t.name, ":", (t.description or "")[:80])

            # 调本地 RAG
            rag = await session.call_tool(
                "rag_search",
                arguments={"query": "MCP 是什么", "top_k": 3},
            )
            print("\nrag_search result:")
            print(rag)

            # 调联网（没 Key 可能空列表，但不应整段崩溃）
            web = await session.call_tool(
                "tavily_search",
                arguments={"query": "Model Context Protocol", "max_results": 2},
            )
            print("\ntavily_search result:")
            print(web)

            page = await session.call_tool(
                "fetch_url",
                arguments={"url": "https://modelcontextprotocol.io/introduction", "max_chars": 400},
            )
            print("\nfetch_url result:")
            print(page)


if __name__ == "__main__":
    asyncio.run(main())