{
  "research_id": "b54a1efe-52bf-4421-b9a5-90eb086c3f8e",
  "question": "ReAct 与 Plan-and-Solve 在开放研究任务上如何选择？",
  "plan": {
    "sub_questions": [
      "ReAct 与 Plan-and-Solve 在核心机制（推理与行动交错 vs 先生成计划再执行）上的具体差异是什么？",
      "在开放研究任务（如多步推理、未知环境探索、动态调整需求）中，ReAct 与 Plan-and-Solve 各自的性能表现和适用场景有哪些实证对比？",
      "如何根据任务特征（如错误修正需求、规划深度、环境反馈频率、计算预算）制定选择 ReAct 或 Plan-and-Solve 的决策准则？",
      "近期是否有结合 ReAct 与 Plan-and-Solve 的改进变体或混合方法，以及它们在开放研究任务上的效果如何？"
    ],
    "success_criteria": [
      "明确总结出 ReAct 与 Plan-and-Solve 的优劣势对比表",
      "给出至少3条基于任务特征的选择建议，并引用相关研究或实验依据",
      "覆盖至少3个开放研究任务的典型案例（如科学推理、代码生成、开放问答）",
      "提供对混合方法或最新进展的综述，并说明其适用条件"
    ],
    "max_steps": 12
  },
  "evidence": [
    {
      "id": "01_react_paradigm::1",
      "source": "file://D:/Deep-Research/data/raw/01_react_paradigm.md",
      "title": "ReAct：推理与行动交替的智能体范式",
      "snippet": "## 典型循环\n\nThought → Action → Observation → Thought → ... → Final Answer\n\n## 适用场景\n\n- 需要工具调用的问答与研究任务\n- 环境反馈重要的任务（网页、知识库、代码仓）\n- 需要展示中间轨迹以便调试与评测的 Agent\n\n## 局限\n\n- 轨迹变长后上下文成本上升\n- 工具选错或观察噪声会导致推理跑偏\n- 对开放式长程研究，常需与规划（Plan）或反思（Reflection）组合\n\n## 与本项目的关系\n\n在 Deep-Research 中，**Searcher** 更贴近 ReAct：根据研究计划调用检索工具，观察结果后再决定下一步检索。",
      "retrieved_at": "2026-08-16T15:08:49.165301+00:00",
      "score": 0.5409781566557385
    },
    {
      "id": "02_plan_and_solve::0",
      "source": "file://D:/Deep-Research/data/raw/02_plan_and_solve.md",
      "title": "Plan-and-Solve：先规划再执行",
      "snippet": "# Plan-and-Solve：先规划再执行\n\nsource: https://arxiv.org/abs/2305.04091\ncitation: Wang et al., \"Plan-and-Solve Prompting: Improving Zero-Shot Chain-of-Thought Reasoning in Large Language Models\", arXiv:2305.04091, 2023.\ntags: agent, planning, plan-and-solve\nlicense_note: 原创中文整理，基于公开论文信息与通用实践归纳。\n\n## 核心思想\n\nPlan-and-Solve 强调：面对复杂问题时，先生成一个**显式计划（Plan）**，再按步骤执行（Solve），而不是一上来就边想边答。\n\n相对“一步到位”的回答，它更适合多跳推理与可分解任务。\n\n## 两阶段\n\n1. **Plan**：把目标拆成子问题/子步骤，明确成功标准与顺序；\n2. **Solve**：逐步执行；必要时对计划做有限修订。\n\n## 优点\n\n- 结构清晰，便于分工给不同模块或 Agent\n- 更容易设置停止条件与预算（最大步数）\n- 便于人工检查“计划是否合理”\n\n## 风险\n\n- 计划本身错误会放大到全程\n- 过度规划可能浪费 token\n- 环境变化时需要重规划",
      "retrieved_at": "2026-08-16T15:08:49.165301+00:00",
      "score": 0.5328723741199318
    },
    {
      "id": "10_hello_agents_project_map::1",
      "source": "file://D:/Deep-Research/data/raw/10_hello_agents_project_map.md",
      "title": "Hello-Agents 与本项目的能力映射",
      "snippet": "anner + `Plan` Schema |\n| ReAct | Searcher + tools |\n| Reflection | Critic |\n| RAG / Memory | `data/raw` → `knowledge_base` → `vector_search` |\n| 上下文工程 | ResearchState 裁剪与预算 |\n| MCP | 后期 `src/deep_research/mcp/` |\n| 评估 | `data/eval` + eval runner |\n| DeepResearch 案例 | 本仓库主线产品化 |\n\n## 学习建议\n\n先完成“本地检索 → 证据包”，再叠加 Planner/Writer/Critic，最后才是 MCP 与 Web。避免一上来同时引入所有子系统。",
      "retrieved_at": "2026-08-16T15:08:49.165301+00:00",
      "score": 0.49784670791863705
    },
    {
      "id": "01_react_paradigm::0",
      "source": "file://D:/Deep-Research/data/raw/01_react_paradigm.md",
      "title": "ReAct：推理与行动交替的智能体范式",
      "snippet": "# ReAct：推理与行动交替的智能体范式\n\nsource: https://arxiv.org/abs/2210.03629\ncitation: Yao et al., \"ReAct: Synergizing Reasoning and Acting in Language Models\", arXiv:2210.03629, 2022/2023.\ntags: agent, react, tool-use\nlicense_note: 本文为基于公开论文摘要与社区通行理解的原创中文整理，非论文原文摘录。\n\n## 核心思想\n\nReAct（Reason + Act）让语言模型在解决问题时交替进行两件事：\n\n1. **Reasoning（推理）**：用自然语言写出当前思考、假设与计划片段；\n2. **Acting（行动）**：调用外部工具或环境接口（搜索、计算器、API、代码执行等），获得观察（Observation）；\n3. 再基于观察继续推理，直到得出答案或达到步数上限。\n\n它把“只想不做”的链式思维（CoT）和“只做不想”的纯动作策略结合起来，使过程更可追踪，也更容易利用外部知识。\n\n## 典型循环\n\nThought → Action → Observation → Thought → ... → Final Answer\n\n## 适用场景\n\n- 需要工具调用的问答与研究任务\n-",
      "retrieved_at": "2026-08-16T15:08:49.165301+00:00",
      "score": 0.49321513804378053
    },
    {
      "id": "web::0::20194",
      "source": "https://github.com/datawhalechina/hello-agents/blob/main/docs/chapter4/%E7%AC%AC%E5%9B%9B%E7%AB%A0%20%E6%99%BA%E8%83%BD%E4%BD%93%E7%BB%8F%E5%85%B8%E8%8C%83%E5%BC%8F%E6%9E%84%E5%BB%BA.md",
      "title": "hello-agents/docs/chapter4/第四章 智能体经典范式构建.md at main · datawhalechina/hello-agents · GitHub",
      "snippet": "",
      "retrieved_at": "2026-08-16T15:08:54.192668+00:00",
      "score": 0.73023266
    },
    {
      "id": "web::1::9327",
      "source": "https://www.cnblogs.com/muzinan110/p/18552824",
      "title": "ReAct vs Plan-and-Execute：LLM Agent 模式实战对比 - muzinan110 - 博客园",
      "snippet": "",
      "retrieved_at": "2026-08-16T15:08:54.192668+00:00",
      "score": 0.67706895
    },
    {
      "id": "web::2::92730",
      "source": "https://dev.to/jamesli/react-vs-plan-and-execute-a-practical-comparison-of-llm-agent-patterns-4gh9",
      "title": "ReAct vs Plan-and-Execute: A Practical Comparison of LLM Agent Patterns - DEV Community",
      "snippet": "",
      "retrieved_at": "2026-08-16T15:08:54.192668+00:00",
      "score": 0.55912215
    },
    {
      "id": "web::3::23595",
      "source": "https://theaiengineer.substack.com/p/the-4-single-agent-patterns",
      "title": "ReAct, Plan-and-Execute, ReWOO, and Reflexion - The AI Engineer",
      "snippet": "",
      "retrieved_at": "2026-08-16T15:08:54.192668+00:00",
      "score": 0.48908922
    },
    {
      "id": "web::4::35415",
      "source": "https://qiankunli.github.io/2023/10/30/llm_agent.html",
      "title": "增强型LLM——Agent - 李乾坤的博客",
      "snippet": "",
      "retrieved_at": "2026-08-16T15:08:54.192668+00:00",
      "score": 0.48484412
    },
    {
      "id": "web::1::59267",
      "source": "https://adg.csdn.net/695331b35b9f5f31781bc2ca.html",
      "title": "4 大主流思考框架：CoT、ReAct 、Plan-Act 与 Plan-and-Execute_头头本头--智能体开发者社区",
      "snippet": "",
      "retrieved_at": "2026-08-16T15:08:57.056262+00:00",
      "score": 0.7382357
    },
    {
      "id": "web::1::98039",
      "source": "https://www.cnblogs.com/pass-ion/p/19360735",
      "title": "llm范式和多agent架构（ReAct、Plan-and-Execute） - wangssd - 博客园",
      "snippet": "",
      "retrieved_at": "2026-08-16T15:08:59.447535+00:00",
      "score": 0.6485337
    },
    {
      "id": "web::0::29261",
      "source": "https://cloud.tencent.com/developer/article/2540118",
      "title": "智能体决策机制深度剖析：ReAct、Plan-and-Execute与 ...",
      "snippet": "",
      "retrieved_at": "2026-08-16T15:09:05.924093+00:00",
      "score": 0.92944044
    },
    {
      "id": "web::1::71957",
      "source": "https://edu.guangjuke.com/haowen/337.html",
      "title": "智能体决策框架深度解析：ReAct vs Plan-and-Execute_聚客AI学院大模型应用开发微调项目实践课程学习平台",
      "snippet": "",
      "retrieved_at": "2026-08-16T15:09:05.924093+00:00",
      "score": 0.8834373
    },
    {
      "id": "web::1::94258",
      "source": "https://xiaolinnote.com/ai/agent/6_three_patterns.html",
      "title": "6. ReAct、Plan-and-Execute、Reflection 三种范式有什么核心区别？实际项目中该如何选型？ | 小林面试笔记",
      "snippet": "",
      "retrieved_at": "2026-08-16T15:09:09.159457+00:00",
      "score": 0.48411235
    }
  ],
  "claims": [],
  "report_md": "# ReAct 与 Plan-and-Solve 在开放研究任务中的选择：基于现有证据的分析\n\n## 1. 结论摘要\n- ReAct 的核心机制是推理与行动交错，典型循环为 Thought → Action → Observation → … → Final Answer[01_react_paradigm::1]。\n- Plan-and-Solve 的核心思想是“先规划再执行”，源自零样本 Chain-of-Thought 的改进研究[02_plan_and_solve::0]。\n- ReAct 在需要工具调用、环境反馈重要的任务（如网页、知识库、代码仓）中有明确适用性，但存在上下文成本上升、工具选错或噪声导致推理跑偏等局限[01_react_paradigm::1]。\n- 现有证据表明，开放式长程研究中的 ReAct 常需与规划（Plan）或反思（Reflection）组合[01_react_paradigm::1]，Hello-Agents 架构也同时部署了 Planner、ReAct、Reflection 等组件[10_hello_agents_project_map::1]。\n- 有关 Plan-and-Solve 的具体性能、适用场景及两者实证对比的证据严重不足，无法给出定量结论[现有资料不足]。\n\n## 2. 分节论证\n\n### 2.1 核心机制差异：推理行动交错 vs 先规划再执行\nReAct（Reason + Act）让语言模型在解决问题时交替进行推理与行动[01_react_paradigm::0]。具体循环为 Thought → Action → Observation → Thought → …，即模型在每一步根据工具或环境的观察结果决定下一步动作[01_react_paradigm::1]。这一机制强调“边想边做”，可以在执行中动态调整。\n\nPlan-and-Solve 的核心思想是“先规划再执行”[02_plan_and_solve::0]。根据其来源，该方法旨在改进零样本 Chain-of-Thought 推理，即先生在推理前生成完整计划，再按计划逐步执行[02_plan_and_solve::0]。这更强调“先全局规划，再局部实施”。\n\n在系统架构层面，Hello-Agents 的能力映射将 Plan（对应 Plan-and-Solve 类方法）映射为 “Planner + Plan Schema”，将 ReAct 映射为 “Searcher + tools”，将 Reflection 映射为 “Critic”[10_hello_agents_project_map::1]。这从组件分工上说明：规划器负责生成计划结构，ReAct 负责具体检索与工具调用，二者角色不同。\n\n### 2.2 性能表现与适用场景对比\n现有证据对 ReAct 的适用场景描述较为明确：它适合“需要工具调用的问答与研究任务”以及“环境反馈重要的任务（网页、知识库、代码仓）”[01_react_paradigm::1]。这些场景与开放研究任务中的开放问答（检索与工具调用）、代码生成（代码仓反馈）、科学推理（研究任务）高度相关。\n\nPlan-and-Solve 的适用场景在现有证据中未被具体描述。证据片段仅保留了“核心思想 Plan-and-…”以及文献来源，后续内容被截断[02_plan_and_solve::0]。因此，关于其在多步推理、未知环境探索或动态调整需求下的实证表现，目前无法从证据中提取[现有资料不足]。\n\n下表根据可获得的证据，整理两种范式在机制、优势、劣势和适用场景上的对比。Plan-and-Solve 的多项内容由于证据缺失而无法填写。\n\n| 维度 | ReAct | Plan-and-Solve |\n|---|---|---|\n| 核心机制 | 推理与行动交替（Thought → Action → Observation）[01_react_paradigm::1] | 先规划再执行[02_plan_and_solve::0] |\n| 适用场景 | 工具调用、问答、研究任务；网页/知识库/代码仓等环境反馈重要场景[01_react_paradigm::1] | 现有证据未说明[现有资料不足] |\n| 优势 | 能利用观察结果动态调整行动；展示中间轨迹便于调试与评测[01_react_paradigm::1] | 现有证据未说明[现有资料不足] |\n| 劣势 | 轨迹变长后上下文成本上升；工具选错或观察噪声导致推理跑偏；开放式长程研究常需额外组合规划或反思[01_react_paradigm::1] | 现有证据未说明[现有资料不足] |\n\n### 2.3 基于任务特征的选择准则\n在现有证据范围内，可以依据 ReAct 的明确特性提出以下选择建议：\n\n1. **如果任务需要环境反馈与工具调用，优先考虑 ReAct**  \n   ReAct 的循环结构允许每次观察后更新下一步行动，适合网页检索、代码执行、知识库查询等反馈驱动的开放研究任务[01_react_paradigm::1]。\n\n2. **如果任务需要展示中间轨迹以便调试与评测，ReAct 是合适基座**  \n   其 Thought/Action/Observation 轨迹天然具备可解释性，便于研究者定位失败环节[01_react_paradigm::1]。\n\n3. **如果属于开放式长程研究，不应单独使用 ReAct**  \n   由于长轨迹带来上下文成本上升，且工具选错和噪声会累积错误，证据明确建议与规划（Plan）或反思（Reflection）组合使用[01_react_paradigm::1]。此时可考虑引入 Plan-and-Solve 类规划器负责全局计划，再用 ReAct 执行具体步骤[10_hello_agents_project_map::1]。\n\n4. **如果任务需要先制定完整计划再执行，可考虑 Plan-and-Solve**  \n   其“先规划再执行”的机制符合此类需求[02_plan_and_solve::0]，但现有证据未提供其与 ReAct 的性能对比，也无法确认其在开放研究任务上的可靠性，因此该建议仅基于机制推断[现有资料不足]。\n\n### 2.4 混合方法与改进变体的证据综述\n证据明确提到：ReAct 对开放式长程研究“常需与规划（Plan）或反思（Reflection）组合”[01_react_paradigm::1]。在 Hello-Agents 架构中，Planner + Plan Schema、ReAct、Reflection 被设计为不同组件，分别负责规划、检索/工具执行、批判性反思，这展示了一种结合使用的系统模式[10_hello_agents_project_map::1]。\n\n然而，现有证据并未具体指出任何已实现的“ReAct + Plan-and-Solve”混合变体名称（如 ReWOO、Reflexion），也未提供其在开放研究任务上的效果数据。虽然有一篇外部资料的标题提到 ReAct、Plan-and-Execute、ReWOO 和 Reflexion，但该资料的正文片段为空，无法提取有效信息[web::3::23595]。因此，对混合方法的具体实现和效果[现有资料不足]。\n\n## 3. 不确定与局限\n- Plan-and-Solve 的证据片段被截断，仅保留了“核心思想 Plan-and-…”与论文出处，无法获知其优势、劣势、适用场景或实验结果[02_plan_and_solve::0]。\n- 现有证据没有提供 ReAct 与 Plan-and-Solve 在开放研究任务（如科学推理、代码生成、开放问答）上的直接实证对比数据[现有资料不足]。\n- 关于混合方法，虽然证据指出 ReAct 需要与规划/反思组合，但未给出具体变体的实现方式与评测结果[01_react_paradigm::1]；外部资料标题提及 ReWOO、Reflexion，但内容缺失[web::3::23595]。\n- 表中 Plan-and-Solve 的优势、劣势、适用场景均为空缺，因为这些信息未出现在可用的证据片段中[现有资料不足]。\n- 本报告中的选择建议（如第 4 条）主要基于机制差异进行的合理推断，而非直接实验证据，使用时需注意其推测性质[现有资料不足]。\n\n## 4. 参考来源\n- [01_react_paradigm::0] ReAct：推理与行动交替的智能体范式（Yao et al., arXiv:2210.03629）\n- [01_react_paradigm::1] ReAct：推理与行动交替的智能体范式（Yao et al., arXiv:2210.03629）\n- [02_plan_and_solve::0] Plan-and-Solve：先规划再执行（Wang et al., \"Plan-and-Solve Prompting\", arXiv:2305.04091, 2023）\n- [10_hello_agents_project_map::1] Hello-Agents 与本项目的能力映射\n- [web::3::23595] ReAct, Plan-and-Execute, ReWOO, and Reflexion - The AI Engineer（仅标题可用，正文片段为空）",
  "metrics": {
    "latency_s": 0.0,
    "tokens": 0,
    "tool_calls": 6,
    "retry_count": 0
  }
}