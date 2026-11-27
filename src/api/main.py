from dotenv import load_dotenv
load_dotenv()

from contextlib import asynccontextmanager
from fastapi import FastAPI,Header,HTTPException
from pydantic import BaseModel
from langchain_core.messages import HumanMessage
from src.agent.checkpointer import get_checkpointer
from src.agent.graph import build_react_graph
import uuid

@asynccontextmanager
async def lifespan(app: FastAPI):
    global graph_instance
    check_pointer = await get_checkpointer()
    graph_instance = build_react_graph(checkpointer=check_pointer)
    print("[API] Agent 初始化完成！")
    yield  # 必须加 yield
    print("[API] 正在关闭应用...")

app = FastAPI(title="Agent App", lifespan=lifespan)

class ChatRequest(BaseModel):
    message:str
    thread_id:str = None

graph_instance = None



@app.post("/chat")
async def chat(request:ChatRequest, x_user_role:str = Header(default="user")):
    role = x_user_role
    if role not in ["user","admin","guest"]:
        raise HTTPException(status_code=403, detail="无效角色")

    thread_id = request.thread_id or str(uuid.uuid4())

    config ={
        "configurable": {
            "thread_id": thread_id,
            "role": role
        }
    }

    result = await graph_instance.ainvoke(
        {
            "messages":[HumanMessage(content=request.message)],"step_count": 0
        },
        config = config
    )

    return {
        "thread_id": thread_id,
        "role": role,
        "reply": result["messages"][-1].content
    }

@app.get("/")
def index()->str:
    return "hongyy"