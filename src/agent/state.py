# AgentState TypedDict 定义

from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages


class AgentState(TypedDict):
    """
    AgentState 是一个 TypedDict，用于表示代理的状态信息。

    Attributes:
        messages (list): 消息列表，包含与代理相关的消息。
        step_count (int): 步骤计数器，用于跟踪代理的操作步骤。
    """

    messages: Annotated[list, add_messages]
    step_count: int