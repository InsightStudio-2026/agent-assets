---
description: "从 0 到 1 的项目立项与母本生成工作流（/project-inception）专属的触发判定、状态转换路由、状态权威与动作决策矩阵"
---

# 项目立项决策矩阵（/project-inception）

## 0. 触发与临界路由决策表

| ID | 前置条件 | 匹配动作 | 下一步/目标路由 | 源 / 备注 |
| ---- | ---------- | ---------- | ----------------- | ----------- |
| R-ROUTE-INCP-1 | 用户显式 `/project-inception` | 启用 workflow | 进入 Phase 1 (Inception Intake) | 显式入口 |
| R-ROUTE-INCP-2 | 用户明确要商业生死判断 / 付费意愿 / 替代方案 / Pivot-Kill | 停止并分流 | 路由至 `/business-model-audit` | 商业生死分流 |
| R-ROUTE-INCP-3 | 用户意图是商业产品，且付费主体 / 替代方案 / MVP 投入依据不清 | 停止并分流 | 路由至 `/business-model-audit` | 商业风险分流 |
| R-ROUTE-INCP-4 | 用户只有项目想法、方向、愿景、商业念头，无需生死判断 | 启用 workflow | 进入 Phase 1 (Inception Intake) | 想法引导 |
| R-ROUTE-INCP-5 | 仓库缺失母本 / L1 SSOT，且用户需要从零开始一个新项目 | 启用 workflow | 进入 Phase 1 (Inception Intake) | 绿色通道 (临界 2) |
| R-ROUTE-INCP-6 | `/project-steward` 判定 State = `NO_PROJECT_SSOT` | 启用 workflow | 进入 Phase 1 (Inception Intake) | 管家分流 |
| R-ROUTE-INCP-7 | `/project-steward` 判定 State = `SSOT_NEEDS_REPAIR` 且需重建立项 | 启用 workflow | 进入 Phase 1 (Inception Intake) | 管家分流 (修复模式) |
| R-ROUTE-INCP-8 | 系统状态不清、下一步推进方向不明 | 停止并分流 | 路由至 `/project-steward` | 临界状态 1 |
| R-ROUTE-INCP-9 | 属于纯缺陷根因诊断 | 停止并分流 | 路由至 `diagnose` 技能 | 临界状态 3 |
| R-ROUTE-INCP-10 | 已拥有健康的母本（L1 SSOT），用户需要进行具体功能/需求开发 | 停止并分流 | 路由至 `/specs-write` 与 `/specs-execute` | 临界状态 4 |
| R-ROUTE-INCP-11 | 逻辑简单明确且适合 TDD 验证 | 停止并分流 | 路由至 `tdd` 技能或直接执行 | 临界状态 5 |
| R-ROUTE-INCP-12 | 以上皆不满足且非立项场景 | 不启用 workflow | 不启用本 workflow | 默认退出 |

## 0.1 主路径

```text
Phase 1 Inception Intake
  → Phase 2 Problem / Audience Discovery
  → Phase 3 Market / Alternative Hypothesis Capture
  → Phase 4 Product Positioning
  → Phase 5 Functional Model
  → Phase 6 UX / UI / Interaction Model
  → Phase 7 Architecture Seed
  → Phase 8 L1 SSOT Draft
  → Phase 9 Gate & Handoff
```

## 0.2 状态与路由汇总 (State / Route Summary)

| 状态 (State) | 判定 | 下一步 | Gate / DAG ID 映射 |
| ------- | ------ | -------- | --------------------- |
| `/project-inception:IDEA_INTAKE` | 只有模糊 idea、空白仓库或未成形方向 | 进入 Phase 1 | — |
| `/project-inception:SSOT_REPAIR_INTAKE` | 已有母本存在但不可派生，需要重建或修复项目级定位 | 定位 / 用户 / MVP 修复进入 Phase 1-4；功能模型修复进入 Phase 5；UX / UI 修复进入 Phase 6；架构种子修复进入 Phase 7 | 预装配 `HG-STRAT-{slug}-repair`（SSOT 修复 = 战略级动作） |
| `/project-inception:DISCOVERY_READY` | 目标用户、问题和项目类型已有初始假设 | 进入 Phase 2-3 | — |
| `/project-inception:BUSINESS_AUDIT_NEEDED` | 付费主体、替代方案、获客、MVP 投入或商业生死裁定风险高 | 分流 `/business-model-audit` | `R-AUDIT-5`（`../../specs-write/protocols/entry-decision-tree.md §7.5`） |
| `/project-inception:POSITIONING_READY` | 用户、问题、价值、MVP 与非目标已可成文 | 进入 Phase 5，并按 Phase 5 → 6 → 7 → 8 顺序推进 | — |
| `/project-inception:PRODUCT_MODEL_READY` | 功能模型与 UX / UI 模型已收敛，尚未形成架构种子 | 进入 Phase 7 | — |
| `/project-inception:ARCHITECTURE_SEED_READY` | 技术选型、系统边界与风险验证已收敛 | 进入 Phase 8 | 架构种子涵跨边界设计 → 预装配 `HG-DESIGN-{slug}-arch-seed` |
| `/project-inception:SSOT_DRAFT_READY` | L1 SSOT 草案已生成但未授权 | 进入 Phase 9 Gate | 创建 `DAG-N-SPEC-{slug}-l1-ssot` （status: Draft） |
| `/project-inception:SSOT_REPAIR_DRAFT_READY` | 修复草案已生成但未授权替换 Authoritative SSOT | 进入 Phase 9 Gate | 同上 + repair 标签 |
| `/project-inception:SSOT_PROPOSED` | L1 SSOT 草案已展示为权威候选，等待用户批准；未批准前不得报告 `/project-inception:AUTHORITATIVE_READY_RETURN` 或 `/project-inception:AUTHORITATIVE_ROUTE_TO_SPEC_READY` | 等用户批准 | `S-HG-4 WAITING_GATE_APPROVAL` + `HG-STRAT-{slug}-001`（母本权威化）；packet F-HG-1~8 必齐 |
| `/project-inception:AUTHORITATIVE_REPAIR_PROPOSED` | 修复草案已展示为权威替换候选，等待用户批准；未批准前不得替换 Authoritative SSOT | 等用户批准 | `S-HG-4` + `HG-STRAT-{slug}-repair`（原 Authoritative 被替换） |
| `/project-inception:AUTHORITATIVE_READY_RETURN` | 用户批准母本可作为上游，但未明确要求继续派生 feature spec | 返回 `/project-steward` | `S-HG-5 GATE_APPROVED` + `HG-STRAT-*` Approved；`DAG-N-SPEC-{slug}-l1-ssot` Done |
| `/project-inception:AUTHORITATIVE_ROUTE_TO_SPEC_READY` | 用户批准母本可作为上游，且明确要求继续编写首个 feature spec | 报告 route input；若同轮明确要求继续则分流 `/specs-write` | 同上 + route input（feature 候选 + Project Mode） |
| `/project-inception:GATE_APPROVAL_PENDING` | Strategy 或 Critical Design Gate 命中，需要用户裁决定位、MVP、技术栈、数据边界或核心 UX 路径 | 等用户裁决 | `S-HG-4` + Gate A → `HG-STRAT-*` / Gate B → `HG-DESIGN-*` |
| `/project-inception:REAL_WORLD_SIDE_EFFECT_APPROVAL_PENDING` | Gate C 命中，需要外部发布、真实用户调研、真实付费、生产账号或外部 API 承诺 | 等用户批准；不得执行真实动作 | `S-HG-4` + `HG-IRREV-*`（TTL-HG-6 单次执行不缓存） |
| `/project-inception:BLOCKED` | 关键事实缺失、授权被拒绝或上游冲突导致不能继续生成可批准母本 | 修当前草案、回上游或分流 | `S-HG-6 GATE_REJECTED` 或 `FA-HG-1`（如被拒绝） |

## 0.3 状态权威与路由动作 (State Authority / Route Action)

- **State Authority**：本表 State 只用于本 workflow 调度；母本权威状态只由用户批准后的 SSOT 文件或明确批准语句决定。
- **Route Action**：`进入 Phase` = `CONTINUE_IN_WORKFLOW`；`分流 / 返回 / 下游 handoff-ready` = `REPORT_AND_STOP`，除非用户明确要求继续；`展示草案 / 请求权威批准 / 等用户 / GATE_APPROVAL_PENDING / REAL_WORLD_SIDE_EFFECT_APPROVAL_PENDING` = `WAIT_FOR_USER`；创建 / 替换 Authoritative SSOT = `CONFIRMED_ACTION`，但只授权已展示并获批的母本写入或替换，不授权 feature spec 编写、代码修改、tracker 写入或真实世界副作用；进入 `/specs-write` 只是下游入口确认，下游必须重新执行自己的 Gate。

## 0.4 中断恢复事实源 (Resume Source)

| 恢复需求 (Resume Need) | 事实源 | 下一步判定 |
| ------------- | -------- | ------------ |
| 立项简报未完成 | Inception Brief + 用户原始 idea | 回 Phase 1-2 |
| 商业风险未闭环 | Hypothesis Capture 输出 + `Need Audit?` 判定 | 分流或恢复 `/business-model-audit` |
| 商业审计已返回 | `/business-model-audit` Return Contract + verdict + route input | 应用已批准修订；仅在新证据或 unresolved risk 出现时重新审计 |
| 母本草案未授权 | L1 SSOT Draft / Repair Draft + Gate 输出 | 等用户批准或修订草案 |
| 母本已批准 | Authoritative SSOT 路径 + 用户批准语句 | 返回 `/project-steward` 或按明确请求进入 `/specs-write` |

## 0.5 角色责任

AI 在本 workflow 中默认承担：

- **总设计师**：把分散想法收敛成 coherent project concept。
- **产品负责人**：界定用户、问题、价值、MVP 和非目标。
- **商业假设记录者**：记录付费意愿、市场替代、获客难度和商业风险的立项级假设；不输出商业生死裁定。
- **架构师**：提出技术选型与系统边界的早期判断。
- **UI / UX 设计师**：设计核心用户路径、信息架构、交互原则和界面方向。
- **SSOT 守护者**：确保母本能被 `/specs-write` 派生，而不是堆砌愿望清单。

## 0.6 阶段纪律

1. **从问题开始**：不得先沉迷技术栈或页面细节。
2. **先假设后验证**：所有商业、用户、技术判断必须标注置信度。
3. **母本不是 spec**：不产出 `requirements.md` / `design.md` / `tasks.md`。
4. **不伪造调研**：没有外部资料时，只能写“待验证假设”，不能假装市场事实。
5. **用户少问但关键必问**：AI 可主动提出推荐方案；只有 Strategy / Critical Design / Real-World Side Effect Gate 命中才停下让用户裁决。
6. **SSOT 修改需批准**：若已有 Authoritative SSOT，只能先给 Repair Draft / Stewardship Suggestions，不能静默覆盖。
