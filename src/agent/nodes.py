# agent 节点、tools 节点
from datetime import datetime

from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, ToolMessage
from .state import AgentState
from src.tools.client import load_tools_resilient
from src.security.policy_engine import PolicyEngine
import os
import json

llm = ChatOpenAI(
        model="deepseek-flash",
        temperature=0,
        openai_api_key=os.getenv("DEEPSEEK_API_KEY"),
        base_url=os.getenv("DEEPSEEK_API_BASE_URL", "https://api.deepseek.com")
        )

mcp_tools = None
mcp_tools_by_name = {}  # 工具名 -> Tool 对象的映射

async def call_model(state: AgentState) -> dict:
    """
    call_model 是一个异步函数，用于调用模型进行推理。

    Returns:
        dict: 返回一个字典，表示模型的输出结果。
    """
    # 在这里可以添加调用模型的逻辑
    # 例如，使用 OpenAI API 或其他模型进行推理
    # 这里我们返回一个示例输出

    global mcp_tools, mcp_tools_by_name
    if mcp_tools is None:
        try:
            mcp_tools = await load_tools_resilient()
            mcp_tools_by_name = { tool.name: tool for tool in mcp_tools }
        except:
            mcp_tools = []
            mcp_tools_by_name = {}

    llm_with_tools  = llm.bind_tools(mcp_tools) if mcp_tools else llm
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

async def tools_node(state: AgentState) -> dict:
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

    if mcp_tools is None:
        raise RuntimeError("tools_node 执行时 mcp_tools 尚未加载")

    global mcp_tools_by_name
    tool_messages = []
    _policy_engine  = PolicyEngine()
    for t in last.tool_calls:

        role = "user"
        tool_name = t.get("name")
        tool_call_id = t.get("id")
        query = t.get("args", {})
        tool = mcp_tools_by_name.get(tool_name)  
        decision = _policy_engine.get_decision(tool_name, role)

        if not tool_call_id:
            tool_messages.append(ToolMessage(
                content=json.dumps({
                    "error": True,
                    "code": "MISSING_TOOL_CALL_ID",
                    "message": "工具调用ID缺失",
                    "retryable": False
                }, ensure_ascii=False),
                tool_call_id=None
            ))
            continue
        
        if decision == "deny":
            tool_messages.append(ToolMessage(
                content= json.dumps({
                    "error":True,
                    "code":"PERMISSION_DENIED",
                    "message":  f"当前角色 {role} 无权调用工具 {tool_name}",
                    "retryable": False
                }, ensure_ascii= False),
                tool_call_id = tool_call_id
            ))
            continue

        if decision == "require_approval":
            tool_messages.append(ToolMessage(
                content= json.dumps({
                    "error":True,
                    "code":"APPROVAL_REQUIRED",
                    "message":  f"工具 {tool_name} 需要人工审批，当前流程暂不支持",
                    "retryable": False
                }, ensure_ascii= False),
                tool_call_id = tool_call_id
            ))
            continue

        if tool is None:
            tool_messages.append(ToolMessage(
                content=json.dumps({
                    "error": True,
                    "code": "UNKNOWN_TOOL",
                    "message": f"未知工具: {tool_name}",
                    "retryable": False
                }, ensure_ascii=False),
                tool_call_id=tool_call_id
            ))
            continue

        try:
            raw = await tool.ainvoke(query)
            text = raw

            if isinstance(raw, list) and raw and isinstance(raw[0], dict):
                text = raw[0].get("text")

            if not isinstance(text, str) or not text.strip():
                tool_messages.append(ToolMessage(content=json.dumps({"error": True, "code": "EMPTY_RESULT", "message": "工具返回为空", "retryable": False}, ensure_ascii=False), tool_call_id=tool_call_id))
                continue

            try:
                obj = json.loads(text)
            except json.JSONDecodeError:
                tool_messages.append(ToolMessage(
                content=json.dumps({
                        "error": True,
                        "code": "INVALID_JSON",
                        "message": "工具返回格式非合法JSON",
                        "retryable": False
                    }, ensure_ascii=False),
                    tool_call_id=tool_call_id
                ))
                continue

            if isinstance(obj, dict) and obj.get("ok") is True:
                tool_messages.append(ToolMessage(content=json.dumps(obj.get("data"),ensure_ascii=False), tool_call_id=tool_call_id))
                continue

            error = obj.get("error",{})
            if error.get("retryable") is True:
                err_msg = error.get("message", str(error))
                err_code = error.get("code")
                if err_code =="SERVICE_UNAVAILABLE":
                    print(f"[DEBUG] 准备抛出异常，当前时间: {datetime.now()}")
                    raise ConnectionError(f"工具 {tool_name} 服务不可用: {err_msg}")
                else:
                    print(f"[DEBUG] 准备抛出异常，当前时间: {datetime.now()}")
                    raise TimeoutError(f"工具 {tool_name} 调用超时: {err_msg}")
                        
            tool_messages.append(ToolMessage(content=text, tool_call_id=tool_call_id))  

        except TimeoutError as e:
            raise TimeoutError(f"工具 {tool_name}, 信息：{e}")
        except ConnectionError as e:
            raise ConnectionError(f"工具 {tool_name}, 信息：{e}")
        except Exception as exc:
            raise RuntimeError(f"工具 {tool_name} 调用失败: {exc}")

    return {"messages": tool_messages}