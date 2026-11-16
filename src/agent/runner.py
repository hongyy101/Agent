# 入口：invoke / stream / resume

import asyncio
from .graph import build_react_graph
from langchain_core.messages import HumanMessage

async def main():
   graph = build_react_graph()
   result = await graph.ainvoke(
       {
           "messages": [HumanMessage(content="LangGraph 是什么？")],
           "step_count": 0
       }
   )

   print("=== 最终消息列表 ===")
   
   for msg in result["messages"]:
       print(f" {msg.type}: {msg.content}")


if __name__ == "__main__":
    asyncio.run(main())