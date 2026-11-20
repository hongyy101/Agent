# 策略表
CREATE TABLE IF NOT EXISTS tool_policy (
    id SERIAL PRIMARY KEY,
    tool_name TEXT NOT NULL,
    role TEXT NOT NULL,
    decision TEXT NOT NULL CHECK (decision IN ('allow', 'deny', 'require_approval')),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE (tool_name, role)
);
