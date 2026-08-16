from __future__ import annotations

from datetime import datetime,timezone

from tavily import TavilyClient

from deep_research.config import SEARCH_API_KEY
from deep_research.schemas import Evidence

def web_search(query:str,max_results:int=5)->list[Evidence]:
    if not SEARCH_API_KEY:
        print("[web_search] missing SEARCH_API_KEY,skip")
        return []

    client=TavilyClient(api_key=SEARCH_API_KEY)
    resp=client.search(query=query,max_results=max_results)

    #SDK一般返回dict
    results=resp.get("results",[]) if isinstance(resp,dict) else []
    now=datetime.now(timezone.utc).isoformat()
    evidence_list:list[Evidence]=[]

    for i,item in enumerate(results):
        url=item.get("url","") or ""
        title=item.get("title","") or ""
        snippet=item.get("snippet","") or ""
        score=float(item.get("score",0.0) or 0.0)

        evidence_list.append(
            Evidence(
                id=f"web::{i}::{abs(hash(url))%100000}",
                source=url,
                title=title,
                snippet=snippet[:800],
                retrieved_at=now,
                score=score,
            )
        )
    return evidence_list

if __name__ == "__main__":
    import sys
    from pathlib import Path
    SRC = Path(__file__).resolve().parents[2]
    if str(SRC) not in sys.path:
        sys.path.insert(0, str(SRC))
    hits = web_search("MCP vs Function Calling", max_results=3)
    print("hits:", len(hits))
    for e in hits:
        print("-", e.title)
        print(" ", e.source)