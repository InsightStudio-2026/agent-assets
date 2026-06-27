---
description: "将已批准的任务清单发布到 issue tracker工作流（/tasks-to-issues）专属的触发判定、状态转换路由、状态权威与动作决策矩阵"
---

# 任务发 Issue 决策矩阵（/tasks-to-issues）

## 0. 触发与临界路由决策表

| ID | 前置条件 | 匹配动作 | 下一步/目标路由 | 源 / 备注 |
| ---- | ---------- | ---------- | ----------------- | ----------- |
| R-ROUTE-TTI-1 | 用户显式 `/tasks-to-issues` | 启用 workflow | 进入 Phase 1 (Intake) | 显式入口 |
| R-ROUTE-TTI-2 | 用户要把已批准的 `tasks.md` 内的 feature Tasks 发布为可分发 issues | 启用 workflow | 进入 Phase 1 (Intake) | 任务导出 |
| R-ROUTE-TTI-3 | 用户要把 approved handoff plan、或已过门禁的战略/设计计划导出到外部 tracker | 启用 workflow | 进入 Phase 1 (Intake) | 计划导出 |
| R-ROUTE-TTI-4 | 系统状态不清、下一步推进方向不明 | 停止并重定向 | 路由至 `/project-steward` | 临界状态 1 |
| R-ROUTE-TTI-5 | 缺失母本或 L1 SSOT | 停止并重定向 | 路由至 `/project-inception` | 临界状态 2 |
| R-ROUTE-TTI-6 | 属于纯缺陷根因诊断（局部、具体 bug） | 停止并重定向 | 路由至 `diagnose` 技能 | 临界状态 3 |
| R-ROUTE-TTI-7 | 属于新功能、新需求开发、大重构落地（而非单纯的任务计划向 tracker 导出） | 停止并重定向 | 路由至 `/specs-write` 与 `/specs-execute` | 临界状态 4 |
| R-ROUTE-TTI-8 | 逻辑简单明确且适合 TDD 验证 | 停止并重定向 | 路由至 `tdd` 技能或直接执行 | 临界状态 5 |
| R-ROUTE-TTI-9 | 以上皆不满足，且无任务向 tracker 导出的需求 | 不启用 workflow | 不启用本 workflow | 默认退出 |

## 0.1 状态与路由汇总 (State / Route Summary)

| 状态 (State) | 判定 | 下一步 | Gate / DAG ID 映射 |
| ------- | ------ | -------- | --------------------- |
| `/tasks-to-issues:SOURCE_MISSING` | 没有 approved tasks / handoff / 满足最低事实源的 approved plan | 分流 `/specs-write` | `/specs-write:HANDOFF_READY` 上游缺 |
| `/tasks-to-issues:NO_TRACKER_CONFIG` | 源任务存在但缺 issue tracker 配置或标签词表 | 分流 `/repo-agent-setup` | 预装配 `HG-OPS-{repo}-context` |
| `/tasks-to-issues:SOURCE_READY` | 源任务、批准状态与 tracker 配置已确认 | 进入 Phase 2 | 读取 `DAG-N-TASK-{slug}-###` 全部节点；F-N-6/7 Depends On / Blocks 解析为 issue blocker 关系 |
| `/tasks-to-issues:ALREADY_PUBLISHED` | 源任务已有 external references 或 tracker 中已有对应 issue | 报告映射，收束到 `/tasks-to-issues:DONE`，不重复创建 | DAG-N-TASK-*F-N-5 已含 issue URL；不重复投影 |
| `/tasks-to-issues:DUPLICATE_RISK` | 无法确认是否已发布，或 tracker 中存在疑似重复 issue | 停下让用户裁决 | — |
| `/tasks-to-issues:DRAFT_READY` | issue 草案、依赖、AFK/HITL 标记已生成 | 等用户确认 | issue body 必须显式列 `DAG-N-TASK-*` ID + F-N-9 Gate Required（PRJ-6）；不让 issue 成为第二事实源 |
| `/tasks-to-issues:CONFIRMED_TO_PUBLISH` | 用户已确认 issue 粒度、依赖和 AFK/HITL 标记 | 进入 Phase 5；创建结果必须回读 provider 编号 / URL | tracker 写入 = 受限授权；不传递为 HG-*/ DAG-*跨 workflow 授权 |
| `/tasks-to-issues:PUBLISHED` | issues 已创建并打初始标签，待判断是否可回填 external references | 进入 Phase 6 | DAG-N-TASK-* F-N-5 += issue URL；F-N-6/7 → issue blocker 关系（DAG-E-BLK 投影） |
| `/tasks-to-issues:BACKFILL_SAFE_TO_APPLY` | 源文件明确允许记录 external references，回填位置可确认，且不会改 `Status` / `Execution Notes` | 回填 references | `S-HG-1 GATE_NOT_REQUIRED`（受限 safe-write，不改权威字段） |
| `/tasks-to-issues:BACKFILL_CONFIRMATION_REQUIRED` | 源文件是否允许回填或回填位置不明确 | 只报告映射，除非用户确认 | — |
| `/tasks-to-issues:PARTIAL_PUBLISHED` | 部分 issue 已创建，剩余因权限、网络或 tracker 冲突失败 | 停止批量发布，报告映射与失败项，等待用户裁决 | DAG-N-TASK-*部分投影成功；失败项保持 unreferenced |
| `/tasks-to-issues:PUBLISH_FAILED` | issue 写入失败且没有可确认的成功创建项 | 不回填源文件，报告失败与恢复建议 | — |
| `/tasks-to-issues:BACKFILL_SKIPPED` | 源文件无 external references 槽位或无法确认 | 只报告映射，收束到 `/tasks-to-issues:DONE` | — |
| `/tasks-to-issues:DONE` | 发布和可选回填完成 | 报告 `/tasks-to-issues:DONE` 后返回 `/project-steward` | DAG-N-TASK-* 全部投影到 issue（或部分 + 报告）；issue 是 DAG 投影，不是新事实源（PRJ-6） |

## 0.2 状态权威与路由动作 (State Authority / Route Action)

- **State Authority**：源任务的 `Status` / `Execution Notes` 仍由 `tasks.md` 和 `/specs-execute` 维护；发布后的 issue 状态流转归 `/issue-triage`。
- **Route Action**：`进入 Phase` = `CONTINUE_IN_WORKFLOW`；`/tasks-to-issues:BACKFILL_SAFE_TO_APPLY` = `CONTINUE_IN_WORKFLOW` with 受限 safe-write 例外（固定含义：exact target / existing slot / no authority escalation / no downstream authorization / report scope after write），只允许按源文件明示槽位回填 external references，且不得改 `Status` / `Execution Notes`；该例外不是 `CONFIRMED_ACTION`，不可传递到其他源文件、下游 workflow 或 issue 状态流转；`等用户确认 / 裁决 / BACKFILL_CONFIRMATION_REQUIRED` = `WAIT_FOR_USER`；`只报告映射 / 返回 / 分流` = `REPORT_AND_STOP`，除非用户明确要求继续；`/tasks-to-issues:ALREADY_PUBLISHED` 只可收束到 `/tasks-to-issues:DONE`，不得继续发布；`/tasks-to-issues:CONFIRMED_TO_PUBLISH` = `CONFIRMED_ACTION`，但只授权本次已展示的 issue 创建集合，不授权回填源文件、修改 issue 后续状态或执行下游 workflow。

## 0.3 中断恢复事实源 (Resume Source) 与伴生文档 (Companion Documents)

| 恢复需求 (Resume Need) | 事实源 | 下一步判定 |
| ------------- | -------- | ------------ |
| 源任务未确认 | Source path / approval status / tracker config | 回 Phase 1 |
| issue 草案待确认 | Draft Issue Set + dependency order + AFK/HITL 标记 | 等确认或修草案 |
| 发布中断 | 已创建 issue 映射 + provider 输出 | 停止批量发布，报告部分结果 |
| 回填未确认 | Issue Mapping + 源文件 external references 槽位 | 回填或只报告映射 |
| 发布完成 | Issue Mapping + Source Integrity | 返回 `/project-steward` |
