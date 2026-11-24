import json

from mcp.server.fastmcp.server import FastMCP
from schemas import WeatherOutput, WeatherInput
from pydantic import ValidationError

mcp = FastMCP("WeatherServer", host="127.0.0.1", port=8001)

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
def fake_weather_http(params:WeatherInput) -> str:
    '''通过http外部API查询指定城市的实时天气。当用户询问任何城市或地区的天气、温度、下雨、晴天等气象信息时使用。参数 city 是城市名，如'北京'、'上海'。'''

    if params.city == "故障市":
        return _error("SERVICE_UNAVAILABLE", "当前市的服务故障，请稍候再试！", True)
    
    raw = {
        "city" : params.city,
        "condition":"晴",
        "temperature_c" : 22,
        "humidity_pct" : 66,
        "internal_station_id": "WS001",
        "data_source": "api_v2"
    }

    result = WeatherOutput(**raw)
    return _ok(result.model_dump())  

if __name__ == "__main__":
    mcp.run(transport="streamable-http")