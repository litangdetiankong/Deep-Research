# Plan-and-Solve：先规划再执行

source: https://arxiv.org/abs/2305.04091
citation: Wang et al., "Plan-and-Solve Prompting: Improving Zero-Shot Chain-of-Thought Reasoning in Large Language Models", arXiv:2305.04091, 2023.
tags: agent, planning, plan-and-solve
license_note: 原创中文整理，基于公开论文信息与通用实践归纳。

## 核心思想

Plan-and-Solve 强调：面对复杂问题时，先生成一个**显式计划（Plan）**，再按步骤执行（Solve），而不是一上来就边想边答。

相对“一步到位”的回答，它更适合多跳推理与可分解任务。

## 两阶段

1. **Plan**：把目标拆成子问题/子步骤，明确成功标准与顺序；
2. **Solve**：逐步执行；必要时对计划做有限修订。

## 优点

- 结构清晰，便于分工给不同模块或 Agent
- 更容易设置停止条件与预算（最大步数）
- 便于人工检查“计划是否合理”

## 风险

- 计划本身错误会放大到全程
- 过度规划可能浪费 token
- 环境变化时需要重规划机制

## 与本项目的关系

Deep-Research 的 **Planner** 采用 Plan-and-Solve 思路：先产出 `sub_questions`、`success_criteria`、`max_steps`，再交给 Searcher 执行检索。