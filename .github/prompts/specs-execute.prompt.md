---
name: specs-execute
description: 按 Spec 合同的 Task 单元逐个执行，强制 TDD Red-Green-Refactor 循环。
argument-hint: '[TASK-### 编号]'
agent: agent
---

# 执行 Task

执行指定的 Task 单元。

严格按 `.github/skills/specs-execute/SKILL.md` 流程：

1. 读取 tasks.md 中对应 Task 条目，强制复述上游锚点
2. TDD Red → Green → Refactor 不跳步
3. Phase 7 双层 DoD 验证
4. 更新 tasks.md Status / Execution Notes

外科手术——只改 Touches 范围内的代码，不扩 scope。

Task：${input:taskId}
