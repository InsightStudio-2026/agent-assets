# Forbidden Actions Table

> **When to read**: 在 `/specs-write` 任意阶段做违规自检，或出现禁止动作风险时读取本文并按处置锚点回切。

| Phase | 严禁动作 | 处置锚点 |
| ------- | ---------- | ---------- |
| Phase 0 maturity intake | 跳过 Project Maturity 判定或 SSOT Health Check | `templates/maturity-intake.md §Phase 0 判定硬规则` 停下补 `maturity-intake.md` |
| Phase 0 maturity intake | 将 `Needs Repair` / `Unfit As Source` 的 SSOT 继续派生为 charter / requirements / design | `templates/maturity-intake.md §Phase 0 判定硬规则` 执行 SSOT Repair 或 Gate A 用户裁决 |
| Phase 0 maturity intake | Seed / Greenfield 的 N/A 无 evidence 或无 Future Audit Trigger | `templates/maturity-intake.md` §2 补 Baseline / Greenfield Survey 证据 |
| 任意阶段 | 未经用户明确批准直接修改 Authoritative SSOT（母本 / L1 SSOT / .github/standards 权威章节） | `cross-cutting.md §1.4-B` 改写为 `SSOT Stewardship Suggestions` / `Repair Draft` 并请求 Gate A/B 批准 |
| 任意阶段 | 写业务代码 / 跑迁移 / 改真实 DB | 主 workflow §1.3 与 §2.6.3 workflow 边界 |
| 任意阶段 | 无 Decision Gate 留痕伪造 `Approval.Status = Approved` | `cross-cutting.md §2.3` 防伪追问 |
| 任意阶段 | 越阶段产出（一次产多件文件） | 主 workflow §0.3 节奏一次一件 |
| 任意阶段 | 复述 SSOT 已定义事实 | `cross-cutting.md §1.4-B` 改 `@<路径>#<章节>` 引用 |
| 任意阶段 | 行号区间定位 spec 内引用 | `cross-cutting.md §1.3` 改 ID 锚点 |
| Phase 1.5 audit | grep 命中当审计 / 只读 1–2 文件即推进 / "看起来是" 写 EXIST-*/ DB-API-UI-FS 状态未真实校验 / 省略 unknowns | `templates/audit.md §Phase 1.5 审计硬规则` 五条审计偷懒禁令 |
| Phase 1.5 audit | DB / API / UI / FS 类 EXIST 缺 `Verified By:` 4 项 / 原文 dump 超 2 句 / evidence_file 首行 4 桶分类缺失 | `appendix.md §A.4` 防 4 工具原文外置三铁律 |
| Phase 1.5 audit | Audit Depth Gate 未达 PASS_TO_REQUIREMENTS 即推进 Phase 2 | `templates/audit.md §Phase 1.5 审计硬规则` 必须同时满足 14 面覆盖 + Overall Confidence ≥ 80% + 两个强证据面（真实数据库面 / 文档 SSOT 面）各自 confidence ≥ 80% + Blocking Unknowns = none |
| Phase 2 requirements | REQ 缺 EARS AC 或缺 BDD Scenario | `cross-cutting.md §3.3` 强制配对 |
| Phase 2 requirements | 失败分支 BDD 缺失（涉及外部调用 / 写入 / 跨进程 / 批量作业） | `cross-cutting.md §3.2` 补失败分支场景 |
| Phase 3 design | 引入 INV-BAN-* 禁用依赖 | `cross-cutting.md §5.3` 停下回 Phase 1 修 charter |
| Phase 3 design | 重新定义 SSOT 已定义契约 | `cross-cutting.md §1.4-B` 改 `@<路径>#<章节>` 引用 |
| Phase 3 design | 跨边界 DSN 漏 Failure Strategy | `design-rules.md §1` 拒推进 Phase 4 |
| Phase 3 design | DSN-LLM 三件防御不全 | `design-rules.md §1` 补全 Prompt Boundaries / Deterministic Fallback / Context Truncation |
| Phase 3 design | 跨端通信两端手写结构体 | `design-rules.md §1` 改单端 SSOT + autogen |
| Phase 3 design | DSN-DB Replaces 漏 Migration Strategy（命中条件时） | `design-rules.md §1` 补三选一策略 |
| Phase 4 tasks | Task 头部缺必填字段 | `task-rules.md §1` 拒推进 Phase 5 |
| Phase 4 tasks | Traceability Matrix 手改单元格 | `appendix.md §A.1` 走 `traceability_regen` 脚本 |
| Phase 4 tasks | P0 Essential 超 5 条（跨边界 / 动凭据 超 7 条） | `appendix.md §A.5` Task 裁切不够细，回 Phase 4 拆 |
| Phase 4 tasks | A 类字段（Touches / Existing Touches / Verification Commands / Artifacts）未用 `[ ]` checkbox / B 类字段误用 `[ ]` | `task-rules.md §1` 字段二分硬规则 |
| Phase 4 tasks | Revert Conflict Risk 漏检共享文件 | `appendix.md §A.3` 防 3 强制声明 shared_with + shared_files |
| Phase 4 tasks | 修改既有源码 / 改既有 DB schema 已部署版 / 改既有 ORM 模型 / 改进程拓扑 / 写本地非源码状态 但 Revert Command 填 N/A | `task-rules.md §1` 五条铁律必填非 N/A |
| Phase 4 tasks | DSN-DB Replaces 命中迁移策略时，Revert Command 填 `git checkout` 物理回滚 | `task-rules.md §1` 必须改业务可回路径 |
| Phase 4 tasks | DB Test Isolation 命中时缺三要素任一 | `task-rules.md §1` 补隔离机制 / 副作用边界 / 收尾断言 |
| Phase 4 tasks | DB Test Isolation 缺 tier 档位选择 / Tier 3 缺"为何不能用 Tier 1/2"的豁免理由 / Tier 3 缺 reset + seed 配套 | `task-rules.md §1` 三档优先级反模式 |
| Phase 4 tasks | 项目层启用 `Goal / Steps / Task DoD` 扩展但未遵守 `task-rules.md §1` 字段二分（A 类未用 `[ ]` / B 类误用 `[ ]`） | `templates/tasks.md` 模板说明 #6 协议自检公式 |
| Phase 3 design / Phase 4 tasks | 使用枚举外 `<domain>` 但未在 charter / audit Notes 登记 `OTHER` 理由 + 转正方向 | `cross-cutting.md §1.2` 子域枚举硬规则 |
| Phase 4 tasks | Task 适用 INV-SEC-* 且 Touches 涉凭据 / 第三方 API / .env / 遥测 / 凭据轮转，但 Verification Commands 缺 secret-scan 命令 | `task-rules.md §1` Secret-Scan 命令条件化必填规则 |
| Phase 5 handoff | handoff-payload.yaml 缺 invariants 全文 / first_task 全量字段 / critical_contracts 全量 Task 跨边界 DSN 摘要 | `cross-cutting.md §4.3` schema 硬约束 |
| Phase 5 handoff | implementation_reflections 存活 > 10 未走 GC | `appendix.md §A.7` GC 流程 |
| 任意阶段 | 项目根 reports / tmp / output 散落 spec 副产物 | 主 workflow §1.6 artifacts/ 子目录硬约束；spec Done 时执行 cleanup_manifest |

---

## Post-Write Format Validation Gate（产出后格式校验门）

> **When**: 每个 Phase 产出文件后、标记该 Phase Done 前，必须执行本节校验。违反任一命令 → Phase 未完成，修复后重新校验。

### 通用规则

- 所有校验命令以 PowerShell `Select-String` 形式给出，零依赖，在项目根执行。
- 若某 Phase 被跳过（如 Medium 跳 audit/design），对应校验也跳过。
- 校验失败不得以"内容正确只是格式不对"为由推进——ID 格式是机器可追溯性的硬前提。

### Phase 0 校验：maturity-intake.md

```powershell
# 必须存在 Decision Summary 块
Select-String -Path "docs/specs/active/<slug>/maturity-intake.md" -Pattern "Decision Summary" -Quiet

# 必须包含 Project Maturity Evidence 表（至少 6 行）
$n = (Select-String -Path "docs/specs/active/<slug>/maturity-intake.md" -Pattern '^\| ').Matches.Count; if ($n -lt 6) { throw "maturity-intake: evidence table rows < 6" }

# Decision 必须为合法枚举值
Select-String -Path "docs/specs/active/<slug>/maturity-intake.md" -Pattern "PROCEED_TO_CHARTER|PAUSE_FOR_GATE_A|BLOCKED_SSOT_REPAIR|BLOCKED_UNFIT_SOURCE" -Quiet

# _status.md 存在且状态字段已写入（Phase 0 必须创建——状态机事实源，后续恢复依赖此文件）
Select-String -Path "docs/specs/active/<slug>/_status.md" -Pattern "State:" -Quiet
```

### Phase 1 校验：charter.md

```powershell
# 必须包含 Sources 表（SRC-### 格式）
Select-String -Path "docs/specs/active/<slug>/charter.md" -Pattern "SRC-\d{3}" -Quiet

# 必须声明 Mode 和 Complexity
Select-String -Path "docs/specs/active/<slug>/charter.md" -Pattern "Mode:.*(Seed|Greenfield|Hybrid|Brownfield)" -Quiet
Select-String -Path "docs/specs/active/<slug>/charter.md" -Pattern "Complexity:.*(Small|Medium|Large)" -Quiet

# 必须含 Architectural Invariants（INV-BAN / INV-LIM / INV-SEC 至少一种）
Select-String -Path "docs/specs/active/<slug>/charter.md" -Pattern "INV-(BAN|LIM|SEC)-\d{3}" -Quiet
```

### Phase 1.5 校验：audit.md（仅 Hybrid/Brownfield）

```powershell
# 必须含 Audit Coverage 或 14 面覆盖声明
Select-String -Path "docs/specs/active/<slug>/audit.md" -Pattern "Audit Depth Gate|14.*面" -Quiet

# EXIST-* 锚点格式正确
Select-String -Path "docs/specs/active/<slug>/audit.md" -Pattern "EXIST-(DSN|REQ|API|DB|UI|FS)-\d{3}" -Quiet
```

### Phase 2 校验：requirements.md

```powershell
# 每条 REQ 有 ID（REQ-###）
$reqs = (Select-String -Path "docs/specs/active/<slug>/requirements.md" -Pattern '^### REQ-\d{3}').Matches.Count; if ($reqs -eq 0) { throw "requirements: no REQ-### found" }

# 必须有 BDD Scenario（gherkin 代码块）
Select-String -Path "docs/specs/active/<slug>/requirements.md" -Pattern '```gherkin' -Quiet

# 必须有 EARS AC（AC-### 格式）
Select-String -Path "docs/specs/active/<slug>/requirements.md" -Pattern "AC-\d{3}\.\d+" -Quiet

# NFR 六类槽位至少显式声明
Select-String -Path "docs/specs/active/<slug>/requirements.md" -Pattern "NFR-(SEC|PERF|OBS|REL|UX|PLAT)-\d{3}" -Quiet

# Derivation Map 存在
Select-String -Path "docs/specs/active/<slug>/requirements.md" -Pattern "Derivation Map|Derived From" -Quiet
```

### Phase 3 校验：design.md（仅 Large 模式）

```powershell
# 每个 DSN 有 ID（DSN-<domain>-###）
Select-String -Path "docs/specs/active/<slug>/design.md" -Pattern "DSN-(DB|API|UI|ARCH|LLM|SEC|PERF|OBS|REL|PLAT|PROC|MSG|CONF|DATA|MATH|FS|OTHER)-\d{3}" -Quiet

# 跨边界 DSN 含 Failure Strategy
Select-String -Path "docs/specs/active/<slug>/design.md" -Pattern "Failure Strategy" -Quiet
```

### Phase 4 校验：tasks.md

```powershell
# 每个 Task 头部有 Implements 字段
$tasks = (Select-String -Path "docs/specs/active/<slug>/tasks.md" -Pattern '^- Implements:').Matches.Count; if ($tasks -eq 0) { throw "tasks: no Task with Implements field" }

# A 类字段用 - [ ] checkbox
Select-String -Path "docs/specs/active/<slug>/tasks.md" -Pattern '^- Touches' -Quiet

# Traceability Matrix 存在
Select-String -Path "docs/specs/active/<slug>/tasks.md" -Pattern "Traceability Matrix" -Quiet

# Test Plan / DoD / Rollback 三章节存在
Select-String -Path "docs/specs/active/<slug>/tasks.md" -Pattern "Test Plan" -Quiet
Select-String -Path "docs/specs/active/<slug>/tasks.md" -Pattern "Definition of Done" -Quiet
Select-String -Path "docs/specs/active/<slug>/tasks.md" -Pattern "Rollback Plan" -Quiet
```

### Phase 5 校验：handoff-payload.yaml

```powershell
# YAML 文件存在且可解析
$yaml = "docs/specs/active/<slug>/handoff-payload.yaml"
if (-not (Test-Path $yaml)) { throw "handoff-payload.yaml missing" }
python -c "import yaml; yaml.safe_load(open('$yaml'))" 2>$null; if ($LASTEXITCODE -ne 0) { throw "YAML parse failed" }

# schema_version 声明
Select-String -Path "docs/specs/active/<slug>/handoff-payload.yaml" -Pattern "schema_version:" -Quiet

# invariants 节含完整 rule 字段（非仅 ID）
Select-String -Path "docs/specs/active/<slug>/handoff-payload.yaml" -Pattern "rule:" -Quiet

# traceability 节枚举全量 Task
Select-String -Path "docs/specs/active/<slug>/handoff-payload.yaml" -Pattern "- id: TASK-" -Quiet

# first_task 节存在
Select-String -Path "docs/specs/active/<slug>/handoff-payload.yaml" -Pattern "first_task:" -Quiet

# critical_contracts 节存在（至少 [] 空声明）
Select-String -Path "docs/specs/active/<slug>/handoff-payload.yaml" -Pattern "critical_contracts:" -Quiet

# 全部 9 文件存在性（7 spec + YAML + _status）
$files = @("maturity-intake.md","charter.md","audit.md","decisions.md","requirements.md","design.md","tasks.md","handoff-payload.yaml","_status.md"); $missing = $files | Where-Object { -not (Test-Path "docs/specs/active/<slug>/$_") }; if ($missing) { throw "missing files: $missing" }

# 双源 TASK 数自洽（YAML traceability vs tasks.md Traceability Matrix 行数）
$yamlCount = (Select-String -Path "docs/specs/active/<slug>/handoff-payload.yaml" -Pattern '^\s+- id: TASK-\d{3}$').Matches.Count; $mdCount = ((Get-Content "docs/specs/active/<slug>/tasks.md" -Raw) -split '\n' | Select-String -Pattern '^\| TASK-\d{3} \|').Matches.Count; if ($yamlCount -ne $mdCount) { throw "traceability mismatch: YAML=$yamlCount tasks.md=$mdCount" }
```

### 违规处置

| 违规 | 处置 |
|---|---|
| 任一 Phase 校验命令不通过 | 该 Phase 标记 NOT DONE，修正 spec 后重跑全部校验 |
| 连续 2 次校验失败 | 回读对应 `templates/<file>.md`，确认模板理解无误 |
| 校验通过但内容语义错误 | 不属本 Gate 管辖——交 `stop-conditions.md` Decision Gate 判定 |

> **设计意图**：本 Gate 仅拦截格式级违规（ID 缺失、必填字段漏写、checkbox 误用），不替代语义审查。它是防 5（注意力稀释）的最后一道自动防线。

---

## Phase Exit Gate（阶段出口门禁）

> **When**: 每个 Phase 产出完成、准备标记 Done 并进入下一 Phase 前，必须通过本门禁。

每个 Phase 出口必须同时满足以下三条件，缺一不得推进：

| # | 条件 | 验证方式 | 失败处置 |
|---|------|---------|---------|
| 1 | **Format Validation Gate 通过** | 执行 `forbidden-actions.md §Phase N 校验` 全部命令，全部 PASS | 修正 spec → 重跑 → 仍失败则回读模板 |
| 2 | **self-check.md 对应节全部 [x]** | Agent 逐条朗读 self-check 该 Phase 清单并确认已完成 | 补做未完成项 → 重新自检 |
| 3 | **_status.md 状态已更新** | 检查 `_status.md` 的 `Current State` 已反映当前 Phase 完成态 | 补写状态转移记录 |

**禁止行为**：

- ❌ Format Gate 失败但以"内容正确只是格式不对"为由跳过 → 格式是机器可追溯性的硬前提
- ❌ self-check 跳过某条说"不重要" → 每条都是前人踩坑总结
- ❌ _status.md 不更新 → 下次恢复时无锚可依，等同于盲飞

**Phase 0 特殊要求**：Phase 0 必须**创建**（而不仅是更新）`_status.md`，写入初始状态转移记录。后续 Phase 在此文件追加。
