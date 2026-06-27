# Entry Decision Tree · /specs-write 入口决策树

> 本文是 `/specs-write` + `/specs-execute` 体系的**入口决策树**。
> 用户请求来 → 走 6 个判定 → 落到唯一推荐路径。让 agent 在 30 秒内完成入口分流，无需通读全部支撑文档。

---

## 0. 定位与用法

### 0.1 文档定位

- 决策树是**导航工具**，不是规则字典：每个判定给「触发条件 → 唯一推荐路径」，不解释规则细节。
- 规则细节去：
  - 一页方法论 → `methodology-kernel.md`
  - 完整术语字典 → `terminology.md`
  - Phase 内部流程 → `orchestration.md` / `../../specs-execute/protocols/phase-rules.md`
  - 模板字段 → `templates/<file>.md`
- 决策树是 `/specs-write` 入口 §1.2 「必走 / 跳过」清单的**全场景扩展**，不重复 §1.2 已给的事实。

### 0.2 6 个判定 + 1 个查询表

| § | 判定 | 关键问题 | 输出 |
| --- | ------ | ---------- | ------ |
| §1 | 入口判定 1 | 是否进入 /specs-write 体系？ | 走 / 不走 / 边缘 |
| §2 | 入口判定 2 | Project Mode 是哪一种？ | Seed / Greenfield / Hybrid / Brownfield |
| §3 | 入口判定 3 | 复杂度 Mode 是哪一档？ | Small / Medium ① / Medium ② / Large |
| §4 | 上游分流判定 | SSOT 是否健康？需要分流到哪个上游 workflow？ | Healthy → 进 charter / 其他 4 态 → 分流 |
| §5 | 回切判定 | 执行端发现 spec 缺陷，回切到哪？ | SPEC_REPAIR_REQUIRED / EXTERNAL_AUDIT_REQUIRED |
| §6 | 抢占触发判定 | 临时任务来了，走哪档抢占？ | P-INLINE / P-SIBLING / P-CROSS |
| §7 | 完整决策规则表 | 覆盖 §1-§6 所有判定 | — |
| §8 | 边界场景查询表 | 30+ 常见场景 → 推荐路径 | — |

### 0.3 引用规则

- 与 `methodology-kernel.md` / `terminology.md` / `/specs-write.md` / `/specs-execute.md` / `cross-cutting.md` / `appendix.md` / `templates/*` 字面零漂移。
- 每条判定尾部带 `源：`<file>`#<section>` 指向真实事实源。
- 决策树出现路径与 `/specs-write` 入口 §1.2 / §1.3.1 / §1.4 / §1.5 不一致时 → 视为决策树失效，必须先修上游再修本文。

---

## 1. 入口判定 1 · 是否进入 /specs-write

### 1.1 必走清单（来自 specs-write §1.2 + 扩展）

- 新功能（新模块 / 新页面 / 新接口 / 新数据流 / 新 UI 入口 / 新业务流程）
- 跨模块重构 / 架构边界变动
- Schema 变更 / API 契约变更 / 协议变更 / 事件契约变更
- 权限 / 计费 / 合规 / 数据治理
- AI / LLM pipeline / Agent / 长链路任务
- 复杂 Bug（根因不明 / 影响面大 / 跨模块）
- **扩展场景（kernel + terminology 派生）**：
  - 单文件 bug 但根因未知 → 必走（先做最小 audit + REQ + DoD）
  - 错字但涉及 SSOT / charter / 标准文档 → 必走（轻量 Medium ②）
  - 用户已给完整代码级指令但范围**超过**1 个文件 → 必走（即使指令清晰）
  - 用户要求"顺便重构" / "顺手优化" → 必走（外科手术原则）
  - 跨 feature 临时任务（线上 P0）→**不进 /specs-write**，但需走 P-CROSS 抢占协议（详 §6）

### 1.2 跳过清单

- 错字 / 文档勘误（不涉及 SSOT / charter / 标准文档）
- 单文件小 bug（根因明确 + 修复影响只在该文件 + 用户已给完整代码级指令）
- 纯查询 / 解释 / 阅读代码
- 一次性脚本 / 探索性原型（不进项目主干）
- **边缘场景澄清**：
  - 用户已给完整代码级指令 + 修改 ≤ 1 文件 + 不涉 SSOT → 跳过
  - 用户已给完整代码级指令 + 修改 > 1 文件 → 升级到 Medium ②
  - 用户问"该怎么做" → 先答问题，**不**直接进 /specs-write

### 1.3 必停澄清场景（不直接判走 / 不走）

| 场景 | 处理 |
| ------ | ------ |
| 用户请求模糊（"改一下"、"优化一下"、"想要个 X 功能"） | 必先澄清范围 / 边界 / 验收标准，再判走 / 不走 |
| 用户已给指令但与现有 spec 冲突 | 先按 `/specs-write:GATE_BLOCKED` 报告冲突，等用户裁决 |
| 用户给的指令命中 charter §5 INV-* 红线 | 必停问 Gate A 战略级 |
| 同时涉及多个 feature 的修改 | 拆成多个 spec 或评估为跨 feature 重构 |

### 1.4 决策规则表
  
详 §7.1 R-ENTRY-1 ~ R-ENTRY-5。

- **源**：`/specs-write.md §0.1 + §1.2`。

---

## 2. 入口判定 2 · Project Mode 判定

> 判定权威源 = `templates/maturity-intake.md` 第 5 行起。判定后绑定 Audit Profile 与是否走 Phase 1.5。

### 2.1 6 维信号必查清单

判定 Project Mode 之前，必查以下 6 维信号；**最少六维齐查**才能下 `Seed / Init` 或 `Greenfield` 判断；任一维存在真实负载 → 升级到 `Hybrid` / `Brownfield`。

1. **仓库骨架**：`README.md` / `package.json` / `pyproject.toml` / `Cargo.toml` 等
2. **源代码**：`src/` / `lib/` / `app/` 中是否有真实业务代码（非脚手架）
3. **DB schema**：`migrations/` / `schema.sql` / `prisma/schema.prisma` / ORM models
4. **测试**：`tests/` / `__tests__/` / `*_test.go` 是否有真实测试
5. **docs SSOT**：`.github/instructions/` / `docs/specs/done/` / `delivery-log.md` / 母本文件
6. **历史 commit / 部署脚本**：`git log` / CI / Dockerfile / deploy 脚本

### 2.2 4 模式判定规则表（按顺序匹配，第一条命中即返回）

| ID | 前置条件 | Project Mode | Audit Profile | Phase 1.5 |
| ---- | ---------- | -------------- | ---------------- | ----------- |
| R-MODE-1 | 6 维任一维存在真实负载（非脚手架） + 本 feature 主要修改 / 替换 / 扩展既有 | Brownfield | Feature-Scoped Full-Surface Audit | 必走 |
| R-MODE-2 | 6 维任一维存在真实负载（非脚手架） + 本 feature 涉及领域内 ≥ 1 既有模块 / 表 / 接口 / 路由 / UI + 同时有明显新建部分 | Hybrid | Feature-Scoped Full-Surface Audit | 必走 |
| R-MODE-3 | 6 维有 README / .github/standards / CI / 测试约束 / 母本，但与既有系统物理隔离 | Greenfield | Greenfield Survey | 跳 |
| R-MODE-4 | 6 维基本为空 + 任务是建立项目骨架 / 初始 SSOT / 第一批基础设施 | Seed / Init | Baseline Survey | 跳 |

**匹配优先级**：R-MODE-1 > R-MODE-2 > R-MODE-3 > R-MODE-4（先升级到 Brownfield / Hybrid，证否后才能下 Greenfield / Seed）。

### 2.3 反模式

- **6 维未齐就判 Seed**：跳过 4 维信号扫描，凭印象判断 → Phase 1.5 必出现 audit_debt
- **把 Greenfield 当无现状**：Greenfield 不是「无现状」，必须审项目基础设施 / 共享规范 / SSOT / 测试 / CI / 数据策略槽位
- **用「当前为空」替代证据**：Baseline / Greenfield Survey 中的 N/A 必给 evidence + Future Audit Trigger

### 2.4 升级规则

- 一旦 6 维任一维出现真实负载（不是脚手架）→ 必须升级到 Hybrid / Brownfield
- 「领域内 ≥ 1 个既有模块」即触发 Hybrid，不必整个项目大量代码

- **源**：`templates/maturity-intake.md` 第 5-13 行 + `terminology.md §2.1`。

---

## 3. 入口判定 3 · 复杂度 Mode 判定

> 判定权威源 = `/specs-write.md §1.5`。复杂度只裁剪文件，不裁剪九层语义层。

### 3.1 4 档复杂度判定规则表（按顺序匹配，第一条命中即返回）

| ID | 前置条件 | 复杂度 Mode | 文件形态 | Mode 标记 |
| ---- | ---------- | ------------- | ---------- | ----------- |
| R-CMPLX-1 | 命中 §3.2 升级触发任一项（Schema 变更 / API 外部消费者 > 1 / 跨边界 Failure Strategy 复杂 / 并发锁-事务边界 / 设计多替代未达共识 / INV-* 候选） | Large | 完整三件套 requirements + design + tasks | `Mode: Large` |
| R-CMPLX-2 | 新功能 / 跨模块重构 / 架构边界变动 / Schema-API-协议变更 / 权限-计费-合规 / 数据治理 / AI-LLM pipeline / Agent / 长链路任务 / 复杂 Bug | Large | 完整三件套 | `Mode: Large` |
| R-CMPLX-3 | 单人小特性 + 设计无替代 + 不涉 schema / API 外部消费者 + 写作端倾向单文件 | Medium ② | 单文件 spec.md（内部仍保留 Requirements / Design / Tasks 三段 + Decision Gate） | `Mode: Medium (single-file:`<reason>`)` |
| R-CMPLX-4 | 单人小特性 + 设计无替代 + 不涉 schema / API 外部消费者 + 写作端倾向跳 design | Medium ① | requirements.md + tasks.md（跳 design） | `Mode: Medium (design skipped:`<reason>`)` |
| R-CMPLX-5 | 错字 / 单文件 bug + 根因明确 + 用户已给完整代码级指令 + 不涉 SSOT | Small | 不启用 workflow | — |

### 3.2 Medium → Large 升级触发

任一命中即升 Large：

- 涉及 Schema 变更 → Large
- API 外部消费者超过 1 个 → Large
- 跨边界 Failure Strategy 复杂 → Large
- 并发锁 / 事务边界 → Large
- 设计存在多种合理替代且未达共识 → Large
- 任一 INV-* 候选触发 → Large

### 3.3 Medium ② 单文件硬约束

- 内部仍保留 Requirements / Design / Tasks **三段**+ Decision Gate 判定
- 缺段视为越界 → 回退 Large
- `Mode: Medium (single-file:`<reason>`)` 头部 reason 必填

### 3.4 边缘场景

| 场景 | 推荐 | 理由 |
| ------ | ------ | ------ |
| 单文件 bug + 根因不明 | Medium ② | 需先做最小 audit 锁影响面 |
| 增加 1 个 API endpoint + 不破坏既有契约 | Medium ① | 跳 design |
| 增加 1 个 API endpoint + 影响外部消费者 | Large | 涉外部契约 |
| 修复 1 处 Schema migration | Large | 涉 Schema |
| 重命名 1 个内部函数（无外部引用） | Small | 不涉契约 |
| 重命名 1 个 export 函数（被其他模块引用） | Medium ② | 涉跨模块影响 |

-**源**：`/specs-write.md §1.5` + `templates/*` 头部 + `terminology.md §3`。

---

## 4. 上游分流判定（SSOT Health 五态 + 4 类外部审计）

### 4.1 SSOT Health 五态分流

| 状态 | 决策 | 路径 |
| ------ | ------ | ------ |
| `Healthy` | `PROCEED_TO_CHARTER` | 进 Phase 1 |
| `Needs Clarification` | `PROCEED_TO_CHARTER` | 进 Phase 1，但必须把不确定项列入 `Blocking Issues` / `Open Questions`，按 Gate A/B/N/A 分类 |
| `Needs Repair` | `BLOCKED_SSOT_REPAIR` | 阻塞下游 → 走 `/grill-with-docs` 或 `/project-inception` 修复 SSOT |
| `Unfit As Source` | `BLOCKED_UNFIT_SOURCE` | 阻塞下游 → 走 `/project-inception` 重建 SSOT |
| `SSOT Absent` | `BLOCKED_SSOT_REPAIR`（视同需修复） | 阻塞下游 → 走 `/project-inception` 创建 SSOT |

### 4.2 4 类外部审计分流（来自 specs-write §1.3.1）

Phase 1.5 / Phase X 发现超出本 feature 范围的问题时，分流而**不**吞进当前 spec：

| 场景 | 推荐路径 | 状态 |
| ------ | ---------- | ------ |
| 项目级架构摩擦 / 浅模块 / seam / interface 重塑 | `/architecture-audit` | `EXTERNAL_AUDIT_REQUIRED` |
| bug 影响面 / 严重性 / 根因假设 / 修复路线 | `/bug-audit` | `EXTERNAL_AUDIT_REQUIRED` |
| 术语 / ADR / 领域文档冲突 | `/grill-with-docs` | `EXTERNAL_AUDIT_REQUIRED` |
| 项目定位 / 目标用户 / MVP / 母本级缺陷 | `/project-inception` | `EXTERNAL_AUDIT_REQUIRED` |
| 商业闭环 / 付费主体 / 替代方案 / 工程 ROI 生死判断 | `/business-model-audit` | `EXTERNAL_AUDIT_REQUIRED` |

### 4.3 分流后回归契约

- 每次分流必带 **Return Contract**：
  - `triggered_from`：本 feature 哪个 Phase 的哪条阻塞证据
  - `expected_output`：期望外部 workflow 产出哪份产物（如 `/architecture-audit` 输出 ADR / `/bug-audit` 输出根因报告）
  - `resume_anchor`：外部 workflow 完成后，本 spec 应回到哪个 Phase
- 分流期间本 spec 状态：`/specs-write:EXTERNAL_AUDIT_REQUIRED`，Route Action `REPORT_AND_STOP`。
- 外部 workflow 完成 → 回当前 Phase 复判；若已解决，进下一 Phase；若未解决，更新阻塞证据再判分流或就地处理。

### 4.4 反模式

- **吞进当前 spec**：把项目级架构问题塞进本 feature 的 audit.md → 违反 §1.3.1
- **不带 Return Contract 分流**：分流后无返回锚点 → 上下游脱钩
- **静默修 SSOT**：未走 `/grill-with-docs` 或 `/project-inception` 就直接改 SSOT → 违反 Authoritative SSOT 边界

- **源**：`/specs-write.md §1.3.1` + `templates/maturity-intake.md` 第 15-22 行 + `terminology.md §15.5`。

---

## 5. 回切判定（执行端 → 写作端）

> 执行端 `/specs-execute` 在 Phase 1-7 任一阶段发现 spec 不能安全执行时，回切到 `/specs-write`。

### 5.1 SPEC_REPAIR_REQUIRED 5 种触发

| 触发 | 检测点 | 处理 |
| ------ | -------- | ------ |
| 上游锚点失效（REQ / DSN / EXIST-* 引用不存在） | Phase 1 Locate | 回切 `/specs-write` 修对应文件 |
| Touches 越界（实现需修改非 `Existing Touches` 声明文件） | Phase 5 Green / Phase 6 Refactor | 回切 `/specs-write` 修 tasks.md `Existing Touches` |
| Schema / API 契约与 design 不符 | Phase 5 Green | 回切 `/specs-write` 修 design.md |
| BDD Scenario 不可实现 / 与 EARS AC 矛盾 | Phase 4 Red | 回切 `/specs-write` 修 requirements.md §7 |
| 跨边界 Failure Strategy 缺失 | Phase 3 Plan | 回切 `/specs-write` 修 design.md |

### 5.2 EXTERNAL_AUDIT_REQUIRED 触发

执行端发现需要外部 workflow 才能解决的问题：

| 场景 | 推荐路径 |
| ------ | ---------- |
| 实现期发现项目级架构问题（深度浅模块 / seam 错位） | 回切 `/specs-write` → 触发 `/architecture-audit` |
| 实现期发现 bug 根因超出本 feature | 回切 `/specs-write` → 触发 `/bug-audit` |
| 实现期发现 SSOT / 术语 / ADR 冲突 | 回切 `/specs-write` → 触发 `/grill-with-docs` |
| 实现期发现项目定位 / 商业模式问题 | 回切 `/specs-write` → 触发 `/project-inception` 或 `/business-model-audit` |

### 5.3 回切 Return Contract

- **来自执行端**：`/specs-execute:SPEC_REPAIR_REQUIRED` 必带：
  - 阻塞证据（哪个 Task / 哪个 Phase / 哪条 Verification 失败）
  - 推荐 spec 修订位置（哪个 ID 失效 / 哪个文件 / 哪个 §）
  - 执行端是否需保留当前 Task 现场（决定是否走 P-SIBLING / P-INLINE）
- **写作端响应**：进 Phase 0 复判 SSOT Health → 决定走 §4.1 健康分流，或仅做局部 spec 修订；修订后重新进 Phase 5 Handoff，更新 `handoff-payload.yaml` schema_version。

### 5.4 反模式

- **执行端就地改 spec**：在 Task 执行中改 spec 文件而不回切 → 违反阶段隔离
- **回切不带证据**：只说「spec 有问题」不指明 ID / Task / Phase → 写作端无法定位
- **回切后跳 Phase 0**：直接修对应文件而不复判 SSOT Health → 可能漏掉根因

- **源**：`/specs-execute.md §0.2.1`（SPEC_REPAIR_REQUIRED / EXTERNAL_AUDIT_REQUIRED）+ `terminology.md §9.2`。

---

## 6. 抢占触发判定（临时任务 → 三档抢占）

> 抢占协议详则在 `appendix.md §A.6` + `blocking-and-rollback.md §1.6`。本节给入口判定。

### 6.1 三档抢占判定规则表（按顺序匹配，第一条命中即返回）

| ID | 前置条件 | 抢占档 | 现场保护 | 计 depth | 特殊 |
| ---- | ---------- | -------- | ---------- | ---------- | ------ |
| R-PREEMPT-1 | 同 Task 内紧急修补（typo / Task 边缘小 bug） | P-INLINE | 不冻结 / 不写 `suspended_state` | 不计 | 走 /specs-execute Refactor 路径处理 |
| R-PREEMPT-2 | 同 feature 跨 Task 切换（用户改主意先做 TASK-003 再回 TASK-001） | P-SIBLING | 现场保护三件套 + 写 `suspended_state` 节 | 计入（≤ 2） | — |
| R-PREEMPT-3 | 跨 feature / 全新临时任务（线上 P0 bug / 用户突然要做另一个 feature） | P-CROSS | 现场保护三件套 + 写 `suspended_state` 节 | 计入（≤ 2） | 连续 P-CROSS = 紧急 bug 风暴或战略不明，必停问用户 |

### 6.2 现场保护三件套（P-SIBLING / P-CROSS · Suspend）

抢占触发时必写 `handoff-payload.yaml#suspended_state` 节，含：

1. `resume_anchor`：phase / task_id / spec / branch / commit
2. `resume_strategy`：mode = `lightweight_wip_commit` 或 `wip_branch_reset`
3. `test_anchors_locked_at`：抢占发生时刻锁定的 ISO 8601（跨中断 §A.2 hash 校验的免责锚点）

### 6.3 Resume 三件套

抢占解除后进入新 feature / 回原 feature 时，执行端 Locate 优先读 `suspended_state`：

1. **Locate**：读 `suspended_state` 而非常规 Phase 1 Intake
2. **Restore**：按 `resume_strategy.mode` 分流恢复工作树；恢复后必校验 Test Anchors hash 与 `test_anchors_locked_at` 时刻锁定值对照
3. **Resume**：从 `resume_anchor.phase` 接力到原 Task 流；同步**物理删除** `suspended_state` 节（仅变状态位 = 失职）

### 6.4 GC 衔接（写作端 Phase 0 必查）

写作端 Phase 0 在读 `implementation_reflections` 之前**必须先**扫描 `handoff-payload.yaml` 是否存在 `suspended_state` 节：

| 状态 | 处理 |
| ------ | ------ |
| 该 feature 已 Done 但仍有 `suspended_state` | 视为执行端 Resume 漏删，停下追问用户后手动从 YAML 删除 |
| 该 feature 未 Done 且有 `suspended_state` | **不得**启动新 feature 的 Phase 1，建议先回该 feature 走 `/specs-execute` 完成 Resume + 后续 Task |

### 6.5 反模式

- **连续 P-CROSS**不停问 → 项目失控信号未上报

-**Resume 后未删 suspended_state**→ 视为执行端 Resume 漏删
-**嵌套 depth > 2**→ 项目失控
-**P-INLINE 写 suspended_state**→ 越界（P-INLINE 不冻结、不写）

-**源**：`appendix.md §A.6` + `blocking-and-rollback.md §1.6` + `terminology.md §11`。

---

## 7. 完整决策规则表（覆盖 §1-§6 所有判定）

> 本节是 `/specs-write` + `/specs-execute` 入口决策的**唯一机读事实源**。Agent 按表顺序匹配，第一条命中即按「动作」列执行；规则可被任何文档以 `R-*` ID 精确引用。

### 7.1 入口判定（§1）

| ID | 前置条件 | 动作 | 下一步状态 | 源 |
| ---- | ---------- | ------ | ------------ | ---- |
| R-ENTRY-1 | 用户请求 matches §1.2 跳过清单 | 直接处理（不启用 workflow） | — | §1.2 |
| R-ENTRY-2 | 用户请求 matches §1.3 必停澄清场景 | 询问澄清后重判 | `WAIT_FOR_USER` | §1.3 |
| R-ENTRY-3 | 用户请求 matches §1.1 必走 + 命中 §6.1 抢占触发 | 跳 §6.1 R-PREEMPT-* | 见 R-PREEMPT-* | §1.1 + §6.1 |
| R-ENTRY-4 | 用户请求 matches §1.1 必走 | 进 /specs-write Phase 0 | 见 R-PHASE0-*/ R-MODE-* | §1.1 |
| R-ENTRY-5 | 以上均不命中 | 询问用户是否启用 workflow | `WAIT_FOR_USER` | — |

### 7.2 Phase 0 · SSOT Health 五态分流

| ID | 前置条件 | 动作 | 下一步状态 | 源 |
| ---- | ---------- | ------ | ------------ | ---- |
| R-PHASE0-1 | SSOT Health = `Healthy` | PROCEED_TO_CHARTER | 进 Phase 1 + 见 R-MODE-* | §4.1 |
| R-PHASE0-2 | SSOT Health = `Needs Clarification` | PROCEED_TO_CHARTER + 列 Blocking Issues / Open Questions（按 Gate A/B/N/A 分类） | 进 Phase 1 + 见 R-MODE-* | §4.1 |
| R-PHASE0-3 | SSOT Health = `Needs Repair` | BLOCKED_SSOT_REPAIR + 分流 /grill-with-docs 或 /project-inception + Return Contract | `/specs-write:EXTERNAL_AUDIT_REQUIRED` | §4.1 |
| R-PHASE0-4 | SSOT Health = `Unfit As Source` | BLOCKED_UNFIT_SOURCE + 分流 /project-inception + Return Contract | `/specs-write:EXTERNAL_AUDIT_REQUIRED` | §4.1 |
| R-PHASE0-5 | SSOT Health = `SSOT Absent` | BLOCKED_SSOT_REPAIR + 分流 /project-inception 创建 SSOT | `/specs-write:EXTERNAL_AUDIT_REQUIRED` | §4.1 |

### 7.3 Phase 0 · Project Mode 判定

详 §2.2 R-MODE-1 ~ R-MODE-4。

### 7.4 复杂度 Mode 判定

详 §3.1 R-CMPLX-1 ~ R-CMPLX-5。

### 7.5 外部审计分流（§4.2）

| ID | 前置条件 | 动作 | 状态 | 源 |
| ---- | ---------- | ------ | ------ | ---- |
| R-AUDIT-0 | 系统状态不清、现存计划有严重摩擦无法继续，或需撤销/推翻 | 分流 /project-steward | `/specs-write:BLOCKED` (退交 DRI) | §4.2 |
| R-AUDIT-1 | 项目级架构摩擦 / 浅模块 / seam / interface 重塑 | 分流 /architecture-audit + Return Contract | `/specs-write:EXTERNAL_AUDIT_REQUIRED` | §4.2 |
| R-AUDIT-2 | bug 影响面 / 严重性 / 根因假设 / 修复路线 | 分流 /bug-audit + Return Contract | `/specs-write:EXTERNAL_AUDIT_REQUIRED` | §4.2 |
| R-AUDIT-3 | 术语 / ADR / 领域文档冲突 | 分流 /grill-with-docs + Return Contract | `/specs-write:EXTERNAL_AUDIT_REQUIRED` | §4.2 |
| R-AUDIT-4 | 项目定位 / 目标用户 / MVP / 母本级缺陷 | 分流 /project-inception + Return Contract | `/specs-write:EXTERNAL_AUDIT_REQUIRED` | §4.2 |
| R-AUDIT-5 | 商业闭环 / 付费主体 / 替代方案 / 工程 ROI 生死判断 | 分流 /business-model-audit + Return Contract | `/specs-write:EXTERNAL_AUDIT_REQUIRED` | §4.2 |

### 7.6 执行端 → 写作端回切判定（§5）

| ID | 前置条件 | 动作 | 状态 | 源 |
| ---- | ---------- | ------ | ------ | ---- |
| R-RETURN-1 | Phase 1 Locate：上游锚点失效（REQ / DSN / EXIST-* 引用不存在） | 回切 /specs-write 修对应文件 | `/specs-execute:SPEC_REPAIR_REQUIRED` | §5.1 |
| R-RETURN-2 | Phase 5 Green / Phase 6 Refactor：Touches 越界 | 回切 /specs-write 修 tasks.md `Existing Touches` | `/specs-execute:SPEC_REPAIR_REQUIRED` | §5.1 |
| R-RETURN-3 | Phase 5 Green：Schema / API 契约与 design 不符 | 回切 /specs-write 修 design.md | `/specs-execute:SPEC_REPAIR_REQUIRED` | §5.1 |
| R-RETURN-4 | Phase 4 Red：BDD Scenario 不可实现 / 与 EARS AC 矛盾 | 回切 /specs-write 修 requirements.md §7 | `/specs-execute:SPEC_REPAIR_REQUIRED` | §5.1 |
| R-RETURN-5 | Phase 3 Plan：跨边界 Failure Strategy 缺失 | 回切 /specs-write 修 design.md | `/specs-execute:SPEC_REPAIR_REQUIRED` | §5.1 |
| R-RETURN-6 | 实现期发现项目级架构问题 | 回切 /specs-write → 触发 /architecture-audit | `/specs-execute:EXTERNAL_AUDIT_REQUIRED` | §5.2 |
| R-RETURN-7 | 实现期发现 bug 根因超出本 feature | 回切 /specs-write → 触发 /bug-audit | `/specs-execute:EXTERNAL_AUDIT_REQUIRED` | §5.2 |
| R-RETURN-8 | 实现期发现 SSOT / 术语 / ADR 冲突 | 回切 /specs-write → 触发 /grill-with-docs | `/specs-execute:EXTERNAL_AUDIT_REQUIRED` | §5.2 |
| R-RETURN-9 | 实现期发现项目定位 / 商业模式问题 | 回切 /specs-write → 触发 /project-inception 或 /business-model-audit | `/specs-execute:EXTERNAL_AUDIT_REQUIRED` | §5.2 |

### 7.7 抢占触发判定

详 §6.1 R-PREEMPT-1 ~ R-PREEMPT-3。

### 7.8 active → done 迁移判定（kernel §5）

| ID | 前置条件 | 动作 | 状态 | 源 |
| ---- | ---------- | ------ | ------ | ---- |
| R-CLOSEOUT-1 | 全 Task Status = Done，无 Blocked / Blocked(Suspended) 残留 | 进 Phase 9 Closeout 准备 | `/specs-execute:CLOSEOUT_READY` | kernel §5 + /specs-execute Phase 9 |
| R-CLOSEOUT-2 | R-CLOSEOUT-1 + artifacts 与所有 Task 的 `Artifacts:` 声明一致（无遗漏 / 无外溢）+ 项目根 reports/tmp/output 无散落 | 继续准备 git mv | `/specs-execute:CLOSEOUT_READY` | kernel §5 |
| R-CLOSEOUT-3 | R-CLOSEOUT-2 + `docs/specs/project archives/delivery-log.md` 已追加本条 feature 交付记录 | 执行 git mv active/ → done/ | `/specs-execute:CLOSEOUT_DONE` | kernel §5 |
| R-CLOSEOUT-4 | R-CLOSEOUT-1/2/3 任一未齐 | 拒绝 git mv，PR 拒合并 | `/specs-execute:CLOSEOUT_READY` 不变 | kernel §5 |

### 7.9 规则匹配总则

- **优先级**：表内规则按 ID 数字升序匹配；第一条命中即返回，不继续匹配。
- **跨表跳转**：R-ENTRY-*命中 §6.1 抢占触发时跳到 R-PREEMPT-*；命中必走时进 R-PHASE0-*与 R-MODE-* 串联判定。
- **可寻址**：任何文档可用 `R-ENTRY-3` / `R-MODE-2` / `R-CLOSEOUT-3` 等 ID 精确引用本表规则。
- **修订规则**：本表规则修订必须同 PR 修订上游事实源（kernel / terminology / specs-write / specs-execute）；与上游字面冲突 → 视为本表失效。

---

## 8. 边界场景查询表（30+ 场景）

### 8.1 用户请求 → 推荐路径

| 用户请求文本 | 推荐路径 | 复杂度 | 理由 |
| -------------- | ---------- | -------- | ------ |
| 「修一下 README 错字」 | 不启用 workflow | Small | 文档勘误，不涉 SSOT |
| 「修一下 charter 错字」 | /specs-write | Medium ② | 涉权威 SSOT，必走轻量 spec |
| 「这个 bug 的 stack trace 是 ... 怎么修」 | /specs-write 或 /bug-audit | Medium ②（已知根因）/ /bug-audit（根因不明） | 看根因是否明确 |
| 「写一个新页面 X」 | /specs-write | Large | 新功能 |
| 「在 X 页面加一个按钮调 Y API」 | /specs-write | Medium ① 或 Large | 看 Y API 是否新增 / 现有 |
| 「重构 X 模块」 | /specs-write | Large | 跨模块重构 |
| 「重命名一个内部函数（无外部引用）」 | 不启用 workflow | Small | 不涉契约 |
| 「重命名一个 export 函数（被其他模块引用）」 | /specs-write | Medium ② | 跨模块影响 |
| 「这段代码什么意思」 | 直接答 | Small | 纯解释 |
| 「应该用 X 还是 Y 库」 | 先答问题 | — | 不直接进 /specs-write |
| 「设计一个新功能 X」 | /specs-write | Large | 新功能 |
| 「我想要个 X 功能」 | 必停澄清 | — | 范围 / 边界 / 验收不明 |
| 「优化一下性能」 | 必停澄清 | — | 范围不明 |
| 「我们用什么数据库好」 | /project-inception | — | 项目级决策 |
| 「现有架构有问题，重新设计」 | /architecture-audit | — | 项目级架构 |
| 「这个 bug 影响多大不知道，先调查」 | /bug-audit | — | 根因 / 影响面不明 |
| 「术语对齐：X 在 A 文档叫 X，B 文档叫 Y」 | /grill-with-docs | — | 术语 / ADR 冲突 |
| 「这个商业模式靠不靠谱」 | /business-model-audit | — | 商业级决策 |
| 「从零开始一个新项目」 | /project-inception | — | 项目立项 |
| 「线上 P0 bug，立刻修」 | P-CROSS 抢占 | — | 跨 feature 紧急 |
| 「先停下当前 Task，做另一个 Task-003」 | P-SIBLING 抢占 | — | 同 feature 跨 Task |
| 「同 Task 边缘小修补」 | P-INLINE 不冻结 | — | 同 Task 内 |
| 「在 Task-001 执行中发现 design 错了」 | /specs-execute:SPEC_REPAIR_REQUIRED 回切 | — | 回切判定 |
| 「Task-001 验证失败需回滚」 | /specs-execute:ROLLBACK_REQUIRED | — | 回滚判定 |
| 「这个 Schema migration 失败了」 | /specs-execute:BLOCKED 或 SPEC_REPAIR_REQUIRED | — | 看是 Migration 写错（spec 缺陷）还是环境问题 |
| 「实现期发现项目级深度浅模块」 | /specs-execute:EXTERNAL_AUDIT_REQUIRED → /architecture-audit | — | 跨 feature 架构 |
| 「写完 spec 了，下一步」 | /specs-execute TASK-001 | — | 进入执行端 |
| 「全 Task Done 了，下一步」 | active → done 三条件齐 + git mv + delivery-log.md 追加 | — | 收尾 |
| 「上次 Task-002 中断了，怎么继续」 | /specs-execute Resume | — | 抢占恢复 |
| 「想做新 feature 但发现 SSOT 不健康」 | 先走 /grill-with-docs 修 SSOT | — | SSOT Health 优先 |
| 「想做 feature X 但用户没说清要什么」 | 必停澄清 ≤ 5 条 Open Questions | — | 防 5 注意力稀释 |

### 8.2 跨 workflow 场景查询

| 场景 | 进入 /specs-write 之前 | 进入之后 |
| ------ | ------------------------ | ---------- |
| 项目刚起步，无任何 spec | /project-inception | /specs-write Seed / Greenfield 模式 |
| 已有 charter / SSOT，要做第一个 feature | — | /specs-write Greenfield / Hybrid 模式 |
| 已有大量代码，想做新 feature | — | /specs-write Hybrid / Brownfield 模式 |
| 已有 spec，要执行下一个 Task | — | /specs-execute |
| 想知道下一步该做什么 | /project-steward | 视输出分流 |
| 想审查最近的代码改动 | /review | — |
| 想拷问当前计划是否合理 | /grill-me 或 /grill-with-docs | — |

---

## 9. 与 /specs-write 入口 §1.2 的关系

### 9.1 不重复关系

- `/specs-write.md §1.2` 给「必走 / 跳过」一句话清单（10+ 必走 + 5+ 跳过）。
- 本文 §1 是 §1.2 的**全场景扩展**：补充边缘场景、必停澄清场景、单文件 bug / 错字 SSOT / 跨模块影响等中间情况。
- 本文 §2-§6 是 §1.2 之外的 5 个判定，§1.2 不涉及。

### 9.2 修订规则

- §1 「必走 / 跳过」清单与 `/specs-write.md §1.2` 字面冲突 → 视为本文失效，必须先修 §1.2 再修本文。
- §2-§6 与 `templates/maturity-intake.md` / `cross-cutting.md` / `appendix.md` / `terminology.md` 冲突 → 同上。

### 9.3 决策树的边界

- 决策树**不**做 Decision Gate 判定（Gate A/B/C / Irreversible / AI-DRI），那是 `cross-cutting.md §2`。
- 决策树**不**做 Phase 内部流程，那是 `orchestration.md` / `phase-rules.md`。
- 决策树**只**做入口分流：用户请求 → 推荐路径。

- **源**：`/specs-write.md §1.2 / §1.3.1 / §1.4 / §1.5` + `methodology-kernel.md §10`。

---

**修订规则**：本文与 `methodology-kernel.md` / `terminology.md` / `/specs-write.md` / `/specs-execute.md` / `cross-cutting.md` / `appendix.md` / `templates/*` 字面零漂移。任一上游修改 → 同 PR 修订本文；本文修订 → 同 PR 修订下游受影响文档。
