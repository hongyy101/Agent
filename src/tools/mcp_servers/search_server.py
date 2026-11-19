import json

from mcp.server.fastmcp.server import FastMCP

mcp = FastMCP("SerchServer")

def _ok(data: dict) -> str:
    result = { "ok" : True,  "data" : data }
    return json.dumps(result,ensure_ascii=False)

def _error(code:str, message:str, retryable:bool)->str:

    result  = {
        "ok": False,
        "error": { 
            "code":code, 
            "message":message, 
            "retryable": retryable
        }
    }

    return json.dumps(result,ensure_ascii=False)

@mcp.tool()
def fake_search(query:str) -> str:
    '''搜索 LangGraph 相关文档。当用户询问 LangGraph 概念、用法或原理时使用。'''

    if not query or "langgrap" not in query.lower():
        return _error("UNSUPPORT_QUERY","该工具仅支持 LangGraph 相关查询",False)

    raw = {
        "query" : query,
        "results":[
            {
                "title" : "LangGraph 概念介绍",
                "snippet" : f"这是一个关于「{query}」的模拟搜索结果"
            }
        ],
        "total":1
    }

    return _ok(raw)

@mcp.tool()
def fake_weather(city:str) -> str:
    '''查询指定城市的实时天气。当用户询问任何城市或地区的天气、温度、下雨、晴天等气象信息时使用。参数 city 是城市名，如'北京'、'上海'。'''

    if not city or not city.strip():
        return _error("INVALID_ARGUMENT","城市名不能为空", False)

    if len(city) > 4:
        return _error("INVALID_ARGUMENT", "城市名太长", False)

    raw = {
        "city" : city,
        "condition":"晴",
        "temperature_c" : 25,
        "humidity_pct" : 60,
        "internal_station_id": "WS001",
        "data_source": "api_v2"
    }

    result = {
       k: v for k, v in raw.items() if not k.startswith("internal_") and k != "data_source"
    } 

    return _ok(result)  

if __name__ == "__main__":
    mcp.run(transport="stdio")