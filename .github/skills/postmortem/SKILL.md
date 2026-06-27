---
name: postmortem
description: 起草事故复盘、故障时间线、影响面、根因、防复发项和行动项。Use when user asks for incident postmortem, outage report, RCA, retrospective after failure, or says 事故复盘 / 故障复盘 / 根因分析报告 / postmortem。
---

# Postmortem

## 1. 输入事实源

| Rule ID | 事实源 | 用途 | 缺失处理 |
| --------- | -------- | ------ | ---------- |
| PM-SRC-1 | incident timeline / alerts / logs | 构建时间线 | 标记 unknown，不补脑 |
| PM-SRC-2 | observability-incident report | 读取分级、止血、恢复、用户影响 | 缺失时建议路由 `/observability-incident` |
| PM-SRC-3 | release-deploy / rollback report | 判断是否发布或回滚引发 | 缺失时不归因到发布 |
| PM-SRC-4 | bug-audit / diagnose findings | 读取根因证据 | 无证据时写 hypotheses |

## 2. 复盘原则

| Rule ID | 原则 | 禁止 |
| --------- | ------ | ------ |
| PM-R1 | Blameless，但不无责 | 归咎个人或逃避系统责任 |
| PM-R2 | 事实、推断、未知分离 | 把猜测写成根因 |
| PM-R3 | 行动项必须 owner + due +验证方式 | “加强监控”“提高意识” |
| PM-R4 | 用户影响必须量化或声明 unknown | “影响较小”无证据 |
| PM-R5 | 防复发项回到 workflow / spec / test / alert | 只写会议纪要 |

## 3. 模板 (Template)

```markdown
## 故障复盘报告 (Incident Postmortem)

## 故障概述 (Summary)

- 发生事件 (What happened):
- 影响范围 (Impact):
- 持续时长 (Duration):
- 严重级别 (Severity):

## 故障时间线 (Timeline)
|  | 时间 (Time) | 事件 (Event) | 数据源/提供者 (Source) |  |
|  | ------ | ------- | -------- |  |
|  | `<timestamp>` | <event> | <log/alert/person> |  |

## 根本原因 (Root Cause)

- 确认根因 (Confirmed cause):
- 诱发/促成因素 (Contributing factors):
- 未知数/疑点 (Unknowns):

## 故障发现与响应 (Detection and Response)

- 如何被发现 (How detected):
- 有效响应动作 (What worked):
- 失效/迟滞动作 (What failed):

## 用户影响 (Customer / User Impact)

- 受影响用户数 (Affected users):
- 受影响功能 (Affected functionality):
- 客户沟通发送情况 (Communication sent):

## 改动/行动项 (Action Items)
|  | 行动项 (Action) | 责任人 (Owner) | 截止日期 (Due) | 验证方式 (Verification) | 跟踪路由 (Route) |  |
|  | -------- | ------- | ----- | -------------- | ------- |  |
|  | <action> | <owner> | <date> | <how verified> | </workflow or issue> |  |
```

## 4. 路由规则 (Routing Rules)

| 条件 (Condition) | 路由 (Route) |
| ----------- | ------- |
| 事故仍在进行 | `/observability-incident` |
| 根因未知且需要排查 | `diagnose` or `/bug-audit` |
| 需要修复 spec / tests | `/specs-write` or `/specs-execute` |
| 发布 / rollback 缺口 | `/release-deploy` |
| 监控 / alert / runbook 缺口 | `/observability-incident` |

## 5. 完成检查 (Completion Checklist)

| 检查项 (Check) | 合格标准 (PASS) |
| ------- | ------ |
| Timeline grounded | 每个关键时间点有来源或标 unknown |
| Root cause honest | confirmed / contributing / unknown 分开 |
| Impact clear | 用户、功能、时长、严重性清楚 |
| Actionable | 每个 action 有 owner / due / verification / route |
| Actions tracked | 行动项已创建为可追踪条目（见 §6） |

## 6. 行动项落地

复盘中的行动项如果只停留在文档中，很容易断链。完成复盘后：

- 若行动项 ≥ 3 个，建议使用 `/tasks-to-issues` 批量创建可追踪的 issues。
- 若有运维教训值得长期记忆，建议使用 `operational-learnings` 沉淀。
- 若复盘发现的系统性问题需要重构，建议路由 `/architecture-audit`。
