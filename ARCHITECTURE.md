# Deep-Research 架构说明

> 项目路径：`D:\Deep-Research`  
> 垂直领域：技术知识研报（Technical Research）  
> 文档阶段：M0 立项骨架（架构已定义，Agent 尚未实现）  
> 版本：v0.1｜2026-08-15

---

## 1. 一句话定位

输入一个**技术调研类问题**，系统通过多智能体协作完成「规划 → 检索取证 → 交叉校验 → 结构化写作」，输出一份**带引用、可追溯**的 Markdown 深度研究报告，并同时留下可回放的运行轨迹（trace）。

本项目对标求职作品集中的 Deep Research Agent，而不是普通聊天机器人。

---

## 2. 目标与非目标

### 2.1 目标

- 在「技术知识研报」领域产出可用的研究报告（Agent / RAG / MCP / 框架对比等）
- 关键结论必须绑定证据（URL 或本地文档 ID）
- 多智能体职责清晰，过程可观测、可评测
- 工程上可本地一键运行（README + `.env`）

### 2.2 非目标（当前阶段明确不做）

- 不做金融荐股、医疗诊断、隐私数据抓取
- 不把 Agentic RL / 模型训练当主线
- M0～M2 不做复杂 Web 产品化与多租户
- 不追求一次性堆叠大量 Agent 角色

---

## 3. 总体架构

### 3.1 流水线

```text
用户问题
   │
   ▼
┌─────────────┐
│  Planner    │  拆解子问题、制定检索计划、设定停止条件
└──────┬──────┘
       │ Research Plan (JSON)
       ▼
┌─────────────┐     ┌──────────────────────┐
│  Searcher   │────▶│ Retriever / Tools    │
│ (可多实例)   │     │ web_search           │
└──────┬──────┘     │ fetch_url            │
       │            │ vector_search (RAG)  │
       │            └──────────────────────┘
       │ Evidence Pack (JSON)
       ▼
┌─────────────┐
│  Critic     │  检查无引用断言、证据冲突，决定通过或打回补检
└──────┬──────┘
       │ 通过 / 打回（受限轮次）
       ▼
┌─────────────┐
│  Writer     │  按模板写作，结论绑定 evidence_id
└──────┬──────┘
       ▼
研究报告 (Markdown) + 轨迹日志 (JSONL) + 指标 (metrics)
```

### 3.2 可选扩展角色（未实现）

- **Librarian（图书管理员）**：会话记忆压缩、目录索引、同会话增量研究  
- 计划在完整版（记忆 / 追问能力）再引入，避免早期过度设计

---

## 4. 角色职责

| 角色 | 输入 | 输出 | 核心职责 |
|------|------|------|----------|
| Planner | 用户原问题 | `plan` | 拆子问题、定义成功标准、限制最大步数 |
| Searcher | `plan` + 工具结果 | `evidence[]` | 按计划检索、去重合并、形成证据包 |
| Critic | `evidence[]` + 候选 `claims` / 草稿 | 通过或补检指令 | 防幻觉、查矛盾、控制质量闸门 |
| Writer | `plan` + Top 证据 + 通过的 claims | `report_md` | 结构化写作并落盘引用 |

设计原则：

1. **单角色单职责**，便于单独改进与评测  
2. **角色之间传结构化对象**，不靠大段自然语言传话  
3. **Critic 有否决权**：证据不足时允许「拒答 / 标注信息不足」，禁止编造

---

## 5. 范式映射（Hello-Agents）

| 模块 | 范式 | 选择理由 |
|------|------|----------|
| Planner | Plan-and-Solve | 开放研究需要先规划再执行 |
| Searcher | ReAct | 需要根据工具返回结果动态决定下一步 |
| Critic | Reflection | 对证据与中间结论做反思与修订 |
| Writer | 受限生成 + 模板 | 降低跑题、格式漂移和「无引用断言」 |

说明：早期可用「顺序脚本编排」跑通闭环；后续再用 LangGraph（或等价状态机）显式建模节点与边，便于讲解与扩展。

---

## 6. 核心数据对象（Schema 约定）

> 实现落点：`src/deep_research/schemas.py`（第 1 周完成）。  
> 此处先定义契约，保证各 Agent 说同一种「数据语言」。

### 6.1 顶层对象 `ResearchState`

```json
{
  "research_id": "uuid",
  "question": "用户原问题",
  "plan": {},
  "evidence": [],
  "claims": [],
  "report_md": "",
  "metrics": {}
}
```

### 6.2 `plan`

```json
{
  "sub_questions": ["子问题1", "子问题2"],
  "success_criteria": ["每条核心结论有引用", "覆盖对比维度X/Y"],
  "max_steps": 12
}
```

### 6.3 `evidence`（证据包条目）

```json
{
  "id": "e1",
  "source": "url_or_doc_id",
  "title": "来源标题",
  "snippet": "关键摘录",
  "retrieved_at": "ISO-8601",
  "score": 0.0
}
```

### 6.4 `claim`（可引用结论）

```json
{
  "text": "结论句",
  "evidence_ids": ["e1", "e3"],
  "confidence": 0.0
}
```

### 6.5 `metrics`

```json
{
  "latency_s": 0,
  "tokens": 0,
  "tool_calls": 0,
  "retry_count": 0
}
```

---

## 7. 记忆与上下文工程（原则）

| 层级 | 内容 | 策略 |
|------|------|------|
| 工作记忆 | 当前 plan、最近证据、待验证点 | 条数硬上限，超出则摘要 |
| 证据库 | Evidence Pack | Writer 只注入 Top-K 相关证据 |
| 会话记忆 | 追问历史（完整版） | 摘要 + 关键 claim 索引 |
| 长期记忆 | 跨会话领域笔记（可选） | 向量库按主题召回 |

硬规则：

1. 禁止把原始网页全文无限制塞进 Writer 上下文  
2. Searcher 每轮结束后做证据去重与合并  
3. Critic 主要审查 claims 与对应 evidence，不吞全量工具日志

---

## 8. 工具层设计

### 8.1 MVP 工具

| 工具 | 作用 |
|------|------|
| `web_search` | 关键词检索，返回候选 URL/摘要 |
| `fetch_url` | 抓取页面并抽取正文 |
| `vector_search` | 检索本地技术知识库（RAG） |

### 8.2 完整版（MCP 化）

将检索、读页、RAG 封装为 MCP Server，由 Agent Runtime 经 MCP Client 调用，便于演示「协议化工具接入」。

---

## 9. 质量闸门（防幻觉）

1. Writer 输出前：每条核心 claim 至少绑定 1 个 `evidence_id`  
2. Critic：发现无引用断言 → 打回；证据冲突 → 标记争议并降低置信度  
3. 报告模板强制分区：`结论 / 论证与证据 / 不确定与局限 / 参考来源`  
4. 对 URL 引用做可达性抽样检查（能做则做）  
5. 补检循环设置上限（如 `MAX_CRITIC_ROUNDS`），防止无限检索  

---

## 10. 目录与模块映射

```text
D:\Deep-Research\
├── ARCHITECTURE.md          # 本文件
├── README.md                # 项目说明与阶段状态
├── src/deep_research/
│   ├── config.py            # 配置与环境变量
│   ├── schemas.py           # 数据结构契约
│   ├── graph.py             # 编排（后续）
│   ├── agents/              # Planner/Searcher/Critic/Writer
│   ├── tools/               # search/fetch/rag
│   ├── memory/              # 工作记忆与存储
│   ├── mcp/                 # MCP（后期）
│   ├── eval/                # 评测（后期）
│   └── api/                 # Web API（后期）
├── data/                    # 原始文档与评测集
├── knowledge_base/          # 向量库落盘
└── outputs/
    ├── reports/             # 研究报告
    └── traces/              # JSONL 轨迹
```

---

## 11. 技术选型（当前约定）

| 层级 | 选择 | 说明 |
|------|------|------|
| 语言 | Python 3.10+ | 与主流 Agent 生态一致 |
| 配置 | `.env` + `.env.example` | 密钥不进 Git |
| 编排 | 先顺序闭环，后状态图/LangGraph | 先正确，再框架化 |
| LLM | OpenAI 兼容 API | 通过环境变量配置 |
| 向量库 | 后期 Chroma 等本地方案 | MVP 可先工具检索 |
| 日志 | JSONL traces | 保证可回放 |

---

## 12. 里程碑与当前状态

| 里程碑 | 标志 | 状态 |
|--------|------|------|
| M0 立项 | 仓库目录 + 架构骨架 | **进行中 / 架构已定** |
| M1 证据闭环 | CLI 产出证据包 JSON | 未开始 |
| M2 报告闭环 | 带引用 Markdown 报告 | 未开始 |
| A MVP | 可演示、可写简历 | 未开始 |
| M3 MCP + 编排 | 协议化工具 + 状态图 | 未开始 |
| M4 评测 | 指标与评测集 | 未开始 |
| B 完整作品 | Web + 评测 + 面试稿 | 未开始 |

---

## 13. 演示问题方向（领域锚定）

后续 Demo / 评测题围绕技术知识研报，例如：

1. ReAct 与 Plan-and-Solve 在开放研究任务上的适用边界  
2. MCP 与普通 Function Calling 的差异与适用场景  
3. 多智能体常见失败模式与缓解策略  
4. Deep Research 引用质量应如何评估  
5. 上下文工程中摘要与检索如何配合  

---

## 14. 修订记录

| 日期 | 变更 |
|------|------|
| 2026-08-15 | 初始化架构文档（M0） |