from __future__ import annotations
from typing import Optional
from pydantic import BaseModel,Field

class Evidence(BaseModel):
    id:str
    source:str
    title:str=""
    snippet:str=""
    retrieved_at:str=""
    score:float=0.0

class Claim(BaseModel):
    text:str
    evidence_ids:list[str]=Field(default_factory=list)
    confidence:float=0.0

class Plan(BaseModel):
    sub_questions:list[str]=Field(default_factory=list)
    success_criteria:list[str]=Field(default_factory=list)
    max_steps:int=12

class Metrics(BaseModel):
    latency_s:float=0.0
    tokens:int=0
    tool_calls:int=0
    retry_count:int=0

class ResearchState(BaseModel):
    research_id:str
    question:str
    plan:Optional[Plan]=None
    evidence:list[Evidence]=Field(default_factory=list)
    claims:list[Claim]=Field(default_factory=list)
    report_md:str=""
    metrics:Metrics=Field(default_factory=Metrics)
