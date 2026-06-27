---
name: handoff
description: 将当前对话压缩为交接文档，方便另一个代理继续接手。Use when user asks for a handoff, transfer note, or says 交接/压缩上下文。
argument-hint: "下一次会话要继续什么工作？"
---

# 交接压缩（handoff）

## 1. 定位

Handoff 是**跨代理交接**——为一个全新代理（零上下文）提供最小必要信息以继续工作。它不是 `session-context`（同项目同代理恢复现场），不是 `tasks.md`（权威任务状态），不是 `delivery-log.md` 或 `done/`（交付归档）。

| 场景 | 用哪个 |
| ------ | -------- |
| 当前会话中断、下次自己继续 | `session-context` |
| 交给另一个代理或另一个人 | **handoff** |
| 项目级任务追踪 | `tasks.md` / spec |
| 已完成工作归档 | `delivery-log.md` + `done/` |

## 2. 存放规则

| 条件 | 目标路径 |
| ------ | ---------- |
| 有 active spec | `docs/specs/<feature-slug>/artifacts/handoff-`<timestamp>`.md` |
| 无 spec 且项目有 `tmp/` | `tmp/handoff-`<timestamp>`.md` |
| 无项目上下文 | 系统临时目录（Windows: `$env:TEMP`） |

若目标文件已存在，写入前必须先读取。

## 3. 模板 (Template)

```markdown
## 工作交接件 (Handoff)

## 工作目标 (Objective)

- <当前工作的目标，一句话>

## 上下文环境 (Context)

- 运行工作流/技能 (Active workflow / skill): <当前使用的 workflow 或 skill>
- 权威规格说明书 (SSOT / spec path): <路径或 N/A>
- 当前开发分支 (Branch): <当前分支或 N/A>

## 任务状态 (State)

- 已完成的关键步骤 (Completed):
- 进行中的工作 (In progress):
- 被阻塞项与原因 (Blocked):

## 关键决策 (Key Decisions)
|  | 决策事项 (Decision) | 事实依据 (Evidence) | 逆转/回滚风险 (Reversal risk) |  |
|  | ---------- | ---------- | --------------- |  |
|  | <decision> | <path/user quote> | <low/medium/high> |  |

## 下一步行动 (Next Action)

- <接手代理应该做的第一件事>

## 推荐启用技能 (Recommended Skills / Workflows)

- <接手代理应启用的 skill 或 workflow>

## 禁止事项 (Do Not)

- <接手代理不应该做的事>

```

## 4. 写作纪律

- 不复制已存在于 spec / issue / archive / ADR / commit 中的内容——只引用路径。
- 不写流水账——只写接手代理做出正确决策所需的最小信息。
- 若用户传入参数，将其视为下一次会话的重点，据此裁剪文档。

## 5. 禁止项

| 禁止项 | 原因 |
| -------- | ------ |
| 不把 handoff 当 session-context | 二者受众不同 |
| 不复制全文代码或长日志 | handoff 是索引，不是存档 |
| 不省略 Next Action | 接手代理必须知道第一步 |
| 不省略 Do Not | 防止接手代理重复已排除的方向 |
