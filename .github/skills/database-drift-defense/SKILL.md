---
name: database-drift-defense
description: 数据库 Schema 漂移防线哲学框架——任何 Schema/ORM/索引/CHECK/触发器/视图变更必须通过的分层防御体系。Use when making database schema changes, designing migration pipelines, or setting up DB drift guardrails.
argument-hint: "数据库 Schema 变更？"
---

# 数据库漂移防线 · Database Drift Defense

> **核心哲学**：Schema 变更不是一次性动作，而是**持续性契约维护**。每一个 `ALTER TABLE`、每一次索引创建、每一条 CHECK 约束，都在向系统承诺"这层逻辑将保持同步"。漂移防线的作用不是阻止变更，而是**让每一次变更都有可追溯、可验证、可回滚的证据**。

---

## 0. 触发与分流

| ID | 条件 | 动作 |
| --- | --- | --- |
| R-DD-1 | 进行数据库 Schema / ORM / 索引 / CHECK / 触发器 / 视图任何变更 | 加载 14 层防线核对清单 |
| R-DD-2 | CI/CD 中 `ci_db_alignment` 任一 FAIL | 逐层定位漂移根因 |
| R-DD-3 | 首次为项目搭建数据库漂移防线 | 参考本框架设计适合项目的防线 |
| R-DD-4 | 仅讨论 DB 架构设计，未涉及 Schema 物理变更 | 不触发，仍归 `specs-write` / `specs-execute` |

---

## 1. 哲学：为什么要 14 层

### 1.1 防线不是安全网，是契约网

传统 "schema.sql 是真理" 的想法在单一开发者场景勉强可行，但一旦引入多环境（PostgreSQL / SQLite）、多端（后端 ORM / 前端 SQLite）、CI/CD、真实生产数据后，**schema.sql 只是诸多"对数据库的陈述"之一**：

- ORM 模型是对数据库的 Python/TypeScript 陈述
- 真库索引是对数据库的 Postgres 引擎陈述
- 前端 SQLite 是对数据库的端侧离线陈述
- OpenAPI spec 是对数据库的消费者契约陈述

**每个陈述都在不同时间、不同工具、不同心智上下文中独立演化。** 漂移防线要做的就是把它们**统一拉回到同一个契约网中**——每个陈述都与其他陈述可比较。

### 1.2 分层是收敛策略

14 层不是"14 个独立检查"，而是**一条收敛链**：

```text
D1 迁移完整 → D2 静态对齐（schema ↔ ORM ↔ SQLite ↔ 真库）→
D3 视图契约 → D4 类型系统 → D5 端侧同步 → D6 外部契约
```

每层验证一个**陈述对**。D2 家族（D2.1~D2++++）在同一概念层内从粗到细逐步收紧；D3/D4/D5/D6 验证跨层陈述。

### 1.3 Baseline 不是懒惰许可证

Baseline 可以吸收已知的 legacy drift，但**"no new drift since baseline"** 才是防线目标。修掉旧 drift 时必须刷新基线固化战果；新增 drift 一律拒绝。

---

## 2. 14 层防线清单（通用哲学版）

以下清单是**任何项目**都可以嵌入的实现框架。具体脚本名称、语言、工具链由项目自行实现。

### D1 · Migration 完整性

| 属性 | 值 |
| --- | --- |
| **左侧** | `migrations/*.sql` 文件集合 |
| **右侧** | 数据库中的 `schema_migrations` 记录表 |
| **验证** | 左侧的每个 migration 都在右侧有对应记录（按 hash 或文件名） |
| **失败即** | 有 migration 文件未执行 / 有执行记录但有文件缺失 |
| **哲学** | migration 是 Schema 变更的**唯一合法路径**；绕过 migration 的任何 DDL 都是漂移 |

### D1+ · Migration 命名唯一性

| 属性 | 值 |
| --- | --- |
| **验证** | migration 文件名前缀（时间戳或序号）在集合内唯一 |
| **失败即** | 两个 migration 使用相同前缀 |
| **哲学** | 时间戳冲突暴露并发开发中的未同步操作 |

### D2.1 · schema.sql ↔ ORM（PostgreSQL 方言）

| 属性 | 值 |
| --- | --- |
| **左侧** | `schema.sql`（DDL 静态语句） |
| **右侧** | ORM 模型映射到 PostgreSQL 方言的列/类型/约束 |
| **验证** | 左侧每张表、每列的类型和约束在右侧存在且一致 |
| **哲学** | DDL 是"设计意图"；ORM 是"运行时实现"；两者必须一致。不一致意味着要么 DDL 是废纸，要么 ORM 不能正确映射 |

### D2.2 · schema.sql ↔ SQLite

| 属性 | 值 |
| --- | --- |
| **左侧** | `schema.sql`（SQLite 方言段落） |
| **右侧** | 端侧 SQLite 数据库文件的实际 schema |
| **验证** | 左侧表/列/类型在右侧一致 |
| **哲学** | 前后端同步场景（离线优先 App）会出现后端用 PG、前端用 SQLite，两者 schema 必须可比较 |

### D2.3 · schema.sql ↔ 真实生产数据库

| 属性 | 值 |
| --- | --- |
| **左侧** | `schema.sql` |
| **右侧** | 真实生产 PostgreSQL 的 `information_schema.columns` / `pg_indexes` 等系统视图 |
| **验证** | 真实库 ≤ schema.sql（右侧可以有更多历史列，但不能少列、不能类型错） |
| **哲学** | 生产环境是终极真相；任何其他陈述如果与生产冲突，以生产为准并触发调查 |

### D2.4 · 基线吸收政策合规性

| 属性 | 值 |
| --- | --- |
| **验证** | 当前 baseline 文件中的"已知漂移"都在合法吸收清单内 |
| **哲学** | baseline 不是垃圾桶——只有明确审查过的 legacy drift 才能被吸收 |

### D2+ · 列类型漂移

| 属性 | 值 |
| --- | --- |
| **左侧** | `schema.sql` 每列的类型字面量 |
| **右侧** | ORM 每列的 `column.type.compile(dialect)` |
| **验证** | 字面量一致（如 `VARCHAR(255)` vs `String(255)` 需归一化后比对） |
| **哲学** | 类型漂移是最隐蔽的 bug——数据库接受的列宽和 ORM 认为的列宽不一致可能导致静默截断 |

### D2++ · CHECK 约束体

| 属性 | 值 |
| --- | --- |
| **左侧** | `schema.sql` 中所有 `CHECK (...)` 表达式 |
| **右侧** | ORM 中所有 `CheckConstraint` 定义 |
| **哲学** | CHECK 是数据库级业务规则；ORM 层如果缺少它，应用程序可能接受不合规数据 |

### D2+++ · 索引漂移

| 属性 | 值 |
| --- | --- |
| **左侧** | `schema.sql` 中 `CREATE INDEX` / `CREATE UNIQUE INDEX` 语句 |
| **右侧** | 真库 `pg_indexes` 系统视图 |
| **验证** | 每个左侧索引在右侧存在且列组合一致 |
| **哲学** | 索引是查询性能契约；缺失索引 = 慢查询炸弹；多余索引 = 写入负担 |

### D2++++ · 触发器 / 函数漂移

| 属性 | 值 |
| --- | --- |
| **左侧** | `schema.sql` 中 `CREATE TRIGGER` / `CREATE FUNCTION` |
| **右侧** | 真库 `pg_trigger` + `pg_proc` |
| **哲学** | 触发器是数据库级业务逻辑，变更风险极高，必须纳入防线 |

### D3 · 视图列契约

| 属性 | 值 |
| --- | --- |
| **左侧** | `schema.sql` 中 `CREATE VIEW` 的列数 |
| **右侧** | 真库 `information_schema.columns` 对应视图列数 |
| **验证** | 列数一致（跨方言时名称可能不同，但数目和类型必须对应） |
| **哲学** | 视图是 API 消费者看到的"虚拟表"；列契约断裂破坏所有依赖该视图的代码 |

### D4 · 类型系统对齐（mypy / tsc）

| 属性 | 值 |
| --- | --- |
| **验证** | 项目类型检查器（mypy / tsc）对 ORM 层的错误数 ≤ baseline |
| **哲学** | 类型系统漂移 = ORM 接口契约漂移；新增 type error 意味着某个消费者被破坏 |

### D5 · 端侧同步与契约

| 属性 | 值 |
| --- | --- |
| **验证** | 前端 TypeScript 数据模型与后端 DSN 契约一致 |
| **哲学** | 前后端分离架构中，端侧离线库和后端表结构的契约是双边绑定——任一边变更必须触发另一边同步 |

### D6 · OpenAPI 契约冻结

| 属性 | 值 |
| --- | --- |
| **左侧** | 运行时 `app.openapi()` 生成的 spec |
| **右侧** | 冻结的 `OPENAPI_SPEC.json` |
| **验证** | 两者一致；不一致 = API 契约已漂移 |
| **哲学** | OpenAPI spec 是外部调用者的契约；任何不通知的契约变更都是对他们代码的破坏 |

---

## 3. 防线嵌入指南（如何落地）

### 3.1 最少启动集合（3 层）

如果你的项目刚起步，不需要 14 层全上。从这 3 层开始：

1. **D1**（migration 完整性）—— 至少确保 migration 被执行
2. **D2.1**（schema ↔ ORM）—— 防止 DDL 和代码分裂
3. **D2+++**（索引漂移）—— 防止手工创建的索引被 ORM 覆盖

### 3.2 CI 编排

推荐做法：

- D1~D4：每次 PR 进入 CI（预发/Staging 环境）
- D5：pre-commit 本地拦截（快速反馈）
- D6：release 前 CI 特殊检查
- 生产对比（D2.3）：仅在 Staging 环境 CI 中跑，不直连生产

### 3.3 Baseline 刷新准则

- **允许刷新**：修掉了已知 legacy drift（如补了一个被 ORM 遗漏的历史列）
- **禁止刷新**：新增了未审查的 drift、临时 hack
- **刷新后必须**：在 PR 描述中列出"本次 baseline 变化"，含增删项和理由

---

## 4. 现实建议

### 4.1 不是所有项目都需要 14 层

- **单人小项目**：D1 + D2.1 + D2+++ 足够
- **前后端分离 App**：追加 D2.2（SQLite 对齐）+ D5（端侧同步）
- **多环境 / 多消费者**：追加 D2.3（生产对齐）+ D3（视图）+ D6（OpenAPI）
- **金融 / 医疗 / 合规**：全量 14 层 + 人工审批 Gate

### 4.2 防线不是性能杀手

大部分防线检查是**静态对比**（schema.sql vs ORM code），不连真库；只有 D2.3 / D2+++ / D2++++ 需要连库，这些应放在 staging CI 中，不阻塞本地开发。

### 4.3 与 DoD 门禁的关系

14 层防线 ALL GREEN 是 `database.instructions.md` 中 Schema 变更 DoD 的**强制前置**。详见 [`.github/instructions/database.instructions.md`](../../instructions/database.instructions.md)。

---

## 5. 实现模式（可复制的检查脚本骨架）

以下是核心防线层级的**可复制实现模式**。语言/框架无关，可直接翻译为 Python / TypeScript / Bash。

### 5.1 D2.1 模式：DDL ↔ ORM 列对比

```text
## 伪代码骨架——任何语言都可用此逻辑

function check_ddl_vs_orm():
    ddl_columns = parse_schema_sql("schema.sql")  # {table: {col: type}}
    orm_columns = introspect_orm_models()          # {table: {col: type}}
    errors = []

    for table in ddl_columns:
        if table not in orm_columns:
            errors.append(f"Table {table} in DDL but not in ORM")
            continue
        for col, typ in ddl_columns[table].items():
            if col not in orm_columns[table]:
                errors.append(f"Column {table}.{col} in DDL but not in ORM")
            elif normalize_type(typ) != normalize_type(orm_columns[table][col]):
                errors.append(f"Type mismatch: {table}.{col} DDL={typ} ORM={orm_columns[table][col]}")

    return errors  # 空列表 = PASS
```

**关键点**：类型归一化（`VARCHAR(255)` = `String(255)` = `varchar`）是最大坑。建议先做 DDL 侧解析时统一 lowercase，再对比。

### 5.2 D2+++ 模式：索引对比（需要连库）

```text
function check_indexes():
    ddl_indexes = parse_create_index_from_schema_sql("schema.sql")
    # 格式: {index_name: {table, columns[], unique}}

    live_indexes = query("""
        SELECT indexname, indexdef
        FROM pg_indexes
        WHERE schemaname = 'public'
    """)  # 用 MCP 执行

    errors = []
    for idx_name, idx_def in ddl_indexes.items():
        if idx_name not in live_indexes:
            errors.append(f"Index {idx_name} in DDL but missing in live DB")
        else:
            # 对比列组合（解析 CREATE INDEX 语句）
            ddl_cols = extract_columns(idx_def["definition"])
            live_cols = extract_columns(live_indexes[idx_name])
            if ddl_cols != live_cols:
                errors.append(f"Index {idx_name} column mismatch: DDL={ddl_cols} Live={live_cols}")

    return errors
```

### 5.3 通用校验脚本入口模式

```text
## 推荐的项目目录结构：

scripts/
  drift/
    check_schema_ddl_vs_orm.py    # D2.1
    check_indexes.py              # D2+++
    check_constraints.py          # D2++
    check_column_types.py         # D2+
    check_triggers.py             # D2++++
    check_openapi_spec.py         # D6
    ci_db_alignment.sh            # 一键编排入口
    ci_db_alignment.ps1           # Windows 对等

## ci_db_alignment.sh 骨架：

#!/bin/bash
set -e
FAILED=""
run_check() { python scripts/drift/$1 || FAILED="$FAILED $1"; }

run_check check_schema_ddl_vs_orm.py
run_check check_indexes.py
run_check check_constraints.py
# ... 依次跑 14 层

if [ -n "$FAILED" ]; then
  echo "FAILED:$FAILED" >&2
  exit 1
fi
echo "ALL GREEN - 14-layer drift defenses passed"
```

---

## 6. CI 集成示例（GitHub Actions）

```yaml
## .github/workflows/db-drift.yml

name: Database Drift Defense
on:
  pull_request:
    paths:
      - "database/schema/**"
      - "backend/models/**"
      - "migrations/**"

jobs:
  drift-check:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_PASSWORD: drift_test
        ports:
          - 5432:5432
    steps:
      - uses: actions/checkout@v4
      - name: Apply migrations
        run: python scripts/run_migrations.py --apply
      - name: Run 14-layer drift defense
        run: bash scripts/drift/ci_db_alignment.sh
```

**注意**：生产对比（D2.3）**不应**在此 workflow 中跑——生产数据库凭证不应出现在 CI 环境变量中。D2.3 的建议做法是：

1. CI 触发后，由维护者手动在本地跑 `check_schema_drift.py --target production`（通过 MCP 连接）
2. 或者在 staging 环境 CI 中单独配置只读副本凭证

---

## 7. Baseline 文件格式

每条防线的 baseline 存储已知 legacy drift。推荐 JSON 格式：

```json
{
  "_meta": {
    "generated_at": "2026-06-27T10:00:00+08:00",
    "layer": "D2.1",
    "target": "postgres",
    "allowed_drift_count": 3,
    "policy": "no_new_drift_since_baseline"
  },
  "known_drifts": [
    {
      "id": "DRIFT-001",
      "table": "legacy_orders",
      "column": "shipping_method",
      "ddl_type": "VARCHAR(100)",
      "orm_type": "String(50)",
      "reviewed_by": "calvin",
      "reviewed_at": "2026-05-15",
      "reason": "旧列宽与历史数据兼容，下一大版本统一",
      "expires_at": "v3.0.0"
    }
  ]
}
```

**硬规则**：

- 每条 `known_drifts` 必须有 `reviewed_by` + `reviewed_at` + `reason` + `expires_at`（或 `expires_at: "never"` 需特殊审批）
- 缺少任一字段 = baseline 不合法，应视为所有 drift 为新漂移
- Baseline 文件必须随代码一起版本控制（`database/schema/*_BASELINE.json`）

---

## 8. 逐层失败处置指南

| 层 | 失败场景 | 处置动作 | 不可绕过 |
| --- | --- | --- | --- |
| **D1** | migration 未执行 | 运行 migration；检查 CI pipeline 是否遗漏 | 严禁手动补 DDL 绕过 migration |
| **D1+** | 时间戳冲突 | 合并分支后重新生成唯一时间戳 | 按 `git merge` 时间重排 |
| **D2.1** | DDL 与 ORM 列不一致 | 确定哪个是真源（DDL 是设计意图，ORM 是运行时）→ 对齐另一侧 | 不允许同时改两侧但不验证 |
| **D2.2** | SQLite 与 PG 不一致 | 确认是否是有意方言差异；无意差异 → 对齐 SQLite 段 | 方言差异需在 schema.sql 中显式注释 |
| **D2.3** | 生产库有额外列 | 先确认是否是合法运维操作（如 DBA 添加的监控列）→ 合法则吸收到 baseline；非法则评估回滚 | 涉及生产环境操作必须走 Gate C 审批 |
| **D2.4** | baseline 有未审查项 | 补齐 `reviewed_by` + `reason`；无法补齐的移出 baseline 视为新漂移 | 不允许"先加 baseline 后审" |
| **D2+~D2++++** | 列类型/约束/索引/触发器漂移 | 以 `schema.sql` 为准，修正 ORM 或刷新 baseline | 必须先改 schema.sql，再同步 ORM |
| **D3** | 视图列数不对 | 检查最近是否有人改了 VIEW 定义但没更新 schema.sql | VIEW 变更必须同时改 schema.sql |
| **D4** | type error 增加 | 修正类型标注或更新 baseline | 新增 type error 绝不能靠改 baseline 掩盖 |
| **D5** | 端侧数据模型过期 | 同步前后端类型定义 | 前端离线库 schema 必须与后端 DDL 同步变更 |
| **D6** | OpenAPI spec 漂移 | 重新冻结 spec 并更新 `OPENAPI_SPEC.json` | spec 变更必须在 PR 描述中列出 breaking change |

---

## 9. 相关资源

- **完整实现参考**：14 层防线的完整 Python 实现（含 baseline 管理、CI 编排、MCP 集成）存在于生产项目中。本 skill 提取其哲学与模式层，使其可被任何项目采用。
- **相关文档**：Schema 变更 SOP 见 `database.instructions.md`（`applyTo: '**/*.sql'` 自动加载）；Gate C 审批见 `rules.instructions.md` §1.1；MCP 工具使用规范见项目开发协议 §3.2。
