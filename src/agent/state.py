# AgentState TypedDict 定义

from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages


class AgentState(TypedDict):
    """
    AgentState 是一个 TypedDict，用于表示代理的状态信息。

    Attributes:
        messages (list): 消息列表，包含与代理相关的消息。
    """

    messages: Annotated[list, add_messages]