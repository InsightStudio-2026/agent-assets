---
description: "代理资产质量门工作流（/asset-quality-gates）专属的触发判定、状态转换路由、状态权威与动作决策矩阵"
---

# 代理资产质量门决策矩阵（/asset-quality-gates）

## 0. 触发与临界路由决策表

| ID | 前置条件 | 匹配动作 | 下一步/目标路由 | 源 / 备注 |
| ---- | ---------- | ---------- | ----------------- | ----------- |
| R-ROUTE-AQG-1 | 用户显式 `/asset-quality-gates` | 启用 workflow | 进入 Phase 1 (Detecting) | 显式入口 |
| R-ROUTE-AQG-2 | 用户要新增、删除、重命名、移动、拆分 workflow 或 skill 资产 | 启用 workflow | 进入 Phase 1 (Detecting) | 内部资产变更 |
| R-ROUTE-AQG-3 | 用户要引入外部 workflow、skill 或 agent 资产 | 启用 workflow | 强制进入 Phase 2.5 (Quarantine) | 外部资产引入 |
| R-ROUTE-AQG-4 | 用户修改 `.github/workflow-docs/` 目录结构 | 启用 workflow | 进入 Phase 1 (Detecting) | 支撑文档变更 |
| R-ROUTE-AQG-5 | 用户修改 `../../specs-write/examples/` 或 `../../specs-write/conformance-fixtures/` | 启用 workflow | 进入 Phase 1 (Detecting) | 规范集与合规测试变更 |
| R-ROUTE-AQG-6 | `/project-steward` 推荐资产质量门、或检测到索引与目录漂移 | 启用 workflow | 进入 Phase 1 (Detecting) | 上游或管家引流 |
| R-ROUTE-AQG-7 | `/repo-safety-setup` 检测到本地安全基线在资产层缺失质量门保护 | 启用 workflow | 进入 Phase 1 (Detecting) | 联动触发 |
| R-ROUTE-AQG-8 | 系统状态不清、下一步推进方向不明 | 停止并重定向 | 路由至 `/project-steward` | 临界状态 1 |
| R-ROUTE-AQG-9 | 缺失母本或 L1 SSOT | 停止并重定向 | 路由至 `/project-inception` | 临界状态 2 |
| R-ROUTE-AQG-10 | 属于纯缺陷根因诊断（局部、具体 bug） | 停止并重定向 | 路由至 `diagnose` 技能 | 临界状态 3 |
| R-ROUTE-AQG-11 | 属于新功能、新需求开发、大重构落地 | 停止并重定向 | 路由至 `/specs-write` 与 `/specs-execute` | 临界状态 4 |
| R-ROUTE-AQG-12 | 逻辑简单明确且适合 TDD 验证 | 停止并重定向 | 路由至 `tdd` 技能或直接执行 | 临界状态 5 |
| R-ROUTE-AQG-13 | 以上皆不满足且无资产维护或质量门需求 | 不启用 workflow | 不启用本 workflow | 默认退出 |

## 0.1 状态与路由汇总 (State / Route Summary)

| 状态 (State) | 判定 | 下一步 | Gate / DAG ID 映射 |
| ------- | ------ | -------- | --------------------- |
| `/asset-quality-gates:DETECTING` | 正在识别变更资产范围（内部修订 vs 外部 intake vs 索引同步） | 进入 Phase 2 | 创建 `DAG-N-AUDIT-{repo}-asset-quality` 节点（status: Detecting） |
| `/asset-quality-gates:SCOPE_DEFINED_INTERNAL` | 范围 = 内部 workflow / skill / 支撑文档变更（非外部引入） | 进入 Phase 3 检查清单 | `S-HG-2 GATE_REQUIRED`；预装配 `HG-OPS-{repo}-asset`（仓库级资产变更） |
| `/asset-quality-gates:SCOPE_DEFINED_EXTERNAL_INTAKE` | 范围 = 引入外部 workflow / skill / agent 资产 | 强制进入 Phase 2.5 quarantine | 预装配 `HG-OPS-{repo}-asset-intake` + `HG-SEC-{repo}-license`（外部 license / provenance 风险） |
| `/asset-quality-gates:SCOPE_DEFINED_INDEX_SYNC` | 范围 = AGENTS.md 索引 vs 真实目录漂移 | 进入 Phase 3.5 index sync 检查 | `HG-OPS-{repo}-asset`（索引一致性变更） |
| `/asset-quality-gates:SCOPE_DEFINED_SPEC_CONFORMANCE` | 范围 = `../../specs-write/examples/` / `../../specs-write/conformance-fixtures/` 变更 | 进入 Phase 3.6 spec conformance 检查 | `HG-OPS-{repo}-asset`（spec conformance 套件变更） |
| `/asset-quality-gates:QUARANTINED` | 外部资产已落入 `.github/.quarantine/<source-slug>/`，未进入启用路径 | 进入 Phase 3 检查清单 | `S-HG-3 GATE_PACKET_INCOMPLETE`（待补 provenance / license / 适配证据） |
| `/asset-quality-gates:CHECKS_RUNNING` | 正在按 `checks-catalog.md` R-CHK-1~15 顺序执行检查 | 收集所有失败项 | DAG-N-AUDIT-*F-N-5 累积每条 R-CHK-* 命中状态 |
| `/asset-quality-gates:CHECKS_FAILED_NEEDS_REVISION` | ≥ 1 项 R-CHK-*失败 | 生成 patch 草案 → 用户裁决 → 修订或退回 | `S-HG-9 GATE_FAILED`；按失败类别触发 `FA-HG-*`（结构性 → FA-HG-1；license → FA-HG-2；index → FA-HG-3） |
| `/asset-quality-gates:CHECKS_PASSED_PENDING_USER_APPROVAL` | 所有 R-CHK-* 通过；待用户批准启用 / 修订 / 索引同步写入 | 等待用户批准 | `S-HG-4 WAITING_GATE_APPROVAL` + `HG-OPS-*`；packet F-HG-1~8 齐 |
| `/asset-quality-gates:ACTIVATION_BLOCKED_BY_PATH_VIOLATION` | 外部资产尝试直接落入 `.github/workflows/` / `.github/skills/`，未经 quarantine + 检查 | 强制回退到 `/asset-quality-gates:QUARANTINED` 或终止 | `S-HG-9 GATE_FAILED` + `FA-HG-4`（启用路径污染，触发 IRREV 等级反弹） |
| `/asset-quality-gates:ACTIVATION_APPROVED_PENDING_WRITE` | 用户已批准启用范围 + 索引补登记 + AGENTS.md patch | 进入 Phase 5 写入 | `S-HG-5 GATE_APPROVED`；F-HG-6 含完整回滚（`git restore` 或 `git rm` + AGENTS 反向 patch） |
| `/asset-quality-gates:WRITES_APPLIED_PENDING_VERIFY` | 启用 / 索引 / 支撑文档写入已应用，待验证 | 进入 Phase 6 验证 | 写入完成；待 `S-HG-8 GATE_PASSED`（验证通过） |
| `/asset-quality-gates:VERIFY_FAILED_ROLLBACK_REQUIRED` | 验证失败（启用后 frontmatter / 索引 / 入口骨架破裂） | 按 F-HG-6 回滚 | `S-HG-9 GATE_FAILED`；触发 `DAG-E-RBK` 指向 `DAG-N-ROLLBACK-{repo}-asset` |
| `/asset-quality-gates:ROLLED_BACK` | 本 workflow 写入已按展示过的回滚方式撤销 | 报告回滚结果，返回 `/project-steward` | `DAG-E-RBK` 已激活；`DAG-N-ROLLBACK-{repo}-asset` Done；HG-OPS-*终态 = Failed + 已回滚 |
| `/asset-quality-gates:INDEX_SYNC_GAP_REPORTED` | 已识别 AGENTS.md ↔ 真实目录漂移；不直接写入，只报告 | 报告漂移清单，等待用户裁决 | 不直接绑 HG-* 写入；仅 advisory 报告 |
| `/asset-quality-gates:EXTERNAL_INTAKE_DECLINED` | 用户审阅 quarantine 资产后拒绝采用 | 删除 `.github/.quarantine/<slug>/` + 报告决策 | `S-HG-6 GATE_REJECTED`（intake 闸口） |
| `/asset-quality-gates:DONE` | 所有检查通过、启用与验证完成或用户确认仅报告无写入 | 报告 `/asset-quality-gates:DONE` 后返回 `/project-steward` | `S-HG-8 GATE_PASSED`（有写入）或 `S-HG-1 GATE_NOT_REQUIRED`（仅报告）；DAG-N-AUDIT-{repo}-asset-quality Done |

本表 `State` 为本 workflow 的 local suffix；任何报告、handoff 或 route 建议必须输出为 workflow-qualified state，例如 `/asset-quality-gates:CHECKS_FAILED_NEEDS_REVISION`。

## 0.2 状态权威与路由动作 (State Authority / Route Action)

- **State Authority**：`.github/workflows/`、`.github/skills/`、`.github/workflow-docs/`、`AGENTS.md` 是资产层权威事实源；本表 State 只用于检查 / 启用 / 索引同步调度。`.github/.quarantine/<slug>/` 不是启用路径，Cascade / Windsurf 自动发现不会从此处加载 workflow / skill。
- **Route Action**：`进入 Phase` = `CONTINUE_IN_WORKFLOW`；`生成 patch 草案 / 等用户批准 / 等用户裁决` = `WAIT_FOR_USER`；`分流 / 仅报告 / EXTERNAL_INTAKE_DECLINED / INDEX_SYNC_GAP_REPORTED` = `REPORT_AND_STOP`，除非用户明确要求继续；`/asset-quality-gates:ACTIVATION_APPROVED_PENDING_WRITE` = `CONFIRMED_ACTION`，但只授权已展示的资产启用 / 索引补登记 / 支撑文档写入 / quarantine 删除，不授权业务代码、feature spec、tracker 外部写入或下游 workflow 执行。

## 0.3 写入确认门

进入 `/asset-quality-gates:ACTIVATION_APPROVED_PENDING_WRITE` 前，确认内容必须覆盖：

- 待启用资产清单（quarantine 路径 → 启用路径目标）
- 每个文件 frontmatter 草案 + 入口骨架草案
- AGENTS.md 索引补登记 patch
- 支撑文档目录 `.github/workflow-docs/<name>/` 是否新建
- 验证命令（启用后再跑 R-CHK-1~9 内部检查全部通过）
- 回滚方式（`git restore` 启用路径 + AGENTS.md 反向 patch + 重新放回 quarantine 或删除）

缺任一项则保持 `/asset-quality-gates:CHECKS_PASSED_PENDING_USER_APPROVAL`，不得进入写入阶段。

## 0.4 启用路径禁入硬规则

| 路径 | 启用语义 | 本 workflow 禁入条件 |
| ------ | --------- | --------------------- |
| `.github/workflows/*.md` | Windsurf 自动发现为 workflow 入口 | 未通过 R-CHK-1~9 + R-CHK-10~15（外部）+ 用户批准，**绝对禁止**任何直接 `cp` / `mv` / 新建写入 |
| `.github/skills/<name>/SKILL.md` | Windsurf 自动发现为 skill 入口 | 同上；未通过检查不得直接写入 |
| `.github/workflow-docs/<name>/*.md` | workflow 支撑文档（被入口引用即生效） | 可在 `/asset-quality-gates:ACTIVATION_APPROVED_PENDING_WRITE` 后写入；但不得绕过入口 workflow 直接对外暴露 |
| `.github/.quarantine/<slug>/` | **非启用路径**：Cascade / Windsurf 不发现 | 外部资产 intake 默认落点；可自由读写，但不得 `cp` 到上面三类路径而不走本 workflow |
| `AGENTS.md` 启用 Workflow / Skill 索引 | 资产启用的元事实源 | 必须随启用路径写入同步；漂移 = `/asset-quality-gates:INDEX_SYNC_GAP_REPORTED` |

任何尝试绕过本表的写入动作 → 立刻进入 `/asset-quality-gates:ACTIVATION_BLOCKED_BY_PATH_VIOLATION`，并报告给用户。

## 0.5 中断恢复事实源 (Resume Source)

| 恢复需求 (Resume Need) | 事实源 | 下一步判定 |
| ------------- | -------- | ------------ |
| 哪些资产在 quarantine | 列 `.github/.quarantine/<slug>/` 目录 | 有则进入 `/asset-quality-gates:QUARANTINED`；无则视为内部范围 |
| 检查跑到第几条 R-CHK-* | DAG-N-AUDIT-* F-N-5 累积日志（如已生成 report） | 续跑剩余项 |
| 用户是否已批准启用 | 同一轮用户原话；缺则保持 `/asset-quality-gates:CHECKS_PASSED_PENDING_USER_APPROVAL` | 未批准 → 不写入 |
| 启用路径是否被污染 | `git status` + `.github/workflows/` / `.github/skills/` 新增项 | 如有未经本 workflow 的新增 → `/asset-quality-gates:ACTIVATION_BLOCKED_BY_PATH_VIOLATION` |
| AGENTS.md 索引同步状态 | 索引表 vs 真实目录 diff | 漂移则 `/asset-quality-gates:INDEX_SYNC_GAP_REPORTED` |
| Spec conformance 检查跑到哪条子规则 | DAG-N-AUDIT-* F-N-5 累积日志（R-CHK-EX-1.1~1.8 状态表） | 续跑剩余子规则 + 剩余 example/fixture |
