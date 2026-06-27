---
name: project-steward
description: 项目缺省 DRI (首席责任人)。依托大模型的高维语境统筹与精确推演能力，以母本 SSOT 为权威基准，执行全表面系统级扫描与架构水位评估，精准洞察项目缺口与技术债，并输出确定性的执行分流决策。Use when project status is unclear, next steps unknown, need health assessment/gap analysis, or says 项目诊断/项目体检/技术债评估/下一步/项目分流。
argument-hint: "项目有什么问题？"
---


# /project-steward · 项目首席责任人 (Project DRI)

**核心意义与定位**：项目级缺省 DRI (Directly Responsible Individual)。本工作流的设计范式基于：**在确立了高信度的母本 SSOT 锚点后，全面释放大模型的宏观系统诊断能力。你能够以远超人工审查的上下文跨度与并发关联能力，执行严密的依赖拓扑分析与状态核验，精确透视项目当前的交付缺口、架构摩擦与演进盲区。**以此为准绳，Project DRI 将接管全局研判，回答“当前系统的真实成熟度水位在哪，下一步工程 ROI 最高的推进路径是什么”。

**边界**：默认只做状态审计、分流决策与下一步建议；不直接写业务代码，不替代 `/specs-write` 写 spec，不替代 `/specs-execute` 执行 Task，不静默修改 Authoritative SSOT。

**斜杠命令**：`/project-steward`

**调用对象**：`/project-inception`、`/business-model-audit`、`/specs-write`、`/specs-execute`、`/release-deploy`、`/security-privacy-audit`、`/observability-incident`、`/architecture-audit`、`/grill-with-docs`、`/bug-audit`、`/issue-triage`、`/tasks-to-issues`、`/repo-agent-setup`、`/repo-safety-setup`、`review`、`diagnose`、`handoff`。

**交叉引用**：本 skill 通过 `../specs-write/entry-decision-tree.md` 引用 R-PHASE0-*/ R-AUDIT-* / R-CLOSEOUT-*等规则；通过 `../specs-write/gate-dag-protocol.md` 引用 HG-* / S-HG-*/ DAG-N-* 等命名空间；通过 `../release-deploy/readiness-dashboard.md` 引用 R-RDY-* 发布就绪信号 。

---

## 懒加载契约

- **MUST read**: `./decision-matrix.md`
- 开始判定或执行 Phase 流程前，必须完整懒加载上述细节。

---

## 1. 阶段 1 — 范围与安全评估

### 1.1 读取用户意图

识别用户当前请求属于哪类：

- **Idea**：模糊 / 设想 / 愿景 / 方向性说法（“我想做 X”、“我觉得应该 Y”、“用户反馈说 Z”）。进入 Phase 1.5。
- **Status**：想知道项目状态。
- **Continue**：想让你继续推进。
- **Plan**：想知道下一轮做什么。
- **Recover**：中断后恢复。
- **Bug**：出现缺陷、报错、失败测试。
- **Review**：想审查已完成变更。
- **Business**：想判断商业模式、付费意愿、获客、替代方案、Pivot / Kill。
- **Architecture**：想审计架构摩擦、重构机会、模块深化。
- **Setup**：缺 issue tracker / 标签词表 / 领域文档读取规则 / 本地安全基线。
- **IssueExport**：想把 approved tasks / plan 发布到 issue tracker。
- **AssetMaintenance**：用户要维护代理资产（workflow / skill / AGENTS.md / 仓库级代理规则），无论这些资产位于独立资产仓库还是普通代码库。
- **Release**：准备上线、发布、回滚、canary、smoke、readiness dashboard 或 release notes。
- **SecurityPrivacy**：涉及权限、密钥、PII、OAuth、支付、依赖供应链、外部攻击面或安全隐私 gate。
- **ObservabilityIncident**：涉及生产事故、用户影响、告警、runbook、日志、指标、trace 或状态页。
- **Command**：明确点名另一个 workflow 或 routine。

原“Launch” / “Feature” 意图现在由 **Idea**类在 Phase 1.5 贴合检查后决定走 `/project-inception`（无母本）还是 `/specs-write`（有母本）。不再拍脑门预判。

### 1.2 安全边界判定

在任何路径上，

命中任一项时，不得直接执行实现动作，只能报告并分流：

- 缺少 Authoritative SSOT 且请求涉及产品方向 / 项目定位。
- active spec 的 Approval 状态不明。
- 当前变更包含数据库、迁移、权限、计费、凭据、生产副作用。
- 用户请求“继续”，但存在多个可继续方向且无明确优先级证据。
- 发现 spec 与代码 / 文档 / 用户目标冲突。
- 发现复杂 bug 但影响面未知。
- 商业产品 / 付费方向的用户、买方、替代方案或 MVP 投入依据不清。

---

## 1.5 阶段 1.5 — 构想锚定与对齐核查

仅在 Phase 1.1 判定意图为**Idea** 时激活。目的是让后续实现与推荐贴合原始 idea，**不是反过来 grilling 用户**。

### 1.5.1 构想锚定收集

把用户原始话语逐字记下作为 Idea Anchor。不重写、不总结、不推演。输出模板：

```markdown
## Idea Anchor
> <用户原话逐字引用>

## Anchor Hash
<本轮对话 ID 或 时间戳>
```

Anchor 会被 Phase 5 输出里所有推荐引用，避免下游漂移。

### 1.5.2 SSOT 优先路径选择

严格按以下顺序，不问用户：

```text

IF Idea 涉及商业产品 / 付费 / 获客 / MVP 投入，且买方、替代方案或关键验证证据不清
  → 先走 /business-model-audit
ELIF 仓库存在健康的母本 / L1 SSOT (需经 Phase 2 验证)
  → 走 SSOT 派生路径：Idea 作为 feature 输入交给 /specs-write
  → 不重启 /project-inception
ELIF 仓库有母本但不健康
  → 先修上游 (SSOT_NEEDS_REPAIR)、推荐 /grill-with-docs 或 /project-inception 修复模式
ELIF 仓库无母本 / 是全新项目
  → 走正常立项路径：/project-inception
ELSE  // 意图是 Idea 但不是全新方向，只是面向某模块的想法
  → 按 Idea 性质路由：

```

- 架构性 → /architecture-audit
- bug 样态 → /bug-audit
- 纯几问句 → 直接回答，不启用任何 workflow

```text

```

### 1.5.3 Alignment Self-Check (唯一允许中断点)

生成路由推荐前，作一次静默自检：

```text

[ ] 推荐动作是否能被 Anchor 原话直接推出？
[ ] 推荐是否隐含了 Anchor 未明说的范围扩展？
[ ] 推荐是否跳过了 Anchor 明说要做的某件事？
[ ] 是否需要用户拍板才能决定走哪个子路径？

```

所有项 "贴合 / 否" → 继续进入 Phase 2。

只要出现以下一个以上时，才停下以一句以内复述 + 一个问题的形式跟用户确认，不开启 grilling：

- 推荐动作明显超出 Anchor 范围（scope creep）。
- Anchor 同时能推出两个不同主路径（如 `/specs-write` vs `/architecture-audit`）且无优先级证据。
- Anchor 隐含的动作命中 1.2 安全边界。

复述模板：

```markdown
## Alignment Check
Anchor: "<原话>"
I will route to: <workflow + 其原因>
This stays inside the anchor because: <贴合证据>
<只在不贴合时加> Confirm anchor or correct it?
```

### 1.5.4 想法简报 (仅在走 /project-inception 或 /specs-write 时生成)

把 Anchor 包装为下游 workflow 能直接消费的输入（你应将其初始内容直接落盘至全局草稿板 `docs/Idea.md` 中孕育，在后续流转至 `/specs-write` 时，它将被自动吸收并定盘为 `decisions.md`）：

```markdown
## Idea Brief

## Original Anchor
> <原话>

## Route Decision
<workflow> because <证据>

## Pre-known Constraints (from SSOT)

- @<路径>#<章节>
- ...

## Open Questions Deferred to Downstream

- <由下游 workflow 按其自己的节奏 grilling>

```

Idea Brief 是令牌，不是代替下游的 spec。

---

## 2. 阶段 2 — 项目入口与现状审计 (Unified 14-Surface Audit)

> **MUST read**: `./unified-14-surface-audit.md`

作为 Project DRI，必须基于统一的 14 面审计准则对项目进行智能深广扫描。由你自主决断当前上下文是否需要完整 14 面全仓扫描 (Full-Surface Audit) 或范围裁剪抽查 (Scoped Full-Surface Audit)。**绝不可做流于表面的走马观花**。最少检查并覆盖以下核心表面：

### 2.1 拓扑序贯式五阶审计 (Topology-Ordered 5-Phase Audit)

在决定执行完整全仓扫描 (Full-Surface Audit) 还是局部范围抽样时，必须严格遵循**五阶向下钻取**的依赖关系，核心威胁绝对不可跳过：

- **第一阶：锚点基准 (The Anchor)**：重点勘察文档 SSOT 面 `[强证据]`。查找项目母本、`AGENTS.md`、`.github/standards`。母本不健康视为最高级阻塞。
- **第二阶：中枢与架构 (The Foundation)**：重点勘察真实数据库面 `[强证据]`、数据面与代码架构面。**强制使用真实工具 (MCP / CLI) 进行勘察**，绝不可假借静态 schema.sql 猜测数据模型。
- **第三阶：网域与契约 (The Web)**：排查前后端数据契约、依赖关系面及内部接口边界。
- **第四阶：端点与交互 (The Interface)**：排查 UI 面与外部可见的入口逻辑。
- **第五阶：非功能与生命周期 (NFR & Lifecycle)**：确认安全与隐私面、运行与部署面、测试面以及历史遗留债。

### 2.2 动态裁剪策略

作为 DRI，你应智能判定当前意图，并在五阶审计的框架下动态侧重：

- **Idea/立项类意图**：偏重第一阶（锚点基准）与第五阶（历史遗留）。
- **Bug/Issue 类意图**：偏重第二阶（代码入口/真实库）与第五阶（测试/运行日志）。
- **发布/安全类意图**：强迫勘察第五阶（安全与隐私、可观测性）及第三阶（依赖/接口）。

---

## 3. 阶段 3 — 状态分流与定义

必须把项目归入一个主状态。

### 3.1 状态与路由总览

| State | 判定 | 主推荐 | Gate / DAG / R-*ID 映射 | State Authority / Route Action |
| ------- | ------ | -------- | --------------------------- | -------------------------------- |
| `/project-steward:AGENT_ASSET_MAINTENANCE_NEEDED` | 用户请求维护 workflow / skill / AGENTS.md / 代理规则，或请求明确命中这些路径且存在索引、路由、目录契约或启用状态缺口 | direct asset maintenance（仅当前仓库代理资产外科维护；写入需按 `AGENTS.md` 编辑安全与验证清单） | 预装配 `HG-OPS-{repo}-asset`（仓库级配置变更）；如涉 git history 修改 → `HG-IRREV-*` | `REPORT_AND_STOP` |
| `/project-steward:AGENT_ASSET_REVIEW_COMPLETED_WITH_RECOMMENDATIONS` | 用户请求审查代理资产，结构健康但存在非阻断性边界、状态或措辞优化建议 | 报告建议；只有用户明确要求修正时才进入 direct asset maintenance | `S-HG-1 GATE_NOT_REQUIRED`（仅建议） | `REPORT_AND_STOP` |
| `/project-steward:AGENT_ASSET_CONTEXT_HEALTHY` | 用户请求审查代理资产，且索引、路由、目录契约与启用状态健康 | 报告无需修改或返回 `/project-steward` | — | `REPORT_AND_STOP` |
| `/project-steward:NO_PROJECT_SSOT` | 无母本 / 项目方向不清 | `/project-inception` | `R-AUDIT-4`（`../specs-write/protocols/entry-decision-tree.md §7.5`） | `REPORT_AND_STOP` |
| `/project-steward:SSOT_NEEDS_REPAIR` | 母本存在但不可派生 | 修复 SSOT 或 `/project-inception` | `R-PHASE0-3/4/5` + `R-AUDIT-4`（`../specs-write/protocols/entry-decision-tree.md §7.2 + §7.5`） | `REPORT_AND_STOP` |
| `/project-steward:READY_FOR_SPEC` | 有健康上游，但无 active spec | `/specs-write` | `R-PHASE0-1/2`（进 specs-write Phase 0） | `REPORT_AND_STOP` |
| `/project-steward:BUSINESS_MODEL_RISK` | 商业闭环、付费主体、替代方案或 MVP 投入依据不清 | `/business-model-audit` | `R-AUDIT-5`（`../specs-write/protocols/entry-decision-tree.md §7.5`） | `REPORT_AND_STOP` |
| `/project-steward:RELEASE_READINESS_NEEDED` | 已有 release candidate、用户请求上线 / 回滚 / canary / smoke，或 readiness dashboard / rollback plan 缺口阻塞交付 | `/release-deploy` | 读取 `../release-deploy/references/readiness-dashboard.md` R-RDY-*；如涉真实环境动作，交由 `/release-deploy` 判定 `WAITING_DEPLOY_APPROVAL` | `REPORT_AND_STOP` |
| `/project-steward:SECURITY_PRIVACY_AUDIT_NEEDED` | 涉权限、密钥、PII、OAuth、支付、依赖供应链、外部攻击面，或 NFR-SEC-* Active 且 security gate packet 缺失 | `/security-privacy-audit` | `HG-AUDIT-SEC-*` / `HG-IRREV-*` 候选；由 `/security-privacy-audit` 装配 packet | `REPORT_AND_STOP` |
| `/project-steward:OBSERVABILITY_INCIDENT_NEEDED` | 存在生产事故、用户影响、告警触发、状态页 / 降级需求，或 NFR-OBS-* Active 且 observability gate packet 缺失 | `/observability-incident` | `HG-AUDIT-OBS-*` / INCIDENT-* 候选；由 `/observability-incident` 分级、止血、runbook 与 packet | `REPORT_AND_STOP` |
| `/project-steward:SPEC_IN_PROGRESS` | active spec 正在写 | 继续 `/specs-write` 当前 Phase | 读 `/specs-write` 当前 State 表（含 HG-*/ DAG-N-SPEC-* 映射） | `CONTINUE_IN_WORKFLOW` |
| `/project-steward:READY_FOR_EXECUTION` | spec Approved 且有 Pending Task | `/specs-execute` | `DAG-N-TASK-{slug}-001` ready；`/specs-execute:TASK_LOCATED` | `REPORT_AND_STOP` |
| `/project-steward:EXECUTION_IN_PROGRESS` | 存在 In Progress Task | 继续 `/specs-execute` 或恢复中断 | 读 `/specs-execute:IN_PROGRESS` State；如 PAUSE_AND_ASK_PENDING → `S-HG-4 + HG-IRREV-001~004` | `CONTINUE_IN_WORKFLOW` |
| `/project-steward:READY_FOR_REVIEW` | 实现完成但未审查 | `review` | review skill 按 `../specs-write/protocols/gate-dag-protocol.md §4.4 RV-1~5` 核验 | `REPORT_AND_STOP` |
| `/project-steward:READY_FOR_DELIVERY_CLOSEOUT` | Task 全 Done 但未归档 / artifacts 未核验 | `/specs-execute` Phase 9 或交付收尾 | `R-CLOSEOUT-1/2/3`（`../specs-write/protocols/entry-decision-tree.md §7.8`） | `REPORT_AND_STOP` |
| `/project-steward:ARCHITECTURE_AUDIT_NEEDED` | 存在架构摩擦、模块浅、重构方向不清 | `/architecture-audit` | `R-AUDIT-1`（`../specs-write/protocols/entry-decision-tree.md §7.5`） | `REPORT_AND_STOP` |
| `/project-steward:AGENT_CONTEXT_MISSING` | issue tracker / 标签词表 / 领域文档规则缺失 | `/repo-agent-setup` | 预装配 `HG-OPS-{repo}-context` | `REPORT_AND_STOP` |
| `/project-steward:SAFETY_BASELINE_MISSING` | 缺本地安全基线、pre-commit 或危险 git 保护 | `/repo-safety-setup` | 预装配 `HG-OPS-{repo}-safety`；如涉危险 git 拦截 → `HG-IRREV-*` | `REPORT_AND_STOP` |
| `/project-steward:APPROVED_TASKS_NEED_ISSUES` | approved tasks / handoff plan 需要发布为 issues | `/tasks-to-issues` | `DAG-N-TASK-*` 投影到 issue blocker；不让 issue 成为第二事实源（PRJ-6） | `REPORT_AND_STOP` |
| `/project-steward:BUG_REPORTED` | 用户报告 bug，影响面未知 | `/bug-audit` | `R-AUDIT-2`（`../specs-write/protocols/entry-decision-tree.md §7.5`） | `REPORT_AND_STOP` |
| `/project-steward:BUG_READY_FOR_FIX` | bug 已明确且简单，且满足 `/bug-audit` direct small fix 条件 | `diagnose` / `tdd` 或 Small fix | `S-HG-1 GATE_NOT_REQUIRED`（小 bug 不触发 HG-*） | `REPORT_AND_STOP` |
| `/project-steward:VIBE_TRACK_READY` | 变更属于单一文件、无依赖牵连、无需架构决策的微型修补（如UI微调、单点异常修复） | 绕过 `/specs-write`，直通带 Scope Guard 的局部执行 (Vibe Track) | `S-HG-1 GATE_NOT_REQUIRED` | `REPORT_AND_STOP` |
| `/project-steward:BLOCKED` | 存在硬阻塞 | 先解除阻塞 | —（取决于阻塞性质） | `REPORT_AND_STOP` |
| `/project-steward:LOOP_COMPLETE` | 当前闭环完成 | 推荐下一轮 feature 或维护动作 | `R-CLOSEOUT-3` 完成（active → done git mv 已执行）；可启新 R-ENTRY-* 路径 | `REPORT_AND_STOP` |

本表 `State` 为本 workflow 的 local suffix；任何报告、handoff 或 route 建议必须输出为 workflow-qualified state，例如 `/project-steward:READY_FOR_EXECUTION`。Gate / DAG / R-*ID 详 `.github/skills/specs-write/gate-dag-protocol.md`（HG-* / DAG-N-*/ DAG-E-* / S-HG-*/ RV-* / PRJ-*）+ `entry-decision-tree.md §7`（R-AUDIT-* / R-PHASE0-*/ R-CLOSEOUT-*）。术语不更名；表中 ID 为机读字面映射，project-steward 不写 HG-*/ DAG-* 状态，只读取并路由。

### 3.2 状态归属与路由动作

`State` 只用于路由；权威状态见对应 workflow、`tasks.md`、issue tracker 或 Authoritative SSOT。Route Action 统一语义：

- `CONTINUE_IN_WORKFLOW`：当前 workflow 内继续。
- `WAIT_FOR_USER`：必须等待用户回答或批准。
- `REPORT_AND_STOP`：只报告推荐 route / entry input，不自动执行下游；只有用户在同一轮明确说“继续执行 <route / task / phase>”才可进入下游。
- `CONFIRMED_ACTION`：用户已批准本 workflow 内明确范围的文件写入、外部副作用或下游入口动作；下游 workflow 和真实世界副作用必须重新按各自 Gate 判定，不继承本状态的授权。

`推荐/分流/下游/返回` 默认 `REPORT_AND_STOP`；§5.3 仅允许在唯一方向明确时继续。

`direct asset maintenance` 不是下游 workflow；它只允许对当前仓库的 workflow / skill / `AGENTS.md` / 代理规则做外科式维护。任何文件写入仍必须由具体 diff、权威事实源和仓库验证清单约束，不授权业务代码、feature spec、tracker 外部写入或真实世界副作用。

所有报告 / handoff / route 建议中的 State 必须写成 workflow-qualified state，例如 `/project-steward:READY_FOR_EXECUTION` 或 `/specs-execute:TASK_DONE`，不得只写裸 `/project-steward:DONE` / `/project-steward:BLOCKED` / `READY_*`。

`Draft / Ready / Proposed / Recommended` 只表示候选或可进入下一步，不等于 `Applied / Written / Published / Done`；任何写入、tracker 更新、真实世界动作或下游执行都必须由对应 workflow 的事实源和确认门重新判定。

### 3.2.1 交付与完工状态契约

`*_HANDOFF_READY` / `READY_*` 只表示 route input、候选材料或下游入口包已经准备好；不表示下游 workflow 已开始，不表示代码 / tracker / SSOT 已修改，不授权真实世界副作用。下游 workflow 必须重新读取自己的事实源并执行自己的 Gate。

`/project-steward:DONE` local suffix 只在输出它的 workflow 内闭环。它可能表示审计、setup、发布或报告闭环已完成；不得推断其他 workflow、真实环境、代码实现或交付归档已经完成，除非报告中同时给出对应 workflow-qualified state 与 Authority / Fact Source 证据。

### 3.2.2 直接资产维护契约

`direct asset maintenance` 的事实源是 `AGENTS.md`、目标 skill 入口文件、`.github/skills/` 目录契约与用户本轮请求。

允许写入仅限：用户请求直接覆盖的 workflow / skill / `AGENTS.md` / 代理规则差异；新增、删除、重命名或启停资产时必须同步索引。跨文件重塑必须先给计划；单文件外科修复可在请求明确、diff 可追溯、无外部副作用时直接执行。

每次写入前后必须能说明：修改范围、权威依据、索引影响、验证清单和未授权范围。未授权范围固定包括：业务代码、feature spec、tracker 写入、真实世界副作用和下游 workflow 执行。

### 3.3 Resume Source（中断恢复事实源）

| Resume Need | 事实源 | 下一步判定 |
| ------------- | -------- | ------------ |
| 状态审计未完成 | Phase 2 Project Surface Scan 证据清单 | 补扫缺失表面后回 Phase 3 |
| Idea 路由未完成 | Idea Anchor + Alignment Self-Check 输出 | 回 Phase 1.5 或进入 Phase 5 |
| route 推荐已出但未执行 | Project Steward Report + Recommended Next Action | 报告后停止或按明确请求进入下游 |
| 存在阻塞 | Blocking Issues + 证据路径 / 命令输出 | 解除阻塞或分流对应 workflow |
| 闭环完成待下一步 | Current State + Gaps / Risks + Not Recommended Now | 推荐唯一下一动作或暂停 |

若多个状态同时成立，优先级：

```text

BLOCKED
  > OBSERVABILITY_INCIDENT_NEEDED with active user impact
  > BUG_REPORTED with high severity
  > SECURITY_PRIVACY_AUDIT_NEEDED
  > RELEASE_READINESS_NEEDED
  > AGENT_ASSET_MAINTENANCE_NEEDED
  > AGENT_ASSET_REVIEW_COMPLETED_WITH_RECOMMENDATIONS
  > AGENT_ASSET_CONTEXT_HEALTHY
  > READY_FOR_DELIVERY_CLOSEOUT
  > EXECUTION_IN_PROGRESS
  > READY_FOR_EXECUTION
  > SPEC_IN_PROGRESS
  > BUSINESS_MODEL_RISK
  > SSOT_NEEDS_REPAIR
  > NO_PROJECT_SSOT
  > READY_FOR_REVIEW
  > READY_FOR_SPEC
  > ARCHITECTURE_AUDIT_NEEDED
  > AGENT_CONTEXT_MISSING
  > SAFETY_BASELINE_MISSING
  > APPROVED_TASKS_NEED_ISSUES
  > LOOP_COMPLETE

```

例外：若 `/project-steward:BUSINESS_MODEL_RISK` 否定 active spec 上游，先归入 `/project-steward:BLOCKED` 或 `/project-steward:SSOT_NEEDS_REPAIR`，不得因 `/project-steward:SPEC_IN_PROGRESS` / `/project-steward:READY_FOR_EXECUTION` 更高而继续。

---

## 4. 阶段 4 — 差距、风险与阻塞点分析

输出前必须完成三类判断：

### 4.1 缺口 / 风险 / 阻塞

- **实施差量分析 (Implementation Delta Analysis)**：强制度量工程当前态与目标态的差量。计算公式：`Implementation Delta (Δ) = SSOT Blueprint (权威蓝图) - Verified Assets (已验证交付物)`。必须明确当前工程所处的成熟度阶段。
- **缺口 (Asset Void)**：基于上述差量，列出代码库中缺失的核心组件，以及其他交付态缺失（如 spec / 设计 / 任务拆分 / 验证 / 回滚 / bug 影响面 / 交付归档 / 商业证据 / issue tracker / 安全基线 / release readiness / security packet / observability packet）。
- **风险**：SSOT 漂移、scope creep、active spec 过多、任务上下文过重、测试缺失、数据 / 权限 / 安全 / 计费风险、artifacts 散落、代码与 spec 不同步、商业假设未验证却进入 spec / 实现、生产告警缺口、回滚不可验证。
- **硬阻塞**：Authoritative SSOT 不健康但仍要派生下游；active spec Approval 无效；用户目标与 spec 冲突；**发现历史或当前 active specs 存在严重设计缺陷、架构摩擦或过时（Project DRI 拥有直接阻塞并提出推翻/重构方案的权力，绝不机械执行陈旧任务）**；复杂 bug 缺复现且可能高影响；真实生产副作用无回滚方案；security / observability / release gate 缺事实源却准备上线。

### 4.2 SSOT 修复职责矩阵

| 场景 | 发现者 | 修复草案 owner | 批准后写入 | 下游 |
| ------ | -------- | ---------------- | ------------ | ------ |
| 历史/当前 Specs 存在架构缺陷或过时 | `/project-steward` (Project DRI) | `/project-steward` (提出推翻重组方案) | 用户批准后执行 | `/specs-write` (重写) |
| 项目定位 / 母本缺陷 | `/project-steward` | `/project-inception` | 用户批准后执行 | `/specs-write` |
| 术语 / ADR 冲突 | `/architecture-audit` / `/grill-with-docs` | `/grill-with-docs` | 用户批准后执行 | `/specs-write` |
| feature spec 派生前 SSOT 不健康 | `/specs-write` | `/project-inception` 或 `/grill-with-docs` | 用户批准后执行 | 回 `/specs-write` |
| bug 暴露 SSOT 错误 | `/bug-audit` | `/specs-write` 或 `/project-inception` | 用户批准后执行 | 修复 Task |

### 4.3 审计职责归属矩阵

| 场景 | 归属 | 边界 / 产物权限 | 下游 |
| ------ | ------ | ---------------- | ------ |
| 为当前 feature 派生 spec 所需的现状证据 | `/specs-write` Phase 1.5 | 只证明本 feature 的 REQ / DSN / TASK 可安全派生；不承接项目级审计 | `/specs-execute` |
| 项目级架构摩擦、浅模块、seam / interface 重塑 | `/architecture-audit` | 只输出 advisory interface / refactor sequence；不可直接执行，必须被 `/specs-write` 编入合同 | `/specs-write` |
| bug 影响面、严重性、根因假设、修复路线 | `/bug-audit` | 只做缺陷审计与修复路线；不深挖具体根因、不直接 patch | `diagnose` / `/specs-write` / `/specs-execute` |
| 商业闭环、付费主体、替代方案、工程 ROI 生死判断 | `/business-model-audit` | 只输出 Kill / Pivot / Validate / Proceed 裁定与验证计划；不写母本或 spec | `/project-inception` / `/specs-write` |
| 术语 / ADR / 领域文档冲突 | `/grill-with-docs` | 只更新普通领域文档或草拟权威修订；不改 feature spec，不静默改 Authoritative SSOT | `/specs-write` / `/project-inception` |
| 发布 readiness、部署、canary、smoke、rollback、release report | `/release-deploy` | 只由 release workflow 装配 release gate、部署计划、回滚与 smoke；project-steward 只路由 | `/specs-execute` / `/security-privacy-audit` / `/observability-incident` |
| 权限、密钥、PII、OAuth、支付、依赖供应链、外部攻击面 | `/security-privacy-audit` | 只由 security workflow 装配 security gate packet；project-steward 不替代威胁建模或批准 | `/specs-write` / `/specs-execute` / `/release-deploy` |
| 生产事故、用户影响、告警、runbook、log / metric / trace 缺口 | `/observability-incident` | 只由 observability workflow 分级、止血、runbook、incident packet；project-steward 不替代事故响应 | `/bug-audit` / `/release-deploy` |

---

## 5. 阶段 5 — 最优下一步执行决策

### 5.1 输出格式

每次必须输出以下结构：

```markdown
## 项目管家审计报告 (Project Steward Report)

## 想法/灵感锚点 (Idea Anchor)
<仅在本轮意图为 Idea 时保留 Phase 1.5 那段原话引用；其他意图下写 N/A>

## 首席责任人诊断 (DRI Diagnosis)

- <对项目架构健康度、现有 specs 质量及技术债的一针见血的独立评价，绝不机械汇报状态>

## 当前状态 (Current State)

- 状态标签 (State): /project-steward:<STATE>
- 置信度 (Confidence): <High | Medium | Low>
- 事实依据 (Evidence):
  - <file / directory / command / user quote>

## 交付态与母本对齐矩阵 (Delivery State & SSOT Alignment)

- 已实现能力 (Realized Capabilities): <基于 SSOT，当前已拥有 verified evidence 的核心资产或里程碑>
- 待实现差距 (Implementation Delta): <SSOT 中已定义，但当前库中表现为 Missing Asset 或 Untested 的组件>
- 工程完备度水平线 (Maturity Watermark): <当前工程所处的绝对阶段，如 Data Layer Ready / Critical Path Blocked / Release Candidate>

## 审计结论 (Outcome)

- <Route recommended | Waiting | Blocked | Loop complete>

## 阻塞问题 (Blocking Issues)

- <None 或具体阻塞>

## 差距与风险 (Gaps / Risks)

- <按重要性排序>

## 被推翻的规格 (Challenged / Invalidated Specs)

- <如果推翻了现有计划，列出被否定的规格及理由；否则填 N/A>

## 推荐下一步行动 (Recommended Next Action)

- 推荐动作 (Action): <唯一推荐动作>
- 推荐路由 (Route): </project-inception | /business-model-audit | /specs-write | /specs-execute | /release-deploy | /security-privacy-audit | /observability-incident | /architecture-audit | /grill-with-docs | /bug-audit | /issue-triage | /tasks-to-issues | /repo-agent-setup | /repo-safety-setup | review | diagnose | direct>
- 锚点贴合度 (Anchor fit): <一句话说明推荐动作为何贴合 Anchor，意图不为 Idea 时写 N/A>
- 决策依据 (Why this first): <原因>

## 路由动作与授权边界 (Route Action / Authorization Boundary)

- 路由动作 (Route Action): <CONTINUE_IN_WORKFLOW | WAIT_FOR_USER | REPORT_AND_STOP | CONFIRMED_ACTION>
- 授权范围 (Authorized scope): <report only | exact direct asset maintenance files | named downstream entry input>
- 未授权范围 (Not authorized): <business code / feature spec writing / tracker external write / real-world side effects / downstream workflow internal actions>

## 暂不推荐路径 (Not Recommended Now)

- <说明为什么不走其他看似合理路径>

## 下一步行动计划 (What I'm Going To Do Next)

- <一句话说明下一动作；是“报告后停”还是“立刻推进”>

## 质量门禁 (Gate)

- <N/A | 需要用户批准的问题>

```

### 5.2 分流规则

| 条件 | 推荐动作 |
| ------ | ---------- |
| 发现现有 Specs (active/done) 存在重大设计缺陷、与架构产生摩擦或逻辑过时 | 推荐推翻，报告 `/project-steward:SPECS_INVALIDATED`，等待确认重写 |
| SSOT 中明确定义了某项能力，但当前代码库与 Specs 中出现空白 (Asset Void) | 触发主动能力救济 (Proactive Capacity Remediation)，带入缺失上下文强制挂载下游 `/specs-write`，消除 Implementation Delta |
| 用户请求维护 workflow / skill / AGENTS.md / 代理规则 | direct asset maintenance（只限外科维护；跨文件重塑先输出计划） |
| 用户请求审查代理资产且只有非阻断性建议 | 报告 `/project-steward:AGENT_ASSET_REVIEW_COMPLETED_WITH_RECOMMENDATIONS`；不自动写入 |
| 用户请求把代理运行上下文应用到目标项目，且缺 issue tracker / 标签 / 领域文档规则 | `/repo-agent-setup` |
| 无母本 / 只有想法 | `/project-inception` |
| 商业产品方向但付费主体 / 替代方案 / MVP 投入依据不清 | `/business-model-audit` |
| 准备上线 / 回滚 / canary / smoke，或 release readiness / rollback plan / release report 缺口 | `/release-deploy` |
| 涉权限、密钥、PII、OAuth、支付、依赖供应链、外部攻击面，或 security gate packet 缺失 | `/security-privacy-audit` |
| 涉生产事故、用户影响、告警触发、runbook / log / metric / trace 缺口，或 observability gate packet 缺失 | `/observability-incident` |
| 母本不健康 | SSOT Repair；严重时 `/project-inception` 重建 |
| 已有健康母本 + 新功能 | `/specs-write` |
| 有架构摩擦但重构方向未审计 | `/architecture-audit` |
| spec 未写完 | 继续 `/specs-write` 当前 Phase |
| spec 已 Approved + Task Pending | `/specs-execute TASK-###` |
| Task 执行中断 | `/specs-execute` Resume |
| Task 全 Done + 未归档 | `/specs-execute` 交付收尾 |
| Approved tasks 需要外部分发 | `/tasks-to-issues` |
| issue tracker / 标签 / 领域文档规则缺失 | `/repo-agent-setup` |
| 本地安全基线缺失 | `/repo-safety-setup` |
| 已实现但未审查 | `review` |
| bug 影响面未知 | `/bug-audit` |
| bug 根因明确且小，且有最小复现或可写回归测试、无数据 / 权限 / 安全 / 计费 / SSOT / spec 影响 | `diagnose` / `tdd` 或 direct Small fix |
| 单一文件、无依赖牵连、无需架构决策的微型修补 | `Vibe Track` (微型变更直通车)，带入 Scope Guard 直通执行 |
| 用户只问解释 | 直接回答，不启动重 workflow |

`direct asset maintenance` 是 workflow / skill / `AGENTS.md` 的资产维护路径；不走 feature / spec flow。它只允许外科维护：每一处 diff 必须可追溯到用户请求；复杂跨文件重塑先输出计划；新增、删除、重命名或启停 workflow / skill 时必须同步 `AGENTS.md` 索引。执行时仍须遵守 `AGENTS.md` 的编辑安全、索引同步、目录契约与验证清单。

`direct Small fix` 只表示不启用重 workflow，不表示无纪律执行；仍必须满足 `/bug-audit` 的 small route 条件，并按 `diagnose` / `tdd` 的复现、回归测试与 Red → Green → Refactor 纪律处理。

### 5.3 自动推进规则

允许自动推进：

- 只读状态审计。
- 推荐下一步。
- 用户明确说“继续执行当前 approved task”，且唯一 active spec / unique pending task 可判定。
- 用户明确说“继续写当前 spec”，且当前 Phase 明确。

自动推进只允许当前 workflow 内继续，或恢复已批准 spec / task 的明确入口；不得把“唯一方向明确”解释为新开下游 workflow 内部动作、真实世界副作用、tracker 写入或 Authoritative SSOT 修改授权。

必须停下报告，不自动推进：

- 需要创建或修改 Authoritative SSOT。
- 多个可执行方向并列且无优先级证据。
- 新开 feature spec。
- 复杂 bug 可能有高影响面。
- 涉及生产数据、权限、计费、凭据或不可逆外部副作用。

---

## 6. 阶段 6 — 路由或交付接续

### 6.1 如果推荐进入其他 workflow

输出应包含：

- 当前 workflow-qualified state。
- 推荐 workflow。
- 入口参数。
- 需要读取的最小上下文。
- 不应读取的低价值上下文。
- 若继续执行，第一步应该做什么。

示例：

```text

Current state: /project-steward:READY_FOR_EXECUTION
Recommended route: /specs-execute TASK-003
Required context: docs/specs/active/`<feature>`/handoff-payload.yaml + tasks.md TASK-003 + Context Required P0
Do not start a new spec: current active spec still has Pending work.

```

### 6.2 如果当前闭环完成

推荐下一轮方向：

- 新 feature。
- 技术债修复。
- bug audit。
- 文档 / SSOT 修复。
- 发布 / 归档。
- 暂停，无下一步。

必须说明依据。

---

## 7. 禁用行为

- 绝对禁止机械式执行陈旧或存在设计缺陷的 specs 队列。遇到不合理的 specs 必须果断阻塞并提出重组/推翻建议。
- 绝对禁止流于表面的浅层审计，必须严格落实统一 14 面审计的强证据要求（如真实 DB readback）。
- 不把“我没看见”当成“不存在”。
- 不用 grep 命中冒充全局理解。
- 不在没有健康 SSOT 时强开 feature spec。
- 不在 Task 未 Done / 未归档时跳去新 feature。
- 不静默修改母本 / L1 SSOT。
- 不把复杂 bug 直接当 Small fix。
- 不替用户做 Strategy / Critical Design / Real-World Side Effect 类裁决。
- 不输出“都挺好，继续吧”这类无证据结论。
- 不重写 / 总结 / 推演 Idea Anchor；只能原话逐字引用。
- 不在 Idea 路径上反过来 grilling 用户；需要明确化时只复述一句 + 一个确认问题。
- 不在存在健康母本时重启 `/project-inception`；该走 `/specs-write`。

---

## 8. 快速自检清单

报告前自检：

- [ ] 你是否识别了用户当前意图类型？
- [ ] 若意图为 Idea，你是否逐字锁定了 Anchor、走过 SSOT 优先路径选择、做了 Alignment Self-Check？
- [ ] 你是否查过母本 / L1 SSOT？
- [ ] 你是否查过 active / done spec 状态，并且**批判性地评估了它们的技术合理性（而不只是盲目执行）**？
- [ ] 你是否判断了当前唯一主状态？
- [ ] 你是否列出证据而不是凭感觉？
- [ ] 你是否给出唯一推荐下一步？
- [ ] 你是否说明了为什么不走其他路径？
- [ ] 你是否避免直接越权执行？

## 支撑资源

- [decision-matrix.md](./references/decision-matrix.md)
- [unified-14-surface-audit.md](./protocols/unified-14-surface-audit.md)
