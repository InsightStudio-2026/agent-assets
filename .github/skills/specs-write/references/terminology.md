# Terminology · /specs-write 术语字典

> **本文是 `/specs-write` + `/specs-execute` 体系的术语字典**。每个术语给：一句话定义 + 现有锚点 + 必填字段 / 判定规则 + 与其他术语的关系 + 反模式（如有）。
> 概念抽象与命名压缩在 `methodology-kernel.md`；本文是它的字典化展开，**不重复 kernel 已给的事实**。

---

## 0. 定位与索引

### 0.1 适用范围

- 覆盖：spec 生命周期 9 层 / 4 种 Project Mode / 3 档复杂度 / 7 种 Delta Operation / 5 种 Relation / 5 类 Decision Gate / 12+11 种 workflow state / 7 种 reflection kind / 6 种 reflection resolution / 3 档抢占协议 / 防 1-5 / 三轨方法论 / 文件路径契约 / 反流路径。
- 不覆盖：模板字段细节（在 `templates/<file>.md`）、Phase 内部流程（在 `../protocols/orchestration.md` / `../../specs-execute/protocols/phase-rules.md`）、Decision Gate 防伪协议原文（在 `cross-cutting.md §2.3`）、handoff-payload schema（在 `cross-cutting.md §4.2`）。

### 0.2 引用规则

- 任一条目尾部带 `源：`<file>`#<section>` 指向真实事实源。
- 与 `methodology-kernel.md`、`cross-cutting.md`、`appendix.md`、`/specs-write.md`、`/specs-execute.md`、`templates/*` 字面零漂移。
- 本文修订必须同 PR 修订下游受影响文档；下游文档与本文出现术语漂移 → 视为本文失效，必须先修本文再修下游。

### 0.3 章节索引

| § | 类别 | 核心术语数 |
| --- | ------ | ------------ |
| §1 | Spec 生命周期九层语义层 | 9 |
| §2 | Project Mode 与 Audit Profile | 4 + 3 |
| §3 | 复杂度 Mode | 3 |
| §4 | ID 锚点系统 | 10+ |
| §5 | Delta Operation | 7 |
| §6 | Relation to Existing | 5 |
| §7 | Decision Gate / Pause-and-Ask | 5 + 4 + 4 决策类型 |
| §8 | Approval.Status / Task Status | 5 + 5 |
| §9 | Workflow State | 12 + 11 |
| §10 | Reflection（kind / resolution / severity） | 7 + 6 + 3 |
| §11 | 抢占协议 | 3 + 三件套 |
| §12 | 防御机制（防 1-5） | 5 |
| §13 | 三轨方法论 / TDD-Lock / Test Anchors | 3 + 关键字段 |
| §14 | 文件路径 / 目录契约 | 10+ |
| §15 | 反流路径与权威 SSOT | 6 |

---

## 1. Spec 生命周期九层语义层（L0-L8）

> 完整生命周期定义与文件承载见 `methodology-kernel.md §1`。本节补充每层的判定规则、必填字段、与上下层关系。

### L0 · Maturity & SSOT Health

- **定义**：判定项目处于什么成熟度（Seed / Greenfield / Hybrid / Brownfield）+ 母本 / L1 SSOT 是否健康可派生。
- **承载**：`<feature-slug>/maturity-intake.md`。
- **必填**：`Project Maturity` / `Audit Profile` / `SSOT Health` / `Confidence` / `Decision` / `Blocking Issues` / `SSOT Stewardship Suggestions`（详 `templates/maturity-intake.md`）。
- **决策枚举**：`PROCEED_TO_CHARTER` / `PAUSE_FOR_GATE_A` / `BLOCKED_SSOT_REPAIR` / `BLOCKED_UNFIT_SOURCE`。
- **与上下层关系**：L0 是其他层的前置；`PROCEED_TO_CHARTER` 才能进 L1；其余三态阻塞或回切上游。
- **源**：`/specs-write.md §2.0` + `templates/maturity-intake.md`。

### L1 · Charter / Proposal

- **定义**：把模糊问题压成可审查的「工程合宪」；给出做什么 / 不做什么 / 谁授权 / 红线在哪。
- **承载**：`<feature-slug>/charter.md`。
- **必填**：`Sources`（含 SRC-### + timestamp）/ `Open Questions`（≤ 5 条开工必答）/ `Complexity` / `Out of Charter` / `Derivation Constraints` / `## 5. Architectural Invariants`（含 INV-BAN-*/ INV-LIM-* / INV-SEC-*）/ 决策类型区分（L-STRAT / L-DESIGN / L-IMPL / L-OPS）。
- **轻量化**：`Approval.Status: Acknowledged`，不走完整 Decision Gate。
- **源**：`/specs-write.md §2.1` + `templates/charter.md` + `cross-cutting.md §5`。

### L2 · Current-state Audit（仅 Hybrid / Brownfield）

- **定义**：把「本 feature 影响面里既有什么」摸清楚；反向标识 EXIST-*；决定 Reuse / Extend / Replace / Deprecate。
- **承载**：`<feature-slug>/audit.md` + `<feature-slug>/audit-evidence/`（4 桶 DB / API / UI / FS 真实校验工具产出）。
- **必填**：feature-scoped 14 面审计（五阶全景）+ Conflict 解决方向 + DB/API/UI/FS 类 EXIST 必填 `Verified By:` 4 项 + `## 11. Audit Refresh Log`。
- **必过**：**Audit Depth Gate 双层门**= 14 面覆盖 + 真实数据库面 / 文档 SSOT 面不可 N/A + Overall Confidence ≥ 80% + 两强证据面各 ≥ 80% + Unknowns 清零。

-**跳过**：Seed / Greenfield 跳本层（但不跳 Baseline / Greenfield Survey 与 SSOT Health Check）。

- **源**：`/specs-write.md §2.2` + `templates/audit.md` + `appendix.md §A.4`。

### L3 · Behavior Spec / Delta Requirements

- **定义**：系统的外部可观察行为是什么；相对既有行为做哪种 Delta Operation。包含 functional REQ + non-functional NFR 双轨。
- **承载**：`<feature-slug>/requirements.md`（§1-§9 functional + §10 NFR-* 6 类槽位）。
- **functional 必填**：每条 REQ ≥ 1 EARS AC + ≥ 1 BDD Scenario / EARS-BDD 互查无孤立 / 至少关联一个 US / AC 主语为系统-模块-服务-存储且可观察可验证可写测试 / **禁用模糊词**/ 必填 `Derived From` + `Relation to Existing` / Hybrid / Brownfield 必写 `## 5. Existing Coverage` + `## 8. Derivation Map`。

-**non-functional 必填**：§10.0 High-Risk Assessment 表必填（6 类 Risk Trigger 各标 High / Low）；任一类 High → 该类必有 ≥ 1 条 `Status: Active` NFR；Low 类必显式 `N/A: <理由>`，不允许留空；每条 Active NFR 必有 `Verification` + `Routed to` 字段；Brownfield 每条 NFR 必有 `Delta Operation` 字段。

- **源**：`/specs-write.md §2.3` + `templates/requirements.md` + `cross-cutting.md §3` + `methodology-kernel.md §1.1`。

### L4 · Technical Plan / Design

- **定义**：跨边界契约、失败策略、并发锁、迁移路径设计；设计是契约不是实现。
- **承载**：`<feature-slug>/design.md`。
- **必填**：稳定 DSN-`<domain>`-### / 追溯到 REQ / Reuse vs New 摘要 / `## 2. Architectural Invariants Inheritance` 表（复述 charter §5 INV-* 与本设计绑定）/ 跨边界 Failure Strategy / 并发锁 / Alternatives / DB migration 安全网。
- **跳过**：Medium ① 跳本层，标 `Mode: Medium (design skipped:`<reason>`)`。
- **源**：`/specs-write.md §2.4` + `templates/design.md` + `../protocols/design-rules.md` + `cross-cutting.md §5`。

### L5 · Tasks / DAG / Handoff

- **定义**：把设计转译成单 Task 可独立完成的 Red→Green→Refactor 队列 + 机读消费契约。
- **承载**：`<feature-slug>/tasks.md` + `<feature-slug>/handoff-payload.yaml`。
- **必填**（tasks.md）：每 Task ≤ 1 day / 可测试 / 可回滚 / 头部七字段齐全 / BDD 单一所有权 / Test Anchors / Revert Command / Context Required（P0 / P1 严格二分）/ Anti-Invariants / DoD / Verification Commands / Artifacts / Existing Touches / `Relation to Existing`。
- **必填**（handoff-payload.yaml）：`schema_version: 0.6` / `feature_slug` / `mode` / `project_mode` / `audit_profile` / `invariants`（复述 charter §5 全文）/ `traceability`（机读 SSOT）/ `first_task` 全量复制 / `critical_contracts`（全 Task 跨边界 DSN）/ `implementation_reflections`（≤ 10 条）。
- **源**：`/specs-write.md §2.5-2.6` + `templates/tasks.md` + `../protocols/task-rules.md` + `cross-cutting.md §4`。

### L6 · Execution / Verification

- **定义**：实际跑 Red → Green → Refactor → Verify，留命令输出与 artifacts。
- **承载**：`/specs-execute` Phase 1-7 + `<feature-slug>/artifacts/` 副产物。
- **必填**：每 Phase MUST read 对应 `../specs-execute/<file>` + 强制复述 Context Required 锚点原文 + TDD-Lock（Phase 4 末 SHA-256）+ Verification Commands 全 PASS + DoD 三闭环（ATDD / BDD / TDD）+ 条件化检查门（Secret-scan / Migration / Test Anchors / Failure readback / Artifacts / type drift / regression）。
- **源**：`/specs-execute.md` 全文。

### L7 · Reflection / Reflux

- **定义**：执行期发现的实现选择 / 候选 INV / 复用模式 / spec drift / audit debt / SSOT 改进建议如何回流。
- **承载**：热数据 `handoff-payload.yaml#implementation_reflections.active`（≤ 10 条）+ 冷数据 `<feature-slug>/reflections-archive.md`（append-only）。
- **必填**：每条 reflection 含 `id` / `task_id` / `kind` / `severity` / `summary` / `suggested_target` / `raised_at` / `raw_path:<feature-slug>/reflections/REF-###.md`。
- **源**：`appendix.md §A.7`。

### L8 · Archive / Merge Back

- **定义**：交付后哪些进 feature 内归档（不反流全局）；哪些回并到 charter / standards / 母本 / SSOT（影响后续 feature）。
- **承载**：active → done `git mv` + INV-* 上升（charter §5）+ standards 蒸馏（.github/instructions/）+ folded_into_ssot / promoted_to_ssot_patch（母本）。
- **三条件齐**（active → done）：详 `methodology-kernel.md §5`。
- **反流 5 种 resolution**：详 `methodology-kernel.md §6.2`。
- **源**：`appendix.md §A.7.4` + `methodology-kernel.md §5-6`。

---

## 2. Project Mode 与 Audit Profile

> 判定权威源 = `templates/maturity-intake.md` 第 5 行起。

### 2.1 Project Mode（4 模式）

| 模式 | 判定关键词 | Audit Profile | Phase 1.5 |
| ------ | ------------ | ---------------- | ----------- |
| **Seed / Init** | 仓库 / spec / 代码 / DB / 测试 / 归档基本为空，且当前任务是建立项目骨架 / 初始 SSOT / 第一批基础设施 | Baseline Survey | 跳 |
| **Greenfield** | 与既有系统物理隔离，但项目已有 README / .github/standards / CI / 测试约束 / 技术红线 / 母本 SSOT；**不是「无现状」** | Greenfield Survey | 跳 |
| **Hybrid** | 本 spec 涉及领域内存在 ≥ 1 个既有模块 / 表 / 接口 / 路由 / UI 入口，同时有明显新建部分 | Feature-Scoped Full-Surface Audit | **必走** |
| **Brownfield** | 本 spec 主要修改 / 替换 / 扩展既有模块、表、接口、数据流或历史行为 | Feature-Scoped Full-Surface Audit | **必走** |

-**判定证据要求**：仓库骨架 / 源代码 / DB schema / 测试 / docs SSOT / Project Archives / 历史 commit / 部署脚本，**最少六维信号**才能下 `Seed / Init` 或 `Greenfield` 判断；任一维存在真实负载 → 升级到 `Hybrid` / `Brownfield`。

- **机读 / 人读字段**：`handoff-payload.yaml` 中 `project_mode: Seed | Greenfield | Hybrid | Brownfield`（机读单值）+ `project_mode_label: "Seed / Init" | ...`（人读别名，保留 "Seed / Init" 复合标签作历史兼容）。
- **反模式**：把项目当 Greenfield 跳 Phase 1.5 直接写 requirements / 用「当前为空」替代证据 / 没有六维信号就下 Seed 判断。
- **源**：`templates/maturity-intake.md` + `cross-cutting.md §4.2`。

### 2.2 Audit Profile（3 种）

| Profile | 何时使用 | 必产 |
| --------- | ---------- | ------ |
| **Baseline Survey** | Seed / Init 模式 | `maturity-intake.md §2` Baseline 表 + 每个 N/A 配 Future Audit Trigger |
| **Greenfield Survey** | Greenfield 模式 | `maturity-intake.md §2` Greenfield 表 + 基础设施 / SSOT / 测试 / CI / 数据策略槽位审计 |
| **Feature-Scoped Full-Surface Audit** | Hybrid / Brownfield 模式 | `audit.md` 14 面审计（五阶全景）+ EXIST-* 反向锚点 + audit-evidence/ 4 桶 + 必过 Audit Depth Gate 双层门 |

- **N/A 必证据化**：任何 N/A 必给 evidence + Future Audit Trigger，不得用「当前为空」替代证据。
- **源**：`templates/maturity-intake.md` + `appendix.md §A.4`。

### 2.3 Audit Depth Gate（双层门）

- **定义**：Phase 1.5 audit.md 必过的硬门，不过 → 阻塞下游。
- **第一层**：本 feature 影响面内 14 面覆盖 + 真实数据库面 / 文档 SSOT 面不可 N/A。
- **第二层**：Overall Confidence ≥ 80% + 两强证据面各 ≥ 80% + Blocking Unknowns 清零。
- **强证据 2 面**：真实数据库面 + 文档 SSOT 面（其余 9 面是基础证据面）。
- **源**：`/specs-write.md §2.2` + `appendix.md §A.4`。

---

## 3. 复杂度 Mode（3 档 + 文件裁剪规则）

| Mode | 标记 | 文件形态 | 适用 |
| ------ | ------ | ---------- | ------ |
| **Small** | — | 不启用 workflow | 错字 / 单文件 bug / 用户已给完整代码级指令 / 纯查询 / 解释 / 阅读代码 |
| **Medium ①** | `Mode: Medium (design skipped:`<reason>`)` | `requirements.md` + `tasks.md`（跳 design） | 设计无替代 / 不涉 schema / API 外部消费者 |
| **Medium ②** | `Mode: Medium (single-file:`<reason>`)` | 单文件 `spec.md`（内部仍保留 Requirements / Design / Tasks 三段 + Gate 判定） | 单人小特性 / 设计无替代 / 不涉 schema / API 外部消费者 |
| **Large** | `Mode: Large` | 完整三件套 `requirements.md` + `design.md` + `tasks.md`（必要时含 audit.md） | 新功能 / 跨模块重构 / 架构边界变动 / Schema / API / 协议 / 事件契约变更 / 权限 / 计费 / 合规 / 数据治理 / AI/LLM pipeline / Agent / 长链路任务 / 复杂 Bug |

-**硬规则**：文件可裁，**§1 九层语义不可裁**。即使 Medium 单文件，L1 / L3 / L4 / L5 段必须存在；缺段视为越界，回退 Large。

- **`reason` 必填**：Medium ① / ② 头部 `Mode:` 字段中 reason 不得丢；handoff-payload.yaml `mode` 字段同步。
- **源**：`/specs-write.md §1.5` + `templates/*` 头部。

---

## 4. ID 锚点系统

> 完整 ID 格式表与子域枚举见 `cross-cutting.md §1.1-1.2`。本节补充每个 ID 的范围与跨文件定位规则。

### 4.1 ID 类型表

| ID | 格式 | 范围 | 一旦分配 |
| ---- | ------ | ------ | ---------- |
| **SRC** | `SRC-###` | maturity-intake / charter Sources 节 | 不变 |
| **US** | `US-###` | requirements §3 User Stories | 不变 |
| **REQ** | `REQ-###` | requirements §6 Requirements | 不变 |
| **AC** | `AC-###.#` | requirements EARS Acceptance Criteria（`###` 跟随 REQ） | `###` 跟随 REQ |
| **DSN-`<domain>`-###** | `DSN-`<domain>`-###` | design DSN 章节（domain 8 主流：`ARCH/DB/API/UI/SEC/OBS/DATA/LLM`；不主流 6：`MIG/INFRA/INT/FS/FLOW/CONFIG/CACHE`；兜底 1：`OTHER`） | 不变 |
| **EXIST-`<type>`-###** | `EXIST-REQ-* / EXIST-DSN-`<domain>`-* / EXIST-INV-*` | audit.md 反向标识既有事实 | 不变 |
| **TASK** | `TASK-###` | tasks.md 任务编号（顺序 ≥ 依赖拓扑） | 不变（Done 后保留） |
| **INV-BAN** | `INV-BAN-###` | charter §5 禁用红线（不引入新外部依赖 / 不调真实数据库 / etc.） | 不变 |
| **INV-LIM** | `INV-LIM-###` | charter §5 限度红线（性能上限 / 时间窗口 / 并发上限 / etc.） | 不变 |
| **INV-SEC** | `INV-SEC-###` | charter §5 安全红线（凭据 / API Key / PII / 跨网域 / 交易 / 合规） | 不变 |
| **NFR-SEC** | `NFR-SEC-###` | requirements §10.1 Security NFR（authz / PII / secrets / audit / encryption / input-validation / supply-chain） | 不变 |
| **NFR-PERF** | `NFR-PERF-###` | requirements §10.2 Performance Budget（latency / memory / bundle / cold-start / API-throughput / DB-query） | 不变 |
| **NFR-OBS** | `NFR-OBS-###` | requirements §10.3 Observability（log / metric / trace / alert / dashboard / runbook） | 不变 |
| **NFR-REL** | `NFR-REL-###` | requirements §10.4 Release Constraints（feature flag / migration / rollback / canary / blue-green） | 不变 |
| **NFR-UX** | `NFR-UX-###` | requirements §10.5 UX / A11y（keyboard / screen-reader / contrast / focus / aria / responsive / errors / loading / i18n） | 不变 |
| **NFR-PLAT** | `NFR-PLAT-###` | requirements §10.6 Platform Constraints（OS / browser / device / network） | 不变 |

### 4.2 跨文件定位规则（cross-cutting §1.3）

- spec 文件之间引用：`<file>#<id>` 或 `<file>#<heading-anchor>`（**不允许行号**）。
- 引用代码：`<file path>::<symbol>` 或 `<file path>::`<class>`::<method>`，或 git 永久 SHA。
- 引用既有 spec：`docs/specs/<feature-slug>/<file>.md#<id>`。
- 归档版本快照：`docs/Archives/specs/<file>.snapshot.`<YYYY-MM-DD>`.md`，**不参与活跃锚点**。
- **行号禁令**：除归档快照外，禁用行号引用（spec 编辑会导致行号漂移）。

### 4.3 BDD Scenario 锚点

- 格式：`REQ-###.S<n>`（如 `REQ-001.S1`）。
- 落点：`requirements.md §7 BDD Scenarios` 标题写 `Scenario:` + tasks.md `Test Anchors` 引用。
- **单一所有权**：每个 BDD Scenario 由唯一 Task `Test Anchors` 拥有；多 Task 共享所有权 → 防 2 检测违规。
- **源**：`cross-cutting.md §3.2` + `appendix.md §A.2`。

---

## 5. Delta Operation（7 种）

> 完整 7 种语义与现有锚点映射表见 `methodology-kernel.md §4`。本节补充每种 delta 的判定示例 + 反模式。

### 5.1 Add

- **判定示例**：新功能 / 新模块 / 新 API endpoint / 新 schema 表 / 新 UI 入口 / 全新业务流程，**且**SSOT 与既有现状均未覆盖。

-**必填**：`Justification`（为何 SSOT 与现状均未覆盖；写作端要主动证否而不是默认 Add）。

- **反模式**：未做 Phase 1.5 audit 就标 `Net New` / 未在 SSOT Health Check 中证否就标 `Net New`。
- **锚点**：`Relation to Existing: Net New`。

### 5.2 Modify

- **判定示例**：在现有 EXIST-* 基础上叠加字段 / 增加分支 / 拓展边界，但保留原有契约的可观察行为。
- **必填**：EXIST-* 锚点 + `Derived From` SRC + 不破坏原有 AC 的证明。
- **反模式**：实际是 Replace（破坏原契约）但标 Modify / EXIST 锚点失效（`Verified By:` 超 7 天）未 refresh。
- **锚点**：`Relation to Existing: Extends EXIST-*`。

### 5.3 Replace

- **判定示例**：替换既有实现 / 替换既有 schema / 替换既有 API endpoint / 替换既有数据流，导致原契约可观察行为变化。
- **必填**：EXIST-* 锚点 + 迁移路径（Migration Plan / Failure Strategy）+ Schema migration 安全网。
- **反模式**：缺 Migration Plan 直接 Replace / 没有提供回滚路径 / 跨边界 DSN 缺 Failure Strategy。
- **锚点**：`Relation to Existing: Replaces EXIST-*`。

### 5.4 Deprecate（组合表达 · 现有体系无单锚点语法）

- **判定示例**：弃用某既有能力 / EXIST-* 但本 feature 不立即替换；或宣告兼容窗口结束后清理。
- **必填**（三处组合）：
  1. `charter.md §6. Out of Charter` 显式登记弃用范围；
  2. 新 spec 中以 `Replaces EXIST-*` 路径表达替换关系（即使本 feature 不实施替换）；
  3. `audit.md ## 11. Audit Refresh Log` 追加 deprecate 行（含 owner / 删除条件 / 验证方式 / 清理 task）。
- **现状缺口**：现有体系无单条 EXIST-* 锚点的弃用标记语法；kernel 如实记录此缺口，不在 kernel / terminology 范围内修复。
- **反模式**：只在 charter §6 写 deprecate 但未补 Audit Refresh Log / 缺兼容窗口与清理 task。
- **锚点**：组合 `charter §6` + `Replaces EXIST-*` + `audit.md ## 11`。

### 5.5 Preserve

- **判定示例**：依赖既有 EXIST-* 不动；本 feature 通过既有契约消费但不修改。
- **必填**：EXIST-* 锚点 + 不动理由（如 EXIST 是稳定 SSOT / 修改影响超出本 feature scope）。
- **反模式**：实际是 Modify（改了内部实现）却标 Preserve / 未明示「为何不动」。
- **锚点**：`Relation to Existing: Depends EXIST-*`。

### 5.6 Merge Back（5 种 resolution）

- **判定示例**：实现期发现可升入项目级 SSOT 的稳定模式 / 候选 INV / 复用模式 / SSOT 健康改进。
- **必填**：reflection ID + `kind` + `resolution` + `target`（真实落点）+ 用户批准（仅 `folded_into_ssot` / `promoted_to_ssot_patch` 必需）。
- **5 种 resolution**：详 §10.2 + `methodology-kernel.md §6.2`。
- **反模式**：直接修母本 / charter §5 INV-* / .github/standards 而无用户批准 / 改 YAML 状态位但不删节点 / 同 reflection-id 在 YAML 与 archive 重复存在。
- **锚点**：`Reflection.resolution`。

### 5.7 Archive Only

- **判定示例**：feature 交付完成，反思条目无需升入项目级 SSOT，作为 feature 内部「实现旁注备忘」归档。
- **必填**（active → done 三条件齐）：详 `methodology-kernel.md §5`。
- **反模式**：三条件未齐就 `git mv` / 项目根 reports/tmp/output 散落产物未清理。
- **锚点**：active → done `git mv` + `<feature-slug>/reflections-archive.md` append-only。

### 5.8 未决前置态（不是独立 delta）

- **`Conflicts EXIST-*`**：与既有冲突待解。**必给解决方向**，不得只罗列矛盾；解决后落到 §5.1-5.4 之一。
- **源**：`cross-cutting.md §1.4 A`。

---

## 6. Relation to Existing（5 种）

> 5 种枚举与判定表详 `cross-cutting.md §1.4 A`。本节补充各字段的使用范围 + 与 Delta Operation 的映射。

| 关系 | 含义 | 使用范围 | 映射 Delta |
| ------ | ------ | ---------- | ------------ |
| `Net New` | 既无 SSOT 也无现状承接 | REQ / DSN / TASK | Add |
| `Extends EXIST-*` | 在既有基础上叠加 | REQ / DSN / TASK | Modify |
| `Replaces EXIST-*` | 替换既有 | REQ / DSN / TASK | Replace（含 Deprecate 组合的一部分） |
| `Conflicts EXIST-*` | 与既有冲突待解 | REQ / DSN / TASK | 未决前置态 → 解决后落到 Add / Modify / Replace / Deprecate |
| `Depends EXIST-*` | 依赖既有不动 | REQ / DSN / TASK | Preserve |

- **`Net New` 必附 `Justification`**：为何 SSOT 与现状均未覆盖。
- **Greenfield 模式**：可统一填 `Net New`（但仍需 SSOT Health Check 证否）。
- **Hybrid / Brownfield 模式**：每条 REQ / DSN / TASK 必填，缺一视为越界。
- **源**：`cross-cutting.md §1.4 A`。

---

## 7. Decision Gate / Pause-and-Ask / 决策类型

### 7.1 Decision Gate（5 类）

> 完整白名单详 `cross-cutting.md §2.2`。本节补充每类的判定标准 + 留痕要求。

| Gate | 触发场景 | 决策权 | 留痕 |
| ------ | ---------- | -------- | ------ |
| **Gate A · L-STRAT 战略级** | 产品方向 / 商业模型 / 合规红线 / 资源投入 / Charter 红线变更 / 重大 SSOT 修订 | **必停问用户** | `Approval.Notes:` 引用块复制用户原话 + 时间戳（详 cross-cutting §2.3） |
| **Gate B · L-DESIGN 设计级** | 新 feature 架构 / Schema 结构 / API 契约 / 新引入依赖 / UI 大版本 / 跨系统集成 | **必停问用户** | 同上 |
| **Gate C · Spec Breach** | 当前阶段产出违反上游 SSOT / charter §5 INV-* / 已 Approved 的 spec | **必停问用户** | 同上 |
| **Irreversible Action** | 写真实数据库 / 推送远端 / 改 CI / 改 IAM / 调用付费 API / 涉资金流接口 | **必停问用户** | 同上 |
| **Anything else (L-IMPL / L-OPS)** | 实现细节 / 内部重构 / migration 文件名 / 测试写法 / 库 API 用法 | **AI-DRI 自决** | `Notes:` 写入 `AI-DRI auto-approved` 留痕 |

-**Gate B 衍生 · Existing Touches 扩展回流**：执行端某 Task 自动追加 ≥ 2 个公共契约相关文件至 `Existing Touches`，触发 `kind: audit_debt + extension_payload` 反流（详 `appendix.md §A.7.5`）。

- **留痕要求**：必须出现明示同意词；用户复述他人意见、emoji（"👍"）、笑脸或问句**不视作批准**；用户继续讨论 / 修订意见亦**不视作批准**。
- **源**：`cross-cutting.md §2.2-2.3`。

### 7.2 决策类型（4 种）

| 类型 | 含义 | 处理 |
| ------ | ------ | ------ |
| **L-STRAT** | 战略级（产品方向 / 商业 / 合规 / 资源） | 触发 Gate A |
| **L-DESIGN** | 设计级（架构 / Schema / API / 依赖 / UI / 集成） | 触发 Gate B |
| **L-IMPL** | 实现级（实现细节 / 内部重构 / 测试写法） | AI-DRI 自决 + 简报留痕 |
| **L-OPS** | 运维级（migration 文件名 / 库 API 用法 / 临时工具选择） | AI-DRI 自决 + 简报留痕 |

-**charter 必区分**：每条 Open Question 必标 L-STRAT / L-DESIGN / L-IMPL / L-OPS，决定是否需 Gate 批准。

- **反模式**：把 L-IMPL 决策上交用户问「要不要」反复倒灌 → 违反缺省立法（AI-DRI 是缺省 DRI）。
- **源**：`/specs-write.md §0.1` + `cross-cutting.md §2`。

### 7.3 Pause-and-Ask（4 项白名单）

- **定义**：执行端 Phase 3 Plan 中识别出的「必须停下问用户」场景，不命中则 AI-DRI 直进 Phase 4。
- **4 项**：
  1. **生产 DB 写入**/ 删除 / schema 变更
  2.**删除破坏**/ 不可逆删除文件 / 删除生产分支
  3.**付费对外发布**/ 调用付费 API / 推送付费集群
  4.**L-DESIGN 高风险兜底** / 设计级反复未达共识 / 设计触及 INV-* 边界
- **低风险豁免**：纯新增 / 仅测试 / 加性脚手架 / artifact / 私有 helper → AI-DRI 直进 Phase 4。
- **状态**：命中 → `/specs-execute:PAUSE_AND_ASK_PENDING` → 等用户裁决。
- **源**：`/specs-execute.md §3.2` + `/specs-execute.md §0.2.1`。

---

## 8. Approval.Status / Task Status

### 8.1 Approval.Status（spec 文件 5 种 · cross-cutting §2.1）

| Status | 含义 | 下一步 | AI 是否可自决 |
| -------- | ------ | -------- | ---------------- |
| `Draft` | 写完待批 | 进入 Gate 判定 | — |
| `Approved` | 用户批准（命中 Gate）或 AI-DRI 自动批准（未命中 Gate） | 进入下一 Phase | Gate N/A 时可 |
| `Needs Changes` | 命中 Gate 且用户要求修订 | 修订后重提 Gate | ❌ |
| `Acknowledged` | charter 专用（轻量，不走独立批准） | 进入 Phase 1.5 / Phase 2 | — |
| `Superseded` | 被新版本替代 | 保留作历史 | ❌ |

- **AI-DRI 自决规则**：在 Gate N/A 时可自行将状态从 `Draft` / `Needs Changes` 改为 `Approved`，必在 `Notes` 留 `AI-DRI auto-approved` 痕迹。
- **命中 Gate A/B/C / Spec Breach / Irreversible 时**：AI 不得自决，必须等用户白名单批准。
- **反模式**：Gate 命中时 AI 自标 `Approved` / Gate N/A 时未在 Notes 写入 `AI-DRI auto-approved` 留痕（视为伪 Approved）。
- **源**：`cross-cutting.md §2.1` + `cross-cutting.md §2.3`。

### 8.2 Task Status（5 种 · templates/tasks.md）

| Status | 含义 | 进入条件 | 退出条件 |
| -------- | ------ | ---------- | ---------- |
| `Pending` | 待执行 | 任务定义完成 | Phase 1 Locate 选中 → `In Progress` |
| `In Progress` | 执行中 | Phase 1 Locate 通过 | 全 Verification PASS + 无 Pause-and-Ask 未决 → `Done`；阻塞 → `Blocked`；抢占 → `Blocked(Suspended)` |
| `Done` | 完成 | Verification / DoD 全 PASS 且无 Pause-and-Ask 未决 | 不变（除非新发现导致 Reopen） |
| `Blocked` | 阻塞 | 上游锚点失效 / Touches 越界 / 测试环境 / 真实 DB 不可达 | 阻塞解除 → 回 `In Progress` |
| `Blocked(Suspended)` | 抢占冻结 | P-SIBLING / P-CROSS 触发 + suspended_state 现场保护三件套写入 | Resume 三件套完成 → 回 `In Progress`；同步删除 `suspended_state` 节 |

- **Done 唯一门槛**：Verification / DoD 全 PASS 且无 Pause-and-Ask 未决；AI **不得**在未全 PASS 时自行标 `Done`。
- **反模式**：未全 PASS 标 Done / Resume 后未删 `suspended_state` 节（视为执行端 Resume 漏删）。
- **源**：`/specs-execute.md §0.2.1` + `cross-cutting.md §2.1` + `appendix.md §A.6`。

---

## 9. Workflow State

### 9.1 /specs-write State（12 种 · §0.2.1）

| 状态 (State) | 进入条件 | 退出 / 路由 | 路由动作 (Route Action) |
| ------- | ---------- | -------------- | --------------- |
| `NO_HEALTHY_SSOT` | Phase 0 SSOT Health = `Needs Repair` / `Unfit As Source` | 阻塞下游 / 分流上游 | `REPORT_AND_STOP` |
| `CHARTER_READY` | Phase 1 charter 写完 + Acknowledged | 进 Phase 1.5 / 2 | `CONTINUE_IN_WORKFLOW` |
| `AUDIT_REQUIRED` | Hybrid / Brownfield 必走 Phase 1.5 | 进 Phase 1.5 | `CONTINUE_IN_WORKFLOW` |
| `EXTERNAL_AUDIT_REQUIRED` | Phase 1.5 / Phase X 发现超本 feature 范围的架构 / 缺陷 / 商业 / SSOT 修复问题 | 分流外部审计 workflow（详 §0.2.1 表 `/specs-write.md`） | `REPORT_AND_STOP` |
| `APPROVAL_PENDING` | 当前 Phase 命中 Gate A/B/C / Irreversible | 等用户白名单批准 | `WAIT_FOR_USER` |
| `CURRENT_GATE_APPROVED` | 当前 Phase Gate 通过（不等于整 spec 可执行） | 进下一 Phase | `CONTINUE_IN_WORKFLOW` |
| `REQUIREMENTS_READY` | Phase 2 requirements 写完 | 进 Phase 3 / 4 | `CONTINUE_IN_WORKFLOW` |
| `DESIGN_READY` | Phase 3 design 写完（或 Medium ① 跳过） | 进 Phase 4 | `CONTINUE_IN_WORKFLOW` |
| `TASKS_READY` | Phase 4 tasks 写完 | 进 Phase 5 | `CONTINUE_IN_WORKFLOW` |
| `HANDOFF_READY` | Phase 5 handoff-payload.yaml + 人读简报 + tasks.md Traceability Matrix 三件套产齐 | 等用户裁决是否启动 `/specs-execute` | `REPORT_AND_STOP`（除非用户明确继续） |
| `GATE_BLOCKED` | Gate A/B/C 用户驳回 / 持续 Needs Changes 未达成共识 | 等用户决定下一步 | `WAIT_FOR_USER` |
| `BLOCKED` | 其他硬阻塞（不属于以上各分类） | 等用户裁决或分流 | `WAIT_FOR_USER` 或 `REPORT_AND_STOP` |

- **报告必须使用 workflow-qualified state**：`/specs-write:HANDOFF_READY` 等，不得用裸 `DONE` / `BLOCKED`。
- **State Authority**：spec 目录文件 + `handoff-payload.yaml` 是合同事实源；State 仅用于 spec 编写调度。
- **源**：`/specs-write.md §0.2.1-0.2.3`。

### 9.2 /specs-execute State（11 种 · §0.2.1）

| 状态 (State) | 进入条件 | 退出 / 路由 | 路由动作 (Route Action) |
| ------- | ---------- | -------------- | --------------- |
| `NO_APPROVED_SPEC` | 无 approved spec 或无可执行 Task | 分流 `/specs-write` 或 `/project-steward` | `REPORT_AND_STOP` |
| `TASK_LOCATED` | Phase 1 Locate 完成 + 11 项前置检查全过 | 进 Phase 2 | `CONTINUE_IN_WORKFLOW` |
| `IN_PROGRESS` | 已进入 Phase 2-7 闭环 | 继续 Red→Green→Refactor→Verify | `CONTINUE_IN_WORKFLOW` |
| `PAUSE_AND_ASK_PENDING` | 命中 §7.3 4 项白名单 | 等用户裁决 | `WAIT_FOR_USER` |
| `ENVIRONMENT_BLOCKED` | 测试环境 / 依赖 / 权限 / 本地工具链阻塞，且非 Spec 缺陷 | 按 `../../specs-execute/protocols/blocking-and-rollback.md` 处理 | `WAIT_FOR_USER` |
| `ROLLBACK_REQUIRED` | 本 Task 写入导致不可接受风险或验证失败需回滚 | 已批准 + 无真实副作用 → 执行回滚；否则等用户裁决 | `CONFIRMED_ACTION`（仅本 Task Revert + Notes）/ `WAIT_FOR_USER` |
| `BLOCKED` | 上游锚点失效 / Touches 越界 / 其他硬阻塞 | 按 `../../specs-execute/protocols/blocking-and-rollback.md` 处理 | `REPORT_AND_STOP` |
| `SPEC_REPAIR_REQUIRED` | 需求 / 设计 / SSOT 缺陷导致不能安全执行 | 回切 `/specs-write` | `REPORT_AND_STOP` |
| `TASK_DONE` | Verification / DoD 全 PASS + 无 Pause-and-Ask 未决 | 更新 tasks.md + 报告 + 选下一 Task | `CONTINUE_IN_WORKFLOW` |
| `CLOSEOUT_READY` | 全 Task Done + 需归档 / artifacts 核验 | 进 Phase 9 交付收尾 | `CONTINUE_IN_WORKFLOW` |
| `CLOSEOUT_DONE` | 交付收尾完成 + active → done 物理迁移完成 | 返回 `/project-steward` | `REPORT_AND_STOP` |

- **CONFIRMED_ACTION 边界**：仅授权当前 Task 的本地 Revert Command + Execution Notes 更新，不授权真实副作用回滚 / spec 修改 / 下游 workflow / 其他 Task。
- **源**：`/specs-execute.md §0.2.1-0.2.3`。

---

## 10. Reflection（kind / resolution / severity）

### 10.1 kind（7 种 · appendix §A.7.3）

| kind | 含义 | 阻塞规则 | 软累计 |
| ------ | ------ | ---------- | -------- |
| `implementation_choice` | 实现期选了某方案，记录权衡 | 不阻塞 | 任意 severity |
| `new_invariant_candidate` | 发现可升格为 charter §5 INV-* 的项目级红线 | `INV-BAN-* / INV-SEC-*` 候选 → Gate B 阻塞；`INV-LIM-*` / 软红线候选 → Gate B 但不阻塞 | — |
| `reusable_pattern` | 可抽到 `.github/instructions/` 的通用模式 | 不阻塞 | 任意 severity |
| `spec_drift` | 实现与 spec 不一致 | `severity: high` → 阻塞新 feature 启动 Phase 1 | low / medium 不阻塞 |
| `audit_debt` | Phase 1.5 漏审的现状，事后补 | `severity: medium / high` 或 `extension_payload` 非空 → 阻塞 | `severity: low` 软累计（在 audit.md `## 11. Audit Refresh Log` 追加一行） |
| `ssot_stewardship` | 发现 SSOT 健康风险 / 改进建议，建议 SSOT Patch | `severity: high` 或 `approval_required: yes 且不修改 Authoritative SSOT 就无法继续` → Gate A/B 阻塞 | low / medium 且 `approval_required: no` 软累计 |
| `test_modified` | 防 2 TDD 作弊检测专用 | 必填 `before_sha256` / `after_sha256` / `reason` 三字段；缺任一字段 → 防 2 机读自检脚本不予认可 | 由 §A.2 hash 校验机械触发 |

- **Existing Touches 扩展回流**（`audit_debt` 子类型）：执行端某 Task 自动追加 ≥ 2 公共契约文件至 `Existing Touches`，必填 `extension_payload` 节（详 `appendix.md §A.7.5`）。
- **源**：`appendix.md §A.7`。

### 10.2 resolution（6 种 · appendix §A.7.2）

| resolution | 真实落点 | 是否需用户批准 |
| ------------ | ---------- | ---------------- |
| `promoted_to_invariant` | charter.md `## 5. Architectural Invariants`（升 INV-BAN-*/ INV-LIM-* / INV-SEC-*） | Gate B 裁决 |
| `distilled_to_standards` | `.github/instructions/<主题>.md` 新增条目 | Gate B 裁决（INV-BAN-*/ INV-SEC-* 候选）/ 软累计（reusable_pattern） |
| `folded_into_spec` | `requirements.md` / `design.md` / `audit.md` 对应 ID 修订 | Gate C（Spec Breach 修订）/ AI-DRI（执行端微调） |
| `folded_into_ssot` | charter / .github/standards / 母本对应权威章节 | **必需用户明确批准**（Authoritative SSOT 修改边界） |
| `promoted_to_ssot_patch` | `docs/specs/active/<patch-slug>/` 新建 SSOT Patch spec 或 `.github/instructions/` 新增建议草案文件 | **必需用户明确批准**（不直接改母本） |
| `dismissed` | 显式驳回 + archive 留 `reason` | Gate B / AI-DRI 视情况 |

- **同 PR 物理删除 + 追加**：归档时同 PR 从 YAML 物理删除条目（不是改状态位）+ 同 PR 在 `reflections-archive.md` 追加。
- **YAML 与 archive 不得同 ID 重复**：出现重复 → 视为 GC 失职，回滚 PR。
- **`reflections-archive.md` 不反流全局**：feature 内「实现旁注备忘」，对其他 feature 不直接可见；全局反流走 §15 五条路径。
- **源**：`appendix.md §A.7.2-A.7.4`。

### 10.3 severity（3 级）

- `low`：影响范围小，可软累计；
- `medium`：影响下一轮 spec 派生准确性，按 §10.1 阻塞规则处理；
- `high`：阻塞新 feature 启动，必须先回写 spec / charter / SSOT。

---

## 11. 抢占协议（3 档 · appendix §A.6）

### 11.1 三档抢占

| 类型 | 触发场景 | 现场保护 | depth ≤ 2 |
| ------ | ---------- | ---------- | ----------- |
| `P-INLINE` | 同 Task 内紧急修补 | **不冻结**、**不写 `suspended_state`**，直接走 `/specs-execute` Refactor 路径处理 | — |
| `P-SIBLING` | 同 feature 跨 Task 切换（用户改主意先做 TASK-003） | 现场保护三件套（详 `blocking-and-rollback.md §1.6.1`）+ 写 `suspended_state` 节 | 计入 |
| `P-CROSS` | 跨 feature / 全新临时任务（线上 P0 bug） | 现场保护三件套 + 写 `suspended_state` 节 | 计入 |

- **`P-CROSS` 禁连续**：连续 P-CROSS = 紧急 bug 风暴或战略不明，必须停下让用户介入。
- **嵌套 depth ≤ 2**：超过即视为项目失控。

### 11.2 三件套（Suspend）

- **Resume Strategy.mode**：`lightweight_wip_commit` / `wip_branch_reset` 两路径。
- **`test_anchors_locked_at` 字段**：跨中断 §A.2 hash 校验的免责锚点；缺失 → 视为非法中断现场，Resume 时必须先补 hash 重锁。
- **`suspended_state` 生命周期**：仅在 Suspend 期间存在；Resume 时**物理删除**该节（仅变状态位 = 失职）。
- **源**：`appendix.md §A.6.2-A.6.4` + `blocking-and-rollback.md §1.6.2`。

### 11.3 三件套（Resume）

1. **Locate**：执行端 Locate 阶段优先读 `handoff-payload.yaml#suspended_state` 而非常规 Phase 1 Intake——抢占恢复必走「快速接力」路径。
2. **Restore**：按 `Resume Strategy.mode` 分流恢复工作树；恢复后必校验 Test Anchors hash 与 `suspended_state.test_anchors_locked_at` 时刻锁定值对照。
3. **Resume**：从 `suspended_state.resume_anchor.phase` 接力到原 Task 流；同步删除 `suspended_state` 节。

- **源**：`appendix.md §A.6.3` + `blocking-and-rollback.md §1.6.3`。

### 11.4 与 GC 衔接（A.7.1）

写作端 Phase 0 在读 `implementation_reflections` 之前**必须先**扫描 `handoff-payload.yaml` 是否存在 `suspended_state` 节：

- **(a) 该 feature 实际已 Done**→ 视为执行端 Resume 漏删，停下追问用户后手动从 YAML 删除；

-**(b) 该 feature 未 Done**→ 不得启动新 feature 的 Phase 1，建议先回该 feature 走 `/specs-execute` 完成 Resume + 后续 Task。

---

## 12. 防御机制（防 1-5）

| 防 | 名称 | 触发场景 | 处置 |
| ---- | ------ | ---------- | ------ |
| **防 1** | SSOT 撕裂 | tasks.md Traceability Matrix 与 handoff-payload.yaml `traceability` 不一致 | `traceability_check_script` exit code：0=同步 / 4=撕裂 / 其他=结构错；非 0 拒进 Phase 9 |
| **防 2** | TDD 作弊 | Phase 4 末未跑 TDD-Lock / Phase 5 Green 改 [TDD-Lock] 锁定文件 / Phase 6 Refactor 修测试未同步重锁 | Phase 7 拦截；未输出 [TDD-Lock] / 测试文件 SHA-256 漂移 → 退 Phase 4 或回切 |
| **防 3** | Revert 雪崩 | 多 Task 触动同一既有文件，单 Task `Revert Command` 直接执行会回滚其他已 Done Task | `revert_dependency_graph` 求交集 + `git diff --quiet` 预检 |
| **防 4** | MCP 幻觉 | audit.md EXIST-* 类条目用「看起来是」式判断填充；evidence 用纯文字描述无法判断 AI 是否真去跑过工具 | DB / API / UI / FS 类 EXIST 必填 `Verified By:` 4 项 + audit-evidence/ 4 桶分类 |
| **防 5** | 注意力稀释 | 执行端 Hydrate 每个 Task 加载 SSOT / charter / audit / design 全量上下文导致 attention_budget 爆炸 | `Context Required Before Execution` P0 / P1 严格二分；P0 超上限 → 回 Phase 4 拆分 |

-**跳读 Companion Documents `MUST read`**= 违反对应防御机制。
-**源**：`/specs-write.md §17` + `/specs-execute.md §22` + `appendix.md §A.1-A.5`。

---

## 13. 三轨方法论（ATDD / BDD / TDD）

### 13.1 三轨分工（cross-cutting §3.5）

| 方法 | 关注层 | 落点 | 形式 |
| ------ | -------- | ------ | ------ |
| **ATDD**（验收驱动） | 系统级 / 「什么算完成」 | `requirements.md` 的 AC + `tasks.md` 的 DoD | EARS 六句式 + Traceability Matrix |
| **BDD**（行为驱动） | 功能级 / 「什么动作 → 什么状态变化」 | `requirements.md §7` + `tasks.md` 仅引用 Scenario 锚点 | `Given / When / Then` 三段式 |
| **TDD**（测试驱动） | 代码级 / 「代码实现是对的」 | `tasks.md` 的 `Verification` + 执行阶段 Red-Green-Refactor | 单元测试先行 |

- **三者关系**：ATDD 定目标 → BDD 锁路径 → TDD 保实现。
- **EARS 6 句式**：在 `cross-cutting.md §3.1`；要求可观察、可验证、可写测试；单条 AC 不超过 1 行业务行为。
- **BDD Scenario 是契约**：不是测试代码；spec 中**禁写测试代码**（mock / fixture body / Jest 语法）→ 越界到 TDD。
- **TDD 在 spec 中只留锚点**：`Test Anchors` 字段写测试文件路径 + Scenario ID；测试代码在 `/specs-execute` 落地。
- **源**：`cross-cutting.md §3`。

### 13.2 TDD-Lock（防 2 · Phase 4 末必跑）

- **定义**：Phase 4 Red 写完测试后跑 SHA-256 锁定，回填 tasks.md `Test Anchors` + handoff-payload `first_task.test_anchors`，输出 `[TDD-Lock]` 声明。
- **Phase 5 Green 严禁改 [TDD-Lock] 锁定文件**；§5.1 后必重算 SHA-256 与 §4.2 比对，不一致 → 退 Phase 4 或走 `blocking-and-rollback.md §1`。
- **Phase 6 Refactor 修测试例外**：允许修（提取 fixture / 重命名）但必同步：(1) 跑全测仍 Green；(2) 重算 SHA-256 同 PR 更新 tasks.md `Test Anchors` + handoff-payload `first_task.test_anchors`；(3) `Reflections: kind: test_modified` 留【before_sha256 / after_sha256 / reason】；(4) 未同步 → §7 视为作弊拦截。
- **源**：`/specs-execute.md §4.2 / §5.3 / §6` + `appendix.md §A.2`。

### 13.3 Test Anchors（appendix §A.2）

- **定义**：`tasks.md` Task 头部字段，记录测试文件路径 + BDD Scenario ID + SHA-256 hash。
- **唯一所有权**：每个 BDD Scenario 由唯一 Task `Test Anchors` 拥有；多 Task 共享所有权 → 防 2 检测违规。
- **跨中断免责字段**：`test_anchors_locked_at`（ISO 8601）—— 抢占 Suspend 时刻锁定值；缺失 → 非法中断现场。
- **源**：`appendix.md §A.2` + `cross-cutting.md §4.2 schema`。

### 13.4 DoD 三闭环（/specs-execute Phase 7）

- **ATDD**：每条 AC 有 Acceptance Test 路径（`Verification Commands` 含对应单测 / E2E）。
- **BDD**：每条 US 有 Scenario 覆盖（`requirements.md §7` Scenario 在 `Test Anchors` 引用）。
- **TDD**：`Verification Commands` 单测全 PASS。
- **任一闭环失败**：不得标 `Done`；Status 留 `In Progress` 或改 `Blocked`。
- **源**：`/specs-execute.md §7.2`。

---

## 14. 文件路径 / 目录契约

### 14.1 specs_root 解析

- **查找顺序**：`docs/specs/` → `specs/` → 都没有则**建议**在 `docs/specs/` 创建并待用户确认。
- **二级分仓**（强制）：`<specs_root>/active/<feature-slug>/` 进行中；`<specs_root>/done/<feature-slug>/` 已交付。
- **simple-write 简写**：本工作流中 `docs/specs/<feature-slug>/...` 是**抽象简写**，物理上必解析到 active/ 或 done/，不得落平铺位置。
- **源**：`/specs-write.md §1.6`。

### 14.2 feature-slug 命名规则

- **格式**：kebab-case；不带日期 / 版本号 / 空格。
- **唯一性**：一对一不复用；交付后 `git mv` 到 done/，slug 不变。
- **示例**：`user-onboarding-flow` ✅ / `User_Onboarding_2026Q2 v2` ❌。
- **源**：`/specs-write.md §1.6`。

### 14.3 feature 目录结构（active / done 同构）

- **`<specs_root>/active/<feature-slug>/`**
  - `maturity-intake.md`：L0 · Phase 0 必产
  - `charter.md`：L1 · Phase 1 必产
  - `audit.md`：L2 · 仅 Hybrid / Brownfield 必产
  - `audit-evidence/`：Phase 1.5 真实校验工具产出（DB / API / UI / FS 4 桶）
  - `requirements.md`：L3 · Phase 2 必产
  - `design.md`：L4 · Phase 3（Medium ① 可缺）
  - `tasks.md`：L5 · Phase 4 必产
  - `handoff-payload.yaml`：L5 · Phase 5 必产；机读 SSOT
  - `artifacts/`：L6 · /specs-execute 期间副产物落点（分类子目录）
  - `reflections/`：包含具体 reflections 记录（如 `REF-###.md`）
  - `reflections-archive.md`：append-only · 写作端 Phase 0 GC 后归档

### 14.4 artifacts 落点硬约束

- spec 执行期任何 Task 产生的非源码副产物（plan / verify / cost ledger / quarantine / dry-run / 4 闸口报告 / drift 报告）**必写入**`<feature-slug>/artifacts/` 或子目录。

- **禁项目根**`reports/` / `tmp/` / `output/` 产生散落产物；散落者按 `cleanup_manifest_<date>.md` 迁移。
-**必落 tasks.md `Artifacts:` 声明路径**；项目根通用目录无豁免 → 越界。

- **源**：`/specs-write.md §1.6` + `/specs-execute.md §5.2 / §9`。

### 14.5 audit-evidence 4 桶（防 4）

- **DB 桶**：真实数据库查询输出（schema dump / 字段类型 / 索引 / 行数 / 触发器等）。
- **API 桶**：真实 API 调用响应（curl / Postman / OpenAPI / 真实环境调用）。
- **UI 桶**：真实页面截图 + Playwright / Selenium / 浏览器查询输出。
- **FS 桶**：文件系统真实清单（tree / find / 文件大小 / 权限 / 修改时间）。
- **`Verified By:` 4 项**：`tool` / `command_or_query` / `output_path` / `verified_at: <ISO 8601>`（7 天有效期重检）。
- **源**：`appendix.md §A.4` + `templates/audit.md`。

### 14.6 Project Archives 路径

- **路径**：`docs/specs/project archives/工程交付归档-YYYY-MM-DD.md`。
- **性质**：项目层归档；feature 交付时 AI 在交付 PR 中追加一条；只引用 reflection 概要 ID（如 `REF-001 · distilled_to_standards`），**不复制全文**。
- **与 reflections-archive.md 区别**：reflections-archive 是 feature 内「实现旁注备忘」，不反流全局；Project Archives 是项目层交付事实。
- **源**：`appendix.md §A.7.4`。

---

## 15. 反流路径与权威 SSOT

### 15.1 Authoritative SSOT 边界

- **定义**：母本 / L1 SSOT / `.github/instructions/` 中作为权威输入的章节。
- **修改边界**：未获用户明确批准前，**不得直接修改**Authoritative SSOT；允许写入 spec 内的 `SSOT Stewardship Suggestions` / `Repair Draft` / `SSOT Gap` 作为候选。

-**源**：`cross-cutting.md §1.4 B 第 5-6 条`。

### 15.2 SSOT 修订请求流程（轻量）

1. 在 `maturity-intake.md SSOT Stewardship Suggestions` / `Repair Draft`、`audit.md §5` 或 `charter.md Notes` 记录冲突；
2. 通知用户决定（a 回流 SSOT / b spec 局部豁免，需在 `charter §6 Out of Charter` 显式登记）；
3. 不得在未决前推进下游。

- **源**：`cross-cutting.md §1.4 B 第 7 条`。

### 15.3 五条全局反流路径（影响后续 feature）

| Resolution | 落点 | 触发 Gate |
| ------------ | ------ | ----------- |
| `promoted_to_invariant` | `charter.md §5` 升 INV-BAN-*/ INV-LIM-* / INV-SEC-* | Gate B |
| `distilled_to_standards` | `.github/instructions/<主题>.md` 新增条目 | Gate B（INV-BAN-*/ INV-SEC-* 候选）/ AI-DRI（reusable_pattern 软累计） |
| `folded_into_spec` | `requirements.md` / `design.md` / `audit.md` 对应 ID 修订 | Gate C / AI-DRI |
| `folded_into_ssot` | charter / .github/instructions / 母本对应权威章节 | **用户明确批准**（必需） |
| `promoted_to_ssot_patch` | `docs/specs/active/<patch-slug>/` 新建 SSOT Patch spec 或 `.github/instructions/` 新增建议草案 | **用户明确批准**（必需，不直接改母本） |

### 15.4 Feature 内归档（不反流全局）

- **路径**：`<feature-slug>/reflections-archive.md`（active / done 同名）。
- **性质**：append-only，不修改历史记录；**不反流为全局历史**；对其他 feature 不直接可见。
- **触发**：reflection 热数据超 10 条 / 已裁决者，由写作端 Phase 0 GC 归档。
- **源**：`appendix.md §A.7.4`。

### 15.5 SSOT Health 五态（maturity-intake.md）

| 状态 | 含义 | 下一步 |
| ------ | ------ | -------- |
| `Healthy` | SSOT 健康可派生 | 进 charter |
| `Needs Clarification` | 部分不确定但不阻塞 | 进 charter，但必须列入 `Blocking Issues` / `Open Questions`，并按 Gate A/B/N/A 分类 |
| `Needs Repair` | 健康风险已影响下游派生 | 阻塞下游 / 先修 SSOT |
| `Unfit As Source` | 不足以作为权威输入 | 阻塞下游 / 分流上游 workflow（如 `/project-inception`） |
| `SSOT Absent` | 缺 SSOT | 阻塞下游 / 创建 SSOT |
| **AI 边界** | AI 有 SSOT 建议权但**无静默改写权** | 不得在未获用户批准前直接修改 Authoritative SSOT |

-**源**：`templates/maturity-intake.md` 第 15 行起 + `cross-cutting.md §1.4 B`。

---

## 附录 · 字母索引（核心 50 条）

| 术语 | 章节 |
| ------ | ------ |
| Acknowledged | §8.1 |
| active / done 二级分仓 | §14.1 |
| Add | §5.1 |
| AI-DRI 自决 | §7.1 + §8.1 |
| Anti-Invariants | §1 (L5) |
| Approval.Status | §8.1 |
| Archive Only | §5.7 |
| ATDD | §13.1 |
| audit-evidence 4 桶 | §14.5 |
| Audit Depth Gate | §2.3 |
| Audit Profile | §2.2 |
| Audit Refresh Log | §1 (L2) + §5.4 |
| Authoritative SSOT | §15.1 |
| Baseline Survey | §2.2 |
| BDD | §13.1 + §4.3 |
| Blocked / Blocked(Suspended) | §8.2 |
| Brownfield | §2.1 |
| Charter | §1 (L1) |
| Conflicts EXIST-* | §5.8 + §6 |
| CONFIRMED_ACTION | §9.2 |
| Context Required（P0 / P1） | §12（防 5） |
| CONTINUE_IN_WORKFLOW | §9.1-9.2 |
| Decision Gate A / B / C | §7.1 |
| Delta Operation 7 种 | §5 |
| Deprecate | §5.4 |
| Depends EXIST-* | §6 |
| design.md | §1 (L4) |
| distilled_to_standards | §10.2 + §15.3 |
| DoD 三闭环 | §13.4 |
| Done | §8.2 |
| EARS 6 句式 | §13.1 |
| EXIST-* | §4.1 |
| Existing Touches 扩展回流 | §10.1（audit_debt） |
| Extends EXIST-* | §6 |
| Feature-Scoped Full-Surface Audit | §2.2 |
| folded_into_spec / folded_into_ssot | §10.2 + §15.3 |
| Greenfield | §2.1 |
| Greenfield Survey | §2.2 |
| handoff-payload.yaml | §1 (L5) + §14.3 |
| HANDOFF_READY | §9.1 |
| Hybrid | §2.1 |
| INV-BAN-*/ INV-LIM-* / INV-SEC-* | §4.1 |
| Irreversible Action | §7.1 |
| L-STRAT / L-DESIGN / L-IMPL / L-OPS | §7.2 |
| Large | §3 |
| Locate | §1 (L6) + §11.3 |
| Medium ① / ② | §3 |
| Merge Back | §5.6 + §15.3 |
| methodology-kernel | §0 + §12 (kernel.md) |
| Modify | §5.2 |
| Net New | §5.1 + §6 |
| new_invariant_candidate | §10.1 |
| Out of Charter | §1 (L1) + §5.4 |
| P-INLINE / P-SIBLING / P-CROSS | §11.1 |
| PAUSE_AND_ASK_PENDING | §9.2 |
| Pause-and-Ask 4 项 | §7.3 |
| Pending | §8.2 |
| Preserve | §5.5 |
| project-mode | §2.1 |
| Project Archives | §14.6 |
| promoted_to_invariant | §10.2 + §15.3 |
| promoted_to_ssot_patch | §10.2 + §15.3 |
| REPORT_AND_STOP | §9.1-9.2 |
| Replaces EXIST-* | §6 |
| Replace | §5.3 |
| reflections-archive.md | §15.4 |
| Reflection kind 7 种 | §10.1 |
| Reflection resolution 6 种 | §10.2 |
| Resume 三件套 | §11.3 |
| reusable_pattern | §10.1 |
| Seed / Init | §2.1 |
| severity（low / medium / high） | §10.3 |
| Small | §3 |
| spec_drift | §10.1 |
| SPEC_REPAIR_REQUIRED | §9.2 |
| ssot_stewardship | §10.1 + §15.1-15.2 |
| SSOT Health 五态 | §15.5 |
| Superseded | §8.1 |
| suspended_state | §11.2 |
| TASK-### | §4.1 |
| TASK_DONE / TASK_LOCATED | §9.2 |
| Test Anchors | §13.3 |
| TDD | §13.1 |
| TDD-Lock | §13.2 |
| test_modified | §10.1 |
| Traceability Matrix | §1 (L5) + §12（防 1） |
| WAIT_FOR_USER | §9.1-9.2 |
| workflow-qualified state | §9.1 + §9.2 |

---

**修订规则**：本文与 `methodology-kernel.md` / `/specs-write.md` / `/specs-execute.md` / `cross-cutting.md` / `appendix.md` / `templates/*` 字面零漂移。任一上游修改 → 同 PR 修订本文；本文修订 → 同 PR 修订下游受影响文档。
