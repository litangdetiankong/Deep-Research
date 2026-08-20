# Deep-Research

面向**技术知识研报**的多智能体深度研究系统（Deep Research Agent）。

输入一个调研问题，系统自动完成：**规划 → 检索取证（本地 RAG + 联网搜索 + 高分网页深读）→ 带引用写作 → Critic 质量闸门**，并输出可追溯的 Markdown 研究报告。提供 CLI、FastAPI 网页（历史、Markdown 渲染、步骤进度），以及评测脚本与 MCP 工具封装（层次 A 自测，层次 B 可开关接入主检索）。

> 垂直领域：Technical Research（Agent / RAG / MCP / 框架对比等）

---

## 功能特性

- **Planner**：DeepSeek 生成结构化研究计划（子问题 / 成功标准 / 步数预算）
- **Searcher**：本地 Chroma RAG + Tavily 联网搜索，对最高分 2 个网页 `fetch_url` 深读正文
- **Writer**：固定报告模板 + 模型写作，关键结论带 `[evidence_id]` 引用
- **Critic**：规则检查（结构 / 假引用 / 摘要引用密度）；失败则补检并有限次重写
- **Web**：FastAPI + 左侧历史 / 右侧报告；Markdown 渲染；`POST /research/stream` 显示当前步骤
- **Eval**：固定题集一键评测（题集 `data/eval/`，脚本 `src/deep_research/eval/runner.py`）
- **MCP**：层次 A 为 Server/Client 自测；层次 B 可通过 `.env` 中 `USE_MCP=1` 让主检索经 MCP Client 调用
- **可落盘**：`outputs/reports/` 保存证据包 JSON 与报告 Markdown
- **进度**：网页走 `POST /research/stream`，状态栏显示当前步骤

---

## 系统架构

```text
用户问题
   │
   ▼
Planner (DeepSeek) ──► Plan(JSON)
   │
   ▼
Searcher ──► vector_search + Tavily + fetch_url（Top-2）──► Evidence[]
   │            （USE_MCP=1 时经 MCP Client 调用同名工具）
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
USE_MCP=0
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

- 页面：http://127.0.0.1:8000/（强制刷新后，状态栏会显示「规划 / 检索 / 深读 / 写作 / 检查」）
- API 文档：http://127.0.0.1:8000/docs
- 同步接口：`POST /research`（评测仍走这条）
- 进度接口：`POST /research/stream`（网页使用）

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
脚本：`src/deep_research/eval/runner.py`

```powershell
python src\deep_research\eval\runner.py
```

脚本位于 `src/deep_research/eval/`：`parents[2]` 是 `src`（用于 import），`parents[3]` 是项目根（用于读题集、写 `outputs/eval`）。不要再按 `data/eval/runner.py` 的路径去改 `parents`。

输出：

- `outputs/eval/eval_results.json`
- `outputs/eval/eval_report.md`

最新一轮（2026-08-20 重跑，含 `fetch_url` 深读）：`critic_pass_rate=100%`，`unknown_id_citation_rate=0%`，`avg_latency_s=67.65`。汇总见 [`docs/portfolio.md`](./docs/portfolio.md)。

---

## MCP（层次 A / B）

将本地 RAG / Tavily / `fetch_url` 封装为 MCP 工具。SDK 为 **mcp 2.0**，使用 `MCPServer`（不是旧文档里的 `FastMCP`）。

- Server：`src/deep_research/mcp/kb_server.py`
- Tools：`rag_search`、`tavily_search`、`fetch_url`
- Client 自测：`scripts/test_mcp_client.py`
- 层次 B 桥接：`src/deep_research/tools/mcp_bridge.py`

```powershell
python scripts\test_mcp_client.py
```

`.env` 中 `USE_MCP=0`（默认）：主链路直接调用 Python 函数，演示更稳。  
`USE_MCP=1` 时 `run_plan_and_search` 经 MCP Client 做检索与深读（改完需重启 uvicorn）。Critic 补检仍走本地 `vector_search`。

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
│   └── eval/                # 评测题集 questions.jsonl
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
    ├── tools/rag.py
    ├── tools/search.py
    ├── tools/fetch.py
    ├── tools/mcp_bridge.py
    ├── mcp/kb_server.py
    ├── eval/runner.py
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
- 评测脚本（`src/deep_research/eval/runner.py` + `data/eval/questions.jsonl`）；2026-08-20 三题 Critic 通过率 100%
- MCP 层次 A（Server + Client 自测，含 `fetch_url` 工具）
- MCP 层次 B（`USE_MCP=1` 时主检索经 Client；默认 `0` 直调函数。Critic 补检仍走本地 RAG）
- `fetch_url` 深读分数最高的 2 个网页，失败不中断主流程
- 网页步骤进度（`/research/stream`）

### 可继续增强

- 扩大评测题集，补 token / 费用
- LangGraph 状态图编排
- 演示视频与 GitHub 推送
- token / 耗时写入 `Metrics`；Critic 补检也可走 MCP

---

## 求职一句话

> 独立实现 Deep Research Agent：基于结构化状态契约，完成本地 RAG + 联网检索与高分网页深读、多智能体规划写作与 Critic 自动补检；提供 FastAPI 网页（历史回看、步骤进度）、固定 Demo 与评测脚本（3 题 Critic 通过率 100%，未知 evidence_id 率 0%）；检索工具封装为 MCP Server，主链路可用 `USE_MCP` 切换是否经 Client 调用。

---

## 许可证

MIT License. 详见 [`LICENSE`](./LICENSE)。

---

## 致谢

- [Hello-Agents](https://github.com/datawhalechina/hello-agents)（Datawhale）
- DeepSeek / Tavily / Chroma / FastAPI / MCP Python SDK