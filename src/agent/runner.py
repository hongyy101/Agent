# 入口：invoke / stream / resume

import asyncio
from .graph import build_smoke_graph

async def main():
   graph = build_smoke_graph()
   result = await graph.ainvoke(
       {"messages": [{"role": "user", "content": "你好"}]}
   )

   print("=== 最终消息列表 ===")
   
   for msg in result["messages"]:
       print(f" {msg.type}: {msg.content}")


if __name__ == "__main__":
    asyncio.run(main())

    