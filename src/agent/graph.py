# StateGraph 组装、条件边

from langgraph.graph import StateGraph, START, END
from .state import AgentState
from .nodes import placeholder_node

def build_smoke_graph():
    builder = StateGraph(AgentState)
    builder.add_node("placeholder", placeholder_node)
    builder.add_edge(START, "placeholder")
    builder.add_edge("placeholder", END)
    return builder.compile()
