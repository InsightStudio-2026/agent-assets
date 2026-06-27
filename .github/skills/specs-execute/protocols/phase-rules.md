# Specs Execute  Per-Phase Detailed Rules

> **When to read**: The main workflow instructs Cascade to load **the relevant Phase section**of this file at the**entry of each Phase**, before drafting any plan / test / code / verification for that Phase. Skipping = violation of TDD lock / placeholder ban / coverage gate.
>
> Cross-references like `A.6.5` / `2.5.3` / `A.7.5` point back into the main workflow / `/specs-write` workflow.

---

## 1. Phase 1  Locate  Detailed Preflight Rules

### 1.1 前置检查（按顺序，任一失败即停）

1. 任务事实源文件存在：`<specs_root>/active/<feature-slug>/tasks.md` 存在；若是 Medium 单文件模式，则为 `spec.md` 存在（下称“任务事实源”，spec 未备付前一律在 `active/<feature-slug>/`，**不得从 `<specs_root>/<feature-slug>/` 平铺位置读取**，active → done 迁移仅在 §9.2 交付 PR 中执行）
2. 任务事实源的 `Approval.Status = Approved`
3. **`maturity-intake.md` 存在**且 `Approval.Status = Approved`、`Decision = PROCEED_TO_CHARTER`；`SSOT Health ∈ {Healthy, Needs Clarification, SSOT Absent}`，不得为 `Needs Repair` / `Unfit As Source`
4. **`charter.md` 存在**且 `Approval.Status = Acknowledged`（charter 走轻量路径，**不进入完整 Decision Gate**，故只允许 `Acknowledged`；历史 spec 误写 `Approved` → 回切 `blocking-and-rollback.md §1.3` `/specs-write` 修正状态字串后重启）
5. **Hybrid / Brownfield 项目模式分支**（二选一，按项目模式严格分支）：
    - **5a Hybrid / Brownfield 路径**：项目模式 ∈ {Hybrid, Brownfield} 时，`audit.md` 存在且 `Approval.Status = Approved`
    - **5a.1 Audit Depth Gate 防返工检查**（仅在 5a 命中时走）：必须存在 `Audit Coverage Matrix`，且 14 面覆盖完整（代码入口 / 架构与模块 / 数据 / 真实数据库 / 契约与接口 / UI / 运行与部署 / 测试 / 依赖关系 / 历史 / 文档 SSOT / 安全与隐私 / 可观测性 / 合规与版权）、12 个基础面的细项证据逐项列出、真实数据库面有 PostgreSQL MCP / SQLite MCP 或等价 readback、文档 SSOT 面有深读证据、**Overall Confidence ≥ 80%**、**两个强证据面（真实数据库面 / 文档 SSOT 面）confidence 各自 ≥ 80%**（即使 Overall ≥ 80%，若任一强证据面 < 80% 即拒）、Blocking Unknowns = none；否则视为 Audit Debt，不得进入实现
    - **5b Seed / Greenfield 路径**（与 5a 互斥·仅在项目模式 ∈ {Seed / Init, Greenfield} 时走）：不得要求 audit.md，但 maturity-intake 必须包含 Baseline / Greenfield Survey、所有 N/A 的 evidence、Future Audit Trigger；缺失则视为 Maturity Intake Debt，不得进入实现
6. 上游需求已批准：`requirements.md`（与 `design.md`，若非 Medium）`Approval.Status = Approved`；若为 Medium 单文件模式，则校验 `spec.md` 具有 `Approval.Status = Approved` 即可
7. 目标 Task 的 `Status` ∈ `{Pending, In Progress}`
8. Task 的依赖前序已 `Done`（按任务事实源中任务顺序，或 tasks.md §2 Execution Order）
9. Task 的头部完整：`Implements / Design Refs / Touches / Existing Touches / Reuse Notes / Verification Commands / Context Required Before Execution`（Seed / Greenfield 可填 `N/A` 的字段除外）
10. **任务事实源（`tasks.md` 或 `spec.md`）的 `## Approval` · `Notes:` 中存在有效批准留痕**（二选一）：
    - **用户 Gate 批准型**：Notes 含 `>` Markdown 引用块 + 用户原话片段（含明示同意词，如「同意」/「go ahead」/「可以推进」）+ 时间戳；单词 / 表情 / 问句 / 「先这样后面再改」不计 Approved。
    - **AI-DRI auto-approved 型**：Notes **必同时含 4 行结构**：

    ```text
      AI-DRI auto-approved: no Pause-and-Ask trigger
      Gate Check: A=N/A, B=N/A, C=N/A
      Evidence: <已读 SSOT / audit / code anchors / constraints 摘要>
      Timestamp: <ISO 8601>

    ```

    - **伪留痕判定**：仅有状态字串（如 `Status: Approved`）而无任何 Notes / 仅 1 行 "AI-DRI auto-approved" 字串而缺 `Gate Check` / `Evidence` / `Timestamp` 三行 / 用户原话不含明示同意词 → 均视为伪造 Approved，必须停下推进并要求用户重新走 Decision Gate 完整批准（口头同意亦需补留原话引用块 / 4 行结构到 Notes）
11. **attention_budget_check（防 5 注意力稀释）**：估算本轮 Prompt 的 token 总量 = handoff-payload.yaml 体积 + tasks.md 本 Task 节 + `first_task.context_required.p0_essential` 所指各文件相关章节体积。两个阈值取自写端 §6.1 项目级槽位（默认值 / 项目层 Adapter 可在 `.github/skills/specs-write/SKILL.md` §6 覆盖）：
    - **P1 上限**：`attention_budget_p1_ceiling`（默认 200000 / 200k tokens）— 未超 → 可同时拉取 P1 Reference 作为辅助上下文
    - **P0-only 上限**：`attention_budget_p0_only_ceiling`（默认 300000 / 300k tokens）— 超 P1 上限但 ≤ P0-only 上限 → 本轮仅加载 P0 Essential，P1 在 Phase 2-7 按需拉取
    - 超 P0-only 上限 → 超载告警，告知用户"spec 本 Task 上下文过重，建议回 Phase 4 拆 Task"；仅读 payload + first_task 节推进，后续错点 / 幻觉风险由用户承担
    本检查项不为阻塞项，但超 P1 上限时必在 Intake 产出中明言「P0/P1 裁切状态」。项目层若使用不同 LLM context window（如 Claude 200k / GPT-4o 128k / Gemini 2M）须同步调整两个槽位；硬约束 `attention_budget_p0_only_ceiling > attention_budget_p1_ceiling`。

### 1.2 Phase 1 Locate 输出格式示例

```text

- 目标: TASK-007 — Add CSV size guard at upload router
- Status: Pending
- 依赖: TASK-001..TASK-006 全部 Done
- Spec: docs/specs/active/user-csv-import/ (Approved)
- Project Mode: Hybrid
- P0 Essential 待复述:
  - requirements.md#AC-007.2
  - design.md#DSN-API-007
  - charter.md#INV-LIM-002
- Touches / Existing Touches:
  - backend/upload_router.py
  - backend/tests/test_upload.py
- Verification:
  - pytest backend/tests/test_upload.py
  - schema drift check（不涉及，跳过）

前置检查通过；未命中 Pause-and-Ask，确认进入 Phase 2 复述。

```

---

## 2. Phase 2  Hydrate Context  Handoff Payload + Anchor Recovery

### 2.1 Handoff Payload 优先读取（如存在）

若 `<specs_root>/active/<feature-slug>/handoff-payload.yaml` 存在：

- **先读该 Payload 作为 Context 注入起点**：invariants 全文 · first_task 全量 · critical_contracts Failure Strategy · type_ssot · **traceability 全量追溯矩阵**（实际 schema 以 handoff-payload.yaml 本身有哪些节点为准）；这是高信噪比的“当前任务上下文 + 绝对禁区”摘要，有效抵抗长 spec Token 累积导致的注意力衰减
- **`traceability` 节是本 Task 【REQ/AC · DSN · EXIST · INV · BDD Scenario · Touches · Artifacts】六维关系的唯一机读 SSOT**（与写端 `cross-cutting.md §4.2` schema `traceability.tasks[]` **8 键**完全对齐：`id / implements / design_refs / derived_from_existing / anti_invariants / bdd_scenarios_owned / touches / artifacts`；其中 `touches` 为防 3 `revert_dependency_graph` 求交集输入源，**不投影到 Markdown 表格**仅留 YAML 供机读；其余 7 键投影到表格 7 列：Task / Implements / Design Refs / Existing / Anti-Invariants / BDD Scenarios Owned / Artifacts，`id` 通过 `Task` 列承载即 `Task` 列的值就是 `id`；Artifacts 列展示 `artifacts[]` 中 `kind=planner_output` 那条 path · 详写端 `appendix.md §A.1` 第 2 项投影规则），与 tasks.md 顶部 Markdown 表格冲突时以 YAML 为准（表格是投影）；如发现二者不一致 → 优先走项目层注入的脚本槽位 `traceability_regen_script`（默认值与命令字面以**写端 `project-adapter.md §1` 项目级槽位表为单点 SSOT**；项目层 Adapter 可在 `project-adapter.md §1` 覆盖）重生；重生后仍不一致 → 报告用户 + 在 Execution Notes 记录事实不一致，建议回切 `/specs-write`
- **P0 / P1 上下文分级读取（防 5）**：`first_task.context_required` 严格二分 `p0_essential` / `p1_reference`。本 Phase 必同时读两者加载到上下文。如 §1.1 attention_budget 触发「只加载 P0」或「仅 payload」档位 → 本节只读 P0 Essential（跨边界 Task / 动凭据 Task 上限 7 条，其他 5 条）；P1 在 Phase 3-7 按需拉取并在 Execution Notes 记录「补读 P1：`<file>`#`<id>` · reason: <为何需此备查>」。
- **P0 超上限 = spec 裁切不够细**：P0 节超上限（普通 Task 5 条 / 跨边界·动凭据 Task 7 条） → 停下报告用户，建议回 Phase 4 拆 Task；AI 不得「合并主题」或「选出 5 条老话」后推进
- **但 Payload 不代替源文件**：主 workflow §2.1 必读锚点仍须逐条打开源文件定位原文；Payload 只是索引加摘要，不是 SSOT
- **Payload 与源文件冲突时以源文件为准**，并在 Execution Notes 记录该冲突，提醒后续重生 Payload

若 Payload 不存在（早期 spec 未产出 / Medium 模式简化）→ 跳过本节，直接走主 workflow §2.1。

### 2.2 锚点失效处理

- 锚点 ID 在上游文件中找不到 → **停下**，提示用户该锚点已失效，建议回切 `/specs-write`
- 锚点章节为空或语义模糊 → **停下**，请求用户补充
- 锚点在 `Superseded` 版本里 → 切到当前版本，复述当前版本原文
- **`charter.md#SRC-*` 指向的 SSOT 外部章节定位不到**→ 停下，提示 SSOT 可能被修订，建议回切 `/specs-write` 刷新 Charter

-**`audit.md#EXIST-DSN-*` 的 Code Anchors 与当前代码不一致**（符号不存在 / 路径重名 / 表字段变更） → 停下，提示现状已漂移，建议回切 `/specs-write` 重跑 Audit

- **`audit.md#EXIST-DSN-*` 的 `Verified By:` 早于本次执行超过 7 天（且该表 / 接口 / UI / 产物在 Approved 后可能变动）**→**停下**，调用运行时工具（PG `information_schema` / SQLite `PRAGMA` / curl-httpx / Playwright snapshot / `Get-ChildItem`）重检一次现状。重检走 4 项格式（`tool` / `command` / `evidence_file` / `interpretation`）；原始输出追加到 `docs/specs/<feature-slug>/audit-evidence/<EXIST-id>.txt`，首行包含 4 桶分类 `[bucket=env_error|permission|not_found|actual_state]`（防 4 MCP 幻觉）。与原 `interpretation` 不一致 → 回切 `/specs-write` 重跑 Audit；一致 → 在 Execution Notes 记录本次重检时间戳 + 工具名 + evidence_file 起期以供下次查证

绝不脑补，绝不"按语义猜"。

### 2.3 Phase 2 复述格式示例

```text

### Context: requirements.md#AC-007.2

> WHEN 用户上传 CSV 文件超过 10MB THEN the 服务 SHALL 立即返回 413 错误并不消耗后端解析资源.

本 Task 在 upload router 入口处增加 size guard，并用 acceptance test 锁定 413 响应与不进入解析流程.

```

---

## 3. Phase 3  Plan  Touches Boundary, Verification Expansion, Pause-and-Ask

### 3.1 Touches 边界确认

- 列出本 Task 实际将动的文件，分为：
  - **新建**：对照 Task 的 `Touches`
  - **修改既有**：对照 Task 的 `Existing Touches`（Hybrid/Brownfield）
- **超出两者并集但属于本 Task 必需的执行级补齐**（测试文件、fixture、脚本参数、artifact 目录、import/helper 小修、同模块私有函数拆分）→ AI-DRI 自决追加，并在 Execution Notes 记录 `Touches auto-extension`、理由、追溯锚点。
- **超出两者并集且改变公共契约 / schema / API / UI 大版本 / 新外部依赖 / 跨 feature 范围** → 命中 Pause-and-Ask 或 Spec Breach，回切 `/specs-write` 把追加文件写进 Touches / Existing Touches、同时补 audit.md 中对应 EXIST-*。
- **修改既有代码但未在 audit.md 中反向标识** → 若是同 Task 私有实现级补齐，先在 Execution Notes 留 `EXIST gap` 并继续；若影响公共契约或复用边界，回切 `/specs-write` 补 EXIST-*。

### 3.2 Verification Commands 展开

- 把 `Verification Commands` 抽象项展开为可执行命令（`pytest <path>` / `npm test` / drift 脚本 / 手工步骤）
- 标注哪些是单元测试、集成测试、手工验证
- 缺命令 → 在 Plan 中先补上
- **DB Test Isolation 三要素核对**：凡 Verification Commands 含 DB 状态断言，必须复述 tasks.md `## 4. Test Plan` 节 DB Test Isolation 三要素原文——(a) 隔离机制 / (b) 副作用边界 / (c) 不再测后留垃圾——并与实际命令对照：若 spec 声明的隔离机制（如 transaction rollback）与实际命令（如直接 INSERT 不开事务 / 不 cleanup）不一致 → 停下，要求用户确认是修命令还是修 Spec；不触 DB 的 Task 跳过本项；详写端 `task-rules.md §1` + `templates/tasks.md §4`
- **跨边界任务项选检 Concurrency & Lock**：如 design.md 对应 DSN 填了 `Concurrency & Lock`，Verification 中需存在至少一项验证该场景的命令（并发压测 / 锁冲突复现 / 429 退避路径）或在 Execution Notes 说明为何本 Task 不是 Concurrency 验证点
- **DSN-DB “Replaces” 迁移一致性检验选检**：如 design.md 对应 `DSN-DB-*` 填了非 N/A 的 `Migration Strategy`，必须在 Plan 中明言该 Task 走哪一份一致性检验命令（strategy=shadow_write → 双写 diff；backward_compatible_stepwise → 本阶段子集验证；downgrade_script → down dry-run + 表行数不变）与哪一条业务可回 `Revert Command`；如此两项未在 tasks.md Verification Commands / Revert Command 中出现 → 停下追问是修命令还是修 Spec，不得静默通过
- **Artifacts 路径核对（条件化）**：如 tasks.md 该 Task 填了 `Artifacts:` 非 N/A，本 Phase Plan 必须核对 Verification Commands 中调用的脚本是否会把产物写到声明路径——逐一检查 CLI 是否传了 `--reports-dir` / `--output-dir` 等指向 `<feature-slug>/artifacts/` 的参数；若脚本默认输出到项目根 `reports/` 等通用目录而 CLI 未覆盖 → 在 Plan 中明示要补该参数，或回切 `/specs-write` 修 spec

### 3.3 Pause-and-Ask 白名单

仅承载**就地等用户批准**的场景；"改已批准合同"类一律走 `blocking-and-rollback.md §1.3` 回切 `/specs-write`。

以下 Task 在进入 Phase 4 前必须显式征求用户同意（**Irreversible Action 三类 + 调查置信度兜底 = 共 4 项**）：

- **Irreversible Action · 真实生产 DB / 外部状态**：真实生产 DB 写入 / DDL apply / backfill execute / 外部状态真实变更（写端 Gate 矩阵"Irreversible Action"）
- **Irreversible Action · 删除 / 破坏性**：删除数据 / drop 字段或表 / 删除公开 API endpoint / 破坏性不可自动回滚变更（同上）
- **Irreversible Action · 付费 / 对外发布**：真实第三方付费 API / 发送真实通知 / 对外发布 / 上线切流（同上）
- **L-DESIGN 高风险兜底**（写端 Gate B 衍生 · 设计级未决）：AI 充分调查后置信度仍 < 70%，且错误会造成跨模块返工或不可回滚代价（与写端 `templates/charter.md` 的 Opening Questions & Decisions 决策类型分级一致——L-DESIGN 才是设计级，L-IMPL 是实现级；本档位本质是设计级未决，不应套 L-IMPL 标签）

需走 `blocking-and-rollback.md §1.3` 回切（不在本节就地等批准）：改变已批准的需求、设计、技术红线、schema/API 契约或术语定义。

低风险任务（纯新增 / 局部修改 / 仅测试 / 加性验证脚手架 / artifact 生成 / 私有 helper 拆分）由你-DRI 直接进入 Phase 4，对应写端 Gate 矩阵"Anything else (L-IMPL / L-OPS)"。

---

## 4. Phase 4  Red  Constraint-Verification Tasks + TDD-Lock SHA-256

### 4.1 Constraint-Verification 型 Task 的特殊语义

符合 `Design Refs: N/A (constraint-verification)` 的 Task（如 grep / lint / drift / contract test 脚手架）不允许走主 workflow §4.2 例外跳 Red，但 Red 的语义需反转：

#### 4.1.1 Red 语义反转

- **传统 Task**：Red = 写一个期待某能力存在的测试，该能力未实现 → 测试失败
- **Constraint-Verification Task**：Red = 构造一份**故意违反约束的 fixture / 输入 / 代码状态**，运行验证脚手架 → 脚手架应“报警”。报警未出现 = Red 未达成，脚手架本身不生效。

#### 4.1.2 Green 语义

- 则是修正 fixture 为合规状态 / 补全全量脚手架覆盖范围 → 脚手架“不报警”
- 还需保留该 violation fixture 作为回归用例（重命名为 `*_should_fail.*` 或同价、由联合脚手架以 expected-fail 模式验证）

#### 4.1.3 Touches 位置与 Refactor

- Touches 通常仅落 `scripts/` / `tests/` / `.github/workflows/` / drift baseline；不得在业务代码主体发生变更
- 发现为了让验证脚手架运行必须动业务代码 → 停下回切 `/specs-write`，本 Task 可能被错分为 constraint-verification
- §6 Refactor 可跳过（本质上无业务重复可提炼）

#### 4.1.4 Verification 展开

除脚手架本身运行外，需额外记录：

- 脚手架在 violation fixture 上报警（expected-fail 路径）
- 脚手架本身在合规状态下静默（happy-path）
- CI 中脚手架已被接入（如 `.github/workflows/*.yml` / pre-commit hook / drift CI step）

### 4.2 Test Anchors SHA-256 指纹锁（防 2 TDD 作弊）

Red 测试全部完成并确认失败后，Phase 4 末必走：

1. **计算 hash**：对 tasks.md 本 Task `Test Anchors:` 列出的每个文件跑 `git hash-object <file>`（或 `pwsh -c "(Get-FileHash -Algorithm SHA256<file>).Hash.ToLower()"`）得到 SHA-256
2. **回填到两处**：
   - tasks.md 本 Task `Test Anchors:` 字段的每项 `sha256` 填入 64 位十六进制
   - handoff-payload.yaml `first_task.test_anchors` 同步补入
3. **显式声明**：在对话中输出一行「锁定声明」：

```text

   [TDD-Lock] Test files hashed and frozen.

- `<file1>`: `<sha256-1>`
- `<file2>`: `<sha256-2>`
   Proceeding to Phase 5 Implementation. Test files MUST NOT change in Phase 5.

```

   未输出该声明即进 Phase 5 者 → 视为违反防 2 防御，Phase 7 自检会拦住

1. **例外路径**：以下两种情况可跳过此锁定：
   - 仅纯文档 / 纯配置变更 / 项目无测试基础设施（主 workflow §4.2）Task，但需在 Execution Notes 明言 `Test Anchors: N/A (no test files)`。
   - **紧急热修复例外**：若任务标记为 `Emergency: true`（如 P0/P1 线上事故止血修复），可临时豁免此锁定以缩短止血用时，待事故完全止血并 Resolved 后，再补齐锁定。

---

## 5. Phase 5  Green  Boundary, Test-Freeze, Anti-Placeholder Rules

### 5.1 边界纪律

每行 diff 必须能追溯到：

- 某条 `REQ-### / AC-###.# / US-### / REQ-###.S<n>`，或
- 某条 `DSN-`<domain>`-###`，或
- 某条 `EXIST-*`（仅当该修改被 Task 的 Existing Touches 明示覆盖）或
- 某条 `INV-BAN-* / INV-LIM-*`（仅当该改动是为了遵守技术红线，如移除被禁用依赖的 import）

无法追溯的改动 → 视为越界，必须撤回或回切 `/specs-write` 增补 Spec。

另有两项硬规则：

- **不得重新定义或静默修改 SSOT 已定义的契约**（如状态机 / L1-L10 / 词表 / 权限模型 / Authoritative SSOT 章节）。如需修改这类契约 → 停下回切 `/specs-write` 或请求用户 Gate A/B 批准；执行端只能提交 `ssot_stewardship` 草案，不得直接改写母本 / L1 SSOT / .github/standards 权威章节。
- **不得违反 charter.md §5 Architectural Invariants**：实现侧不得引入 INV-BAN-*禁用依赖与部署形态，不得逾越 INV-LIM-* 边界；发现必须跨越 → 停下回切 `/specs-write` 修订 charter 重批 INV-* 红线，不得静默引入。

另有 artifact 落点硬约束（tasks.md 的 `Artifacts:` 字段是唯一声明源）：

- Task 执行期通过脚本生成的非源码副产物（reports / cost ledger / verify / quarantine）必须落到 tasks.md `Artifacts:` 声明的路径（默认 `docs/specs/<feature-slug>/artifacts/`）。
- 落在项目根 `reports/` / `tmp/` 等通用目录 → 视为违反 spec 边界，需在 Phase 7 Verify 前迁回正确路径，或回 `/specs-write` 把豁免在 spec 中明示。
- spec 仅约束本 spec 内部产生的产物；多 spec 共享的 ledger（如跨 feature 的 成本台账）需在各 spec 的 `Artifacts:` 中显式声明为共享例外，否则视为越界。

### 5.2 测试文件冻结令（防 2 TDD 作弊）

- **Phase 5 Green 严禁修改在 §4.2 [TDD-Lock] 中锁定的测试文件**。只动实现代码。意图开启 Red 上下文修补（如发现测试有 import 错 / fixture 拼错） → 退回 Phase 4 重走 §4.2，重新锁定后进 Phase 5；不得在 Phase 5 静默修测试（标记为 `Emergency: true` 的紧急热修复任务可临时豁免本限制）。
- **Phase 5 末必验 hash**：在主 workflow §5.1 测试通过后、进 §6 / §7 前，对 Test Anchors 所列文件重算 SHA-256 与 §4.2 锁定值比对，不一致 → 视为违反锁定令，不得进 Phase 6，仅能退回 Phase 4 / `blocking-and-rollback.md §1` 回切（标记为 `Emergency: true` 的紧急热修复任务可临时豁免此比对约束）。
- **发现 spec drift**（测试表达了与实际不符的期望） → 不得在本 Phase 改测试。走 Phase 8 Reflections 的 `kind: spec_drift` 选项上报 + `blocking-and-rollback.md §1.3` 回切。

### 5.3 完整输出硬约束（反偷懒拦截器）

本 Phase 以及 Phase 6 Refactor / Phase 8 Update 中产生的任何代码输出遵守：

- **绝对禁止出现以下截断 / 占位标记**：
  - JS / TS / Python / SQL 代码中的 `// ... existing code ...` / `/*...*/` / `# ... rest unchanged` / `# ... 不变 ...` / `# (省略)` / `pass  # TODO 填充`
  - 文件输出中出现 `<填入其他代码>` / `<原有内容保留>` / 任何 placeholder 未解析占位符
  - markdown / code block 中近似「中间代码同上」的所有变体
- **任何文件修改仅两种方式合法**：
  - 使用 `edit` / `multi_edit` 工具做精确字符串替换（优先，适用于可唯一锁定的 old_string）
  - 使用 `write_to_file` 输出完整文件结构（适用于新建文件或重构后全量覆写）
- **例外（仅限对话文本）**：Markdown 解释说明中为压缩上下文可使用 "..." 表达「省略中间部分」，但这种表达不得进入实际文件 / diff / 代码块

**检查点**：提交前运行 `git diff`，grep `// \.\.\.|# \.\.\.|<填入|<原有|rest unchanged|existing code` 均为空才可进入 Phase 7 Verify。

---

## 6. Phase 6  Refactor  Test Modification Exception

### 6.1 重构中修测试的例外（防 2 · 需同步重锁 hash + 留痕）

Refactor 阶段**允许**修测试（如提取 fixture / 重命名者 / 拆测试函数），但必同步：

1. 修改后重跑全量测试仍 Green
2. 重算 SHA-256 并同 PR 更新两处（tasks.md `Test Anchors` + handoff-payload `first_task.test_anchors`）
3. 在 tasks.md `Reflections:` 以 `kind: test_modified` 显式记录【before_sha256 / after_sha256 / reason】三项
4. 未同步重锁或未留痕 → §7 Verify 检查会视为作弊拦住

无明显坏味道时可跳过本 Phase。

---

## 7. Phase 7  Verify  DoD Triple-Loop and Conditional Gates

### 7.1 DoD 三闭环检查

对照 `tasks.md §5 Definition of Done`：

- **ATDD 闭环**：本 Task 涉及的 AC 是否有 Acceptance Test 验证路径
- **BDD 闭环**：本 Task 涉及的 US 是否有 BDD Scenario 覆盖
- **TDD 闭环**：本 Task 的 Verification Commands 单元测试是否通过
- **Secret-scan（条件化）**：如 `charter.md § 5. Architectural Invariants` 表中适用于本 Task 的 `INV-SEC-*` 非空，且本 Task 命中以下任一场景——（1）增/改 `.env*` / `config/*` / secrets 加载路径；（2）增/改与第三方 API 交互的客户端（含 SDK / Token / API Key 交换）；（3）调整日志 / 错误报告 / 遥测 / Trace 路径；（4）增/改凭据读取 / 轮转 逻辑——本 Phase 必须运行 tasks.md `Verification Commands` 中列出的 secret-scan 命令（写端 `task-rules.md §1` 已硬化此字段为条件化必填）并确认 0 告警；告警 → 不得进入 Phase 8，返回 Phase 5 清除凭据后重跑。tasks.md 未列出 secret-scan 命令但本 Task 命中场景 → 视为写端 `task-rules.md §1` 契约违规，回切 `blocking-and-rollback.md §1.3` `/specs-write` 补 secret-scan 命令后重启 Phase。豁免者在 tasks.md `Test Plan` + Execution Notes 双点明言理由与适用 INV-SEC-* 原文
- **Migration Strategy 一致性验证（条件化）**：如 design.md 对应 `DSN-DB-*` 的 `Migration Strategy` 非 N/A，本 Phase 必须运行该策略指定的一致性校验命令并记录 PASS：shadow_write → 双写 diff 脚本连续 N 小时 0 差异；backward_compatible_stepwise → 本步独立验证 + 上一步表/列仍可读；downgrade_script → down 脚本 dry-run + 表行数不变。任一项失败 → 不得进入 Phase 8，走 `blocking-and-rollback.md §1` 回切路径
- **Test Anchors hash 校验（防 2）**：对 tasks.md `Test Anchors:` 所列文件重算 SHA-256，与 §4.2 [TDD-Lock] 锁定值比对。不一致 且 `Reflections:` 中未以 `kind: test_modified` 显式声明前后 hash + 理由 → **视为作弊**，不得 Done，返回 Phase 4 重走 §4.2（**紧急热修复例外**：标记为 `Emergency: true` 的紧急热修复任务可临时豁免此比对校验，待事故完全止血并 Resolved 后重新锁定补齐）。允许路径：Phase 6 Refactor 改测试后同步重锁（§6.1）
- **失败契约 readback（防 5）**：凡本 Task 动了跨边界 DSN（涉 critical_contracts 节凡一条）者，Verify 阶段需逐字复述 critical_contracts[本 Task DSN] 的 failure_strategy 三类故障（timeout / crash / data_layer）原文，**并紧随以 `<file>:<line>` 错点指出实现中对应代码**：

```text

  [Failure Strategy Readback] DSN-API-001

- timeout (原文): 检测=>3s · 重试=客户端 3 次指数退避 · 最终态=HTTP 504 + 降级提示
    实现点: backend/clients/llm.py:142-168 (timeout=3s) + backend/routers/upload.py:88 (504 fallback)
- crash / data_layer: 同上逐条复述 + 错点

```

  做不到逐字复述 + 错点指代码 → 视为注意力已稀释，不得 PASS；冷路径 / 纯本地 Task 可豁免但需在 Execution Notes 明言「本 Task 不涉跨边界 DSN」

- **Artifacts 路径核验（条件化）**：如 tasks.md `Artifacts:` 非 N/A，本 Phase 必须 `Test-Path` 验证每条声明路径都已实际生成；同时核验:
  - 没有同名/类似产物散落到 `<feature-slug>/artifacts/` 之外（grep 项目根 `reports/` / `tmp/` / `output/`）。
  - 路径名包含 batch_id / timestamp 等可追溯标识。
  失败 → 不得进入 Phase 8，迁移到正确路径或回切 `/specs-write`。
- **跨端类型契约 drift check（条件化）**：如 handoff-payload.yaml `type_ssot` 节非空（即项目存在跨端通信 DSN），且本 Task 命中以下任一场景——（1）修改 `type_ssot` 节中任一 DSN 对应的单端权威源（如 `backend/schemas/*.py` / OpenAPI 定义 / Pydantic / dataclass 主体）；（2）修改对应 DSN 的 `generated_side`（如 `frontend/types/generated/*.ts` / 自动生成代码）；（3）修改 contract regen 脚本本身（`regen_command` 槽位指向的工具链）——本 Phase 必须运行该 DSN 声明的 `drift_check` 命令并确认 0 告警；告警 → 不得进入 Phase 8，返回 Phase 5 重跑 `regen_command` 同步两端类型后再 verify。tasks.md 未列出 drift_check 命令但本 Task 命中场景 → 视为写端 `design-rules.md §1` 跨端通信 DSN 硬规则违规（"严禁两端分别手写结构体"），回切 `blocking-and-rollback.md §1.3` `/specs-write` 补 drift_check 命令后重启 Phase。`type_ssot` 节为空（项目无跨端通信场景）→ 本项 N/A。
- 是否破坏回归测试 / drift 检查
