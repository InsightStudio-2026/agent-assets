---
name: internal-comms
description: 起草内部沟通材料，包括状态报告、领导层更新、项目公告、FAQ、newsletter、风险通报和事故沟通草案。Use when user asks for internal communications, status reports, leadership updates, project updates, FAQs, newsletters, or says 内部沟通 / 周报 / 项目通报 / 领导汇报 / FAQ。
---

# Internal Comms

## 1. 定位

Internal Comms 用于内部沟通材料的结构化起草与修订。它不替代 `release-notes` 的用户可见发布说明，不替代 `postmortem` 的事故复盘，不替代 `/content-publishing-ops` 的对外内容发布，也不虚构进度、指标或决策。

## 2. 触发与分流

| Rule ID | 条件 | 动作 | 分流 |
| --------- | ------ | ------ | ------ |
| IC-R1 | 用户要写状态报告、领导更新、项目通报、FAQ、newsletter | 启动内部沟通流程 | 本 skill |
| IC-R2 | 用户要对外发布说明 / changelog | 分流 | `release-notes` |
| IC-R3 | 用户要事故 RCA / postmortem | 分流 | `postmortem` |
| IC-R4 | 用户要对外平台发布 | 分流 | `/content-publishing-ops` |
| IC-R5 | 内容涉及未确认战略 / 人事 / 法务 / 安全事件 | 标记需人工确认 | WAIT_FOR_USER |

## 3. 常见格式

| 格式 (Format) | 适用场景 | 必备结构 |
| -------- | ---------- | ---------- |
| Status Report | 周报 / 进度同步 | Goal / Done / In Progress / Risks / Needs / Next |
| Leadership Update | 向上汇报 | Executive Summary / Decision needed / Risks / Options / Recommendation |
| Project Update | 项目组同步 | Context / Progress / Blockers / Changes / Next actions |
| FAQ | 解释变化或决策 | Question / Short Answer / Detail / Source / Owner |
| Newsletter | 周期性内部资讯 | Highlights / Changes / Upcoming / Kudos / Links |
| Incident Comms Draft | 事故过程沟通 | What happened / Impact / Current status / Next update / Owner |

## 4. 输入表

| 字段 (Field) | 是否必需 (Required) | 说明 |
| ------- | ---------- | ------ |
| Audience | Yes | 团队、领导、跨部门、全员 |
| Purpose | Yes | 告知、求决策、求资源、降风险、同步进展 |
| Facts | Yes | 已完成、指标、时间线、来源 |
| Sensitive boundaries | Yes | 不能说、未确认、需审批内容 |
| Ask / CTA | Conditional | 需要读者做什么 |
| Tone | Conditional | 简洁、正式、安抚、行动导向 |

## 5. 质量门

| 检查项 (Check) | 合格标准 (PASS 标准) | 失败信号 (FAIL 信号) |
| ------- | ----------- | ----------- |
| Truthfulness | 事实、状态、风险可追溯 | 编造进展或淡化风险 |
| Audience fit | 信息量与读者职责匹配 | 技术细节过载或太空泛 |
| Decision clarity | 需要决策时写明选项和推荐 | 只描述问题，不给下一步 |
| Risk honesty | 阻塞、风险、未知数明确 | 把不确定说成确定 |
| Update cadence | 有下一次更新时间或 owner | 发完无人负责 |

## 6. 模板

```markdown
## 内部沟通草案 (Internal Comms Draft)

## 目标受众 (Audience)

- <受众>

## 目的 (Purpose)

- <通知 / 对齐 / 请求 / 升级 (inform / align / ask / escalate)>

## 核心内容 (Message)
<草案正文 (draft)>

## 事实源引用 (Facts Used)
|  | 事实 (Fact) | 事实来源 (Source) |  |
|  | ------ | -------- |  |
|  | <fact> | <source> |  |

## 敏感边界 (Sensitive Boundaries)

- 绝对不可声称 (Do not claim):
- 需审批项 (Needs approval):

## 明确要求/下一步行动 (Ask / Next Step)

- <具体行动 (action)>

```

## 7. 禁止项

| 禁止项 | 原因 |
| -------- | ------ |
| 不虚构指标、进展、用户反馈或决策 | 内部沟通信任边界 |
| 不把内部草稿当对外发布稿 | 对外发布归 `/content-publishing-ops` |
| 不替代事故复盘 | 根因和行动项归 `postmortem` |
| 不隐藏重大风险以换取好看汇报 | 风险诚实优先 |
