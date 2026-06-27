# 横切契约（Cross-Cutting Contracts）

> **When to read**: 主 workflow 在多个 Phase 出口的 MUST read 指令均会指向本文相应子节。

---

## 1. 标识与追溯（合并 ID 格式 / 子域 / 定位 / 派生与追溯协议 / 执行门禁）

### 1.1 ID 格式

| 类型 | 格式 | 范围 |
| ------ | ------ | ------ |
| 来源 | `SRC-###` | charter |
| User Story | `US-###` | requirements |
| 需求 | `REQ-###` | requirements |
| 验收（EARS） | `AC-###.#` | requirements，REQ-001 下的第 N 条 |
| BDD 场景 | `<REQ-###>.S<n>`（n 从 1 起编） | requirements |
| 设计 | `DSN-`<domain>`-###` | design |
| 既有需求（反向标识） | `EXIST-REQ-###` | audit |
| 既有设计（反向标识） | `EXIST-DSN-`<domain>`-###` | audit |
| 任务 | `TASK-###` | tasks |
| 架构红线 | `INV-`<TYPE>`-###`（TYPE: BAN / LIM / SEC） | charter |

`SRC` / `US` / `REQ` / `EXIST-*` / `INV-*` 一旦分配不变。`AC-###.#` 中的 `###` 跟随 REQ。

### 1.2 `<domain>` 枚举

`DSN-`<domain>`-###` 与 `EXIST-DSN-`<domain>`-###` 共享同一枚举：

| domain | 含义 | 典型项 |
| -------- | ------ | -------- |
| `ARCH` | 架构 / 路由注册 / 服务边界 | 注册中间件、服务启动顺序、模块拓扑 |
| `DB` | 表 / 列 / 索引 / 约束 / 访问路径 | schema.sql、ORM、迁移、视图 |
| `API` | HTTP / RPC / 外部契约 | endpoint、请求响应、错误码 |
| `UI` | 页面 / 组件 / 交互 / 状态机 | 路由、页面 state、组件 props |
| `SEC` | 鉴权 / 鉴别 / 密钥 / 合规 | middleware、RLS、审计日志、凭据流 |
| `OBS` | 日志 / 指标 / 告警 / 后台任务 / 幂等 | logger、metric、cron、worker |
| `DATA` | 数据契约 / 字段语义 / 跨表语义 / fixture / seed | data contract、derivation map、metadata schema |
| `LLM` | 提示词 / 模型选型 / 成本 / fallback | prompt 模板、模型路由、防御三件套 |
| `MIG` | 数据迁移 / 兼容性 / 升级 / 回滚 | DB 迁移、config 迁移、shadow_write / stepwise / downgrade 三选一 |
| `INFRA` | 部署 / 容器 / 依赖服务 / 镜像 / CI | CI 脚手架、环境变量、容器编排 |
| `INT` | 三方集成 / SDK / webhook | OAuth provider、payment provider、第三方 API client |
| `FS` | 文件系统 / 文件格式 / 目录约定 | jsonl/csv 产出、目录布局、脚本路径 |
| `FLOW` | 业务流程 / SOP / workflow / 人工环节 | HITL 流程、审查 SOP、批量作业链 |
| `CONFIG` | 配置文件 / yaml / env / feature flag | yaml、env、feature flag、profile |
| `CACHE` | 缓存 / TTL / 一致性策略 | 内存缓存、materialized view、本地缓存目录 |
| `OTHER` | 以上都不匹配时临时使用 | 必须在该 DSN 章节 Notes 说明为什么需要新子域 |

**硬规则**：

- spec 内不得使用枚举以外的子域名（除非同时在 charter / audit Notes 里登记使用 `OTHER` 的具体理由 + 候选转正方向）。
- 枚举表演进需在本 workflow 追加（schema_version 升级记录）。
- cross-spec 引用 `EXIST-DSN-*` 时，不同 spec 的同一子域语义必须一致；不一致 → 视为术语漂移，回 §1.4-B 派生协议处置。
- 选择优先级：能用主流 8 项（`ARCH/DB/API/UI/SEC/OBS/DATA/LLM`）就用，不主流子域（`MIG/INFRA/INT/FS/FLOW/CONFIG/CACHE`）只在确实表达更精确时启用，`OTHER` 仅作临时兜底。

### 1.3 跨文件定位

- spec 文件之间引用：`<file>#<id>` 或 `<file>#<heading-anchor>`（不允许行号）。
- 引用代码：`<file path>::<symbol>` 或 `<file path>::`<class>`::<method>`，或 git 永久 SHA。
- 引用既有 spec：`docs/specs/<feature-slug>/<file>.md#<id>`。
- 归档版本快照：`docs/Archives/specs/<file>.snapshot.`<YYYY-MM-DD>`.md`，不参与活跃锚点。

### 1.4 派生与追溯协议

**A · ID 关系语义（`Relation to Existing` 五选一）**：

| 关系 | 含义 | 使用范围 |
| ------ | ------ | ---------- |
| `Extends EXIST-*` | 在既有基础上叠加 | REQ / DSN / TASK |
| `Replaces EXIST-*` | 替换既有 | REQ / DSN / TASK |
| `Conflicts EXIST-*` | 与既有冲突待解 | REQ / DSN / TASK |
| `Depends EXIST-*` | 依赖既有不动 | REQ / DSN / TASK |
| `Net New` | 既无 SSOT 也无现状承接 | REQ / DSN / TASK |

- `Net New` 必须附 `Justification`：为何 SSOT 与现状均未覆盖。
- `Conflicts` 必须有**解决方向**，不得只罗列矛盾。
- Greenfield 模式下 `Relation to Existing` 可统一填 `Net New`。

**B · 派生协议**（spec 与 Authoritative SSOT 关系）：

1. 每条 `REQ / DSN` 必须填 `Derived From`，引用 `SRC-### / SRC-###@<章节>`。
2. `Net New` 必须附 `Justification`。
3. **不得复述 SSOT 已定义的事实**；spec 中涉及已定义概念时必须用 `@<路径>#<章节>` 引用。
4. 发现 spec 与 Authoritative SSOT 冲突 → **停下**，进入"SSOT 修订请求"流程，**不得就地修 spec 妥协**。
5. AI 对 SSOT 有理解、审查与守护责任：当发现明显上游缺陷、健康风险或显著改进空间时，可提出缺省判断、质量诊断、`Proposed SSOT Patch` 与强推荐修订方案；无实质发现时不为形式主义每轮制造建议。
6. Authoritative SSOT 修改边界：未获用户明确批准前，不得直接修改母本 / L1 SSOT / .github/standards 中作为权威输入的章节；允许写入 spec 内的 `SSOT Stewardship Suggestions` / `Repair Draft` / `SSOT Gap` 作为候选。
7. SSOT 修订请求流程（轻量）：在 maturity-intake.md `SSOT Stewardship Suggestions` / `Repair Draft`、audit.md §5 或 charter.md Notes 记录冲突 → 通知用户决定（a 回流 SSOT / b spec 局部豁免，需在 charter §6 Out of Charter 显式登记） → 不得在未决前推进下游。

**C · 现状协议**（spec 与既有代码关系）：

1. Hybrid / Brownfield 模式必须先做 Phase 1.5；audit.md 的 `EXIST-*` 是新 spec 的反向锚点。
2. 新 REQ / DSN / TASK 必须填 `Relation to Existing`。
3. 决定 Replace / Conflict 必须给出迁移路径或冲突解决方向。
4. Seed / Init / Greenfield 模式：跳过 Phase 1.5，但不得"假装项目是空的"——必须在 maturity-intake.md `Baseline / Greenfield Survey` 中证明"空白本身"或"基础设施已就绪"。

**D · 追溯强制协议**（防 1 双源单写）：

1. `tasks.md` 顶部必含 Traceability Matrix（详 `appendix.md §A.1`）；表头标注 `<!-- generated-from: handoff-payload.yaml#traceability -->`。
2. `handoff-payload.yaml` 的 `traceability` 节是该矩阵的**唯一机读事实源**；Markdown 表格从 YAML 重生，不得反向手改。
3. 每个 Task 必须出现在矩阵中，且 `Implements / Design Refs / Existing / Anti-Invariants / BDD Scenarios Owned / Artifacts` 字段不得为空（可填 `N/A (mode=...)` / `none (no applicable)`）。
4. `Existing` 列填 `N/A (mode=Greenfield)` 或 `N/A (mode=Seed)` 优于留空；保证 `mode_propagated` 可机器校验。

**E · 执行门禁**（与 `/specs-execute` 联动 · 防 5）：

`tasks.md` 中每个 Task 必须包含 `Context Required Before Execution` 节（详 `appendix.md §A.5`），按 P0 Essential / P1 Reference 严格二分。执行端在 Hydrate 阶段必须逐条复述 P0；P0 超上限即视为 Task 裁切不够细，回 Phase 4 拆分。**动作层细节见 §1.5**。

### 1.5 执行门禁动作清单

- 必读锚点顺序与复述要求：详 `/specs-execute §2.1` + `§2.2`。
- 锚点失效处理（含 EXIST `Verified By:` 7 天有效期重检）：详 `/specs-execute §2.3`。
- tasks.md `Context Required Before Execution` 字段合规要求详 `appendix.md §A.5`（P0/P1 严格二分 / 跨边界 Task 必含适用 INV-* + Failure Strategy + Concurrency & Lock）；字段不合规 → 执行端按 `blocking-and-rollback.md §1.3` 回切。

---

## 2. Decision Gate（唯一审批语义）

### 2.1 状态枚举

| Status | 含义 | 下一步 |
| -------- | ------ | -------- |
| `Draft` | 写完待批 | 进入 Gate 判定 |
| `Approved` | 用户批准（命中 Gate）或 AI-DRI 自动批准（未命中 Gate） | 进入下一 Phase |
| `Needs Changes` | 命中 Gate 且用户要求修订 | 修订后重提 Gate |
| `Acknowledged` | charter 专用（轻量，不走独立批准） | 进入 Phase 1.5 / Phase 2 |
| `Superseded` | 被新版本替代 | 保留作历史 |

**你可以在 Gate N/A 时自行将状态从 `Draft` / `Needs Changes` 改为 `Approved`**，但必须在 `Notes` 留痕（详 §2.3）。命中 Gate A/B/C、Spec Breach 或 Irreversible 时，AI 不得自行批准，必须等待用户白名单批准。

> **澄清**：本表枚举的是 **spec 文件的 `Approval.Status`**（5 选 1：Draft / Approved / Needs Changes / Acknowledged / Superseded）。**Task 自身的 `Status`**另有 5 个枚举（`Pending | In Progress | Done | Blocked | Blocked(Suspended)`），定义点在 `templates/tasks.md` Task 头部 Status 字段。

### 2.2 Gate 判定白名单（决定何时停下问用户）

| Gate | 触发场景 | 例 |
| ------ | ---------- | ----- |
| **Gate A · L-STRAT 战略级** | 产品方向 / 商业模型 / 合规红线 / 资源投入 / Charter 红线变更 / 重大 SSOT 修订 | "本 feature 是否纳入本季度交付"、"是否引入新一类外部依赖" |
| **Gate B · L-DESIGN 设计级** | 新 feature 架构 / Schema 结构 / API 契约 / 新引入依赖 / UI 大版本 / 跨系统集成 | "Order 表是否拆分子表"、"是否引入消息队列" |
| **Gate C · Spec Breach** | 当前阶段产出违反上游 SSOT / charter §5 INV-*/ 已 Approved 的 spec | "新设计违反 charter INV-BAN-001" |
| **Irreversible Action** | 写真实数据库 / 推送远端 / 改 CI / 改 IAM / 调用付费 API / 涉资金流接口 | 任意此类动作 |
| **Gate B 衍生 · Existing Touches 扩展回流** | 执行端某 Task 实施中 AI-DRI 自动追加 ≥ 2 个公共契约相关文件至 `Existing Touches`，触发 `kind: audit_debt + extension_payload` 反流（详 `appendix.md §A.7.5`） | AI-DRI 起草 EXIST-* 补丁 + 等用户裁决；裁决后补 audit.md `EXIST-DSN-*` + 同 PR 更新对应 Task `Existing Touches` |
| **Anything else (L-IMPL / L-OPS)** | 实现细节 / 内部重构 / migration 文件名 / 测试写法 / 库 API 用法 | AI-DRI 自决，事后简报一行 |

凡命中以上 Gate → 你必须**停下**，给：

```text
🚦 Gate `<X>` 命中: <一句话场景>
推荐方案: <强推荐 · 1 句>
备选方案 (≤ 2): <方案 B · 代价> | <方案 C · 代价>
代价对比: <每个方案 1 句>
请确认: 选 A/B/C 或继续讨论
```

未命中 Gate → AI-DRI 自决推进。

### 2.3 防伪协议

#### Gate 命中时

AI **必须**：

1. 在该文件 `## Approval` 节的 `Notes:` 字段下用引用块复制用户原话（`>` 引用 + 时间戳），形如：

   ```yaml
   Approval:
     Status: Approved
     Notes: |
       > Approved by User on 2026-05-04T15:30:00+08:00
       > "<用户原话片段，包含明确同意意图，如 '同意' / 'go ahead' / '可以推进'>"
     Timestamp: 2026-05-04T15:30:00+08:00
   ```

2. 留痕原话要求：必须出现明示同意词；用户复述他人意见、用 emoji（"👍"）、笑脸或问句不视作批准；用户继续讨论 / 修订意见亦不视作批准。

#### Gate N/A 时（AI-DRI 自动批准）

在 `Notes:` 写入：

```text
AI-DRI auto-approved: no Pause-and-Ask trigger
Gate Check: A=N/A, B=N/A, C=N/A
Evidence: <已读 SSOT / audit / code anchors / constraints 摘要>
Timestamp: <ISO 8601>
```

#### 反模式（AI 自查）

- ❌ 用户说"看起来不错"/"整体可以" → 不算 Approved（含模糊保留）
- ❌ 用户用 👍 / 笑脸表情 → 不算 Approved
- ❌ 用户说"先这样，后面再改" → 不算 Approved（含未来修订意图）
- ❌ AI 在 Gate 命中时未给强推荐 + ≤ 2 备选 + 代价，伪造 Approved → 协议违规
- ❌ Gate N/A 时未在 Notes 写入 `AI-DRI auto-approved` 留痕 → 视为伪 Approved
- ❌ AI 把 L-IMPL 决策上交用户问"要不要"反复倒灌 → 违反缺省立法

### 2.4 Superseded 归档协议

当 Approved 文件需要重大修订（已影响下游设计 / 任务 / 实现）时：

1. 不得就地覆盖。必须先把当前版本归档为 `<file>.v<N>.md`（例 `requirements.v1.md`）。
2. 归档版本的 `Approval.Status` 改为 `Superseded`，并在 `Notes` 写明被替代原因与新版本路径。
3. 新版本继承原文件名（`requirements.md`），从 `Draft` 状态重新走 Decision Gate。
4. 下游文件（`design.md` / `tasks.md`）必须刷新 `Requirements Ref` / `Design Ref` 指向新版本，并复检追溯链。
5. Traceability Matrix 中如有 ID 失效或语义变更，必须在新版本里显式标注迁移说明。

---

## 3. EARS / BDD / TDD

### 3.1 EARS 风格 AC（目标态契约）

EARS 6 句式：

| 模式 | 模板 |
| ------ | ------ |
| Ubiquitous | THE `<system>` SHALL `<action>` |
| Event-Driven | WHEN `<event>` THE `<system>` SHALL `<action>` |
| State-Driven | WHILE `<state>` THE `<system>` SHALL `<action>` |
| Optional Feature | WHERE `<feature_enabled>` THE `<system>` SHALL `<action>` |
| Unwanted Behavior | IF `<error>` THEN THE `<system>` SHALL `<fail-safe>` |
| Conditional | IF `<condition>` THEN THE `<system>` SHALL `<action>` |

每条 AC：

- 明确主语 / 触发 / 行为 / 度量。
- **可观察、可验证、可写测试**。
- 单条 AC 不超过 1 行业务行为。

### 3.2 BDD（Gherkin · 行为驱动）

每条 REQ 至少 1 条 Gherkin Scenario。**Scenario 是契约，不是测试代码**：

```gherkin
Scenario: 用户在订单列表页过滤已退款订单
  Given 用户登录账号 "alice"
  And 数据库存在 5 条订单（2 已退款 / 3 未退款）
  When 用户在订单列表页勾选 "已退款"
  Then 列表只显示 2 条已退款订单
  And 列表头部显示总数 "2"
```

硬规则：

- 主语必须是**用户 / 角色 / 触发系统**，不是开发者；不要写"调用 API"；要写"用户点击按钮"或"系统接收事件"。
- Given 必须给**可复现的前置数据**（fixture / factory / seed 锚点）；非平凡数据态的 Given 必须引用 fixture：
  - 例：`Given seed/users.test.json#user-001`
  - 例：`Given factory: OrderFactory.create(status='refunded', count=2)`
- When 是**单个事件**；不要 "when ... and when ..."。
- Then 必须**可观察**：UI 文案 / 数据库行 / API 响应 / 事件投递；不要"系统应正确处理"。
- 一个 REQ 写 ≥ 1 条**典型路径** Scenario；命中以下任一场景必加失败分支 Scenario：(a) 调用外部 API / 远程服务 / 网络；(b) 写入数据库 / 文件系统 / 队列；(c) 跨进程 / 跨服务消息；(d) 涉及批量 / 长时任务。

`Scenario:` 标题作为 BDD 锚点写入 `Test Anchors`，例：`REQ-001.S1`。

### 3.3 EARS 与 BDD 的配对规则

| 维度 | EARS AC | BDD Scenario |
| ------ | --------- | -------------- |
| 视角 | 系统目标态契约（"系统必须 …"） | 用户 / 角色行为驱动（"用户做 …，系统反馈 …"） |
| 形式 | 单句 SHALL / IF-THEN | 多步 Given-When-Then |
| 测试归属 | 单元 / 契约 / 集成测试 | 验收 / 端到端 / Acceptance 测试 |
| 命名 | `AC-001.1` … | `REQ-001.S1` … |
| 防漂移 | 互查时不可孤立 |  |

互查规则：

- 每条 EARS AC 至少被一条 BDD Scenario 覆盖。
- 每条 BDD Scenario 至少落在一条 EARS AC 的契约范围内（**不能写"系统未保证"的行为**）。
- 写作端在产 requirements 时必须做一次反向自查（是否有孤立 AC / 孤立 Scenario）。

### 3.4 与 TDD 的边界

EARS / BDD 是需求阶段产出的契约（AC + Scenario）；TDD（Red→Green→Refactor）由 `/specs-execute` Phase 4-6 落地，具体测试代码 / stub / mock 按 Test Anchors（详 `appendix.md §A.2`）锁回 spec。

### 3.5 三轨职责矩阵（ATDD / BDD / TDD 分工）

| 方法 | 关注层 | 在本 workflow 的落点 | 形式 |
| ------ | -------- | ---------------------- | ------ |
| **ATDD**（验收驱动） | 系统级 / "什么算完成" | `requirements.md` 的 AC + `tasks.md` 的 DoD | EARS 六句式 + Traceability Matrix |
| **BDD**（行为驱动） | 功能级 / "什么动作 → 什么状态变化" | `requirements.md §7` + `tasks.md` 仅引用 Scenario 锚点 | `Given / When / Then` 三段式 |
| **TDD**（测试驱动） | 代码级 / "代码实现是对的" | `tasks.md` 的 `Verification` + 执行阶段 Red-Green-Refactor | 单元测试先行 |

三者关系：**ATDD 定目标 → BDD 锁路径 → TDD 保实现**。

- ATDD + BDD **同条 REQ 内**双落地于 `requirements.md`，写作端在产 requirements 时强制配对（详 §3.3）；
- TDD 由 `/specs-execute` 在执行 Task 时遵循 Red→Green→Refactor，并把测试文件锚点写回 `tasks.md` 的 Test Anchors（详 `appendix.md §A.2`）。

**反模式**：

- ❌ 写作端直接在 spec 里写测试代码（mock / fixture body / Jest 语法）→ 越界到 TDD
- ❌ tasks.md `Verification` 只写 "写单元测试" 不指 BDD Scenario 锚点 → ATDD-BDD-TDD 链断
- ❌ BDD Scenario 写在执行端某个测试文件里而没回写 `requirements.md §7` → BDD 锚点孤立，违反 §3.3 互查

---

## 4. Spec Contract Schema（machine-readable）

### 4.1 设计目的

`tasks.md` 顶部 Traceability Matrix 是**人类可读的版本**；`handoff-payload.yaml` 是**机器消费的版本**。两者必须自洽，且后者是 SSOT。

### 4.2 完整 schema（产 `handoff-payload.yaml`）

```yaml
schema_version: 0.6
feature_slug: `<feature-slug>`
mode: "Large" | "Medium (design skipped: `<reason>`)" | "Medium (single-file: `<reason>`)"   # 与主 workflow §1.5 / 各模板头部枚举完全一致； reason 不得丢
project_mode: Seed | Greenfield | Hybrid | Brownfield   # 来自 maturity-intake.md；Seed 即原 "Seed / Init" 合档（主 workflow §1.4 模式表已合一，本 schema 不再分写）
project_mode_label: "Seed / Init" | "Greenfield" | "Hybrid" | "Brownfield"   # 人读别名（保留 "Seed / Init" 复合标签作历史兼容，机读取 project_mode 单值）
audit_profile: Baseline Survey | Greenfield Survey | Feature-Scoped Full-Surface Audit
generated_at: <ISO 8601>

charter: charter.md
audit: audit.md   # 仅 Hybrid / Brownfield
requirements: requirements.md
design: design.md
tasks: tasks.md

invariants:    # 复述 charter §5 全文，不只是 ID（防 5 跨边界 Task P0 引用底）

  - id: INV-BAN-001
    type: Ban
    rule: "<复述 charter §5 全文>"
    scope: "<复述>"
  - id: INV-LIM-001
    type: Limit
    rule: "<复述>"
    scope: "<复述>"
  - id: INV-SEC-001
    type: Security
    rule: "<复述>"
    scope: "<复述>"

## 防 1 双源单写（详 appendix.md §A.1）：tasks.md 顶部 Markdown 表格从本节重生
traceability:
  generated_from: handoff-payload.yaml#traceability
  generated_at: <ISO 8601>
  tasks:

    - id: TASK-001
      implements: [REQ-001]
      design_refs: [DSN-API-001]
      derived_from_existing: [Replaces EXIST-DSN-DB-003]
      anti_invariants: [INV-LIM-001]
      bdd_scenarios_owned:
        - REQ-001.S1
      touches:    # 防 3 revert_dependency_graph 输入源（详 appendix.md §A.3 + revert_dependency_graph.generated_from 引用）；表格投影 `Touches`（新建）+ `Existing Touches`（修改）并集
        - migrations/0NNN_<名称>.sql
        - backend/models/order.py
      artifacts:
        - docs/specs/`<feature-slug>`/artifacts/reports/plan_001.json
        - docs/specs/`<feature-slug>`/artifacts/reports/cost_ledger.jsonl

first_task:    # 完整复制目标 Task 全部字段
  id: TASK-001
  title: "<动词 + 对象>"
  status: Pending
  context_required:
    p0_essential:    # 防 5：上限 5 条 / 跨边界 / 动凭据 上限 7 条

      - kind: design
        ref: design.md#DSN-API-001
        excerpt: "<request schema 全文复述>"
      - kind: invariant
        ref: charter.md#INV-SEC-001
        excerpt: "<INV 全文复述>"
      - kind: failure_strategy
        ref: design.md#DSN-API-001
        excerpt: "超时=... · 进程崩溃=... · 数据层错误=..."
      - kind: concurrency_lock
        ref: design.md#DSN-API-001
        excerpt: "..."
    p1_reference:    # 备查
      - kind: source
        ref: SRC-002
        anchor: <章节>
      - kind: existing
        ref: audit.md#EXIST-DSN-DB-003
      - kind: design
        ref: design.md#DSN-DB-002
        anchor: Migration Strategy
  test_anchors:    # 防 2 BDD 场景所有权 + Test Anchors（sha256 锁定时机 · 详 appendix.md §A.2.3）
    - path: tests/test_order_create.py
      sha256: <64 位十六进制 · Phase 4 Red 末锁定; Phase 5 仅校验不重写; Phase 6 改测试重锁>
      bdd_scenarios:
        - requirements.md#REQ-001.S1
  verification_commands:
    - pytest -k "test_order_create"
    - python tools/verify_constraints.py
  artifacts:
    - path: docs/specs/`<feature-slug>`/artifacts/reports/plan_001.json
      kind: planner_output
      cardinality: per_task
    - path: docs/specs/`<feature-slug>`/artifacts/reports/verify_001.json
      kind: verify_report
      cardinality: per_task
    - path: docs/specs/`<feature-slug>`/artifacts/reports/cost_ledger.jsonl
      kind: cost_ledger
      cardinality: append_only
    - path: docs/specs/`<feature-slug>`/artifacts/reports/quarantine_001.jsonl
      kind: quarantine_samples
      cardinality: per_task_optional
  revert_command:
    type: business_revert | new_file_only | none
    command: "<具体命令或 N/A 说明>"
  revert_conflict_risk:    # 防 3
    shared_with: [TASK-000]
    shared_files:
      - backend/models/order.py
  resume_strategy:    # appendix.md §A.6 抢占式中断（禁用 git stash · 详 §A.6.2）
    mode: lightweight_wip_commit | wip_branch_reset
    threshold:
      tasks_completed_count_at_pause: <数字>
  links:
    requirements:
      - requirements.md#REQ-001.S1
      - requirements.md#REQ-003

critical_contracts:    # 跨边界 DSN 的 Failure Strategy 摘要
  # 聚合算法：遍历 traceability.tasks[*].design_refs；凡命中跨进程 / 跨网络 / 跨服务 / 跨 LLM 四类跨边界 DSN 者全部纳入。
  # 覆盖范围必须是 tasks.md 全量 Task 触及的跨边界 DSN，禁止只包含 first_task；去重键为 DSN id。

  - id: DSN-API-001
    surface: "POST /api/v1/`<endpoint>`"
    failure_strategy:
      timeout:
        detector: "504 / SLA 3s"
        retry: "1 次 + 指数退避 · 幂等"
        terminal_state: "返回 user-facing error toast"
        compensation: "无（前端重试）"
      crash:
        detector: "process exit code != 0"
        retry: "由 supervisor 拉起；任务进队列重试"
        terminal_state: "users see queue position"
        compensation: "queue table"
      data_layer:
        detector: "PG serialization_failure"
        retry: "3 次 + jitter"
        terminal_state: "Transaction rollback + user prompt"
        compensation: "outbox event"
    concurrency_lock:
      model: "fastapi worker × 4 · queue depth = 100"
      backoff: "指数退避 · cap 5s · max retry 3"
      user_fallback: "429 + retry-after header"
      detection: "queue full / database is locked"

type_ssot:    # 跨端类型契约 SSOT（条件化 · 详 templates/design.md 跨端通信 DSN 硬规则 + project-adapter.md §1）
  # 从 design.md 中所有跨端通信 DSN（DSN-API-* / DSN-UI-* 含 "Type SSOT" 子节者）聚合而成
  # 执行端 Locate / Verify 据此判定 contract drift；缺失即视为跨端类型契约防漂移在 payload 层失效
  # 项目无跨端通信场景 → 本节填 [] 并在备注写 "no cross-end type contract"

  - dsn: DSN-UI-001
    type_ssot: backend/schemas/payment.py::PaymentRequest    # 单端权威源；与 design.md DSN-UI-001 "Type SSOT" 字段一致
    generated_side: frontend/types/generated/payment.ts      # 自动生成端
    regen_command: <项目脚本 contract_regen 槽位 · 详 project-adapter.md §1>
    drift_check: <项目脚本 contract_drift 槽位 · 详 project-adapter.md §1>
    note: "design.md DSN-UI-001 跨端类型契约子节的机读投影；两端手写结构体 = templates/design.md 跨端通信硬规则违规"

revert_dependency_graph:    # 防 3 求交集结果（详 appendix.md §A.3）；从 traceability.touches 起手生成，与各 Task 头部 Revert Conflict Risk 互证
  generated_from: traceability.touches
  generated_at: <ISO 8601>
  edges:

    - from: TASK-002
      to: TASK-001
      shared_files:
        - backend/models/order.py
      note: "从 traceability.touches 集合求交集自动生成；不得反向手改本节"

suspended_state:    # 仅 P-SIBLING / P-CROSS Suspend 期间存在；Resume 时必物理删除（详 appendix.md §A.6.4 / §A.7.1）
  interrupt_type: P-SIBLING | P-CROSS    # P-INLINE 不写入本节
  wip_commit_sha: `<SHA>`
  test_anchors_locked_at: <ISO 8601>     # 跨中断 §A.2 hash 校验的免责锚点；缺失 → 非法中断现场
  phase: <执行端被中断时的 Phase 编号 · 4 | 5 | 6 | 7>    # 供 /specs-execute Resume 定位中断点
  depth: `<N>`                              # 中断栈深度 · depth ≤ 2，≥3 拒绝叠加（详 §A.6.4）
  resume_anchor:
    task_id: TASK-###
    phase: <执行端 phase 编号或名称>
    next_step: <Phase 内子步骤编号或动作描述>    # 限定 Resume 起点到 Phase 内具体动作
  suspended_at: <ISO 8601>
  reason: "<一句话描述抢占原因>"

implementation_reflections:    # 详 appendix.md §A.7（执行端写入；写作端定义热数据上限）
  next_phase_zero_input: true   # 下轮 Phase 0 必读本节
  retention_limit: 10
  active:

    - id: REF-001                                              # archive 与 payload 强制；tasks.md 内联条目可省
      task: TASK-002                                           # 跨视图反查必备
      kind: implementation_choice | new_invariant_candidate | reusable_pattern | spec_drift | audit_debt | ssot_stewardship | test_modified
      severity: low | medium | high
      summary: "<≤ 2 句>"
      suggested_target: charter.md#INV-LIM-NNN                 # 单值；多目标拆多条 reflection；与 tasks.md / archive 三处对齐

        # 候选值范围: charter.md#INV-LIM-NNN | .github/instructions/`<file>`.md | design.md#DSN-* | 母本.md#<章节> | N/A
      approval_required: yes | no
      raised_at: 2026-05-04T10:11:00+08:00
      resolved_at: null                                        # archive 阶段补 · payload 期为 null
      raw_path: `<feature-slug>`/reflections/REF-001.md          # payload 必填；tasks.md 内联条目可省
      # 条件化字段 · 仅 kind: test_modified 必填（详 appendix.md §A.2 与 §A.7 kind 枚举）：
      before_sha256: <64 位十六进制 · Phase 4 锁定值>
      after_sha256: <64 位十六进制 · Phase 6 Refactor 重锁后值>
      reason: "<一句：为何 Refactor 阶段改测试>"
      # 条件化字段 · 仅 kind: audit_debt 且 Existing Touches 扩展场景必填（详 appendix.md §A.7.5）：
      extension_payload:
        task: TASK-007
        added_files: [backend/repositories/X.py, backend/schemas/Y.py]
        reason: "<一句：为何实施期需追加这些公共契约文件>"
        public_contract_impact: none | schema | api | credential | ui
```

### 4.3 schema 硬约束

- **机器友好**：YAML 必须可被 `yaml.safe_load` 解析；不得含未解析占位符。
- **红线全文**：`invariants` 节必须复制 charter §5 表中的 `rule` 与 `scope` 全文，**不只是 ID**。
- **第一个 Task 必全量**：`first_task` 节复制目标 Task 的所有字段。
- **跨边界 DSN 的 Failure Strategy 必摘要**：`critical_contracts` 必须包含 **tasks.md 全量 Task** 触及的所有跨边界 DSN（不只是 first_task）。聚合算法：遍历 `traceability.tasks[*].design_refs`，凡命中跨进程 / 跨网络 / 跨服务 / 跨 LLM 四类跨边界 DSN 者全部纳入；缺一即 payload 不可 Approved。
- **跨端类型契约必摘要（条件化）**：`type_ssot` 节必须聚合 design.md 中所有 `DSN-API-*` / `DSN-UI-*` 含 "Type SSOT" 子节者；项目无跨端通信场景填 `[]` + 备注 `no cross-end type contract`，**不得整节缺省**。执行端 Locate 据此判定跨端 contract drift；缺失视为跨端类型契约防漂移在 payload 层失效。
- **追溯矩阵 SSOT**：`traceability` 节必须枚举全量 Task；每条 Task 必产 **8 键**（`id / implements / design_refs / derived_from_existing / anti_invariants / bdd_scenarios_owned / touches / artifacts`，详 appendix.md §A.1 第 2 项）；可空字段使用 `[]` 显式声明，不得缺省。Markdown 表格从本节重生，投影 7 列（`touches` 不投影，仅留 YAML 供机读；`id` 通过 `Task` 列承载）。
- **抢占现场全量**：`suspended_state` 节仅 P-SIBLING / P-CROSS Suspend 期间存在；Resume 时必物理删除（仅变状态位 = 失职）。出现本节 → §A.7.1 GC 前置检查阻塞，不得启动新 feature 的 Phase 1。
- **回滚依赖图必从 traceability 重生**：`revert_dependency_graph` 节从 `traceability.touches` 求交集生成；与各 Task 头部 `Revert Conflict Risk` 不一致 → 以 graph 为准重生 Task 字段，不得反向手改 graph。
- **Reflections 热数据上限**：`implementation_reflections` 存活 ≤ 10；超限走 §A.7 GC。
- **`severity: high` 且 `kind: spec_drift` 阻塞**：未被处理者 → 不得启动新 feature 的 Phase 1。
- **`mode_propagated` 校验**：`project_mode` / `audit_profile` 必须与 maturity-intake.md 一致；`traceability.tasks[*].derived_from_existing` 在 Greenfield / Seed 模式下统一为 `[Net New]` 或 `N/A (mode=...)`。

---

## 5. Architectural Invariants（INV-*）

### 5.1 ID 与字段格式

详 §1.1。每条 INV 在 charter.md `## 5` 中以表格行存在，并必填：

| 字段 | 含义 |
| ------ | ------ |
| `id` | `INV-`<TYPE>`-###` |
| `type` | `Ban` / `Limit` / `Security` |
| `rule` | 一句完整描述（不仅是关键词） |
| `scope` | 适用范围（模块 / DSN domain / 全局） |
| `rationale` | 一句话理由 |

### 5.2 写作端必须留出的反向追溯

- design.md 中必有 `## 2. Architectural Invariants Inheritance` 表，复述每条 charter `## 5` 中相关 INV-* 与本设计绑定关系（详 `templates/design.md`）。
- tasks.md 每个 Task 必须列 `Anti-Invariants:`（charter `## 5` 中本 Task 严禁违反的 INV-*）；为空填 `none (no applicable INV-* in scope)`。
- handoff-payload.yaml `invariants` 节复制全文（详 §4.2 schema 硬约束）。

### 5.3 写作端硬规则

- charter 必填 `## 5. Architectural Invariants`，至少有 1 条 `INV-BAN-*` 与 1 条 `INV-LIM-*`；无可写时填 `INV-BAN-001: 本 feature 不引入新外部依赖 / 无附加禁用项`。
- 涉凭据 / API Key / PII / 跨网域 / 交易 / 合规类 → 至少 1 条 `INV-SEC-*`；不适用必须在 `## 6. Out of Charter` 明言「无 INV-SEC 适用」。
- design 中若需违反 INV-* → 必须停下、回 Phase 1 修 charter 重批，不得就地豁免。
- INV-* 例子库与项目级注入由 `project-adapter.md §2` 提供。

### 5.4 红线突破处置

- **越界判定**：任意下游阶段（design / tasks / handoff / 执行端反流）引入与 INV-* 冲突的**能力 / 依赖 / 部署形态 / 凭据流 / 跨边界通信**，视为越界，无论该冲突源于显式选型还是隐式后果。
- **处置路径**：停下 → 回 Phase 1 修订 charter `## 5. Architectural Invariants` → 走 Gate A/B 重批 → 重新派生下游。**不得在下游就地豁免、就地降级或加注"临时例外"绕过**。
- **反流补丁通道**：若收到执行端反流的 `kind: spec_drift` + `severity: high`，AI 在 Phase 1 走 SSOT Repair 流程；不得静默修改 charter `## 5`。

---

## 6. 反模式与修复（B-* · Phase 执行期常见路障）

### 6.1 定位

本节是 `/specs-write` Phase 0-5 执行期的**反模式查询表**：每条规则给「触发场景 → 推荐修复 → 回切位置」，agent 在生成过程中可命中规则提前规避。本节与 `entry-decision-tree.md` R-*规则体系互补：R-* 是**判定规则**（用户请求该走哪条路径），B-* 是**反模式规则**（Phase 执行期常见错误如何修复）。

适用范围：所有 Project Mode（Seed / Greenfield / Hybrid / Brownfield） + 所有复杂度 Mode（Medium ① / Medium ② / Large）。Small 复杂度不启用 workflow，不适用。

### 6.2 反模式表（按 ID 升序匹配；第一条命中即返回）

| ID | 触发场景 | 推荐修复 | 回切位置 |
| ---- | ---------- | ---------- | ---------- |
| B-001 | Phase 0 6 维信号扫到真实负载但当前判定为 Greenfield / Seed | 按 R-MODE-1 / R-MODE-2 升级到 Hybrid / Brownfield；必走 Phase 1.5 Spec Derivation Audit | Phase 0 重判 |
| B-002 | Phase 0 SSOT Health = `Needs Repair` / `Unfit As Source` / `SSOT Absent` 但未分流 | 按 R-PHASE0-3/4/5 分流到 `/grill-with-docs` 或 `/project-inception`；带 Return Contract | Phase 0 重判 |
| B-003 | Phase 1 charter `## 5. Architectural Invariants` 无法定义（项目无任何红线候选） | 至少补 1 条 `INV-BAN-001: 本 feature 不引入新外部依赖 / 无附加禁用项`；避免 charter 空红线 | Phase 1 |
| B-004 | Phase 2 REQ 写完发现实际是 `Extends EXIST-*` / `Replaces EXIST-*` / `Conflicts EXIST-*`（不是 Net New） | 按 R-MODE-* 重判 Project Mode；若涉既有 → 走 Hybrid / Brownfield 流程，必走 Phase 1.5 | Phase 0 重判 |
| B-005 | Phase 2 AC 含模糊词（「合适的」「足够的」「响应迅速」「优雅地」） | 重写为可观察可验证可写测试的具体阈值（参 §3.1 EARS 6 句式） | Phase 2 |
| B-006 | Phase 2 BDD Scenario 无法用 Given / When / Then 三段式表达 | 重新拆解：Given = 系统前置状态；When = 用户 / 系统动作；Then = 可观察后果（参 §3.2 BDD） | Phase 2 |
| B-007 | Phase 3 跨边界 DSN（DSN-API / DSN-DB / DSN-EXT 等）无 Failure Strategy | Medium ② 简写也不可空；至少写「失败时返回错误码 + 用户提示 + 日志」；涉跨系统必扩展到 §3.3 Resilience Policy | Phase 3 |
| B-008 | Phase 4 Task 估算 > 1 day | 拆分到 ≤ 1 day；调整 `Depends On` 依赖图；保持每 Task 单一价值交付 | Phase 4 |
| B-009 | Phase 4 Task `Context Required` P0 > 3 项 | 拆分 Task 或重新评估 P0 边界（防 5 注意力稀释硬规则）；P1 不得 > 5 项 | Phase 4 |
| B-010 | Phase 4 Task `Verification Commands` 是自由文本（不是命令） | 改写为可独立运行的命令；不可独立运行则增加 `Setup` 步骤；命令包含完整参数与工作目录 | Phase 4 |
| B-011 | Phase 5 handoff-payload.yaml `traceability` 与 spec.md `## 2.8 Traceability Matrix` 不一致 | 防 1 SSOT 撕裂触发；以 yaml 为 SSOT，spec.md `## 2.8` 同步；不得让 yaml 与 spec.md 各自演进 | Phase 5 |
| B-012 | 某 Phase 命中 Gate A / Gate B / Gate C / Irreversible 但 AI 自决越权 | 必停问；不得 AI-DRI 自决；输出 workflow-qualified state `/specs-write:APPROVAL_PENDING`（参 §2.3 防伪协议） | 等用户批准 |
| B-013 | Phase 执行过程中发现工作量远超 Mode 预期（如 Medium 写到 design 多替代未达共识 / Schema 变更 / API 外部消费者 > 1） | 触发 R-CMPLX-1 升级到 Large；重判复杂度 Mode；不得在 Medium 形态下强行收口 | 回 Phase 0 重判复杂度 |
| B-014 | spec.md 缺 Charter / Requirements / Design / Tasks 四段之一（误以为 Medium 可省略段落） | Medium ② 仍保留四段（仅文件数减少，语义层不减）；缺段视为越界，回退完整三件套 Large 流程 | Phase 3 / Phase 4 |
| B-015 | 多个 Task 触动同一既有文件且 `Revert Command` 重叠 | 防 3 Revert 雪崩触发；用 `revert_dependency_graph` 求交集；拆分 Task 或重设 `Depends On` 依赖 | Phase 4 重组 Task |

### 6.3 与上游规则的关系

| 路障 ID | 必触发的上游规则 | 不得绕过的硬规则 |
| --------- | ------------------ | ------------------ |
| B-001 / B-002 / B-004 | `entry-decision-tree.md` R-MODE-*/ R-PHASE0-* 重判 | 不得就地修补；必须回 Phase 0 |
| B-013 | `entry-decision-tree.md` R-CMPLX-* 重判 | 不得在 Medium 形态下强行收口 Large 工作量 |
| B-012 | `cross-cutting.md §2.3` 防伪协议 | 不得 AI-DRI 自决跨 Gate A/B/C/Irreversible |
| B-014 | `methodology-kernel.md §1` 九层语义层 | 文件数 ≠ 语义层；裁文件不裁语义 |
| B-011 / B-015 | 防 1 SSOT 撕裂 / 防 3 Revert 雪崩 | 必须以机读 SSOT 为准；不得让 yaml 与 markdown 各自演进 |
| B-005 / B-006 | `cross-cutting.md §3.1 EARS` / `§3.2 BDD` | AC 与 Scenario 必须可观察可验证 |
| B-003 / B-007 | `cross-cutting.md §5` Architectural Invariants / `§3.3 Resilience Policy` | charter 红线与跨边界 Failure Strategy 不可空 |

### 6.4 修订规则

- 本表与 `entry-decision-tree.md` / `methodology-kernel.md` / `terminology.md` / `/specs-write.md` / `/specs-execute.md` 字面零漂移。
- 新增反模式时，必须同 PR 在 `terminology.md` 补术语条目（如适用），并在 `entry-decision-tree.md` 评估是否需补 R-* 前置规避规则。
- 删除反模式时，必须确认该路障已被规则表（R-*）前置规避或被项目演进消除，否则不得删除。
- 本表 ID（B-001 ~ B-015）可被任何文档以 `B-*` 精确引用；新增时按数字升序追加，不得复用已删除 ID。
