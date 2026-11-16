 # agent 节点、tools 节点
from langchain_core.messages import AIMessage, ToolMessage
from .state import AgentState

def fake_search(query:str) -> str:

    """
    fack_search 是一个模拟搜索函数，用于根据查询返回搜索结果。

    Args:
        query (str): 搜索查询字符串

    Returns:
        dict: 返回一个搜索结果。
    """
    # 在这里可以添加搜索逻辑
    # 例如，调用搜索引擎 API 或数据库查询
    # 这里我们返回一个示例输出

    return f"这是一个关于 {query} 的搜索结果"

async def call_model(state: AgentState) -> dict:
    """
    call_model 是一个异步函数，用于调用模型进行推理。

    Returns:
        dict: 返回一个字典，表示模型的输出结果。
    """
    # 在这里可以添加调用模型的逻辑
    # 例如，使用 OpenAI API 或其他模型进行推理
    # 这里我们返回一个示例输出

    step = state.get("step_count", 0) + 1
    if step == 1:
        msg = AIMessage(
            content="模型推理结果：需要调用工具。",
            tool_calls=[
                { 
                    "name": "fake_search", 
                    "args": {"query": "LangGraph"}, 
                    "id": "tool_call_1" 
                }
            ])
    else:
        msg = AIMessage(content="根据搜索结果，LangGraph 是一个图编排框架。")

    return {"messages": [msg], "step_count": step}

def router(state: AgentState) -> str:
    """
    router 是一个路由函数，用于根据代理的状态决定下一步的操作。

    Args:
        state (AgentState): 代理的状态信息

    Returns:
        str: 返回一个字符串，表示路由的输出结果。
    """
    # 在这里可以添加路由逻辑
    # 例如，根据 state 的内容决定下一步的操作
    # 这里我们返回一个示例输出

    last = state['messages'][-1] 
    
    if isinstance(last, AIMessage) and last.tool_calls:
        return "tools"
    else:
        return "end"


def tools_node(state: AgentState) -> dict:
    """
    tools_node 是一个工具节点函数，用于在代理的状态中执行特定工具操作。

    Args:
        state (AgentState): 代理的状态信息

    Returns:
        dict: 返回一个字典，表示工具节点的输出结果。
    """
    # 在这里可以添加对 state 的处理逻辑
    # 例如，调用特定的工具或执行操作
    # 这里我们返回一个示例输出

    last = state['messages'][-1] 
    if isinstance(last, AIMessage) and last.tool_calls:
        tool_call = last.tool_calls[0]
        if tool_call["name"] == "fake_search":
            query = tool_call["args"]["query"]
            search_result = fake_search(query)
            return {"messages": [ToolMessage(content=search_result, tool_call_id=tool_call["id"])]}
    
    return {"messages": [ToolMessage(content="No tool call found.", tool_call_id=None)]}