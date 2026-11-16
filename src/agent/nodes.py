 # agent 节点、tools 节点
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, ToolMessage
from .state import AgentState
import os

llm = ChatOpenAI(
        model="deepseek-flash",
        temperature=0,
        openai_api_key=os.getenv("DEEPSEEK_API_KEY"),
        base_url=os.getenv("DEEPSEEK_API_BASE_URL", "https://api.deepseek.com")
        )

def fake_search(query:str) -> str:

    """
    搜索 LangGraph 相关文档。当用户询问 LangGraph 概念、用法或原理时使用。

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

    llm_with_tools  = llm.bind_tools([fake_search])

    response = await llm_with_tools.ainvoke(state['messages'])

    return {"messages": [response]}

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
    if not isinstance(last, AIMessage) or not last.tool_calls:
        return {"messages": [ToolMessage(content="No tool call found.", tool_call_id=None)]}

    tool_messages = []
    for tool in last.tool_calls:
        tool_name = tool.get("name")
        tool_call_id = tool.get("id")
        if tool_name == "fake_search":
            query = tool.get("args", {}).get("query")
            search_result = fake_search(query)
            tool_messages.append(ToolMessage(content=search_result, tool_call_id=tool_call_id))
        else:
            tool_messages.append(ToolMessage(content=f"Unknown tool: {tool_name}", tool_call_id=tool_call_id))

    return {"messages": tool_messages}