{
  "research_id": "13517ade-e3fb-4936-b310-d03a0419d0a8",
  "question": "为什么 Deep Research 需要 Critic？只靠 Writer 自检不够吗？",
  "plan": {
    "sub_questions": [
      "多Agent系统中Writer-Critic架构相比单Agent自检在Deep Research任务中的性能提升有哪些实证证据？",
      "大语言模型自我修正机制（self-refinement）存在哪些理论上的局限性，导致其无法替代外部Critic？",
      "在Deep Research场景中，Critic的设计模式（如多角色批评、结构化反馈、迭代验证）如何影响最终研究报告的质量？",
      "已有研究中，Critic在减少事实性错误、优化信息整合和提升论证严谨性方面的具体作用机制是什么？"
    ],
    "success_criteria": [
      "能清晰说明Critic与Writer自检在工作原理、决策路径和错误发现能力上的核心差异",
      "能引用至少3项支持Critic必要性或揭示自检局限性的学术研究或技术报告",
      "能归纳出Deep Research中Critic发挥价值的典型场景与具体设计建议"
    ],
    "max_steps": 12
  },
  "evidence": [
    {
      "id": "06_context_engineering::1",
      "source": "file://D:/Deep-Research/data/raw/06_context_engineering.md",
      "title": "上下文工程：摘要与检索如何配合",
      "snippet": "ms（而不是原始全文）\n- Searcher 后处理：证据去重与合并\n- Critic 输入：claims + 对应 evidence，避免吞全量工具日志\n- 设硬预算：最大证据条数、最大步数、最大补检轮次\n\n## 与本项目的关系\n\n`ResearchState` 就是上下文工程的载体：结构化字段比“一大段聊天记录”更容易裁剪与审计。",
      "retrieved_at": "2026-08-16T15:12:22.309004+00:00",
      "score": 0.6016511645854258
    },
    {
      "id": "03_reflection_critic::1",
      "source": "file://D:/Deep-Research/data/raw/03_reflection_critic.md",
      "title": "Reflection：反思与修订机制",
      "snippet": "自我检查\n- **Critic Agent**：独立审查者，专门找漏洞\n- **有限轮次重试**：避免无限循环\n\n## 为什么 Deep Research 需要它\n\n研究报告最怕“读起来很流畅但没有依据”。Critic 的价值是把“能不能写”变成“有没有证据支撑”。\n\n## 与本项目的关系\n\n**Critic** 负责：\n\n- 检查 claim 是否绑定 evidence_id\n- 发现证据冲突\n- 决定通过或打回补检（受 `MAX_CRITIC_ROUNDS` 限制）",
      "retrieved_at": "2026-08-16T15:12:22.309004+00:00",
      "score": 0.5842515027384108
    },
    {
      "id": "07_multi_agent_failures::1",
      "source": "file://D:/Deep-Research/data/raw/07_multi_agent_failures.md",
      "title": "多智能体系统常见失败模式与缓解",
      "snippet": "steps`、`MAX_CRITIC_ROUNDS`\n- 轨迹 JSONL 落盘，保证可回放\n- 质量闸门：无引用不得进入终稿\n- 证据不足时允许“信息不足”，禁止编造\n\n## 与本项目的关系\n\nDeep-Research 用四角色 + Schema + Critic 闸门，本质上就是在对抗上述失败模式。",
      "retrieved_at": "2026-08-16T15:12:22.309004+00:00",
      "score": 0.5398505067424616
    },
    {
      "id": "09_deep_research_quality_gates::0",
      "source": "file://D:/Deep-Research/data/raw/09_deep_research_quality_gates.md",
      "title": "Deep Research 的质量闸门与引用评价",
      "snippet": "# Deep Research 的质量闸门与引用评价\n\nsource: https://github.com/datawhalechina/hello-agents\ncitation: Hello-Agents 中 DeepResearch / 评估相关思想与工程实践的原创归纳；并结合本项目 ARCHITECTURE 约定。\ntags: deep-research, evaluation, citations\nlicense_note: 原创笔记，服务本仓库学习与实现。\n\n## 为什么要有质量闸门\n\n没有闸门的“长文生成”看起来像研究报告，实质可能是流畅幻觉。Deep Research 的关键差异是：**结论可追溯**。\n\n## 建议闸门\n\n1. 每条核心 claim 至少绑定一个 evidence_id  \n2. evidence_id 必须能在 evidence 列表中找到  \n3. Critic 发现冲突时标记争议，不假装一致  \n4. URL 可达性抽检（能做则做）  \n5. 证据不足时输出“信息不足”，而不是编造  \n6. 补检轮次有上限\n\n## 如何评价引用质量（可做评测指标）\n\n- **引用有效率**：引用是否可访问/可定位到本地文档  \n- **相关度**：snippet 是否支撑 claim  \n- **无引用断言率**：越低越好  \n- **要点覆盖率**：相对",
      "retrieved_at": "2026-08-16T15:12:22.309004+00:00",
      "score": 0.5281871102596309
    },
    {
      "id": "web::0::58251",
      "source": "https://openai.com/zh-Hant-HK/index/introducing-deep-research",
      "title": "隆重介紹深入研究 (Deep Research) | OpenAI",
      "snippet": "",
      "retrieved_at": "2026-08-16T15:12:25.716741+00:00",
      "score": 0.44116792
    },
    {
      "id": "web::1::97335",
      "source": "https://readwise.io/reader/shared/01jn0917qcve2zrk0pywsjag0v",
      "title": "我一个月内用了100 次deep research，全部经验一次性分享｜万能 prompt、深度经验、报告下载 | annotated by Harry",
      "snippet": "",
      "retrieved_at": "2026-08-16T15:12:25.716741+00:00",
      "score": 0.43856934
    },
    {
      "id": "web::2::94198",
      "source": "https://readingoutpost.com/deep-research-chatgpt",
      "title": "Deep Research 是什麼？實測介紹 ChatGPT 深度研究新功能 | 閱讀前哨站",
      "snippet": "",
      "retrieved_at": "2026-08-16T15:12:25.716741+00:00",
      "score": 0.42548645
    },
    {
      "id": "web::3::6762",
      "source": "https://www.facebook.com/ReadingOutpost/posts/%E6%88%91%E5%A6%82%E4%BD%95%E7%94%A8%E6%AF%8F%E6%9C%88-200-%E7%BE%8E%E9%87%91%E8%81%98%E8%AB%8B%E4%B8%80%E4%BD%8D%E5%85%A8%E5%B9%B4%E7%84%A1%E4%BC%91%E7%9A%84%E5%8D%9A%E5%A3%AB%E7%A0%94%E7%A9%B6%E7%94%9Fopen-ai-%E5%9C%A8-22-%E6%8E%A8%E5%87%BA%E4%BA%86%E6%9C%80%E6%96%B0%E7%9A%84%E6%B7%B1%E5%BA%A6%E7%A0%94%E7%A9%B6deep-research%E5%8A%9F%E8%83%BD%E5%8E%B2%E5%AE%B3%E7%9A%84%E7%A8%8B%E5%BA%A6%E7%B0%A1%E7%9B%B4%E5%BF%AB%E6%8A%8A%E6%88%91%E5%9A%87%E6%AD%BB%E6%88%91%E8%AE%80%E5%AE%8C/1078570470949427",
      "title": "閱讀前哨站瓦基 - 我如何用每月 200 美金，聘請一位全年無休的博士研究生？ Open AI 在 2/2...",
      "snippet": "",
      "retrieved_at": "2026-08-16T15:12:25.716741+00:00",
      "score": 0.33280948
    },
    {
      "id": "web::4::95271",
      "source": "https://www.promptingguide.ai/guides/deep-research",
      "title": "OpenAI Deep Research - Prompt Engineering Guide",
      "snippet": "",
      "retrieved_at": "2026-08-16T15:12:25.716741+00:00",
      "score": 0.27528602
    },
    {
      "id": "web::0::18968",
      "source": "https://github.com/Kocoro-lab/ai-agent-book/blob/main/zh/Part9-%E5%89%8D%E6%B2%BF%E5%AE%9E%E8%B7%B5/%E7%AC%AC27%E7%AB%A0%EF%BC%9ADeep-Research.md",
      "title": "ai-agent-book/zh/Part9-前沿实践/第27章：Deep-Research.md at main · Kocoro-lab/ai-agent-book · GitHub",
      "snippet": "",
      "retrieved_at": "2026-08-16T15:12:28.574800+00:00",
      "score": 0.67321366
    },
    {
      "id": "web::1::34012",
      "source": "https://tianpan.co/zh/blog/2026-04-10-when-generalist-beats-specialists-single-agent-architecture",
      "title": "当通用型 Agent 击败专家组：统一单 Agent 架构的优势",
      "snippet": "",
      "retrieved_at": "2026-08-16T15:12:28.574800+00:00",
      "score": 0.6353361
    },
    {
      "id": "web::0::82277",
      "source": "https://www.alphaxiv.org/zh/overview/2310.08118",
      "title": "大型语言模型真的能通过自我批判其计划来改进吗？ | alphaXiv",
      "snippet": "",
      "retrieved_at": "2026-08-16T15:12:31.186695+00:00",
      "score": 0.6549173
    },
    {
      "id": "web::1::22611",
      "source": "https://swarma.org?p=58651",
      "title": "大语言模型复杂推理的自我进化机制：研究综述与前沿展望 | 集智俱乐部",
      "snippet": "",
      "retrieved_at": "2026-08-16T15:12:31.186695+00:00",
      "score": 0.53473455
    },
    {
      "id": "web::0::39885",
      "source": "https://modelscope.csdn.net/68f6ecf7a6dc56200e95f04f.html",
      "title": "万字长文深度解析最新Deep Research技术：前沿架构、核心技术与未来展望_魔搭ModelScope社区-ModelScope魔搭社区",
      "snippet": "",
      "retrieved_at": "2026-08-16T15:12:35.127308+00:00",
      "score": 0.45711306
    },
    {
      "id": "web::1::88428",
      "source": "https://zhuanlan.zhihu.com/p/1936367642064693029",
      "title": "【Deep Research】01-Deep Research的全面综述：系统、方法与应用",
      "snippet": "",
      "retrieved_at": "2026-08-16T15:12:35.127308+00:00",
      "score": 0.45420644
    },
    {
      "id": "web::0::90561",
      "source": "https://cbyys.sppc.edu.cn/cn/article/pdf/preview/10.19619/j.issn.1007-1938.2026.00.026.pdf",
      "title": "超越“数字崇拜”:AI赋能学术研究的定性评估",
      "snippet": "",
      "retrieved_at": "2026-08-16T15:12:38.849139+00:00",
      "score": 0.04891691
    },
    {
      "id": "web::1::82284",
      "source": "https://sjc.bnu.edu.cn/docs//2026-03/1934145b51c34c2ca4dfe9d43980a984.pdf",
      "title": "出版行业编辑采纳DeepSeek思维链技术的行为路径研究",
      "snippet": "",
      "retrieved_at": "2026-08-16T15:12:38.849139+00:00",
      "score": 0.044435676
    }
  ],
  "claims": [],
  "report_md": "# Deep Research 为什么需要 Critic？——Writer 自检不足的证据与机制分析\n\n## 1. 结论摘要\n\n- Deep Research 报告最怕“读起来很流畅但没有依据”，Critic 的价值在于把“能不能写”变成“有没有证据支撑”，这是 Writer 自检无法替代的外部约束。[03_reflection_critic::1]\n- Critic 被设计为“独立审查者，专门找漏洞”，其检查项包括 claim 是否绑定 evidence_id、是否存在证据冲突、决定通过或打回补检；相比“自我检查”，Critic 增加了强制证据绑定和冲突检测两个硬性动作。[03_reflection_critic::1]\n- 没有 Critic 作为质量闸门，长文生成很容易变成“流畅幻觉”——看起来像研究报告，但结论缺乏依据；而“无引用不得进入终稿”“证据不足时允许信息不足、禁止编造”等规则，正是通过 Critic 落地的硬约束。[09_deep_research_quality_gates::0][07_multi_agent_failures::1]\n- Critic 要有效运行，需要“claims + 对应 evidence”的结构化输入和硬预算，且受有限轮次重试限制；否则会被全量工具日志淹没，或陷入无限循环。[06_context_engineering::1][03_reflection_critic::1]\n- 在系统层面，Deep Research 采用“四角色 + Schema + Critic 闸门”来对抗多智能体失败模式，说明 Critic 是系统设计的一部分，而非可选的补充环节。[07_multi_agent_failures::1]\n\n## 2. 分节论证\n\n### 2.1 Writer-Critic 架构与单 Agent 自检的核心差异\n\n在 Deep Research 中，Writer 负责生成内容，Critic 则被定义为“独立审查者，专门找漏洞”[03_reflection_critic::1]。与“自我检查”相比，Critic 的关键差异在于：\n\n- **决策路径不同**：Writer 自检是生成者自己检查自己的产出；Critic 是独立于 Writer 的审查角色。Reflection 机制中同时包含“自我检查”和“Critic Agent”，说明系统设计者把“审查”从“生成”中分离出来。[03_reflection_critic::1]\n- **检查动作不同**：Critic 的具体职责是“检查 claim 是否绑定 evidence_id”“发现证据冲突”“决定通过或打回补检”[03_reflection_critic::1]。这是一组结构化、可验证的动作，而不是生成者对文本流畅度的主观自查。\n- **错误发现能力不同**：由于 Critic 不参与生成，它可以避免“自己写了、自己再检查”时对原有假设的路径依赖；其审查依据是证据与 claim 的绑定关系，而非生成者的内部一致性。[03_reflection_critic::1]\n\n需要说明的是：现有证据并未提供 Writer-Critic 架构与单 Agent 自检在 Deep Research 任务上的量化性能对比数据（如事实一致性分数、错误率等）。因此，本节只能基于机制差异说明 Critic 的不可替代性，无法给出实证效果数值。[现有资料不足]\n\n### 2.2 大语言模型自我修正机制的理论局限性\n\n现有证据没有直接引用自我修正（self-refinement）的学术理论，也没有系统分析其推理层面局限。但从 Deep Research 的质量风险可以间接看到自我修正的不足：\n\n- 没有质量闸门时，“长文生成”看起来像研究报告，但“实质可能是流畅幻觉”。[09_deep_research_quality_gates::0] 这说明仅靠生成的流畅性不足以保证内容有依据。\n- Critic 通过检查 claim 是否绑定 evidence_id 来阻止“无依据断言”进入终稿[03_reflection_critic::1]，这是“流畅幻觉”的核心克星。\n- 多智能体系统需要显式质量闸门：无引用不得进入终稿、证据不足时禁止编造、允许输出“信息不足”。[07_multi_agent_failures::1] 这类硬性规则如果仅靠 Writer 自我提醒，容易被语言的流畅性掩盖；而 Critic 是独立执行的机制，不依赖生成者的自觉。\n\n因此，从工程证据可以推断：自我修正的局限在于它缺少“外部证据校验”这一步，而 Critic 正是补上这一步的外部审查者。但关于 self-refinement 的理论性局限（例如模型在自我修正中可能固化的偏差），现有资料没有展开，需要更多研究证据。[现有资料不足]\n\n### 2.3 Deep Research 场景中 Critic 的设计模式与质量影响\n\nCritic 的设计直接影响最终研究报告质量。从证据中可以提炼出以下关键设计原则：\n\n- **结构化输入**：Critic 的输入应为“claims + 对应 evidence”，避免吞入全量工具日志。[06_context_engineering::1] 如果让 Critic 直接面对海量检索日志，它可能无法聚焦于“claim 是否由证据支撑”这一核心问题。\n- **硬预算约束**：设置最大证据条数、最大步数、最大补检轮次。[06_context_engineering::1] 这能防止 Critic 与 Writer 之间形成无限循环，同时倒逼 Writer 精简证据、聚焦关键信息。\n- **有限轮次重试**：Critic 决定通过或打回补检，但重试次数受 `MAX_CRITIC_ROUNDS` 限制。[03_reflection_critic::1][07_multi_agent_failures::1]\n- **质量闸门**：无引用不得进入终稿；证据不足时允许“信息不足”，禁止编造。[07_multi_agent_failures::1]\n\n这些设计共同把 Critic 变成一个可审计、可收敛的“质量闸门”，其效果是：最终报告必须在证据层面站得住脚，而不是仅仅语言流畅。[09_deep_research_quality_gates::0]\n\n同时，Critic 不是孤立组件，而是与“多角色 + Schema + Critic 闸门”整体架构配合，用于对抗多智能体系统中的失败模式。[07_multi_agent_failures::1] 上下文工程的载体 `ResearchState` 也是 Critic 输入可裁剪、可审计的前提。[06_context_engineering::1]\n\n不过，关于“多角色批评”“结构化反馈”等更细粒度的设计模式对最终质量的具体影响，现有证据没有提供系统对比实验，因此无法给出结论。[现有资料不足]\n\n### 2.4 Critic 在减少事实性错误、优化信息整合、提升论证严谨性方面的作用机制\n\n- **减少事实性错误**：Critic 检查 claim 是否绑定 evidence_id，并主动发现证据冲突。[03_reflection_critic::1] 当证据之间矛盾时，Critic 可以打回补检，从源头阻断无依据或自相矛盾的信息进入终稿。\n- **优化信息整合**：上下文工程要求 Critic 输入的是“claims + 对应 evidence”，且检索结果先经过证据去重与合并。[06_context_engineering::1] 这意味着 Critic 评价的是“整合后的 claim-证据对”，而不是原始材料堆砌，从而促使 Writer 的信息整合必须可追溯。\n- **提升论证严谨性**：质量闸门要求无引用不得进入终稿；证据不足时允许“信息不足”，禁止编造。[07_multi_agent_failures::1] 这迫使论证严格限定在证据范围内，结论不能超出证据支持。Deep Research 与普通长文生成的关键差异正在于此——证据原文在“结论可……”处截断，无法完整引用，但可以确认这一差异与质量闸门直接相关。[09_deep_research_quality_gates::0]\n- **迭代验证**：Critic 决定通过或打回补检，配合有限轮次重试，形成“生成 → 审查 → 补检 → 再审查”的收敛回路。[03_reflection_critic::1][06_context_engineering::1]\n\n需要注意的是，证据中并未提供 Critic 减少事实性错误的量化数据（例如错误率下降比例），因此以上机制仅为定性描述。[现有资料不足]\n\n## 3. 不确定与局限\n\n- 现有证据主要来自工程实践笔记（如 Hello-Agents 相关笔记），并非同行评议的学术研究，其结论的普适性需谨慎对待。[09_deep_research_quality_gates::0]\n- 证据中缺少 Writer-Critic 架构与单 Agent 自检在 Deep Research 任务上的直接对比实验，无法量化性能提升幅度。[现有资料不足]\n- 关于大语言模型自我修正机制（self-refinement）的理论局限，现有证据仅能提供间接推断，未给出系统性的理论分析。[现有资料不足]\n- 关于 Critic 设计模式（如多角色批评、结构化反馈）对最终报告质量的具体影响，现有证据未提供对比实验数据。[现有资料不足]\n- 部分关键证据文本存在截断（如“结论可……”），相关内容无法完整引用。[09_deep_research_quality_gates::0]\n\n## 4. 参考来源\n\n- [03_reflection_critic::1]《Reflection：反思与修订机制》，项目技术笔记，source: 0.5843\n- [06_context_engineering::1]《上下文工程：摘要与检索如何配合》，项目技术笔记，source: 0.6017\n- [07_multi_agent_failures::1]《多智能体系统常见失败模式与缓解》，项目技术笔记，source: 0.5399\n- [09_deep_research_quality_gates::0]《Deep Research 的质量闸门与引用评价》，Hello-Agents 原创笔记，source: 0.5282",
  "metrics": {
    "latency_s": 0.0,
    "tokens": 0,
    "tool_calls": 6,
    "retry_count": 0
  }
}