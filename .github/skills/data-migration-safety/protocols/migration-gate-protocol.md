# 数据迁移门禁协议 (Migration Gate Protocol)

## 1. 范围分类

| 规则 ID (Rule ID) | 迁移类型 (Migration Type) | 命中条件 | 最低证据 | 默认严重性 |
| --------- | ---------------- | ---------- | ---------- | ------------ |
| MGP-1 | schema | DDL / ORM migration / index / constraint / enum / column | migration file + dry-run + rollback / downgrade | Critical |
| MGP-2 | backfill | 大量更新 / 衍生字段填充 / 旧数据补齐 | row-count + chunking + idempotency + resume | Critical |
| MGP-3 | data-repair | 修复脏数据 / 合并重复 / 状态纠偏 | before/after sample + audit query + backup | High |
| MGP-4 | batch-delete | 批量删除 / drop table / drop column / purge | destructive disclosure + backup + restore rehearsal | Critical |
| MGP-5 | restore | 从备份恢复 / point-in-time recovery | restore rehearsal + blast radius + incident route | Critical |
| MGP-6 | downgrade | down migration / feature rollback dependent data shape | downgrade dry-run + app compatibility check | Critical |

## 2. Migration Strategy 对照

| 迁移策略 (Strategy) | 必需字段 | 必需验证 | FAIL 信号 |
| ---------- | ---------- | ---------- | ----------- |
| `shadow_write` | dual-write scope / diff query / cutover criteria | 双写 diff = 0 或阈值说明 | 只写双写但无 diff |
| `backward_compatible_stepwise` | step list / compatibility window / cleanup task | old app + new app 均可读写 | 一步破坏兼容 |
| `downgrade_script` | down path / irreversible fields / data loss disclosure | down dry-run + row count preserved or disclosed | down 只回滚代码不回数据 |
| `manual_repair` | operator / checklist / sample verification | 手工步骤可复现 + 双人审查 | 只写“手工处理” |
| `restore_from_backup` | backup ID / restore target / RPO / RTO | restore rehearsal PASS | 未演练 restore |

## 3. 红绿判定

| 规则 ID (Rule ID) | 检查项 | PASS 标准 | FAIL 信号 | 路由 |
| --------- | -------- | ----------- | ----------- | ------ |
| MGP-R1 | 上游锚点 | `NFR-REL-*` / `DSN-DB-*` / Task 均可追溯 | migration 来源不明 | `/specs-write` |
| MGP-R2 | dry-run | 非生产或 shadow dry-run 有证据 | 未跑或证据过期 | `MIGRATION_BLOCKED` |
| MGP-R3 | backup | 生产数据风险有 backup 或明确 N/A 理由 | 无 backup | `MIGRATION_BLOCKED` |
| MGP-R4 | restore | restore rehearsal 已跑或不可回滚已明示 | 只有 backup 无 restore | `MIGRATION_BLOCKED` |
| MGP-R5 | rollback | rollback / downgrade / abort 路径可执行 | 只写代码回滚 | `/specs-write` |
| MGP-R6 | observability | migration 期间有 logs / metrics / alert / abort trigger | 无可观测信号 | `/observability-incident` |
| MGP-R7 | release handoff | packet 可供 R-RDY-6 消费 | packet 缺字段 | `/data-migration-safety` Phase 5 |

## 4. 判定输出

| 条件 | 状态 (State) |
| ------ | ------- |
| MGP-R1~R7 全 PASS | `/data-migration-safety:MIGRATION_GATE_PACKET_READY` |
| 任一 Critical 缺事实源 | `/data-migration-safety:MIGRATION_BLOCKED` |
| 上游 spec 不足 | `/specs-write` |
| 实现 / 脚本缺失 | `/specs-execute` |
| 已有生产影响 | `/observability-incident` |
