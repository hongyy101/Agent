# 用户信息 MCP Server
from mcp.server.fastmcp import FastMCP
import json
import sys
from pathlib import Path

# 当前文件在 src/tools/mcp_servers/，往上 3 层是项目根目录
PROJECT_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(PROJECT_ROOT))

from src.tools.schemas.user import UserOutput

mcp = FastMCP("UserServer", host="127.0.0.1", port=8002)

def _ok(data: dict) -> str:
    return json.dumps({"ok":True, "data": data}, ensure_ascii=False)

def _error(code:str, message:str, retryable:bool) -> str:
    return json.dumps({"ok": False, "error":{  "code":code, "message": message, "retryable":retryable}}, ensure_ascii=False)

@mcp.tool()
async def get_user_info(user_id:int) -> str:
    """根据用户ID查询。当需要确认用户身份、联系方式或账号状态时使用。"""

    if not user_id or user_id < 1:
        return _error("INVALID_ARGUMENT", "用户ID无效", False)

    raw = {
        "user_id": user_id,
        "user_name": "Hongyy",
        "email": "hongyy123@qq.com",
        "status": "active",
        "internal_field" : "this a internal field, that should be exclude from the result"
    }

    data = UserOutput(**raw)
    return _ok(data.model_dump())

if __name__ == "__main__":
    mcp.run(transport="streamable-http")