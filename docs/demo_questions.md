# Deep-Research Demo 问题集

> 领域：技术知识研报  
> 更新日期：2026-08-20

---

## 使用方式

### 网页

1. 启动：`uvicorn deep_research.api.main:app --app-dir src --reload --host 127.0.0.1 --port 8000`
2. 打开 http://127.0.0.1:8000/
3. 粘贴下列任一问题 →「开始研究」（状态栏会显示当前步骤；若仍是旧页面请 Ctrl+F5）
4. 将满意的 `outputs/reports/report_*.md` 复制到 `docs/samples/` 并改名保存

### 命令行

```powershell
python src\deep_research\pipeline_m1.py
```

按提示输入同一问题。

---

## Demo 1：MCP vs Function Calling（主演示题，优先）

**问题：**

```text
MCP 和 Function Calling 有什么区别？各自适合什么场景？
```

**考察点：**

- 能否同时用到本地 MCP 文档与联网结果
- 报告是否有清晰对比（定义、差异、场景）
- 引用是否出现本地 id（如 `04_mcp_overview::*`）和/或网页 URL

**预期要点（人工验收，不必逐字一致）：**

1. MCP 是连接 AI 应用与外部工具/数据的开放协议（可类比 USB-C）
2. Function Calling 更偏向模型 API 内的工具调用格式
3. 二者可配合：MCP 工具最终仍可能映射为可调用函数
4. 适合场景：跨应用复用工具生态 vs 单应用内快速接工具
5. 报告含「局限/不确定」而不是假装穷尽所有厂商实现

**建议输出命名：**

- `docs/samples/demo1_mcp_vs_function_calling.md`

**运行记录（自行填写）：**

- 日期：
- research_id：
- evidence_count：
- final_passed / retry_count：
- 备注：

---

## Demo 2：ReAct vs Plan-and-Solve

**问题：**

```text
ReAct 与 Plan-and-Solve 在开放研究任务上如何选择？各自的适用边界是什么？
```

**考察点：**

- 能否检索到范式相关本地文档（`01_react_paradigm`、`02_plan_and_solve`）
- 是否讲清「边做边看」vs「先规划再执行」
- 是否联系到本项目：Searcher≈ReAct，Planner≈Plan-and-Solve

**预期要点：**

1. ReAct：Thought→Action→Observation 循环，适合工具反馈密集的任务
2. Plan-and-Solve：先拆计划再执行，适合可分解的开放研究
3. 开放研究常组合使用：先规划，检索阶段用 ReAct 式工具调用
4. 风险：ReAct 易轨迹过长；Plan 错误会全局放大
5. 有引用、有局限说明

**建议输出命名：**

- `docs/samples/demo2_react_vs_plan_and_solve.md`

**运行记录（自行填写）：**

- 日期：
- research_id：
- evidence_count：
- final_passed / retry_count：
- 备注：

---

## Demo 3：为什么需要 Critic

**问题：**

```text
为什么 Deep Research 需要 Critic？只靠 Writer 自检不够吗？常见失败模式有哪些，如何缓解？
```

**考察点：**

- 能否用到质量闸门 / 多智能体失败模式相关语料
- 论证「独立质检」价值
- 能对应本项目 Critic：未知引用、缺章节、补检重写、轮次上限

**预期要点：**

1. Writer 目标是写完，容易放过无引用断言
2. Critic 目标是找错，职责分离更利于降幻觉
3. 常见失败：角色漂移、假引用、无限重试、上下文爆炸
4. 缓解：结构化 Evidence、强制引用、有限轮补检、证据不足则写局限
5. 报告结构完整且带引用

**建议输出命名：**

- `docs/samples/demo3_why_critic.md`

**运行记录（自行填写）：**

- 日期：
- research_id：
- evidence_count：
- final_passed / retry_count：
- 备注：

---

## 验收清单（每题跑完勾选）

- [ ] 报告含：结论摘要 / 分节论证 / 不确定与局限 / 参考来源
- [ ] 关键结论带 `[evidence_id]` 或可追溯来源
- [ ] 无明显编造（不确定处有说明）
- [ ] 已保存到 `docs/samples/` 对应文件名
- [ ] README / portfolio 已能链到该样例（如已整理）

---

## 备选加试题（时间够再跑）

4. RAG 在 Agent 系统中的位置：什么时候该检索，什么时候该调用工具？  
5. 上下文工程中，「摘要」与「检索」应如何配合才能控制 token？  
6. 对比 LangGraph 与 AutoGen 的编排思路，各自更适合什么任务？

---

## 样例目录约定

```text
docs/
  demo_questions.md          # 本文件
  samples/
    demo1_mcp_vs_function_calling.md
    demo2_react_vs_plan_and_solve.md
    demo3_why_critic.md
```

若 `docs/samples/` 不存在，请先创建该文件夹，再把精选报告复制进去。