from __future__ import annotations

import sys
from pathlib import Path

SRC = Path(__file__).resolve().parents[2]
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from deep_research.pipeline_m1 import run_plan_and_search
from deep_research.agents.critic import apply_critic_loop
from deep_research.agents.searcher import save_evidence_pack
from deep_research.agents.writer import save_report
from datetime import datetime, timezone
from deep_research.history_store import append_history
from deep_research.history_store import list_history, get_history

class ResearchRequest(BaseModel):
    question:str=Field(...,min_length=1,description="研究问题")
    max_rounds:int=Field(2,ge=0,le=3,description="Critic最大重写轮数")

class ResearchResponse(BaseModel):
    research_id: str
    question: str
    plan_sub_questions: list[str]
    evidence_count: int
    retry_count: int
    report_md: str
    evidence_path: str
    report_path: str

app=FastAPI(title="Deep-Research API",version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/research", response_model=ResearchResponse)
def research(req: ResearchRequest):
    q = req.question.strip()
    if not q:
        raise HTTPException(status_code=400, detail="question 不能为空")

    try:
        state = run_plan_and_search(q)
        state = apply_critic_loop(state, max_rounds=req.max_rounds)

        evidence_path = save_evidence_pack(state)
        report_path = save_report(state)

        append_history(
            {
                "research_id": state.research_id,
                "question": state.question,
                "created_at": datetime.now(timezone.utc).isoformat(),
                "evidence_count": len(state.evidence),
                "retry_count": state.metrics.retry_count,
                "report_path": str(report_path),
                "evidence_path": str(evidence_path),
                "report_md": state.report_md or "",
                "plan_sub_questions": list(state.plan.sub_questions) if state.plan else [],
            }
        )

        return ResearchResponse(
            research_id=state.research_id,
            question=state.question,
            plan_sub_questions=list(state.plan.sub_questions) if state.plan else [],
            evidence_count=len(state.evidence),
            retry_count=state.metrics.retry_count,
            report_md=state.report_md or "",
            evidence_path=str(evidence_path),
            report_path=str(report_path),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

ROOT = Path(__file__).resolve().parents[3]
WEB_DIR = ROOT / "web"

if WEB_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(WEB_DIR)), name="static")

    @app.get("/")
    def index_page():
        index = WEB_DIR / "index.html"
        if not index.exists():
            raise HTTPException(status_code=404, detail="index.html missing")
        return FileResponse(index)

@app.get("/history")
def api_list_history(limit: int = 50):
    return {"items": list_history(limit=limit)}
@app.get("/history/{research_id}")
def api_get_history(research_id: str):
    item = get_history(research_id)
    if not item:
        raise HTTPException(status_code=404, detail="history not found")
    # 若历史没存 report_md，则从文件读
    if not item.get("report_md") and item.get("report_path"):
        p = Path(item["report_path"])
        if p.exists():
            item["report_md"] = p.read_text(encoding="utf-8")
    return item