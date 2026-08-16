from __future__ import annotations

import json
import sys
import uuid
from datetime import datetime,timezone
from pathlib import Path

#保证能import deep_research
SRC=Path(__file__).resolve().parents[2]
if str(SRC) not in sys.path:
    sys.path.insert(0,str(SRC))

from deep_research.schemas import ResearchState
from deep_research.tools.rag import vector_search

def run_searcher(question:str,top_k:int=4)->ResearchState:
    state=ResearchState(
        research_id=str(uuid.uuid4()),
        question=question,
    )

    evidence=vector_search(question,top_k=top_k)
    state.evidence=evidence
    state.metrics.tool_calls=1

    return state

def save_evidence_pack(state:ResearchState)->Path:
    root=Path(__file__).resolve().parents[3]
    out_dir=root / "outputs" / "reports"
    out_dir.mkdir(parents=True,exist_ok=True)

    out_path=out_dir / f"evidence_{state.research_id}.json"
    out_path.write_text(
        state.model_dump_json(indent=2),
        encoding="utf-8",
    )
    return out_path

if __name__ == "__main__":
    q = "MCP 和 Function Calling 有什么区别？"
    state = run_searcher(q, top_k=4)
    path = save_evidence_pack(state)

    print("research_id:", state.research_id)
    print("evidence_count:", len(state.evidence))
    for e in state.evidence:
        print(f"- {e.id} | {e.score:.4f} | {e.title}")
    print("saved:", path)