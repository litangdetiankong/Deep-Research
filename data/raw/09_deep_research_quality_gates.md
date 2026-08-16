# Deep Research 的质量闸门与引用评价

source: https://github.com/datawhalechina/hello-agents
citation: Hello-Agents 中 DeepResearch / 评估相关思想与工程实践的原创归纳；并结合本项目 ARCHITECTURE 约定。
tags: deep-research, evaluation, citations
license_note: 原创笔记，服务本仓库学习与实现。

## 为什么要有质量闸门

没有闸门的“长文生成”看起来像研究报告，实质可能是流畅幻觉。Deep Research 的关键差异是：**结论可追溯**。

## 建议闸门

1. 每条核心 claim 至少绑定一个 evidence_id  
2. evidence_id 必须能在 evidence 列表中找到  
3. Critic 发现冲突时标记争议，不假装一致  
4. URL 可达性抽检（能做则做）  
5. 证据不足时输出“信息不足”，而不是编造  
6. 补检轮次有上限

## 如何评价引用质量（可做评测指标）

- **引用有效率**：引用是否可访问/可定位到本地文档  
- **相关度**：snippet 是否支撑 claim  
- **无引用断言率**：越低越好  
- **要点覆盖率**：相对参考要点清单的覆盖程度  
- **成本与延迟**：tokens、秒数、工具调用次数

## 与本项目的关系

这些指标对应后续 `data/eval/` 与 `src/deep_research/eval/`。现在先保证 Evidence/Claim Schema 能承载它们。