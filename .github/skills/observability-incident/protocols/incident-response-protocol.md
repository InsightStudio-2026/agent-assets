# 事故响应协议 (Incident Response Protocol) · /observability-incident Incident 主线事实源

> **本文是 `/observability-incident` workflow Incident 主线的事故声明 / 止血 / 通信 / postmortem 协议字典**。所有 R-INC-* 规则在此定义；入口 workflow 按 ID 引用，不重复事实。
> 本文档自身遵循结构化规则表 + ID 体系格式规范（入口骨架 + 支撑文档分离 + 零 ASCII 流程图）。

---

## 0. 定位与索引

### 0.1 文档定位

- 事故响应协议字典；与 `observability-incident` SKILL.md 事故材料面 + Hard-gate 项零漂移。
- 不是事故剧本；不替代真实 on-call 训练；只规定 INCIDENT_DECLARED → POSTMORTEM_COMPLETE 路径上每步必须满足的语义。
- 三大命名空间：R-INC-DECLARE-*声明；R-INC-MITIG-* 止血；R-INC-POST-* postmortem。

### 0.2 ID 命名空间

- `R-INC-DECLARE-1~5`：事故声明协议。
- `R-INC-MITIG-1~7`：止血协议（含 Hard-gate 触发）。
- `R-INC-POST-1~6`：postmortem 协议。

---

## 1. 事故声明（R-INC-DECLARE-*）

| 规则 ID (Rule ID) | 协议 | 触发范围 | 必填 | 失败动作 |
| --------- | ------ | --------- | ------ | --------- |
| `R-INC-DECLARE-1` | Severity 分级 | 所有事故 | P0 全站 / P1 核心路径 / P2 局部 / P3 边缘 | 缺则按最坏假设按 P1 处理 |
| `R-INC-DECLARE-2` | 影响面快照 | 所有事故 | 影响用户数 / 区域 / 功能 / 时间窗口；初步估算可后续修正 | 缺则不进入 MITIGATION_IN_PROGRESS |
| `R-INC-DECLARE-3` | Owner 指派 | 所有事故 | Incident Commander + 每条 mitigation 子任务 owner；不允许"待定" | 无 owner → 决策真空；强制阻塞 |
| `R-INC-DECLARE-4` | 通信通道 | P0/P1 必，P2/P3 视范围 | 内部 IM 群 / on-call rotation / 工程师群组 | 缺则信息漂移 |
| `R-INC-DECLARE-5` | 事故 ID + 命名 | 所有事故 | `INC-{slug}-{YYYYMMDD}-{seq}`；写入 DAG-N-INCIDENT-* | 缺则无法溯源 |

### 1.1 Severity 分级判定矩阵

| Severity | 判定条件（任一命中即升级） | 响应时限 |
| ---------- | -------------------------- | --------- |
| P0 | 全站不可用 / 核心业务全部失败 / 安全数据泄露 / 资金损失 | 立即 + 24/7 全员 |
| P1 | 核心路径部分失败（注册 / 支付 / 同步等）/ > 10% 用户受影响 | 15 分钟内响应 |
| P2 | 非核心路径失败 / < 10% 用户受影响 / 功能降级可恢复 | 工作时段响应 |
| P3 | 边缘问题 / 仅小群体 / 不影响业务 | 排期处理 |

---

## 2. 止血协议（R-INC-MITIG-*）

| 规则 ID (Rule ID) | 协议 | 触发范围 | 必填 | 强控门禁 (Hard-gate) |
| --------- | ------ | --------- | ------ | ---------- |
| `R-INC-MITIG-1` | 优先用 runbook 已定义 mitigation | 所有事故 | 先看 runbook 推荐步骤；无 runbook → 创建 runbook 草稿（事后补完整） | - |
| `R-INC-MITIG-2` | 用户通知 / 状态页更新 | 影响用户的 P0/P1 必；P2 视范围 | 文案 + 通道 + 发送时机；用户原话批准入 F-HG-3 | `HG-IRREV-003`（对外通信）+ `HG-INCIDENT-*` |
| `R-INC-MITIG-3` | 生产降级（流量切流 / 限流 / 服务降级） | 流量类事故 | 降级范围 + 持续时长 + 恢复条件；用户原话批准 | `HG-IRREV-004` + `HG-INCIDENT-*` |
| `R-INC-MITIG-4` | 生产 rollback | 发布回归 / 配置错误 | 通过 `/release-deploy` rollback 链；不本 workflow 直接执行 | `HG-IRREV-001/002/004`（按操作）+ 启 `/release-deploy:ROLLBACK_REQUIRED` |
| `R-INC-MITIG-5` | Feature flag 大范围操作 | flag 类事故 | flag 名 + 影响范围 + 二次确认；用户原话批准 | `HG-RELEASE-*`（事故场景）+ `HG-INCIDENT-*` |
| `R-INC-MITIG-6` | 紧急 hotfix 部署 | 不可降级 / 不可 rollback | 仍走 `/release-deploy` 紧急路径；不绕过 Hard-gate；packet F-HG-1~8 全齐 | `HG-IRREV-*` 候选 + `HG-INCIDENT-*` |
| `R-INC-MITIG-7` | 止血确认 | 所有事故 | 核心指标恢复绿 + 用户报告无新增 + 内部确认 | `INCIDENT_RESOLVED_PENDING_POSTMORTEM` 进入条件 |

### 2.1 止血 Forbidden

- ❌ 在未止血时跳到 postmortem
- ❌ 用户通知 / 生产降级 / rollback / 状态页未批准就执行
- ❌ "我们再等等看"超过事故 severity 响应时限
- ❌ Mitigation 失败后无 fallback（runbook 必须含至少 2 种 mitigation）
- ❌ Hard-gate 用"事故紧急"理由跳过；紧急路径仍需 packet + 用户原话

---

## 3. Postmortem 协议（R-INC-POST-*）

| 规则 ID (Rule ID) | 协议 | 触发范围 | 必填 | 时限 |
| --------- | ------ | --------- | ------ | ------ |
| `R-INC-POST-1` | 强制触发 | P0 / P1 | 不允许跳过；用户裁决也不允许 | 72h 内完成草稿；2 周内完成最终版 |
| `R-INC-POST-2` | 可选触发 | P2 / P3 | 用户裁决；视影响面与学习价值 | 用户裁决时限 |
| `R-INC-POST-3` | 时间线 | 所有 | 分钟级时间线（detection / declared / notified / mitigation 开始 / 完成 / resolved） | 必须；时间戳源 = monitoring + IM 历史 |
| `R-INC-POST-4` | 5 Whys / 多根因 | 所有 | 至少 3 层原因分析；不允许单一根因结论 | 必须 |
| `R-INC-POST-5` | 修复项 + 防复发 | 所有 | 立即 mitigation（短期）+ 长期改进项；每项含 owner + 截止；handoff 给 `/specs-write` 或 `/bug-audit` | 必须 |
| `R-INC-POST-6` | 复盘会议 | P0 / P1 | 召开复盘会 + 记录纪要附件；blameless 文化 | P0 强制召开 |

### 3.1 Postmortem 模板

```markdown
## 事故复盘报告 (Postmortem) · {Incident ID}

## 故障概述 (Summary)

- 严重级别 (Severity): P0 / P1 / P2 / P3
- 发现时间 (Detected): `<timestamp>`
- 恢复时间 (Resolved): `<timestamp>`
- 持续总时长 (Total Duration): <分钟> (minutes)
- 影响评估 (Impact): <影响用户数 / 受损功能 / 业务经济损失> (users / functions / business loss)

## 故障时间线 (Timeline - 分钟级)
|  | 时间 (Time) | 关键事件 (Event) | 事实来源 (Source) |  |
|  | ------ | ------- | -------- |  |
|  | ... | 触发告警 (Alert fired) | monitoring |  |
|  | ... | 确认宣判定级为 P1 (Declared P1 by <owner>) | IM |  |
|  | ... | 用户通报批准 (User notification approved by <user 原话引用>) | F-HG-3 |  |
|  | ... | 开始执行止血动作 (Mitigation started) | runbook step |  |
|  | ... | 止血完成，业务初步恢复 (Mitigation complete) | metric recovery |  |
|  | ... | 故障彻底恢复确认无新增 (Resolved - 确认无新增) | core metric green |  |

## 根本原因深度分析 - 至少3层 (Root Cause Analysis - ≥ 3 层)

- 第 1 层 - 技术层面原因 (Layer 1 - technical): <技术层原因>
- 第 2 层 - 流程层面原因 (Layer 2 - process): <流程层原因>
- 第 3 层 - 组织层面原因 (Layer 3 - organizational): <组织 / 沟通 / 优先级>

## 其他促成/诱发因素 (Contributing Factors)

- ...

## 有效响应动作/闪光点 (What Went Well)

- ...

## 失效/迟滞动作/改进空间 (What Went Poorly)

- ...

## 改善与行动项 (Action Items)
|  | 行动项 (Item) | 责任人 (Owner) | 截止日期 (Due) | 严重程度 (Severity) | 接续路由 (Handoff) |  |
|  | ------ | ------- | ----- | ---------- | --------- |  |
|  | Hotfix X bug | A | 2026-05-30 | High | /specs-write mitigation-{slug} |  |
|  | Add alert rule | B | 2026-06-15 | Medium | /specs-execute |  |
|  | Improve runbook | C | 2026-06-30 | Medium | runbook update |  |

## 长期防复发机制 (Prevent Recurrence)

- 长期改进项：架构 / 流程 / 培训 / 工具

```

### 3.2 Postmortem Forbidden

- ❌ 单一根因（"是 X 个 bug 导致的"）
- ❌ Blame 文化（指责个人；事故责任在系统设计）
- ❌ Action items 无 owner / 无截止
- ❌ "经验教训"作为唯一防复发；必须有具体可执行项
- ❌ 跳过复盘会议（P0 / P1）

---

## 4. 与其他 workflow 联动

| 联动方向 | 触发 | 路由 |
| --------- | ------ | ------ |
| 根因 → 修复 | postmortem 输出 mitigation tasks | `/specs-write` 或 `/bug-audit` 或 `diagnose` |
| 发布回归 → rollback | R-INC-MITIG-4 | `/release-deploy:ROLLBACK_REQUIRED` |
| 安全相关事故 | 数据泄露 / 越权 | 同时启 `/security-privacy-audit` |
| 数据相关事故 | DB 损坏 / 误删除 | 同时启 `/data-migration-safety`（如适用） |
| Observability gap 暴露 | 事故中发现 monitoring 盲区 | Setup 主线补 R-OBS-SIG-*/ R-OBS-MAT-* |

---

## 5. 修订规则

- 本文修订必须同 PR 修订 `observability-incident.md` Phase 6-7 骨架与 §0.3 Hard-gate 表。
- R-INC-* ID 一旦分配不得复用；废弃改 deprecated。
- §1.1 Severity 矩阵 / §3 Postmortem 强制条件任何放宽必须先在 `observability-incident` SKILL.md 同步并经用户裁决；P0 / P1 强制 postmortem 不允许放宽。
- Postmortem 模板（§3.1）字段任何减项必须先在 `observability-incident` SKILL.md 事故材料面同步事实源。
