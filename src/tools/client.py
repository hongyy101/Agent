 # MultiServerMCPClient 封装
from langchain_mcp_adapters.client import MultiServerMCPClient
import sys

SERVER_CONFIGS = {
    "search" : {
        "command": sys.executable,
        "args": ["src/tools/mcp_servers/search_server.py"],
        "transport": "stdio"
    },
    "weather" : {
        "url": "http://127.0.0.1:8001/mcp",
        "transport": "streamable_http"
    },
    "user": {
        "url": "http://127.0.0.1:8002/mcp",
        "transport": "streamable_http",
    }
}

async def load_tools_resilient() -> list:
    all_tools = []
    for name, cfg in SERVER_CONFIGS.items():
        try:
            client = MultiServerMCPClient({name: cfg})
            tools = await client.get_tools()
            all_tools.extend(tools)
            print(f"[mcp] {name} 加载成功，{len(tools)} 个工具")
        except Exception as e:
            print(f"[mcp] {name} 加载失败，跳过: {e}")

    return all_tools