---
name: engineering-retro
description: 基于 commit、PR、测试、热点文件、失败修复和发布记录做周期性工程复盘，输出趋势、风险和行动建议。Use when user asks for engineering retrospective, team/solo retro, development cadence review, or says 工程复盘 / 周期复盘 / 研发节奏 / 热点文件分析。
---

# Engineering Retro

## 1. 定位

Engineering Retro 是轻量复盘 skill，只做证据汇总、趋势判断和行动建议；不自动重排 roadmap，不修改 spec，不替代 `/code-health-dashboard`、`/ci-quality-gates` 或 `review`。

## 2. 输入事实源

| Rule ID | 事实源 | 用途 | 缺失处理 |
| --------- | -------- | ------ | ---------- |
| ER-SRC-1 | git log / commit range | 开发节奏、提交粒度 | 要求 fixed range 或标 unknown |
| ER-SRC-2 | PR / issue history | 协作流、review 延迟、返工 | 无 tracker 时标 N/A |
| ER-SRC-3 | test / coverage / CI history | 质量趋势 | 分流 `/code-health-dashboard` |
| ER-SRC-4 | release reports | 发布节奏、回滚、事故关联 | 无 release 时标 N/A |
| ER-SRC-5 | incident / bug audit / postmortem | 重复故障与防复发 | 分流对应 workflow |

## 3. 复盘维度

| 维度 (Dimension) | 检查项 | 风险信号 | 路由 (Route) |
| ----------- | -------- | ---------- | ------- |
| Cadence | commit / PR / release 频率 | 长期无发布或突增大 PR | `/project-steward` |
| Quality | test pass、coverage、flaky | 测试下降或 flaky 增多 | `/code-health-dashboard` / `/ci-quality-gates` |
| Hotspots | 高频修改文件 / 模块 | 热点文件反复改且缺测试 | `/architecture-audit` |
| Rework | revert / fix-forward / bug churn | 同类修复反复出现 | `/bug-audit` / `diagnose` |
| Operability | release / incident / rollback | 事故后无行动项闭环 | `/observability-incident` / `postmortem` |
| Collaboration | issue readiness、AFK/HITL、handoff | 上下文缺失或交接失败 | `session-context` / `/issue-triage` |

## 4. 模板 (Template)

```markdown
## 工程复盘报告 (Engineering Retro)

## 复盘范围 (Scope)

- 复盘模式 (Mode): 个人 (solo) | 团队 (team)
- 复盘周期 (Period):
- 仓库与模块范围 (Repositories / areas):

## 事实依据摘要 (Evidence Summary)
|  | 信号类型 (Signal) | 事实细节 (Evidence) | 状态说明 (Status) |  |
|  | -------- | ---------- | -------- |  |
|  | 提交记录 (commits) | <range> | <summary> |  |
|  | 测试与 CI (tests / CI) | `<artifact>` | <summary> |  |
|  | 发布版本 (releases) | <report> | <summary> |  |

## 审计发现 (Findings)
|  | 问题描述 (Finding) | 严重程度 (Severity) | 事实依据 (Evidence) | 跟踪路由 (Route) |  |
|  | --------- | ---------- | ---------- | ------- |  |
|  | <finding> | 高/中/低 (High / Medium / Low) | <path/output> | <route> |  |

## 推荐改善行动 (Recommended Actions)
|  | 改善行动 (Action) | 责任人 (Owner) | 验证手段 (Verification) | 对应路由 (Route) |  |
|  | -------- | ------- | -------------- | ------- |  |
|  | <action> | <owner or TBD> | <how checked> | <workflow/skill> |  |
```

## 5. 判定规则

| Rule ID | 条件 | 动作 |
| --------- | ------ | ------ |
| ER-R1 | evidence 不足 | 标 unknown，不补脑 |
| ER-R2 | 质量信号缺 dashboard | 推荐 `/code-health-dashboard` |
| ER-R3 | CI 阻塞或 required checks 缺失 | 推荐 `/ci-quality-gates` |
| ER-R4 | 热点文件结构性反复 | 推荐 `/architecture-audit` |
| ER-R5 | 事故或回滚反复 | 推荐 `postmortem` / `/observability-incident` |
| ER-R6 | 行动项需要 roadmap 变更 | 提出建议，等待用户裁决 |

## 6. 禁止项

| 禁止项 | 原因 |
| -------- | ------ |
| 不用单个坏提交推断长期趋势 | 趋势需要范围证据 |
| 不把复盘建议自动变成 roadmap | 策略变更需用户批准 |
| 不替代专项审计 | 发现风险后路由到对应 workflow |
| 不输出无 owner / 无验证方式的行动项 | 复盘必须可闭环 |

## 7. 下游沉淀

复盘不是终点——发现需要落地才有价值：

| 发现类型 | 下游 | 说明 |
| ---------- | ------ | ------ |
| 行动项 ≥ 3 个 | `/tasks-to-issues` | 批量创建可追踪 issues |
| 反复出现的环境/平台/测试坑 | `operational-learnings` | 记录可复用教训 |
| 事故后行动项未闭环 | `postmortem` 补检 | 检查原 postmortem 的 action items 完成状态 |
| 趋势揭示架构腐烂 | `/architecture-audit` | 路由专项审计 |
