{
  "research_id": "7b7f5162-1a21-4e05-8d7e-9e0882a6d9fa",
  "question": "MCP 和 Function Calling 有什么区别？各自适合什么场景？",
  "plan": {
    "sub_questions": [
      "MCP (Model Context Protocol) 的核心架构、设计目标和标准协议实现是什么？它与传统的Function Calling在技术机制上有哪些根本性差异？",
      "Function Calling（如OpenAI GPT、Claude等）的标准调用流程、函数描述格式和工具调用限制是什么？其优势与局限在哪里？",
      "MCP和Function Calling各自适用的典型场景有哪些？例如多Agent协作、动态工具发现、企业级集成等场景下如何选择？",
      "在实际项目中，MCP与Function Calling是否可以互补或共存？有没有主流的框架或平台对两者做了集成与对比？"
    ],
    "success_criteria": [
      "清晰阐述MCP和Function Calling在技术实现上的本质区别（如协议层 vs API层，动态发现 vs 静态注册）",
      "列出适用于不同业务场景的选型建议，并给出具体案例或数据支撑",
      "对比两者在性能、灵活性、扩展性、生态支持等方面的优劣，并说明是否可共存或替代",
      "引用至少3个权威来源（如官方文档、技术博客、论文）作为依据"
    ],
    "max_steps": 12
  },
  "evidence": [
    {
      "id": "04_mcp_overview::0",
      "source": "file://D:/Deep-Research/data/raw/04_mcp_overview.md",
      "title": "MCP（Model Context Protocol）概览",
      "snippet": "# MCP（Model Context Protocol）概览\n\nsource: https://modelcontextprotocol.io/introduction\ncitation: Anthropic / MCP 社区, Model Context Protocol 官方文档（Introduction）.\ntags: mcp, tools, protocol\nlicense_note: 基于官方公开介绍页面的原创中文归纳，非文档逐字翻译拷贝。\n\n## 一句话理解\n\nMCP 是一种开放标准，用来把 AI 应用（客户端）与外部系统（数据源、工具、工作流）以统一方式连接起来。官方常用类比：**像 AI 应用的 USB-C 接口**。\n\n## 能做什么\n\n- 让 Agent 连接文件、数据库、搜索、日历等外部能力\n- 让开发者把工具封装成 MCP Server，一次实现、多客户端复用\n- 降低“每个应用各自发明一套 function calling 集成”的成本\n\n## 为什么重要\n\n- **开发者**：减少接入复杂度\n- **Agent 应用**：可获得更丰富的工具生态\n- **终端用户**：助手能真正读数据、办任务，而不仅是聊天\n\n## 与普通 Function Calling 的差别（实践视角）\n\n| 维度 | Function Calling | MCP |\n|-----",
      "retrieved_at": "2026-08-16T15:04:43.436574+00:00",
      "score": 0.5048169271599203
    },
    {
      "id": "04_mcp_overview::1",
      "source": "file://D:/Deep-Research/data/raw/04_mcp_overview.md",
      "title": "MCP（Model Context Protocol）概览",
      "snippet": "端用户**：助手能真正读数据、办任务，而不仅是聊天\n\n## 与普通 Function Calling 的差别（实践视角）\n\n| 维度 | Function Calling | MCP |\n|------|------------------|-----|\n| 重心 | 模型 API 内的工具调用格式 | 跨应用的工具/资源互操作协议 |\n| 复用 | 往往绑定单一应用实现 | Server 可被多种客户端复用 |\n| 生态 | 随模型厂商而异 | 强调开放标准与生态连接 |\n\n二者并非互斥：很多系统在运行时仍会把 MCP 工具“映射”成模型可调用的函数。\n\n## 与本项目的关系\n\nMVP 可先用本地 Python 工具函数；完整版把 `vector_search` / 读文档等封装为 MCP Server，以体现协议化工具接入。",
      "retrieved_at": "2026-08-16T15:04:43.436574+00:00",
      "score": 0.4641403430339454
    },
    {
      "id": "06_context_engineering::0",
      "source": "file://D:/Deep-Research/data/raw/06_context_engineering.md",
      "title": "上下文工程：摘要与检索如何配合",
      "snippet": "# 上下文工程：摘要与检索如何配合\n\nsource: https://github.com/datawhalechina/hello-agents\ncitation: Datawhale Hello-Agents 教程（上下文工程相关章节与社区补充材料）公开大纲与通行实践归纳。\ntags: context-engineering, memory, token-budget\nlicense_note: 原创学习笔记式整理，不复制教程受版权保护的大段原文。\n\n## 问题\n\n长程 Agent 任务中，上下文窗口有限。若把全部网页、日志、历史对话塞进提示词，会导致：\n\n- 费用与延迟上升\n- 关键信号被淹没\n- 模型更容易“遗忘”约束\n\n## 两种常用手段\n\n### 1）检索（Retrieve）\n\n只取与当前子问题最相关的证据片段（Top-K）。适合知识新鲜、来源多样、需要引用的场景。\n\n### 2）摘要（Summarize）\n\n把历史轨迹、长文档压缩成短摘要。适合保留决策线索、降低重复信息。\n\n## 配合原则（实践）\n\n- Writer 输入：计划摘要 + Top 证据 + 已通过 claims（而不是原始全文）\n- Searcher 后处理：证据去重与合并\n- Critic 输入：claims + 对应 evidence，避免吞全量工具日志\n- 设硬预算：最大证据条数、最大步数、最大补",
      "retrieved_at": "2026-08-16T15:04:43.436574+00:00",
      "score": 0.4204574092678777
    },
    {
      "id": "10_hello_agents_project_map::1",
      "source": "file://D:/Deep-Research/data/raw/10_hello_agents_project_map.md",
      "title": "Hello-Agents 与本项目的能力映射",
      "snippet": "anner + `Plan` Schema |\n| ReAct | Searcher + tools |\n| Reflection | Critic |\n| RAG / Memory | `data/raw` → `knowledge_base` → `vector_search` |\n| 上下文工程 | ResearchState 裁剪与预算 |\n| MCP | 后期 `src/deep_research/mcp/` |\n| 评估 | `data/eval` + eval runner |\n| DeepResearch 案例 | 本仓库主线产品化 |\n\n## 学习建议\n\n先完成“本地检索 → 证据包”，再叠加 Planner/Writer/Critic，最后才是 MCP 与 Web。避免一上来同时引入所有子系统。",
      "retrieved_at": "2026-08-16T15:04:43.436574+00:00",
      "score": 0.40847941411507677
    },
    {
      "id": "web::0::97382",
      "source": "https://cloud.tencent.com/developer/article/2515271",
      "title": "MCP vs Function Calling，该如何选？-腾讯云开发者社区",
      "snippet": "",
      "retrieved_at": "2026-08-16T15:04:46.677048+00:00",
      "score": 0.9314689
    },
    {
      "id": "web::1::2948",
      "source": "https://www.geekpm.com/archives/mcp-fuctioncalling",
      "title": "Agent学习之：MCP和Function Call - 极客产品GeekPM",
      "snippet": "",
      "retrieved_at": "2026-08-16T15:04:46.677048+00:00",
      "score": 0.92359936
    },
    {
      "id": "web::2::90757",
      "source": "https://www.youtube.com/watch?v=V6SlMKDtLAw",
      "title": "【人工智能】Function Calling/MCP/A2A有什么区别",
      "snippet": "",
      "retrieved_at": "2026-08-16T15:04:46.677048+00:00",
      "score": 0.9018604
    },
    {
      "id": "web::3::70667",
      "source": "https://developer.aliyun.com/article/1666097",
      "title": "面向多工具任务调度的两种路径：MCP vs Agent + Function call",
      "snippet": "",
      "retrieved_at": "2026-08-16T15:04:46.677048+00:00",
      "score": 0.8315952
    },
    {
      "id": "web::4::87892",
      "source": "https://www.youtube.com/watch?v=BT5tPe9dcpU",
      "title": "MCP 与Function Calling 到底什么关系—— 以及为什么我认为大 ...",
      "snippet": "",
      "retrieved_at": "2026-08-16T15:04:46.677048+00:00",
      "score": 0.44565076
    },
    {
      "id": "web::0::51696",
      "source": "https://developer.volcengine.com/articles/7533551311816818724",
      "title": "MCP从理论到实战，别再和Function Calling搞混了！建议收藏(附实战案例)",
      "snippet": "",
      "retrieved_at": "2026-08-16T15:04:49.961211+00:00",
      "score": 0.88799405
    },
    {
      "id": "web::1::48995",
      "source": "https://mcpcn.com/blog/understanding-mcp-protocol",
      "title": "一文读懂MCP协议：大模型AI-Agent的USB-C接口",
      "snippet": "",
      "retrieved_at": "2026-08-16T15:04:49.961211+00:00",
      "score": 0.87605256
    },
    {
      "id": "web::0::25764",
      "source": "https://zilliz.com.cn/blog/Function-Calling-Outdated-MCP-The-Real-LLM-Standard",
      "title": "Function Calling已经过时，MCP才是真正的大模型接口标准",
      "snippet": "",
      "retrieved_at": "2026-08-16T15:04:58.461647+00:00",
      "score": 0.78493005
    },
    {
      "id": "web::0::63628",
      "source": "https://www.cnblogs.com/itech/p/18799272",
      "title": "比较LLM的function calling，Agent 和MCP - iTech",
      "snippet": "",
      "retrieved_at": "2026-08-16T15:05:02.421412+00:00",
      "score": 0.83932644
    },
    {
      "id": "web::1::90340",
      "source": "https://ppio.com/blogs/post/aiquan-bao-huo-de-mcp-ni-zui-xu-yao-liao-jie-zhe-5ge-guan-jian-wen-ti",
      "title": "AI圈爆火的MCP，你最需要了解这5个关键问题 - PPIO.com",
      "snippet": "",
      "retrieved_at": "2026-08-16T15:05:06.219824+00:00",
      "score": 0.7742597
    }
  ],
  "claims": [],
  "report_md": "# MCP与Function Calling的区别及选型分析\n\n## 1. 结论摘要\n- MCP是一种开放标准协议，目标是统一连接AI应用与外部系统；Function Calling是模型API内的工具调用格式，两者重心不同。[04_mcp_overview::0][04_mcp_overview::1]\n- Function Calling往往绑定单一应用实现，复用范围有限；MCP Server可被多种客户端复用，更强调开放标准与生态连接。[04_mcp_overview::1]\n- MCP与Function Calling并非互斥：实际系统中经常会把MCP工具“映射”成模型可调用的函数，二者可分层共存。[04_mcp_overview::1]\n- 针对性能、扩展性、灵活性的量化对比，以及具体业务场景案例，现有证据不足，选型时需结合项目实际进一步验证。[现有资料不足]\n\n## 2. 分节论证\n\n### 2.1 核心架构与设计目标\nMCP官方定位为“AI应用的USB接口”，是一种开放标准，用来把AI应用（客户端）与外部系统（数据源、工具、工作流）以统一方式连接起来。[04_mcp_overview::0] 它的重心是“跨应用的工具/资源互操作协议”，强调开放标准与生态连接。[04_mcp_overview::1]\n\nFunction Calling则被描述为“模型API内的工具调用格式”，其重心在模型API内部，解决“模型如何调用工具”的表示问题，往往绑定单一应用实现，生态随模型厂商而异。[04_mcp_overview::1]\n\n### 2.2 技术机制的根本性差异\n从现有证据看，二者的差异主要体现在三个维度：\n\n- **重心不同**：Function Calling是模型API内的工具调用格式；MCP是跨应用的工具/资源互操作协议。[04_mcp_overview::1]\n- **复用性不同**：Function Calling往往绑定单一应用实现；MCP Server可以被多种客户端复用，提升了工具/资源的可移植性。[04_mcp_overview::1]\n- **生态归属不同**：Function Calling的生态随模型厂商而异；MCP则强调开放标准与生态连接。[04_mcp_overview::1]\n\n从本质上看，MCP更接近跨应用的协议层，Function Calling更接近模型API内部的格式层。但现有证据未提供“动态发现 vs 静态注册”等更底层实现细节。\n\n### 2.3 适用场景分析\n根据上述差异，可以形成初步的选型方向：\n\n- **单一应用内、依赖特定模型API**：如果工具调用只在某个AI应用内部使用，且直接绑定特定模型API，Function Calling的路径更直接。[04_mcp_overview::1]\n- **跨应用复用、强调生态开放**：如果希望同一组工具/资源能被多种AI客户端复用，或需要融入开放标准生态，MCP的Server复用机制和开放标准更合适。[04_mcp_overview::1]\n- 需要说明的是，证据中未给出具体业务案例、性能数据或扩展性对比，因此上述方向属于基于架构特征的推断，而非量化选型结论。[现有资料不足]\n\n### 2.4 互补与共存\n证据明确指出：“二者并非互斥：很多系统在运行时仍会把MCP工具‘映射’成模型可调用的函数。”[04_mcp_overview::1] 这意味着在实际架构中，MCP可以作为工具/资源的统一接入层，而Function Calling可以作为模型调用这些工具的具体接口格式。二者可以通过“映射”机制共存，MCP负责互操作，Function Calling负责模型侧调用。\n\n不过，关于主流框架或平台对两者集成与对比的实践案例，现有资料中未提供相关内容。[现有资料不足]\n\n## 3. 不确定与局限\n- 现有证据主要来自MCP官方介绍，对Function Calling的描述较简略，未涉及具体函数描述格式、标准调用流程、工具调用限制等细节。[现有资料不足]\n- 没有提供性能、延迟、灵活性、扩展性的量化对比数据。[现有资料不足]\n- 未提供多Agent协作、动态工具发现、企业级集成等场景下的具体案例或数据支撑。[现有资料不足]\n- 因此，本报告的结论主要用于方向性判断，不能视为完整的工程选型依据。建议在真实项目中通过原型验证进一步确认。\n\n## 4. 参考来源\n- 04_mcp_overview::0, MCP（Model Context Protocol）概览, source: 0.5048（原文：https://modelcontextprotocol.io/introduction）\n- 04_mcp_overview::1, MCP（Model Context Protocol）概览, source: 0.4641（原文：https://modelcontextprotocol.io/introduction）",
  "metrics": {
    "latency_s": 0.0,
    "tokens": 0,
    "tool_calls": 6,
    "retry_count": 0
  }
}