# Deep-Research 作品集说明

> 项目名称：Deep-Research  
> 定位：技术知识研报方向的 Deep Research Agent  
> 仓库路径：`D:\Deep-Research`  
> 更新日期：2026-08-16

---

## 1. 一句话介绍

独立设计并实现一套多智能体深度研究系统：输入技术调研问题后，自动完成研究规划、本地知识库与联网检索取证、带引用报告写作，并通过 Critic 质量闸门进行有限次补检重写，最终产出可追溯的 Markdown 研究报告；同时提供 FastAPI 网页演示与历史回看。

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
| Searcher | Chroma 本地 RAG + Tavily 联网搜索，统一为 `Evidence` |
| Writer | 固定报告模板 + 模型写作，关键结论绑定 `[evidence_id]` |
| Critic | 规则检查结构与引用；失败则补检索并重写（有轮次上限） |
| Web | FastAPI + 前端；支持自定义提问、历史记录回看 |
| 产物 | `outputs/reports/report_*.md`、`evidence_*.json` |

端到端链路：

```text
问题 → Planner → Searcher(本地+网页) → Writer → Critic(补检重写) → 报告/历史
```

---

## 4. 技术亮点（面试可讲）

1. **结构化状态契约**  
   使用 Pydantic 定义 `Plan` / `Evidence` / `Claim` / `ResearchState`，避免 Agent 间纯自然语言传话导致上下文失控。

2. **检索双通道**  
   本地语料保证领域稳定覆盖；Tavily 补充最新公开网页证据；按 id/source 去重合并。

3. **防幻觉工程化**  
   Writer 强制引用格式；Critic 检查未知引用、章节完整性、结论摘要引用密度；证据不足时应暴露局限而非编造。

4. **可观测与可演示**  
   证据包与报告落盘；网页可复现提问与历史回看，适合作品集演示。

5. **从零工程落地**  
   含配置管理、知识库 ingest、CLI 编排、FastAPI 服务化，而不仅是 Notebook Demo。

---

## 5. 我负责的工作

- 项目立项、目录与架构设计（对齐 Hello-Agents 范式）
- Schema / 配置 / LLM 封装
- 本地知识库建设与 ingest、vector_search
- Tavily 联网搜索接入与证据合并
- Planner / Searcher / Writer / Critic 实现与串联
- FastAPI 接口、前端页面与历史记录
- README 与作品集文档整理

---

## 6. 如何演示

### 方式 A：网页（推荐）

```powershell
cd D:\Deep-Research
.\.venv\Scripts\activate
uvicorn deep_research.api.main:app --app-dir src --reload --host 127.0.0.1 --port 8000
```

打开 [http://127.0.0.1:8000/](http://127.0.0.1:8000/)，输入 Demo 问题并查看报告与历史。

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
目前主链路和 FastAPI 演示已经完成，后续计划补系统评测、MCP 工具协议和更强的可观测性。

---

## 8. 量化结果（待填）

> 跑完固定评测后，把真实数字填在这里。

| 指标 | 结果 | 备注 |
|------|------|------|
| Demo 题成功率 | 待测 | 3 题人工验收 |
| 平均证据条数 | 待测 | 本地+网页合并后 |
| Critic 首轮通过率 | 待测 | `final_passed` |
| 平均耗时 | 待测 | 端到端秒数 |
| 未知引用率 | 待测 | 越低越好 |

---

## 9. 局限与下一步

**局限**

- 尚无系统化自动评测脚本与基准集
- 编排仍为脚本流水线，未升级为 LangGraph 状态图
- 工具层尚未 MCP 化
- 网页报告渲染与长任务进度反馈仍可加强
- 联网结果多为搜索摘要，深读全文（fetch_url）可继续增强

**下一步**

1. 补齐 `docs/samples` 精选报告与演示视频  
2. 增加评测集与 `eval` 脚本（引用有效率/覆盖率/成本）  
3. 引入状态图编排与 MCP 工具协议  
4. 优化前端 Markdown 渲染与运行进度展示  

---

## 10. 简历条目（可直接改写）

> 独立实现 Deep Research 多智能体系统（Python）：完成 Planner/Searcher/Writer/Critic 闭环，集成 Chroma 本地 RAG 与 Tavily 联网检索，基于 Pydantic 状态契约保证引用可追溯；提供 FastAPI 网页演示与历史回看，支持技术知识研报场景下的带引用报告生成。

---

## 11. 相关文档

- [README.md](../README.md)
- [ARCHITECTURE.md](../ARCHITECTURE.md)
- [demo_questions.md](./demo_questions.md)