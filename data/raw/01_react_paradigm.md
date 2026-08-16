# ReAct：推理与行动交替的智能体范式

source: https://arxiv.org/abs/2210.03629
citation: Yao et al., "ReAct: Synergizing Reasoning and Acting in Language Models", arXiv:2210.03629, 2022/2023.
tags: agent, react, tool-use
license_note: 本文为基于公开论文摘要与社区通行理解的原创中文整理，非论文原文摘录。

## 核心思想

ReAct（Reason + Act）让语言模型在解决问题时交替进行两件事：

1. **Reasoning（推理）**：用自然语言写出当前思考、假设与计划片段；
2. **Acting（行动）**：调用外部工具或环境接口（搜索、计算器、API、代码执行等），获得观察（Observation）；
3. 再基于观察继续推理，直到得出答案或达到步数上限。

它把“只想不做”的链式思维（CoT）和“只做不想”的纯动作策略结合起来，使过程更可追踪，也更容易利用外部知识。

## 典型循环

Thought → Action → Observation → Thought → ... → Final Answer

## 适用场景

- 需要工具调用的问答与研究任务
- 环境反馈重要的任务（网页、知识库、代码仓）
- 需要展示中间轨迹以便调试与评测的 Agent

## 局限

- 轨迹变长后上下文成本上升
- 工具选错或观察噪声会导致推理跑偏
- 对开放式长程研究，常需与规划（Plan）或反思（Reflection）组合

## 与本项目的关系

在 Deep-Research 中，**Searcher** 更贴近 ReAct：根据研究计划调用检索工具，观察结果后再决定下一步检索。