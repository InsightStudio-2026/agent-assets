# Dry-run与灾备恢复协议 (Dry-run / Backup / Restore Protocol)

## 1. 证据类型

| 证据 ID (Evidence ID) | 证据 | 适用场景 | 最低字段 | 过期规则 |
| ------------- | ------ | ---------- | ---------- | ---------- |
| DBR-E1 | dry-run output | schema / backfill / downgrade | command / env / timestamp / row count / result | 7 天或 migration 文件变更后过期 |
| DBR-E2 | backup proof | production / destructive / restore | backup ID / scope / timestamp / retention / operator | 24 小时或数据写入窗口变化后过期 |
| DBR-E3 | restore rehearsal | production / destructive / restore | backup ID / target env / duration / verification query | 7 天或 schema 变化后过期 |
| DBR-E4 | row-count estimate | backfill / delete / repair | query / count / sampling method / max chunk | 24 小时或表写入活跃时过期 |
| DBR-E5 | abort / resume proof | chunked backfill / long migration | checkpoint key / resume command / abort command | migration plan 变化后过期 |

## 2. Dry-run 规则

| 规则 ID (Rule ID) | 检查项 | PASS 标准 | FAIL 信号 |
| --------- | -------- | ----------- | ----------- |
| DBR-R1 | 环境隔离 | dry-run 不写生产，或写 shadow / staging 且明确数据来源 | 直接在生产试跑但无批准 |
| DBR-R2 | 命令可复现 | 命令、参数、env、migration revision 记录完整 | 只有截图或口头说明 |
| DBR-R3 | 结果可验证 | 至少有 schema diff / row count / validation query | 只写 “success” |
| DBR-R4 | 失败输出保留 | dry-run 失败时保留 stderr / error code / rollback 状态 | 失败后只重试无记录 |
| DBR-R5 | 过期复跑 | 证据过期后重新 dry-run | 使用旧 dry-run 放行 |

## 3. Backup 规则

| 规则 ID (Rule ID) | 检查项 | PASS 标准 | FAIL 信号 |
| --------- | -------- | ----------- | ----------- |
| DBR-R6 | backup scope | 覆盖被 migration 影响的 DB / table / collection / object store | 只备份部分表但全库 migration |
| DBR-R7 | retention | retention 覆盖 migration window + rollback window | 备份可能在回滚前过期 |
| DBR-R8 | recoverability | backup 可定位、可访问、权限已确认 | backup ID 不可读或权限未知 |
| DBR-R9 | destructive disclosure | destructive change 明确不可完全恢复的字段 | drop / purge 风险隐藏 |

## 4. 恢复性排练规则 (Restore Rehearsal Rules)

| 规则 ID (Rule ID) | 检查项 | PASS 标准 | FAIL 信号 |
| --------- | -------- | ----------- | ----------- |
| DBR-R10 | rehearsal target | restore 到隔离环境，不污染生产 | restore 演练目标不明 |
| DBR-R11 | verification query | restore 后用 query / checksum / sample 验证数据 | 只确认命令退出 0 |
| DBR-R12 | RPO / RTO | 记录可接受数据丢失点与恢复耗时 | 不知道 restore 要多久 |
| DBR-R13 | app compatibility | restore / downgrade 后应用版本兼容 | 数据回去了但应用读不了 |
| DBR-R14 | incident route | restore 失败时有 `/observability-incident` 路由 | 失败后无用户影响处理 |

## 5. 证据表模板

| 字段 (Field) | 值 (Value) |
| ------- | ------- |
| Evidence ID | DBR-E* |
| Source Anchor | NFR-REL-*/ DSN-DB-* / TASK-* |
| Command | `<command>` |
| Environment | local / staging / shadow / production |
| Timestamp | ISO 8601 |
| Result | PASS / FAIL |
| Evidence Path | `<feature>/artifacts/migration/<file>` |
| Expires At | ISO 8601 |

## 6. 判定

| 条件 | 状态 (State) |
| ------ | ------- |
| dry-run + backup + restore rehearsal 全 PASS 且未过期 | `/data-migration-safety:MIGRATION_GATE_PACKET_READY` |
| dry-run 缺失或过期 | `/data-migration-safety:DRY_RUN_REQUIRED` |
| backup / restore rehearsal 缺失 | `/data-migration-safety:BACKUP_RESTORE_REQUIRED` |
| restore 失败或数据损坏 | `/data-migration-safety:MIGRATION_INCIDENT_ROUTE` |
