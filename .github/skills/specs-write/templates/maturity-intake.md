# maturity-intake.md 模板

> **When to read**: The main workflow instructs Cascade to load this file when producing the Phase 0 file in `/specs-write` Phase 0.

## Phase 0 判定硬规则（落 spec 前必读）

- **Project Maturity 必先查**：仓库骨架 / 源代码 / DB schema / 测试 / docs SSOT / Project Archives / 历史 commit / 部署脚本，最少六维信号才能下 `Seed / Init` 或 `Greenfield` 判断；任一维存在真实负载 → 升级到 `Hybrid` / `Brownfield`。
- **模式判定**：
  - `Seed / Init`：仓库 / spec / 代码 / DB / 测试 / 归档基本为空，且当前任务是建立项目骨架 / 初始 SSOT / 第一批基础设施。
  - `Greenfield`：与既有系统物理隔离，但项目已有 README / .github/standards / CI / 测试约束 / 技术红线 / 母本 SSOT；Greenfield 不是"无现状"，必须审项目基础设施、共享规范、SSOT、测试 / CI、数据策略槽位。
  - `Hybrid`：本 spec 涉及领域内存在 ≥ 1 个既有模块 / 表 / 接口 / 路由 / UI 入口，同时有明显新建部分。
  - `Brownfield`：本 spec 主要修改 / 替换 / 扩展既有模块、表、接口、数据流或历史行为。
- **审计轮廓绑定**：`Seed / Init` → Baseline Survey；`Greenfield` → Greenfield Survey；`Hybrid` → Feature-Scoped Full-Surface Audit；`Brownfield` → Feature-Scoped Full-Surface Audit。`Hybrid` / `Brownfield` 必走 Phase 1.5；`Seed / Greenfield` 跳 Phase 1.5 但不得跳过 Baseline / Greenfield Survey 与 SSOT Health Check。
- **N/A 必须证据化**：Baseline / Greenfield Survey 中任何 N/A 都必须给 evidence 与 Future Audit Trigger；不得用"当前为空"替代证据。
- **SSOT Health 五态动作**：
  - `Healthy`：可进入 charter。
  - `Needs Clarification`：可进入 charter，但必须把不确定项列入 Blocking Issues / Open Questions，并按 Gate A/B/N/A 分类。
  - `Needs Repair`：不得继续派生 feature spec；先提交 Repair Draft，等待用户裁决或 SSOT 修复。
  - `Unfit As Source`：不得作为上游派生源；必须暂停并请求 Gate A 裁决替代来源 / 修复策略。
  - `SSOT Absent`：可进入 charter，但 charter 必须显式标注"SSOT 待建立"，列出 Open Questions 的 SSOT 重建计划，并在 SSOT Stewardship Suggestions 中给出草案。
- **SSOT 修改边界**：AI 有理解、审查、建议与 Repair Draft 草拟权；未获用户明确批准前，不得直接修改 Authoritative SSOT，也不得把 SSOT 修复静默倒灌为 feature 设计。

## Project Maturity & SSOT Health Intake — `<Feature Name>`

Feature Slug: `<feature-slug>`
Created At: `<ISO timestamp>`

## 0. Decision Summary

- Project Maturity: Seed / Init | Greenfield | Hybrid | Brownfield
- Audit Profile: Baseline Survey | Greenfield Survey | Feature-Scoped Full-Surface Audit
- SSOT Health: Healthy | Needs Clarification | Needs Repair | Unfit As Source | SSOT Absent
- Confidence: <0-100%>
- Decision: PROCEED_TO_CHARTER | PAUSE_FOR_GATE_A | BLOCKED_SSOT_REPAIR | BLOCKED_UNFIT_SOURCE
- Reason: <3-7 句，必须指向下方 evidence>

## 1. Project Maturity Evidence

| 面 | 当前状态 | Evidence | Interpretation | Next Required Decision |
| ---- | ---------- | ---------- | ---------------- | ------------------------ |
| Repository Skeleton | `<empty/minimal/mature>` | `<evidence file or command>` | <说明> | <N/A 或需决策> |
| Source Code | <none/minimal/has modules> | `<fd/find result>` | <说明> | <N/A 或需决策> |
| Database / Schema | <none/schema only/live db> | `<schema/db readback>` | <说明> | <N/A 或需决策> |
| Tests / CI | `<none/minimal/established>` | `<tests/ci evidence>` | <说明> | <N/A 或需决策> |
| Docs / SSOT | `<absent/draft/healthy>` | `<doc anchors>` | <说明> | <N/A 或需决策> |
| Archives / History | `<none/sparse/rich>` | `<archive scan>` | <说明> | <N/A 或需决策> |
| Runtime Commands | <unknown/not runnable/runnable> | `<command dry check>` | <说明> | <N/A 或需决策> |

## 2. Baseline / Greenfield Survey（Seed / Greenfield 必填；Hybrid / Brownfield 可 N/A）

| 面 | Current Blank / Baseline State | Evidence | Future Audit Trigger |
| ---- | ------------------------------- | ---------- | ---------------------- |
| Code | <无 src / 有脚手架 / 有共享模块> | `<evidence>` | <一旦出现何物则进入 14 面审计> |
| DB | <无 DB / schema only / live DB> | `<evidence>` | <触发条件> |
| Tests | <无 tests / 有 test stack> | `<evidence>` | <触发条件> |
| CI / DoD | <无 / 有 lint/test/drift> | `<evidence>` | <触发条件> |
| Docs SSOT | <无 / 草稿 / 健康> | `<evidence>` | <触发条件> |
| Runtime | <无入口 / 有启动命令> | `<evidence>` | <触发条件> |

## 3. SSOT Health Check

| 维度 | Status | Evidence | Issue | Recommendation |
| ------ | -------- | ---------- | ------- | ---------------- |
| 目标清晰度 | PASS/WARN/FAIL/N/A | `<anchor>` | <问题> | <建议> |
| 范围边界 | PASS/WARN/FAIL/N/A | `<anchor>` | <问题> | <建议> |
| 术语一致性 | PASS/WARN/FAIL/N/A | `<anchor>` | <问题> | <建议> |
| 需求闭环 | PASS/WARN/FAIL/N/A | `<anchor>` | <问题> | <建议> |
| 架构可行性 | PASS/WARN/FAIL/N/A | `<anchor>` | <问题> | <建议> |
| 数据/契约完整性 | PASS/WARN/FAIL/N/A | `<anchor>` | <问题> | <建议> |
| 质量红线 | PASS/WARN/FAIL/N/A | `<anchor>` | <问题> | <建议> |
| 迁移与演进 | PASS/WARN/FAIL/N/A | `<anchor>` | <问题> | <建议> |
| 风险与未知 | PASS/WARN/FAIL/N/A | `<anchor>` | <问题> | <建议> |

## 4. Blocking Issues

- BI-001: <必须先裁决或修复的问题>
  - Gate: A | B | N/A
  - Recommended Action: <AI 强推荐>
  - Alternatives: <≤2 个备选>
  - Cost of Delay / Wrong Decision: <代价>

## 5. SSOT Stewardship Suggestions（AI 缺省建议）

- SUG-001:
  - Target SSOT: `<path>#<section>` | new section needed | SSOT absent
  - Problem: <AI 认为母本/SSOT 可更优之处>
  - Default Recommendation: <AI 强推荐方案>
  - Alternatives: <≤2 个备选，可 N/A>
  - User Approval Required: yes | no
  - Can Proceed Without Applying: yes | no

## 6. Repair Draft（Needs Repair / Unfit 时必填）

- Proposed SSOT Patch:
  - Target: `<path>#<section>`
  - Change Summary: <建议如何补目标/术语/边界/契约/验收>
  - User Decision Needed: yes/no
  - Approval Boundary: 未获用户明确批准前，不得直接修改 Authoritative SSOT；本 patch 仅为草案

## 6.5 Critical Assumptions Summary

> Phase 0 本身常含强假设（如「本项目成熟度仍在 Seed/Init」 / 「SSOT 其他未阅读章节不影响本 feature」）；不得隐藏。

- 至少 1 条，最多 3 条；每条标注 `Confidence: <high|mid|low>` 与 `Validation: <如何验证>`。
- 或填 `N/A: <为何 Phase 0 无 Critical Assumption>`，并在同行接写必填理由（如「全量证据面均已验证，不依赖假设」）。
- 空话黑名单（§0.5）在本节同样生效。

## 7. Approval

- Status: Draft | Approved | Blocked
- Notes: <用户原话 或 AI-DRI auto-approved 留痕，详 §3.2.3>
- Timestamp: <ISO 8601>
