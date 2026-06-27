# Specs Execute  Blocking, Rollback, and Preemption Rules

> **When to read**: The main workflow MUST instruct Cascade to load this file the moment any Phase needs blocking / rollback / preemption handling.
>
> Section numbers are local to this extracted support document; references to phase rules point to `phase-rules.md`.

---

## 1. 阻塞与回溯

### 1.1 Task 失败时的条件化回滚

本 Task 任一 Phase（尤其 Phase 5 Green / Phase 6 Refactor）在运行验证或集成测试出现不可恢复错误时，回滚优先级：

1. **如本 Task 填了 `Revert Command`**→ 优先执行该命令（标注为条件化回滚点，须先按 §1.5 跑共享文件 Diff 预检；适用于 DB migration / 跨进程契约变更 / 破坏性变更 / 多文件协同）；执行后在 Execution Notes 记录：命令 + 成功 / 失败状态 + 人工复检点

2.**如仅是单文件源码改动失败**→ `git checkout HEAD -- <file>` 即可
3.**如跨多个 Task 需回滚**→ 升级到 `tasks.md §6 Rollback Plan`，走全局回滚并趋同用户
4.**如发现需修改 Spec**→ 不走 Revert、走 §1.3 回切；Revert 仅适用于“实现失败但 Spec 还是对的”场景

设计原则：Task 级 Revert 是“安全重试按键”，是多进程 / 多端交互项目中”出错了敢不敢重试“问题的物理控制点。

### 1.2 阻塞处理

任何阶段发现不合理现象——不能绕道，必须停下：

- 上游 Spec 未 Approved
- maturity-intake.md 缺失、未 Approved、Decision 非 PROCEED_TO_CHARTER、或 SSOT Health 为 Needs Repair / Unfit As Source
- Seed / Greenfield 的 maturity-intake 缺 Baseline / Greenfield Survey evidence 或 Future Audit Trigger
- Hybrid/Brownfield 的 audit.md 缺 Audit Coverage Matrix、真实数据库 readback、文档 SSOT Survey、或 Audit Depth Gate 未 PASS（含 Overall Confidence ≥ 80% / 两个强证据面 confidence 各自 ≥ 80% / Blocking Unknowns = none 三条任一失守）
- Context Required 锚点不存在或为空
- Touches 范围之外被迫修改且不属于 `phase-rules.md §3.1` 允许的执行级补齐
- design.md 缺接口契约 / DB schema
- 测试无法本地运行（环境问题）
- 真实数据库 / 外部依赖不可达
- Pause-and-Ask 白名单命中但未获用户明确批准

### 1.3 回切 `/specs-write` 触发条件

- 实现中发现需求漏洞
- 实现中发现设计冲突
- 实现中发现上游成熟度判定错误（例如 Seed/Greenfield 实际已有既有系统承载，或 Hybrid/Brownfield 被误判为 Greenfield）
- 实现中发现上游现状审计不充分（Audit Debt），尤其是漏真实数据库状态、文档 SSOT、历史归档、调用链或测试基线
- 实现中发现母本 / L1 SSOT 不健康但 Phase 0 未拦截（SSOT Health Debt）
- 实现中发现母本 / L1 SSOT / .github/standards 存在可显著改进点，且不修改 Authoritative SSOT 就无法继续；AI 只能提出 `ssot_stewardship` 草案，不得静默改写
- Touches / Existing Touches 边界需扩展且影响公共契约 / schema / API / UI 大版本 / 新外部依赖 / 跨 feature 范围
- AC 在真实环境下不可达成
- 出现 Breaking Change 而原 Design 未声明

-**charter.md 中的 SRC-### 指向的 SSOT 被发现不够准确或已被修订**-**audit.md 中的 EXIST-* 与当前代码不一致**（现状已漂移）

- 实现中发现本 Task 与 SSOT 的 Authoritative 章节冲突 → 走 charter.md §5 SSOT 修订请求流程
- 执行中需要直接修改 Authoritative SSOT（母本 / L1 SSOT / .github/standards 权威章节）→ 必须回切 `/specs-write` 或请求用户 Gate A/B 批准；执行端不得静默修改

### 1.4 回切流程

1. 在 Task `Execution Notes` 写明触发原因
2. Status 改回 `Blocked`
3. 提示回切 `/specs-write` 修订上游；若修订属于 Gate N/A，可由你-DRI 自动批准并返回执行
4. 上游修订 + Approved（用户 Gate 批准或 AI-DRI 自动批准）后再回 `/specs-execute`

### 1.5 回滚机制·条件化回滚与 Diff 预检（防 3 Revert 雪崩）

执行 Task 级 `Revert Command` 前必走**共享文件预检**，防雪崩：

1. **读共享清单**：从 handoff-payload `revert_dependency_graph` 节取本 Task 的 `shared_files`（该节从 `traceability.touches` 求交集自动生成 · 详写端 §A.3）。
2. **跑 Diff 预检**：

```bash
   git diff --quiet <revert_target>..HEAD -- <shared_file_1> <shared_file_2> ...
```

- exit code = 0 → 共享文件未被后续 Task 改动，可安全跑 `Revert Command`
- exit code != 0 → **禁止自动回滚**，Status 改 `Blocked`，在 Execution Notes 记录【冲突文件清单 + 由哪几个 Task 介入 (查 revert_dependency_graph)】，升级到 `tasks.md §6 Rollback Plan` 走全局回滚 + 人工介入

1. **首个 Task / 无共享者**：`Revert Conflict Risk: N/A` 可跳过预检直接跑 `Revert Command`
2. **原子表述修正**：文档里不再称「原子回滚」，调为「条件化回滚（Conditional Revert）」。跨步骤需回滚 → 同上走全局 Rollback Plan
3. **无法回滚的破坏性变更**→ 必须事前用户批准（`phase-rules.md §3.3` Pause-and-Ask 白名单），并在 `Execution Notes` 留全量回滚步骤

### 1.6 抢占式中断协议（Preemption Protocol）

>**存在意义**：真实工程是抢占式调度网，不是无干扰真空。本节为 §1.1 / §1.2 / §1.3 / §1.5 之外的**第五条逃生通道**，专门处理"用户主动打断当前 Task 去做更紧急 / 更重要的事"的非线性场景。区别于 §1.2 被动阻塞（依赖未就绪）、§1.3 回切（Spec 缺陷）、§1.1 / §1.5 回滚（实现失败），抢占的特点是 **"当前 Task 仍然有效，只是优先级被临时压低"**。

#### 1.6.1 抢占类型三分（必须先分类，不同类型存档粒度不同）

| 类型 | 定义 | 典型场景 | 存档粒度 |
| ------ | ------ | ---------- | ---------- |
| **P-INLINE** | 同 feature 同 Task 内插一行紧急修补 | 发现一个 typo 不修测试就跑不动 / 一个 import 漏写 | 不切 Task，仅 Execution Notes 一行注脚 + 当行 diff 写入 Implements 追溯 |
| **P-SIBLING** | 同 feature 内跨 Task 抢占 | TASK-007 做到一半要先做新插入的 TASK-002.5 紧急重构 | Task 级冻结：状态 + Test Anchors + payload 中途快照 |
| **P-CROSS** | 跨 feature / 全新临时任务 | 线上 P0 bug / 架构顿悟需即刻验证 / 客户紧急需求 | Feature 级冻结：wip commit + 分支隔离 + payload 全量 + 建议新会话窗口 |

AI 在面对"用户提到打断"时，必须**先判定类型再动作**；判定不清 → 默认按更重档位处理（举棋不定时升档不降档），并停下追问用户确认。

#### 1.6.2 Suspend 三件套（机械化动作）

任一抢占触发时 AI 必跑：

```text

1. [Freeze] 物理现场冻结
   - P-INLINE: 不冻结，直接走 `phase-rules.md §6.1` Refactor 路径处理紧急修补
   - P-SIBLING / P-CROSS：按写端 §A.6.2 `Resume Strategy.mode` 二选一分流（轻档 / 重档阅读 tasks.md 本 Task `Resume Strategy:` 字段 + handoff-payload `first_task.resume_strategy.mode`）：
     - **lightweight_wip_commit**（Touches < 5 · 同模块 · Pause 前 ≤ 1 Task Done）：
```

```text
       git add -A && git commit -m "wip(TASK-###): suspend at Phase `<n>` for `<reason>`"

       # 记录 wip_commit_sha 到 suspended_state；Resume 时走 git reset --soft `<wip_commit_sha>`
```

```diff

     - **wip_branch_reset**（Touches ≥ 5 · 跨模块 · Pause 前 ≥ 2 Task Done）：
```

```text
       PRE_WIP_SHA=$(git rev-parse HEAD)               # 记录入 suspended_state.pre_wip_sha
       git checkout -b wip/`<feature-slug>`/`<task-id>`     # 开 wip 分支隔离
       git add -A && git commit -m "wip(TASK-###): suspend at Phase `<n>` for `<reason>`"
       WIP_COMMIT_SHA=$(git rev-parse HEAD)             # 记录入 suspended_state.wip_commit_sha
       git checkout -                                   # 切回主线
       git reset --hard $PRE_WIP_SHA                    # 主线回到中断前状态，P-CROSS 可独立挥希

       # Resume 时走 git cherry-pick `<wip_commit_sha>` 或切回 wip 分支重启
```

```text

     （不用 git stash：stash 会漏 audit-evidence/ 的 untracked 文件 + 未跟踪的 migration / wip 产物；wip commit / wip branch 对中断恢复语义更稳定，且天然纳入 revert_dependency_graph 计算）
     `Resume Strategy.mode` 留空处置：**先按写端 §A.6.2 阈值表自动判档**——Touches < 5 / 同模块 / Pause 前 ≤ 1 Task Done → `lightweight_wip_commit`；Touches ≥ 5 / 跨模块 / Pause 前 ≥ 2 Task Done → `wip_branch_reset`；阈值参数无法判定（如跨模块边界模糊 / Touches 计数与模块归属冲突）→ 停下问用户。`mode` 已声明但与阈值不一致 → 停下问用户 + 在 Execution Notes 留痕冲突点（写端 §A.6.2 反模式：mode 留空让你「自己选」是协议违规，但留空交由协议自动判档不算违规）

2. [Snapshot] payload 中途快照
   重新生成 handoff-payload.yaml，新增 suspended_state 节，字段集与枚举按写端 `cross-cutting.md §4.2` schema 写入。本步关键动作：
     - interrupt_type: 按 §1.6.1 分类填 `P-SIBLING` 或 `P-CROSS`（P-INLINE 不写入本节，详本节顶 P-INLINE 豁免说明）
     - wip_commit_sha: 取 [Freeze] 步骤产出的 wip commit SHA
     - test_anchors_locked_at: 取本 Task `phase-rules.md §4.2` [TDD-Lock] 锁定时间戳（防跨中断 hash 误判免责锚点）
     - phase / depth / resume_anchor / suspended_at / reason: 按 schema 注释填具体值；`depth ≤ 2`，≥3 拒绝叠加（§1.6.4）

1. [Status] tasks.md 状态机更新
   - Status: Blocked(Suspended)    # 机读 token 无空格
   - Notes 加用户原话引用块 + 时间戳（仅状态字串无原话留痕 = 伪造 Approved · 详 `phase-rules.md §1.1` 第 10 项）
   - 输出控制台声明：
     [Preemption-Suspend] TASK-### at Phase `<n>` · type=<P-*> · depth=<N>
     wip_commit=<sha7> · payload snapshot updated.
     建议：<P-CROSS 时建议新开 AI 会话窗口隔离上下文>

```

#### 1.6.3 Resume 三件套（机械化动作）

```text

1. [Locate] 读 handoff-payload.yaml#suspended_state 定位被中断 Phase
   - depth >= 2 → 必须按栈顶逐层 Resume，不允许跳层
   - suspended_state 节缺失但 Status=Blocked(Suspended) → 视为非法中断，停下追问用户

2. [Restore] 物理现场恢复·按 `suspended_state.interrupt_type` + 上游 `Resume Strategy.mode` 分流
   - **共同前置**：校验 git log / `wip/<feature-slug>/<task-id>` 分支中是否存在 `wip_commit_sha`；不存在 → 停下追问当前分支 / wip 分支是否被误删
   - **lightweight_wip_commit 路径**：

```

```text
     git reset --soft `<wip_commit_sha>`    # 解开 wip commit，回到中断那一刻的 working tree
```

```diff

- **wip_branch_reset 路径**（二选一，按主线是否仍住在 `pre_wip_sha`）：

```

```text
     # 选项 A：cherry-pick 回主线（主线未介入新 commit）
     git cherry-pick `<wip_commit_sha>`
     # 选项 B：切回 wip 分支重启（主线介入新 commit 且如果 cherry-pick 会冲突）
     git checkout wip/`<feature-slug>`/`<task-id>`
```

```text

     恢复后需在 Execution Notes 指明选项与主线中断期间的 commit 类型。

- 重算 Test Anchors hash 与 test_anchors_locked_at 时刻锁定值比对：
     · 一致 → 中断期间未动测试 → 直接续 Phase 5 / 6 / 7
     · 不一致但 git log 显示中断期间测试文件无 commit 改动 → 视为合法中断恢复，
       不算 `phase-rules.md §4.2 / §7.1` 防 2 作弊（test_anchors_locked_at 字段是免责锚点）
     · 不一致且测试文件被中断期间 commit 修改 → 视为 `phase-rules.md §6.1` Refactor 路径，
       需补 Reflections kind=test_modified 留痕 before/after hash

1. [Status] tasks.md Status = In Progress
   - suspended_state 节从 payload 物理删除（GC 哲学：仅变状态位 ≠ 删除；必须从 YAML 中删节点）
   - Execution Notes 追加 Resume 时间戳 + 中断时长 + 是否触发 `phase-rules.md §2.2` EXIST Verified By 重检
   - 输出控制台声明：
     [Preemption-Resume] TASK-### back to Phase `<n>` · suspended for <duration>
     · evidence_freshness=<7d-OK | re-verified | re-verify-needed>

```

#### 1.6.4 嵌套抢占红线

- **中断栈深度上限 depth=2**：允许"原 Task 抢占中再插一次紧急任务"，但禁止第三次叠加；命中第三次 → 必须先消化栈顶或全栈 Blocked 后人工介入
- **同类抢占禁连续**：P-CROSS 期间禁止再启动新的 P-CROSS（防止"P0 修着修着又冒出来一个 P0"无限递归）；如确需 → 升级到全局 Rollback + 人工
- **嵌套必同类型或更轻**：P-CROSS 内允许嵌 P-SIBLING / P-INLINE；P-SIBLING 内只允许嵌 P-INLINE；P-INLINE 内允许再嵌 P-INLINE（同档自嵌套合法）；**禁止"轻档抢占嵌重档"**（P-SIBLING 内冒出 P-CROSS 时必须先 Resume P-SIBLING 或将其转为 Blocked 后再走 P-CROSS）
- **跨子领域并行边界**：抢占跨 feature 时仍受**项目级开发协议**"同子领域禁止并行 P2+"约束（来源：项目 user_global / 开发协议 §4.1，非本 spec workflow 自定义）；命中同子领域 → P-CROSS 须先把原 Task Status 强转 Blocked 而非 Blocked(Suspended)，并清空 suspended_state（视为放弃 Resume 路径）

#### 1.6.5 与防御矩阵衔接

- **防 1 SSOT 撕裂**：Resume 后第一件事走 `traceability_check_script`（项目层注入的脚本槽位，默认值详写端 `project-adapter.md §1`）确认表格与 YAML 同步；中断期间表格被 P-CROSS 任务改动者必拒 Resume，先重生
- **防 2 TDD 作弊**：`suspended_state.test_anchors_locked_at` 字段是 §1.6.3 Restore 步骤的免责锚点；该字段缺失 / 与 `phase-rules.md §4.2` [TDD-Lock] 时间戳不一致 → 视为非法中断，强制走 `phase-rules.md §4.2` 重锁
- **防 3 Revert 雪崩**：`wip_commit_sha` 自动加入 `revert_dependency_graph.shares_with` 共享文件计算；P-SIBLING / P-CROSS 期间另一 Task 触发 §1.5 Revert 必跑共享文件 diff 预检，命中冲突 → 升级人工介入
- **防 4 MCP 幻觉**（执行端按写端 §A.6.5 Audit Refresh 子流程执行）：Resume 时若距 `audit.md#EXIST-DSN-*` 的 `Verified By:` 已超 7 天 → 进入写端 §A.6.5 **Audit Refresh 子流程**（仅限被超期 evidence 覆盖的 EXIST-* 重跑 §2.3 重检 4 项格式 + audit-evidence/ · 防 4）。「全面超期 / 新 conflict」判定标准（含 30 天阈值）与处置规则**单点定义于写端 §A.6.5**，本节不重复。执行端追加 Execution Notes 留痕格式：

```text

  evidence_freshness=stale-30d · suspended_at=<起> · resumed_at=<止>

```

  （仅当命中写端 §A.6.5 (c) 条「中断时长 > 30 天」回切判定时写入；非 30 天命中场景按 §A.6.5 (a)/(b) 处置或不回切。）

- **防 5 注意力稀释**：Resume 入口仅吃 `suspended_state` + `first_task.context_required.p0_essential`，**不重读 P1 Reference**（避免重复加载推高 attention_budget）；如 `phase-rules.md §1.1` 估算超 200k → 走 P0-only 档位

#### 1.6.6 与 §1.1 / §1.3 / §1.5 的关系矩阵

| 现象 | 应走 | 不应走 |
| ------ | ------ | -------- |
| 实现跑不通但 Spec 仍对 | §1.1 Task 失败条件化回滚 | 不走 §1.6（Spec 没问题，不是优先级问题） |
| 发现 Spec 缺陷 | §1.3 回切 `/specs-write` | 不走 §1.6（Resume 后还是错的） |
| 跨 Task 共享文件冲突 | §1.5 条件化回滚 + 全局 Rollback | 不走 §1.6（不是抢占而是事故） |
| 用户主动说"先停一下" | **§1.6 Preemption** | 不走 §1.1 / §1.5（当前 Task 仍有效） |
| 依赖 Task 未 Done / API 不可达 | §1.2 Blocked | 不走 §1.6（不是用户主动抢占） |

判定不清 → 默认 §1.6 P-CROSS（最重档位），并停下追问用户确认归类。

---
