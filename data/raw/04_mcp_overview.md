# MCP（Model Context Protocol）概览

source: https://modelcontextprotocol.io/introduction
citation: Anthropic / MCP 社区, Model Context Protocol 官方文档（Introduction）.
tags: mcp, tools, protocol
license_note: 基于官方公开介绍页面的原创中文归纳，非文档逐字翻译拷贝。

## 一句话理解

MCP 是一种开放标准，用来把 AI 应用（客户端）与外部系统（数据源、工具、工作流）以统一方式连接起来。官方常用类比：**像 AI 应用的 USB-C 接口**。

## 能做什么

- 让 Agent 连接文件、数据库、搜索、日历等外部能力
- 让开发者把工具封装成 MCP Server，一次实现、多客户端复用
- 降低“每个应用各自发明一套 function calling 集成”的成本

## 为什么重要

- **开发者**：减少接入复杂度
- **Agent 应用**：可获得更丰富的工具生态
- **终端用户**：助手能真正读数据、办任务，而不仅是聊天

## 与普通 Function Calling 的差别（实践视角）

| 维度 | Function Calling | MCP |
|------|------------------|-----|
| 重心 | 模型 API 内的工具调用格式 | 跨应用的工具/资源互操作协议 |
| 复用 | 往往绑定单一应用实现 | Server 可被多种客户端复用 |
| 生态 | 随模型厂商而异 | 强调开放标准与生态连接 |

二者并非互斥：很多系统在运行时仍会把 MCP 工具“映射”成模型可调用的函数。

## 与本项目的关系

MVP 可先用本地 Python 工具函数；完整版把 `vector_search` / 读文档等封装为 MCP Server，以体现协议化工具接入。