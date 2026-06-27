---
name: grill-me
description: >
  对用户的计划、设计、术语或文档进行高压追问，沿决策树逐分支澄清，直到达成共享理解。
  覆盖两类场景：设计方案拷问 + 术语文档守护（沉淀 CONTEXT.md / ADR）。
  Use when user wants to stress-test a plan, get grilled on their design, clarify terminology,
  mentions "grill me" / "grill with docs", or asks 压测方案/拷问设计/追问我/术语冲突/文档守护。
---

# 拷问计划（grill-me）

通过引用全局统一的 [unified-14-surface-audit.md](../project-steward/protocols/unified-14-surface-audit.md) 对要评估的方案执行全景现状审计，识别方案与项目的 Gap 和技术债。根据审计结果为方案动态量身定制专属的"拷问树"。

本技能是一个**上下文感知、高度解耦**的通用高压推演引擎。它的目标持久化位置由其被调用的上下文（Context）决定：

1. **Context 1：临时/游离态探索**：纯粹为了理清架构争论、或未立项的想法孵化，结果落盘至草稿板 `docs/Idea.md` 或临时 scratch 文件。
2. **Context 2：立项前夜 (Pre-Inception)**：为形成商业与架构锚点，落盘至相关的项目草稿或由 `/project-inception` 指定的临时文件。
3. **Context 3：规格派生 (Specs-Write 附着态)**：作为定盘工具被调用时，落盘至专属的 `decisions.md`。
4. **Context 4：专项审计 (Bug/Arch)**：在 `/bug-audit` 或 `/architecture-audit` 中辅助深度根因追问，结果落盘至对应的审计报告中。

## 0. 触发与临界路由

| ID | 前置条件 | 匹配动作 | 下一步/目标路由 | 备注 |
| ---- | ---------- | ---------- | ----------------- | ------ |
| R-ROUTE-GRILL-1 | 用户显式提及 `grill-me` 技能或输入 `/grill-me` | 启用本技能 | 进入 Phase 1 (14面现状审计) | 显式入口 |
| R-ROUTE-GRILL-2 | 需要对架构方案、复杂重构、或关键 Feature 计划进行深度评估 | 建议或自动启用本技能 | 进入 Phase 1 (14面现状审计) | 计划压测 |
| R-ROUTE-GRILL-3 | 问题纯属 L-IMPL (实现级) 或 L-ROUTINE (例行级) 细节，且已有明确的最佳实践 | 降级自决，不启用本技能 | 按照开发协议自决执行，并在交付时简报 | 避免无意义发问 |
| R-ROUTE-GRILL-4 | 发现计划中涉及 L-STRAT 战略变化或全新业务模型 | 升级路由 | 路由至 `/business-model-audit` 或 `/project-inception` | 战略级偏离 |
| R-ROUTE-GRILL-5 | 发现计划涉及复杂的跨模块契约、新引入依赖或数据库 Schema 级重构 | 升级路由 | 路由至 `/specs-write` 编写规格合同 | 规格化治理 |

---

## Phase 1 — 现状审计（依赖注入优先）

### 为避免与上游流程发生死锁和重复劳动，你必须先判断当前工作流状态

- **附着态 (已被 /specs-write 调用)**：直接消费上游在步进 3 产出的 `audit.md`，**跳过**以下 14 面审计动作，直接进入 Phase 2。
- **游离态 (无上游输入独立调用)**：你必须依据待估方案，完全套用 [unified-14-surface-audit.md](../project-steward/protocols/unified-14-surface-audit.md) 中的 Unified 14-Surface Audit 准则开展现状审计：

1. **五阶拓扑序审计**：
   - 严格按照从第一阶（文档 SSOT 面、历史面）到第五阶的依赖关系进行审计。
   - 使用真实工具（MCP/CLI）寻找强证据支持，校验诸如 **真实数据库面**（检测 Drift）及 **契约与接口面**等关键位置，严禁主观脑补。

2.**提炼审计 GAP 与 Debt**：

- 梳理出该方案会影响到哪些物理文件、数据表、接口端点。
- 找出可能对该方案产生阻碍、存在脏数据或缺失回归测试缝隙的受影响表面。

---

## Phase 2 — 动态构建专属拷问树并落盘

### 严禁直接预定义或套用死板的拷问维度。必须根据 Phase 1 审计出的实际 Gap，为当前方案量身定制专属的“拷问树”大纲，并依据当前所处的调用上下文（Context），将大纲动态写入对应的目标文件中（如：`Idea.md`, `decisions.md`, `bug-audit-report.md` 或由用户/上游指定的其他草稿）

1. **设计专属决策点（拷问树）**：
   - 针对审计出 Gap 的表面（例如发现真实数据库有 Drift，或者契约面接口缺少强类型限制），动态归纳出 3–5 个最有针对性的拷问决策点（命名为 `[D-1]` 到 `[D-N]`）。
   - 按决策所有权矩阵（DOM）对决策点进行判级（L-DESIGN / L-STRAT）。
2. **落盘持久化契约**：
   - 将审计摘要和拷问树写入对应的文档。写入格式如下：

   ```markdown
   # [方案/计划名称] 现状审计与拷问决策记录
   
   ## 1. 统一 14 面审计 Gap 摘要

   - **[受影响表面编号 & 名称]**: [审计发现的 GAP、数据证据及技术债现状]
   - **[受影响表面编号 & 名称]**: [详细说明对本方案的潜在阻碍]
   
   ## 2. 拷问树决策状态

   - `[ ]` [D-1: 决策点名称] (分类：L-DESIGN / L-STRAT)
   - `[ ]` [D-2: 决策点名称] (分类：L-DESIGN / L-STRAT)
   
   ---
   ## 3. 决策过程详情
   <!-- 详细的提问、推荐方案和用户共识将追加在下方 -->

   ```

---

## Phase 3 — 强贴合项目的高质量推荐答案

对于大纲中列出的每一个拷问决策点，在提问时你必须同时给出一个**强推荐答案**，该推荐答案必须满足：

1. **项目特异性（Project Specificity）**：
   - 引用项目中已有的具体文件及行号（使用 markdown 相对链接，如 `[base.py](backend/app/models/base.py#L12-L35)`），说明：“推荐仿照该处的 X 模式来实现本功能”。
2. **具象化草案（Concrete Drafts）**：
   - 必须给出立即可用的代码片段（例如具体的 TypeScript/Python 装饰器、Pydantic Schema、SQL 迁移语句等）。
3. **权衡说明（Trade-offs）**：
   - 简要陈述推荐方案与备选方案（如果有，最多 2 个）的代价对比（如：实现复杂度 vs. 运行效率 vs. 维护成本）。
4. **决策等级划分（DOM Binding）**：
   - **L-IMPL (实现级) 推荐**：直接以“我计划默认采用此实现，若您无异议，下一轮我将直接进入该路径，不阻塞推进”的形式告知。
   - **L-DESIGN / L-STRAT (设计/战略级) 推荐**：必须明确指出“这需要您在 A、B、C 方案中进行选择或授权”，等待用户确认。

---

## Phase 4 — 持久化交互与共识更新（Docs Up-to-Date）

1. **单步深入（One-Question-at-a-Time）**：
   - 严格一次只问一个最核心、最阻碍下一步的问题。绝对禁止一次性抛出 5 个以上问题的长表单。
2. **同步更新文档**：
   - 每一轮提问，使用文件编辑工具将提问内容、推荐代码/配置草案追加到目标文档的 `## 3. 决策过程详情` 中。
3. **闭环用户确认**：
   - 当用户对拷问做出反馈（或直接批准推荐方案）后，必须使用文件编辑工具：
     - 将 `## 2. 拷问树决策状态` 中对应的项从 `[ ]` 改为 `[x]`。
     - 在详情处记录最终达成的共识设计（Approved Design）及回滚锚点。
   - 重复此步骤，直到拷问树所有节点均变为 `[x]`。当所有共识达成后，**将控制权交还给触发本次拷问的用户或上游 Workflow**（例如，提示“决策树已定盘，是否继续由 /specs-write 派生需求”），由其决定下一步流转方向。

---

## 文档与术语守护（原 grill-with-docs）

> 以下内容来自原 /grill-with-docs workflow，合并入 grill-me。侧重术语挑战、领域语言澄清、CONTEXT.md/ADR 沉淀。

## /grill-with-docs · 文档拷问

**定位**：把一段计划放在领域语言下打磨。挑战术语、解决冲突，把稳定领域语言沉淀进 `CONTEXT.md`，把重大架构决策沉淀进 `docs/adr/`。

**边界**：只更新领域文档（词表、ADR）；若术语 / ADR / 领域关系冲突需要触及 L1 SSOT / standards，只能先给 Proposed Patch，获用户明确批准后按批准范围应用；不替代 `/specs-write` 写需求与设计，不写业务代码，不静默改 Authoritative SSOT 中尚未授权的章节。

**SSOT 修复边界**：术语、关系、ADR 冲突由本 workflow 处理；项目定位 / MVP / 目标用户级修复回 `/project-inception`；feature spec 派生错误回 `/specs-write`。

**斜杠命令**：`/grill-with-docs`

**别名声明**：`<gwd>` = `./`（grill-with-docs 已合并至本 skill）。

---

## 懒加载契约

- **MUST read**: `./decision-matrix.md`
- 开始判定或执行 Phase 流程前，必须完整懒加载上述细节。

---

## 1. 工作原则

1. **一问一答**：每次只问一个具体问题，等用户回答再继续。
2. **能查代码就先查代码**：术语含义、关系判定能从代码或文档读出的，不要问用户。
3. **先挑战，再记录**：术语冲突先解决，再决定写不写下来。
4. **文档懒创建**：目标项目只有第一次需要时才创建 `CONTEXT.md` / `docs/adr/`；agent assets 仓库不创建。
5. **不动权威**：发现冲突涉及 Authoritative SSOT，提出修订草案，等用户批准再改。

### 1.1 文档权威等级

| 文档类型 | 本 workflow 可直接改？ | 条件 |
| ---------- | ------------------------ | ------ |
| 普通 `CONTEXT.md` | 小补丁可以 | 目标项目中达成术语共识后更新；新建或大改需等待批准 |
| ADR | 可以建议 / 创建 | 目标项目中满足三条 ADR 条件 |
| L1 SSOT / 母本 | 不可静默改 | 只给 `Proposed SSOT Patch` |
| `.github/standards` | 不可静默改 | 需用户批准 |
| feature spec | 不改 | 分流 `/specs-write` |

权限判定顺序：

```text

IF 文档是 L1 SSOT / 母本 / .github/standards → 只输出 Proposed Patch，等待批准
ELIF 文档是 feature spec → 分流 /specs-write
ELIF 是已存在普通 CONTEXT.md 且术语共识已达成且为小补丁，且不改变行为承诺 / 验收 / MVP / 架构决策状态 → 可更新
ELSE → 先问一个确认问题

```

---

## 阶段 1 — 探索领域入口面

### 1.1 读取领域文档

按存在情况读取：

- 已存在的仓库根 `CONTEXT.md`
- 已存在的 `CONTEXT-MAP.md`（多上下文）+ 各上下文 `CONTEXT.md`
- 已存在的 `docs/adr/` 与子上下文 `docs/adr/`
- 母本 / L1 SSOT
- 项目 `README.md`

### 1.2 识别布局

- 仅根 `CONTEXT.md` → 单上下文
- 存在 `CONTEXT-MAP.md` → 多上下文，根据当前讨论判断属于哪一个；不确定时问用户
- 都不存在 → 单上下文模式，懒创建；若检测到 agent assets 仓库（判定标准：存在 .github/skills + .github/workflows 且 AGENTS.md 头部包含 "# 仓库布局"），只报告无领域文档，不创建 `CONTEXT.md`

---

## 阶段 2 — 压力测试实施计划

### 2.1 拷问风格

按 decision tree 逐分支提问，每个问题给推荐答案。

可用动作：

- **挑战词表**：用户用的词与 `CONTEXT.md` 已有定义不一致时，立即追问。
  - "你的词表里 `cancellation` 指 X；你刚才说的是 Y，是哪个？"
- **锐化模糊语**：用户用过载词时，提议精确替代。
  - "你说 `account`，是 `Customer` 还是 `User`？两者不同。"
- **代入具体场景**：边界含糊时，构造极端用例迫使用户精确化。
- **代码交叉验证**：用户陈述系统行为时，对照代码。冲突就摊开。
  - "代码里只取消整张订单，你说支持部分取消，哪个对？"

### 2.2 提问纪律

- 一次一个问题。
- 给推荐答案。
- 等用户回答再继续。
- 复杂问题拆成小问题。
- 不允许在没有共识时跳到"那就这样"。

---

## 阶段 3 — 更新 CONTEXT.md（按需）

### 3.1 何时更新

每个术语或关系达成共识后，先判定目标文档权限并草拟最小 patch。目标是已存在的普通 `CONTEXT.md` 且属于小补丁、已达成术语共识、不触及 L1 SSOT / standards / feature spec、不改变行为承诺 / 验收 / MVP / 架构决策状态时，先进入 `/grill-with-docs:ORDINARY_PATCH_DRAFTED`，再确认目标位置与权限后进入 `/grill-with-docs:ORDINARY_PATCH_SAFE_TO_APPLY` 并可直接写入；新建 `CONTEXT.md`、新建 ADR、修改 L1 SSOT 或 `.github/standards`、大改普通领域文档，必须先展示 patch 并等待批准。若目标项目尚无 `CONTEXT.md`，先确认不是 agent assets 仓库，再按单上下文模板创建。不要批量。

### 3.2 CONTEXT.md 规范结构

```markdown
## <Context Name>

<一两句话说明这个上下文是什么、为什么存在>

## Language

**Order**:
<一句话定义这个术语 是什么，不写它做什么>
_Avoid_: Purchase, transaction

**Customer**:
<定义>
_Avoid_: Client, buyer, account

## Relationships

- An **Order**produces one or more**Invoices**- An**Invoice**belongs to exactly one**Customer**## Example dialogue

>**Dev:**"When a Customer places an Order, do we create the Invoice immediately?"
>**Domain expert:** "No — an Invoice is only generated once a Fulfillment is confirmed."

## Flagged ambiguities

- "account" was used to mean both Customer and User — resolved: distinct concepts

```

### 3.3 写作纪律

- 有取舍：多个候选词，挑一个最好的，其他列为 `Avoid`。
- 显式标冲突：`Flagged ambiguities` 写明歧义与解决。
- 定义紧凑：一句话；写它**是什么**，不写它**做什么**。
- 显式关系：用粗体术语 + 基数关系。
- 只写本上下文专属术语：通用编程概念（timeout、retry、error）不进 `CONTEXT.md`，即使项目用得多。
- `CONTEXT.md` 是术语表，**不是**规格、不是 scratch pad、不是实现决策仓库。

### 3.4 多上下文支持

```markdown
## Context Map

## Contexts

- **Ordering**(`./src/ordering/CONTEXT.md`) — receives and tracks customer orders

-**Billing**(`./src/billing/CONTEXT.md`) — generates invoices
-**Fulfillment** (`./src/fulfillment/CONTEXT.md`) — manages picking and shipping

## Relationships (2)

- Ordering → Fulfillment: emits `OrderPlaced`
- Fulfillment → Billing: emits `ShipmentDispatched`
- Ordering ↔ Billing: shared `CustomerId`, `Money`

```

---

## 阶段 4 — 提供 ADR（架构决策记录）

### 4.1 何时建议引入 ADR

三条**全部**满足才建议：

1. **难以反悔**：改变主意的代价显著。
2. **没有上下文会让人困惑**：未来读者会问"为什么这么干"。
3. **真实权衡的结果**：存在备选项，因为具体理由选了一个。

任一不满足，跳过。

### 4.2 架构决策记录（ADR）规范模板

```markdown
## <Short title of the decision>

<1–3 句话：背景、决议、理由。>
```

### 4.3 可选段落

只在真正有价值时加：

- `Status` 前置：`proposed | accepted | deprecated | superseded by ADR-NNNN`
- `Considered Options`：被拒备选值得记下时
- `Consequences`：非显然下游影响

### 4.4 编号

若 `docs/adr/` 存在，扫描最大编号 +1；若目标项目尚无 `docs/adr/` 且三条 ADR 条件全满足，草拟创建目录与 `0001-slug.md`，等待用户批准后写入。agent assets 仓库不创建。

### 4.5 适合记录到 ADR 的内容

- 架构形态决定（monorepo、event-sourced 写模型、读模型投影）
- 上下文间集成模式（事件 vs 同步 HTTP）
- 带锁定成本的技术选型（DB、消息中间件、Auth、部署目标）
- 边界与归属决议（Customer 数据归 Customer 上下文，其他只引用 ID）
- 故意偏离常规路径（"用手写 SQL 不用 ORM 因为 X"）
- 代码外的约束（合规、SLA、合作方契约）
- 非显然的拒绝（比较过 GraphQL 选了 REST 的具体原因）

### 4.6 不适合记录到 ADR 的内容

- 容易反悔的事
- 显而易见的选择
- 没有真实备选的"决议"

---

## 阶段 5 — 权威 SSOT 守护

### 5.1 不静默改

母本 / L1 SSOT / `.github/instructions/` 中作为权威输入的章节，发现冲突时：

1. 把冲突摊到对话面前。
2. 起草 `Proposed SSOT Patch`：影响范围、修订前后对比、若不修订的下游成本。
3. 等用户明确批准再修改。
4. 未批准前不进入实现层。

### 5.2 权威 SSOT 修复与路由

按冲突归属分流：

| 场景 | 推荐 route |
| ------ | ------------ |
| 术语 / ADR / 普通领域文档冲突 | 继续 `/grill-with-docs` |
| feature spec 缺陷或需修复派生合同 | `/specs-write` |
| 项目定位 / 目标用户 / MVP / 母本级缺陷 | `/project-inception` |

如果 feature spec 冲突需要修改 SSOT 才能继续派生：

```text

Recommended route: /specs-write
Reason: SSOT repair must run through Decision Gate A/B before downstream feature spec is derived.

```

---

## 输出格式

每轮结束输出：

```markdown
## 领域语言拷问与设计对齐报告 (Grill With Docs Report)

## 工作流状态 (Workflow State)

- State: /grill-with-docs:<STATE>; common examples: /grill-with-docs:DOMAIN_DOC_UPDATED | /grill-with-docs:ADR_APPROVAL_PENDING | /grill-with-docs:ADR_WRITTEN | /grill-with-docs:QUESTION_PENDING | /grill-with-docs:SSOT_APPROVAL_REQUIRED | /grill-with-docs:DONE

## 审计结论 (Outcome)

- <Question pending | Domain doc updated | ADR written | Proposed patch only | Routed | No-op>

## 已解决事项 (Resolved)

- <领域术语或实体关联关系>: <共识决议/解决结论>
- ...

## 更新文件 (Updated Files)

- CONTEXT.md 更新章节:
- 写入的 ADR (docs/adr/NNNN-<slug>.md - 若有):

## 权威信息与事实源 (Authority / Fact Source)

- 普通领域文档 (Ordinary domain docs):
- 架构决策记录 (ADR):
- 权威母本/规范批准依据 (Authoritative SSOT / standards approval):

## 受约束的安全写入范围 (Safe-write Scope)

- 写入标的 (Exact target): <N/A or existing ordinary doc path + section>
- 已有锚点 (Existing slot): <N/A or heading / anchor>
- 未越权说明 (No authority escalation because): <N/A or reason>

## 批准的修补范围 (Approved Patch Scope)

- <N/A or exact approved authoritative patch path + section + approval quote>

## 授权边界 (Authorization Boundary)

- 路由动作 (Route Action): <CONTINUE_IN_WORKFLOW | WAIT_FOR_USER | CONFIRMED_ACTION | REPORT_AND_STOP>
- 授权来源 (Confirmation source): <N/A for constrained safe-write | user approval quote>
- 授权范围 (Authorized scope): <safe-write scope or approved patch path / ADR target>
- 未授权范围 (Not authorized): <feature spec / code / tracker / downstream workflow / real-world side effects>

## 待决策开放问题 (Open Questions)

- ...

## 母本管家提议 (SSOT Stewardship Suggestions)

- <仅在涉及权威母本修改时保留；需要用户批准>

## 推荐下一步路由 (Recommended Next Route)

- continue grilling | /specs-write | /project-inception | /project-steward

## Return Contract

- Target route:
- Entry input:
- Resolved terms / decisions:
- Still blocked:
- Not authorized:
- Resume source:

```

---

## 5. 禁用行为

- 不一次抛出长问题列表。
- 不在没有共识时把含糊词写进 `CONTEXT.md`。
- 不把实现细节、临时记录、规格内容写进 `CONTEXT.md`。
- 不在三条 ADR 条件不全时强行写 ADR。
- 不静默改 Authoritative SSOT。
- 不把 `/grill-with-docs:ORDINARY_PATCH_SAFE_TO_APPLY` 用于新建文档、大改普通文档、feature spec、L1 SSOT 或 `.github/standards`。
- 不复述 SSOT 已定义的事实，改用 `@<路径>#<章节>` 引用。
- 不假装代码与陈述一致；冲突必须摊开。

## 6. 快速自检清单

报告前自检：

- [ ] 是否通过代码或文档排查了术语的已有定义（而非直接反问）？
- [ ] 针对术语和关系，提问时是否坚持“一问一答”并给出推荐答案？
- [ ] 新建文档、新建 ADR、修改 L1 SSOT 前，是否已获得用户的明确授权？
- [ ] CONTEXT.md 写入的内容是否仅限于术语定义，而不包含实现细节？
- [ ] ADR 的编写是否完全满足“难以反悔、需留上下文、有真实权衡”三条硬性规定？

## 支撑资源

- [decision-matrix.md](./references/decision-matrix.md)
