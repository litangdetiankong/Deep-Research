# 上下文工程：摘要与检索如何配合

source: https://github.com/datawhalechina/hello-agents
citation: Datawhale Hello-Agents 教程（上下文工程相关章节与社区补充材料）公开大纲与通行实践归纳。
tags: context-engineering, memory, token-budget
license_note: 原创学习笔记式整理，不复制教程受版权保护的大段原文。

## 问题

长程 Agent 任务中，上下文窗口有限。若把全部网页、日志、历史对话塞进提示词，会导致：

- 费用与延迟上升
- 关键信号被淹没
- 模型更容易“遗忘”约束

## 两种常用手段

### 1）检索（Retrieve）

只取与当前子问题最相关的证据片段（Top-K）。适合知识新鲜、来源多样、需要引用的场景。

### 2）摘要（Summarize）

把历史轨迹、长文档压缩成短摘要。适合保留决策线索、降低重复信息。

## 配合原则（实践）

- Writer 输入：计划摘要 + Top 证据 + 已通过 claims（而不是原始全文）
- Searcher 后处理：证据去重与合并
- Critic 输入：claims + 对应 evidence，避免吞全量工具日志
- 设硬预算：最大证据条数、最大步数、最大补检轮次

## 与本项目的关系

`ResearchState` 就是上下文工程的载体：结构化字段比“一大段聊天记录”更容易裁剪与审计。