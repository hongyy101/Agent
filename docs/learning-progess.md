# Agent 工程学习进度追踪

> 周期：4 个月 | 每日投入：4 小时+ | 背景：18 年 .NET 后端，MS SQL 精通
> 原则：除 LLM API 外全部免费自托管 | 目标：产品级作品 + 面试叙事

## 总体进度

| 月份 | 主题 | 状态 | 完成周数 |
|------|------|------|---------|
| 第 1 月 | LangGraph 运行时底座 + Postgres 持久化 | ✅ 已完成 | 3/4 |
| 第 2 月 | MCP 工具层 + 确定性执行边界 | 🔄 进行中 | 2/4 |
| 第 3 月 | HITL + 容错控制 + 防幻觉 | ⬜ 未开始 | 0/4 |
| 第 4 月 | 可观测性 + 审计 + 求职作品打磨 | ⬜ 未开始 | 0/4 |

状态图例：⬜ 未开始 / 🔄 进行中 / ✅ 已完成 / ⚠️ 有阻塞

## 第 1 月：LangGraph 运行时底座与 Postgres 持久化

**学习目标**：不依赖 create_react_agent 黑盒，手写 StateGraph，理解状态流转与持久化。

| 周次 | 核心任务 | 状态 | 验收标准 | 完成日期 | 备注 |
|------|---------|------|---------|---------|------|
| 第1周 | Python 异步范式对齐 + LangGraph 核心概念 | ✅ | 能读懂官方异步示例；理解 StateGraph/Node/Edge/Checkpointer 职责边界 | 2026-11-16 | |
| 第2周 | 手写 ReAct 循环（不用 prebuilt） | ✅ | StateGraph 手动定义 agent/tools 节点，实现决策→执行→回传→再决策闭环 | 2026-11-16 | |
| 第3周 | Postgres Checkpointer 深度集成 | ✅ | ConnectionPool + PostgresSaver 持久化；理解 thread_id 与状态恢复；能画出 checkpoint 流转图 | 2026-11-17 | |
| 第4周 | 错误处理与状态恢复实验 | ⚠️ | 模拟进程中断后从 Postgres 恢复；验证子图不应带独立 checkpointer | 2026-11-18 | 已通过 checkpoint 流转图及数据库查询验证 |

### 第 1 月关键概念自查（每周末打勾）
- [✅] 能解释 StateGraph 中 Node 和 Edge 的区别
- [✅] 能说清 Checkpointer 存的是什么、不存什么
- [✅] 能画出一次 invoke 在 Postgres 中产生的 checkpoint 记录
- [✅] 能解释为什么子图不应带独立 checkpointer
- [✅] 能手写一个两节点图并 invoke 出结果

## 第 2 月：MCP 工具层与确定性执行边界

**学习目标**：把企业 API 复用为 Tool，建立不依赖 Prompt 的确定性安全边界。

| 周次 | 核心任务 | 状态 | 验收标准 | 完成日期 | 备注 |
|------|---------|------|---------|---------|------|
| 第5周 | FastMCP Server 开发（stdio） | ✅ | 2-3 个模拟 .NET API 封装为 MCP Tool；理解 docstring 对决策的影响 | 2026-11-20 | 完成 stdio 模式天气、搜索工具开发与调试 |
| 第6周 | streamable-http + MultiServerMCPClient | ✅ | HTTP 传输；多 Server 同时连接，模拟不同部门 API | 2026-11-25 | 实现了混合传输（stdio+http）、独立降级、权限检查、输入/输出契约、错误分类与重试机制探索 |
| 第7周 | 自写权限中间件（FastAPI + Postgres 策略表） | 🔄 | 工具调用前查策略表；拒绝时返回结构化错误；不用 0.x 小库 | | |
| 第8周 | 工具输入/输出契约 + 错误分类 | ⬜ | Pydantic 输入/输出模型；输出裁剪；错误码映射（可重试 vs 不可重试） | | |

### 第 2 月关键概念自查
- [✅] 能区分 MCP 架构中 Host / Client / Server 三者角色
- [✅] 能解释为什么权限判断必须在工具调用边界做，不能靠 Prompt
- [✅] 能说清 MCP Server 为什么不承载业务逻辑
- [✅] 能解释"输出裁剪"对 token 成本和防幻觉的双重意义

### 第 2 月扩展项（可选，不阻塞主线）
- [ ] `pgvector` + 文档切片，写 `knowledge_server.py` 作为额外 MCP Tool
- [ ] 切片策略：结构分块优先，512 token / 10-15% 重叠作为固定分块起点

## 第 3 月：HITL、容错控制与防幻觉

**学习目标**：把不可靠的模型关进可靠的工程边界。

| 周次 | 核心任务 | 状态 | 验收标准 | 完成日期 | 备注 |
|------|---------|------|---------|---------|------|
| 第9周 | LangGraph interrupt() + Postgres 审批状态 | ⬜ | 敏感工具触发中断；审批记录写 Postgres；Command(resume) 恢复 | | |
| 第10周 | 自写 FastAPI 审批页面（带外通道） | ⬜ | 极简 HTML 列出待审批调用；批准/拒绝/改参；Agent 无法伪造确认 | | |
| 第11周 | 超时 + 断路器 + 幂等 | ⬜ | asyncio.wait_for 超时；三态断路器按依赖隔离；写操作稳定幂等键 | | |
| 第12周 | 字段级验证器（防幻觉） | ⬜ | 回复中订单号/状态/金额与 Tool 原始 JSON 一致；不一致拒绝并带反馈重试 | | |

### 第 3 月关键概念自查
- [ ] 能解释为什么 HITL 审批必须走 Agent 无法伪造的带外通道
- [ ] 能画出断路器三态（closed/open/half-open）转换图
- [ ] 能说清哪些操作需要幂等键、哪些不需要
- [ ] 能解释字段级验证器与 Prompt 约束的区别

## 第 4 月：可观测性、审计与求职作品打磨

**学习目标**：让作品可展示、可讲述、可验证。

| 周次 | 核心任务 | 状态 | 验收标准 | 完成日期 | 备注 |
|------|---------|------|---------|---------|------|
| 第13周 | Langfuse 自托管集成 | ⬜ | 部署 Langfuse；trace 记录 LLM/工具耗时与 token；trace 图入 README | | |
| 第14周 | Postgres 审计日志表 | ⬜ | agent_audit_log 表（thread_id/tool/decision/operator/timestamp/latency）；与 Checkpointer 表分离 | | |
| 第15周 | README + 架构图 + 演示视频 | ⬜ | 架构图标注 Postgres 三角色；2 分钟演示：查询→审批→执行 | | |
| 第16周 | 面试叙事打磨 + 预设追问 | ⬜ | 3 分钟项目讲述；5 个预设追问的答案 | | |

### 面试准备自查
- [ ] 能 3 分钟讲完项目核心叙事（确定性边界 + 带外审批 + 断路器隔离 + Langfuse）
- [ ] 准备好"工具从 3 个变 1000 个怎么扩展"的答案
- [ ] 准备好"没有真实产线数据，验证器规则从哪来"的答案
- [ ] 准备好"为什么自写权限中间件不用现成库"的答案

## 阻塞与调整记录

| 日期 | 问题 | 处理方式 | 状态 |
|------|------|---------|------|
| 2026-11-17 | psycopg 找不到 libpq | psycopg[binary,pool] | ✅ |
| 2026-11-17 | Windows 上 ProactorEventLoop 和 psycopg 异步不兼容 | asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy()) | ✅ |
| 2026-11-17 | AsyncConnectionPool 构造时自动打开被弃用 | open=False + await pool.open(wait=True) | ✅ |
| 2026-11-17 | PostgresSaver 导入路径错误 | langgraph.checkpoint.postgres，不是 langchain_core.savers | ✅ |
| 2026-11-19 | MCP stdio 配置缺 args 导致 Connection closed | 配置里加 "args": ["脚本路径"]，command 用 sys.executable | ✅ |
| 2026-11-19 | _ok 里 "data": dict 笔误导致 JSON 序列化失败 | 改成 "data": data | ✅ |
| 2026-11-19 | tools_node 多次 append 导致同一 tool_call 产生多条 ToolMessage | 每个分支加 continue，确保每个 tool_call_id 只 append 一次 | ✅ |
| 2026-11-20 | None \| str 运算符误用 | 改成 dsn or os.getenv(...) | ✅ |
| 2026-11-22 | 单 Client 包所有 Server 导致一损俱损 | 改为每 Server 独立加载、独立降级 | ✅ |
| 2026-11-25 | 框架级 RetryPolicy 用于业务错误导致节点级并发污染 | 明确重试边界：RetryPolicy 用于基础设施故障，业务错误在 Tool 层按 for 循环隔离重试 | ✅ |

## 阶段性里程碑

- [✅] **M1（第 4 周末）**：手写 StateGraph + Postgres Checkpointer 跑通，进程中断可恢复
- [ ] **M2（第 8 周末）**：MCP 工具层 + 权限中间件跑通，拒绝路径可演示
- [ ] **M3（第 12 周末）**：HITL + 断路器 + 验证器跑通，敏感操作全流程可演示
- [ ] **M4（第 16 周末）**：Langfuse trace + 审计表 + 演示视频 + 面试叙事就绪