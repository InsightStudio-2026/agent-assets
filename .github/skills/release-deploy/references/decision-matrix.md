---
description: "发布部署闭环工作流（/release-deploy）专属的触发判定、状态转换路由、状态权威与动作决策矩阵"
---

# 发布部署闭环决策矩阵（/release-deploy）

## 0. 触发与临界路由决策表

| ID | 前置条件 | 匹配动作 | 下一步/目标路由 | 源 / 备注 |
| ---- | ---------- | ---------- | ----------------- | ----------- |
| R-ROUTE-RD-1 | 用户显式 `/release-deploy` | 启用 workflow | 进入 Phase 1 (Intake) | 显式入口 |
| R-ROUTE-RD-2 | 用户准备打 tag、发版、实际部署、或发布物理安装器 | 启用 workflow | 进入 Phase 1 (Intake) | 部署诉求 |
| R-ROUTE-RD-3 | 用户要生成 release notes、执行 post-deploy smoke 或部署 canary 分支 | 启用 workflow | 进入 Phase 1 (Intake) | 部署发布配套 |
| R-ROUTE-RD-4 | `/specs-execute` 报告 `RELEASE_READY` 类信号，证明代码已完工可备交付 | 启用 workflow | 进入 Phase 1 (Intake) | 下游完工联动 |
| R-ROUTE-RD-5 | `/project-steward` 推荐 release closeout 进入发布就绪评估 | 启用 workflow | 进入 Phase 1 (Intake) | 管家引流 |
| R-ROUTE-RD-6 | 需求未批准、实现未完成、或仅属于本地一次性原型 (未经验证) | 停止并重定向 | 路由至 `/specs-execute` 或 `/project-steward` | 阻断未完工发布 |
| R-ROUTE-RD-7 | 系统状态不清、下一步推进方向不明 | 停止并重定向 | 路由至 `/project-steward` | 临界状态 1 |
| R-ROUTE-RD-8 | 缺失母本或 L1 SSOT | 停止并重定向 | 路由至 `/project-inception` | 临界状态 2 |
| R-ROUTE-RD-9 | 属于纯缺陷根因诊断 | 停止并重定向 | 路由至 `diagnose` 技能 | 临界状态 3 |
| R-ROUTE-RD-10 | 逻辑简单明确且适合 TDD 验证 | 停止并重定向 | 路由至 `tdd` 技能或直接执行 | 临界状态 5 |

## 0.1 状态与路由汇总 (State / Route Summary)

| 状态 (State) | 判定 | 下一步 | Gate / DAG ID 映射 |
| ------- | ------ | -------- | --------------------- |
| `/release-deploy:NO_RELEASE_CANDIDATE` | 无可发布候选（spec 未 Done / Task 未 Verify / 无 release branch / tag） | 分流 `/specs-execute` 或 `/project-steward` | `S-HG-1 GATE_NOT_REQUIRED`；建议 `R-AUDIT-0` |
| `/release-deploy:RELEASE_CANDIDATE_DETECTED` | 已识别候选（Task 全 Done + Verification + Artifacts 齐 + 目标环境定义） | 进入 Phase 2 Readiness | 创建 `DAG-N-RELEASE-{slug}-{version}`（status: Candidate） |
| `/release-deploy:READINESS_BLOCKED` | Readiness Dashboard 任一红灯（spec / task / review / test / security / migration / observability / documentation / rollback / performance） | 报告缺项 + 分流上游；不进入 deploy | `S-HG-3 GATE_PACKET_INCOMPLETE`；按缺项触发 `FA-HG-3` 路由对应上游 |
| `/release-deploy:READINESS_DASHBOARD_GREEN` | Readiness Dashboard 全绿 | 进入 Phase 3 Plan Completion Audit | DAG-N-RELEASE-*F-N-5 += 全部 readiness 信号快照 |
| `/release-deploy:PLAN_COMPLETION_AUDIT_FAILED` | required Task 未 Done / Verification 缺失 / Artifacts 与声明漂移 / diff 越 scope | 修正后重审；严重 → 回切 `/specs-execute` | `S-HG-9 GATE_FAILED` + `FA-HG-1`；路由 `R-RETURN-1~5`（`../../specs-write/protocols/entry-decision-tree.md §7.6`） |
| `/release-deploy:DOCUMENTATION_SYNC_PENDING` | public surface 暴露 / README / AGENTS / CHANGELOG / release notes / 架构图 / 运行手册待同步；如触叙事 / 哲学 / 安全模型 / 大段删除 → 升级 `S-HG-4 + HG-STRAT-{slug}-doc-narrative` | 进入 Phase 4 Documentation Sync；触发战略级时等用户裁决 | 不直接绑 HG-RELEASE-*；事实更新可自动；叙事 / 安全模型 = 战略级（详 `../protocols/documentation-sync.md`） |
| `/release-deploy:DEPLOY_PLAN_DRAFTED` | release-plan / deploy-checklist / rollback-plan / smoke 计划已草拟 | 首次真实发布 / 全新环境 → 必须 dry-run；否则展示等批准 | 预装配 `HG-RELEASE-{slug}-{env}-{version}` packet（F-HG-1~8 齐 + F-HG-6 rollback-plan） |
| `/release-deploy:DRY_RUN_FAILED` | dry-run 暴露平台 / URL / health endpoint / deploy 命令缺陷 | 修 plan 重 dry-run；不进入真实 deploy | `S-HG-9 GATE_FAILED` + `FA-HG-1`（packet 装配失败） |
| `/release-deploy:WAITING_DEPLOY_APPROVAL` | plan + dry-run + Readiness 全绿；待批准生产 / 用户可见 / 付费 / 迁移 / 外部副作用 | 等用户批准；命中 `HG-IRREV-001~004`（详 §0.3） | `S-HG-4 WAITING_GATE_APPROVAL` + `HG-RELEASE-*` + 命中时 `HG-IRREV-001~004`；R-INH-3 不继承 spec / task 批准 |
| `/release-deploy:APPROVED_TO_DEPLOY` | 用户已明确批准（本次目标环境 + release candidate + 命令 + 回滚计划，原话引用入 F-HG-3） | 进入 Phase 6 Deploy | `S-HG-5 GATE_APPROVED`；授权仅对本次范围，**不继承**到其他环境 / 版本 / 后续外部副作用 |
| `/release-deploy:DEPLOYING` | 正在按批准 plan 执行 deploy | 等完成；监控失败 | DAG-N-RELEASE-*status: Deploying |
| `/release-deploy:DEPLOY_FAILED` | deploy 命令失败 / 平台报错 / 部分 service 未就绪 | 进入 `/release-deploy:ROLLBACK_REQUIRED` 或修复重试 | `S-HG-9 GATE_FAILED` + `FA-HG-5`；触发 `DAG-E-RBK` 候选 |
| `/release-deploy:DEPLOYED_PENDING_SMOKE` | deploy 成功，待 smoke + health + canary | 进入 Phase 7 Smoke / Canary | `S-HG-5` 已 deploy；待 `S-HG-8` 等 smoke 通过 |
| `/release-deploy:SMOKE_FAILED` | smoke / health check / canary 任一红灯 | 进入 `/release-deploy:ROLLBACK_REQUIRED` 或修复重 deploy | `S-HG-9 GATE_FAILED` + `FA-HG-5`；触发 `DAG-E-RBK` |
| `/release-deploy:CANARY_REGRESSION_DETECTED` | canary 性能 / 错误率 / 关键路径回归（p95 / LCP / CLS / INP / 资源数 / 总传输量 vs baseline） | 进入 `/release-deploy:ROLLBACK_REQUIRED` 或扩大 canary 暴露面 | `S-HG-9 GATE_FAILED` + `FA-HG-5`；`HG-INCIDENT-{slug}-{version}` 候选触发 |
| `/release-deploy:ROLLBACK_REQUIRED` | deploy / smoke / canary 失败且 rollback-plan 可执行 | 按 rollback-plan 执行 → `/release-deploy:ROLLED_BACK` | 触发 `DAG-E-RBK` 指向 `DAG-N-ROLLBACK-RELEASE-{slug}-{version}`；如 migration 不可回滚 → `RG-6` 标记 |
| `/release-deploy:ROLLED_BACK` | 按展示过的 rollback-plan 撤销 | 报告回滚结果 + 是否启 incident workflow | `DAG-E-RBK` 已激活；`DAG-N-ROLLBACK-RELEASE-*` Done；HG-RELEASE-* 终态 = Failed + 已回滚 |
| `/release-deploy:POST_DEPLOY_REGRESSION_NEEDS_INCIDENT` | 发布后用户报告 / 监控告警 / SLO 违约 | 分流 `/observability-incident` | 路由 `HG-INCIDENT-{slug}-{version}`；本 workflow 报告并停止 |
| `/release-deploy:RELEASE_DONE` | deploy + smoke + canary 全过；release-notes / CHANGELOG / documentation sync 完成；release-report 已生成 | 报告 `/release-deploy:RELEASE_DONE` 后返回 `/project-steward` | `S-HG-8 GATE_PASSED`；DAG-N-RELEASE-* Done；F-N-10 += release-report + smoke + canary 证据 |

## 0.2 状态权威与路由动作 (State Authority / Route Action)

- **State Authority**：实际 deploy / smoke / canary / rollback 命令输出与目标环境 health endpoint 是权威事实源；本表 State 只用于流程调度。release-report.md 是本 workflow 终态事实源。
- **Route Action**：`进入 Phase / 修 plan 重 dry-run / 修复重 deploy` = `CONTINUE_IN_WORKFLOW`；`展示 plan 等批准 / 等用户裁决叙事 / 等用户裁决回滚或启 incident` = `WAIT_FOR_USER`；`分流 / 报告并停止 / READINESS_BLOCKED / POST_DEPLOY_REGRESSION_NEEDS_INCIDENT` = `REPORT_AND_STOP`，除非用户明确要求继续；`/release-deploy:APPROVED_TO_DEPLOY` = `CONFIRMED_ACTION`，但只授权本次展示的目标环境、release candidate、命令、回滚计划，**不继承**到其他环境 / 版本 / 后续外部副作用；rollback 执行 = `CONFIRMED_ACTION`，但只授权已展示的回滚步骤。

## 0.3 Hard-gate 命中条件（自动升级到 HG-IRREV-*）

| 条件 | 命中 Gate |
| ------ | ---------- |
| 真实生产 DB 操作 / migration / backfill / 数据删除 | `HG-IRREV-001` + `HG-RELEASE-*` |
| 删除破坏（删 release branch / 删 tag / git history rewrite） | `HG-IRREV-002` + `HG-RELEASE-*` |
| 付费对外发布（应用商店 / 包注册中心 / 邮件批发 / webhook 推送） | `HG-IRREV-003` + `HG-RELEASE-*` |
| 权限 / 认证 / 密钥 / 证书 / token 变更 | `HG-IRREV-004` + `HG-SEC-*` 候选 |
| desktop code signing / notarization / installer / 更新通道切换 | `HG-IRREV-002` + `HG-RELEASE-*` |
| feature flag 大范围关闭 / 启 | `HG-RELEASE-*`；rollback 复杂 → 标 `RG-3` |
| canary 扩量到全量 | `HG-RELEASE-*`（每次扩量都需重批） |

任一命中 → `/release-deploy:WAITING_DEPLOY_APPROVAL` 必须包含对应
packet F-HG-1~8 全齐；F-HG-3 必含用户原话引用；F-HG-6 必含完整回滚方
案或不可回滚明示。

## 0.4 中断恢复事实源 (Resume Source)

| 恢复需求 (Resume Need) | 事实源 | 下一步判定 |
| ------------- | -------- | ------------ |
| 当前 release candidate | git tag / branch / spec `tasks.md` Status 列 | 命中 → `/release-deploy:RELEASE_CANDIDATE_DETECTED` |
| Readiness Dashboard 是否绿 | `readiness-dashboard.md` 10 类信号最近快照 | 任一缺 → `/release-deploy:READINESS_BLOCKED` |
| Deploy plan / Approval 是否已批 | 同一轮用户原话 + F-HG-3 引用 | 未批 → `/release-deploy:WAITING_DEPLOY_APPROVAL`，绝不 deploy |
| Deploy 是否已执行 | 命令输出 + 目标环境 health endpoint | 已 deploy → `/release-deploy:DEPLOYED_PENDING_SMOKE` |
| Smoke / canary 结果 | post-deploy-smoke.md + canary 输出 | 任一失败 → `/release-deploy:SMOKE_FAILED` / `/release-deploy:CANARY_REGRESSION_DETECTED` |
| 是否已 rollback | rollback 命令输出 + git revert / DB restore 证据 | 已回滚 → `/release-deploy:ROLLED_BACK` |
