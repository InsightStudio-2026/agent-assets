# design.md 硬规则

> **When to read**: 在 `/specs-write` Phase 3 落 `design.md` 前，必须与 `templates/design.md`、`cross-cutting.md §5` 一起读取。
>
> Cross-references: `cross-cutting.md §1` covers IDs / derivation / traceability; `cross-cutting.md §4` covers `handoff-payload.yaml`; `appendix.md §A.*` covers 防 1-5.

---

## 1. Design 硬规则

> 本节按“必填条件 + 硬规则码 + 字段最小集”格式化；详细解释见 `cross-cutting.md §4` / `appendix.md §A.*`。

- 每个章节有稳定 `DSN-`<domain>`-###` ID（`<domain>` 枚举见 `cross-cutting.md §1.2`）。
- 每个章节必须声明 `Linked Requirements`；不得存在孤立设计。
- **每个 DSN 必须填 `Derived From`**+ `Relation to Existing`（五选一，详 `cross-cutting.md §1.4`）；Net New 附 Justification。
- Hybrid / Brownfield 模式必须写 `## 1.5 Reuse vs New` 决策一览。

-**不得重新定义 SSOT 已定义的契约**（状态机 / L1-L10 / 词表 / 权限模型），必须用 `@<路径>#<章节>` 引用（详 `cross-cutting.md §1.4`）。

- **不得引入 charter.md §5 INV-* 禁用的能力 / 依赖 / 部署形态**；如需突破 → 停下回 Phase 1 修订 charter 重批。
- **不得违反 INV-SEC-***：凡涉及凭据 / API Key / PII / 内网拓扑 / 交易接口 的 `DSN-API-*` / `DSN-SEC-*` / `DSN-OBS-*` 必须**显式复述适用的 INV-SEC-* 原文**；明言凭据读取路径（KMS / Vault / keyring / env 注入点），不得含真实凭据值。
- **条件化展开**：
  - 涉及数据 → `DSN-DB-*` + Migration Strategy（条件化必填，见下“DSN-DB Replaces 数据迁移安全网”）。
  - 涉及接口 → `DSN-API-*` + 请求/响应契约。
  - 涉及 UI → `DSN-UI-*` + 状态/空态/错误态（推荐附视觉锚点 Figma node ID / 设计稿哈希 / Storybook story）。
  - 涉及后台任务 → 幂等性 / 重试 / 日志 / 监控。
  - 涉及 AI/LLM → `DSN-LLM-*`（**三件防御必填**：Prompt Boundaries 注入防御 + Deterministic Fallback 保底静态逻辑 + Context Truncation Strategy 上下文裁剪优先级）。
  - 涉及跨端通信 → `DSN-API-*` 或 `DSN-UI-*` 必须声明：(a) **类型契约 SSOT 方**（哪一端是单一事实来源），(b) **类型生成方式**（autogen 脚本路径或 contract test 坐标，详 `project-adapter.md §1`），(c) **drift 检查**（CI 如何检测两端类型不同步）；**严禁两端分别手写结构体**。
  - 涉及安全 → 权限模型 / 数据分级 / 审计日志。
- **跨边界 DSN 必填 Failure Strategy**（跨进程 / 跨网络 / 跨服务 / 跨 LLM 调用边界的 `DSN-API-*` / `DSN-ARCH-*` / `DSN-OBS-*`）；至少覆盖三类故障 × 四元素：
  - 三类故障：**超时**/**进程崩溃**/**数据层错误**（死锁 / 连接丢失 / 验证失败）。
  - 四元素：**检测信号**（SLA 阈值 / exception 类型）/ **重试策略**（次数 / 退避 / 是否幂等）/ **用户可见最终态**/**是否落补偿事件**。
  - 单进程内部 DSN 可豁免，但需备注 `Failure Strategy: N/A (in-process)`。
- **Concurrency & Lock**（条件化必填）：跨边界 DSN 命中以下任一场景必填——(a) 接口可被多端 / 多 Task 并发调用；(b) 涉及共享资源（SQLite 写路径 / 本地文件锁 / 本地缓存目录 / 唯一索引热点）；(c) 异步 IPC / message queue / event bus / 后台 worker pool；(d) LLM 调用涉及 token quota / rate limit / 代理连接池共享。字段至少覆盖：
  - **并发模型**（worker 数 / 队列深度 / 锁粒度：表锁 / 行锁 / 进程内 mutex / 文件锁）。
  - **退避与排队**（指数退避参数 / 最大重试 / FIFO 队列上限）。
  - **用户可见兜底**（拥塞时给前端的状态码 / 文案 / 是否排队 / 是否快速失败）。
  - **检测信号**（SQLite `database is locked` / PG `serialization_failure` / 429 / queue full）。
  - 不命中场景的纯函数式 / 冷路径 DSN 可填 `Concurrency & Lock: N/A (single-caller / pure)`。
- 必须写 `Alternatives Considered`（至少 1 条对比）与 `Risks`。
- **DSN-DB "Replaces" 数据迁移安全网**（条件化必填）：凡 `DSN-DB-*` 同时满足 (1) `Relation to Existing: Replaces EXIST-DSN-DB-*` 且 (2) 命中以下任一——(a) 改既有列定义 / 约束（NOT NULL / FK / CHECK / type）；(b) 改既有表语义（enum 收紧 / 拆合既有表 / 重命名列）；(c) drop 既有列 / 既有表——必填 `Migration Strategy:` **三选一**：
  - **策略 1 · Shadow Write / Dual Write**：双写期窗口（起止条件） + 一致性校验脚本路径（表 vs 影子表对账 + 样本 diff） + 切流条件（连续 N 小时校验 0 差异） + 回切窗口（发现差异多久内能回切）。
  - **策略 2 · Backward-Compatible Stepwise**：分多 PR 阶段部署，每阶段可独立部署且可独立回滚；step 1 = add column nullable / add new table；step 2 = backfill；step 3 = switch reads；step 4 = drop 旧列 / 旧表；每步必明言「部署后多久才进下步」与「本步独立回滚命令」。
  - **策略 3 · Downgrade Script**：保留旧结构镜像表 / 双向可执行的 down 迁移脚本，能将新结构业务数据**无损**转回旧结构；**不是**`git checkout` / `migrate downgrade` 这类只在无业务数据时才可行的物理回滚。
  -**豁免（加性变更）**：纯新增表 / 纯加索引 / 纯加 nullable 列且 default 兼容 → 可填 `Migration Strategy: N/A (additive only)`，但需在 DSN 上明言「兼容性等级 = 加性变更」。
  - **必含 `business_data_safety_proof`**：1–2 句说明为何本策略能保证业务数据无损转回，而非仅是 schema 能回。
  - **rationale**：物理 `Revert Command` 对已产生新结构业务数据的场景 = 丢数据；本条强制在业务设计层预留可逆路。
