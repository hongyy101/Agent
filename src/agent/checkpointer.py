# PostgresSaver + ConnectionPool 初始化
import os

from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from psycopg_pool import AsyncConnectionPool

_pool = None
_checkpointer = None

async def get_checkpointer(): 

    global _checkpointer, _pool
    
    if _checkpointer is None:
        # 初始化 ConnectionPool
        if _pool is None:
            _pool = AsyncConnectionPool(
                os.getenv("POSTGRES_DSN"),
                max_size=5,
                open=False,
                kwargs={"autocommit": True, "prepare_threshold": 0},
            )

        await _pool.open(wait=True)   # 关键：wait=True
        # 初始化 PostgresSaver
        _checkpointer = AsyncPostgresSaver(_pool)
        await _checkpointer.setup()
    return _checkpointer