---
description: "数据迁移安全闸口工作流（/data-migration-safety）专属的触发判定、状态转换路由、状态权威与动作决策矩阵"
---

# 数据迁移安全闸口决策矩阵（/data-migration-safety）

## 0. 触发判定

| ID | 前置条件 | 动作 | 下一步 | 源 |
| ---- | ---------- | ------ | -------- | ------ |
| R-DMS-ENTRY-1 | 用户显式 `/data-migration-safety` | 启动审计 | Phase 1 | 本文件 §0 |
| R-DMS-ENTRY-2 | spec 含 `NFR-REL-* Type: migration` 或 `Migration Plan Ref: /data-migration-safety` | 启动 migration gate | Phase 1 | `../../specs-write/templates/requirements.md §10.4` |
| R-DMS-ENTRY-3 | design 含 `DSN-DB-* Migration Strategy` 非 N/A | 启动 migration strategy 审计 | Phase 1 | `../../specs-write/protocols/design-rules.md` |
| R-DMS-ENTRY-4 | release readiness `R-RDY-6` 缺 migration packet | 阻塞 release 并审计 | Phase 1 | `../../release-deploy/references/readiness-dashboard.md` |
| R-DMS-ENTRY-5 | 真实生产 DB 写入 / schema apply / backfill / batch delete / restore | 装配 RWSE Gate packet | Phase 5 | 本文件 §0.3 |
| R-DMS-ENTRY-6 | 只有本地测试 DB reset / fixture seed | 不启用本 workflow | `/repo-safety-setup` 或 direct | 本文件 §4 |
| R-DMS-ENTRY-7 | 系统状态不清、下一步推进方向不明 | 停止并重定向 | 路由至 `/project-steward` | 临界状态 1 |
| R-DMS-ENTRY-8 | 缺失母本或 L1 SSOT | 停止并重定向 | 路由至 `/project-inception` | 临界状态 2 |
| R-DMS-ENTRY-9 | 属于纯缺陷根因诊断（局部、具体 bug） | 停止并重定向 | 路由至 `diagnose` 技能 | 临界状态 3 |
| R-DMS-ENTRY-10 | 属于新功能、新需求开发、大重构落地 | 停止并重定向 | 路由至 `/specs-write` 与 `/specs-execute` | 临界状态 4 |
| R-DMS-ENTRY-11 | 逻辑简单明确且适合 TDD 验证 | 停止并重定向 | 路由至 `tdd` 技能或直接执行 | 临界状态 5 |

## 0.1 状态与路由汇总 (State / Route Summary)

| 状态 (State) | 判定 | 下一步 | Gate / DAG ID 映射 |
| ------- | ------ | -------- | --------------------- |
| `/data-migration-safety:NO_MIGRATION_SCOPE` | 无 schema / data / backfill / delete / restore 风险 | 报告 N/A | `REPORT_AND_STOP` |
| `/data-migration-safety:MIGRATION_SCOPE_DEFINED` | 已识别 migration 范围、环境、数据域、上游锚点 | 进入 Phase 2 | 创建 `DAG-N-MIGRATION-{slug}` |
| `/data-migration-safety:MIGRATION_PLAN_INCOMPLETE` | 缺 dry-run、backup、restore、rollback、owner、窗口或验证 | 回 `/specs-write` 或 `/specs-execute` | `S-HG-3 GATE_PACKET_INCOMPLETE` |
| `/data-migration-safety:DRY_RUN_REQUIRED` | 需要非生产或 shadow 环境 dry-run | 进入 Phase 3 | `HG-IRREV-001` 候选 |
| `/data-migration-safety:BACKUP_RESTORE_REQUIRED` | 生产或不可逆数据风险需要 backup + restore rehearsal | 进入 Phase 4 | `HG-IRREV-001` + `RG-6` 候选 |
| `/data-migration-safety:WAITING_MIGRATION_APPROVAL` | 真实生产 migration / backfill / delete / restore 待用户批准 | 等用户批准 | `S-HG-4 WAITING_GATE_APPROVAL` |
| `/data-migration-safety:MIGRATION_GATE_PACKET_READY` | dry-run、backup、restore、DAG、rollback 事实源齐 | 输出 packet 给 `/release-deploy` | `R-RDY-6` PASS 候选 |
| `/data-migration-safety:MIGRATION_BLOCKED` | 数据风险不可接受、不可回滚未明示、证据过期或 restore 失败 | 阻塞 release | `R-RDY-6` FAIL |
| `/data-migration-safety:MIGRATION_INCIDENT_ROUTE` | 已发生数据损坏、restore 失败或生产影响 | 分流 `/observability-incident` | `HG-INCIDENT-*` 候选 |

## 0.2 状态权威与路由动作 (State Authority / Route Action)

| 事项 | 权威事实源 | 路由动作 (Route Action) |
| ------ | ------------ | -------------- |
| migration 需求 | `requirements.md#NFR-REL-*` + `design.md#DSN-DB-*` | `CONTINUE_IN_WORKFLOW` |
| 迁移任务 | `tasks.md` + `handoff-payload.yaml#traceability` | `CONTINUE_IN_WORKFLOW` |
| dry-run / backup / restore 证据 | `<feature>/artifacts/migration/` | `CONTINUE_IN_WORKFLOW` |
| 生产迁移批准 | 用户原话 + gate packet F-HG-3 | `WAIT_FOR_USER` |
| release 放行 | `/release-deploy` readiness dashboard | `REPORT_AND_STOP` |

## 0.3 真实世界副作用 Gate

| 条件 | Gate | 必需证据 | 未满足动作 |
| ------ | ------ | ---------- | ------------ |
| 生产 schema migration apply | `HG-IRREV-001` | dry-run + backup + restore rehearsal + rollback / downgrade | `/data-migration-safety:WAITING_MIGRATION_APPROVAL` |
| 生产 backfill / data repair | `HG-IRREV-001` | row-count estimate + idempotency + chunking + resume / abort | `/data-migration-safety:WAITING_MIGRATION_APPROVAL` |
| 批量删除 / destructive change | `HG-IRREV-002` | irreversible disclosure + backup + restore rehearsal | `/data-migration-safety:MIGRATION_BLOCKED` |
| 生产 restore | `HG-IRREV-001` | restore plan + blast radius + user impact + incident route | `/data-migration-safety:WAITING_MIGRATION_APPROVAL` |
