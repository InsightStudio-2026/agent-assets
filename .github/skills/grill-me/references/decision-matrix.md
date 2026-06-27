---
description: "领域语言挑战与文档守护工作流（/grill-with-docs）专属的触发判定、状态转换路由、状态权威与动作决策矩阵"
---

# 领域语言挑战与文档守护决策矩阵（/grill-with-docs）

## 0. 触发与临界路由决策表

| ID | 前置条件 | 匹配动作 | 下一步/目标路由 | 源 / 备注 |
| ---- | ---------- | ---------- | ----------------- | ----------- |
| R-ROUTE-GWD-1 | 用户显式 `/grill-with-docs` | 启用 workflow | 进入 Phase 1 (Intake) | 显式入口 |
| R-ROUTE-GWD-2 | 用户要求压力测试计划、澄清术语，且仓库存在领域文档 | 启用 workflow | 进入 Phase 1 (Intake) | 文档拷问诉求 |
| R-ROUTE-GWD-3 | `/project-steward` 推荐进行压力测试、文档澄清或 SSOT 修复 | 启用 workflow | 进入 Phase 1 (Intake) | 管家引流 |
| R-ROUTE-GWD-4 | 系统状态不清、下一步推进方向不明 | 停止并重定向 | 路由至 `/project-steward` | 临界状态 1 |
| R-ROUTE-GWD-5 | 缺失母本或 L1 SSOT | 停止并重定向 | 路由至 `/project-inception` | 临界状态 2 |
| R-ROUTE-GWD-6 | 属于纯缺陷根因诊断（局部、具体 bug） | 停止并重定向 | 路由至 `diagnose` 技能 | 临界状态 3 |
| R-ROUTE-GWD-7 | 属于新功能、新需求开发、大重构落地 | 停止并重定向 | 路由至 `/specs-write` 与 `/specs-execute` | 临界状态 4 |
| R-ROUTE-GWD-8 | 逻辑简单明确且适合 TDD 验证 | 停止并重定向 | 路由至 `tdd` 技能或直接执行 | 临界状态 5 |
| R-ROUTE-GWD-9 | 以上皆不满足且无文档打磨澄清需求 | 不启用 workflow | 不启用本 workflow | 默认退出 |

## 0.1 状态与路由汇总 (State / Route Summary)

| 状态 (State) | 判定 | 下一步 | Gate / DAG ID 映射 |
| ------- | ------ | -------- | --------------------- |
| `/grill-with-docs:DISCOVERING_DOMAIN` | 正在读取 `CONTEXT.md` / ADR / SSOT | 进入 Phase 2 | 创建 `DAG-N-AUDIT-{slug}-domain` 节点（status: Discovering） |
| `/grill-with-docs:QUESTION_PENDING` | 一个领域问题已抛出，等待用户回答 | 不继续追问 | — |
| `/grill-with-docs:ANSWER_RECEIVED` | 用户已回答领域问题但尚未复判代码 / 文档冲突 | 回 Phase 2 | F-N-5 Outputs += 用户回答 |
| `/grill-with-docs:CONSENSUS_REACHED` | 术语、关系或决议已达成共识 | 判定目标文档权限 | F-N-5 += 共识记录 |
| `/grill-with-docs:DOMAIN_DOC_CREATE_NEEDED` | 目标项目缺普通 `CONTEXT.md` / ADR 目录且已达成共识 | 草拟创建 patch，等待批准 | 预装配 patch 草案；不直接绑 HG-*（受限 safe-write） |
| `/grill-with-docs:ADR_CANDIDATE_READY` | ADR 三条件全满足，ADR 草案已生成 | 判定是否已有新建 ADR 预授权；无预授权则进入 `/grill-with-docs:ADR_APPROVAL_PENDING` | 预装配 `HG-DESIGN-{slug}-adr-{nnn}` packet（ADR = design-level decision） |
| `/grill-with-docs:ADR_APPROVAL_PENDING` | 新建 ADR 或 ADR 目标位置 / 编号 / 状态需确认 | 等用户批准 | `S-HG-4 WAITING_GATE_APPROVAL` + `HG-DESIGN-{slug}-adr-{nnn}`；R-INH-2 继承 Gate B；packet F-HG-1~8 必齐 |
| `/grill-with-docs:ADR_WRITTEN` | ADR 已按批准范围写入 | 输出报告并收束到 `/grill-with-docs:DONE` | `S-HG-5 GATE_APPROVED`；DAG-N-AUDIT-* Done |
| `/grill-with-docs:ORDINARY_PATCH_DRAFTED` | 已存在普通领域文档的小补丁已草拟，且不触及 L1 SSOT / standards / feature spec，并且对话中已达成术语共识 | 判定是否安全写入 | `S-HG-1 GATE_NOT_REQUIRED`（普通领域文档小补丁、受限 safe-write） |
| `/grill-with-docs:ORDINARY_PATCH_SAFE_TO_APPLY` | 小补丁目标、位置、事实源和权限均已确认；不新建文档、大改、不触及权威文档、不改变行为承诺或验收 | 仅写入该小补丁，并在报告中列出 safe-write scope | `S-HG-1 GATE_NOT_REQUIRED`；受限 safe-write 不升级为 CONFIRMED_ACTION 跨 workflow |
| `/grill-with-docs:DOMAIN_DOC_UPDATED` | 普通 `CONTEXT.md` 已按共识更新 | 输出报告 | DAG-N-AUDIT-* F-N-5 += 已更新文件 + 章节 |
| `/grill-with-docs:SSOT_APPROVAL_REQUIRED` | 涉及 L1 SSOT / standards 权威章节 | 输出 Proposed SSOT Patch，等待批准 | `S-HG-4` + `HG-STRAT-{slug}-ssot-patch`（L1 SSOT 修订 = 战略级）；R-INH-1 继承 Gate A |
| `/grill-with-docs:PATCH_APPROVED` | Proposed SSOT Patch 已获批准且目标文件可改 | 仅按批准 patch 更新 | `S-HG-5 GATE_APPROVED`；HG-STRAT-*Approved；DAG-N-AUDIT-* Done |
| `/grill-with-docs:PATCH_DECLINED` | 用户拒绝权威修订 | 记录取舍并返回或分流 | `S-HG-6 GATE_REJECTED` + `FA-HG-1` |
| `/grill-with-docs:ROUTED_TO_SSOT_REPAIR` | 冲突需要进入 spec / 项目定位 / 母本修复流程 | 按冲突归属分流 | `R-AUDIT-3`（ADR / 领域）或 `R-AUDIT-4`（母本）；`/specs-write` Phase 0 R-PHASE0-3~5 |
| `/grill-with-docs:DONE` | 文档更新或建议已交付 | 报告 `/grill-with-docs:DONE` 后返回 `/project-steward` | DAG-N-AUDIT-{slug}-domain Done；F-N-10 Done Evidence 填入 Resolved + Updated Files |

## 0.2 状态权威与路由动作 (State Authority / Route Action)

- **State Authority**：普通 `CONTEXT.md` / ADR 写入后是领域文档事实源；L1 SSOT、standards、feature spec 的权威状态仍由各自 owner 维护。
- **Route Action**：`进入 / 回 Phase / 判定目标文档权限 / 草拟 patch / ORDINARY_PATCH_DRAFTED` = `CONTINUE_IN_WORKFLOW`；`/grill-with-docs:ORDINARY_PATCH_SAFE_TO_APPLY` = `CONTINUE_IN_WORKFLOW` with 受限 safe-write 例外（固定含义：exact target / existing slot / no authority escalation / no downstream authorization / report scope after write），只限已存在普通领域文档的小补丁，且目标位置明确、已达成术语共识、不触及 L1 SSOT / standards / feature spec、不改变行为承诺 / 验收 / MVP / 架构决策状态；该例外不是 `CONFIRMED_ACTION`，不可传递到其他文件、下游 workflow 或权威文档；`等待批准 / 回答 / 新建领域文档 / ADR_APPROVAL_PENDING / 修改 L1 SSOT 或 standards / 大改普通领域文档` = `WAIT_FOR_USER`；`/grill-with-docs:PATCH_APPROVED` / 已预授权或已批准的新建 ADR / 新建普通领域文档写入 = `CONFIRMED_ACTION`，但只授权已展示且获批的 patch、目标路径、编号与状态；`分流 / 返回 / ADR_WRITTEN` = `REPORT_AND_STOP`，除非用户明确要求继续。

## 0.3 中断恢复事实源 (Resume Source)

| 恢复需求 (Resume Need) | 事实源 | 下一步判定 |
| ------------- | -------- | ------------ |
| 问题等待回答 | 最近一个领域问题 + 用户回答 | 回 Phase 2 复判 |
| 共识已达成但未写入 | Resolved terms / relationships + patch draft | 判定文档权限 |
| ADR 草案待批准 | ADR draft + 目标路径 / 编号 / 状态 | 等批准或修订草案 |
| 普通文档小补丁未应用 | patch draft + 目标文件权限判定 | 进入 `/grill-with-docs:ORDINARY_PATCH_SAFE_TO_APPLY` 或等待批准 |
| 权威修订未批准 | Proposed SSOT Patch + 用户裁决 | 等待、修订或分流 |
| 裁定已出 | Verdict + Recommended Next Route | 报告 `/grill-with-docs:ROUTE_HANDOFF_READY`，不自动执行下游 |
