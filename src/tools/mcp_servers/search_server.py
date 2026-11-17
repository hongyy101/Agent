from mcp.server.fastmcp.server import FastMCP

mcp = FastMCP("SerchServer")

@mcp.tool()
def fake_search(query:str) -> str:
    '''搜索 LangGraph 相关文档。当用户询问 LangGraph 概念、用法或原理时使用。'''

    return f"这是一个关于「{query}」的模拟搜索结果"

@mcp.tool()
def fake_weather(query:str) -> str:
    '''搜索天气相关的问题。当用户询问某个城市或地区天气时使用。'''

    return f"这是一个关于「{query}」的搜索结果，用户询问某个城市或地区天气，当不明确位置时，可以使用IP地址去推断大体的地址"

if __name__ == "__main__":
    mcp.run(transport="stdio")