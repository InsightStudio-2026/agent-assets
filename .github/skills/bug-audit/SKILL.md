---
name: bug-audit
description: 广度与深度缺陷审计；从 bug 报告、失败测试或异常行为出发，评估复现、影响面、严重性、系统性根因与修复路径，分流到 issue-triage / diagnose / specs-write / specs-execute / review。Use when user reports a bug, asks to assess impact/severity, needs bug triage/root-cause broad scan, or says 缺陷审计/影响面评估/Bug分流/严重性分级。
argument-hint: "什么缺陷？"
---


# /bug-audit · 缺陷审计

**定位**：复杂缺陷的审计与分流。判断 bug 是否真实、影响面多大、是否系统性问题、应直接修复还是进入 `/specs-write`。

**边界**：不替代 `/issue-triage` 做 issue 状态管理，不替代 `diagnose` 深挖具体根因，不替代 `review` 审查已完成 diff，不直接执行修复代码；Small direct fix 只输出推荐路线，后续切换到 `diagnose` / `tdd` / direct with TDD discipline 处理。本审计聚焦爆炸半径与专科定位，**不强制执行完整的 14 面全局审计（unified-14-surface-audit）**，但在评估阶段可按需局部映射参考相关表面的规范（如安全面、数据面）。

**斜杠命令**：`/bug-audit`

**上下游能力**：`/issue-triage`、`diagnose`、`/specs-write`、`/specs-execute`、`review`、`/project-steward`。

---

## 懒加载契约

- **MUST read**: `./decision-matrix.md`
- 开始判定或执行 Phase 流程前，必须完整懒加载上述细节。

---

## 1. 阶段 1 — 缺陷引入标准化

### 1.1 输入来源

可能来自：

- 用户自然语言描述。
- issue / ticket。
- failing test。
- CI failure。
- runtime error / stack trace。
- production incident。
- review finding。
- regression after a recent change。

### 1.2 标准化缺陷说明（Bug Statement）

把输入改写成：

```markdown
## 缺陷陈述 (Bug Statement)

- 实际现象 (Observed behavior):
- 预期行为 (Expected behavior):
- 发现位置 (Where observed):
- 受影响范围 (Who is affected):
- 开始时间 (When it started):
- 发生频率 (Frequency):
- 规避方法 (Known workaround):
- 事实依据 (Evidence):

```

### 1.3 最小澄清

只有缺失以下信息且无法从仓库 / 日志 / issue 推断时，才问用户：

- 复现步骤。
- 期望行为。
- 影响用户 / 环境。
- 是否生产中发生。
- 是否涉及数据损坏、安全、计费、权限。

不得一次抛出长问卷。最多先问 3 个阻塞问题。

---

## 2. 阶段 2 — 复现评估

### 2.1 复现状态

分类：

- `Reproduced`：已本地或测试复现。
- `Reproducible by report`：用户步骤清晰但 AI 未运行。
- `Intermittent`：间歇性。
- `Cannot reproduce yet`：暂不可复现。
- `Not enough information`：信息不足。

### 2.2 最小复现

尽量收敛到：

- 最少步骤。
- 最小数据集。
- 最小权限角色。
- 最小环境差异。
- 最小代码路径。

### 2.3 输出

```markdown
## 复现验证 (Reproduction)

- 复现状态 (Status):
- 置信度 (Confidence): <High | Medium | Low>
- 极简复现步骤 (Minimal steps):
- 依赖数据/角色/环境 (Required data / role / environment):
- 复现依据 (Evidence):
- 未知数/疑点 (Unknowns):

```

---

## 3. 阶段 3 — 爆炸半径审计

### 3.1 影响面维度

检查：

- 用户群体：全部用户 / 某角色 / 某租户 / 某配置。
- 功能路径：单页面 / 核心路径 / 后台任务 / API / webhook。
- 数据范围：读错误 / 写错误 / 数据丢失 / 数据污染 / 隐私泄露。
- 时间范围：新问题 / 长期存在 / 回归。
- 系统范围：前端 / 后端 / DB / queue / cron / external API / auth / billing。
- 运维范围：部署、配置、环境变量、迁移、缓存。

### 3.2 证据来源

可使用：

- 代码路径阅读。
- 测试失败位置。
- 日志 / stack trace。
- 最近提交。
- issue 历史。
- schema / migration。
- docs / spec / mother SSOT。

### 3.3 输出

```markdown
## 爆炸半径 (Blast Radius)

- 受影响用户 (Affected users):
- 受影响工作流 (Affected workflows):
- 受影响模块 (Affected modules):
- 数据影响 (Data impact):
- 外部集成影响 (External impact):
- 运维/运行影响 (Operational impact):
- 置信度 (Confidence):
- 事实依据 (Evidence):

```

---

## 4. 阶段 4 — 严重性与风险分级

### 4.1 严重性等级

| Severity | 判定 |
| ---------- | ------ |
| `S0 Incident` | 生产不可用、数据损坏、安全泄露、计费严重错误、广泛用户阻断 |
| `S1 Critical` | 核心路径失败、无可靠 workaround、影响重要用户或业务流程 |
| `S2 High` | 重要功能错误，但有 workaround 或影响范围有限 |
| `S3 Medium` | 局部错误、体验明显受损、风险可控 |
| `S4 Low` | 小问题、边缘场景、文案或轻微 UI 行为 |

### 4.2 风险标签

可多选：

- `data-loss`
- `data-corruption`
- `security`
- `privacy`
- `authz`
- `billing`
- `availability`
- `performance`
- `regression`
- `spec-ambiguity`
- `architecture-boundary`
- `test-gap`
- `observability-gap`

### 4.3 输出

```markdown
## 严重程度 (Severity)

- 严重级别 (Severity):
- 风险标签 (Risk tags):
- 用户影响 (User impact):
- 业务面影响 (Business impact):
- 紧急程度 (Urgency):
- 定级理由 (Rationale):

```

---

## 5. 阶段 5 — 根因假设

### 5.1 根因层级

判断最可能层级：

- Product expectation mismatch。
- Spec ambiguity / wrong requirement。
- UI state / interaction。
- API contract。
- Domain logic。
- Persistence / migration / data model。
- Auth / permission。
- Integration / external service。
- Background job / async ordering。
- Config / environment。
- Build / deploy。
- Test fixture / test-only issue。

### 5.2 假设格式

```markdown
## 根因假设 (Root Cause Hypotheses)

- HYP-001: <假设描述 (hypothesis)>
  - 故障层级 (Layer):
  - 支持证据 (Supporting evidence):
  - 矛盾证据 (Contradicting evidence):
  - 置信度 (Confidence):
  - 下一步诊断动作 (Next diagnostic step):

```

> [!IMPORTANT]
> **挂载推演引擎 (`grill-me`)**：当根因假设存在多重博弈，或因 SSOT 盲区导致判定僵持时，你**必须**主动挂载调用 [[grill-me 技能]] (.github/skills/grill-me/SKILL.md) 引擎，由其接管这部分高压问答，辅助剥离出最可信的核心故障源，绝不可在模糊中自行瞎猜。

### 5.3 与 diagnose 的职责边界

本 workflow 只提出和排序根因假设。若需要深入定位，应分流：

```text

Recommended route: diagnose
Reason: root cause unknown but bug is concrete and reproducible.

## Steps to reproduce

1. [步骤 1]
2. [步骤 2]

```

`diagnose` 返回后不得直接实现；带回根因证据、复现证据和反证，进入 Phase 6 判定 implementation / spec / SSOT / architecture 归属。

从本 workflow 调用 `diagnose` 时，除非当前状态已是 `/bug-audit:SMALL_FIX_ROUTE_READY` 且用户意图明确要求实现，否则 `diagnose` 处于 evidence-return mode：只复现、定位根因并返回 §5.4 字段，不直接 patch。

### 5.4 诊断返回契约

`diagnose` 回到本 workflow 时，必须带回以下字段。若定位成功，进入 `/bug-audit:DIAGNOSIS_RETURNED`；若定位由于环境或复现限制失败无结果，必须带回 `No-change explanation` 并进入 `/bug-audit:DIAGNOSIS_FAILED_UNRESOLVED` 退出诊断循环，不得强行滞留：

```markdown
## 诊断返回结果 (Diagnose Return)

- 复现证据 (Reproduction evidence):
- 根因证据 (Root cause evidence): <N/A when diagnosis failed>
- 矛盾证据 (Contradicting evidence):
- 受影响文件/模块 (Affected files / modules):
- 置信度 (Confidence):
- 无改动/未修复说明 (No-change explanation): <required when no patch was made or no root cause was proven>

```

`/bug-audit:DIAGNOSIS_RETURNED` 只表示根因证据足以进入 Phase 6 分流判定，不表示可以直接 patch。

---

## 6. 阶段 6 — 规范与 SSOT 影响评估

### 6.1 判断缺陷类型

| Bug Type | 判定 | 推荐 | HG-*/ R-* 触发 |
| ---------- | ------ | ------ | ------------------ |
| `implementation-bug` | spec / 母本正确，实现偏离 | direct fix / diagnose / specs-execute | `S-HG-1 GATE_NOT_REQUIRED`（纯实现级）或 `HG-IMPL-*`（如涵不可逆动作） |
| `spec-gap` | spec 没覆盖失败分支、边界、验收 | 回 `/specs-write` 修 spec | `R-RETURN-4`（`entry-decision-tree.md §7.6`） |
| `wrong-spec` | spec 本身要求错误 | 回 `/specs-write` 或母本修复 | `R-RETURN-1/4` 或 `R-AUDIT-4`（如母本级）；可能预装配 `HG-STRAT-*` |
| `ssot-conflict` | 母本 / L1 SSOT 与实现目标冲突 | 停下做 SSOT Repair | `R-AUDIT-3`（ADR / 领域冲突）或 `R-AUDIT-4`（母本） |
| `architecture-bug` | 边界、数据流、契约、模块责任错误 | `/specs-write` 设计修订 | `R-AUDIT-1`（`/architecture-audit`）；重塑 → `HG-DESIGN-*` |
| `test-only` | 测试错误或 fixture 过期 | 修测试，但必须说明产品行为不受影响 | `S-HG-1 GATE_NOT_REQUIRED` |
| `cannot-determine` | 信息不足 | 补复现 / diagnose | —（信息不足，先补证据再装配 HG-*） |

### 6.2 上游文件检查

按存在情况读取：

- 母本 / L1 SSOT。
- `CONTEXT.md`。
- active / done specs。
- `requirements.md`。
- `design.md`。
- `tasks.md`。
- ADR / standards。

### 6.3 输出

```markdown
## 规格与母本影响 (Spec / SSOT Impact)

- 缺陷分类 (Bug type):
- 关联的母本/规格锚点 (Relevant SSOT / spec anchors):
- 需求/行为冲突 (Conflict):
- 是否需要修补规格 (Needs spec repair): <yes | no>
- 是否需要修补母本 (Needs SSOT repair): <yes | no>
- 评估理由 (Rationale):

```

---

## 7. 阶段 7 — 修复路径决策

### 7.1 路径矩阵

| 条件 | 推荐路径 |
| ------ | ---------- |
| S0/S1 + 生产风险 | 先止血 / rollback / hotfix plan，再补 spec |
| 小、明确、单文件、无契约影响 | 推荐 direct Small fix route，并切换 `diagnose` / `tdd` / direct |
| 可复现但根因未知 | `diagnose` |
| `diagnose` 已返回根因证据 (DIAGNOSIS_RETURNED) | 回 Phase 6 判定 Spec / SSOT Impact，不直接 patch |
| `diagnose` 诊断定位失败 (DIAGNOSIS_FAILED_UNRESOLVED) | 路由至 `/issue-triage` 挂起标记为 Blocked，提供排查日志，退出诊断死锁 |
| 涉及新需求 / 失败分支 / 验收缺失 | `/specs-write` |
| 涉及架构、DB、API、权限、计费、安全 | `/specs-write` |
| 已有 approved spec 且 bug 属于当前 Task 范围 | `/specs-execute` 回到相关 Task 或新增修复 Task（按 spec 规则） |
| 修复已完成但需审查 | `review` |
| 只是 issue 信息不足 | `/issue-triage` 补 intake |

### 7.2 输出

```markdown
## 修复路径 (Repair Path)

- 推荐路径 (Recommended path):
- 决策依据 (Why):
- 首要行动 (First action):
- 归属路由 (Owner route):
- 暂不实施动作 (Do not do now):

```

---

## 8. 阶段 8 — 回归与验证计划

### 8.1 回归测试要求

每个真实 bug 必须指定：

- 应新增或修改的测试层级。
- 失败测试应先红后绿。
- 覆盖的复现路径。
- 防止回归的断言。

### 8.2 验证命令

列出：

- 最小验证命令。
- 全量验证命令。
- 需要手动验证的 UI / 外部集成路径。
- 不可本地验证的项目，说明替代证据。

### 8.3 输出

```markdown
## 回归测试与功能验证 (Regression & Verification)

- 所需回归测试 (Regression test required):
- 测试层级 (Test layer):
- 最小运行命令 (Minimal command):
- 全量验证命令 (Full command):
- 手动验证步骤 (Manual verification):
- 可观测性/日志需求 (Observability / logging needs):

```

---

## 9. 阶段 9 — 完工收口与交付

### 9.1 标准报告格式

```markdown
## 缺陷审计报告 (Bug Audit Report)

## 工作流状态 (Workflow State)

- State: /bug-audit:<STATE>; common examples: /bug-audit:ROUTED | /bug-audit:ROOT_CAUSE_UNKNOWN | /bug-audit:SPEC_REPAIR_NEEDED | /bug-audit:SMALL_FIX_ROUTE_READY | /bug-audit:INCIDENT_RISK | /bug-audit:DIAGNOSIS_FAILED_UNRESOLVED

## 审计结论 (Outcome)

- <Routed | Root cause unknown | Small fix route ready | Spec repair needed | SSOT repair needed | Incident risk | Diagnosis failed unresolved>

## 权威信息与事实源 (Authority / Fact Source)

- Bug 证据 (Bug evidence): <user report / issue / failing test / logs>
- 复现证据 (Reproduction evidence):
- 规格锚点 (Spec / SSOT anchors):
- 故障审批来源 (Incident approval source): <N/A or user approval quote>

## 授权边界 (Authorization Boundary)

- 路由动作 (Route Action): <CONTINUE_IN_WORKFLOW | WAIT_FOR_USER | REPORT_AND_STOP | CONFIRMED_ACTION>
- 授权范围 (Authorized scope): <audit report / incident entry plan / small-route recommendation / named downstream entry input>
- 未授权范围 (Not authorized): <code patch / production rollback / data repair / tracker write / spec edit / downstream workflow internal actions>

## 缺陷陈述 (Bug Statement) (2)

- [请在此填入已标准化的 Observed/Expected behavior 缺陷陈述]

## 缺陷复现 (Reproduction)

- 复现状态 (Status):
- 置信度 (Confidence):

## 爆炸半径 (Blast Radius) (2)

- [请在此填入受影响的用户、模块及爆炸半径评估 findings]

## 严重程度 (Severity) (2)

- 严重级别 (Severity):
- 风险标签 (Risk tags):

## 根因假设 (Root Cause Hypotheses) (2)

- HYP-001:

## 规格/母本影响 (Spec / SSOT Impact)

- 缺陷类型 (Bug type):
- 是否需要修补规格 (Needs spec repair):
- 是否需要修补母本 (Needs SSOT repair):

## 修复路径 (Repair Path) (2)

- 推荐路径 (Recommended path):
- 首要行动 (First action):

## 回归与验证 (Regression & Verification)

- [请在此填入所需的回归测试层级与具体验证命令]

## 恢复/返航契约 (Return Contract)

- 目标路由 (Target route):
- 准入输入 (Entry input):
- 已解决 (Resolved):
- 仍受阻 (Still blocked):
- 未授权 (Not authorized):
- 恢复事实源 (Resume source):

## 质量门禁 (Gate)

- <N/A | Gate A/B/C | Incident approval needed>

```

### 9.2 文件落地规则

默认只在对话中报告。只有以下情况才建议落文件：

- S0 / S1。
- 需要进入 `/specs-write`。
- 涉及数据、安全、计费、权限。
- 需要多人协作或长期追踪。
- 用户明确要求留档。

建议路径：

```text

docs/specs/active/`<bug-slug>`/bug-audit.md

```

但如果 spec 尚未创建，先让 `/specs-write` 创建 feature / bugfix spec 根目录，再把 audit 纳入该目录。

### 9.3 关卡判定

| Gate | 命中条件 | 动作 |
| ------ | ---------- | ------ |
| Gate A Strategy | bug 暴露产品方向 / 用户承诺 / 商业规则错误 | 停下给推荐方案和备选 |
| Gate B Critical Design | 修复涉及架构、DB、API、权限、计费、安全边界 | 停下或回 `/specs-write` |
| Gate C Real-World Side Effect | 需要生产 rollback、数据修复、通知用户、外部 API 变更 | 等用户批准 |
| Incident | S0 / S1 且生产风险 | 优先止血方案，明确风险与回滚 |
| N/A | 小型实现 bug | 分流 direct small fix outside this workflow / diagnose，不在本 workflow 内 patch |

---

## 10. 与现有能力的边界

| 能力 | 负责 | 不负责 |
| ------ | ------ | -------- |
| `/issue-triage` | 收集 bug、建 issue、状态流转 | 系统性影响面审计 |
| `/bug-audit` | 影响面、严重性、根因假设、修复路径 | 深入修代码 |
| `diagnose` | 复现和定位根因 | 产品 / spec / SSOT 分流决策 |
| `/specs-write` | 复杂 bug 的修复合同 | 实现修复 |
| `/specs-execute` | 执行修复 Task | 改需求 / 设计 |
| `review` | 审查修复 diff | 前置影响面审计 |
| `/project-steward` | 判断 bug 之后项目下一步 | 具体 bug 审计细节 |

Small direct fix 仅限影响面明确、无 spec / SSOT 缺陷、无数据 / 安全 / 权限 / 计费风险；本 workflow 只判定是否可走 Small route。根因定位可用 `diagnose`，实现仍应遵守 `tdd` 的 Red-Green-Refactor。

---

## 11. 禁用行为

- 不在影响面未知时直接修复杂 bug。
- 不把无法复现说成已复现。
- 不把测试失败自动等同于产品 bug。
- 不忽略数据、安全、权限、计费风险。
- 不用“应该是前端问题”这类无证据归因。
- 不绕过 spec 修复需求或设计缺陷。
- 不用代码 patch 掩盖母本 / spec 错误。
- 不承诺生产数据修复，除非用户明确批准。

---

## 12. 快速自检清单

报告前自检：

- [ ] 是否标准化了 observed / expected？
- [ ] 是否给出复现状态和置信度？
- [ ] 是否检查了 blast radius？
- [ ] 是否评估数据、安全、权限、计费、可用性风险？
- [ ] 是否区分 implementation bug / spec gap / wrong spec / SSOT conflict？
- [ ] 是否给出唯一推荐修复路径？
- [ ] 是否指定 regression test requirement？
- [ ] 是否说明了不应立即做什么？

## 支撑资源

- [decision-matrix.md](./references/decision-matrix.md)
