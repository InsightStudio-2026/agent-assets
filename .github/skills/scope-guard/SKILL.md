---
name: scope-guard
description: 为简单任务、资产维护或临时会话声明允许修改范围、禁止范围、边界扩展门和危险命令提醒。Use when user asks to keep changes scoped, set edit boundaries, avoid scope creep, or says 控制范围 / 外科手术 / 不要乱改 / scope guard。
user-invocable: false
---

# Scope Guard

## 1. 定位

Scope Guard 是会话级编辑边界，不替代 spec、tasks、issue 或 workflow 权威状态。它只约束当前会话允许修改什么、禁止触碰什么、何时必须停下请求确认。

## 2. 范围约束信息包 (Scope Packet)

```markdown
## 范围约束信息包 (Scope Guard Packet)

## 允许修改路径 (Allowed Paths)
|  | 物理路径 (Path) | 允许原因 (Reason) |  |
|  | ------ | -------- |  |
|  | <path> | <why allowed> |  |

## 禁止修改路径 (Forbidden Paths)
|  | 物理路径 (Path) | 禁止原因 (Reason) |  |
|  | ------ | -------- |  |
|  | <path> | <why forbidden> |  |

## 允许操作行为 (Allowed Actions)
|  | 操作 (Action) | 边界约束 (Boundary) |  |
|  | -------- | ---------- |  |
|  | <edit/read/verify> | <limit> |  |

## 边界扩展判定门禁 (Boundary Expansion Gate)
|  | 条件 (Condition) | 必需行动 (Required Action) |  |
|  | ----------- | ----------------- |  |
|  | 需要修改 Allowed Paths 以外的文件 (Need to edit outside Allowed Paths) | 解释原因并等待用户确认 (explain reason + wait for confirmation) |  |
|  | 需要执行破坏性命令 (Need destructive command) | 等待明确的用户授权确认 (wait for explicit confirmation) |  |
|  | 需要引发真实世界的副作用 (Need real-world side effect) | 路由到对应的专项工作流 (route to responsible workflow) |  |

## 最终验证 (Verification)

- <在声明完成前必须通过的核验 (checks required before saying done)>

```

## 3. 判定规则

| Rule ID | 条件 | 动作 |
| --------- | ------ | ------ |
| SG-R1 | 用户给定明确文件 / 目录 | Allowed Paths 限定到该范围 |
| SG-R2 | 发现必须改范围外文件 | 暂停并说明扩展原因 |
| SG-R3 | 范围外改动只是顺手优化 | 不做 |
| SG-R4 | 需要删除、重置、强推、生产操作、数据库写入 | 等用户明确确认；必要时路由专项 workflow |
| SG-R5 | 任务已有 spec / tasks | Scope Guard 只能收窄当前会话，不改权威范围 |

## 4. 报告模板 (Report Template)

```markdown
## 范围约束 (Scope Guard)

- 允许修改路径 (Allowed paths):
- 禁止触碰路径 (Forbidden paths):
- 是否需要扩展边界 (Boundary expansion needed): yes / no
- 边界扩展原因 (Expansion reason):
- 用户确认授权状态 (User confirmation): required / not required

```

## 5. 禁止项

| 禁止项 | 原因 |
| -------- | ------ |
| 不把 Scope Guard 当 spec | 它不是需求权威 |
| 不因“顺手”修改邻近代码 | 外科手术边界 |
| 不自动扩大 Allowed Paths | 扩边必须说明并确认 |
| 不覆盖 workflow 的真实世界副作用 gate | 生产 / 数据 / 发布等归专项 workflow |
