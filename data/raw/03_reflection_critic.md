# Reflection：反思与修订机制

source: https://arxiv.org/abs/2303.11366
citation: Shinn et al., "Reflexion: Language Agents with Verbal Reinforcement Learning", arXiv:2303.11366, 2023.（社区常以此讨论 Agent Reflection 路线）
tags: agent, reflection, critic
license_note: 原创中文整理；Reflection/Critic 亦广泛见于 Hello-Agents 等教程中的工程实践。

## 核心思想

Reflection（反思）让模型在得到中间结果后，不只是继续往下写，而是：

1. 评估结果质量（是否矛盾、是否缺证据、是否跑题）；
2. 生成可执行的改进意见；
3. 带着意见重试或修订。

它类似“口头形式的强化学习信号”：用自然语言记录失败原因，指导下一轮更好的行为。

## 在工程上的常见形态

- **Self-Reflection**：同一 Agent 自我检查
- **Critic Agent**：独立审查者，专门找漏洞
- **有限轮次重试**：避免无限循环

## 为什么 Deep Research 需要它

研究报告最怕“读起来很流畅但没有依据”。Critic 的价值是把“能不能写”变成“有没有证据支撑”。

## 与本项目的关系

**Critic** 负责：

- 检查 claim 是否绑定 evidence_id
- 发现证据冲突
- 决定通过或打回补检（受 `MAX_CRITIC_ROUNDS` 限制）