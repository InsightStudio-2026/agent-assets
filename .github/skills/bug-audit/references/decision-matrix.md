---
description: "缺陷审计工作流（/bug-audit）专属的触发判定、状态转换路由、状态权威与动作决策矩阵"
---

# 缺陷审计决策矩阵（/bug-audit）

## 0. AI Boot Sequence

### 0.1 触发与临界路由决策表

| ID | 前置条件 | 匹配动作 | 下一步/目标路由 | 源 / 备注 |
| ---- | ---------- | ---------- | ----------------- | ----------- |
| R-ROUTE-BGAU-1 | 用户显式 `/bug-audit` | 启用 workflow | 进入 Phase 1 (Bug Intake Normalization) | 显式入口 |
| R-ROUTE-BGAU-2 | 用户报告 bug，但明确要求仅记录到 tracker、进行状态跟踪而无需全面审计 | 停止并分流 | 路由至 `/issue-triage` | tracker 状态分流 |
| R-ROUTE-BGAU-3 | 用户报告 bug / 异常 / 回归 / 失败测试，且其影响面、严重性或系统性根因未知 | 启用 workflow | 进入 Phase 1 (Bug Intake Normalization) | 复杂缺陷审计 |
| R-ROUTE-BGAU-4 | `/project-steward` 判定 State = `BUG_REPORTED` 且性质复杂 | 启用 workflow | 进入 Phase 1 (Bug Intake Normalization) | 管家引流 |
| R-ROUTE-BGAU-5 | `review` 技能审查发现严重行为错误且影响面未知 | 启用 workflow | 进入 Phase 1 (Bug Intake Normalization) | 审查质量防线 |
| R-ROUTE-BGAU-6 | 系统状态不清、下一步推进方向不明 | 停止并重定向 | 路由至 `/project-steward` | 临界状态 1 |
| R-ROUTE-BGAU-7 | 缺失母本或 L1 SSOT | 停止并重定向 | 路由至 `/project-inception` | 临界状态 2 |
| R-ROUTE-BGAU-8 | 属于纯缺陷根因诊断（局部、简单、且影响面已知） | 停止并重定向 | 路由至 `diagnose` 技能 | 临界状态 3 |
| R-ROUTE-BGAU-9 | 逻辑简单明确且适合 TDD 验证（单模块/单测试、不改变 API / 契约 / Schema） | 停止并重定向 | 路由至 `tdd` 技能或直接执行 | 临界状态 5 |
| R-ROUTE-BGAU-10 | 修复确认需要变更数据库 Schema、API 契约或跨模块边界 | 停止并重定向 | 路由至 `/specs-write` 与 `/specs-execute` | 临界状态 4 |
| R-ROUTE-BGAU-11 | 以上皆不满足且非缺陷审计诉求 | 不启用 workflow | 不启用本 workflow | 默认退出 |

### 0.2 主路径

```text
Phase 1 Bug Intake Normalization
  → Phase 2 Reproduction Assessment
  → Phase 3 Blast Radius Audit
  → Phase 4 Severity & Risk Classification
  → Phase 5 Root Cause Hypothesis
  → Phase 6 Spec / SSOT Impact Review
  → Phase 7 Repair Path Decision
  → Phase 8 Regression & Verification Plan
  → Phase 9 Handoff
```

### 0.2.1 状态与路由汇总 (State / Route Summary)

| 状态 (State) | 判定 | 下一步 | Gate / DAG ID 映射 |
| ------- | ------ | -------- | --------------------- |
| `/bug-audit:INTAKE_NEEDED` | observed / expected / evidence 未标准化 | 进入 Phase 1 | 创建 `DAG-N-AUDIT-{bug-id}-bug` 节点（status: Intake） |
| `/bug-audit:REPRO_UNKNOWN` | 复现状态不明或信息不足 | 进入 Phase 2；若必须由用户补充复现 / 环境 / 影响面信息，则追问并等待 | F-N-5 Outputs += Reproduction Plan |
| `/bug-audit:BLAST_RADIUS_UNKNOWN` | 影响面未审清且可能复杂 | 进入 Phase 3 | F-N-5 += Blast Radius |
| `/bug-audit:INCIDENT_RISK` | S0/S1、生产、数据、安全、权限或计费风险 | 只输出止血 / rollback / hotfix plan，进入 `/bug-audit:INCIDENT_ACTION_APPROVAL_PENDING` | 预装配 `HG-INCIDENT-{bug-id}-001`；创建 `DAG-N-INCIDENT-*`；如需数据恢复 → `DAG-E-RBK` 指向 `DAG-N-ROLLBACK-DATA-*` |
| `/bug-audit:INCIDENT_ACTION_APPROVAL_PENDING` | 事故计划涉及生产、数据、安全、权限、计费或外部副作用 | 等用户批准；未批准不得执行真实动作，只能报告或返回 | `S-HG-4 WAITING_GATE_APPROVAL` + `HG-INCIDENT-*`（+ `HG-IRREV-*` 如涵不可逆动作）；TTL-HG-6 单次执行不缓存；失败 → `FA-HG-9` |
| `/bug-audit:INCIDENT_ROUTE_HANDOFF_READY` | 用户已批准事故处置入口动作，且路线、恢复边界与回归验证已明确 | 报告 route / entry input 后停止；真实执行由下游 workflow 或人工流程重新 Gate | `S-HG-5 GATE_APPROVED`（事故入口范围）；不继承给下游真实执行 |
| `/bug-audit:ROOT_CAUSE_UNKNOWN` | 可复现但根因仍是假设 | 分流 `diagnose` | DAG-N-AUDIT-*被 `diagnose` blocked（DAG-E-BLK） |
| `/bug-audit:DIAGNOSIS_RETURNED` | `diagnose` 已按 §5.4 返回完整诊断交接合同，但尚未判定上游影响 | 回 Phase 6 | F-N-5 += Root Cause Evidence |
| `/bug-audit:SPEC_REPAIR_NEEDED` | bug 暴露 spec / SSOT / 架构契约缺陷 | 分流 `/specs-write` 或 SSOT Repair | `R-AUDIT-4`（母本）或 `R-AUDIT-3`（ADR）；重塑 → 如跨契约 → 预装配 `HG-DESIGN-*` |
| `/bug-audit:SMALL_FIX_ROUTE_READY` | 影响面明确、可写回归测试、无上游缺陷、无高风险，且满足 §0.3 direct preconditions | 按 §0.3.1 分流 `diagnose` / `tdd` / direct small fix；本 workflow 不 patch | `S-HG-1 GATE_NOT_REQUIRED`（小 bug 不触发 HG-*） |
| `/bug-audit:ROUTED` | 唯一修复路线和回归计划已输出 | 返回 `/project-steward` | `DAG-N-AUDIT-{bug-id}-bug` Done；F-N-10 Done Evidence 填入 Repair Path + Regression Plan |

本表 `State` 为本 workflow 的 local suffix；任何报告、handoff 或 route 建议必须输出为 workflow-qualified state，例如 `/bug-audit:ROUTED`。

### 0.2.2 状态权威与路由动作 (State Authority / Route Action)

- **State Authority**：本表 State 只用于 bug 审计调度；issue 状态、spec 状态和 task 状态仍由各自事实源维护。
- **Route Action**：`进入 / 回 Phase` = `CONTINUE_IN_WORKFLOW`；`追问用户补复现 / 环境 / 影响面信息 / INCIDENT_ACTION_APPROVAL_PENDING` = `WAIT_FOR_USER`；`分流 / 返回 / INCIDENT_ROUTE_HANDOFF_READY` = `REPORT_AND_STOP`；`Incident` 或真实副作用命中时必须等待批准，批准事故处置入口动作才是 `CONFIRMED_ACTION`，且本 workflow 仍不得直接 patch 或执行真实副作用。

### 0.2.3 中断恢复事实源 (Resume Source)

| 恢复需求 (Resume Need) | 事实源 | 下一步判定 |
| ------------- | -------- | ------------ |
| bug intake 未清 | Bug Statement / 用户报告 / issue body | 补 Phase 1 |
| 复现或影响面未清 | Reproduction / Blast Radius 输出 | 补 Phase 2-3 |
| 事故计划待批 | Incident Plan + rollback / hotfix route + Gate C 风险 | 等批准或报告 `/bug-audit:INCIDENT_ROUTE_HANDOFF_READY` |
| 根因仍是假设 | Root Cause Hypotheses / Diagnose Return | 分流或恢复 `diagnose` |
| 上游影响未判定 | Spec / SSOT Impact 输出 + 相关 spec / SSOT 锚点 | 回 Phase 6 |
| 修复路线已清 | Repair Path + Regression & Verification | 报告 `/bug-audit:ROUTED`，不在本 workflow patch |

### 0.3 工作原则

1. **先审计，后修复**：影响面未知前，不急着改代码。
2. **复现优先**：能复现的问题优先最小复现；不能复现的问题标注置信度，不伪造结论。
3. **广度与深度分离**：先判断 blast radius，再判断可能根因。
4. **Simple 不重装**：小而明确的 bug 可以分流到 direct fix / `diagnose`，不强行开 spec；direct 只表示不启用重 workflow，不表示可以跳过复现、回归测试或 TDD。
5. **Complex 必升格**：跨模块、数据、权限、计费、安全、架构、需求歧义类 bug 必须考虑 `/specs-write`。
6. **回归测试必问**：每个真实 bug 都必须给 regression requirement。
7. **SSOT 优先**：若 bug 暴露需求 / 母本错误，先修上游，不静默用代码绕过。
8. **Direct 仍守纪律**：direct small fix 不得触及数据、权限、计费、安全、SSOT 或 spec；必须有最小复现或回归测试，且不得在根因仍未知、复现不足或无法写出回归测试时进入 `/bug-audit:SMALL_FIX_ROUTE_READY`，走 Red → Green → Refactor。实现中一旦发现影响面扩大、上游契约错误或无法写出回归测试，立即回到本 workflow 或分流 `/specs-write`。

### 0.3.1 Small Route 判定

| 条件 | Route |
| ------ | ------- |
| root cause known / blast radius bounded / regression test obvious | `tdd` 或 direct small fix with TDD discipline |
| root cause not proven / reproduction stable / blast radius bounded | `diagnose` |
| 修复会改变 contract / schema / 权限 / 计费 / 安全 / 跨模块行为 | `/specs-write` |
