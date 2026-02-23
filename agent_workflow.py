from langgraph.graph import StateGraph, END
from state import AgentState
from planner import planner_node
from researcher import researcher_node
from coder import coder_node
from evaluator import evaluator_node

def create_research_graph():
    """Workflow: Planner -> Researcher -> Coder -> Evaluator -> END"""
    workflow = StateGraph(AgentState)

    workflow.add_node("planner", planner_node)
    workflow.add_node("researcher", researcher_node)
    workflow.add_node("coder", coder_node)
    workflow.add_node("evaluator", evaluator_node)

    # Fixed linear path to avoid any routing errors
    workflow.set_entry_point("planner")
    workflow.add_edge("planner", "researcher")
    workflow.add_edge("researcher", "coder")
    workflow.add_edge("coder", "evaluator")
    workflow.add_edge("evaluator", END)

    return workflow.compile()
