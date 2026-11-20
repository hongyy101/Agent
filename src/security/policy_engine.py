# 查 Postgres 策略表，返回 allow/deny/approval
import os
import psycopg

class PolicyEngine:
    def __init__(self, dsn: str | None = None):
        self.dsn = dsn or os.getenv("POSTGRES_DSN")

        if not self.dsn:
            raise RuntimeError("POSTGRES_DSN 未设置，无法连接策略表")

    def get_decision(self, tool_name:str, role:str) -> str:
        with psycopg.connect(self.dsn) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT decision FROM tool_policy WHERE tool_name = %s AND role = %s",
                    (tool_name, role)
                )

                row = cur.fetchone()
                return row[0] if row else "deny"