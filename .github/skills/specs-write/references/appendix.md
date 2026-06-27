# 附录 · 高级防线（A.1-A.7.5）

> **When to read**: 在 `/specs-write` 需要防 1-5 横切防御、抢占式中断协议、Reflections 反流或归档规则时读取对应小节。

---

## A.1 防 1 · Traceability 双源单写

**问题**：tasks.md 顶部 Traceability Matrix 与 handoff-payload.yaml `traceability` 节同语义双源，AI 多轮编辑易漂移。

**解法**：

1. **唯一事实源**：`handoff-payload.yaml#traceability` 为 SSOT；Markdown 表格通过 `traceability_regen_script`（`project-adapter.md §1`）重生。
2. **写作端必产字段**：
   - `tasks.md` 顶部表格上方加 HTML 注释 `<!-- generated-from: handoff-payload.yaml#traceability -->`
   - `handoff-payload.yaml#traceability.tasks[]` 枚举全量 Task，每条 Task 必产 **8 键**：`id / implements / design_refs / derived_from_existing / anti_invariants / bdd_scenarios_owned / touches / artifacts`。其中 `touches` 是防 3 `revert_dependency_graph` 求交集输入源——**不投影到 Markdown 表格**，仅留在 YAML 供机读。其余 7 键投影到表格的 7 列：Task / Implements / Design Refs / Existing / Anti-Invariants / BDD Scenarios Owned / Artifacts；`id` 通过 `Task` 列承载（即 `Task` 列的值就是 `id`）。可空字段使用 `[]` 显式声明而非缺省。
   - **Artifacts 列投影规则**（防 1 同步检查脚本判定依据）：Markdown 表格 `Artifacts` 列展示该 Task `artifacts[]` 中 **`kind=planner_output`**那条（也称"主产物锚点"，每 Task 唯一；不存在时退而展示 `kind=verify_report` 那条）的 `path` 字段；其余 kind（`cost_ledger` / `quarantine_samples` / `verify_report` 在 planner_output 已选时）不投影到表格，仅保留在 YAML 中。`traceability_regen_script`（`project-adapter.md §1`）按本规则展开，`traceability_check_script` 按本规则比对——任何脚本实现偏离本规则即视为 §A.1 SSOT 投影违规。

3.**禁止手改 Markdown 单元格**：发现漂移 → 走 `traceability_regen_script` 重生。

1. **同步检查**：`traceability_check_script`（`project-adapter.md §1` 槽位）独立于 regen 仅做对照；返回非 0 视为撞裂或结构错，需跑 regen 重生后再提交。

**反模式**：

- ❌ 在 tasks.md 顶部表格手动加一行 Task，未同步 YAML → AI-DRI 自查必失败
- ❌ YAML `traceability.tasks` 缺某 Task，但 Markdown 表格有 → 视为 Markdown 反向手改
- ❌ CI 只跑 regen 不跑 check → 漂移不会被拦截

---

## A.2 防 2 · BDD 场景所有权 + Test Anchors 唯一性

**问题**：BDD Scenario 多 Task 共享所有权、测试文件路径漂移、Phase 4 Red 后 sha256 锁定失败。

**解法**：

1. **Scenario 单一所有权**：每条 BDD Scenario 仅出现在一个 Task 的 `BDD Scenarios Owned` 列；多 Task 共享同一 Scenario = 失格，必须拆 Scenario。
2. **写作端必产字段**：每个 Task 的 `Test Anchors:` 至少 1 条（除纯文档 / 纯配置 Task），格式：

   ```yaml
   Test Anchors:

     - path: tests/test_order_create.py
       sha256: <Phase 4 Red 后补>
       bdd_scenarios:
         - requirements.md#REQ-001.S1

   ```

3. **sha256 占位**：spec 阶段 `sha256:` 填占位字符串；hash 计算 / 校验 / 重锁由执行端 `phase-rules.md §4.2 / §5.2 / §6.1 / §7.1` 处理。
4. **校验工具**：`bdd_owner_diff_script`（`project-adapter.md §1`）扫所有 Task 的 `BDD Scenarios Owned`，发现重复 → fail。
5. **Constraint-Verification 型 Task**：当 Task 的 `Verification` 是 grep / lint / drift 脚本 / migration apply 等"无单元测试"形式时，`Test Anchors` 改指脚本路径，sha256 锁定脚本本身；Phase 4 Red 语义 = 脚本先失败，Phase 5 Green = 脚本通过。

**反模式**：

- ❌ TASK-001 与 TASK-002 都列了 `REQ-001.S1`
- ❌ Test Anchors 给路径但无 BDD Scenario 绑定 → 失去防 2 闭环

---

## A.3 防 3 · Revert Conflict Risk（共享文件冲突可视化）

**问题**：多 Task 触动同一既有文件，单 Task `Revert Command` 直接执行会回滚其他已 Done Task 的修改。

**解法**：

1. **写作端必产字段**：填了非 N/A `Revert Command` 且与先行 Done Task 共享 `Existing Touches` 者，必须填：

   ```yaml
   Revert Conflict Risk:
     shared_with: [TASK-000]
     shared_files:

       - backend/models/order.py

   ```

2. **首个 Task / 无共享**：填 `N/A (no shared files with prior Done tasks)`，不得留空。
3. **`revert_dependency_graph_script`（`project-adapter.md §1`）**：根据全量 Task 的 `Existing Touches` 构建有向依赖图；执行端在 Revert 前先跑此脚本，列出受影响的下游 Task。
4. **handoff-payload `revert_dependency_graph` 节**：从 `traceability.touches` 起手求交集（详 `cross-cutting.md §4.2`），供执行端 `blocking-and-rollback.md §1.5` Revert 预检消费。

**反模式**：

- ❌ Revert Command 填了具体命令但 Revert Conflict Risk 留空
- ❌ shared_with 写了 TASK ID 但 shared_files 留空

---

## A.4 防 4 · Audit Evidence 工具原文外置（DB / API / UI / FS 真实校验）

**问题**：audit.md 中 EXIST-* 类条目被"看起来是"式判断填充；原文长 dump 塞进 spec 导致后续不可索引；evidence 用纯文字描述无法判断 AI 是否真去跑过工具。

**三铁律**：

1. **必跑工具**：DB / API / UI / FS 类 EXIST 必须用真实校验工具，按类型分发：
   - **DB**：PostgreSQL MCP / SQLite MCP / `psql -c '\d+'`
   - **API**：`curl` / `httpx` / OpenAPI fetch（不只 grep router 代码）
   - **UI**：Playwright snapshot / Storybook render / 视觉对照（不只 grep JSX 文本）
   - **FS**：`Get-ChildItem -Recurse` / `find` / `tree`（带文件 size + mtime）
2. **原文外置**：evidence 必须写入 `evidence_dir`（`project-adapter.md §1`，例 `audit-evidence/EXIST-DSN-`<domain>`-###.txt`），audit.md 仅留 1–2 句 `interpretation` + evidence_file 路径。
3. **4 桶分类**：每个 evidence_file 首行必须含 `# tool=<...> ; cmd=<...> ; ts=<ISO 8601> ; bucket=<actual_state|env_error|permission|not_found>`，确保 AI 不能用"环境问题"/"权限不足"/"未找到"等四类失败假装"已验证"。

**写作端必产字段**（详 `templates/audit.md`）：

```yaml
Verified By:
  tool: PostgreSQL-MCP   # 或 curl / Playwright / Get-ChildItem
  command: "SELECT column_name, data_type FROM information_schema.columns WHERE table_name='orders'"
  evidence_file: audit-evidence/EXIST-DSN-DB-003.txt
  interpretation: "orders 表当前 13 列；status 字段是 varchar(32) 非 enum，与 SSOT 状态机口径不一致"
```

**反模式**：

- ❌ `Verified By: 已检查代码` → tool 缺失
- ❌ evidence_file 首行无 4 桶分类 → 视为伪验证
- ❌ audit.md 中超 2 句原文 dump → 拒交付，外置到 evidence_file
- ❌ bucket=permission / env_error 但 interpretation 写 "已验证不存在" → 协议违规

---

## A.5 防 5 · Context Required + Anti-Invariants 反向追溯

**问题**：执行端 Hydrate 每个 Task 加载 SSOT / charter / audit / design 全量上下文导致 attention_budget 爆炸；某些 INV-* 在 design 列出但 Task 不知道自己应该规避哪条。

**解法**：

1. **写作端必产字段**（每个 Task）：
   - `Context Required Before Execution:`（P0 Essential ≤ 5 条；跨边界 / 动凭据 Task ≤ 7 条）
   - `Anti-Invariants:`（charter §5 中本 Task 严禁违反的 INV-* 列表）
2. **P0 / P1 严格二分**：
   - P0 Essential：执行端 Hydrate 必逐条复述原文 ≥ 1 句；跨边界 Task 必含适用 INV-* + Failure Strategy + Concurrency & Lock
   - P1 Reference：备查；执行端 attention_budget 超限时可不入初轮 Prompt，仅按需拉取
3. **P0 超上限 = 拆 Task 信号**：超 5 条（跨边界 / 动凭据超 7 条） → 该 Task 裁切不够细，必须回 Phase 4 拆分。
4. **反向追溯**：`inv_violation_check_script`（`project-adapter.md §1`）静态扫每个 Task 的 `Touches / Existing Touches` 是否触及 `Anti-Invariants` 中 INV-* 适用 scope；命中 → fail。

**写作端必产字段示例**（详 `templates/tasks.md`）：

```yaml
Anti-Invariants:

  - INV-LIM-001 (charter.md §5 复述: "单 Task 触动文件 ≤ 8 个")
  - INV-SEC-001 (charter.md §5 复述: "凭据不得 inline 进源码或日志")

Context Required Before Execution:
  P0 Essential:    # ≤ 5 条 / 跨边界 / 动凭据 ≤ 7 条

    - design.md#DSN-API-001 (request schema 全文复述)
    - charter.md#INV-SEC-001 (复述: 凭据从 KMS / Vault / keyring 读取)
    - design.md#DSN-API-001 Failure Strategy (复述: 超时=... · 进程崩溃=... · 数据层错误=...)
    - design.md#DSN-API-001 Concurrency & Lock (复述: ...)
  P1 Reference:
    - SRC-002#<章节>
    - audit.md#EXIST-DSN-DB-003
    - design.md#DSN-DB-002 Migration Strategy

```

1. **Failure Strategy 必产**：`design.md` 中所有跨边界 DSN 的 `Failure Strategy` 三类故障四元素（检测信号 / 重试策略 / 用户可见最终态 / 补偿事件）必须齐全；缺一即 design 不可 Approved。执行端 Phase 7 据此跑 readback。

**反模式**：

- ❌ P0 列了 8 条但 Task 不是跨边界 / 动凭据类 → 拆 Task
- ❌ P0 只写 ref 不写 excerpt → 失去防 5 复述功能
- ❌ Anti-Invariants 留空（即使 Task 真的不触及任何 INV-*） → 必须显式写 `none (no applicable INV-* in scope)`
- ❌ Phase 7 Verify 只跑测试 / lint，不复述 critical_contracts failure_strategy + 不给 `<file>:<line>` 错点 → 防 5 闭环失败

---

## A.6 抢占式中断协议（Preemption Protocol）

### A.6.1 三类抢占

| 类型 | 触发场景 | 存档粒度 |
| ------ | ---------- | ---------- |
| **P-INLINE** | Task 内插补（修一个 import typo 才能跑测试） | 详 `blocking-and-rollback.md §1.6.1` |
| **P-SIBLING** | 同 feature 跨 Task 切换（用户改主意先做 TASK-003） | 详 `blocking-and-rollback.md §1.6.1` |
| **P-CROSS** | 跨 feature / 全新临时任务（线上 P0 bug） | 详 `blocking-and-rollback.md §1.6.1` |

### A.6.2 现场保护三件套（执行端约定）

>**仅 P-SIBLING / P-CROSS 走以下三件套**；P-INLINE 例外（不冻结、不写 `suspended_state`，直接走 `/specs-execute` Refactor 路径处理紧急修补）。

1. **Freeze wip commit**：当前修改全量 wip commit（具体方案见下方 `Resume Strategy`）。
2. **Snapshot `suspended_state`**：在 `handoff-payload.yaml` 新增 `suspended_state` 节（`cross-cutting.md §4.2` schema），含 `wip_commit_sha` / `resume_anchor.phase` / `test_anchors_locked_at` / `interrupt_type` 等字段。
3. **Status Blocked(Suspended)**：本 Task `Status` 改 `Blocked(Suspended)`，并在 tasks.md 留时间戳注脚。

**写作端必产字段 · `Resume Strategy`**（每个 Task 头部 · 条件化 · 详 `task-rules.md §1`）：

存档方案二选一，由执行端按 `tasks_completed_count_at_pause` 决定：

- `lightweight_wip_commit`：Touches < 5 条 / 同模块 / Pause 前 ≤ 1 Task Done → `git add -A && git commit -m "wip(TASK-###): suspend at Phase<n> for<reason>"`；恢复时 `git reset --soft <wip_commit_sha>`（解开 wip commit 回到中断那一刻的 working tree）。轻量、适合小修小补。
- `wip_branch_reset`：Touches ≥ 5 条 / 跨模块 / Pause 前 ≥ 2 Task Done → 把 WIP 提到 `wip/<feature-slug>/<task-id>` 分支并切回主线 reset；恢复时 cherry-pick 或重启。重量、防回滚链塌。

**禁用 `git stash`**：stash 会漏 `audit-evidence/` 的 untracked 文件 + 未跟踪的 migration / wip artifacts（防 4 evidence 与防 3 revert_dependency_graph 共享文件双链），故本协议**不允许 stash 模式**；轻档与重档均走 wip commit 路径（与执行端 `blocking-and-rollback.md §1.6.2` [Freeze] 命令一致）。

```yaml
Resume Strategy:
  mode: lightweight_wip_commit | wip_branch_reset
  threshold:
    tasks_completed_count_at_pause: <数字 · 由执行端 Pause 时填>
```

具体 `git` 命令、wip 分支命名空间、Restore / Resume 命令分流详 `blocking-and-rollback.md §1.6.2 [Freeze] / §1.6.3 [Restore]`。

### A.6.3 Resume 三件套（执行端约定）

1. **Locate**：执行端 Locate 阶段优先读 `handoff-payload.yaml#suspended_state` 而不是常规 Phase 1 Intake——抢占恢复必走"快速接力"路径。详 `blocking-and-rollback.md §1.6.3 [Locate]`。
2. **Restore**：按 `Resume Strategy.mode` 分流恢复工作树（`lightweight_wip_commit` / `wip_branch_reset` 两路径）；恢复后必校验 Test Anchors hash 与 `suspended_state.test_anchors_locked_at` 时刻锁定值对照。详 `blocking-and-rollback.md §1.6.3 [Restore]`。
3. **Resume**：从 `suspended_state.resume_anchor.phase` 接力到原 Task 流；同步删除 `suspended_state` 节（§A.6.4 生命周期硬约束）。详 `blocking-and-rollback.md §1.6.3 [Resume]`。

### A.6.4 中断栈规则

- **depth ≤ 2**（即最多嵌套 1 层）：超过即视为项目失控。
- **P-CROSS 禁连续**：连续 P-CROSS = 紧急 bug 风暴或战略不明，必须停下让用户介入。
- **嵌套必同类型或更轻**：
  - **P-CROSS 内允许嵌 P-SIBLING / P-INLINE**，但不得再嵌 P-CROSS（同档自嵌套违禁）。
  - **P-SIBLING 内只允许嵌 P-INLINE**，**不得再嵌 P-SIBLING**（同档自嵌套违禁）；同档需求出现时按执行端 `blocking-and-rollback.md §1.6.4` 处置（先把外层 Resume 或转 Blocked）。
  - **P-INLINE 内允许再嵌 P-INLINE**（同档自嵌套合法 · 仅 P-INLINE 例外）。
  - **禁止"轻档抢占嵌重档"**：P-SIBLING 内冒出 P-CROSS 时必须先 Resume P-SIBLING 或将其转为 Blocked 后再走 P-CROSS。
  - **设计意图**：仅 P-INLINE 允许同档自嵌套，因其不冻结现场、不消耗 `suspended_state` 栈帧；P-SIBLING / P-CROSS 自嵌套会同时占用两份 `suspended_state` 但 schema 仅有 `depth` 标量、无嵌套结构，且抢占现场保护成本（wip commit / wip branch / payload snapshot）不便宜，故不允许。
- **`suspended_state` 生命周期**：仅在 Suspend 期间存在；Resume 时**物理删除**该节（参照 §A.7 Reflections GC 哲学，仅变状态位 = 失职）。
- **`test_anchors_locked_at` 字段**：跨中断 §A.2 hash 校验的免责锚点；缺失 → 视为非法中断现场，Resume 时必须先补 hash 重锁。

### A.6.5 与防 1–5 衔接

- Resume 后必跑 §A.1 `traceability_check_script` 同步检查（中断期间可能有 YAML / Markdown 不一致）。
- Refresh §A.4 audit evidence 7 天有效期：Resume 时刻发现 evidence 超期 → 进入 **Audit Refresh 子流程**（限于被超期 evidence 覆盖的 EXIST-*重跑 §A.4 4 项验证 + 重判 Audit Depth Gate）；本子流程**不开新中断栈帧**，不升级为 P-CROSS；全面超期或出现新 conflict 才回 Phase 1.5 重走。「全面超期」判定标准：（a）多个 EXIST-* 同时超期且 readback 与原 interpretation 冲突；（b）Audit Refresh 中发现新出现的 SSOT / DB / API conflict；（c）**中断时长 > 30 天**作为全面超期的强证据（执行端在 Execution Notes 记 `evidence_freshness=stale-30d` 后回切）。仅 (a)/(b)/(c) 全不命中且 evidence 仅部分超期 → 子流程重跑后可直接续后续 Phase，不需机械回切。
- `wip_commit_sha` 纳入 §A.3 `revert_dependency_graph` 输入，避免抢占恢复后 Revert 命中 wip 提交。
- §A.5 `Context Required` 必含 `suspended_state.resume_anchor` 锚点（Resume 时执行端必复述）。

**反模式**：

- ❌ P-INLINE 也写 `suspended_state` → 把轻量插补复杂化
- ❌ 连续 P-CROSS 不停下问用户 → 协议违规
- ❌ Resume 后不删 `suspended_state` 节 → §A.7 GC 哲学违规
- ❌ `Resume Strategy.mode` 留空且执行端"任意选"（即未依据本节阈值表自动判档） → 应在 Pause 时填入阈值由协议决定；留空交由 `blocking-and-rollback.md §1.6.2` 按阈值表自动判档不算违规（自动判档落败 → 停下问用户）
- ❌ 使用 `git stash` 模式存档抢占现场 → 会吞掉 `audit-evidence/` 与 wip artifacts（防 3 + 防 4 双线断裂），本协议明确禁用；轻档走 `lightweight_wip_commit`，重档走 `wip_branch_reset`

---

## A.7 Implementation Reflections（执行端→写作端反馈链）

**问题**：执行端在 Phase 5 / 6 / 7 发现的实现选择、新候选 INV-*、可复用模式、spec drift、audit debt、SSOT 改进建议，没有结构化通道回流到 spec / charter / SSOT；多个 feature 重复踩同坑。

**契约**：

1. **热数据存放**：`handoff-payload.yaml#implementation_reflections.active`（详 `cross-cutting.md §4.2` schema）；上限 10 条。
2. **冷数据归档**：超上限 / 已裁决者走 `reflection_archive_script`（`project-adapter.md §1`）归档到 `docs/specs/<feature-slug>/reflections-archive.md`。
3. **kind 枚举**：
   - `implementation_choice`：实现期选了某方案，记录权衡
   - `new_invariant_candidate`：发现一条可升格为 charter §5 INV-* 的项目级红线
   - `reusable_pattern`：可抽到 `.github/instructions/` 的通用模式
   - `spec_drift`：实现与 spec 不一致（执行端选择就地适配 vs 回写 spec 的判断）
   - `audit_debt`：Phase 1.5 漏审的现状，事后补
   - `ssot_stewardship`：发现 SSOT 健康风险 / 改进建议，建议 SSOT Patch
   - `test_modified`：防 2 TDD 作弊检测专用（详 §A.2 与本节 kind 枚举），**必填三个条件化字段 `before_sha256` / `after_sha256` / `reason`**（详 `cross-cutting.md §4.2` schema implementation_reflections.active[] 条件化扩展）；summary 可补一句人读说明；豁免于 Gate 裁决，但需被§A.7 GC 归档；三字段任一缺失 = 防 2 机读自检脚本不予认可
4. **severity 枚举**：low / medium / high
5. **裁决入口**：写作端 Phase 0 必读 `implementation_reflections.active`：
   - `severity: high` 且 `kind: spec_drift` → 阻塞新 feature 启动 Phase 1，必须先回写 spec / charter
   - `kind: new_invariant_candidate` → 走 Gate B 决定是否升格 INV-*
   - `kind: ssot_stewardship` → 走 Gate A/B 决定是否回流 SSOT
   - `kind: reusable_pattern` → 决定是否抽到 `.github/instructions/`
   - `kind: audit_debt` →
     - `severity: medium / high`：回 Phase 1.5 按 reflection 中 `missing_audit_face`（14 面之一）重跑该面的真实校验工具（DB/API/UI/FS 类需走 §A.4 4 项 + audit-evidence/ 4 桶分类），补 EXIST-* 锚点并重过 Audit Depth Gate；Approved 后才能续写下游 / 启动新 feature；归档 `resolution=folded_into_spec`，`target` 指向 `audit.md#EXIST-*` 新增锚点。
     - `severity: low`：在下一轮 Phase 0 启动新 feature 前，于 audit.md 末尾的 `## 11. Audit Refresh Log` 节追加一行记录即可（详 `templates/audit.md §11`），不必重跑 Audit Depth Gate；归档 `resolution=folded_into_spec`，`target` 指向 `audit.md#Audit-Refresh-Log`。
   - `kind: audit_debt` 且 `extension_payload` 非空（详 §A.7.5 Existing Touches 扩展回流） → 回 Phase 1.5 按 `extension_payload.added_files` 补对应 EXIST-* + 回 Phase 4 更新对应 Task 的 `Existing Touches` 字段；Approved 后续推进。
6. **raw_path**：每条 reflection 必有 `<feature-slug>/reflections/REF-###.md` 原文（执行端写入）；写作端只读、裁决、归档。

### A.7.1 GC 前置检查 · `suspended_state` 残留扫描

写作端 Phase 0 在读 `implementation_reflections` 之前**必须先**扫描 `handoff-payload.yaml` 是否存在 `suspended_state` 节。**存在即阻塞 GC**——意味着上一轮 feature 的某 Task 仍处于 Preemption-Suspend 状态未 Resume（详 §A.6）。

处置：

- **(a) 该 feature 实际已 Done**→ 视为执行端 Resume 漏删，停下追问用户后手动从 YAML 删除 `suspended_state` 节点；

-**(b) 该 feature 未 Done** → 不得启动新 feature 的 Phase 1，建议先回该 feature 走 `/specs-execute` 完成 Resume + 后续 Task。

本步骤先于读取 `implementation_reflections`，避免在抢占未关闭的状态下推进新 feature 拉垮反思裁决。

### A.7.2 reflections-archive.md 文件模板

冷数据归档目标文件：`docs/specs/<feature-slug>/reflections-archive.md`，**append-only**，不修改历史记录。模板：

```markdown
## Implementation Reflections Archive — <feature-slug>

> 本文件是 `handoff-payload.yaml#implementation_reflections` 的**归档**，与热数据区构成双轨。
> 热数据区里的反思经写作端 Phase 0 裁决后，同 PR 从 YAML 物理删除 + 补入本文件。
> 本文件只追加（append-only），不修改历史记录。

---

## <reflection-id> · raised_at: <ISO 8601> · resolved_at: <ISO 8601>

- task_id: TASK-001
- kind: implementation_choice | new_invariant_candidate | reusable_pattern | spec_drift | audit_debt | ssot_stewardship | test_modified
- severity: low | medium | high
- summary: <1 句描述>
- suggested_target: <提出 reflection 时建议的落点 · 与 payload / tasks.md 同字段> | N/A
- resolution: promoted_to_invariant | distilled_to_standards | folded_into_spec | folded_into_ssot | promoted_to_ssot_patch | dismissed
- target: charter.md#INV-LIM-005 | .github/instructions/`<file>`.md | design.md#DSN-API-002 | 母本.md#<章节> | N/A    # 裁决后实际落点（可能与 suggested_target 不同）
- reason: <为何这样裁决 · 1–2 句>
- by: <裁决人 / AI 环境标识>

```

每条 reflection 在裁决归档时，**必须**：

1. 同 PR 从 YAML 中**物理删除**已裁决条目（不是改状态位，是删节点）；仅变状态位 = GC 失职。
2. 同 PR 在本文件**追加**同等条目。
3. 若 `resolution=promoted_to_invariant` → 同 PR 修 `charter.md §5` 补新 INV-* 条目。
4. 若 `resolution=distilled_to_standards` → 同 PR 修 `.github/instructions/<主题>.md` 补新条目。
5. 若 `resolution=folded_into_spec` → 同 PR 修 `design.md` / `requirements.md` 对应 ID。
6. 若 `resolution=folded_into_ssot`（ssot_stewardship 裁决后用户批准回流） → 同 PR 修 charter / .github/instructions / 母本对应权威章节；未获用户明确批准前禁止使用本枚举。
7. 若 `resolution=promoted_to_ssot_patch`（用户批准把 stewardship 升格为正式 SSOT Patch 待后续 feature 派生） → 同 PR 在 `docs/specs/active/<patch-slug>/` 新建 SSOT Patch spec 或在 `.github/instructions/` 新增建议草案文件；不直接改母本。

### A.7.3 阻塞规则

Phase 0 启动新 feature 前扫 `implementation_reflections.active`，命中以下任一条 → 不得推进新 feature 的 Phase 1，必须先按对应处置完成：

- `kind: spec_drift` 且 `severity: high` → 回写 spec / charter 后才能续。
- `kind: audit_debt` 且 `severity ∈ {medium, high}`，或缺真实数据库面 / 文档 SSOT 面证据 → 回 Phase 1.5 按 §A.7 第 5 条流程补 EXIST-* 锚点 + 重过 Audit Depth Gate。
- `kind: audit_debt` 且 `extension_payload` 非空（Existing Touches AI-DRI 自动追加 ≥ 2 个公共契约相关文件 · 详 §A.7.5）→ 补 audit.md `EXIST-DSN-*` + 同 PR 更新对应 Task `Existing Touches`。
- `kind: ssot_stewardship` 且（`severity: high` 或 `approval_required: yes` 且不修改 Authoritative SSOT 就无法继续）→ 走 Gate A/B 裁决；批准回流 SSOT 后同 PR 改 charter / .github/standards 权威章节，archive 留 `resolution=folded_into_ssot` 或 `resolution=promoted_to_ssot_patch`；显式驳回则 archive 留 `resolution=dismissed` + 原因。
- `kind: new_invariant_candidate` 且 `suggested_target` 含 `INV-BAN-*` / `INV-SEC-*`（"不该跨越的绝对边界"）→ 走 Gate B 裁决（升格 INV-* 补入 charter §5 / 显式驳回 + archive 留 `resolution=dismissed` + 原因）。
- `implementation_reflections.active` 存活条目 > 10 → 视为 GC 失职，先走 §A.7 GC + 归档（`reflection_archive_script` 槽位）。
- YAML 与 archive 文件出现同 reflection-id 重复存在 → 视为 GC 失职，回滚 PR。

**软累计**（不阻塞下轮 Phase 1，仅留 active 区累计裁决）：

- `kind: audit_debt` 且 `severity: low` → 在 audit.md `## 11. Audit Refresh Log` 追加一行记录（`templates/audit.md`）即可。
- `kind: ssot_stewardship` 且 `severity ∈ {low, medium}` 且 `approval_required: no`。
- `kind: new_invariant_candidate` 且 `suggested_target` 含 `INV-LIM-*` 或软红线候选 → 走 Gate B 但不阻塞。
- `kind: implementation_choice` / `kind: reusable_pattern` → 任意 severity 软累计（reusable_pattern 裁决可 `resolution=distilled_to_standards`）。
- `kind: test_modified` → 由 §A.2 hash 校验机械触发；归档前必检 `before_sha256` / `after_sha256` / `reason` 三字段齐备。

### A.7.4 交付台账与合同归档的关系（归档路径区别 · 含 active/done 迁移时机）

**active → done 迁移触发条件**（三条件齐 → 必走，由你在交付 PR 中执行 `git mv docs/specs/active/<feature-slug>/ docs/specs/done/<feature-slug>/`）：

1. tasks.md `## 3. Task List` 所有 Task `Status = Done` 且无 `Blocked` / `Blocked(Suspended)` 残留；
2. `<feature-slug>/artifacts/` 与所有 Task 的 `Artifacts:` 声明一致（无遗漏 / 无外溢；项目根 `reports/` / `tmp/` / `output/` 无散落产物，散落者按 cleanup_manifest 迁移）；
3. `docs/specs/project archives/delivery-log.md` 已追加本条 feature 的交付记录。

未齐三条件即迁移 → 视为越界，PR 拒合并。执行端 §9.2 在最后一条 Task Done 时呈交清单提醒用户。

**归档路径区别**：

- `reflections-archive.md` 位于 feature 内部（`docs/specs/active/<feature-slug>/reflections-archive.md` → 迁移后 `docs/specs/done/<feature-slug>/reflections-archive.md`）；与主 workflow §1.6 active/done 归档动线一致。
- `docs/specs/project archives/delivery-log.md` 是项目层交付台账（单一文件），每完成一个 feature 追加一行摘要，**不复制 spec 全文**；只在交付事实部分引用 reflection 概要 ID（如 `REF-001 · distilled_to_standards`）。
- 本 feature 的 `reflections-archive.md` 是该 feature 的「实现旁注备忘」，对其他 feature 不直接可见；**不反流为全局历史**。全局反流走 **INV-* 上升**（`charter.md §5`）或 **standards 蒸馏**（`.github/instructions/<主题>.md`）的正路。
- 即：只有被裁决为 `promoted_to_invariant` 或 `distilled_to_standards` 的条目才进入项目级 SSOT 影响后续 feature。

### A.7.5 Existing Touches 扩展回流（audit_debt 子类型）

**问题**：执行端某 Task 实施过程中 AI-DRI 自动追加 ≥ 2 个公共契约相关文件至 `Existing Touches`（隐含写作端 Phase 1.5 audit 范围不准）→ 必须把"追加事实"结构化反流给写端，避免下一轮 spec 仍按旧范围派生。

**写作端必产字段**（reflection 中 `kind: audit_debt` 的扩展 schema，仅 Existing Touches 扩展场景填）：

```yaml

- id: REF-XXX
  task: TASK-007
  kind: audit_debt
  severity: medium    # ≥ 2 公共契约文件追加视同 medium；如其中 ≥ 1 个触动 schema / API / 凭据 / UI（与下方 public_contract_impact 枚举 4 个非 none 值严格对齐 · 与执行端 `tasks-md-schema.md §3.1` 第 5 问同源） → 升 high
  summary: "TASK-007 实施中追加 backend/repositories/X.py + backend/schemas/Y.py 至 Existing Touches"
  suggested_target: audit.md#EXIST-DSN-*    # 指向待补 EXIST-* 锚点（写作端裁决后补真值）
  approval_required: yes
  raised_at: <ISO 8601>
  resolved_at: null
  raw_path: <feature-slug>/reflections/REF-XXX.md
  extension_payload:                         # 仅 Existing Touches 扩展场景非空
    task: TASK-007
    added_files:
      - backend/repositories/X.py
      - backend/schemas/Y.py
    reason: "实施 DSN-API-007 时发现 X.py 需新加 helper 方法以兼容旧 Schema"
    public_contract_impact: <none / schema / api / credential / ui>    # 影响层级，决定 severity 升降

```

**裁决路径**：详 §A.7 第 5 条 audit_debt 项 + §A.7.3 阻塞规则。

**反模式**：

- ❌ 执行端自动追加 ≥ 2 公共契约文件但未在 Reflections 留 `kind: audit_debt + extension_payload`
- ❌ `extension_payload.added_files` 留空 / 仅写一个文件路径
- ❌ 写端裁决时未补 audit.md EXIST-* 锚点就标 resolved
