# 图编排单元测试

from langchain_core.messages import AIMessage, HumanMessage, ToolMessage

from src.agent.nodes import tools_node


def test_tools_node_handles_every_tool_call_id():
    state = {
        "messages": [
            HumanMessage(content="search two queries"),
            AIMessage(
                content="",
                tool_calls=[
                    {"id": "call_1", "name": "fake_search", "args": {"query": "LangGraph"}},
                    {"id": "call_2", "name": "fake_search", "args": {"query": "StateGraph"}},
                ],
            ),
        ]
    }

    result = tools_node(state)

    tool_messages = result["messages"]
    assert len(tool_messages) == 2
    assert [msg.tool_call_id for msg in tool_messages] == ["call_1", "call_2"]
    assert all("LangGraph" in msg.content or "StateGraph" in msg.content for msg in tool_messages)
