---
name: doc-coauthoring
description: 通过结构化协作流程起草、修订和验证文档、proposal、technical spec、decision doc 与说明材料。Use when user wants to co-author documentation, proposals, decision docs, technical specs outside the formal /specs-write contract, or says 文档协作 / 共写文档 / 起草 proposal / 决策文档。
---

# Doc Coauthoring

## 1. 定位

Doc Coauthoring 是通用文档协作 skill，用于帮助用户把目标、读者、上下文和草稿转成可读、可审查、可迭代的文档。它不替代 `/specs-write` 的 feature spec 合同，不替代 `writing-shape` 的文章成稿，也不替代 `release-notes` / `postmortem` 的专用模板。

## 2. 触发与分流

| Rule ID | 条件 | 动作 | 分流 |
| --------- | ------ | ------ | ------ |
| DC-R1 | 用户要写 proposal、decision doc、technical note、说明文档 | 启动共写流程 | 本 skill |
| DC-R2 | 用户要写正式 feature spec / tasks / design | 分流 | `/specs-write` |
| DC-R3 | 用户要把碎片发展成文章 | 分流 | `writing-fragments` / `writing-shape` |
| DC-R4 | 用户要发布说明 | 分流 | `release-notes` |
| DC-R5 | 用户要事故复盘 | 分流 | `postmortem` |

## 3. 协作流程

| 阶段 (Phase) | 目标 | 输出 |
| ------- | ------ | ------ |
| Phase 1 — Brief | 明确文档目的、读者、决策或行动目标 | Doc Brief |
| Phase 2 — Context Transfer | 收集事实源、限制、已有材料、不可说内容 | Context Table |
| Phase 3 — Shape | 选择文档形态：proposal / decision doc / explainer / update / FAQ | Outline |
| Phase 4 — Draft | 生成可审查初稿 | Draft |
| Phase 5 — Reader Test | 从目标读者视角检查清晰度、缺口、下一步 | Revision Plan |
| Phase 6 — Finalize | 输出最终稿和未决问题 | Final Doc |

## 4. 文档企划简案 (Doc Brief)

```markdown
## 文档企划简案 (Doc Brief)

## 目的 (Purpose)

- <为什么存在此文档，要解决什么问题>

## 目标读者 (Audience)

- <谁会阅读此文档>

## 预期效果 (Desired Outcome)

- <是要做出决策、达成共识、触发行动，还是做知识传递>

## 事实源/参考材料 (Source Material)
|  | 事实源/路径/URL (Source) | 作用与价值 (Role) |  |
|  | -------- | ------ |  |
|  | <path/url/note> | <why it matters> |  |

## 边界与约束 (Boundaries)

- 必须包含的内容 (Must include):
- 绝对不能声称的内容 (Must not claim):
- 未决开放问题 (Open questions):

```

## 5. 文档形态规则

| 文档类型 (Doc Type) | 适用条件 | 必备结构 |
| ---------- | ---------- | ---------- |
| Proposal | 需要争取批准或资源 | Problem / Options / Recommendation / Risks / Decision needed |
| Decision Doc | 记录取舍 | Context / Decision / Alternatives / Consequences / Revisit condition |
| Technical Note | 解释实现或机制 | Context / Mechanism / Constraints / Examples / Failure modes |
| Project Update | 汇报进展 | Goal / Progress / Risks / Next actions / Needs |
| FAQ | 面向重复问题 | Question / Short answer / Detail / Source |

## 6. 读者测试 (Reader Test)

| 检查项 (Check) | 合格标准 (PASS 标准) | 失败信号 (FAIL 信号) |
| ------- | ----------- | ----------- |
| Audience fit | 读者无需额外背景即可理解主线 | 术语未定义、上下文跳跃 |
| Action clarity | 读完知道要批准、执行或理解什么 | 只有信息堆叠，无下一步 |
| Evidence | 关键论断有事实源 | 夸大、猜测、无出处 |
| Boundary honesty | 未决问题、风险、限制清楚 | 把草案说成确定结论 |
| Maintenance | 文档有 owner 或更新条件 | 过时风险无人负责 |

## 7. 禁止项

| 禁止项 | 原因 |
| -------- | ------ |
| 不把普通共写文档冒充正式 spec | feature contract 归 `/specs-write` |
| 不虚构事实源、指标或用户反馈 | 文档可信度边界 |
| 不静默改写权威 SSOT | 只提出修订建议 |
| 不复制外部模板专有内容 | 保持本仓原创与 provenance 清晰 |
