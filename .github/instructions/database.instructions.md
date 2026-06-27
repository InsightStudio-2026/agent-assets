---
name: 数据库规范
description: SQL Schema 设计与 Migration 规范。编辑 .sql 文件或执行数据库操作时自动加载。
applyTo: '**/*.sql'
---

# 数据库开发规范

> 编辑 SQL / Migration 文件时自动生效。本文档是数据库漂移防线的权威 SSOT。

## 铁律

任何涉及数据库 Schema、ORM、索引、CHECK、触发器、视图、API 契约的变更，完成前必须跑 **14 层 drift 防线** ALL GREEN。任一层 FAIL 等同于 DoD 未通过。涉及真库检查必须通过 MCP 工具集，不得用裸 `psql`。Migration 必须幂等（`IF NOT EXISTS` / `ON CONFLICT DO NOTHING`）。表字段名、字段注释必须使用中文。

## 1. 14 层防线哲学

14 层漂移防线是**哲学框架**，不是特定脚本名。任何项目的数据库 Schema 变更都应该通过类似的分层验证。完整哲学见 skill [database-drift-defense](../skills/database-drift-defense/SKILL.md)。

防线清单速查：

| 层 | 防线名 | 左侧真源 | 右侧被比对 | 验证手段 |
|---|---|---|---|---|
| **D1** | migration 完整性 | `migrations/*.sql` sha256 | `schema_migrations` 表记录 | `SELECT * FROM schema_migrations`（MCP） |
| **D1+** | migration 时间戳唯一 | migration 文件名前缀集合 | 自检 | 文件系统 glob |
| **D2.1** | schema.sql ↔ ORM | `schema.sql` 列/类型/约束 | ORM Model column/type | 目视对比 + pytest snapshot |
| **D2.2** | schema.sql ↔ SQLite | `schema.sql` SQLite 段 | 端侧 SQLite `.schema` | `sqlite3 <db> ".schema"`（MCP） |
| **D2.3** | schema.sql ↔ 真库 | `schema.sql` | `information_schema.columns` | `SELECT column_name, data_type FROM information_schema.columns WHERE table_name='...'`（MCP） |
| **D2.4** | 基线吸收政策合规 | baseline JSON 文件 | 合法吸收清单 | 逐条核对 `reviewed_by` + `reason` + `expires_at` |
| **D2+** | 列类型漂移 | `schema.sql` 列类型字面量 | ORM column type | 类型字面对比脚本 |
| **D2++** | CHECK 约束体 | `schema.sql` CHECK 表达式 | ORM CheckConstraint | 逐个核对 |
| **D2+++** | 索引漂移 | `schema.sql` CREATE INDEX | `pg_indexes` 系统视图 | `SELECT indexname, indexdef FROM pg_indexes WHERE schemaname='public'`（MCP） |
| **D2++++** | 触发器/函数漂移 | `schema.sql` TRIGGER/FUNCTION | `pg_trigger` + `pg_proc` | `SELECT tgname FROM pg_trigger`（MCP） |
| **D3** | 视图列契约 | `schema.sql` VIEW 列数 | `information_schema.columns` | `SELECT column_name FROM information_schema.columns WHERE table_name='...'`（MCP） |
| **D4** | 类型系统对齐 | ORM 代码 | mypy/tsc baseline | `mypy backend/` / `npx tsc --noEmit` |
| **D5** | 端侧同步 | 前端数据模型 | 后端 DSN 契约 | pre-commit 本地拦截 |
| **D6** | OpenAPI 契约冻结 | 运行时 `openapi()` 输出 | 冻结 spec JSON | JSON diff |

> **说明**：D5 属于端侧数据同步与 APP 消费契约校验，主要在 pre-commit 阶段进行本地拦截。在 CI 编排中默认 bypass（不重复检查），可通过 pre-commit hook 单独重跑。
>
> **"drift baseline zero" 不是最终目标**（基线可以吸收已知的 legacy drift），**"no new drift since baseline" 才是**。修掉旧 drift 时务必刷新基线固化战果；新增 drift 一律拒绝提交。

## 2. 防线实现指南（MCP 驱动）

项目自行实现防线验证脚本时，**优先使用 MCP 工具集**连接数据库进行读回验证（PostgreSQL MCP / SQLite MCP），禁止裸 `psql` / `sqlite3` 命令行。后者绕过了智能体的审计记录，使漂移证据不可追溯。

```text
## 人工/MCP 检查流程示例

D1 验证：
  - 列出 migrations/ 目录下所有 .sql 文件
  - 用 MCP SELECT * FROM schema_migrations 对比执行记录

D2.3 验证（真库对比）：
  - 用 MCP SELECT column_name, data_type, is_nullable FROM information_schema.columns
    WHERE table_schema='public' ORDER BY table_name, ordinal_position
  - 与 schema.sql 逐列对比
```

## 3. 防线嵌入（项目落地指南）

### 最少启动集合（3 层）

单人小项目从以下开始：

1. **D1**（migration 完整性）—— 确保 migration 被执行
2. **D2.1**（schema ↔ ORM）—— 防止 DDL 和代码分裂
3. **D2+++**（索引漂移）—— 防止手工创建的索引被 ORM 覆盖

### CI 编排建议

```text
推荐做法：
- D1~D4：每次 PR 进入 CI（预发/Staging 环境）
- D5：pre-commit 本地拦截（快速反馈）
- D6：release 前 CI 特殊检查
- 生产对比（D2.3）：仅在 Staging 环境 CI 中跑，不直连生产
```

### Baseline 刷新准则

- **允许刷新**：修掉了已知 legacy drift（如补了一个被 ORM 遗漏的历史列）
- **禁止刷新**：新增了未审查的 drift、临时 hack
- **刷新后必须**：在 PR 描述中列出"本次 baseline 变化"，含增删项和理由

## 4. Schema 变更 SOP（强制顺序）

1. **改 SSOT**：先改 `database/schema/schema.sql`
2. **写 migration**：`database/migrations/YYYYMMDD_HHMMSS_描述.sql`，必须幂等
3. **应用到真库**：PostgreSQL 用 MCP；SQLite 直接 exec
4. **同步 ORM**：更新 ORM 模型文件
5. **MCP 读回验证**：对照 ORM 字段
6. **跑 14 层防线**：逐层 CHECK，必须 ALL GREEN
7. **baseline 刷新**：仅当 drift 合法变窄时
8. **跑测试**：`pytest` / `jest` 全量通过
