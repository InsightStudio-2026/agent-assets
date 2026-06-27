---
description: "规格执行工作流（/specs-execute）专属的触发判定、状态转换路由、状态权威与动作决策矩阵"
---

# 规格执行决策矩阵（/specs-execute）

## 0. 触发与临界路由决策表

| ID | 前置条件 | 匹配动作 | 下一步/目标路由 | 源 / 备注 |
| ---- | ---------- | ---------- | ----------------- | ----------- |
| R-ROUTE-SPEX-1 | 用户显式 `/specs-execute TASK-###` | 启用 workflow | 进入 Phase 1 (Locate Task) | 显式入口 |
| R-ROUTE-SPEX-2 | 用户请求为“继续任务 / 执行下一个 Task”，且存在 approved spec 和 Pending/In Progress Task | 启用 workflow | 进入 Phase 1 (Locate Task) | 任务流转 |
| R-ROUTE-SPEX-3 | 无 approved spec，或无任何 Pending/In Progress 的可执行 Task | 停止并重定向 | 路由至 `/specs-write` 或 `/project-steward` | 契约缺失 |
| R-ROUTE-SPEX-4 | 系统状态不清、下一步推进方向不明 | 停止并重定向 | 路由至 `/project-steward` | 临界状态 1 |
| R-ROUTE-SPEX-5 | 缺失母本或 L1 SSOT | 停止并重定向 | 路由至 `/project-inception` | 临界状态 2 |
| R-ROUTE-SPEX-6 | 失败测试、CI 红灯、bug-audit handoff 或 bug 报告，且影响面未知或非当前 Task 引起 | 停止并重定向 | 路由至 `/bug-audit` | 缺陷过滤 |
| R-ROUTE-SPEX-7 | 属于纯缺陷根因诊断（局部简单 Bug），但非 spec/需求契约级缺陷 | 停止并重定向 | 路由至 `diagnose` 技能 | 临界状态 3 |
| R-ROUTE-SPEX-8 | 逻辑简单明确（单模块/单函数、不涉契约/Schema），且适合 TDD 验证 | 停止并重定向 | 路由至 `tdd` 技能或直接执行 | 临界状态 5 |
| R-ROUTE-SPEX-9 | 仅为临时需求变更、修 Spec 文本、纯查询或代码阅读咨询 | 停止并重定向 | 路由至 `/specs-write` 或 `/project-steward` | 契约偏离 |

## 0.1 状态与路由汇总 (State / Route Summary)

| 状态 (State) | 判定 | 下一步 | Gate / DAG ID 映射 |
| ------- | ------ | -------- | --------------------- |
| `/specs-execute:NO_APPROVED_SPEC` | 无 approved spec 或无可执行 Task | 分流 `/specs-write` 或 `/project-steward` | — |
| `/specs-execute:TASK_LOCATED` | 唯一 Task 已定位且前置检查通过 | 进入 Phase 2 | `DAG-N-TASK-{Task ID}` owner 为 `/specs-execute`；F-N-9 Gate Required 列锁定 |
| `/specs-execute:IN_PROGRESS` | Task 已进入执行闭环 | 继续 Red → Green → Refactor → Verify | `DAG-N-TASK-*` 状态 = 执行中；如 `Gate Required` 非空 → 同时调起 `S-HG-2 GATE_REQUIRED` |
| `/specs-execute:PAUSE_AND_ASK_PENDING` | 权限、生产副作用、真实 DB、外部 API、不可逆操作或 Pause-and-Ask 命中 | 等用户裁决 | `S-HG-4 WAITING_GATE_APPROVAL` + `HG-IRREV-001~004`（详 §3.2） |
| `/specs-execute:ENVIRONMENT_BLOCKED` | 测试环境、依赖、权限或本地工具链阻塞，且非 Spec 缺陷 | 按 `../protocols/blocking-and-rollback.md` 处理或等待用户裁决 | —（如需操作真实权限 / 生产资源 → 升级 `HG-IRREV-001` packet） |
| `/specs-execute:ROLLBACK_REQUIRED` | 本 Task 写入导致不可接受风险或验证失败需回滚 | 若已有批准的 Revert Command 且不触及真实副作用，执行回滚计划并重新判定；否则等待用户裁决 | `S-HG-9 GATE_FAILED` + `FA-HG-5`；`DAG-E-RBK` 激活 `DAG-N-ROLLBACK-TASK-{Task ID}`（详 §10 §1.1） |
| `/specs-execute:BLOCKED` | 上游锚点失效、Touches 越界或其他硬阻塞；输出必须列阻塞锚点、受影响 Touches 和事实源 | 按 `../protocols/blocking-and-rollback.md` 处理 | —（取决于阻塞性质：如 Touches 越界 → 可能触发 `R-RETURN-2` |
| `/specs-execute:SPEC_REPAIR_REQUIRED` | 需求 / 设计 / SSOT 缺陷导致不能安全执行 | 回切 `/specs-write` | `R-RETURN-1~5`（`../../specs-write/protocols/entry-decision-tree.md §7.6`） |
| `/specs-execute:TASK_DONE` | Verification / DoD 全 PASS 且无 Pause-and-Ask 未决 | 更新 tasks.md 并报告 | `DAG-N-TASK-*` F-N-10 Done Evidence 已填；如关联 `HG-*` → `S-HG-8 GATE_PASSED` |
| `/specs-execute:CLOSEOUT_READY` | 全 Task Done 且需归档 / artifacts 核验 | 执行 Phase 9 交付收尾 | `R-CLOSEOUT-1`（`../../specs-write/protocols/entry-decision-tree.md §7.8`） |
| `/specs-execute:CLOSEOUT_DONE` | 交付收尾完成 | 返回 `/project-steward` | `R-CLOSEOUT-3`（git mv active → done 完成后） |

本表 `State` 为本 workflow 的 local suffix；任何报告、handoff 或 route 建议必须输出为 workflow-qualified state，例如 `/specs-execute:TASK_DONE`。Gate / DAG ID 详 `../../specs-write/protocols/gate-dag-protocol.md`：HG-*§1 + S-HG-* §1.3 + F-N-*§2.3 + DAG-E-* §2.4 + FA-HG-*§1.5 + RG-* §3.2。术语不更名；表中 ID 为机读字面映射，不引入状态机双轨。

## 0.2 状态权威与路由动作 (State Authority / Route Action)

- **State Authority**：`tasks.md` Status / Execution Notes 与 `handoff-payload.yaml` 是执行事实源；本表 State 只用于单 Task 调度。
- **Route Action**：`继续 / 执行 Phase` = `CONTINUE_IN_WORKFLOW`；`已批准且无真实副作用的本地回滚计划` = `CONFIRMED_ACTION`，只授权当前 Task 的 Revert Command 与 Execution Notes 更新，不授权真实副作用回滚、spec 修改、下游 workflow 或其他 Task；`等用户裁决 / 未批准回滚 / 涉及真实副作用回滚` = `WAIT_FOR_USER`；`回切 / 分流` = `REPORT_AND_STOP`；`/specs-execute:TASK_DONE` 只在 Verification / DoD 全 PASS 后成立。

## 0.3 中断恢复事实源 (Resume Source)

| 恢复需求 (Resume Need) | 事实源 | 下一步判定 |
| ------------- | -------- | ------------ |
| Task 定位未完成 | `tasks.md` + `handoff-payload.yaml` | 回 Phase 1 |
| 执行中断 | `tasks.md` Status / Execution Notes + 最近 Verification 输出 | 恢复 Phase 4-7 或进入阻塞处理 |
| Pause-and-Ask 未决 | 最近一次 Pause-and-Ask 问题 + 用户裁决 | 等待或继续对应 Phase |
| Verification / 回滚失败 | 命令输出 + Execution Notes + Revert Command | 修复、回滚或判定 `/specs-execute:BLOCKED` |
| 交付收尾未完成 | 全 Task Status + Artifacts 声明 + 归档状态 | 进入 Phase 9 |

## 0.4 与 `/specs-write` 的边界

| 动作 | `/specs-write` | `/specs-execute` |
| ------ | ---------------- | ------------------- |
| 写/修 `requirements.md` / `design.md` / 追溯链主体 | ✅ | ❌ |
| 写业务代码 / 测试 / 迁移 / 跑 Verification | ❌ | ✅ |
| 更新 tasks.md Status / Execution Notes | ⚠️ 占位 | ✅ |
| 创建 Spec 新版本（Superseded） | ✅ | ❌ 必回切 |
