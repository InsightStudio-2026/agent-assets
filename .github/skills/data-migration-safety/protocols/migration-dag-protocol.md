# 迁移 DAG 拓扑协议 (Migration DAG Protocol)

## 1. DAG 节点类型

| 节点类型 (Node Type) | ID 模式 | Owner | 输入 | 输出 |
| ----------- | --------- | ------- | ------ | ------ |
| migration-plan | `DAG-N-MIGRATION-{slug}-plan` | `/data-migration-safety` | NFR-REL-*/ DSN-DB-* | migration plan verdict |
| dry-run | `DAG-N-MIGRATION-{slug}-dryrun` | `/data-migration-safety` | migration file / shadow env | dry-run evidence |
| backup | `DAG-N-MIGRATION-{slug}-backup` | `/data-migration-safety` | target env / affected data | backup proof |
| restore | `DAG-N-MIGRATION-{slug}-restore` | `/data-migration-safety` | backup proof / restore target | restore rehearsal evidence |
| release | `DAG-N-RELEASE-{slug}-{version}` | `/release-deploy` | migration gate packet | deploy decision |
| rollback-data | `DAG-N-ROLLBACK-DATA-{slug}` | `/data-migration-safety` | rollback trigger / backup | restore / downgrade result |

## 2. 依赖规则

| 规则 ID (Rule ID) | 前置条件 | 动作 | 下一步 |
| --------- | ---------- | ------ | -------- |
| MDAG-R1 | schema migration 存在 | plan → dry-run → backup → restore → packet 排序 | 不允许跳 dry-run |
| MDAG-R2 | destructive change 存在 | backup 与 restore rehearsal 必须在 release 前完成 | 否则 R-RDY-6 FAIL |
| MDAG-R3 | backfill 长任务存在 | 增加 abort / resume / checkpoint 节点 | 缺 checkpoint 阻塞 |
| MDAG-R4 | migration 与 release 强绑定 | release 节点依赖 migration packet | `/release-deploy` 只消费 packet |
| MDAG-R5 | rollback 需要数据恢复 | 代码 rollback 前先判定 data rollback / restore 依赖 | 防止代码回滚导致 schema 不兼容 |
| MDAG-R6 | 多 migration 并行 | 同表 / 同索引 / 同数据域禁止并行，除非有锁定策略 | 并行风险阻塞 |

## 3. 并行安全矩阵

| 共享域 | 默认并行 | 允许条件 | 禁止条件 |
| -------- | ---------- | ---------- | ---------- |
| same table | No | 不同列且无锁冲突，有 explicit lock plan | 任一 DDL / backfill 触同索引 |
| same index | No | 只读校验 | create/drop/rebuild 同时发生 |
| same object store prefix | No | partition disjoint + checksum | purge / rewrite 同 prefix |
| unrelated table | Yes | 无 FK / trigger / view 依赖 | 共享 transaction / global lock |
| feature flag data shape | No | backward compatible stepwise | app versions 读写 shape 不兼容 |

## 4. Rollback 依赖

| 规则 ID (Rule ID) | 条件 | 数据回滚顺序 | Release 回滚关系 |
| --------- | ------ | -------------- | ------------------- |
| RBK-D1 | backward compatible add column | 可先 code rollback，再保留 column | cleanup 另开 Task |
| RBK-D2 | destructive drop | 先 restore / data repair，再 code rollback 或停服 | 必须用户批准 |
| RBK-D3 | backfill only | 可 abort / resume / reverse patch | code rollback 不等于 data rollback |
| RBK-D4 | shadow_write cutover | 先停写 / freeze / diff，再切回旧读路径 | release rollback 依赖数据一致性 |
| RBK-D5 | downgrade script | 先 down dry-run，再按批准顺序执行 | down 失败触发 incident |

## 5. DAG 输出模板

| 节点 ID (Node ID) | 节点类型 (Node Type) | 所有者 (Owner) | 依赖节点 (Depends On) | 阻碍后续节点 (Blocks) | 验证证据 (Evidence) | 状态 (Status) |
| --------- | ----------- | ------- | ------------ | -------- | ---------- | -------- |
| DAG-N-MIGRATION-`<slug>`-plan | migration-plan | /data-migration-safety | NFR-REL-* | dry-run | `<path>` | Pending / Done / Blocked |
| DAG-N-MIGRATION-`<slug>`-dryrun | dry-run | /data-migration-safety | plan | backup | `<path>` | Pending / Done / Blocked |
| DAG-N-MIGRATION-`<slug>`-backup | backup | /data-migration-safety | dry-run | restore | `<path>` | Pending / Done / Blocked |
| DAG-N-MIGRATION-`<slug>`-restore | restore | /data-migration-safety | backup | release | `<path>` | Pending / Done / Blocked |

## 6. 判定

| 条件 | 结论 (Verdict) |
| ------ | --------- |
| DAG 无环、阻塞清零、证据齐 | PASS |
| DAG 有环 | FAIL：报告最小环路 |
| 共享域并行无锁定策略 | FAIL：禁止并行 |
| rollback-data 节点缺失但 release rollback 依赖数据恢复 | FAIL：R-RDY-6 阻塞 |
