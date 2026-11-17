 # MultiServerMCPClient 封装
from langchain_mcp_adapters.client import MultiServerMCPClient

async def create_client() -> MultiServerMCPClient:
    """创建一个 MultiServerMCPClient 实例"""

    return MultiServerMCPClient({
       "search" : {
                "command": "python",
                "args": ["src/tools/mcp_servers/search_server.py"],
                "transport": "stdio"
        }
    })