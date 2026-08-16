# RAG：检索增强生成基础

source: https://arxiv.org/abs/2005.11401
citation: Lewis et al., "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks", arXiv:2005.11401, 2020.
tags: rag, retrieval, knowledge-base
license_note: 原创中文整理，结合经典 RAG 论文思想与工程通行流程。

## 核心思想

RAG（Retrieval-Augmented Generation）让模型在生成答案前，先从外部知识库检索相关文档片段，再基于检索结果生成，从而：

- 降低纯参数记忆带来的过时与幻觉
- 使答案可追溯到来源片段
- 便于更新知识（改索引，不必重训大模型）

## 典型流水线

1. **Ingest**：原始文档清洗与切块（chunk）
2. **Embed**：块文本转为向量
3. **Index**：写入向量库
4. **Retrieve**：问题向量化后做相似度检索 Top-K
5. **Generate**：把检索片段作为上下文生成答案（本项目后期由 Writer 完成）

## 关键工程点

- chunk 太大：噪声多；太小：缺上下文
- 只检索不校验：仍可能引用不相关片段
- 需要元数据（来源 URL/文档 ID）才能做引用

## 与本项目的关系

当前策略是 **先本地 RAG，搜索 API 待申请**。Searcher 的第一条腿是 `vector_search`：检索结果必须落成 `Evidence`（含 source/snippet）。