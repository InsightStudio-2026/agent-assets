---
name: operational-learnings
description: 记录、修剪、导出和升级项目运行教训，例如环境坑、测试坑、验证命令差异、平台特殊约定。Use when user asks to capture operational learnings, record lessons, prune notes, promote rules, or says 运行教训 / 项目经验 / 踩坑记录 / 经验沉淀。
---

# Operational Learnings

## 1. 定位

Operational Learnings 记录可复用的运行教训，但不是权威规则。只有经用户批准后，稳定教训才可升级为 `AGENTS.md`、`.github/instructions/` 或长期 memory。

## 2. 分层状态

| Layer | 含义 | 存放 | 升级条件 |
| ------- | ------ | ------ | ---------- |
| Ephemeral | 一次性流水账 | 默认不保存 | N/A |
| Project Local | 项目本地可检索教训 | `docs/specs/<feature>/artifacts/operational-learnings/` 或 `tmp/operational-learnings/` | 重复出现或高影响 |
| Promoted | 已批准规则 / 标准 / 记忆 | `AGENTS.md` / `.github/instructions/` / memory | 用户明确批准 |

## 3. 记录规则

| Rule ID | 条件 | 动作 | 禁止 |
| --------- | ------ | ------ | ------ |
| OL-R1 | 环境坑重复出现 | 记录 cause / symptom / fix / verification | 写成泛泛提醒 |
| OL-R2 | 测试命令与文档不一致 | 记录真实命令与漂移来源 | 静默改权威文档 |
| OL-R3 | 平台 / Windows / PowerShell 特殊约定 | 记录约束与失败样例 | 混入一次性噪声 |
| OL-R4 | 需要升级为规则 | 生成 promote proposal | 未批准直接改 AGENTS |
| OL-R5 | 记录过期或错误 | prune 或标记 superseded | 保留冲突旧规则 |

### 上游采集来源

以下 skill / workflow 完成时可能产出值得沉淀的教训：

| 上游 | 典型教训 | 采集时机 |
| ------ | ---------- | ---------- |
| `postmortem` | 事故根因、防复发项、系统性盲区 | postmortem 完成后 §6 建议沉淀 |
| `engineering-retro` | 反复出现的环境坑、平台约定、测试陷阱 | retro §7 建议沉淀 |
| `diagnose` | 难以复现的 bug 模式、调试技巧 | Phase 6 清理时主动检查 |
| `/specs-execute` | 执行中发现的文档与现实偏差 | Task 完成时顺带记录 |

## 4. 模板 (Template)

```markdown
## 运行教训沉淀 (Operational Learning)

## 概述 (Summary)

- <一句话描述>

## 上下文 (Context)

- 项目 (Project):
- 日期 (Date):
- 触发原因 (Trigger):

## 异常现象 (Symptom)

- <什么地方报错、失败或误导了 AI 代理>

## 根本原因与约束条件 (Root Cause / Constraint)

- <为什么会发生此问题>

## 解决方案 (Resolution)

- <经验证可行的解决办法/动作>

## 验证手段 (Verification)

- <具体验证命令 / 生成产物 / 观察结果>

## 复用范围 (Reuse Scope)

- 仅此一次 (one-off) | 项目本地 (project-local) | 晋升候选 (candidate-for-promotion)

## 规范晋升提议 (Promotion Proposal)

- 目标位置 (Target): AGENTS.md | .github/standards | memory | N/A
- 需要用户审批 (Requires user approval): yes / no

```

## 5. 晋升与剪枝判定 (Promote / Prune Decisions)

| 条件 | 动作 |
| ------ | ------ |
| 同一问题重复出现两次以上 | candidate-for-promotion |
| 影响安全、发布、数据或权限 | candidate-for-promotion + route to relevant workflow |
| 只影响一次性环境 | keep ephemeral or discard |
| 已被标准覆盖 | prune duplicate |
| 与权威规则冲突 | report conflict; do not promote |

## 6. 禁止项

| 禁止项 | 原因 |
| -------- | ------ |
| 不把教训自动写入长期 memory | memory 最小化与用户批准边界 |
| 不用教训覆盖权威标准 | 只能提出 promote proposal |
| 不保存流水账 | 降低噪声 |
| 不记录 secrets / 私密路径细节 | 避免泄露 |
