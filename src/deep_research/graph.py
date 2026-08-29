from typing import Any,Callable,TypedDict

from langgraph.graph import END,START,StateGraph
from langchain_core.runnables import RunnableConfig

from deep_research.agents.critic import repair_once, run_critic
from deep_research.agents.searcher import save_evidence_pack
from deep_research.agents.writer import run_writer,save_report
from deep_research.config import MAX_CRITIC_ROUNDS
from deep_research.pipeline_m1 import run_plan_and_search
from deep_research.schemas import ResearchState

class GraphState(TypedDict,total=False):
    question:str
    max_rounds:int
    round_idx:int
    research:ResearchState
    passed:bool
    issues:list[str]

def _progress(config:RunnableConfig | None,stage:str,message:str)->None:
    fn:Callable | None=(config or {}).get("configurable",{}).get("on_progress")
    print(f"[progress] {stage}: {message}")
    if fn:
        fn(stage,message)

def node_plan_and_search(state:GraphState,config:RunnableConfig)->dict:
    on_progress = (config or {}).get("configurable", {}).get("on_progress")
    research = run_plan_and_search(state["question"], on_progress=on_progress)
    return {"research":research,"round_idx":0,"passed":False,"issues":[]}

def node_write(state:GraphState,config:RunnableConfig)->dict:
    _progress(config,"writer","正在撰写报告...")
    research=run_writer(state["research"])
    return {"research":research}

def node_critic(state:GraphState,config:RunnableConfig)->dict:
    research=state["research"]
    round_idx=int(state.get("round_idx") or 0)
    _progress(config,"critic",f"质量检查 round={round_idx}...")
    result=run_critic(research)
    print(f"[critic] round={round_idx},passed={result.passed},issues={result.issues}")
    research.metrics.retry_count=round_idx
    return {
        "research":research,
        "passed":result.passed,
        "issues":result.issues,
    }

def node_repair(state:GraphState,config:RunnableConfig)->dict:
    research=state["research"]
    issues=state.get("issues") or []
    _progress(config,"repair","检查未通过，正在补检...")
    added=repair_once(research,issues,top_k=2)
    print(f"[critic] supplemented_evidence={added}")
    return {"research":research,"round_idx":int(state.get("round_idx") or 0)+1}

def node_fail_note(state:GraphState,config:RunnableConfig)->dict:
    research=state["research"]
    issues=state.get("issues") or []
    note="\n\n---\n## Critic 审查未完全通过\n"+"\n".join(f"-{x}" for x in issues)
    research.report_md=(research.report_md or "")+note
    _progress(config,"critic","质量检查未完全通过，已写入说明")
    return {"research":research}

def node_save(state:GraphState,config:RunnableConfig)->dict:
    research=state["research"]
    save_evidence_pack(research)
    save_report(research)
    return {"research":research}

def _after_critic(state:GraphState)->str:
    if state.get("passed"):
        return "save"
    max_rounds=int(state.get("max_rounds") or MAX_CRITIC_ROUNDS)
    round_idx=int(state.get("round_idx") or 0)
    if round_idx>=max_rounds-1:
        return "fail_note"
    return "repair"

def build_graph():
    g=StateGraph(GraphState)
    g.add_node("plan_and_search",node_plan_and_search)
    g.add_node("write",node_write)
    g.add_node("critic",node_critic)
    g.add_node("repair", node_repair)
    g.add_node("fail_note", node_fail_note)
    g.add_node("save", node_save)

    g.add_edge(START,"plan_and_search")
    g.add_edge("plan_and_search","write")
    g.add_edge("write","critic")
    g.add_conditional_edges(
        "critic",
        _after_critic,
        {"save":"save","fail_note":"fail_note","repair":"repair"},
    )
    g.add_edge("repair","write")
    g.add_edge("fail_note","save")
    g.add_edge("save",END)
    return g.compile()

_APP=None

def run_with_graph(
        question:str,
        max_rounds:int | None=None,
        on_progress:Callable[[str,str],None] | None=None,
)->ResearchState:
    global _APP
    if _APP is None:
        _APP=build_graph()
    if max_rounds is None:
        max_rounds=MAX_CRITIC_ROUNDS
    out=_APP.invoke(
        {"question":question,"max_rounds":max_rounds,"round_idx":0},
        config={"configurable":{"on_progress":on_progress}},
    )
    return out["research"]