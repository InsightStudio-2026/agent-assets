# Gate / DAG Protocol · 跨 workflow 横切协议事实源

> 本文是 `.github/workflows/` 下全部 workflow 的 **Hard-gate / DAG / Revert Graph 横切协议事实源**。
>
> 不是 workflow，是协议层；定义统一命名 / 字段 / 状态 / 投影规则；各 workflow 入口通过引用本文实现 Gate / DAG / Revert 术语统一，不另造审批语义。
>
> 本文档自身遵循结构化规则表 + ID 体系格式规范（入口骨架 + 支撑文档分离 + 零 ASCII 流程图）。

---

## 0. 定位与不做什么

### 0.1 本文是什么

| 属性 | 值 |
| ------ | ----- |
| 资产类型 | 横切协议文档（不是 workflow，不是 skill） |
| 适用范围 | `.github/workflows/` 全部 12 个 workflow + 未来新增 workflow |
| 命名空间 | `HG-*`（Hard-gate）+ `DAG-N-*`（DAG 节点）+ `DAG-E-*`（DAG 边）+ `DAG-D-*`（DAG 依赖类别） |
| 上游事实源 | 本文自身即为横切协议 SSOT；与 `cross-cutting.md §2` Decision Gate + `../../specs-execute/protocols/blocking-and-rollback.md` 字面零漂移 |
| 下游 | 12 个 workflow 入口 + `../references/cross-cutting.md §2` Decision Gate + `../../specs-execute/protocols/blocking-and-rollback.md` |
| 与 R-*/ B-* 关系 | R-*（entry-decision-tree.md）= 路径判定；B-*（cross-cutting.md §6）= 反模式修复；HG-*/ DAG-* = 风险闸 + 依赖图。三套规则互补不重复 |

### 0.2 本文不做什么

| 不做什么 | 理由 |
| ---------- | ------ |
| 不新增独立 `/gate-dag-governance` workflow | 仅在 4.1 §条件化场景启用；默认作为协议层投影到现有 workflow |
| 不另造 Gate 审批语义 | 复用 `cross-cutting.md §2.3` 防伪协议；本文只统一命名层与跨 workflow 投影 |
| 不要求每个微小任务都建 DAG 节点 | DAG 只用于 §2.2 列出的 7 类依赖 |
| 不要求每次对话都创建 gate packet | Hard-gate 只用于真正高风险 / 不可逆 / 跨边界动作 |
| 不把 Hard-gate 变成"用户批准所有实现细节" | Hard-gate 是横切风险闸，不是 micro-management |
| 不用 DAG 取代 `tasks.md` / `handoff-payload.yaml` / issue provider 的权威状态 | DAG 是依赖投影，不是事实源 |
| 不让 Gate 批准继承到下游真实世界副作用 | `APPROVED` 仅限当前批准范围；不可传递到其他环境 / 版本 / 后续动作 |

### 0.3 本文与既有 Decision Gate 的层次关系

| 层 | 文档 | 范围 | 例 |
| ---- | ------ | ------ | ---- |
| L1 · Decision Gate（specs-write 内部） | `cross-cutting.md §2` | specs-write Phase 0-5 + specs-execute Phase 0-9 | Gate A / Gate B / Gate C / Irreversible Action / Approval.Status |
| L2 · Hard-gate（横切） | **本文 §1** | 全部 workflow + 跨 workflow 投影 | HG-RELEASE-*/ HG-SEC-* / HG-MIGR-*/ HG-IRREV-* |
| L3 · DAG / Revert Graph（横切） | **本文 §2 / §3** | 全部 workflow 的 task / spec / audit / migration / release / rollback / incident 依赖 | DAG-N-*/ DAG-E-* / `revert_dependency_graph` |

**继承规则**：L2 / L3 的概念以 L1 的防伪协议（`cross-cutting.md §2.3`）为底；本文不重复 L1 已定义的批准语义，只补充横切命名 + 字段 + 状态 + 投影。

---

## 1. Hard-gate 协议

### 1.1 ID 体系 · `HG-`<DOMAIN>`-###` 命名空间

| ID 前缀 | Domain | 风险类别 | 继承 L1 Decision Gate |
| --------- | -------- | ---------- | ------------------------ |
| `HG-STRAT-###` | Strategy | 战略 / scope / charter / 母本级 | Gate A 战略级 |
| `HG-DESIGN-###` | Design | 跨边界设计 / API 契约 / Schema | Gate B 设计级 |
| `HG-IMPL-###` | Implementation | 实现期非可逆动作 | Gate C 实现级 |
| `HG-OPS-###` | Operations | 运营动作 / 配置变更 / 权限变更 | — |
| `HG-IRREV-###` | Irreversible | 删除 / 生产部署 / 付费 / 外部副作用 | Irreversible Action |
| `HG-RELEASE-###` | Release | 生产发布 / 部署 / 真实迁移 | — |
| `HG-SEC-###` | Security | 权限模型 / PII 流向 / 密钥 / 证书 | — |
| `HG-MIGR-###` | Migration | Schema 变更 / backfill / 兼容窗口 | — |
| `HG-AUDIT-###` | Audit | 14 面审计强证据面阈值 / 强必审项 | Audit Depth Gate |
| `HG-INCIDENT-###` | Incident | 事故响应 / runbook / 止血动作 | — |

**命名规则**：

- `<DOMAIN>` 必须是上表枚举之一；不得自创新 domain 不登记。
- `###` 为 3 位数字，按 domain 内首次出现顺序递增；不得复用已注销 ID。
- 全表 ID 必须登记到 §5 命名空间登记表（防漂移）。

### 1.2 Hard-gate 最小字段表

每个硬闸至少包含 8 个字段（与 `cross-cutting.md §2` Decision Gate 字段一致）：

| ID | 字段 | 含义 | 必填 | 示例 |
| ---- | ------ | ------ | ------ | ------ |
| F-HG-1 | **Gate ID** | 稳定 ID（HG-`<DOMAIN>`-###） | 是 | `HG-RELEASE-001` |
| F-HG-2 | **触发原因** | 为什么必须进硬闸 | 是 | "首次生产部署 / 用户可见发布" |
| F-HG-3 | **授权主体** | 谁批准；若用户批准，保留批准原话 | 是 | `user:Calvin` + 原话引用 |
| F-HG-4 | **作用范围** | 环境 / 文件 / 数据表 / issue / release channel / 外部服务 | 是 | "production env / users 表 / GitHub release v1.2.0" |
| F-HG-5 | **前置证据** | 测试 / 审计 / dry-run / 备份 / 监控 / review | 是 | `tests passed: 1234`, `dry-run: 2026-05-23T10:00`, `backup: s3://...` |
| F-HG-6 | **回滚方案** | 命令 / 步骤 / 触发条件 / 不可回滚说明 | 是 | `git revert <SHA>` + 回滚步骤；不可回滚必明示 |
| F-HG-7 | **失败状态** | 失败后进入哪个 workflow / state | 是 | `→ /bug-audit:BUG_AUDIT_REQUIRED` |
| F-HG-8 | **过期规则** | 证据过期时间 | 是 | "migration dry-run 超过 7 天需重跑" |

### 1.3 Hard-gate 状态枚举（9 种）

| ID | 状态 | 含义 | 转入 |
| ---- | ------ | ------ | ------ |
| S-HG-1 | `GATE_NOT_REQUIRED` | 当前动作不触发 Hard-gate | 不需批准 |
| S-HG-2 | `GATE_REQUIRED` | 已识别需要 Hard-gate，待装配 packet | → `GATE_PACKET_INCOMPLETE` 或 `WAITING_GATE_APPROVAL` |
| S-HG-3 | `GATE_PACKET_INCOMPLETE` | packet 缺字段（F-HG-1~8 任一未填） | 补字段 → `GATE_REQUIRED` 或 `WAITING_GATE_APPROVAL` |
| S-HG-4 | `WAITING_GATE_APPROVAL` | packet 完整，等授权主体批准 | → `GATE_APPROVED` / `GATE_REJECTED` / `GATE_EXPIRED` |
| S-HG-5 | `GATE_APPROVED` | 已批准；可执行受限范围内动作 | → `GATE_PASSED`（执行成功）/ `GATE_FAILED`（执行失败） |
| S-HG-6 | `GATE_REJECTED` | 授权主体拒绝 | → 修订上游或终止动作 |
| S-HG-7 | `GATE_EXPIRED` | packet 证据已过期（按 F-HG-8 规则） | 重跑证据 → `GATE_REQUIRED` |
| S-HG-8 | `GATE_PASSED` | 动作执行完成且与 packet 声明一致 | 终态 |
| S-HG-9 | `GATE_FAILED` | 动作执行失败 | 走 F-HG-7 失败状态 |

### 1.4 与 specs-write Decision Gate 的继承规则

| ID | 规则 | 适用 |
| ---- | ------ | ------ |
| R-INH-1 | `HG-STRAT-###` 必须同时是 specs-write Gate A | charter / scope / 母本级动作 |
| R-INH-2 | `HG-DESIGN-###` 必须同时是 specs-write Gate B | 跨边界设计 / Schema / API 契约 |
| R-INH-3 | `HG-IMPL-###` 必须同时是 specs-write Gate C 或 specs-execute 实现期审批 | 实现期非可逆动作 |
| R-INH-4 | `HG-IRREV-###` 必须同时是 specs-write Irreversible Action（cross-cutting.md §2.3） | 删除 / 生产部署 / 付费 / 外部副作用 |
| R-INH-5 | `HG-OPS-*` / `HG-RELEASE-*` / `HG-SEC-*` / `HG-MIGR-*` / `HG-AUDIT-*` / `HG-INCIDENT-*` | 不强制继承 L1，按本协议 §1.2 / §1.3 独立装配 |
| R-INH-6 | 任一 HG-*命中后，必须按 cross-cutting.md §2.3 防伪协议留批准证据；AI 不得 AI-DRI 自决 | 全部 HG-* |

### 1.5 失败动作与回切（F-HG-7 字段细则）

| ID | 失败场景 | 回切目标 workflow | 状态种子 |
| ---- | ---------- | ------------------- | ---------- |
| FA-HG-1 | charter / scope 类 HG-STRAT-*被拒 | `/specs-write:GATE_BLOCKED` 或 `/project-inception` | `EXTERNAL_AUDIT_REQUIRED` |
| FA-HG-2 | 设计类 HG-DESIGN-* 被拒 | `/specs-write` Phase 3 修 design.md | `SPEC_REPAIR_REQUIRED` |
| FA-HG-3 | 实现类 HG-IMPL-*失败 | `/specs-execute` Phase 5 重做 / 回切 spec | `SPEC_REPAIR_REQUIRED` |
| FA-HG-4 | 不可逆 HG-IRREV-* 失败 | 必停问用户 + 启动事故响应 | `WAITING_USER` + `/observability-incident`（如适用） |
| FA-HG-5 | 发布 HG-RELEASE-*失败 | `/release-deploy` 触发 rollback；产生 incident 时启动 `/observability-incident` | `ROLLBACK_REQUIRED` |
| FA-HG-6 | 安全 HG-SEC-* 失败 | `/security-privacy-audit` 重审 + `/bug-audit`（如已部署） | `SECURITY_BLOCKED` |
| FA-HG-7 | 迁移 HG-MIGR-*失败 | `/data-migration-safety` 重核 + 数据回滚 | `MIGRATION_BLOCKED` |
| FA-HG-8 | 审计 HG-AUDIT-* 不达阈值 | 回对应审计 workflow 补证据 | `AUDIT_INCOMPLETE` |
| FA-HG-9 | 事故 HG-INCIDENT-* 处置失败 | 升级 + `/observability-incident` 不得绕过 | `INCIDENT_OPEN` |

### 1.6 过期规则（F-HG-8 字段示例）

| ID | 证据类型 | 默认过期窗口 | 重跑触发 |
| ---- | ---------- | -------------- | ---------- |
| TTL-HG-1 | migration dry-run | 7 天 | 超期前必须重跑；schema 任何变更立即过期 |
| TTL-HG-2 | security threat model | 30 天或权限模型变更 | 权限 / PII 流向 / 密钥流向变化立即过期 |
| TTL-HG-3 | audit evidence（14 面审计） | 14 天或上游 SSOT 变更 | charter / requirements / design 任一修订立即过期 |
| TTL-HG-4 | release readiness | 当前 release candidate 生命期 | 任一 commit 进入 release branch 立即过期 |
| TTL-HG-5 | strategy approval（HG-STRAT-*） | charter 生命期 | charter 任一修订立即过期 |
| TTL-HG-6 | irreversible action approval | 单次执行；不缓存 | 每次动作必须重审 |

---

## 2. DAG 协议

### 2.1 ID 体系

| 命名空间 | 含义 | 示例 |
| ---------- | ------ | ------ |
| `DAG-D-<NUM>` | DAG 依赖类别（7 类，详 §2.2） | `DAG-D-1` Task dependency |
| `DAG-N-`<TYPE>`-###` | DAG 节点 | `DAG-N-TASK-001` |
| `DAG-E-<TYPE>` | DAG 边类型（8 种枚举） | `DAG-E-REQ` requires |

### 2.2 DAG 适用范围（7 类依赖）

| ID | 依赖类别 | 含义 | 主要 owner workflow |
| ---- | ---------- | ------ | --------------------- |
| DAG-D-1 | **Task dependency** | Task 之间的接口 / 数据结构 / 顺序依赖 | `/specs-write` + `/specs-execute` |
| DAG-D-2 | **Spec dependency** | Task 依赖 requirement / design / ADR 批准 | `/specs-write` |
| DAG-D-3 | **Audit dependency** | 安全 / 性能 / 数据 / UX 审计必须先于发布 | `/security-privacy-audit` / `/performance-reliability-audit` 等 |
| DAG-D-4 | **Migration dependency** | schema / backfill / 兼容窗口 / 清理任务 | `/data-migration-safety` |
| DAG-D-5 | **Release dependency** | build / migration / feature flag / deploy / smoke / monitoring | `/release-deploy` |
| DAG-D-6 | **Rollback dependency** | 代码回滚前是否必须先恢复数据 / 关闭 flag / 暂停队列 | `/release-deploy` + `/observability-incident` |
| DAG-D-7 | **Parallel safety** | 哪些任务可并行 / 哪些任务因同表-同模块-同路由禁止并行 | `/specs-write` + `/specs-execute` |

### 2.3 DAG 节点最小字段（10 字段）

| ID | 字段 | 含义 | 必填 |
| ---- | ------ | ------ | ------ |
| F-N-1 | **Node ID** | 稳定 ID（DAG-N-`<TYPE>`-###） | 是 |
| F-N-2 | **Node Type** | `spec` / `task` / `audit` / `migration` / `release` / `rollback` / `incident` 之一 | 是 |
| F-N-3 | **Owner Workflow** | 哪个 workflow 拥有本节点（节点状态变更只能由 owner 写） | 是 |
| F-N-4 | **Inputs** | 上游事实源（Anchor / spec section / artifact） | 是 |
| F-N-5 | **Outputs** | 本节点交付物（artifact / state / evidence） | 是 |
| F-N-6 | **Depends On** | 上游节点 ID 列表（DAG-N-*） | 是（无依赖填 `[]`） |
| F-N-7 | **Blocks** | 下游被本节点阻塞的节点 ID 列表 | 是（无下游填 `[]`） |
| F-N-8 | **Parallel Group** | 可并行节点组 ID（不可并行填 `null`） | 是 |
| F-N-9 | **Gate Required** | 关联的 HG-* ID 列表（无 gate 填 `[]`） | 是 |
| F-N-10 | **Done Evidence** | Done 证据（test passed / verification command output / artifact path） | 是 |

### 2.4 DAG 边类型（8 种）

| ID | 边类型 | 语义 | 示例 |
| ---- | -------- | ------ | ------ |
| DAG-E-REQ | `requires` | A 必须在 B 之前完成（强依赖） | DAG-N-TASK-002 requires DAG-N-TASK-001 |
| DAG-E-BLK | `blocks` | A 阻塞 B（A 未完成 B 不得开始） | DAG-N-AUDIT-001 blocks DAG-N-RELEASE-001 |
| DAG-E-VRF | `verifies` | A 验证 B 的正确性 | DAG-N-TASK-002 verifies DAG-N-TASK-001 |
| DAG-E-REL | `releases` | A 释放 B（资源 / 锁 / 部署窗口） | DAG-N-MIGR-001 releases DAG-N-RELEASE-001 |
| DAG-E-RBK | `rolls_back` | A 是 B 的回滚节点 | DAG-N-ROLLBACK-001 rolls_back DAG-N-RELEASE-001 |
| DAG-E-SUP | `supersedes` | A 取代 B（B 废弃；A 是替代实现） | DAG-N-SPEC-002 supersedes DAG-N-SPEC-001 |
| DAG-E-PAR | `can_parallel_with` | A 与 B 可并行（明确并行安全） | DAG-N-TASK-003 can_parallel_with DAG-N-TASK-004 |
| DAG-E-CFL | `conflicts_with` | A 与 B 冲突（同时间禁止并行 / 同资源） | DAG-N-TASK-005 conflicts_with DAG-N-TASK-006（同表 schema 变更） |

### 2.5 DAG 不应引入的过度设计

| ID | 反模式 | 正确做法 |
| ---- | -------- | ---------- |
| AP-DAG-1 | 每个微小任务都建 DAG 节点 | DAG 只用于 §2.2 的 7 类依赖；微小任务用 spec.md 内 `Depends On` 即可 |
| AP-DAG-2 | DAG 报告当成业务事实源 | DAG 只是依赖投影；业务事实源仍是 spec / handoff-payload / issue provider |
| AP-DAG-3 | DAG 节点状态由非 owner workflow 修改 | F-N-3 Owner Workflow 唯一；其他 workflow 只读 |
| AP-DAG-4 | 用 DAG 取代 `tasks.md` Depends On 字段 | DAG-N-TASK-* 与 tasks.md 字段一一对应；不重复定义 |
| AP-DAG-5 | DAG 节点缺 F-N-9 Gate Required 字段 | 即使无关联 gate 也必须填 `[]`；缺字段视为 packet 不完整 |

---

## 3. Revert Graph 协议

### 3.1 复用 specs-execute 现有契约

| 契约 | 当前位置 | 本协议关系 |
| ------ | ---------- | ------------ |
| `revert_dependency_graph` 字段 | `../../specs-execute/protocols/blocking-and-rollback.md` + `tasks.md` 每 Task 头部 | 本协议**继承不重写**；不新造命名 |
| `Revert Command` 字段 | `tasks.md` 每 Task 7 字段之一 | 本协议作为 Hard-gate F-HG-6 回滚方案的最小执行单元 |
| Shared file diff 预检 | `../../specs-execute/protocols/blocking-and-rollback.md §1.4` | 本协议 §3.2 的衔接点 |

### 3.2 Revert Graph 与 Hard-gate / DAG 衔接

| ID | 规则 | 适用 |
| ---- | ------ | ------ |
| RG-1 | 任一 HG-*的 F-HG-6 回滚方案必须可投影到 `revert_dependency_graph`；不可投影 = 不可回滚必须明示 | 全部 HG-* |
| RG-2 | DAG-E-RBK 边的源节点必须是 `Node Type: rollback`；目标节点必须是被回滚的实际动作节点 | 全部 DAG-N-ROLLBACK-* |
| RG-3 | 多个 Task 触动同一既有文件且 `Revert Command` 重叠 → 按 cross-cutting.md §6 B-015 求 `revert_dependency_graph` 交集；触发防 3 Revert 雪崩 | `/specs-execute` 实现期 |
| RG-4 | 生产部署 HG-RELEASE-* 失败 → DAG-E-RBK 边自动激活；Rollback 节点 owner 是 `/release-deploy` | `/release-deploy` 失败路径 |
| RG-5 | 数据迁移 HG-MIGR-*失败 → 必须先恢复数据再回滚代码（DAG-E-REQ：DAG-N-ROLLBACK-DATA-* requires DAG-N-ROLLBACK-CODE-*） | `/data-migration-safety` 失败路径 |
| RG-6 | 不可回滚动作（F-HG-6 明示不可回滚）→ Revert Graph 中以 `null` 标记；HG-IRREV-* 必须命中此规则 | 全部 HG-IRREV-* |

---

## 4. 跨 workflow 投影对照表

### 4.1 投影原则

| ID | 原则 | 适用 |
| ---- | ------ | ------ |
| PRJ-1 | 现有 workflow 中的 Gate / Pause-and-Ask / Depends On / Revert / rollback 术语**不更名**；只在入口 Companion Documents 中加引用本协议作为命名空间事实源 | 全部 12 个 workflow |
| PRJ-2 | workflow 内部状态枚举（如 `WAITING_GATE_APPROVAL` / `ROLLBACK_REQUIRED`）必须与本协议 §1.3 状态枚举一致；冲突 = 该 workflow 失效 | 全部 |
| PRJ-3 | 每个 workflow 在涉及高风险 / 不可逆动作时必须显式标注 `HG-`<DOMAIN>`-###` ID；不得只用"Hard-gate"无 ID | `/release-deploy` / `/security-privacy-audit` / `/data-migration-safety` / `/desktop-release` / `/specs-execute` Irreversible |
| PRJ-4 | 每个 workflow 输出 artifact 中涉及任务 / 节点依赖时必须显式标注 `DAG-N-`<TYPE>`-###`；不得只用"Depends On"无 ID | `/specs-write` tasks.md / handoff-payload / `/release-deploy` release-plan.md |
| PRJ-5 | review / audit 类 workflow 在检查"是否绕过 Gate"时按本协议 §1.3 + §5.1 命名空间登记表查证；不得自创 ID 名 | `review` / `/architecture-audit` / `/bug-audit` |
| PRJ-6 | issue tracker（GitHub Issues）作为 DAG-N-* 投影目标时，issue body 必须显式标注 owner Node ID + Gate Required 字段；防 issue 成为第二事实源 | `/tasks-to-issues` / `/issue-triage` |

### 4.2 12 个 workflow 现状与投影对照

| Workflow | 现有 Gate 术语 | 现有依赖术语 | 现有回滚术语 | 主要投影 HG-* | 主要投影 DAG-N-* | 整合方式 |
| ---------- | --------------- | -------------- | ------------- | --------------- | ------------------ | ---------- |
| `/specs-write` | `cross-cutting.md §2` Decision Gate（Gate A/B/C/Irreversible）+ `Approval.Status` | `tasks.md` `Depends On` 字段 | tasks.md `Revert Command` | `HG-STRAT-*`（Gate A）/ `HG-DESIGN-*`（Gate B）/ `HG-IMPL-*`（Gate C）/ `HG-IRREV-*`（Irreversible） | `DAG-N-SPEC-*` / `DAG-N-TASK-*` | 在 `tasks.md` / `handoff-payload.yaml` 生成 Task DAG + 风险 gate；spec.md `## Approval` 节标 `Gate ID:` 引用 HG-* |
| `/specs-execute` | `PAUSE_AND_ASK_PENDING` / `WAITING_USER` / Pause-and-Ask 4 项（生产 DB / 删除破坏 / 付费 / L-DESIGN） | `../../specs-execute/protocols/blocking-and-rollback.md` 前置检查 + DAG 前置节点 | `Revert Command` / `revert_dependency_graph` / `ROLLBACK_REQUIRED` | `HG-IMPL-*`（执行级审批）/ `HG-IRREV-*`（4 项 Pause-and-Ask） | `DAG-N-TASK-*`（消费 specs-write 产出）+ `DAG-N-ROLLBACK-*` | 执行 Task 前检查 DAG-N-* 前置节点状态 = `Done` 且 `Gate Required` 全 `GATE_PASSED`；未满足不得 `Done` |
| `/project-steward` | 不直接审批；只识别是否需要 gate / DAG | 不直接管理；只读取下游 workflow 状态 | 不直接执行；只报告 route | — | — | 路由决策时检查任一下游 workflow 是否处于 `WAITING_GATE_APPROVAL` / `ROLLBACK_REQUIRED`；输出 route 时引用对应 HG-*/ DAG-N-* ID |
| `/project-inception` | charter / 母本级动作 = 战略级审批 | — | — | `HG-STRAT-*`（项目定位 / 母本 / MVP 决策） | `DAG-N-SPEC-*`（charter / L1 SSOT 节点） | 输出 L1 SSOT / 母本时绑定 `HG-STRAT-###`；继承 specs-write Gate A 语义 |
| `/business-model-audit` | 商业闭环 / 付费 / Pivot-Kill-Validate-Proceed 决策 | — | — | `HG-STRAT-*`（商业模式生死判断） | `DAG-N-AUDIT-*`（商业审计节点） | 商业闭环判断绑定 `HG-STRAT-###`；输出 artifact 中 Pivot-Kill 决策必须有 Gate ID |
| `/architecture-audit` | 架构摩擦 / 浅模块 / seam / interface 重塑批准 | 设计前置依赖 | — | `HG-DESIGN-*`（架构边界变更） | `DAG-N-AUDIT-*`（架构审计节点） + `DAG-N-SPEC-*`（重构提案） | 架构重构提案绑定 `HG-DESIGN-###`；继承 specs-write Gate B 语义 |
| `/bug-audit` | bug 影响面 / 严重性 / 根因分流批准 | bug 修复依赖（spec / hotfix / 架构） | — | `HG-IMPL-*`（修复执行批准）/ `HG-INCIDENT-*`（如已上线 P0） | `DAG-N-AUDIT-*`（bug 审计节点）+ `DAG-N-INCIDENT-*`（如适用） | bug 分流后绑定对应 `HG-*`；P0 上线 bug 必走 `HG-INCIDENT-*` |
| `/grill-with-docs` | 术语 / ADR / 领域文档冲突解决 | — | — | `HG-DESIGN-*`（如涉及契约重塑） | `DAG-N-AUDIT-*`（领域审计节点） | 文档冲突修复完成后产出 `DAG-N-AUDIT-*` 节点；不直接装配 HG-* |
| `/issue-triage` | issue 状态机 / blocked / ready-for-agent | issue blocker 关系 | — | — | `DAG-N-TASK-*`（issue 投影） | 读取 DAG 判断 `blocked` / `ready-for-agent`；不写 DAG，只投影 issue 状态 |
| `/tasks-to-issues` | approved tasks 发布到 issue tracker | tasks.md `Depends On` → issue blocker | — | — | 把 `DAG-N-TASK-*` 投影到 issue blocker | 把 DAG 依赖投影到 issue blocker；不让 issue 成为第二事实源 |
| `/repo-agent-setup` | 仓库初始化批准（issue tracker / 标签词表 / 领域文档读取规则） | — | — | `HG-OPS-*`（仓库级配置变更） | `DAG-N-SPEC-*`（agent 上下文配置节点） | 配置变更绑定 `HG-OPS-###`；首次启用必有用户批准 |
| `/repo-safety-setup` | 危险 git 操作拦截 / pre-commit / 格式化 / typecheck / 测试入口 | — | rollback 命令（git revert / git reset / 文件恢复） | `HG-OPS-*`（安全基线变更）/ `HG-IRREV-*`（git history 修改） | `DAG-N-SPEC-*`（安全基线配置节点） | 危险 git 操作拦截绑定 `HG-IRREV-*`；任何写 .git/hooks/ 必有用户批准 |

### 4.3 已交付 P0 / P1 workflow 的命名空间映射

| 工作流 | 主要 HG-*命名空间 | 主要 DAG-N-* 命名空间 | 关键状态 |
| ---------------- | --------------------- | ------------------------ | ---------- |
| `/release-deploy` | `HG-RELEASE-*` / `HG-IRREV-*`（首次生产部署 / 真实迁移 / 付费） | `DAG-N-RELEASE-*` / `DAG-N-MIGR-*`（消费）/ `DAG-N-ROLLBACK-*` | `WAITING_DEPLOY_APPROVAL` → `APPROVED_TO_DEPLOY` → `DEPLOYING` → `DEPLOYED_PENDING_SMOKE` |
| `/security-privacy-audit` | `HG-SEC-*`（权限模型 / PII 流向 / 密钥流向变更） | `DAG-N-AUDIT-*`（安全审计节点）+ `DAG-N-AUDIT-*` blocks `DAG-N-RELEASE-*` | `THREAT_MODEL_DRAFTED` → `SECURITY_APPROVED` / `SECURITY_BLOCKED` |
| `/observability-incident` | `HG-INCIDENT-*`（事故响应 / 止血动作） | `DAG-N-INCIDENT-*` + `DAG-N-ROLLBACK-*`（如需回滚） | `INCIDENT_OPEN` → `INCIDENT_TRIAGED` → `INCIDENT_MITIGATED` → `INCIDENT_CLOSED` |
| `/data-migration-safety` | `HG-MIGR-*` / `HG-IRREV-*`（不可逆数据动作） | `DAG-N-MIGR-*` blocks `DAG-N-RELEASE-*` | `MIGRATION_DRY_RUN_REQUIRED` → `MIGRATION_APPROVED` → `MIGRATION_EXECUTED` / `MIGRATION_BLOCKED` |
| `/desktop-release` | `HG-RELEASE-*`（installer / signing / update channel） | `DAG-N-RELEASE-*` | `INSTALLER_BUILD_PENDING` → `SIGNING_APPROVED` → `RELEASED_TO_CHANNEL` |
| `/performance-reliability-audit` | `HG-AUDIT-*`（性能阈值 gate） | `DAG-N-AUDIT-*` blocks `DAG-N-RELEASE-*`（如关键路径回归） | `BENCHMARK_BLOCKED` / `PERF_APPROVED` |

### 4.4 review skill 的核验规则

review 是 skill 不是 workflow，但作为变更审查的最末环节，必须按本协议核验：

| ID | 核验项 | 命中 = 拒合 |
| ---- | -------- | ------------- |
| RV-1 | 变更涉及 HG-RELEASE-*/ HG-IRREV-* / HG-SEC-*/ HG-MIGR-* 范围但 commit / PR 中无对应 Gate ID 引用 | 是 |
| RV-2 | DAG-N-* 节点 `Done Evidence` 字段缺失或与实际 commit 不一致 | 是 |
| RV-3 | 变更绕过 §2 DAG `Depends On` 顺序（依赖节点未 Done 即开始下游） | 是 |
| RV-4 | Gate packet（F-HG-1~8）有任一字段缺失即合并 | 是 |
| RV-5 | `revert_dependency_graph` 与 `Revert Command` 重叠未求交集（B-015） | 是 |

---

## 5. ID 命名空间登记表

### 5.1 已分配命名空间（防漂移）

| 命名空间 | 用途 | 拥有文档 | 审批人 |
| ---------- | ------ | ---------- | -------- |
| `R-ENTRY-*` / `R-MODE-*` / `R-CMPLX-*` / `R-PHASE0-*` / `R-AUDIT-*` / `R-RETURN-*` / `R-PREEMPT-*` / `R-CLOSEOUT-*` | 入口决策规则 | `entry-decision-tree.md` | 写作端 |
| `B-001 ~ B-015` | Phase 执行期反模式 | `../references/cross-cutting.md §6` | 写作端 |
| `HG-STRAT-*` / `HG-DESIGN-*` / `HG-IMPL-*` / `HG-OPS-*` / `HG-IRREV-*` / `HG-RELEASE-*` / `HG-SEC-*` / `HG-MIGR-*` / `HG-AUDIT-*` / `HG-INCIDENT-*` | Hard-gate | **本文 §1** | 横切协议（specs-write 维护） |
| `DAG-D-1 ~ DAG-D-7` | DAG 依赖类别 | **本文 §2.2** | 同上 |
| `DAG-N-SPEC-*` / `DAG-N-TASK-*` / `DAG-N-AUDIT-*` / `DAG-N-MIGR-*` / `DAG-N-RELEASE-*` / `DAG-N-ROLLBACK-*` / `DAG-N-INCIDENT-*` | DAG 节点 | **本文 §2.3** | 同上 |
| `DAG-E-REQ` / `DAG-E-BLK` / `DAG-E-VRF` / `DAG-E-REL` / `DAG-E-RBK` / `DAG-E-SUP` / `DAG-E-PAR` / `DAG-E-CFL` | DAG 边类型 | **本文 §2.4** | 同上 |
| `F-HG-1 ~ F-HG-8` | Hard-gate 字段 | **本文 §1.2** | 同上 |
| `S-HG-1 ~ S-HG-9` | Hard-gate 状态 | **本文 §1.3** | 同上 |
| `R-INH-1 ~ R-INH-6` | Hard-gate 与 Decision Gate 继承规则 | **本文 §1.4** | 同上 |
| `FA-HG-1 ~ FA-HG-9` | Hard-gate 失败动作 | **本文 §1.5** | 同上 |
| `TTL-HG-1 ~ TTL-HG-6` | Hard-gate 过期规则 | **本文 §1.6** | 同上 |
| `F-N-1 ~ F-N-10` | DAG 节点字段 | **本文 §2.3** | 同上 |
| `AP-DAG-1 ~ AP-DAG-5` | DAG 反模式 | **本文 §2.5** | 同上 |
| `RG-1 ~ RG-6` | Revert Graph 衔接规则 | **本文 §3.2** | 同上 |

### 5.2 命名空间冲突防护

| ID | 规则 |
| ---- | ------ |
| NS-1 | 任何文档新增 ID 命名空间前必须查 §5.1 登记表；冲突 → 改名或合并 |
| NS-2 | 同一 ID 命名空间不得跨文档分散定义（如 `HG-RELEASE-*` 只能在本文 §1 定义；`/release-deploy` 入口只能引用，不得新增） |
| NS-3 | 删除 ID 时必须同 PR 修订所有引用方；不得"软删除"留死引用 |
| NS-4 | ID 数字段不得复用已注销 ID（如 `HG-RELEASE-001` 注销后，新 gate 用 `HG-RELEASE-002` 起步） |

---

## 6. 修订规则

### 6.1 修订触发

| ID | 触发场景 | 修订路径 |
| ---- | ---------- | ---------- |
| MOD-1 | 新增一类 Hard-gate domain（如 `HG-PERF-*`） | 本文 §1.1 加 domain + §5.1 登记 + 各相关 workflow 入口同 PR 加引用 |
| MOD-2 | 现有 HG-*/ DAG-* 字段语义变更 | 本文 §1.2 / §2.3 修订 + 各下游 workflow 同步 |
| MOD-3 | 新增一类 DAG 依赖（超出现有 7 类） | 本文 §2.2 加 DAG-D-8 + 必有真实业务场景驱动；不得仅为对称添加 |
| MOD-4 | 现有 Decision Gate（`cross-cutting.md §2`）状态枚举变更 | 本文 §1.4 R-INH-* 同步修订 |
| MOD-5 | 横切协议自身修订 | 本文修订必须同 PR 修订所有引用方；本文即为横切协议 SSOT |

### 6.2 修订禁忌

| ID | 禁忌 | 理由 |
| ---- | ------ | ------ |
| NO-MOD-1 | 不得在本文外新增 HG-*/ DAG-* 命名空间 | 防 1 SSOT 撕裂 |
| NO-MOD-2 | 不得让某个 workflow 入口"扩展"本文规则集 | 本文是横切协议；扩展 = 漂移 |
| NO-MOD-3 | 不得用 mermaid / ASCII 流程图替换规则表 | 违反 §0.2 AI 友好格式硬规范 |
| NO-MOD-4 | 不得让 HG-* 状态枚举与 specs-write Decision Gate / specs-execute workflow state 冲突 | 必须可继承可投影 |
| NO-MOD-5 | 不得引入"软 Hard-gate"（即可被 AI 自决跳过的 gate） | Hard-gate 必须真硬 |

### 6.3 与上游事实源的零漂移核验

| 上游事实源 | 同步检查项 |
| ----------- | ------------ |
| 本文即为横切协议 SSOT | 字段 / 状态 / 适用范围 / 节点模型 / 边类型字面一致 |
| `../references/cross-cutting.md §2` Decision Gate | Gate A / B / C / Irreversible Action 投影一致 |
| `../references/cross-cutting.md §6` 反模式表 | B-015 与 RG-3 衔接；不重复定义 |
| `entry-decision-tree.md` R-* 规则 | R-PHASE0-*/ R-AUDIT-* 投影到 HG-AUDIT-*/ HG-STRAT-* 一致 |
| `../../specs-execute/protocols/blocking-and-rollback.md` | `revert_dependency_graph` 字段语义一致；本文 §3 不重写 |

---

## 7. 交付状态与路线图

### 7.1 交付记录表

| 批次 | 状态 | 范围 | 输出 |
| ------ | ------ | ------ | ------ |
| 第一交付 | 已完成 | §0-§3 + §5-§6 + §7（本文） | HG-*/ DAG-* / 字段 / 状态 / 衔接规则定义 |
| 第二交付 | 已完成 | `specs-write.md` + `specs-execute.md` 入口 | 引用本文协议；术语统一 |
| 第三交付 | 已完成 | `project-inception.md` + `business-model-audit.md` + `bug-audit.md` + `project-steward.md` + `grill-with-docs.md` 入口 | 引用本文协议；术语统一 |
| 第四交付 | 已完成 | `architecture-audit.md` + `issue-triage.md` + `repo-agent-setup.md` + `repo-safety-setup.md` + `tasks-to-issues.md` 入口 | 引用本文协议；术语统一 |
| 第五交付 | 已完成 | 核心 P0 / P1 workflow（`/release-deploy` / `/security-privacy-audit` / `/observability-incident` / `/data-migration-safety` 等） | 统一以本文为命名空间事实源 |

每批次交付后必须执行 §6.3 零漂移核验。
