# Deep-Research

面向**技术知识研报**的多智能体深度研究系统（Deep Research Agent）。

输入一个调研问题，系统自动完成：**规划 → 检索取证（本地 RAG + 联网搜索）→ 带引用写作 → Critic 质量闸门**，并输出可追溯的 Markdown 研究报告。提供 CLI、FastAPI 网页（含历史记录与 Markdown 渲染），以及评测脚本与 MCP 工具封装（层次 A）。

> 垂直领域：Technical Research（Agent / RAG / MCP / 框架对比等）

---

## 功能特性

- **Planner**：DeepSeek 生成结构化研究计划（子问题 / 成功标准 / 步数预算）
- **Searcher**：本地 Chroma RAG + Tavily 联网搜索，统一为 `Evidence`
- **Writer**：固定报告模板 + 模型写作，关键结论带 `[evidence_id]` 引用
- **Critic**：规则检查（结构 / 假引用 / 摘要引用密度）；失败则补检并有限次重写
- **Web**：FastAPI + 左侧历史 / 右侧报告；报告支持 Markdown 渲染
- **Eval**：固定题集一键评测（`data/eval/`）
- **MCP（层次 A）**：将检索工具封装为 MCP Server，可用 Client 脚本自测
- **可落盘**：`outputs/reports/` 保存证据包 JSON 与报告 Markdown

---

## 系统架构

```text
用户问题
   │
   ▼
Planner (DeepSeek) ──► Plan(JSON)
   │
   ▼
Searcher ──► vector_search + Tavily web_search ──► Evidence[]
   │            （可选经 MCP Server 暴露同名能力）
   ▼
Writer ──► 带引用 Markdown 报告
   │
   ▼
Critic ──► 通过 / 补检重写（MAX_CRITIC_ROUNDS）
   │
   ▼
report_*.md + evidence_*.json + 历史记录
```

| 模块 | 范式 |
|------|------|
| Planner | Plan-and-Solve |
| Searcher | ReAct（工具观察后继续） |
| Critic | Reflection（规则版闸门） |
| Writer | 模板约束生成 |

更多说明见 [`ARCHITECTURE.md`](./ARCHITECTURE.md)。

---

## 环境要求

- Python 3.10+
- DeepSeek API（OpenAI 兼容）
- Tavily API（推荐；无密钥时可降级为仅本地 RAG）
- 依赖见 `requirements.txt`（另需 `openai`、`mcp` 等，按实际 import 安装）

---

## 快速开始

### 1) 虚拟环境与依赖

```powershell
cd D:\Deep-Research
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
pip install openai mcp
```

### 2) 配置环境变量

```powershell
copy .env.example .env
```

填写：

```env
LLM_API_KEY=你的DeepSeek密钥
LLM_BASE_URL=https://api.deepseek.com
LLM_MODEL=deepseek-v4-flash
SEARCH_API_KEY=你的Tavily密钥
SEARCH_PROVIDER=tavily
MAX_RESEARCH_STEPS=12
MAX_CRITIC_ROUNDS=2
```

**不要提交 `.env`。**

### 3) 构建本地知识库

```powershell
python scripts\ingest_kb.py
```

### 4) 启动网页（推荐演示）

```powershell
uvicorn deep_research.api.main:app --app-dir src --reload --host 127.0.0.1 --port 8000
```

- 页面：http://127.0.0.1:8000/
- API 文档：http://127.0.0.1:8000/docs

### 5) 命令行

```powershell
python src\deep_research\pipeline_m1.py
```

产物：

- `outputs/reports/report_*.md`
- `outputs/reports/evidence_*.json`

---

## Demo 与样例

固定演示题见 [`docs/demo_questions.md`](./docs/demo_questions.md)。

精选报告：

- [`docs/samples/demo1_mcp_vs_function_calling.md`](./docs/samples/demo1_mcp_vs_function_calling.md)
- [`docs/samples/demo2_react_vs_plan_and_solve.md`](./docs/samples/demo2_react_vs_plan_and_solve.md)
- [`docs/samples/demo3_why_critic.md`](./docs/samples/demo3_why_critic.md)

作品集说明：[`docs/portfolio.md`](./docs/portfolio.md)

建议 Demo 题：

1. MCP 和 Function Calling 有什么区别？各自适合什么场景？
2. ReAct 与 Plan-and-Solve 在开放研究任务上如何选择？
3. 为什么 Deep Research 需要 Critic？只靠 Writer 自检不够吗？

---

## 评测（Eval）

题集：`data/eval/questions.jsonl`  
脚本：`data/eval/runner.py`

```powershell
python data\eval\runner.py
```

> 注意：`runner.py` 位于 `data/eval/` 时，项目根目录请用 `Path(__file__).resolve().parents[2]`（不要用 `parents[3]`）。

输出（典型）：

- `outputs/eval/eval_results.json`
- `outputs/eval/eval_report.md`

可将汇总指标填入 `docs/portfolio.md` 量化表。

---

## MCP（层次 A）

将本地 RAG / Tavily 检索封装为 MCP 工具，便于协议化演示。当前 SDK 为 **mcp 2.0**，使用 `MCPServer`（不是旧文档里的 `FastMCP`）。

- Server：`src/deep_research/mcp/kb_server.py`
- Tools：`rag_search`、`tavily_search`
- Client 自测：`scripts/test_mcp_client.py`

```powershell
python scripts\test_mcp_client.py
```

成功时应能 `list_tools` 并调用工具返回 Evidence 列表。

说明：主研究流水线仍可直接调用 Python 工具函数；MCP 用于互操作与作品集叙事。接入 Searcher 主路径属于层次 B（可选）。

---

## 项目结构

```text
Deep-Research/
├── ARCHITECTURE.md
├── README.md
├── .env.example
├── requirements.txt
├── data/
│   ├── raw/                 # 本地语料
│   └── eval/                # 评测题集与 runner
├── docs/
│   ├── demo_questions.md
│   ├── portfolio.md
│   └── samples/             # 精选报告
├── knowledge_base/          # Chroma（通常 gitignore）
├── outputs/
│   ├── reports/
│   ├── history/
│   └── eval/
├── web/index.html
├── scripts/
│   ├── ingest_kb.py
│   └── test_mcp_client.py
└── src/deep_research/
    ├── api/main.py
    ├── agents/
    ├── tools/
    ├── mcp/kb_server.py
    ├── schemas.py
    ├── config.py
    ├── llm.py
    ├── history_store.py
    └── pipeline_m1.py
```

---

## 当前进度与局限

### 已完成

- 工程骨架、Schema、DeepSeek 接入
- 本地 RAG + Tavily 联网检索
- Planner / Writer / Critic 闭环
- FastAPI 网页、历史记录、报告 Markdown 渲染
- Demo 题与 `docs/samples` 精选报告
- 评测脚本（`data/eval`）
- MCP 层次 A（Server + Client 自测；需使用 mcp 2.0 的 `MCPServer`）

### 可继续增强

- 评测指标写入作品集并扩大题集
- MCP 层次 B：Searcher 主路径改为经 MCP Client 调用
- LangGraph 状态图编排
- `fetch_url` 深读网页正文
- 流式进度 / 更强可观测性
- 演示视频

---

## 求职一句话

> 独立实现 Deep Research Agent：基于结构化状态契约，完成本地 RAG + 联网检索、多智能体规划写作与 Critic 自动补检；提供 FastAPI 网页演示、历史回看、固定 Demo 样例、评测脚本，以及 MCP 工具协议封装（层次 A）。

---

## 许可证

MIT License. 详见 [`LICENSE`](./LICENSE)。

---

## 致谢

- [Hello-Agents](https://github.com/datawhalechina/hello-agents)（Datawhale）
- DeepSeek / Tavily / Chroma / FastAPI / MCP Python SDK