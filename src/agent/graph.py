# StateGraph 组装、条件边

from langgraph.graph import StateGraph, START, END
from .state import AgentState
from .nodes import call_model, router, tools_node


def build_react_graph():
    builder = StateGraph(AgentState)
    builder.add_node("call_model", call_model)
    builder.add_node("tools_node", tools_node)
   
    builder.add_edge(START, "call_model")
    builder.add_conditional_edges(
        "call_model",
        router,
        {
            "tools": "tools_node",
            "end": END
        }
    )   
    builder.add_edge("tools_node", "call_model")
    return builder.compile()