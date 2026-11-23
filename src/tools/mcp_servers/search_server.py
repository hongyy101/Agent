import json

from mcp.server.fastmcp.server import FastMCP
from schemas import WeatherOutput, SearchOutput, WeatherInput, SearchInput

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
def fake_search(params: SearchInput) -> str:
    '''搜索 LangGraph 相关文档。当用户询问 LangGraph 概念、用法或原理时使用。'''

    raw = {
        "query" : params.query,
        "results":[
            {
                "title" : "LangGraph 框架",
                "snippet" : f"这是一个关于「{params.query}」框架的模拟搜索结果"
            },
            {
                "title" : "LangGraph 概念介绍",
                "snippet" : f"这是一个关于「{params.query}」概念介绍的模拟搜索结果"
            },
            {
                "title" : "LangGraph 核心思想",
                "snippet" : f"这是一个关于「{params.query}」核心思想的模拟搜索结果"
            },
            {
                "title" : "LangGraph 基本指南",
                "snippet" : f"这是一个关于「{params.query}」基本指南的模拟搜索结果"
            },
            {
                "title" : "LangGraph 未来发展",
                "snippet" : f"这是一个关于「{params.query}」未来发展的模拟搜索结果"
            },
            {
                "title" : "LangGraph 有的没的",
                "snippet" : f"这是一个关于「{params.query}」有的没的的模拟搜索结果"
            }
        ],
        "total":6,
        "page": 1,
        "page_size": 10
    }

    searchOutput = SearchOutput(**raw)
    return _ok(searchOutput.model_dump())

@mcp.tool()
def fake_weather(params: WeatherInput) -> str:
    '''查询指定城市的实时天气。当用户询问任何城市或地区的天气、温度、下雨、晴天等气象信息时使用。参数 city 是城市名，如'北京'、'上海'。'''

    raw = {
        "city" : params.city,
        "condition":"晴",
        "temperature_c" : 25,
        "humidity_pct" : 60,
        "internal_station_id": "WS001",
        "data_source": "api_v2"
    }

    result = WeatherOutput(**raw)
    return _ok(result.model_dump())  

if __name__ == "__main__":
    mcp.run(transport="stdio")