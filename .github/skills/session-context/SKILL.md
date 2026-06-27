---
name: session-context
description: 保存和恢复当前会话的目标、相关文件、已做决策、剩余工作、阻塞项与验证状态。Use when user asks to save session context, resume work, recover context, continue later, or says 会话上下文 / 恢复上下文 / 下次继续 / 保存进度。
---

# Session Context

## 1. 定位

Session Context 是会话级恢复包，不是长期记忆、不是 `tasks.md`、不是 `handoff-payload.yaml`、不是 Project Archives。它只帮助下一次会话快速恢复当前工作现场。

## 2. 触发规则

| Rule ID | 前置条件 | 动作 | 下一步 |
| --------- | ---------- | ------ | -------- |
| SC-R1 | 用户要求保存当前进度 / 下次继续 | 生成 session context | 输出保存路径 |
| SC-R2 | 用户要求恢复某次 session context | 读取并展示，不自动改代码 | 等用户确认下一步 |
| SC-R3 | 当前任务跨多个文件且中断风险高 | 建议生成 session context | 用户确认后写入 |
| SC-R4 | 信息已存在于 spec / issue / archive | 引用路径，不重复复制 | 输出轻量索引 |

## 3. 存放规则

| 条件 | 目标路径 |
| ------ | ---------- |
| 有 active spec | `docs/specs/<feature-slug>/artifacts/session-context/` |
| 无 spec 且只需本地恢复 | `tmp/session-context/` |
| 用户指定路径 | 使用用户路径，但不得覆盖权威文档 |

## 4. 模板 (Template)

```markdown
## 会话上下文 (Session Context)

## 核心目标 (Goal)

- <当前工作目标>

## 编辑范围 (Scope)

- 允许修改路径 (Allowed paths):
- 禁止触碰路径 (Forbidden paths):

## 当前状态 (Current State)

- 已完成 (Completed):
- 进行中 (In progress):
- 待处理 (Pending):
- 受阻/阻塞 (Blocked):

## 关键文件 (Key Files)
|  | 物理路径 (Path) | 重要性说明 (Why it matters) |  |
|  | ------ | ---------------- |  |
|  | <path> | `<reason>` |  |

## 已做决策 (Decisions Made)
|  | 已定决策 (Decision) | 事实依据 (Evidence) | 回滚/逆转条件 (Reversal condition) |  |
|  | ---------- | ---------- | -------------------- |  |
|  | <decision> | <path/user quote> | <condition> |  |

## 验证状态 (Verification State)
|  | 检查项 (Check) | 运行状态 (Status) | 运行证据/日志 (Evidence) |  |
|  | ------- | -------- | ---------- |  |
|  | <check> | PASS / FAIL / NOT RUN / UNKNOWN | <path/output> |  |

## 下一步恢复行动 (Next Resume Step)

- <单步行动指令 (single next action)>

```

## 5. 禁止项

| 禁止项 | 原因 |
| -------- | ------ |
| 不把流水账写进长期 memory | 会话信息默认短期 |
| 不复制已有 spec / issue / archive 全文 | 避免事实源分叉 |
| 恢复时不自动改代码 | 恢复包只是事实源，不是授权 |
| 不把 session context 冒充 Done 证据 | Done 以任务 / workflow 权威状态为准 |
