from __future__ import annotations

import json
import re
import sys
from pathlib import Path

SRC=Path(__file__).resolve().parents[2]
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from deep_research.llm import chat
from deep_research.schemas import Plan

SYSTEM_PROMPT="""
你是技术调研项目的Planner。
请你把用户问题拆成可检索的研究计划，只输出json，不要Markdown，不要解释。
json格式必须是:
{
    "sub_questions":["...","..."],
    "success_criteria":["...","..."],
    "max_steps":12
}
约束:
1.sub_questions 3到5个，具体可检索
2.success_criteria 2到4条
3.max_steps 为8到16的整数
领域:技术知识研报(Agent/RAG/MCP/框架对比等)
""".strip()

def _extract_json(text:str)->dict:
    text=text.strip()
    if "'''" in text:
        m=re.search(r"'''(?:json)?\s*(\{.*?\})\s*'''",text,flags=re.DOTALL)
        if m:
            text=m.group(1)
    return json.loads(text)

def run_planner(question:str)->Plan:
    raw=chat(
        messages=[
            {"role":"system","content":SYSTEM_PROMPT},
            {"role":"user","content":question},
        ],
        temperature=0.2,
    )
    data=_extract_json(raw)
    plan=Plan.model_validate(data)
    return plan