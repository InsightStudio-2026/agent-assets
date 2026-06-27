# tasks.md 硬规则

> **When to read**: 在 `/specs-write` Phase 4 落 `tasks.md` 前，必须与 `templates/tasks.md`、`appendix.md §A.1-A.6` 一起读取。
>
> Cross-references: `cross-cutting.md §4` covers `handoff-payload.yaml`; `appendix.md §A.*` covers 防 1-5 / 抢占式中断 / Reflections.

---

## 1. Tasks 硬规则

> 本节按规则码分类。字段格式 / 防 1-5 详细约束见 `appendix.md §A.*`；schema 字段见 `cross-cutting.md §4`。

**任务粒度**：

- 每个 Task ≤ 1 day 工作量；超出 → 拆分。
- 必须可独立测试（Red→Green→Refactor）。
- 必须可独立回滚（提供 `Revert Command`）；纯文档 / 注释 Task 可填 `Revert Command: N/A (无副作用)`。

**Task 头部必填字段**（22 项 · 本节为字段清单 · 字段定义见 `cross-cutting.md §4` / `appendix.md §A.*`）：

`Phase / Type / Priority / Status / Implements / Depends On / Design Refs / Derived From / Relation to Existing / Touches / Existing Touches / Reuse Notes / Effort / Test Anchors（appendix.md §A.2）/ Verification Commands / Artifacts / Revert Command（appendix.md §A.3）/ Revert Conflict Risk（appendix.md §A.3）/ Anti-Invariants（appendix.md §A.5）/ Resume Strategy（appendix.md §A.6 条件化）/ Context Required Before Execution（appendix.md §A.5）/ Reflections（appendix.md §A.7，执行端写入）`。

**字段二分（A 类执行追踪型 vs B 类规约型 · checkbox 强制规则）**：

- **A 类执行追踪型**（Touches / Existing Touches / Verification Commands / Artifacts）→ **每条以 `- [ ]` 起首**，执行端 Phase 4-7 边写边勾，作为 Task 完成度二级证据。
- **B 类规约型**（其余字段：Phase / Type / Priority / Status / Implements / Depends On / Design Refs / Derived From / Relation to Existing / Reuse Notes / Effort / Test Anchors / Revert Command / Revert Conflict Risk / Anti-Invariants / Resume Strategy / Context Required / Reflections）→ 写作端定值或执行端结构化更新，使用普通 `-` 即可，**严禁误用 `[ ]`**。
- 模板示例与实际产出 spec 必须一致；两者风格混用视为违规。

**协议自检（落 spec 前）**：每个 Task 必须 grep `\[ \]` 命中数 = `len(Touches) + len(Existing Touches) + len(Verification Commands) + len(Artifacts)`；其他字段命中即违规。

**Traceability Matrix · `tasks.md` 顶部**：

```markdown
<!-- generated-from: handoff-payload.yaml#traceability -->

|  | Task | Implements | Design Refs | Existing | Anti-Invariants | BDD Scenarios Owned | Artifacts |  |
|  | ------ | ------------ | ------------- | ---------- | ----------------- | --------------------- | ----------- |  |
|  | TASK-001 | REQ-001 | DSN-API-001 | Replaces EXIST-DSN-DB-003 | INV-LIM-001 | REQ-001.S1 | reports/plan_001.json |  |
|  | TASK-002 | REQ-002 | DSN-DB-002 | Net New | — | REQ-002.S1 · REQ-002.S2 | reports/cost_ledger.jsonl |  |
```

每个 Task 必须出现在矩阵中，且字段必须自洽（详 `appendix.md §A.1` 防 1）。`Existing` 列：填 `N/A (mode=Greenfield)` 或 `N/A (mode=Seed)` 优于留空。

**BDD 场景所有权**（详 `appendix.md §A.2` 防 2）：每个 BDD Scenario 必须**只属于一个**Task；多 Task 共享同一 Scenario = 失格。Scenario 颗粒过粗导致跨 Task 边界 → 拆 Scenario。**Test Anchors**（详 `appendix.md §A.2` 防 2）：除纯文档 / 纯配置 Task 外，每个 Task 必须列 `Test Anchors:` 至少 1 条 `path: <test_file_path>`；**Phase 4 Red 末锁定 sha256（执行端 `phase-rules.md §4.2` [TDD-Lock]）**；Phase 5 Green 仅校验不重写（执行端 `phase-rules.md §5.2` 测试冻结令）；Phase 6 Refactor 改测试 → 同步重锁 + Reflections 以 `kind: test_modified` 留痕。

**Revert Conflict Risk**（详 `appendix.md §A.3` 防 3）：填了非 N/A `Revert Command` 且与先行 Done Task 共享 `Existing Touches` 者，**必须**逐对列 `shared_with` + `shared_files`；首个 Task / 无共享填 `N/A (no shared files with prior Done tasks)`。

**`Revert Command` 五条铁律**（任一命中必填非 N/A；下面 5 条为触发条件，后面 2 条为豁免形式）：

1. 修改 / 删除既有源码或既有迁移
2. 改既有 API 契约 / 既有 DB schema 已部署版
3. 改既有进程拓扑 / 部署方式 / 启动入口
4. 改既有 ORM 模型与既有数据
5. 写入 cloud / 本地非源码状态（生成产物文件、模型文件）

- **纯新增源码文件**可填 `Revert Command: git rm<file>+ git checkout HEAD -- <related>`

-**纯文档 / 注释 Task**可填 `Revert Command: N/A (无副作用)`**DSN-DB "Replaces" 迁移策略与 Task 联动**（条件化必填）：凡 Task 的 `Design Refs` 包含被要求 `Migration Strategy` 三选一的 `DSN-DB-*` 者：

- `Verification Commands` 必含一致性校验命令——shadow_write → 双写 diff 脚本；backward_compatible_stepwise → 本阶段子集验证；downgrade_script → down-migration dry-run + 表行数不变验证。
- `Revert Command` 必须是**业务可回**（指向上述迁移策略的 down/cutover-rollback 路径）而非纯物理丢数据的 `git checkout` 型。
- `Existing Touches` 必含被变更表的 ORM / repository / 迁移文件三者间一致性路径。

**Context Required Before Execution**（详 `appendix.md §A.5` 防 5 · 严格二分）：

- **P0 Essential**（上限 5 条 · 跨边界 / 动凭据 Task 上限 7 条）：执行端 Phase 2 Hydrate 必逐条复述 ≥ 1 句原文；跨边界 Task 必含适用 INV-* / Failure Strategy / Concurrency & Lock。
- **P1 Reference**：备查；执行端 attention_budget 超限时可不入初轮 Prompt，仅按需拉取。
- P0 超上限 → 视为 Task 裁切不够细，回 Phase 4 拆分。

**INV-* 反向追溯**（详 `appendix.md §A.5`）：每个 Task 必须列出 `Anti-Invariants`（本 Task 严禁违反的 INV-*，列在 Traceability Matrix 与 P0 Essential 中）。

**Test Plan / DoD / Rollback**章节必须分别给出（详 `templates/tasks.md`）。**DB Test Isolation 三档优先级 + 三要素**（条件化必填）：凡 Task 的 `Test Anchors` 包含写入真实数据库 / SQLite / 真实文件系统者，必须在 `Test Plan` 内**先选档再答三要素**：

**档位（按优先级降序 · 选最轻可用方案 + 必述选档理由）**：

- **Tier 1（首选）· 测试框架事务级 fixture**：pytest `db_session` rollback fixture / SQLAlchemy `nested transaction` / Django `TransactionTestCase` / pytest-django `db` fixture。适用：单 connection、读写都走 ORM、测试间无 DDL。
- **Tier 2（次选）· 裸 SQL `BEGIN; ... ROLLBACK;`**：仅适用于单 connection、仅读 / 轻量写场景；测试代码自管 transaction 边界。
- **Tier 3（仅 DDL / 完整重置）· 整库 reset / 升降级脚本**：项目层 `db_reset` / `db_downgrade` 槽位（`project-adapter.md §1`）。**仅限**：schema migration / 跨 connection 并发写 / 生产 dump 还原；首尾同框附 reset + seed 脚本，并必须说明**为何不能用 Tier 1/2 事务隔离**。
- **N/A（不触 DB / 不写 FS）**：`DB Isolation: N/A (no DB state)`，纯计算 / 纯函数 / 纯 grep / 纯文档可填。

**三要素（选档后必证）**：

- (a) **隔离机制**：写明所选 Tier 的具体落地手段（fixture 名 / SQL 包裹 / 重置脚本路径）。
- (b) **副作用边界**：测试是否动用户级生产路径、是否生成本地缓存 / 模型文件 / 临时表，且收尾如何清理（持久化用途的副作用必须显式声明）。
- (c) **不再测后留垃圾**：每个测试结束后磁盘 / DB 状态必须可断言为初始态（或显式声明持久化用途的副作用）。

**反模式**：

- ❌ 跳过档位选择直接写三要素 → 视为漏选档，回 `task-rules.md §1` 补理由。
- ❌ 选 Tier 3 但不说明“为何不能用 Tier 1/2” → 视为豁免理由不足。
- ❌ Tier 3 缺 reset / seed 配套 → 视为隔离不闭环。
- ❌ 跨 connection 并发写场景仍用 Tier 1 → 选档错误，必拆 Tier 3。

**Secret-Scan 命令**（条件化必填）：凡当前 Task 适用至少一条 `INV-SEC-*`（在 `Anti-Invariants` 中列出），且 `Touches` / `Existing Touches` 涉及以下任一类资源：

- 凭据读取 / 写入路径（KMS / Vault / keyring / 配置文件中的 token）
- 第三方 API 客户端（含 SDK / HTTP client wrapper）
- `.env` / 环境变量注入入口
- 遥测 / 日志输出路径（可能写入凭据）
- 凭据轮转 / 失效流程

→ `Verification Commands` **必含一条** secret-scan 命令（项目层 `project-adapter.md §1` `secret_scan_tool` 槽位注入具体工具，如 `gitleaks` / `trufflehog`），且执行端 `phase-rules.md §7.1` Verify 必跑该命令并要求 0 告警；豁免情形（如纯查询命令、不涉敏感字段）必须在 `Test Plan` 显式注明豁免理由 + 引用适用的 `INV-SEC-*` 原文。

**Architectural Invariant Compliance**：每个 Task 必须显式声明 `Anti-Invariants:`（charter.md `## 5` 中本 Task 严禁违反的 INV-* 列表，详 `appendix.md §A.5`）；为空填 `Anti-Invariants: none (no applicable INV-* in scope)`。

**WIP Branch Reset 协议**（条件化 · 详 `appendix.md §A.6` 抢占式中断）：凡当前 Task 的 `Touches` ≥ 5 条或包含跨模块改动者，写作端预留 `Resume Strategy` 字段两枚举（`lightweight_wip_commit` / `wip_branch_reset`）；执行端按 `tasks_completed_count_at_pause` 决策。**禁用 `git stash` 模式**·详 `appendix.md §A.6.2`。
