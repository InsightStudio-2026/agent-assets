# Specs Execute  tasks.md Schema and Reflections Contract

> **When to read**: The main workflow instructs Cascade to load this file before touching `tasks.md` traceability matrix or filling Reflections fields in Phase 8.
>
> Cross-references to `A.7.5` point back into the `/specs-write` workflow appendix.

---

## 1. Execution Notes（结构化记录模板）

Phase 8 更新 tasks.md 时，必须在目标 Task 的 `Execution Notes` 追加一条结构化记录；不得只写"已完成"。

```diff

- TASK-### @ <ISO 8601>
  - Touched:
    - <path>
  - Artifacts Generated:
    - <docs/specs/active/<feature-slug>/artifacts/...>
  - Tests: PASS <command summary> | FAIL <command summary>
  - Notes:
    - <关键实现选择 / P1 补读 / 例外豁免 / 无反流原因>

```

规则：

1. `Touched` 必须覆盖实际 diff 的源码 / 测试 / 迁移 / 脚本路径。
2. `Artifacts Generated` 必须列出本 Task 新增或更新的 artifacts 路径；无 artifacts 时写 `N/A (no artifacts generated)`。
3. `Tests` 必须逐项对应 tasks.md `Verification Commands`，不能只写"测试通过"。
4. `Notes` 必须记录任何 P1 补读、测试例外、artifact 豁免、Reflections 为 N/A 的理由。

---

## 2. Traceability Matrix（双源单写·机械化脚本单向生成·防 1 SSOT 撕裂）

追溯矩阵唯一机读 SSOT 为 `handoff-payload.yaml#traceability`；Markdown 表为投影。本 Task 完成后覆盖关系发生变动（新增 / 删除 / 修改 Task 或其 implements / design_refs / touches）时：

1. **先改 YAML**：更新 `handoff-payload.yaml` 的 `traceability` / `execution_order` / `first_task` / `revert_dependency_graph` / `implementation_reflections` 节
2. **走脚本重生 Markdown 表格**：走项目层注入的脚本槽位 `traceability_regen_script`（默认值详写端 `project-adapter.md §1`）。本步仅以 YAML 为输入，覆写 tasks.md §1 表格（首行机读标记保留）
3. **同步检查必跑**：走项目层注入的脚本槽位 `traceability_check_script`（默认值详写端 `project-adapter.md §1`）· exit code 0 = 同步 / 4 = 撞裂 / 其他 = 结构错。非 0 返回 → 不得进 Phase 9 Handoff，返回重跑 `traceability_regen_script` 后补跑 `traceability_check_script`
4. **禁止 inline patch 单行**：不允许手改表格单元格；出现错列 / 漏行 / ID 拼写错 → 视为追溯链断裂，停下跑 regen 重生后提交
5. 如发现 YAML 与 Markdown 表格已不一致 → **以 YAML 为准**重生表格并在 Execution Notes 记录冲突
6. **CI / pre-commit 必含同步检查**：项目需在 CI 与 pre-commit 中接入 `traceability_check_script` 槽位脚本，提交后 CI 报同步撕裂 → 拒合并

---

## 3. Implementation Reflections（实现反流闭环 · 必答六问）

> 本 Task 所产生的实现选择 · 新红线候选 · 可复用模式 · Spec drift · Audit Debt · SSOT Stewardship 候选，是下一轮 `/specs-write` 能否产出更准确 Spec 与更健康 SSOT 的原材料。不填 = 文档写死。本节与主 workflow 步进 8: Handoff Status / 本文 §1 Execution Notes / 本文 §2 Traceability 并列，以「向上反流」为主轴。

### 3.1 必答六问 + 一类机械触发

> **第 7 类 `test_modified` 不在必答六问中**，由 `phase-rules.md §4.2 / §5.2 / §6.1` Test Anchors hash 校验机械触发：
> 若 Phase 5 / 6 重算 hash 与 `phase-rules.md §4.2` 锁定值不一致 → 必须以 `kind: test_modified` 留痕 before/after hash + 修改原因，否则视为防 2 作弊（详 `phase-rules.md §6.1 / §7.1` Test Anchors hash 校验）。

本 Task 进入 Phase 8 Update 时，你必须逐个回答以下六个问题，答案面向 tasks.md `Reflections:` 字段与 handoff-payload `implementation_reflections:` 节：

1. **实现选择（implementation_choice）**：本 Task 中作出了哪些未在 design.md 明示、但未来同类 Task 应遵守的选择？（如 retry 包装方式 / 某 lib 的安全调用顺序 / 超时选型）→ 如有 → 写入 `kind: implementation_choice`。
2. **新红线候选（new_invariant_candidate）**：本 Task 中是否发现了某种“其实不该跨越”的边界（如“该 lib 不能在跨进程下共用 connection” / “该字段不能在 worker 池共用”）？→ 如有 → 写入 `kind: new_invariant_candidate`，`suggested_target` 默认 `charter.md#INV-LIM-NNN` 或 `charter.md#INV-SEC-NNN`。
3. **可复用模式（reusable_pattern）**：本 Task 中出现的某种工程模式（如 retry-with-backoff 包装 / token bucket / 跨 connection 初始化 套路）是否预计还会出现于不同的 ≥ 1 个其他 Task？→ 如有 → 写入 `kind: reusable_pattern`，`suggested_target` 默认 `.github/instructions/<主题>.md`。
4. **Spec drift（spec_drift）**：本 Task 实现中是否发现了 design.md 与实际可行方案的不一致（如某个 DSN 接口在实际运行时不可行 / 某个 Failure Strategy 不适用）？→ 如有 → 写入 `kind: spec_drift`，`severity` 必须评估（low / medium / high）；high 表示下轮 `/specs-write` 启动时必须处理才能推进新 feature。
5. **Audit Debt（audit_debt）**：本 Task 是否因上游 audit.md 漏掉代码入口、架构与模块、数据、真实数据库状态、契约与接口、UI、运行与部署、测试基线、依赖关系、历史约束、文档 SSOT 任一面而返工？→ 如有 → 写入 `kind: audit_debt`，并列 `missing_audit_face`（14 面之一）与应补 evidence。
   - **子场景 · Existing Touches 扩展回流**：若本 Task 因 `Existing Touches` AI-DRI 自动追加 ≥ 2 个公共契约相关文件触发（详 §3.4 硬触发第五 bullet）→ **必须**按写端 §A.7.5 schema 补填 `extension_payload` 子结构（`task` / `added_files` / `reason` / `public_contract_impact` 四字段齐备；`added_files` 不得 < 2 项；`public_contract_impact` 枚举 ∈ {none / schema / api / credential / ui}，其中 schema / api / credential / ui 凡一命中 → `severity` 升为 `high`）。未填该子结构 → 写端 §A.7.3 第 4 条阻塞规则（`kind=audit_debt + extension_payload 非空` 阻塞下轮 Phase 1 启动）会永不触发，反流链断裂。
6. **SSOT Stewardship（ssot_stewardship）**：本 Task 是否暴露出母本 / L1 SSOT / .github/instructions 在目标、术语、边界、验收、数据契约、演进路线上的可优化点？→ 如有 → 写入 `kind: ssot_stewardship`，附 `suggested_target` 与 `approval_required: yes/no`。你可以提出强推荐草案，但不得未经用户明确批准直接修改 Authoritative SSOT。

若六问皆为「无」→ 在 Reflections 字段写 `Reflections: N/A`，且在 Execution Notes 补一句「本 Task 未产生需反流的信息（机械性实现）」。

### 3.2 Reflections 字段格式（tasks.md）

```yaml
Reflections:

  - kind: implementation_choice | new_invariant_candidate | reusable_pattern | spec_drift | audit_debt | ssot_stewardship | test_modified
    summary: 「SQLite WAL 在 worker 池下必须按 connection 初始化，否则出现 lock」
    suggested_target: charter.md#INV-LIM-NNN | .github/instructions/`<file>`.md | design.md#DSN-API-002 | 母本.md#<章节> | N/A
    severity: high
    approval_required: yes | no
    raised_at: 2026-05-09T10:30:00+08:00

    # 条件化字段 · 仅 kind: test_modified 必填：
    before_sha256: <64 位十六进制 · Phase 4 `phase-rules.md §4.2` 锁定值>
    after_sha256: <64 位十六进制 · Phase 6 `phase-rules.md §6.1` Refactor 重锁后值>
    reason: "<一句：为何 Refactor 改测试 · 防 2 hash 漂移留痕>"
```

### 3.3 同步到 handoff-payload

同 PR 中同步补充 handoff-payload.yaml `implementation_reflections:` 节（跨 Task 累计；schema 以 handoff-payload.yaml 已有字段为准）。不得仅填 tasks.md 而不同步 handoff-payload；二者同步为 `/specs-write` 反流闭环的唯一信息源。

### 3.4 硬触发回切 vs 软累计

本 Task Done 后扫本轮产出的 reflection，命中以下任一条 → **不走 Phase 9 常规 Handoff**，改走 `blocking-and-rollback.md §1.3` 回切 `/specs-write` 重订 Spec；告知用户回切理由 + 对应 reflection ID：

- `kind: spec_drift` 且 `severity: high`
- `kind: audit_debt` 且 `severity ∈ {medium, high}`，或缺真实数据库面 / 文档 SSOT 面证据
- `kind: audit_debt` 且 `extension_payload` 非空（Existing Touches AI-DRI 自动追加 ≥ 2 个公共契约相关文件；`extension_payload` 必填 task / added_files / reason / public_contract_impact 四字段齐备 · 详 §3.1 第 5 问 + 写端 §A.7.5）
- `kind: ssot_stewardship` 且（`severity: high` 或 `approval_required: yes` 且不修改 Authoritative SSOT 就无法继续）—— 不静默改写 Authoritative SSOT
- `kind: new_invariant_candidate` 且 `suggested_target` 含 `INV-BAN-*` / `INV-SEC-*`（"不该跨越的绝对边界"）
- Task 失败条件化回滚（`blocking-and-rollback.md §1.1`）且原因归为"原 Spec 不可行" → 绕过 reflection 直接走 `blocking-and-rollback.md §1.3`

**软累计**（仅补入 `implementation_reflections.active`，常规走 Phase 9 Handoff；下轮 `/specs-write` 步进 1: Intake 启动时由写端裁决是否提炼）：

- `kind: audit_debt` 且 `severity: low`
- `kind: ssot_stewardship` 且 `severity ∈ {low, medium}` 且 `approval_required: no`
- `kind: new_invariant_candidate` 且 `suggested_target` 含 `INV-LIM-*` 或软红线候选
- `kind: implementation_choice` / `kind: reusable_pattern` → 任意 severity
- `kind: test_modified` → 由 `phase-rules.md §4.2 / §5.2 / §6.1` Test Anchors hash 校验机械触发；非必答六问

---
