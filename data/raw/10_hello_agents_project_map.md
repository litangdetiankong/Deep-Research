# Hello-Agents 与本项目的能力映射

source: https://github.com/datawhalechina/hello-agents
citation: Datawhale Hello-Agents 开源教程（项目介绍与章节导航，公开仓库）。
tags: hello-agents, curriculum, roadmap
license_note: 基于公开仓库介绍信息的学习映射笔记，不复制教程正文大段内容。

## Hello-Agents 强调什么

Hello-Agents 面向“AI Native Agent”构建，内容覆盖：

- 经典范式：ReAct、Plan-and-Solve、Reflection
- 低代码与主流框架实践
- 自研 Agent 框架思路
- 记忆与 RAG、上下文工程
- 通信协议（MCP 等）
- 评估与综合案例（含 DeepResearch）

## 映射到 Deep-Research 仓库

| 教程能力 | 本项目落点 |
|----------|------------|
| Plan-and-Solve | Planner + `Plan` Schema |
| ReAct | Searcher + tools |
| Reflection | Critic |
| RAG / Memory | `data/raw` → `knowledge_base` → `vector_search` |
| 上下文工程 | ResearchState 裁剪与预算 |
| MCP | 后期 `src/deep_research/mcp/` |
| 评估 | `data/eval` + eval runner |
| DeepResearch 案例 | 本仓库主线产品化 |

## 学习建议

先完成“本地检索 → 证据包”，再叠加 Planner/Writer/Critic，最后才是 MCP 与 Web。避免一上来同时引入所有子系统。