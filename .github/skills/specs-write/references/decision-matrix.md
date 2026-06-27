---
description: "规格编写工作流（/specs-write）专属的触发判定、状态转换路由、状态权威与动作决策矩阵"
---

# 规格编写决策矩阵（/specs-write）

## 0. 触发与临界路由决策表

| ID | 前置条件 | 匹配动作 | 下一步/目标路由 | 源 / 备注 |
| ---- | ---------- | ---------- | ----------------- | ----------- |
| R-ROUTE-SPWR-1 | 用户显式 `/specs-write` | 启用 workflow | 进入 Phase 0 (Maturity & SSOT Intake) | 显式入口 |
| R-ROUTE-SPWR-2 | 用户请求锁定为新 feature / 复杂变更且满足 `../protocols/entry-decision-tree.md` 中 §1.2 「必走」清单 | 启用 workflow | 进入 Phase 0 (Maturity & SSOT Intake) | 契约变更必走 |
| R-ROUTE-SPWR-3 | 用户请求具有健康上游母本，且要进行具体新功能开发、大重构落地或跨模块契约变更 | 启用 workflow | 进入 Phase 0 (Maturity & SSOT Intake) | 典型新特性开发 |
| R-ROUTE-SPWR-4 | 用户请求锁定为 Small/无需 Spec 变更且满足 `../protocols/entry-decision-tree.md` 中 §1.2 「跳过」清单 | 退出并重定向 | 按一般指令/直接回答处理 | 跳过清单 |
| R-ROUTE-SPWR-5 | 系统状态不清、下一步推进方向不明 | 停止并重定向 | 路由至 `/project-steward` | 临界状态 1 |
| R-ROUTE-SPWR-6 | 缺失母本或 L1 SSOT | 停止并重定向 | 路由至 `/project-inception` | 临界状态 2 |
| R-ROUTE-SPWR-7 | 属于纯缺陷根因诊断 | 停止并重定向 | 路由至 `diagnose` 技能 | 临界状态 3 |
| R-ROUTE-SPWR-8 | 逻辑简单明确且适合 TDD 验证 | 停止并重定向 | 路由至 `tdd` 技能或直接执行 | 临界状态 5 |
| R-ROUTE-SPWR-9 | 以上条件未命中，且请求意图不确定 | 停下并询问 | 询问用户是否启用 `/specs-write`，等待回应 | 兜底人机交互门 |

## 0.1 状态与路由汇总 (State / Route Summary)

| 状态 (State) | 判定 | 下一步 | Gate / DAG ID 映射 |
| ------- | ------ | -------- | --------------------- |
| `/specs-write:NO_HEALTHY_SSOT` | 缺母本、SSOT 不健康或 source 不可派生 | 停下修上游；按缺陷归属分流 `/project-inception` / `/grill-with-docs` / `/business-model-audit` | `R-PHASE0-3~5` + `R-AUDIT-3/4/5`（`../protocols/entry-decision-tree.md §7.2 + §7.5`） |
| `/specs-write:CHARTER_READY` | scope、source、复杂度和非目标已明确 | 进入 audit 或 requirements | `R-PHASE0-1/2`；charter 产出同时创建 `DAG-N-SPEC-{slug}-charter` |
| `/specs-write:AUDIT_REQUIRED` | Hybrid / Brownfield 且本 feature 派生所需现状证据未审清 | 进入 Phase 1.5 | `R-MODE-1/2`；启动 `HG-AUDIT-{slug}-001` packet（F-HG-5 = 14 面 + 两强证据面 ≥ 80% + Overall ≥ 80%） |
| `/specs-write:EXTERNAL_AUDIT_REQUIRED` | 发现问题超出本 feature 派生范围，属于架构 / 缺陷 / 商业 / SSOT 修复审计 | 分流对应 workflow | `R-AUDIT-1~5`（`../protocols/entry-decision-tree.md §7.5`） |
| `/specs-write:APPROVAL_PENDING` | 当前 Phase 产物已完成但 Gate A/B/C 需要用户白名单批准句；输出必须列 Current Phase / Gate / Blocking Fact Source / Required Decision | 等待批准，不进入下一 Phase | `S-HG-4 WAITING_GATE_APPROVAL`；Gate A → `HG-STRAT-*` / Gate B → `HG-DESIGN-*` / Gate C → `HG-IMPL-*` / Irreversible → `HG-IRREV-*`（`R-INH-1~4`） |
| `/specs-write:CURRENT_GATE_APPROVED` | 当前 Phase Gate 通过或用户白名单批准已记录 | 进入下一 Phase；不代表整份 spec 可执行 | `S-HG-5 GATE_APPROVED`；该 Phase 对应 `HG-*` ID 进 `Approved` 状态 |
| `/specs-write:REQUIREMENTS_READY` | REQ / AC / BDD 可审查且 Gate 通过 | 进入 design 或 Medium tasks | `DAG-N-SPEC-{slug}-requirements` Done；如命中 Gate → `S-HG-8 GATE_PASSED` |
| `/specs-write:DESIGN_READY` | DSN / INV / 失败策略可追溯且 Gate 通过 | 进入 tasks | `DAG-N-SPEC-{slug}-design` Done；跨边界 DSN → `HG-DESIGN-*` Approved |
| `/specs-write:TASKS_READY` | Task 可独立执行、测试、回滚 | 进入 handoff | `DAG-N-TASK-{slug}-###` 批量创建；F-N-6/7/9 Depends On / Blocks / Gate Required 字段齐 |
| `/specs-write:HANDOFF_READY` | 人读简报与 `handoff-payload.yaml` 已生成，可交接给 `/specs-execute`；不表示下游已执行或已获真实副作用授权 | 报告 handoff-ready；默认不自动执行下游 | `DAG-N-SPEC-{slug}-handoff` Done；handoff-payload `traceability` / `first_task` / `critical_contracts` 齐 |
| `/specs-write:GATE_BLOCKED` | 用户拒绝 Gate 决策、批准语句不完整或授权过期 | 修当前文件或回跳上游 | `S-HG-6 GATE_REJECTED` 或 `S-HG-7 GATE_EXPIRED` + `FA-HG-1/2/3`（按 Gate domain） |
| `/specs-write:BLOCKED` | Spec Breach 或硬阻塞命中；输出必须列阻塞事实源、受影响文件和所需裁决 | 修当前文件或回跳上游 | —（取决于阻塞性质；如上游质量问题 → 可能触发 `R-RETURN-1` → `/specs-execute` 回切） |

`/specs-write:NO_HEALTHY_SSOT` 归属判定：项目定位 / 用户 / MVP → `/project-inception`；术语 / ADR / 领域关系 → `/grill-with-docs`；商业闭环 / 付费 / 替代方案 → `/business-model-audit`；仅本 feature 现状证据不足且上游健康 → 补 Phase 1.5。

`/specs-write:EXTERNAL_AUDIT_REQUIRED` 归属判定：

| 事实依据 (Evidence) | 目标路由 (Route) |
| ---------- | ------- |
| seam / interface / module depth / refactor sequence 不清 | `/architecture-audit` |
| observed bug / failing test / blast radius 未知 | `/bug-audit` |
| buyer / alternative / payment / distribution / MVP ROI 不清 | `/business-model-audit` |
| terminology / ADR / domain relation conflict | `/grill-with-docs` |
| project positioning / target user / MVP 母本缺陷 | `/project-inception` |

外部审计返回后，只有产物包含 Return Contract（target route / entry input / resolved / still blocked / not authorized / resume source）以及原阻塞证据的复判结果，才可回到本 workflow 继续派生。

本表 `State` 为本 workflow 的 local suffix；任何报告、handoff 或 route 建议必须输出为 workflow-qualified state，例如 `/specs-write:HANDOFF_READY`。Gate / DAG ID 详 `../protocols/gate-dag-protocol.md`：HG-*§1 + S-HG-* §1.3 + R-INH-*§1.4 + FA-HG-* §1.5 + DAG-N-*§2.3 + F-N-* §2.3；R-* 详 `../protocols/entry-decision-tree.md §7`。术语不更名；表中 ID 为机读字面映射，不引入状态机双轨。

## 0.2 状态权威与路由动作 (State Authority / Route Action)

- **State Authority**：spec 目录文件与 `handoff-payload.yaml` 是合同事实源；本表 State 只用于 spec 编写调度。
- **Route Action**：`进入 Phase / 修当前文件` = `CONTINUE_IN_WORKFLOW`；`等待批准` = `WAIT_FOR_USER`；`分流 / 回跳上游 / handoff-ready / 切换下游` = `REPORT_AND_STOP`，除非用户明确要求继续。`/specs-write:CURRENT_GATE_APPROVED` 只表示当前 Phase Gate 通过，不等于整份 spec 可执行；可执行性由 `/specs-write:HANDOFF_READY`、文件 Approval 状态与 `/specs-execute` 前置检查共同判定。任何 `WAIT_FOR_USER` / `/specs-write:BLOCKED` 输出必须列 Current Phase、Gate or Blocker、Fact Source、Required Decision。最终报告必须使用 workflow-qualified state。

## 0.3 中断恢复事实源 (Resume Source)

| 阶段状态 (Phase State) | 权威文件 | 最小判定字段 |
| ------------- | ---------- | -------------- |
| `/specs-write:CHARTER_READY` | `charter.md` | scope / source / complexity / Gate 或 Approval Notes |
| `/specs-write:AUDIT_REQUIRED` / `/specs-write:EXTERNAL_AUDIT_REQUIRED` | `maturity-intake.md` + `audit.md`（Hybrid / Brownfield） | Audit Profile / EXIST-* / Audit Depth Gate / Blocking Unknowns |
| `/specs-write:EXTERNAL_AUDIT_REQUIRED` | 外部审计报告（`/architecture-audit` / `/bug-audit` / `/business-model-audit` / `/grill-with-docs`）+ 原阻塞证据 | Return Contract + 原阻塞证据复判；若已解决，回当前 Phase 复判 |
| `/specs-write:REQUIREMENTS_READY` | `requirements.md` | REQ / AC / BDD Scenario / Derivation Map / Gate |
| `/specs-write:DESIGN_READY` | `design.md` | DSN-*/ INV-* / Failure Strategy / Alternatives / Gate |
| `/specs-write:TASKS_READY` | `tasks.md` | Task headers / Dependencies / Verification Commands / Revert / DoD |
| `/specs-write:HANDOFF_READY` | `handoff-payload.yaml` + `tasks.md` | first_task / traceability / critical_contracts / Approval 状态 |

## 0.4 每阶段三铁律

1. **一次一件**（charter / audit / requirements / design / tasks / handoff），产完即做 Gate 判定；产出同时创建对应 `DAG-N-SPEC-{slug}-{phase}` 节点，F-N-9 Gate Required 列必填
2. **必停时机**（见 `stop-conditions.md`）：只限 Gate A/B/C 或硬阻塞（对应 `S-HG-2 GATE_REQUIRED` 或 `S-HG-4 WAITING_GATE_APPROVAL`），不因"文件写完"自动停
3. **Gate 命中才要白名单批准**；未命中时 AI-DRI 自动推进（`S-HG-1 GATE_NOT_REQUIRED`）。留痕规则 = `cross-cutting.md §2.3`；Gate 命中 → 装配 packet（F-HG-1~8 齐）→ `S-HG-4 WAITING_GATE_APPROVAL`

## 0.5 输出骨架 / Critical Assumptions

每件交付的三段输出、Critical Assumptions Summary 和 Gate 后续动作详见 `../protocols/orchestration.md`。每次 Phase 汇报必须包含 `Authority / Fact Source`：当前权威文件、上游 source / SSOT 锚点、Gate / Approval 事实源、下一步是否只是 `REPORT_AND_STOP`；并包含 `Authorization Boundary`：Route Action、authorized scope、not authorized（代码修改 / 迁移执行 / tracker 写入 / 真实世界副作用 / 下游 workflow 自动执行）。

## 0.6 Forbidden Actions（全局禁令）

详见 `../protocols/forbidden-actions.md`。
