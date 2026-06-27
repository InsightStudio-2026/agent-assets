# Methodology Kernel · /specs-write 方法论一页内核

> **本文是 `/specs-write` + `/specs-execute` 体系的一页方法论事实源**。
> 你（执行 spec 工作流的代理或开发者）应在新 feature 开工前、外部学习者首次接触本体系前、对方法论术语存疑时第一站读这里。

---

## 0. 本文定位

本文是 **方法论内核**（Methodology Kernel），不是说明书也不是教程：

- **覆盖**：spec 生命周期九大语义层、四种项目成熟度、三档复杂度、七种 delta 操作语义、active/done 迁移、merge back 与 archive 关系、与 `/specs-write` / `/specs-execute` 状态机的术语锚点。
- **不覆盖**：模板字段细节、Phase 内部流程、Decision Gate 防伪协议原文、handoff-payload schema、抢占协议、Reflections GC 详则。这些放在 `../` 与 `../../specs-execute/` 的支撑文档里，按需懒加载。
- **硬规则**：本文与 `.github/skills/specs-write/SKILL.md` / `.github/skills/specs-execute/SKILL.md` 的状态机术语**零漂移**。任何术语只要在两个入口出现，本文使用同名同义；本文不发明新名词，只压缩与命名。
- **演进路径**：`../references/terminology.md`、`entry-decision-tree.md`、`../examples/`、`../conformance-fixtures/` 都从本文派生，不复制本文事实。Phase 执行期反模式查询表在 `cross-cutting.md §6`（B-* 体系）。

---

## 1. Spec 生命周期 · 九大语义层

`requirements / design / tasks` 只是**核心执行合同三件套**，不是完整 spec 生命周期。完整生命周期始终覆盖以下九层语义；文件可裁剪（详 §3），语义层不可裁剪：

| 层 | 名称 | 回答的问题 | 现有承载 |
| ---- | ------ | ------------ | ---------- |
| L0 | **Maturity & SSOT Health** | 项目处于什么成熟度？母本 / L1 SSOT 是否健康可派生？ | `maturity-intake.md` |
| L1 | **Charter / Proposal** | 为什么做？做什么？不做什么？谁授权？红线在哪？ | `charter.md`（含 `## 5. Architectural Invariants` INV-BAN/LIM/SEC + `## 6. Out of Charter`） |
| L2 | **Current-state Audit** | 本 feature 影响面里既有什么？可复用 / 扩展 / 替换 / 弃用 / 保留什么？ | `audit.md`（仅 Hybrid / Brownfield；EXIST-* 反向锚点） |
| L3 | **Behavior Spec / Delta Requirements** | 系统的外部可观察行为是什么？相对既有行为新增 / 修改 / 替换 / 弃用 / 保留什么？ | `requirements.md`（REQ + AC + BDD Scenario + `Relation to Existing` +**NFR-* §10**6 类槽位 · 详 §1.1） |
| L4 | **Technical Plan / Design** | 怎么做？跨边界契约、失败策略、并发锁、迁移路径是什么？ | `design.md`（DSN-`<domain>`-### + INV 反向追溯 + Failure Strategy） |
| L5 | **Tasks / DAG / Handoff** | 拆成哪些单 Task？依赖如何？测试 / 回滚锚点是什么？ | `tasks.md` + `handoff-payload.yaml` |
| L6 | **Execution / Verification** | 实际跑 Red → Green → Refactor → Verify，留命令输出与 artifacts | `/specs-execute` Phase 1-7 + `<feature-slug>/artifacts/` |
| L7 | **Reflection / Reflux** | 实现期发现的实现选择 / 候选 INV / 复用模式 / spec drift / audit debt / SSOT 改进建议如何回流？ | `handoff-payload.yaml#implementation_reflections.active` + `reflections-archive.md` |
| L8 | **Archive / Merge Back** | 交付后哪些进入 feature 内归档？哪些回并到 charter / standards / 母本 / SSOT？ | active → done `git mv` + INV-* 上升 + standards 蒸馏 + folded_into_ssot / promoted_to_ssot_patch |

**硬规则**：

1. L0 → L8 是**单向语义流**，不得跳层。但 L2 可裁（仅 Hybrid/Brownfield 必走），L4 可裁（仅 Medium ① 路径），L7 / L8 在 feature 内必产但范围因 reflection 是否产生而异。
2. **派生优先**（cross-cutting §1.4 B）：从已批准上游派生，引用而非复述；冲突回流上游，不就地妥协。
3. **稳定锚点**：跨层引用一律走 ID（SRC / REQ / AC / US / DSN-`<domain>`-### / EXIST-*/ TASK / INV-BAN-* / INV-LIM-*/ INV-SEC-* / **NFR-SEC-* / NFR-PERF-* / NFR-OBS-*/ NFR-REL-* / NFR-UX-* / NFR-PLAT-***），禁行号（除归档快照）。
4. **强制复述**（防 5）：执行 Task 前必读并引用 `Context Required` 锚点原文，不凭记忆。

### 1.1 NFR · 六类槽位（L3 子层 · 必填或显式 N/A）

NFR 是 L3 Behavior Spec 的不可裁子层。跟 functional REQ 平行存在，承载 spec 阶段必须显式声明的非功能契约。如果延后到 `/specs-execute` 才发现，会变成返工或硬吞（事实源 `../templates/requirements.md §10` + 本文 §1.1）。

| Type | ID 前缀 | Concern | 主 Routed-to | 高风险触发 |
| ------ | -------- | --------- | ------------- | ----------- |
| Security | `NFR-SEC-*` | authz / PII / secrets / audit / encryption / input-validation / supply-chain | `/security-privacy-audit` | 涉外部 API / OAuth / token / PII / 密钥 / 审计 |
| Performance | `NFR-PERF-*` | latency / memory / bundle / cold-start / API-throughput / DB-query | `/performance-reliability-audit` | 涉关键路径性能 / 大数据量 / 高并发 |
| Observability | `NFR-OBS-*` | log / metric / trace / alert / dashboard / runbook | `/observability-incident` | 需新 SLO / alert / runbook |
| Release | `NFR-REL-*` | feature flag / migration / rollback / canary / blue-green | `/release-deploy` (+ `/data-migration-safety` 如涉 schema) | 涉生产副作用 / migration / rollback |
| UX / A11y | `NFR-UX-*` | keyboard / screen-reader / contrast / focus / aria / responsive / errors / loading / i18n | `/design-system-audit` | 涉用户可见 UI 或 i18n |
| Platform | `NFR-PLAT-*` | OS / browser / device / network | `/desktop-release` 或 `/release-deploy` | 涉桌面 / 多平台 / 浏览器版本 |

**NFR 硬规则**：

1. **High-Risk Assessment 必填**（`templates/requirements.md §10.0`）：6 类 Risk Trigger 各标 High / Low，与 charter Goals / Out-of-Charter / Architectural Invariants 一致。
2. **High → Active 强制**：任一类标 High → 该类必有 ≥ 1 条 `Status: Active` NFR；不允许整类 N/A。
3. **Low → 显式 N/A**：标 Low 的类必须显式 `Status: N/A: <理由>`，不允许整段空白。
4. **Verification 不空**：每条 Active NFR 必有 `Verification` 字段（命令、专项 workflow 锚点或 verification report 锚点之一）。
5. **Brownfield 强制 Delta Operation**：Brownfield 模式下，每条 NFR 必有 `Delta Operation` 字段（Add / Modify / Replace / Deprecate / Preserve）；Greenfield 不强制。
6. **Tasks 引用 traceability**：`tasks.md` 至少有 1 个 Task 引用每条 Active NFR 作为 Verification 输入或 Routed-to 触发；NFR 不能只在 requirements 声明而 tasks 不接。
7. **专项 workflow 双向回链**：高风险 NFR 必标 `Routed to: <专项 workflow>`；专项 workflow 在交付报告中必反向引用本 NFR-* ID（让 spec 与专项审计形成双向 traceability）。

NFR 字段详细模板与槽位结构详 `templates/requirements.md §10`；conformance 校验由 `R-CHK-EX-1.8` 在 `../../asset-quality-gates/references/checks-catalog.md §3.1` 实现。

---

## 2. Project Mode · 四种成熟度

进 Phase 1 前必判 Project Mode；判定权威源 = `templates/maturity-intake.md` 第 5 行起的判定硬规则：

| Mode | 判定 | Audit Profile | Phase 1.5 | 何时跳 |
| ------ | ------ | ---------------- | ----------- | -------- |
| **Seed / Init** | 仓库 / spec / 代码 / DB / 测试 / 归档基本为空，且当前任务是建立项目骨架 / 初始 SSOT / 第一批基础设施 | Baseline Survey | 跳 | 跳 Phase 1.5；不跳 Baseline Survey 与 SSOT Health Check |
| **Greenfield** | 与既有系统物理隔离，但项目已有 README / .github/standards / CI / 测试约束 / 技术红线 / 母本 SSOT | Greenfield Survey | 跳 | 跳 Phase 1.5；不跳 Greenfield Survey 与 SSOT Health Check |
| **Hybrid** | 本 spec 涉及领域内存在 ≥ 1 个既有模块 / 表 / 接口 / 路由 / UI 入口，同时有明显新建部分 | Feature-Scoped Full-Surface Audit | **必走** | 不跳 |
| **Brownfield** | 本 spec 主要修改 / 替换 / 扩展既有模块、表、接口、数据流或历史行为 | Feature-Scoped Full-Surface Audit | **必走** | 不跳 |

**硬规则**：

- N/A 必须**证据化**：Baseline / Greenfield Survey 中的 N/A 必给 evidence + Future Audit Trigger；不得用「当前为空」替代证据。
- Hybrid / Brownfield **必走 Phase 1.5**；走完必过 **Audit Depth Gate 双层门**（14 面覆盖 + 真实数据库面 / 文档 SSOT 面不可 N/A + Overall Confidence ≥ 80% + 两强证据面各 ≥ 80% + Unknowns 清零）。

---

## 3. 复杂度 Mode · 三档（文件裁剪规则）

复杂度只**裁剪承载文件**，不裁剪 §1 的九大语义层。即使 Medium 单文件 spec.md，内部仍保留 Charter / Audit / Requirements / Design / Tasks / Verification 段落与 Decision Gate 判定：

| Mode | 文件形态 | 适用 | 跳过条件 |
| ------ | ---------- | ------ | ---------- |
| **Small** | 不启用 workflow | 错字 / 单文件 bug / 用户已给出完整代码级指令 / 纯查询 / 解释 / 阅读代码 | — |
| **Medium ①** | `requirements.md` + `tasks.md`（跳 design），头部标 `Mode: Medium (design skipped:`<reason>`)` | 设计无替代 / 不涉 schema / API 外部消费者 | 跳 Phase 3 |
| **Medium ②** | 单文件 `spec.md`，头部标 `Mode: Medium (single-file:`<reason>`)`；内部仍保留 Requirements / Design / Tasks 三段与 Gate 判定 | 单人小特性 / 设计无替代 / 不涉 schema / API 外部消费者 | 单文件 |
| **Large** | 完整三件套 `requirements.md` + `design.md` + `tasks.md`（必要时含 audit.md） | 新功能 / 跨模块重构 / 架构边界变动 / Schema / API / 协议 / 事件契约变更 / 权限 / 计费 / 合规 / 数据治理 / AI/LLM pipeline / Agent / 长链路任务 / 复杂 Bug | — |

**硬规则**：**文件数不是方法论**。即使 Medium 单文件，§1 的 L1（charter）/ L3（behavior）/ L4（design）/ L5（tasks）语义段必须存在；缺段视为越界，回退到 Large。

---

## 4. Delta Operation · 七种语义

`requirements / design / tasks` **+ NFR-* §10**中每条新增条目（REQ / DSN / TASK / NFR）都必须能被分类为以下七种 delta 操作之一。Brownfield 不重写全量规格，只表达 delta；Greenfield / Seed 大多数条目落 `Add`：

| # | Delta | 现有锚点 | 何时使用 | 必填字段 |
| --- | ------- | ---------- | ---------- | ---------- |
| 1 | **Add** | `Relation to Existing: Net New`（cross-cutting §1.4 A） | 既无 SSOT 也无现状承接 | `Justification`（为何 SSOT 与现状均未覆盖） |
| 2 | **Modify** | `Relation to Existing: Extends EXIST-*` | 在既有基础上叠加 | EXIST-*锚点 + `Derived From` SRC |
| 3 | **Replace** | `Relation to Existing: Replaces EXIST-*` | 替换既有 | EXIST-* 锚点 + 迁移路径（Migration Plan / Failure Strategy） |
| 4 | **Deprecate** | charter `## 6. Out of Charter` 显式登记 + 新 spec 中 `Replaces EXIST-*` 路径 + `audit.md ## 11. Audit Refresh Log` 追加 deprecate 行 | 弃用某既有能力 / EXIST-*但本 feature 不立即替换 | 弃用范围 + 兼容窗口（owner / 删除条件 / 验证方式 / 清理 task） |
| 5 | **Preserve** | `Relation to Existing: Depends EXIST-*` | 依赖既有不动 | EXIST-* 锚点 + 不动理由 |
| 6 | **Merge Back** | Reflection `resolution ∈ {promoted_to_invariant, distilled_to_standards, folded_into_spec, folded_into_ssot, promoted_to_ssot_patch}`（appendix §A.7.2） | 实现期发现可升入 charter §5 / .github/standards / 母本的稳定模式 | reflection ID + resolution + target 真实落点 + 用户批准（仅 folded_into_ssot / promoted_to_ssot_patch 必需） |
| 7 | **Archive Only** | active → done `git mv` + `reflections-archive.md` append-only（appendix §A.7.4） | 交付后归档但不反流全局 | feature 三条件齐 + Project Archives 条目 |

**Conflicts EXIST-*** 不是独立 delta，而是 Modify / Replace / Deprecate 的**未决前置态**：
`Conflicts` 必须有解决方向，不得只罗列矛盾；解决后落到上面 7 种之一。

**硬规则**：

- 每条 REQ / DSN / TASK 必须能标记为 7 种之一。语言是「改一下」「优化一下」「兼容一下」**不构成 delta 标记**，必须落到具体枚举。
- **Deprecate 当前是组合表达**：现有体系没有「单条 EXIST-* 锚点的弃用标记」语法，必须组合 charter §6 + Replaces 路径 + Audit Refresh Log 三处落点表达。kernel 如实记录这一点，不在 kernel 范围内修复。
- **Merge Back ≠ 自动反流**：`folded_into_ssot` 与 `promoted_to_ssot_patch` 必须用户明确批准；未批准前只能写候选（`SSOT Stewardship Suggestions` / `Repair Draft`），不得静默改母本。

---

## 5. Active / Done 迁移 · 物理边界

`<specs_root>` 默认查找顺序：`docs/specs/` → `specs/` → 都没有则**建议**在 `docs/specs/` 创建并待用户确认。

二级分仓**强制**（specs-write §1.6 + appendix §A.7.4）：

- `<specs_root>/active/<feature-slug>/`：进行中。Phase 0 必在此落地，**不得平铺**。
- `<specs_root>/done/<feature-slug>/`：已交付。三条件齐后由你在交付 PR 中执行 `git mv` 物理迁移。

**active → done 三条件齐**（缺一不可）：

1. `tasks.md ## 3. Task List` 所有 Task `Status = Done`，无 `Blocked` / `Blocked(Suspended)` 残留。
2. `<feature-slug>/artifacts/` 与所有 Task 的 `Artifacts:` 声明一致（无遗漏 / 无外溢）；项目根 `reports/` / `tmp/` / `output/` 无散落产物（散落者按 `cleanup_manifest_<date>.md` 迁移）。
3. `docs/specs/project archives/工程交付归档-YYYY-MM-DD.md` 已加 feature 级交付归档条目。

未齐三条件即迁移 → 视为越界，PR 拒合并。执行端 `/specs-execute` Phase 9 在最后一条 Task Done 时呈交清单提醒用户。

**simple-write 简写解析**：本工作流中 `docs/specs/<feature-slug>/...` 是抽象简写，物理上必解析到 `docs/specs/active/<feature-slug>/`（未交付前）或 `docs/specs/done/<feature-slug>/`（交付后），不得落平铺位置。

**artifact 落点**：spec 执行期任何 Task 产生的非源码副产物（plan / verify / cost ledger / quarantine / dry-run / 4 闸口报告 / drift 报告）必写入 `<feature-slug>/artifacts/` 或子目录，禁项目根 `reports/` / `tmp/` / `output/`。

---

## 6. Archive / Merge Back · 反流路径

**两条归档 / 反流路径，不得混用**：

### 6.1 Feature 内归档（不反流全局）

- **路径**：`docs/specs/active/<feature-slug>/reflections-archive.md` → 迁移后 `docs/specs/done/<feature-slug>/reflections-archive.md`。
- **性质**：append-only，不修改历史记录；该 feature 的「实现旁注备忘」，对其他 feature 不直接可见；**不反流为全局历史**。
- **触发**：reflection 热数据（`handoff-payload.yaml#implementation_reflections.active`）超 10 条 / 已裁决者，由写作端 Phase 0 GC 流程归档。

### 6.2 全局反流（影响后续 feature）

只有以下 5 种 resolution 进入项目级 SSOT，影响后续 feature 派生：

| Resolution | 真实落点 | 是否需用户批准 |
| ------------ | ---------- | ---------------- |
| `promoted_to_invariant` | charter.md `## 5. Architectural Invariants`（升 INV-BAN-*/ INV-LIM-* / INV-SEC-*） | Gate B 裁决 |
| `distilled_to_standards` | `.github/instructions/<主题>.md` 新增条目 | Gate B 裁决（INV-BAN-*/INV-SEC-* 候选）/ 软累计（reusable_pattern） |
| `folded_into_spec` | `requirements.md` / `design.md` 对应 ID 修订 | Gate C（Spec Breach 修订）/ AI-DRI（执行端微调） |
| `folded_into_ssot` | charter / .github/instructions / 母本对应权威章节 | **必需用户明确批准**（Authoritative SSOT 修改边界） |
| `promoted_to_ssot_patch` | `docs/specs/active/<patch-slug>/` 新建 SSOT Patch spec 或 `.github/instructions/` 新增建议草案文件 | **必需用户明确批准**（不直接改母本） |

**硬规则**：

- **同 PR 物理删除 + 追加**：Reflection 裁决归档时，必须**同 PR 从 YAML 物理删除**已裁决条目（不是改状态位），同 PR 在 `reflections-archive.md` 追加同等条目。仅变状态位 = GC 失职。
- **YAML 与 archive 不得同 ID 重复**：出现同 reflection-id 重复 → 视为 GC 失职，回滚 PR。
- **`Project Archives` ≠ `reflections-archive.md`**：`docs/specs/project archives/工程交付归档-YYYY-MM-DD.md` 只在项目交付事实部分**引用 reflection 概要 ID**（如 `REF-001 · distilled_to_standards`），不复制全文。

---

## 7. 状态机锚点表 · 防漂移锁点

本表是 kernel 与 `/specs-write` / `/specs-execute` 入口状态机的**字面对照表**，任一条漂移视为 kernel 失效，必须同 PR 修订本文。

### 7.1 /specs-write Phase（7 个）

`Phase 0 · Project Maturity & SSOT Health Intake` → `Phase 1 · Intake & Charter` → **[Hybrid/Brownfield 必走]**`Phase 1.5 · Spec Derivation Audit` → `Phase 2 · Requirements` → `Phase 3 · Design [Medium ① 可跳]` → `Phase 4 · Tasks` → `Phase 5 · Handoff`。

### 7.2 /specs-write State（12 个，§0.2.1）

`NO_HEALTHY_SSOT` / `CHARTER_READY` / `AUDIT_REQUIRED` / `EXTERNAL_AUDIT_REQUIRED` / `APPROVAL_PENDING` / `CURRENT_GATE_APPROVED` / `REQUIREMENTS_READY` / `DESIGN_READY` / `TASKS_READY` / `HANDOFF_READY` / `GATE_BLOCKED` / `BLOCKED`。报告时必须使用 workflow-qualified state，例如 `/specs-write:HANDOFF_READY`。

### 7.3 /specs-execute Phase（9 个）

`Phase 1 · Locate` → `Phase 2 · Hydrate Context` → `Phase 3 · Plan` → `Phase 4 · Red` → `Phase 5 · Green` → `Phase 6 · Refactor` → `Phase 7 · Verify` → `Phase 8 · Update tasks.md` → `Phase 9 · Handoff`（含 active→done closeout）。

### 7.4 /specs-execute State（11 个，§0.2.1）

`NO_APPROVED_SPEC` / `TASK_LOCATED` / `IN_PROGRESS` / `PAUSE_AND_ASK_PENDING` / `ENVIRONMENT_BLOCKED` / `ROLLBACK_REQUIRED` / `BLOCKED` / `SPEC_REPAIR_REQUIRED` / `TASK_DONE` / `CLOSEOUT_READY` / `CLOSEOUT_DONE`。报告时同样使用 workflow-qualified state。

### 7.5 spec 文件 Approval.Status（5 个，cross-cutting §2.1）

`Draft` / `Approved` / `Needs Changes` / `Acknowledged` / `Superseded`。AI 在 Gate N/A 时可自决 `Draft` / `Needs Changes` → `Approved`，必在 Notes 留 `AI-DRI auto-approved` 痕迹。

### 7.6 Task Status（5 个，templates/tasks.md）

`Pending` / `In Progress` / `Done` / `Blocked` / `Blocked(Suspended)`。Done 唯一门槛 = Verification / DoD 全 PASS 且无 Pause-and-Ask 未决。

### 7.7 Decision Gate（5 类，cross-cutting §2.2）

`Gate A · L-STRAT 战略级` / `Gate B · L-DESIGN 设计级` / `Gate C · Spec Breach` / `Irreversible Action` / `Anything else (L-IMPL / L-OPS) → AI-DRI 自决`。

### 7.8 Reflection kind（7 种，appendix §A.7.3）

`implementation_choice` / `new_invariant_candidate` / `reusable_pattern` / `spec_drift` / `audit_debt` / `ssot_stewardship` / `test_modified`。

### 7.9 Reflection resolution（6 种，appendix §A.7.2）

`promoted_to_invariant` / `distilled_to_standards` / `folded_into_spec` / `folded_into_ssot` / `promoted_to_ssot_patch` / `dismissed`。

### 7.10 抢占协议三档（appendix §A.6.1）

`P-INLINE`（同 Task 内紧急修补，不冻结）/ `P-SIBLING`（同 feature 跨 Task 切换，三件套保护）/ `P-CROSS`（跨 feature 临时任务，三件套保护）。嵌套 depth ≤ 2。

### 7.11 防 1-5（specs-write 入口 Companion Documents）

`防 1 SSOT 撕裂` / `防 2 TDD 作弊` / `防 3 Revert 雪崩` / `防 4 MCP 幻觉` / `防 5 注意力稀释`。跳读 Companion Documents = 违反对应防御机制。

### 7.12 三轨方法论（cross-cutting §3.5）

`ATDD 定目标` → `BDD 锁路径` → `TDD 保实现`。落点：ATDD 在 `requirements.md` AC + `tasks.md` DoD；BDD 在 `requirements.md §7` Scenario + tasks.md 引用锚点；TDD 由 `/specs-execute` Red→Green→Refactor 落地。

---

## 8. Spec 产物 · 七文件 + 二目录

feature 目录结构（active / done 同构，specs-write §1.6）：

-**`<specs_root>/active/<feature-slug>/` 或 `.../done/<feature-slug>/`**- `maturity-intake.md`：L0 · Phase 0 必产

- `charter.md`：L1 · Phase 1 必产
- `audit.md`：L2 · 仅 Hybrid/Brownfield 必产
- `audit-evidence/`：Phase 1.5 真实校验工具产出（DB/API/UI/FS 4 桶）
- `requirements.md`：L3 · Phase 2 必产
- `design.md`：L4 · Phase 3（Medium ① 可缺）
- `tasks.md`：L5 · Phase 4 必产
- `handoff-payload.yaml`：L5 · Phase 5 必产；机读 SSOT
- `artifacts/`：L6 · /specs-execute 期间副产物落点（包含 plan, verify, cost ledger 等）
- `reflections-archive.md`：L7-L8 · append-only；裁决归档**硬约束**：

- 任何 Task 产生的非源码副产物 **必落 `<feature-slug>/artifacts/` 或子目录**，禁项目根 `reports/` / `tmp/` / `output/`。
- `handoff-payload.yaml` 是机读 SSOT；`tasks.md` 顶部 Traceability Matrix 是它的人读投影，禁手改单元格（防 1）。
- `reflections-archive.md` 是 feature 内归档，**不反流为全局历史**；全局反流走 §6.2 五条 resolution 路径。

---

## 9. 反模式 · 常见错误

| 反模式 | 违反层 | 正确做法 |
| -------- | -------- | ---------- |
| 把项目当成 Greenfield，跳 Phase 1.5 直接写 requirements | L0 + L2 | 先证据化判 Mode；Hybrid / Brownfield 必走 Phase 1.5 |
| Medium 单文件省略 Charter / Design 段 | L1 + L4 | 文件可裁，语义层不可裁 |
| 「改一下」「优化一下」「兼容一下」语言 | L3 + §4 | 必落 7 种 delta operation 之一 |
| `Conflicts EXIST-*` 只罗列矛盾不给解决方向 | L2 + L3 | 必给解决方向，落到 Modify / Replace / Deprecate |
| 直接修母本 / charter §5 INV-* / .github/standards 而无用户批准 | L8 + §6.2 | folded_into_ssot / promoted_to_ssot_patch 必需用户明确批准 |
| Reflection 裁决只改 YAML 状态位，不删节点 | L7 | 同 PR 物理删除 YAML 节点 + 追加 `reflections-archive.md` |
| 三条件未齐就 active → done `git mv` | L8 | 三条件齐才迁移；未齐 PR 拒合并 |
| 写作端在 spec 里写测试代码（mock / fixture body / Jest 语法） | §7.12 | spec 只写 BDD Scenario 锚点，TDD 代码由 `/specs-execute` 落地 |
| 跳 Companion Documents `MUST read` 直接推进 Phase | §7.11 | 不读 = 违反防 1-5 |
| 报告用 `DONE` / `BLOCKED` 不带 workflow 限定 | §7.2 + §7.4 | 必须输出 `/specs-write:HANDOFF_READY` 或 `/specs-execute:TASK_DONE` 等 workflow-qualified state |

---

## 10. 上手层 · 三种典型路径速记

| 我有 | 应走 | 第一站读 |
| ------ | ------ | ---------- |
| 一个新 feature 想法（新模块 / 新页面 / 新接口 / 新数据流 / 跨模块重构 / Schema-API-协议变更 / 权限-计费-合规 / AI pipeline / Agent / 复杂 Bug） | `/specs-write` 完整流程 | `templates/maturity-intake.md` 判 Mode |
| 一个已批准 spec 的 Pending Task | `/specs-execute TASK-###` | `../../specs-execute/protocols/phase-rules.md` Phase 1 section |
| 一个错字 / 单文件小 bug / 完整代码级指令 / 纯查询 | **不启用** workflow，直接处理 | — |
| 母本 / L1 SSOT 不健康 / source 不可派生 | 先修上游 | `/project-inception` / `/grill-with-docs` / `/business-model-audit` |
| 架构摩擦 / seam / interface / 浅模块 | `/architecture-audit` | — |
| 现状不明 / 影响面未知 bug | `/bug-audit` 或 `diagnose` | — |

详细决策树后续落 `entry-decision-tree.md`，本表先服务当下。

---

## 11. 与外部 spec 体系的对照

本文做机制对照，**不复制外部目录、命令名或事实源结构**：

| 外部体系 | 外部机制 | 本体系对应 |
| --------- | --------- | ------------ |
| OpenSpec | proposal + delta specs + archive | L1 charter（含 Out of Charter）+ §4 七种 delta operation + §6 reflection / archive |
| OpenSpec | current specs vs change folders 分离 | active / done 二级分仓（§5）+ folded_into_ssot 反流路径（§6.2） |
| Spec Kit | constitution → specify → clarify → plan → tasks → implement | L0 maturity-intake + L1 charter + L2 audit + L3 requirements + L4 design + L5 tasks + L6 /specs-execute |
| Spec Kit | plan 拆 research / data-model / contracts / devex | L4 design + `<feature-slug>/artifacts/` 子目录 |

**胜出条件检查**（对应 §11 对照表）：

- **Spec 方法论本身更强**：本文显式覆盖 L0-L8 九层语义 + 七种 delta operation；外部体系大多只覆盖 L1 + L3 + L5 + L6 四层，无 L0 / L2 / L7 / L8。
- **清晰度更强**：本文压缩到一页（11 章 + 锚点表 + 反模式），不需要通读 cross-cutting / appendix / phase-rules 才能理解方法论。
- **低门槛使用更强**：§10 三种典型路径速记 + `entry-decision-tree.md` 6 判定 + `cross-cutting.md §6` 反模式查询表；新 agent 不通读全部支撑文档也能完成首个 happy-path spec。
- **成熟度 / 生态更强**：后续 `../examples/` + `../conformance-fixtures/` + `/asset-quality-gates` eval；只有真实跑通才宣称成熟，不靠覆盖面。

---

## 12. 本文与下游文档的关系

| 下游文档 | 关系 |
| ---------- | ------ |
| `../references/terminology.md` | 从本文 §7 锚点表抽取定义集；细化每个术语的字段 / 枚举 / 约束。**不重复本文事实** |
| `entry-decision-tree.md` | 从本文 §10 派生完整入口决策树；覆盖更多场景与回切路径 |
| `../examples/` | 从本文 §4 + §6 派生 5 类 canonical examples（Greenfield happy / Brownfield delta / Medium single-file / Spec repair / archive-merge） |
| `../conformance-fixtures/` | 从本文 §4 + §9 派生 pass / fail fixtures，由 `/asset-quality-gates` 与 `skill-eval` 验证 |
| `cross-cutting.md / appendix.md / phase-rules.md / templates/*` | 硬规则深度；本文是它们的入口压缩，不替代它们 |

**演进规则**：本文修订必须同 PR 修订下游受影响文档；下游文档与本文出现术语漂移 → 视为本文失效，必须先修本文再修下游。
