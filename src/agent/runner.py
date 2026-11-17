# 入口：invoke / stream / resume

import asyncio
from .graph import build_react_graph
from langchain_core.messages import HumanMessage
from .checkpointer import get_checkpointer

async def main():
   checkpointer = await get_checkpointer()
   graph = build_react_graph(checkpointer=checkpointer)
   result = await graph.ainvoke(
       {
           "messages": [HumanMessage(content="How's the weather today in Shanghai?")],
           "step_count": 0
       },
       config={"configurable": {"thread_id": "test-thread-8"}}
   )

   print("=== 最终消息列表 ===")
   
   for msg in result["messages"]:
       print(f" {msg.type}: {msg.content}")


if __name__ == "__main__":
    asyncio.run(main(), loop_factory=asyncio.SelectorEventLoop)