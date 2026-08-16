# LangGraph 与 AutoGen：编排思路对比（概述）

source: https://langchain-ai.github.io/langgraph/ ; https://microsoft.github.io/autogen/
citation: LangGraph 官方文档；Microsoft AutoGen 官方文档（公开页面）。本文为对比向原创概述。
tags: langgraph, autogen, orchestration
license_note: 基于官方公开文档的高层次归纳，不复制大段官方原文。

## 为什么要对比

求职与架构访谈常问：何时用图编排，何时用多 Agent 会话协作。二者都可做多智能体，但默认心智模型不同。

## LangGraph（概括）

- 更强调把流程建成**状态图**（节点与边）
- 适合：可画出来的控制流、显式状态、分支/循环/人工介入点
- 调试时“当前在哪个节点、状态是什么”通常更直观

## AutoGen（概括）

- 更强调多 Agent **会话式协作**（角色互相发消息推进任务）
- 适合：需要多角色讨论、工具代理协作的场景
- 工程重点常在对话策略、角色设定与工具代理组织

## 粗对比表

| 维度 | LangGraph | AutoGen |
|------|-----------|---------|
| 主隐喻 | 图 / 状态机 | 多角色对话 |
| 控制流 | 边与条件路由更显式 | 会话推进更灵活 |
| 可观测 | 节点状态清晰 | 依赖对话轨迹设计 |
| 典型问题 | 复杂工作流编排 | 多 Agent 协作任务 |

## 注意

具体产品能力在快速演进，选型应以当前官方文档与任务匹配度为准；面试应强调“问题结构决定编排”，避免背单一结论。

## 与本项目的关系

Deep-Research 可先顺序脚本跑通，再升级为状态图编排（LangGraph 或自研）。简历可写清演进路径。