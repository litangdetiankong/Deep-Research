# 多智能体系统常见失败模式与缓解

source: https://github.com/datawhalechina/hello-agents
citation: 综合 Hello-Agents 多智能体实践主题，以及公开工程经验（角色漂移、通信噪声、无限循环等）的原创归纳。
tags: multi-agent, failure-modes, reliability
license_note: 原创整理，非某一论文全文翻译。

## 常见失败模式

1. **角色漂移**：Searcher 开始直接写最终报告，Critic 变成复读机  
2. **通信噪声**：Agent 之间只传自然语言，关键约束丢失  
3. **无限循环**：补检/重试没有上限  
4. **责任不清**：人人都能改一切，出问题无法定位  
5. **工具幻觉**：声称调用了工具但没有真实观察  
6. **上下文爆炸**：把全部中间结果塞给下游

## 缓解策略

- 单角色单职责，输出必须是结构化对象（plan/evidence/claim）
- 明确消息契约与 Schema 校验
- 设置 `max_steps`、`MAX_CRITIC_ROUNDS`
- 轨迹 JSONL 落盘，保证可回放
- 质量闸门：无引用不得进入终稿
- 证据不足时允许“信息不足”，禁止编造

## 与本项目的关系

Deep-Research 用四角色 + Schema + Critic 闸门，本质上就是在对抗上述失败模式。