from mcp.server.fastmcp.server import FastMCP

mcp = FastMCP("SerchServer")

@mcp.tool()
def fake_search(query:str) -> str:
    '''搜索 LangGraph 相关文档。当用户询问 LangGraph 概念、用法或原理时使用。'''

    return f"这是一个关于「{query}」的模拟搜索结果"

@mcp.tool()
def fake_weather(city:str) -> str:
    '''查询指定城市的实时天气。当用户询问任何城市或地区的天气、温度、下雨、晴天等气象信息时使用。参数 city 是城市名，如'北京'、'上海'。'''

    return f"{city} 今天晴，25 度，湿度 60%"

if __name__ == "__main__":
    mcp.run(transport="stdio")