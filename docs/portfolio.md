# Deep-Research 作品集说明

> 项目名称：Deep-Research  
> 定位：技术知识研报方向的 Deep Research Agent  
> 仓库路径：`D:\Deep-Research`  
> 更新日期：2026-08-29

---

## 1. 一句话介绍

独立设计并实现一套多智能体深度研究系统：输入技术调研问题后，自动完成研究规划、本地知识库与联网检索、高分网页深读、带引用报告写作，并通过 Critic 质量闸门进行有限次补检重写；提供 FastAPI 网页（历史回看、步骤进度）、可开关的 MCP 主检索路径，以及可开关的 LangGraph 状态图编排。

---

## 2. 解决什么问题

普通大模型问答容易出现：

- 结论流畅但缺乏依据（幻觉）
- 过程不可追踪，难以复现与评测
- 检索、写作、质检耦合在一次对话里，难以工程化迭代

Deep-Research 将研究流程拆成可组合模块，用结构化状态（`ResearchState`）在 Agent 间传递，使「计划 / 证据 / 报告 / 重试」可落盘、可检查、可演示。

**适用场景：** Agent / RAG / MCP / 框架对比等技术知识研报（非荐股、非医疗诊断）。

---

## 3. 系统能力（当前版本）

| 能力 | 说明 |
|------|------|
| Planner | DeepSeek 生成 `Plan`（子问题、成功标准、步数预算） |
| Searcher | Chroma 本地 RAG + Tavily 联网 + Top-2 `fetch_url` 深读 |
| Writer | 固定报告模板 + 模型写作，关键结论绑定 `[evidence_id]` |
| Critic | 规则检查结构与引用；失败则补检索并重写（有轮次上限） |
| Web | FastAPI；提问、历史回看、Markdown 渲染、步骤进度（`/research/stream`） |
| MCP | 层次 A：Server/Client 自测；层次 B：`USE_MCP=1` 时主检索经 Client |
| LangGraph | `USE_LANGGRAPH=1` 时 CLI / API 走状态图；默认脚本流水线。评测不走图 |
| 产物 | `outputs/reports/report_*.md`、`evidence_*.json` |

端到端链路：

```text
问题 → Planner → Searcher(本地+网页+深读) → Writer → Critic(补检重写) → 报告/历史
```

---

## 4. 技术亮点（面试可讲）

1. **结构化状态契约**  
   使用 Pydantic 定义 `Plan` / `Evidence` / `Claim` / `ResearchState`，避免 Agent 间纯自然语言传话导致上下文失控。

2. **检索双通道 + 深读**  
   本地语料保证领域稳定覆盖；Tavily 补充公开网页；对分数最高的 2 个 URL 拉正文（失败则保留摘要，不中断）。

3. **防幻觉工程化**  
   Writer 强制引用格式；Critic 检查未知引用、章节完整性、结论摘要引用密度；证据不足时应暴露局限而非编造。

4. **可观测与可演示**  
   证据包与报告落盘；网页可回看历史，并在长任务中显示当前步骤。

5. **工具协议可切换**  
   同一套 `rag_search` / `tavily_search` / `fetch_url` 可直调或经 MCP Client（`USE_MCP`），演示默认直调以保证稳定。

6. **编排可切换**  
   默认顺序脚本；`USE_LANGGRAPH=1` 时用状态图显式建模 `write → critic → repair` 条件边。图只包已有函数，评测钉在旧路径上对照。

---

## 5. 我负责的工作

- 项目立项、目录与架构设计（对齐 Hello-Agents 范式）
- Schema / 配置 / LLM 封装
- 本地知识库建设与 ingest、vector_search
- Tavily 联网搜索、高分网页 `fetch_url` 深读与证据合并
- Planner / Searcher / Writer / Critic 实现与串联
- FastAPI 接口（含流式进度）、前端页面与历史记录
- MCP 层次 A/B（Server、Client 自测、主链路开关）
- LangGraph 状态图（`graph.py`、`repair_once`、`USE_LANGGRAPH` 接入 CLI / API）
- README 与作品集文档整理

---

## 6. 如何演示

### 方式 A：网页（推荐）

```powershell
cd D:\Deep-Research
.\.venv\Scripts\activate
uvicorn deep_research.api.main:app --app-dir src --reload --host 127.0.0.1 --port 8000
```

打开 [http://127.0.0.1:8000/](http://127.0.0.1:8000/)（建议 Ctrl+F5），输入 Demo 问题。状态栏会依次显示规划、检索、深读、写作、检查；完成后可点左侧历史回看。

### 方式 B：样例报告

见 `docs/demo_questions.md` 与 `docs/samples/`（将精选 `outputs/reports/report_*.md` 复制到 samples）。

### 建议 Demo 题

1. MCP 和 Function Calling 有什么区别？各自适合什么场景？  
2. ReAct 与 Plan-and-Solve 在开放研究任务上如何选择？  
3. 为什么 Deep Research 需要 Critic？只靠 Writer 自检不够吗？

---

## 7. 90 秒口述稿

我做的是一个技术知识方向的 Deep Research Agent。  
用户输入调研问题后，Planner 先拆解研究计划；Searcher 结合本地知识库和联网搜索收集证据；Writer 按模板生成带引用的研究报告；Critic 检查引用和结构，不通过就补检并有限次重写。  
和普通聊天相比，它有结构化状态、工具闭环、可落盘产物和网页演示，更能体现 Agent 工程能力。  
固定 3 题评测 Critic 通过率 100%、未知 evidence_id 率 0%，平均约 68 秒。检索上会深读高分网页；工具层封装为 MCP，编排可用 LangGraph 状态图，二者都用环境变量开关，评测走脚本路径以便对照。后续可补演示视频和 GitHub 推送。

---

## 8. 量化结果（2026-08-20 重跑）

来源：`outputs/eval/eval_report.md`（固定 3 题，与 Demo 对齐，`max_rounds=1`；本轮已启用 Top-2 `fetch_url` 深读）。

| 指标 | 结果 | 备注 |
|------|------|------|
| Demo 题成功率 | 3/3 | Critic 规则通过 |
| 平均证据条数 | 约 16.7 | q1=14，q2=17，q3=19 |
| Critic 首轮通过率 | 100% | 三题 `retry_count=0` |
| 平均耗时 | 67.65 秒 | q1=50.07，q2=68.49，q3=84.40；上一轮（未深读）为 54.48 秒 |
| 未知引用率 | 0.00% | 只统计带 `::` 的 evidence_id |

此前通过率为 0%，是因为报告中的 `[现有资料不足]` 被当成假引用。引用提取改为只认 `::` 后，未知 id 率仍为 0%，通过率升至 100%。接入深读后平均耗时上升属预期（多两次网页抓取）。面试应主动讲这次归因，而不是只报 100%。

---

## 9. 局限与下一步

**局限**

- 已有 3 题自动评测；题集偏小，尚未统计 token / 费用
- LangGraph 默认关闭（`USE_LANGGRAPH=0`）；评测不走图，图路径尚未纳入固定题集指标
- MCP 层次 B 默认关闭（`USE_MCP=0`）；Critic 补检仍走本地 RAG
- `fetch_url` 只深读 Top-2，且受站点反爬/超时影响，不保证每次都加长正文

**下一步**

1. 录制 3～5 分钟演示视频  
2. 扩大评测题集，补 token / 费用  
3. 本机推送 GitHub  

---

## 10. 简历条目（可直接改写）

> 独立实现 Deep Research 多智能体系统（Python）：完成 Planner/Searcher/Writer/Critic 闭环，集成 Chroma、Tavily 与高分网页深读，基于 Pydantic 状态契约保证引用可追溯；提供 FastAPI 网页（历史回看、步骤进度）；检索工具封装为 MCP Server（`USE_MCP`），编排可用 LangGraph 状态图（`USE_LANGGRAPH`），评测钉在脚本路径上对照。固定 3 题评测 Critic 通过率 100%，未知 evidence_id 率 0%，平均耗时约 68 秒。

---

## 11. 相关文档

- [README.md](../README.md)
- [ARCHITECTURE.md](../ARCHITECTURE.md)
- [demo_questions.md](./demo_questions.md)