---
name: data-migration-safety
description: 数据迁移安全闸口：审计 schema migration、backfill、批量删除、数据修复、备份、restore 演练、dry-run、迁移 DAG 与数据回滚；产出 migration gate packet 供 /release-deploy R-RDY-6 消费。
argument-hint: "要审计哪个数据迁移？"
disable-model-invocation: true
---


# /data-migration-safety · 数据迁移安全闸口

**定位**：把 schema migration / backfill / data repair / batch delete / restore / downgrade / shadow write 等真实数据副作用变成可审计、可回滚、可阻塞 release 的迁移安全流程；产出 `migration-gate-packet.md`，作为 `/release-deploy` `R-RDY-6 Migration Gate` 的事实源。

**边界**：只做数据迁移安全审计、计划验证、dry-run / backup / restore 演练要求、迁移 DAG 与 gate packet；不替代 `/specs-write` 设计迁移需求，不替代 `/specs-execute` 写迁移代码，不替代 `/release-deploy` 执行发布，不替代 `/observability-incident` 事故响应。真实生产 migration / backfill / delete / restore 必须重新经过用户批准。

**斜杠命令**：`/data-migration-safety`

**上游 / 下游**：上游消费 `NFR-REL-*`、`DSN-DB-* Migration Strategy`、tasks.md `Verification Commands / Revert Command / Artifacts`；下游输出 migration gate packet 给 `/release-deploy` `R-RDY-6`，数据事故或 restore 失败分流 `/observability-incident`，spec 缺陷回切 `/specs-write`。

---

## 懒加载契约

- **MUST read**: `./decision-matrix.md`
- 开始判定或执行 Phase 流程前，必须完整懒加载上述细节。

---

## 1. 伴随文档

| 文档 | 角色 | 何时读 |
| ------ | ------ | -------- |
| `protocols/migration-gate-protocol.md` | migration 范围、策略、红绿判定 | Phase 1 / 2 |
| `protocols/dry-run-backup-restore-protocol.md` | dry-run、backup、restore rehearsal 与证据过期规则 | Phase 3 / 4 |
| `protocols/migration-dag-protocol.md` | migration DAG、依赖、并行安全、rollback 依赖 | Phase 2 / 5 |
| `templates/migration-gate-packet-template.md` | R-RDY-6 可消费 packet 模板 | Phase 5 |

## 2. 阶段骨架

| Phase | 目标 | MUST read | 输出 |
| ------- | ------ | ----------- | ------ |
| Phase 1 — Scope Intake | 确认 migration 类型、环境、数据域、上游锚点 | `protocols/migration-gate-protocol.md` | `/data-migration-safety:MIGRATION_SCOPE_DEFINED` |
| Phase 2 — Plan & DAG Audit | 审查 Migration Strategy、Task、DAG、rollback 依赖 | `protocols/migration-dag-protocol.md` | migration DAG |
| Phase 3 — Dry-run Evidence | 验证 dry-run、row-count、idempotency、chunking、drift | `protocols/dry-run-backup-restore-protocol.md` | dry-run evidence |
| Phase 4 — Backup / Restore | 验证 backup、restore rehearsal、downgrade / abort | `protocols/dry-run-backup-restore-protocol.md` | restore evidence |
| Phase 5 — Gate Packet | 装配 migration gate packet，给 release readiness | `templates/migration-gate-packet-template.md` | `/data-migration-safety:MIGRATION_GATE_PACKET_READY` 或 `/data-migration-safety:MIGRATION_BLOCKED` |

## 3. 输出格式

```markdown
## 数据迁移安全审计报告 (Data Migration Safety Report)

## 工作流状态 (Workflow State)

- State: /data-migration-safety:<STATE>

## 审计范围 (Scope)

- 关联 Feature 标识 (Feature): <slug>
- 迁移类型 (Migration type): 结构变更 (schema) | 数据回填 (backfill) | 数据修复 (repair) | 数据删除 (delete) | 数据恢复 (restore) | 降级 (downgrade)
- 审计环境 (Environment): 本地 (local) | 测试环境 (staging) | 生产环境 (production)

## 审计结论 (Verdict)

- R-RDY-6 迁移安全门禁 (R-RDY-6 Migration Gate): PASS / FAIL
- 阻碍性缺陷 (Blocking gaps): <None or list>

## 推荐接续路由 (Required Route)

- /release-deploy | /specs-write | /specs-execute | /observability-incident

```

## 4. 禁用行为

| 禁止项 | 原因 |
| -------- | ------ |
| 不执行真实生产 migration | 本 workflow 只审计与装配 packet；真实执行归 `/release-deploy` 且需用户批准 |
| 不用代码 rollback 代替数据 restore | 数据状态与代码状态不同步会造成二次事故 |
| 不把 dry-run 缺失标为可接受风险 | R-RDY-6 Critical，缺事实源即 FAIL |
| 不把不可回滚动作藏在脚注 | destructive change 必须显式不可回滚披露 |
| 不在 evidence 过期后复用旧 packet | dry-run / backup / restore evidence 过期需重跑 |

## 5. 快速自检清单

报告前自检：

- [ ] 是否已确认本次数据迁移的类型、运行环境以及受影响的数据域？
- [ ] 迁移计划与 DAG 依赖是否经过了并行安全与回滚依赖审查？
- [ ] 本地或测试环境中是否已验证 Dry-run、幂等性、行数及分批处理？
- [ ] 备份与恢复（Restore Rehearsal）演练是否成功，且演练证据在有效期内？
- [ ] 真实发布前，是否已将装配的数据迁移安全包（Migration Gate Packet）提报至 `/release-deploy`？

## 支撑资源

- [decision-matrix.md](./references/decision-matrix.md)
- [dry-run-backup-restore-protocol.md](./protocols/dry-run-backup-restore-protocol.md)
- [migration-dag-protocol.md](./protocols/migration-dag-protocol.md)
- [migration-gate-packet-template.md](./templates/migration-gate-packet-template.md)
- [migration-gate-protocol.md](./protocols/migration-gate-protocol.md)
