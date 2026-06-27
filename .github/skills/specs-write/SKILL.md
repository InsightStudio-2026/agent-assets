---
name: specs-write
description: 将模糊需求转化为可审查、可实现、可追溯的分阶段规格合同；仅写 Spec，不编码。Use when user wants to write a spec, plan a feature, create design document, transform requirements into contract, or says 写规格/需求分析/技术方案/设计文档/功能规划。
argument-hint: "要做什么功能？"
---


# /specs-write · 规格编写

**核心意义与定位**：把一个模糊需求变成可审查、可实现、可验证、可追溯的 Spec 合同。本工作流的设计范式基于：在确立了高信度的母本 SSOT 锚点后，通过系统性的“自上而下派生”和“自下而上现状核验”双轨闭环，消除实现时的不确定性，提供确定性的工程执行合同。

**边界**：只写 Spec 合同。不写业务代码、不执行迁移、不改真实数据库。

**斜杠命令**：`/specs-write`

**配对实现 workflow**：`/specs-execute`

---

## 伴随文档 · 按需阅读

主体仅保留控制流骨架。详细约束 / 模板 / 矩阵 / 自检清单已抽到 `./`。每个 Phase / 子流程入口的 **MUST read**指令是硬规则——不读 = 违反防 1-5（SSOT 撞裂 / TDD 作弊 / Revert 雪崩 / MCP 幻觉 / 注意力稀释）。调度索引（短名均指本目录下的对应文件名）：

- **方法论内核 / 首次接触 / 术语存疑**：read `methodology-kernel.md`（一页内核：9 层语义 + 7 种 delta + active/done 三条件 + 状态机锚点）+ `terminology.md`（完整术语字典）
- **入口分流 / 用户请求该走哪条路径**：read `entry-decision-tree.md`（6 个判定 + 8 类规则表 + 30+ 边界场景查询）
- **Phase 执行期反模式查询 / 常见路障**：read `cross-cutting.md §6`（B-001 ~ B-015 反模式表）
- **跨 workflow Hard-gate / DAG / Revert Graph 横切协议**：read `gate-dag-protocol.md`（HG-*/ DAG-N-* / DAG-E-*/ DAG-D-* ID 体系 + 12 workflow 投影对照表）
- **各步进核心模板**：read `templates/{maturity-intake|charter|audit|decisions|requirements|design|tasks}.md`（落对应文件前必读）
- **步进 3 (Audit)**：另读 `appendix.md §A.4`
- **步进 5 (Requirements)**：另读 `cross-cutting.md §3.3`（EARS / BDD / TDD 三轨配对）
- **步进 6 (Design)**：另读 `design-rules.md` + `cross-cutting.md §5` + `plan-delta-merge-protocol.md §1`
- **步进 7 (Tasks)**：另读 `task-rules.md` + `appendix.md §A.1-A.6` + `plan-delta-merge-protocol.md §2`
- **步进 8 (Handoff)**：read `cross-cutting.md §4` + `plan-delta-merge-protocol.md §3`（Spec Contract Schema · handoff-payload.yaml + merge-back queue）
- **任意阶段 Approval / Gate**：read `cross-cutting.md §2`（防伪协议）
- **派生 / 追溯协议存疑**：read `cross-cutting.md §1.4`（A-E 关系）
- **每步进交付输出 / 调度参考 / 使用示例**：read `orchestration.md`
- **任一步进入下阶段前**：read `stop-conditions.md`
- **每步进出口自检**：read `self-check.md` 对应小节
- **项目级槽位 / Shell / INV-* 示例**：read `project-adapter.md`
- **执行端反流 / Reflections GC / active→done 迁移**：read `appendix.md §A.7`
- **任意阶段违规自检**：read `forbidden-actions.md`

---

## 懒加载契约

- **MUST read**: `./decision-matrix.md`
- 开始判定或执行步进流程前，必须完整懒加载上述细节。

---

## 0. 总则

### 0.1 核心原则（12 条）

1. **阶段隔离**· 需求不谈方案；设计不拆任务；任务不改需求

2.**上游授权** · 下游不超上游；冲突命中 Gate A/B/C 或 Spec Breach 必回上游（对应 `HG-STRAT-*` / `HG-DESIGN-*` / `HG-IMPL-*` 三类硬闸）；纯实现级 AI-DRI 自决留痕（`S-HG-1 GATE_NOT_REQUIRED`）

1. **稳定锚点** · 只用 ID 引用（SRC/REQ/AC/US/DSN-`<domain>`/EXIST-*/TASK/INV-*）；禁行号（除归档快照）
2. **强制复述**· 执行 Task 前必引用上游锚点原文关键句

5.**最小够用**· Small 不写 Spec；Medium 可合并；Large 走完整三文件
6.**中文主导**· spec 中文；ID / slug / 目录名英文
7.**派生优先**· 从已批准 SSOT 派生，引用而非复述；冲突回流上游不就地妥协
8.**现状先于规划** · Hybrid / Brownfield 必先 Phase 1.5；反向标识 EXIST-*；禁"假装项目是空的"

1. **高质量交付压力**· 主动推 spec 向可执行 / 可验证 / 可交付；不以速度换债务

10.**高自决必须高审计**· 不用 grep / 片段 / 主观猜测替代 14 面审计证据
11.**成熟度感知**· Seed/Init 必做 Baseline Survey；Greenfield审基础设施 + SSOT；Hybrid/Brownfield 进 14 面审计
12.**SSOT 不盲从**· `Needs Repair` / `Unfit As Source` 不得继续派生 feature spec

### 0.2 适用范围

-**必走**：新功能（新模块 / 新页面 / 新接口 / 新数据流）/ 跨模块重构 / 架构边界变动 / Schema / API / 协议 / 事件契约变更 / 权限 / 计费 / 合规 / 数据治理 / AI/LLM pipeline / Agent / 长链路任务 / 复杂 Bug（根因不明、影响面大）。

- **跳过**：错字 / 文档勘误 / 单文件小 bug / 用户已给出完整代码级指令 / 纯查询 / 解释 / 阅读代码。

### 0.3 复杂度分级

- **Small**→ 不启用 workflow，直接处理

-**Medium**→ ① `requirements.md` + `tasks.md`（跳设计，标 `Mode: Medium (design skipped:`<reason>`)`）或 ② 单文件 `spec.md`（标 `Mode: Medium (single-file:`<reason>`)`；内部仍保留 Requirements / Design / Tasks 三段与 Decision Gate 判定；仅限单人小特性 / 设计无替代 / 不涉 Schema/API 外部消费者）
-**Large**→ 完整三文件

### 0.4 目录与文件归仓

- `<specs_root>` 查找顺序：`docs/specs/` → `specs/`。

-**分仓规则**（强制）：

- `active/<feature-slug>/`：进行中（步进 1 必在此落地不得平铺）。
- `done/<feature-slug>/`：完结后归仓。
- **完结条件**：
  1. `tasks.md` 内全 Task 标为 `Done`。
  2. `docs/specs/project archives/delivery-log.md` 内已追加本条 feature 的交付记录。
  3. `handoff-payload.yaml` 状态标为 `status: Acknowledged`。
  - 满足条件后使用 `git mv` 移动并更新全仓所有跨文档引用。
- **`artifacts/` 子目录硬约束**：spec 执行期任何 Task 产生的非源码副产物（plan / verify / cost ledger / quarantine / dry-run / 4 闸口报告 / drift 报告）必写入本目录或子目录，禁项目根 `reports/` / `tmp/` / `output/`。

> **"Handoff" 同名异义**：本 workflow 步进 8 (Handoff) = **交接物产出**（handoff-payload.yaml + 人读简报）；`/specs-execute` Phase 9 Handoff = **完工交付**（TASK 完工报告 + 下一 Task 提示）。

### 0.5 与其它审计类工作流的边界

步进 3 (Audit) 仅证明本 feature 的 REQ / DSN / TASK 能从上游和现状安全派生；它不是独立的全局审计。
当在规格编写期间遭遇系统性障碍或不同场景时，请按照下表分流：

| 场景 | 归属 |
| --- | --- |
| 系统状态不清、现存计划有严重摩擦无法继续，或需撤销/推翻 | `/project-steward` (退回给 DRI 全局诊断) |
| 本 feature 影响面内的代码、DB、API、UI、SSOT 证据 | `/specs-write` 步进 3 (Audit) |
| 项目级架构摩擦、浅模块、seam / interface 重塑 | `/architecture-audit` |
| bug 影响面、严重性、根因假设、修复路线 | `/bug-audit` |
| 术语 / ADR / 领域文档冲突 | `/grill-with-docs` |
| 项目定位、目标用户、MVP 或母本级缺陷 | `/project-inception` |
| 商业闭环、付费主体、替代方案、工程 ROI 生死判断 | `/business-model-audit` |

若 步进 3 (Audit) 发现超出本 feature 的问题，只记录阻塞证据与推荐 route；不得吞进当前 spec。

---

## 1. 步进 1 — 项目成熟度与权威 SSOT 体检 (Intake)

**MUST read** `templates/maturity-intake.md`。

### 1.1 输入

- 用户提出的 feature 意图或设想（通常落地于游离态的 `docs/Idea.md`。若该文件不存在或为空，则基于你对 母本、类SSOT 的全景目标以及当前代码状态的理解，主动洞察出“下一步该做什么”，**由你内生推演**出原始想法并起草建立它）。
- 当前仓库 of L1 SSOT（`docs/blueprints/母本.md`等）及已有规格。

### 1.2 执行要点

1. 判定项目成熟度模式：**Seed / Init**（初始化期）/ **Greenfield**（全新 + 物理隔离）/ **Hybrid**（部分新建 + 部分扩展）/ **Brownfield**（已有大量相关代码）。
2. 执行 SSOT 权威母本的健康度检查（健康 / Needs Repair / Unfit as Source 等）。
3. 产出 `maturity-intake.md`，包含特殊汇报字段（Project Maturity / Audit Profile / SSOT Health / Confidence / Decision / Blocking Issues / SSOT Stewardship Suggestions）。

### 1.3 特殊汇报字段

`Project Maturity` / `Audit Profile` / `SSOT Health` / `Confidence` / `Decision` / `Blocking Issues` / `SSOT Stewardship Suggestions`

---

## 2. 步进 2 — 构想注入与项目宪章 (Charter)

**MUST read** `templates/charter.md`。

### 2.1 输入

- `maturity-intake.md`
- 用户的原始 Idea（通常来自 `docs/Idea.md`。若仍未落盘，请继续基于你对系统差距的洞察进行内生补全，直至具备写宪章的足够信息。此阶段同样禁止调用 grill-me）。

### 2.2 执行要点

1. 将用户的模糊问题压成可审查的“工程合宪”，轻量化用 `Status: Acknowledged` 不走完整 Decision Gate。
2. 锁定 SRC-### 权威来源与不变量（INV-BAN-*/ INV-LIM-* / INV-SEC-*）。
3. 定义复杂度分级与范围边界（In-scope / Out of Charter），区分 L-STRAT / L-DESIGN / L-IMPL / L-OPS 决策。
4. 产出 `charter.md`。

### 2.3 特殊汇报字段

`Mode` + `specs_root` + `slug` + `Open Questions` + `Charter 摘要`

---

## 3. 步进 3 — Spec 派生审计 (Audit, 仅用于 Hybrid / Brownfield)

**MUST read** `templates/audit.md` + `references/appendix.md §A.4` + `../project-steward/protocols/unified-14-surface-audit.md`。

### 3.1 输入

- `charter.md`
- 本 feature 影响范围内的物理代码、数据库及接口现状。

### 3.2 执行要点

1. 开展 Feature-Scoped 14 面审计（基础 12 面 + 强证据 2 面）。
2. 对现状做 `EXIST-*` 反向标识与硬验证（`Verified By` 留痕），提供真实数据库（通过 SQL/PostgreSQL MCP）及 SSOT 查询证据。
3. 对每个冲突或现状进行 Reuse / Extend / Replace / Deprecate 决策判定。
4. 核验 Audit Depth Gate（Overall Confidence ≥ 80% + Unknowns 清零）。
5. 产出 `audit.md`。

### 3.3 特殊汇报字段

`EXIST 数量分布` + `Conflicts 数` + `Audit Depth Gate 结论` + `Overall Confidence` + `Blocking Unknowns`

---

## 4. 步进 4 — 深度拷问与关键决策 (Decisions)

**MUST read** `templates/decisions.md`。

### 4.1 输入

- 游离态的 `docs/Idea.md` 草稿（原始想法。这是高压定盘的前提，若经过前序环节依然缺失该事实源，你必须基于对母本的理解、审计结果的差值与目标期望间的模糊地带，由你自己**内生推演**出一系列架构决策树与备选方案，通过 `grill-me` 抛给用户拍板，并将这些洞察落入此文件）。
- `audit.md` (如有，用于提供约束现状)

### 4.2 执行要点

1. 吸收全局草稿板 `docs/Idea.md` 中的想法，结合 `audit.md` 摸底发现的技术债与约束。
2. 触发 `grill-me` 深度拷问，将所有架构折中、边缘 case、未决事项列为 `[ ]` 决策点。
3. 待所有决策点完成 `[x]` 定盘后，正式产出 `decisions.md`（作为附着态的决议宗卷）。
4. 清空全局草稿板 `docs/Idea.md` 以备孵化下一个特性。

### 4.3 特殊汇报字段

`决策点总数` + `[x] 已定盘数` + `核心折中方向`

---

## 5. 步进 5 — 需求设计 (Requirements)

**MUST read**`templates/requirements.md` + `references/cross-cutting.md §3.3`。

### 5.1 输入

- `charter.md`
- `audit.md` (如有)
- `decisions.md`

### 5.2 执行要点

1. 将“做什么”压到不可再压。
2. 派生 `REQ` 需求、`AC`（Acceptance Criteria，使用 EARS 语法）及 `BDD Scenario`。
3. 建立三轨互查配对，保证无孤立需求或用例。
4. 建立 Derivation Map 关系对齐。
5. 产出 `requirements.md`。

### 5.3 特殊汇报字段

`US 数` + `REQ 数` + `AC 数` + `BDD Scenario 数` + `Derivation Map 概要`

---

## 6. 步进 6 — 详细设计 (Design)**MUST read** `templates/design.md` + `protocols/design-rules.md` + `references/cross-cutting.md §5` + `protocols/plan-delta-merge-protocol.md §1`

### 6.1 输入

- `requirements.md`

### 6.2 执行要点

1. 定义稳定设计契约（`DSN-*`），涵盖数据库 schema、接口、并发锁、异常策略、API 合约等。
2. 将设计与已有的 EXIST-* 模块进行 Reuse vs Net New 关联。
3. 对涉及 DDL/DML 迁移或 API 重塑的变动，在 `Plan Artifacts Register` 中登记。
4. 产出 `design.md`。

### 6.3 特殊汇报字段

`DSN-* ID 列表` (按 domain) + `跨边界 DSN 数` + `Reuse vs New 摘要` + `Migration 命中数` + `Plan Artifacts Register 摘要` + `风险点`

---

## 7. 步进 7 — 任务拆解 (Tasks)

**MUST read** `templates/tasks.md` + `protocols/task-rules.md` + `references/appendix.md §附录 · 高级防线（A.1-A.7.5）` + `protocols/plan-delta-merge-protocol.md §2`。

### 7.1 输入

- `design.md`

### 7.2 执行要点

1. 将设计转译为**单 Task 可独立完成**（工期不超过 1 day）的 Red-Green-Refactor 任务队列。
2. 规定 Task 的 Relation to Existing delta 投影关系。
3. 为每个 Task 定义精确 of Test Anchors、Verification 测试运行命令、DoD 与 Rollback 策略。
4. 产出 `tasks.md`。

### 7.3 特殊汇报字段

`Task 数` + `Mode` + `Existing Touches 统计` + `跨边界 Task 数` + `Delta Projection 风险` + `待人审项`

---

## 8. 步进 8 — 发版与交付 (Handoff)

**MUST read**`references/cross-cutting.md` + `protocols/plan-delta-merge-protocol.md §3`。

### 8.1 输入

- 整套 L2 规格合同。

### 8.2 执行要点

1. 准备 `/specs-execute` 可无缝消费的 `handoff-payload.yaml`（含 `first_task`、`critical_contracts` 跨边界 DSN 汇总及 invariants）。
2. 在 Handoff 报告中输出人读简报与决策成果。
3. 将 state 标为 `/specs-write:HANDOFF_READY`，等待用户进入 `/specs-execute TASK-001`。

### 8.3 特殊汇报字段

`State = /specs-write:HANDOFF_READY` + `Outcome = <Handoff ready | Approval pending | External audit required | Blocked>` + `first_task ID` + `critical_contracts 数` + `invariants 数` + `reflections 存活条数` + `Merge Queue 条数` + `drift 警告数`

---

## 9. 状态机与路由控制

### 9.1 状态转移表（State Authority / Route Action）

`/specs-write` 工作流的执行遵循以下严格的状态机流转，每个状态均有其判定权威与推荐路由动作：

| 源状态 | 目标状态 | 判定权威 (Authority) | 状态动作 (Route Action) | 说明 |
| :--- | :--- | :--- | :--- | :--- |
| `/specs-write:INIT` | `/specs-write:PHASE0_INTAKE` | AI-DRI 自动流转 | `CONTINUE_IN_WORKFLOW` | feature 启动，自动进入步进 1 进行成熟度与 SSOT 健康度体检 |
| `/specs-write:PHASE0_INTAKE` | `/specs-write:CHARTER_READY` | AI-DRI 判定 SSOT 正常 | `CONTINUE_IN_WORKFLOW` | 步进 1 体检通过，自动推进到 Charter 起草阶段 |
| `/specs-write:PHASE0_INTAKE` | `/specs-write:APPROVAL_PENDING` | 母本或战略方向存疑 | `WAIT_FOR_USER` | 命中了 Gate A，暂停并请求用户裁决战略和宪章方向 |
| `/specs-write:PHASE0_INTAKE` | `/specs-write:NO_HEALTHY_SSOT` | AI-DRI 判定母本不健康 | `REPORT_AND_STOP` | 母本存在严重健康度缺陷（Needs Repair/Unfit），阻断并提示先运行 SSOT 修复 |
| `/specs-write:CHARTER_READY` | `/specs-write:AUDIT_READY` | AI-DRI 根据项目模式判定 | `CONTINUE_IN_WORKFLOW` | Hybrid/Brownfield 模式下，宪章通过并自动推进至步进 3 (Audit) |
| `/specs-write:CHARTER_READY` | `/specs-write:DECISIONS_READY` | AI-DRI 根据项目模式判定 | `CONTINUE_IN_WORKFLOW` | Seed/Greenfield 模式下，跳过步进 3，直接进入步进 4 (Decisions) |
| `/specs-write:AUDIT_READY` | `/specs-write:DECISIONS_READY` | AI-DRI 确认 Audit Depth 达标 | `CONTINUE_IN_WORKFLOW` | Audit 深度与信度达标，Unknowns 清零，推进到步进 4 (Decisions) |
| `/specs-write:DECISIONS_READY` | `/specs-write:REQUIREMENTS_READY` | AI-DRI/Grill-Me 确认所有节点定盘 | `CONTINUE_IN_WORKFLOW` | 拷问决策树全部 [x] 定盘，推进到需求定义 |
| `/specs-write:REQUIREMENTS_READY` | `/specs-write:DESIGN_READY` | AI-DRI 自动流转 | `CONTINUE_IN_WORKFLOW` | 需求与 AC/BDD 用例起草完毕，流转到设计层契约定义（Medium 模式若跳过设计则流向 TASKS） |
| `/specs-write:DESIGN_READY` | `/specs-write:TASKS_READY` | AI-DRI 自动流转 | `CONTINUE_IN_WORKFLOW` | 详细设计契约就绪，流转到纵向切片任务拆解 |
| `/specs-write:TASKS_READY` | `/specs-write:HANDOFF_READY` | AI-DRI 验证全套规格完备 | `CONTINUE_IN_WORKFLOW` | 规格五件套通过自检，生成交付 payloads，进入 Handoff 状态 |
| `/specs-write:HANDOFF_READY` | `/specs-execute:INIT` | **用户批准 (Gate B/C)** | `CONFIRMED_ACTION` | 用户批准 Handoff 简报后，授权流转到执行端，开始执行首个 Task |
| 任意状态 | `/specs-write:BLOCKED` | 遇到未知严重技术债或多路径分歧 | `REPORT_AND_STOP` | 阻断推进，报告详细障碍，流转给 `/project-steward` 进行 DRI 宏观诊断 |

### 9.2 可中断流程恢复源（Resume Source）

本工作流支持因以下事件中断：用户暂停审查、Gate 审批阻断、或发现 SSOT 质量问题回流修复。

-**事实源与恢复机制**：

- 规格执行过程的状态与断点记录完全在物理文件 **`docs/specs/active/<feature-slug>/_status.md`** 中进行自解释与持久化（SSOT 状态机事实源）。
- 当中断恢复或重进会话时，AI-DRI 必须首先 read `_status.md` 确定其填充进度、未决 Gate 与 Feature 模式，直接从中断的步进节点重新加载上下文并继续推进，无需依赖任何临时外部缓存。

---

## 10. 禁用行为

| 禁止项 | 原因 |
| --- | --- |
| 不写业务代码 / 脚本 | `/specs-write` 仅限于规格编写与设计，不承接代码实现 |
| 不改动真实数据库 / 执行迁移 | 数据库与架构修改归属于实现期或专项流程，本阶段只定义设计契约 |
| 不静默修改 Authoritative SSOT | 母本及战略修订必须通过 Strategy Gate 获得用户明确批准 |
| 不在没有健康母本时强开 feature spec | 保证上游输入健康是派生 spec 的前置条件 |
| 不在遇到全局阻断或系统状态不清时死磕 | 必须以 BLOCKED 状态跳出，交还给 `/project-steward` 重新进行 DRI 研判 |

---

## 11. 快速自检清单

交付前自检：

- [ ] 是否已加载并执行了 Phase 0 项目成熟度与 SSOT 健康检查？
- [ ] 派生的 Feature Spec 目录结构是否严格遵循 active/done 二级分仓？
- [ ] Requirements 是否确保每一项都与 Acceptance Criteria 及 BDD Scenario 双向对齐？
- [ ] Design 是否定义了清晰的系统契约，且 INV 标识齐全？
- [ ] Tasks 队列是否符合单日纵向切片要求，且 Relation to Existing delta 映射完毕？
- [ ] Handoff 阶段是否已为 first_task 生成了完备 of Test Anchors 与 Critical Contracts？
- [ ] 每步进出口是否均已按照 `self-check.md` 进行勾验？

## 支撑资源

- [appendix.md](./references/appendix.md)
- [cross-cutting.md](./references/cross-cutting.md)
- [decision-matrix.md](./references/decision-matrix.md)
- [design-rules.md](./protocols/design-rules.md)
- [entry-decision-tree.md](./protocols/entry-decision-tree.md)
- [forbidden-actions.md](./protocols/forbidden-actions.md)
- [gate-dag-protocol.md](./protocols/gate-dag-protocol.md)
- [methodology-kernel.md](./protocols/methodology-kernel.md)
- [orchestration.md](./protocols/orchestration.md)
- [plan-delta-merge-protocol.md](./protocols/plan-delta-merge-protocol.md)
- [project-adapter.md](./references/project-adapter.md)
- [self-check.md](./references/self-check.md)
- [stop-conditions.md](./protocols/stop-conditions.md)
- [task-rules.md](./protocols/task-rules.md)
- [terminology.md](./references/terminology.md)
