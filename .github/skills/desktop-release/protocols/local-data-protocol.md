# 本地数据与崩溃协议 (Local Data / Crash Protocol)

## 1. 本地数据范围

| 规则 ID (Rule ID) | 数据类型 | 典型路径 | 风险 |
| --------- | ---------- | ---------- | ------ |
| LDP-1 | user config | AppData / Library / .config | 升级覆盖用户设置 |
| LDP-2 | local database | SQLite / IndexedDB / embedded DB | schema 迁移失败 / 数据损坏 |
| LDP-3 | cache | cache dir / thumbnails / model cache | 空间膨胀 / 清理误删 |
| LDP-4 | offline queue | sync queue / pending uploads | 重复提交 / 丢失 |
| LDP-5 | logs / crash dumps | logs / minidumps / symbols | PII 泄露 / 不可诊断 |
| LDP-6 | user files | documents / export dirs | 误删 / 权限漂移 |

## 2. 本地数据迁移规则

| 规则 ID (Rule ID) | 检查项 | PASS 标准 | FAIL 信号 | 路由 |
| --------- | -------- | ----------- | ----------- | ------ |
| LDP-R1 | Data inventory | 影响哪些本地路径、格式、版本字段已列明 | 不知道会改哪些文件 | `/specs-write` |
| LDP-R2 | Compatibility | 新版本读旧数据，必要时旧版本可读新数据 | 升级后无法回滚 | `/data-migration-safety` |
| LDP-R3 | Backup / copy-on-write | destructive local migration 前有备份或 copy-on-write | 原地破坏写入 | `/data-migration-safety` |
| LDP-R4 | Idempotency | migration 重跑不重复破坏 | 二次启动重复迁移 | `/specs-execute` |
| LDP-R5 | Failure behavior | 中途失败有可见错误、日志、恢复路径 | 启动卡死或静默丢数据 | `/observability-incident` |
| LDP-R6 | Privacy | logs / dumps / telemetry 不含未授权 PII | crash dump 上传敏感数据 | `/security-privacy-audit` |
| LDP-R7 | Disk usage | cache / local DB 增长有预算或清理策略 | 升级后磁盘膨胀 | `/performance-reliability-audit` |

## 3. Crash Reporting 规则

| 规则 ID (Rule ID) | 检查项 | PASS 标准 | FAIL 信号 |
| --------- | -------- | ----------- | ----------- |
| CR-R1 | Crash capture | crash / panic / unhandled rejection 有捕获机制 | 用户设备崩溃无信号 |
| CR-R2 | Symbols | symbols / sourcemap / dSYM / PDB 与 artifact version 对齐 | crash 无法解码 |
| CR-R3 | Privacy | crash payload 脱敏，用户授权边界清楚 | dump 含 token / PII |
| CR-R4 | Runbook | release 后 crash spike 有 triage / rollback route | 只能手工猜 |
| CR-R5 | Offline handling | 无网络时 crash report 缓存 / 丢弃策略明确 | 队列无限增长 |

## 4. Local Data Matrix

| 数据项 (Data Item) | 典型路径 (Path) | 是否版本化 (Versioned) | 是否需要迁移 (Migration Needed) | 是否需要备份 (Backup Needed) | 回滚安全 (Rollback Safe) | 事实依据 (Evidence) |
| ----------- | ------ | ----------- | ------------------ | --------------- | --------------- | ---------- |
| `<item>` | `<path>` | Yes / No | Yes / No | Yes / No | Yes / No | `<artifact path>` |

## 5. 判定

| 条件 | 状态 (State) |
| ------ | ------- |
| 本地数据矩阵、兼容、备份、失败路径齐 | `/desktop-release:DESKTOP_RELEASE_GATE_READY` 候选 |
| 本地数据 migration 风险未闭环 | `/desktop-release:LOCAL_DATA_GATE_BLOCKED` |
| crash reporting / symbols / runbook 缺 | `/desktop-release:CRASH_REPORTING_REQUIRED` |
| privacy 风险 | `/security-privacy-audit` |
