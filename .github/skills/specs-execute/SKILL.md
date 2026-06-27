---
name: specs-execute
description: 严格遵守 /specs-write 产出的 ≤ 七文件合同（按 Project Mode / Mode 裁剪）执行单个 Task；强制懒加载子文档 + 强制复述上游锚点 + TDD Red-Green-Refactor + 不扩 scope。Use when user asks to execute a spec task, implement from specs, run TDD execution, or says 执行Task/按规格实现/TDD执行/执行合同。
argument-hint: "执行哪个 Task？"
---


# /specs-execute · 规格执行

**定位**：消费 `/specs-write` 产出的 Spec 合同，按 Task 单元一次执行一个，严守追溯链与 TDD 循环。

**边界**：只动一个 Task 范围内的代码。不改 Spec 内容（除 tasks.md 的 Status / Execution Notes）；发现 Spec 缺陷必须停下回到 `/specs-write`。

**例外**：Phase 9 closeout 是唯一允许跨 Task 的交付收尾例外，仅限 artifacts 核验、归档、active→done 迁移与下一 Task / 下一 route 提示。

**斜杠命令**：`/specs-execute`

**配对 workflow**：`/specs-write`

---

## 伴随文档 · 按需阅读

本 workflow 主体仅保留控制流骨架。详细约束 / 矩阵 / 模板 / 自检清单已抽到 `./`。每个 Phase 入口的 **MUST read**指令是硬规则——不读 = 视为违反该 Phase 防御机制。调度索引（按触发即读；短名均指本目录下的对应文件名）：

- **Phase 1-7 入口**：read `protocols/phase-rules.md` `## Phase N` 小节 → 前置检查 / 复述 / 边界 / TDD-Lock / 测试冻结 / DoD
- **专项触发 / 失败测试输入 / mitigation handoff**：read `protocols/specialized-triggers.md`（命中即读全文）→ 先看失败输出 / 触发器分类 / Red 语义选择
- **Phase 8 入口**：read `references/tasks-md-schema.md` §1 Execution Notes + §2 Traceability Matrix + §3 Reflections 必答六问
- **触发阻塞 / 回切 / 抢占**：read `protocols/blocking-and-rollback.md` §1.1-§1.6（命中即读全文）
- **每 Phase 出口自检**：read `references/self-check.md` 对应 `### {Locate / Hydrate / Plan / Red-Green-Refactor / Verify / Update} 自检`
- **写 Verification / Revert 命令前**：read `references/shell-conventions.md`（整文）
- **跨 workflow Hard-gate / DAG / Revert Graph 未明**：read `../specs-write/protocols/gate-dag-protocol.md`（HG-*/ DAG-N-* / DAG-E-*/ DAG-D-* ID 体系 + §4.2 跨 workflow 投影表 + §3 Revert Graph 与 revert_dependency_graph 继承规则）
- **全局 FATAL 级规则防线（建议阅读）**：read `.github/skills/fatal-rules-index/README.md`（高危禁止规则索引，防范严重违规风险）

跳过子文档 = 违反对应防御机制：防 1 SSOT 撕裂 / 防 2 TDD 作弊 / 防 3 Revert 雪崩 / 防 4 MCP 幻觉 / 防 5 注意力稀释。

---

## 0. 总则

### 0.1 核心原则

1. **强制复述**：执行 Task 前必读并引用 `Context Required` 锚点原文（≥ 1 句），禁凭记忆。
2. **TDD 闭环**：Red → Green → Refactor，不跳步。
3. **外科手术**：只改 `Touches` / `Existing Touches`；执行级补齐 AI-DRI 自决留痕；越界改契约必回切 `/specs-write`。
4. **Spec 优先**：发现需求/设计漏洞必停下回 `/specs-write`，不静默扩写。
5. **状态守纪**：AI 推 `Pending → In Progress → Done`；`Done` 唯一门槛 = Verification / DoD 全 PASS 且无 Pause-and-Ask 未决。
6. **每步可审计**：Execution Notes 留痕。
7. **完整输出禁令**：代码 diff 禁占位 / 截断；文件修改必须精确 edit / multi_edit 或完整 write。
8. **高质量交付压力**：主动推 Task 向可交付，但守住架构 / SSOT / 验证 / 回滚，不以赶工换债务。

## 懒加载契约

- **MUST read**: `./decision-matrix.md`
- 开始判定或执行 Phase 流程前，必须完整懒加载上述细节。

---

## 1. 阶段 1 — 任务定位（Locate）

**MUST read**`protocols/phase-rules.md`**(Phase 1 section)**before any preflight check. Skip = 视为违反前置检查纪律。

### 1.1 输入

-**显式**：`/specs-execute TASK-007`

- **暗示**："执行下一个 Task" → 选 `tasks.md` 中 Status=Pending 且依赖已 Done 的最小编号 Task
- **延续**："继续上次的任务" → 取最近一条 `In Progress` Task；若无则取下一个可执行 Task

### 1.2 前置检查（11 项硬规则 · 任一失败即停 · 详则全在子文档）

涵盖：tasks/maturity-intake/charter/requirements/design 存在 + Approval / Hybrid-Brownfield audit Depth Gate（14 面 + 两强证据面 ≥ 80% + Overall ≥ 80%）/ Seed-Greenfield Baseline 或 Greenfield Survey + Future Audit Trigger / Task 头部七项字段齐全 / Approval Notes 4 行留痕 / attention_budget_check（防 5 · P0/P1 token 上限）。

### 1.3 Intake 产出（公告非审批）

告知用户 Task ID / Status / 项目模式 / 依赖 / 待复述锚点列表 / 预计 Touches + Existing Touches / 预计 Verification 项清单。前置检查通过且未命中 Pause-and-Ask → AI-DRI 直进 Phase 2。

### 1.4 入场快照 (State Snapshot)

接单并完成前置检查后，在正式进入后续阶段前，**必须为当前工作区执行一次状态快照**（例如：`git commit -m "WIP: Pre-Task<Task-ID>Snapshot"` 或 `git stash`）。此快照是 Phase 7 三振回滚（Rollback）的物理逃生基线，未打快照严禁进入 Phase 2。

---

## 2. 阶段 2 — 上下文装配与复述

**MUST read**`protocols/phase-rules.md`**(Phase 2 section)** for Handoff Payload reading rules + 锚点失效处理. Skip = 视为违反防 5 注意力稀释防御。

### 2.1 必读锚点（上游 → 下游，顺序不得乱）

(1) `maturity-intake.md#Decision-Summary` (2) `charter.md#SRC-###` (3) `charter.md#INV-BAN-/INV-LIM-/INV-SEC-*`（涉依赖/部署/LLM/凭据/PII/跨网域/交易必读）(4) `audit.md#EXIST-REQ-/EXIST-DSN-*`（Hybrid/Brownfield）(5) `requirements.md#REQ-/AC-/US-/REQ-.S<n>` (6) `design.md#DSN-`<domain>`-###`（跨边界必复述 Failure Strategy）(7) 项目 SSOT 章节（SRC-* 指外部且本 Task 引用时）。

### 2.2 复述要求 + 锚点失效

每条锚点 ≥ 1 句原文 + Markdown `>` 块保原文 + 一句话说明本 Task 如何满足（示例详见子文档 Phase 2）。锚点失效（ID 找不到 / Superseded / EXIST-* 漂移 / `Verified By:` 超 7 天）→ **绝不脑补，绝不按语义猜**，按子文档处理路径。

---

## 3. 阶段 3 — 计划制定

**MUST read**`protocols/phase-rules.md`**(Phase 3 section)**+ `references/shell-conventions.md` 在拆步骤与写 Verification 前。

### 3.1 子步骤分解

把 Task 拆成可独立提交的有序子步骤（典型：Red 测试 X → Green for X → Red 测试 Y → Green for Y → 必要时 Refactor → 全量 Verification → 更新 tasks.md）。

### 3.2 Touches / Verification / Pause-and-Ask（详见子文档）

-**Touches 边界**：执行级补齐 AI-DRI 自决；改公共契约 / schema / API / UI / 新外部依赖 / 跨 feature → 回切

- **Verification 展开**：DB Test Isolation 三要素 / Concurrency & Lock / Migration 一致性 / Artifacts 路径
- **Pause-and-Ask 4 项**（每项 = `HG-IRREV-*` 硬闸；packet 字段 F-HG-1~8 见 `../specs-write/protocols/gate-dag-protocol.md §1.2`）：
  - `HG-IRREV-001` 生产 DB 操作（F-HG-5 必含 dry-run + backup；TTL-HG-6 单次执行不缓存；失败 → `FA-HG-4` 必停问 + 启 `/observability-incident`）
  - `HG-IRREV-002` 删除破坏（F-HG-6 必含 `Revert Command` 或不可回滚明示；命中 `RG-6` → `revert_dependency_graph` 标 `null`）
  - `HG-IRREV-003` 付费对外发布（F-HG-3 必含用户原话；失败 → `FA-HG-5` 触发 `/release-deploy` rollback）
  - `HG-IRREV-004` L-DESIGN 高风险兜底（继承 specs-write Gate B；`R-INH-2` 强制；任一未决 → 回切 `/specs-write` Phase 3）
- **低风险**（纯新增 / 仅测试 / 加性脚手架 / artifact / 私有 helper）AI-DRI 直进 Phase 4

---

## 4. 阶段 4 — 红灯阻断与用例编写（Red）

**MUST read**`protocols/phase-rules.md`**(Phase 4 section)**for Red exceptions + Constraint-Verification + TDD-Lock. Skip = 违反防 2 TDD 作弊防御。

### 4.1 测试覆盖 + 必确认失败

每个 AC ≥ 1 Acceptance Test / 每个新增改函数 ≥ 1 单测 / 每个错误路径 ≥ 1 边界测试。写完**必跑**确认失败；通过 → 测试无效，停下检查；报错（如 import）→ 修测试本身直到看到"业务断言失败"。

### 4.2 例外 + Constraint-Verification + TDD-Lock

- **跳 Red 例外**：纯文档 / 纯配置无运行时副作用 / 项目无测试基础设施且本 Task 不引入 → Execution Notes 说明
- **Constraint-Verification 型**Task 不跳 Red，Red 语义反转（详见子文档）

-**Phase 4 末必跑 TDD-Lock**（防 2）：SHA-256 → 回填 tasks.md + handoff-payload → 输出 `[TDD-Lock]` 声明；未输出 → Phase 7 拦截。**紧急热修复例外**：若任务标记为 `Emergency: true`（如 P0/P1 线上事故止血修复），可临时豁免此锁定以缩短止血用时，待事故完全止血并 Resolved 后重新校验并补齐。

---

## 5. 阶段 5 — 绿灯实现与最小够用（Green）

**MUST read**`protocols/phase-rules.md`**(Phase 5 section)**before writing code. Skip = 同时违反追溯 / 防 2 / §0.1 第 7 条。

### 5.1 最小实现 + 测试必通过

最少代码让 Red 转 Green / 不预设未来 / 不顺手改邻近 / 不引 Task 外依赖。跑 Red 确认通过 + 跑相邻确认未破坏 + 任一失败 → 修复或回滚，不得带病推进。

### 5.2 边界纪律（详见子文档 Phase 5 section）

-**追溯硬规则**：每行 diff 追到 `REQ/AC/US/REQ-S<n>` / `DSN-`<domain>`-###` / `EXIST-*`（Existing Touches 明示）/ `INV-BAN/LIM-*`（守红线）；无法追溯 → 越界，撤回或回切

- **不得静默改 SSOT 契约**：状态机 / L1-L10 / 词表 / 权限模型 / Authoritative SSOT → 回切或 Gate 批准；执行端只能提 `ssot_stewardship` 草案
- **不得违 charter §5 INV-***：不引 INV-BAN-* / 不逾 INV-LIM-*
- **artifact 落点**：必落 tasks.md `Artifacts:` 声明路径（默认 `docs/specs/<feature-slug>/artifacts/`）；项目根通用目录无豁免 → 越界

### 5.3 测试冻结 + 完整输出禁令（详见子文档 Phase 5 section）

- **测试冻结**（防 2）：Phase 5 Green 严禁改 §4.2 [TDD-Lock] 锁定文件；§5.1 后必重算 SHA-256 与 §4.2 比对，不一致 → 退 Phase 4 或走 `blocking-and-rollback.md §1`（标记为 `Emergency: true` 的紧急热修复任务可临时豁免测试冻结限制）
- **完整输出禁令**（§0.1 第 7）：禁占位 / 截断（`// ... existing code` / `# ... 不变` / `<填入>` / `<原有>` 等）；改文件仅 `edit` / `multi_edit` / `write_to_file`；提交前 `git diff` grep 上述模式均空才可进 Phase 7

---

## 6. 阶段 6 — 架构重构（必要时）

**MUST read**`protocols/phase-rules.md`**(Phase 6 section)**before modifying any test during refactor.

-**触发**：Green 引入重复 / 命名不清 / 抽象层级混乱 / 边界条件分散；无坏味道 → 跳本 Phase

- **纪律**：不引新功能 + 不改可观察行为 + 每次重构后跑全测仍 Green + 改动可追溯 REQ / DSN
- **修测试例外**（防 2 · 需同步重锁 + 留痕）：允许修（提取 fixture / 重命名）但必同步：(1) 跑全测仍 Green；(2) 重算 SHA-256 同 PR 更新 tasks.md `Test Anchors` + handoff-payload `first_task.test_anchors`；(3) `Reflections: kind: test_modified` 留【before_sha256 / after_sha256 / reason】；(4) 未同步 → §7 视为作弊拦截

---

## 7. 阶段 7 — 运行验证

**MUST read**`protocols/phase-rules.md`**(Phase 7 section)**for DoD + 全部条件化检查门。Skip = 违反所有 Verify 防御。

### 7.1 本地验证命令

逐条执行 tasks.md Task 的 `Verification Commands`，记录命令 + 结果（schema drift / 单测 / 手工 smoke 逐条标 PASS）。

### 7.2 DoD 三闭环 + 条件化检查门（详则全在子文档 Phase 7 section）

-**三闭环必检**：ATDD（AC 有 Acceptance Test 路径）/ BDD（US 有 Scenario 覆盖）/ TDD（Verification Commands 单测 PASS）

- **条件化门**：Secret-scan / Migration / Test Anchors / Failure readback / Artifacts / type drift / regression；命中即按子文档跑，失败不得 Done。

### 7.3 失败与三振回滚 (Three-strike Rollback)

- **单/双次失败**：不得标 `Done`；Execution Notes 记录详情；Status 留 `In Progress` 或改 `Blocked`，返回 Phase 4/5 进行修复。
- **三振出局 (物理熔断)**：若在 TDD 循环中连续尝试 3 次验证（测试/运行）均告失败，严禁继续死磕，以防由于焦躁而不知不觉拆碎底层通用架构。你**必须立即执行 `git reset --hard HEAD`（或恢复 stash）回滚到 1.4 节建立的入场快照点**，丢弃本次脏修复，并将控制权连同失败日志交还给用户或 Steward 重新决策（报告 `SE_Verify 触发三次失败熔断`）。

---

## 8. 阶段 8 — 更新任务状态（tasks.md）

**MUST read**`references/tasks-md-schema.md`**§1 Execution Notes + §2 Traceability Matrix + §3 Reflections**before updating. Skip = 违反防 1 + 反流闭环断裂。

### 8.1 Status + Execution Notes

Status：全 Verification PASS + 无 Pause-and-Ask 未决 → `Done`；部分失败可继续 → `In Progress`；阻塞 → `Blocked`。AI**不得**在未全 PASS 时自行标 `Done`。Execution Notes 结构化记录（时间戳 / Touched / Artifacts Generated / Tests / Notes，模板见子文档）。

### 8.2 Traceability Matrix（防 1 SSOT 撕裂 · 详见 `tasks-md-schema.md §2`）

唯一机读 SSOT = `handoff-payload.yaml#traceability`，Markdown 表为投影。流程：(1) 先改 YAML；(2) 跑 `traceability_regen_script` 覆写 tasks.md §1 表；(3) 跑 `traceability_check_script`，exit 0=同步 / 4=撞裂 / 其他=结构错，非 0 拒进 Phase 9；(4) 禁手改单元格。

### 8.3 完成简报 + Git 边界

汇报"Task Done + 待 commit"：全 PASS 且无白名单未决 → AI-DRI 直标 `Done`；用户"提交" → 建议并执行 commit（**不自动**）；用户"还有问题" → 回 Phase 4/5/6 或走 `blocking-and-rollback.md §1.3` 回切。

### 8.4 Reflections（反流闭环 · 必答六问 · 详则全在 `tasks-md-schema.md §3`）

写入 tasks.md `Reflections:` + handoff-payload `implementation_reflections:`，逐一回答六类：`implementation_choice` / `new_invariant_candidate` / `reusable_pattern` / `spec_drift` / `audit_debt` / `ssot_stewardship`；皆无才写 `N/A`。硬回切：high spec_drift / medium+ audit_debt / ssot_stewardship approval_required / new INV-BAN/SEC / 原 Spec 不可行。

---

## 9. 阶段 9 — 完工收口与交付

完成 / 阻塞报告输出：

```markdown
## 规格执行报告 (Specs Execute Report)

## 工作流状态 (Workflow State)

- State: /specs-execute:<STATE>; common examples: /specs-execute:TASK_DONE | /specs-execute:CLOSEOUT_DONE | /specs-execute:BLOCKED | /specs-execute:SPEC_REPAIR_REQUIRED | /specs-execute:ENVIRONMENT_BLOCKED

## 执行结论 (Outcome)

- <Task done | Closeout done | Blocked | Spec repair required | Rollback required | Environment blocked>

## 权威信息与事实源 (Authority / Fact Source)

- 关联规格 (Spec contract): <path>
- 任务授权依据 (Task authority): <tasks.md Status / Execution Notes>
- 交接授权文件 (Handoff authority): <handoff-payload.yaml>
- 验证证据 (Verification evidence): <commands / artifacts>

## 授权边界 (Authorization Boundary)

- 路由动作 (Route Action): <CONTINUE_IN_WORKFLOW | WAIT_FOR_USER | REPORT_AND_STOP | CONFIRMED_ACTION>
- 授权范围 (Authorized scope): <current Task ID + allowed Touches / Execution Notes update / approved local revert if any>
- 未授权范围 (Not authorized): <spec edits / other Task execution / unapproved rollback / real-world side effects / downstream workflow execution>

## 任务与可溯源性 (Task / Traceability)

- 任务 ID (Task ID):
- 实现需求 REQ-AC (Implements REQ-AC):
- 关联设计 DSN (Design refs):

## 代码变更与功能验证 (Changes / Verification)

- 触碰文件与差异统计 (Touched + diff stats):
- 验证状态 (Verification status):
- 状态流转统计 (Status transition):

## 推荐下一步路由 (Next Route)

- <next executable Task ID | /specs-write | /project-steward | N/A>

```

**全 Task Done 交付收尾**：核验 `<feature-slug>/artifacts/` 与所有 `Artifacts:` 声明一致（无遗漏 / 无外溢）→ 项目根 `reports/` / `tmp/` 等无散落（散落 → 生成 `cleanup_manifest_<date>.md`）→ **自动刷新并验证 Frontmatter 物理完整性**（运行 `powershell -ExecutionPolicy Bypass -File .\verify-completeness.ps1 -Update` 以自动对齐物理统计，若有报错则拒绝收尾）→ **active → done 物理迁移**（三条件齐：所有 Status=Done + Artifacts 核验 PASS + delivery-log.md 已追加记录 → 交付 PR 中 `git mv docs/specs/active/<slug>/ docs/specs/done/<slug>/`；未齐 → PR 拒合并）→ `/specs-execute:CLOSEOUT_DONE`。Spec 缺陷 → 提示回切 `/specs-write`。

---

## 10. 阻塞 / 回切 / 回滚 / 抢占 · 见子文档

**MUST read**`protocols/blocking-and-rollback.md` 当命中任一触发即读全文。Skip = 视为绕道继续干。触发关键词：

-**§1.1 Task 失败条件化回滚**— Phase 5/6 不可恢复错误（`Revert Command` 优先 / 否则按 `revert_dependency_graph` 拓扑）；触发 `S-HG-9 GATE_FAILED`；`DAG-E-RBK` 激活 `DAG-N-ROLLBACK-TASK-{Task ID}`（详 `../specs-write/protocols/gate-dag-protocol.md §3.2 RG-1~3`）
-**§1.2 阻塞**— 上游 Spec / maturity-intake / audit 缺失 / Context 锚点失效 / Touches 越界（公共契约 / schema / API / UI / 跨 feature）/ 测试环境 / 真实 DB 不可达；需操作真实生产 DB → 升级装配 `HG-IRREV-001` packet。Touches 越界 → 可能触发 `R-RETURN-2`。
-**§1.3 回切 `/specs-write`** — 需求漏洞 / 设计冲突 / Audit Debt / SSOT 不健康 / EXIST-* 漂移 / 需修 Authoritative SSOT；状态映射 `R-RETURN-1~5`（详 `../specs-write/protocols/entry-decision-tree.md §7.6`）

- **§1.5 Conditional Revert**— 共享文件冲突 → `revert_dependency_graph` 求交集 + `git diff --quiet` 预检；命中 `B-015`（`../specs-write/references/cross-cutting.md §6` 防 3 Revert 雪崩）→ `RG-3` 必走

-**§1.6 抢占式中断** — P-INLINE / P-SIBLING / P-CROSS 三档 + Suspend / Resume 三件套 + 嵌套 depth ≤ 2；连续 P-CROSS → 必停问用户（`R-PREEMPT-3` 末条）

---

## 11. 禁用行为（范围红线）

(1) 不改 Spec 文档（除 tasks.md Status / Execution Notes）(2) 不跨 Task (3) 不静默扩展（每行 diff 追 REQ/DSN/EXIST-*/INV-*）(4) 不跳 TDD（除 §4.2 例外）(5) 不绕 Verification 标 Done（全 PASS + 无 Pause-and-Ask 未决才 Done）(6) 不自动 commit (7) 不输出截断/占位（§0.1 第 7 + §5.3）(8) 不违 charter §5 INV-* (9) 不污染项目根（输出落 `<feature-slug>/artifacts/`）

---

## 12. 自检 · 见子文档

每 Phase 出口 **MUST read and tick**`references/self-check.md` 对应清单：Phase 1→Locate / Phase 2→Hydrate / Phase 3→Plan / Phase 4-6→Red-Green-Refactor（合并）/ Phase 7→Verify / Phase 8→Update。不读 / 不勾 / 跳项 → 拒进下一 Phase。

---

## 13. Shell 运行纪律**MUST read** `references/shell-conventions.md` before authoring Verification / Revert 命令。核心：PowerShell 全英文 + `Set-Content -Encoding UTF8` + 不用 `&&` + `cd` 走 cwd 参数 + `$LASTEXITCODE` 显式判；bash/zsh 项目层覆盖时写等价命令；跨 shell 通用要求 = 可复现 + exit code 可机读 + 输出落 `<feature-slug>/artifacts/`

---

## 14. 使用示例

用户：`/specs-execute TASK-###`。AI 依次走 Locate → Hydrate → Plan → Red → Green → Refactor → Verify → Update → Handoff；每 Phase 开头按 §Companion 读子文档，结尾按 §12 勾自检。Phase 1 Locate 输出格式 + 完整示例详见 `protocols/phase-rules.md` Phase 1 section。

## 支撑资源

- [blocking-and-rollback.md](./protocols/blocking-and-rollback.md)
- [decision-matrix.md](./references/decision-matrix.md)
- [phase-rules.md](./protocols/phase-rules.md)
- [self-check.md](./references/self-check.md)
- [shell-conventions.md](./references/shell-conventions.md)
- [specialized-triggers.md](./protocols/specialized-triggers.md)
- [tasks-md-schema.md](./references/tasks-md-schema.md)
