---
description: "仓库安全基线初始化工作流（/repo-safety-setup）专属的触发判定、状态转换路由、状态权威与动作决策矩阵"
---

# 仓库安全初始化决策矩阵（/repo-safety-setup）

## 0. 触发与临界路由决策表

| ID | 前置条件 | 匹配动作 | 下一步/目标路由 | 源 / 备注 |
| ---- | ---------- | ---------- | ----------------- | ----------- |
| R-ROUTE-RSS-1 | 用户显式 `/repo-safety-setup` | 启用 workflow | 进入 Phase 1 (Detecting) | 显式入口 |
| R-ROUTE-RSS-2 | 用户要求建立本地拦截机制，阻止危险 git 破坏性操作 | 启用 workflow | 进入 Phase 1 (Detecting) | 防护诉求 |
| R-ROUTE-RSS-3 | 用户要配置 pre-commit、Husky、lint-staged、本地 typecheck 或 formatter | 启用 workflow | 进入 Phase 1 (Detecting) | 基础门禁配置 |
| R-ROUTE-RSS-4 | `/project-steward` 在盘点中发现仓库缺少最基本的本地安全防护基线 | 启用 workflow | 进入 Phase 1 (Detecting) | 管家引流 |
| R-ROUTE-RSS-5 | 系统状态不清、下一步推进方向不明 | 停止并重定向 | 路由至 `/project-steward` | 临界状态 1 |
| R-ROUTE-RSS-6 | 缺失母本或 L1 SSOT | 停止并重定向 | 路由至 `/project-inception` | 临界状态 2 |
| R-ROUTE-RSS-7 | 属于纯缺陷根因诊断（局部、具体 bug） | 停止并重定向 | 路由至 `diagnose` 技能 | 临界状态 3 |
| R-ROUTE-RSS-8 | 属于新功能、新需求开发、大重构落地 | 停止并重定向 | 路由至 `/specs-write` 与 `/specs-execute` | 临界状态 4 |
| R-ROUTE-RSS-9 | 逻辑简单明确且适合 TDD 验证 | 停止并重定向 | 路由至 `tdd` 技能或直接执行 | 临界状态 5 |
| R-ROUTE-RSS-10 | 以上皆不满足且无本地开发防护配置需求 | 不启用 workflow | 不启用本 workflow | 默认退出 |

## 0.1 状态与路由汇总 (State / Route Summary)

| 状态 (State) | 判定 | 下一步 | Gate / DAG ID 映射 |
| ------- | ------ | -------- | --------------------- |
| `/repo-safety-setup:DETECTING` | 正在识别 hooks、package manager、lint / test 配置 | 进入 Phase 2 | 创建 `DAG-N-SPEC-{repo}-safety` 节点（status: Detecting） |
| `/repo-safety-setup:WAITING_SCOPE_DECISION` | Project / Global、hook 方案或依赖安装需用户确认 | 等待用户批准 | `S-HG-3 GATE_PACKET_INCOMPLETE`（待装配 `HG-OPS-{repo}-safety`，F-HG-4 作用范围未定） |
| `/repo-safety-setup:USER_DECLINED` | 用户拒绝安装、依赖或 hook 方案 | 报告未配置项并停止或返回 `/project-steward` | `S-HG-6 GATE_REJECTED` |
| `/repo-safety-setup:UNSUPPORTED_PROJECT` | 当前仓库没有可安全识别的 package manager、hooks 或验证入口 | 输出手动建议，不写配置 | `S-HG-1 GATE_NOT_REQUIRED`（无可写入对象） |
| `/repo-safety-setup:INSTALL_BLOCKED` | 安装依赖、写 hook 或权限操作被环境 / 网络 / 权限阻止 | 停下等待用户裁决 | `S-HG-9 GATE_FAILED`（packet 装配阶段失败） |
| `/repo-safety-setup:READY_TO_CONFIGURE` | 范围、工具链、待写文件、命令和回滚方式已展示并获确认 | 进入 Phase 3-4 | `S-HG-4 WAITING_GATE_APPROVAL` + `HG-OPS-{repo}-safety`；如涉危险 git 拦截 hook → 同时 `HG-IRREV-*`（git history 防护）；F-HG-6 必含 `git config / package script` 回滚 |
| `/repo-safety-setup:CONFIGURED_PENDING_VERIFY` | Guardrails / pre-commit / formatter / typecheck / test 已写入但尚未验证 | 进入 Phase 5 | `S-HG-5 GATE_APPROVED`（写入完成）；待 `S-HG-8 GATE_PASSED`（验证通过） |
| `/repo-safety-setup:PARTIAL_CONFIGURED` | Guardrails / pre-commit / formatter / typecheck / test 只完成一部分 | 报告剩余缺口，等待用户裁决或返回 `/project-steward` | 部分 `S-HG-8`、部分 `S-HG-9`；packet F-HG-5 前置证据不全 |
| `/repo-safety-setup:VERIFY_FAILED_CONFIG_REGRESSION` | 本 workflow 写入导致 smoke test、lint-staged、typecheck 或 test 失败 | 修配置重验；若不可恢复则回滚本 workflow 写入 | `S-HG-9 GATE_FAILED`；触发 `DAG-E-RBK` 指向 `DAG-N-ROLLBACK-{repo}-safety`；按 F-HG-6 回滚方案执行 |
| `/repo-safety-setup:VERIFY_FAILED_EXISTING_PROJECT` | 验证命令暴露既有项目失败，非本 workflow 写入导致 | 停下报告，不把本 workflow 判定为 Done | 不归本 HG-*失败；建议 `R-AUDIT-2` 走 `/bug-audit` |
| `/repo-safety-setup:VERIFY_BLOCKED_ENVIRONMENT` | 工具缺失、权限、网络或环境导致无法验证 | 停下等待用户裁决 | `S-HG-9 GATE_FAILED`（验证阶段失败、环境型） |
| `/repo-safety-setup:ROLLED_BACK` | 本 workflow 写入已按展示过的回滚方式撤销 | 报告回滚结果，返回 `/project-steward` | `DAG-E-RBK` 已激活；`DAG-N-ROLLBACK-{repo}-safety` Done；HG-OPS-* 终态 = Failed + 已回滚 |
| `/repo-safety-setup:DONE` | 配置与验证均完成 | 报告 `/repo-safety-setup:DONE` 后返回 `/project-steward` | `S-HG-8 GATE_PASSED`；DAG-N-SPEC-{repo}-safety Done；F-N-10 += hooks / scripts / 验证证据 |

## 0.2 状态权威与路由动作 (State Authority / Route Action)

- **State Authority**：hooks、package scripts、lint-staged / Prettier 配置和验证输出是权威事实源；本表 State 只用于安装与验证调度。
- **Route Action**：`进入 Phase / 修配置重验 / 已确认且无真实副作用的回滚` = `CONTINUE_IN_WORKFLOW`；`等待用户批准 / 裁决 / 环境阻塞 / PARTIAL_CONFIGURED 后是否继续` = `WAIT_FOR_USER`；`返回 / 只报告未配置项 / 输出手动建议 / 既有项目失败 / ROLLED_BACK` = `REPORT_AND_STOP`，除非用户明确要求继续；已批准安装 / 写入 / 脚本修改 / hook 合并 = `CONFIRMED_ACTION`，但只授权已展示的文件、命令、script、hook 合并与回滚方式，不授权提交、推送、global 安装、业务代码修改或下游 workflow 执行。

## 0.3 写入确认门与 Resume Source

进入 `/repo-safety-setup:READY_TO_CONFIGURE` 前，确认内容必须覆盖：待写文件、安装命令、package script 修改、hook 合并策略、验证命令和回滚方式。缺任一项则保持 `/repo-safety-setup:WAITING_SCOPE_DECISION`。

## 0.4 中断恢复事实源 (Resume Source)

| 恢复需求 (Resume Need) | 事实源 | 下一步判定 |
| ------------- | -------- | ------------ |
| 探测后中断 | Safety Intake + Detect Existing Setup 输出 | 等 scope 决策或停止 |
| 配置待确认 | 待写文件 / 命令 / 回滚方式清单 | 进入配置或等待 |
| 配置后未验证 | Files Changed + package manager + 验证命令 | 进入 Phase 5 |
| 验证失败 | command output + 失败分类 | 修配置、回滚或报告既有失败 |
| 回滚完成 | Rollback output + Files Changed 清单 | 报告 `/repo-safety-setup:ROLLED_BACK` |
| 部分配置 | Configured / Not Configured 清单 | 等用户裁决或停止 |
