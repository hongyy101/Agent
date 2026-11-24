# StateGraph 组装、条件边

from langgraph.graph import StateGraph, START, END
from langchain_core.messages import ToolMessage
from langgraph.types import RetryPolicy
from .state import AgentState
from .nodes import call_model, router, tools_node
import json

def handle_tool_error(state: AgentState)-> dict:
    """当工具重试彻底失败后，生成一个兜底的 ToolMessage，让模型能优雅收尾"""
    print("[error_handler] 工具重试彻底失败，执行兜底逻辑")
    last_message = state["messages"][-1]
    tool_messages = []
    
    # 为每一个工具调用生成一个失败的 ToolMessage
    for t in last_message.tool_calls:
        tool_messages.append(
            ToolMessage(
                content=json.dumps({
                    "error": True,
                    "code": "RETRY_EXHAUSTED",
                    "message": "服务重试次数已达上限，暂时无法获取数据，请稍后再试。",
                    "retryable": False
                }, ensure_ascii=False),
                tool_call_id=t.get("id")
            )
        )
    return {"messages": tool_messages}

def build_react_graph(checkpointer=None) -> StateGraph:
    builder = StateGraph(AgentState)
    builder.add_node("call_model", call_model)
    builder.add_node("tools_node", 
                    tools_node, 
                    retry_policy = RetryPolicy(
                        max_attempts=3,
                        backoff_factor=2.0,
                        jitter=True,
                        retry_on=(ConnectionError,TimeoutError)
                    ),
                    error_handler= handle_tool_error)
   
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
    return builder.compile(checkpointer=checkpointer)