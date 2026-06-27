---
name: architecture-audit
description: 架构审计与重构路线；在领域语言下识别浅模块、提议 deepening 候选、设计接口、产出可分步执行的安全重构序列
argument-hint: "要审计哪个模块或系统？"
disable-model-invocation: true
---


# /architecture-audit · 架构审计

**定位**：审计代码库架构摩擦，找出 deepening 机会，给出可交给 `/specs-write` 编入合同的小步重构序列。目标是 testability 与 AI-navigability。

**边界**：只输出审计报告、建议性重构计划与文档更新建议；不直接重写代码（重构落地走 `/specs-write` + `/specs-execute`），不直接更新领域文档，不静默改 Authoritative SSOT。本 workflow 产出的 interface / refactor sequence 是 advisory input，只有被 `/specs-write` 编入 `design.md` / `tasks.md` 后才成为执行合同。本工作流是深度/接缝专科审计，**不套用 14 面全景五阶序贯流（unified-14-surface-audit）**，但在探测底层模块时可参考其“第 5 面架构面”作为判断基准。

**斜杠命令**：`/architecture-audit`

**交叉引用**：本 skill 通过 `../specs-write/entry-decision-tree.md §7.5` 引用 R-AUDIT-3；通过 `../specs-write/gate-dag-protocol.md` 引用 HG-DESIGN-*/ S-HG-* / R-INH-2 / FA-HG-2 / DAG-N-AUDIT-*/ DAG-N-SPEC-*。

---

## 懒加载契约

- **MUST read**: `./decision-matrix.md`
- 开始判定或执行 Phase 流程前，必须完整懒加载上述细节。

---

## 1. 共享词表（必须严格使用）

不要用 component、service、API、boundary 这些含糊词。

| 术语 | 定义 |
| ------ | ------ |
| **Module** | 任何有 interface + implementation 的东西（function / class / package / 切片） |
| **Interface** | 调用者必须知道的一切：类型、不变量、错误模式、顺序、配置、性能特征。**不只是签名** |
| **Implementation** | 模块内部实现 |
| **Depth** | 接口处的杠杆。**深** = 小接口背后大量行为；**浅**= 接口几乎和实现一样复杂 |
| **Seam** | 可以在不就地修改的位置改变行为的位置（Michael Feathers）。Seam 是 interface 的**位置选择** |
| **Adapter** | 在 seam 处满足 interface 的具体实现 |
| **Leverage** | 调用者从 depth 得到的收益 |
| **Locality** | 维护者从 depth 得到的收益：变更 / bug / 知识集中 |

核心原则：

-**Depth 是 interface 的属性，不是 implementation 的属性**：深模块内部仍可由小、可换、可测的部件组成，但这些不进 interface

- **Deletion test**：想象删掉这个 module。复杂度消失 → 是 pass-through，不值得；复杂度散到 N 个调用点 → 它在挣钱
- **Interface is the test surface**：调用者和测试穿过同一个 seam；想测 interface 之外，多半模块形状不对
- **One adapter = 假想 seam，two adapters = 真实 seam**：除非确实有变化，不要引入 seam

拒绝的框架：

- 把 depth 定义为"实现行数 / 接口行数"（Ousterhout 原意）→ 奖励填充实现，本 workflow 用 depth-as-leverage
- 把 interface 限定为 TS `interface` 关键字 / 类公共方法 → 太窄
- 用 "boundary"（与 DDD bounded context 重叠）→ 用 seam / interface

---

## 阶段 1 — 探索

### 1.1 输入领域语言

读取：

- 已存在的 `CONTEXT.md` / `CONTEXT-MAP.md` 与各上下文 `CONTEXT.md`
- 已存在的触动区域 `docs/adr/`（缺失不阻塞）
- 母本 / L1 SSOT 中与本审计相关章节
- 项目 `README.md` 或其他明确描述领域语言的文档

后续每个建议必须优先使用已存在领域文档 / L1 SSOT 中的领域名，而不是 `FooBarHandler` 之类。若领域文档不存在，明确标注 `Domain docs missing`，不要把代码名伪装成领域名。

### 1.2 走代码

不要按死板启发式探索。组织化漫游，关注摩擦：

- 理解一个概念需要在多个小模块间反复跳转
- 模块**浅**：interface 几乎和 implementation 一样复杂
- 纯函数被抽出仅为可测，但真实 bug 藏在调用方式里（**locality**流失）
- 紧耦合模块跨 seam 泄漏
- 测不到的部分，或当前 interface 难以测的部分

对疑似浅模块跑 deletion test：删了它，复杂度集中还是只是搬家？"集中"才是想要的信号。

---

## 阶段 2 — 提报候选

输出 numbered 候选清单。每条：

```markdown
## 候选方案 `<n>`: <在领域词汇表中的命名 (name in domain vocabulary)>

- 相关文件 (Files): <涉事文件/模块 (involved modules)>
- 问题所在 (Problem): <为什么当前的架构会产生摩擦阻力 (why current architecture is causing friction)>
- 解决方案 (Solution): <简明地说明要做出什么架构改变 (plain-English what would change)>
- 改造收益 (Benefits):
  - 局部性 (Locality): <变更/Bug 是如何局部集中的 (how change/bugs concentrate)>
  - 杠杆率 (Leverage): <调用方能获得什么好处 (how callers gain)>
  - 测试改善 (Tests): <测试体验能得到何种提升 (how testing improves)>

```

强制规则：

- 用已存在领域文档 / L1 SSOT 词汇 + 本节架构词表；缺领域文档时标注 `Domain docs missing`
- 不要在这一阶段提议接口设计
- ADR 冲突：只有当摩擦真实到值得重开 ADR，才显式标 `_contradicts ADR-NNNN — worth reopening because…_`；不要把 ADR 禁止过的东西列一遍

给出推荐候选和原因，再提请用户裁决："想深入哪一个？" 重构深化候选为 L-DESIGN 级（设计级），必须由人类用户确立。输出后状态为 `/architecture-audit:CANDIDATE_RECOMMENDED_WAITING_DECISION`，禁止 AI-DRI 自动跳过或自决授权。

---

## 阶段 3 — 拷问循环（已选候选）

进入对话式深化：约束、依赖、深化后形态、seam 处的内容、哪些测试存活。

每次只抛出一个 load-bearing 问题；问题抛出后进入 `/architecture-audit:ARCHITECTURE_QUESTION_PENDING`，不得继续追问或假装已确认。用户回答后进入 `/architecture-audit:ARCHITECTURE_ANSWER_RECEIVED`，先复判候选约束、依赖类别和接口风险，再决定继续 Phase 3、进入 Phase 4、进入 Phase 5 或分流 `/grill-with-docs`。

> [!IMPORTANT]
>**挂载推演引擎 (`grill-me`)**：若架构约束、依赖边界或接口选择存在重大的模糊与博弈，你**必须**主动挂载调用 [[grill-me 技能]] (.github/skills/grill-me/SKILL.md) 引擎进行极限追问，由其代理这部分高压对峙直至决策清晰，绝不可在模糊中强行通过。

副作用只生成路由或建议，不在本 workflow 里落地：

- **新概念命中？**推荐 `/grill-with-docs` 把术语并入 `CONTEXT.md`

-**锐化模糊词？**同上
-**用户拒绝候选并给出 load-bearing 理由？**在三条 ADR 条件全成立时建议 ADR；ephemeral / 显然的理由不写
-**想探索接口替代？**进入 Phase 5 接口设计

---

## 阶段 4 — 依赖分类（决定测试与 Seam）

按候选的依赖类型分类，决定 seam 形态：

| 类别 | 描述 | 处理 |
| ------ | ------ | ------ |
| **In-process** | 纯计算 / 内存 / 无 I/O | 总可深化；合并模块，直接通过新 interface 测；无需 adapter |
| **Local-substitutable** | 有本地测试替身（PGLite、in-memory FS） | 替身存在则深化；测试套件里跑替身；seam 是内部 |
| **Remote but owned (Ports & Adapters)** | 自己拥有的跨网络服务 | seam 处定义 port；deep module 拥有逻辑；transport 注入为 adapter；测试用 in-memory adapter，生产用 HTTP/gRPC/queue adapter |
| **True external (Mock)** | Stripe / Twilio 等三方服务 | 通过 port 注入；测试用 mock adapter |

Seam 纪律：

-**One adapter = hypothetical seam, two adapters = real seam**：单 adapter seam 只是 indirection，不要引入

- **Internal seams vs external seams**：deep module 可有内部 seam（私有给自己的实现 + 自己的测试用），不必把内部 seam 暴露在 interface 上

Phase 4 出口判定：

```text

IF interface shape is high-risk, has many callers, crosses ownership seams, or has ≥2 plausible designs
  → INTERFACE_EXPLORATION_NEEDED
ELSE
  → DEPENDENCY_CLASSIFIED → Phase 6 with one recommended interface, only after explicit user confirmation

```

公共 API、多调用方、ownership seam 或高风险接口在进入 Phase 5 前先标记 `/architecture-audit:INTERFACE_DECISION_REQUIRES_USER`；方案展示后进入 `/architecture-audit:INTERFACE_OPTIONS_PRESENTED`，不得仅凭 AI 推荐直接接受。

测试策略：替换不要分层。

- 老 unit tests 一旦有了 deepened module 的 interface 测试覆盖，应在后续 `/specs-write` / `/specs-execute` 重构 Task 中标记为可删除候选；本 workflow 不直接删除测试
- 在 deepened module 的 interface 上写新测试。**Interface 是 test surface**
- 测可观察输出，不要测内部状态
- 测试应当抗内部 refactor：要测行为，不要测实现

---

## 阶段 5 — 方案二选一（接口设计）

### 5.1 定界问题

写一份用户向的 problem space：

- 任何新接口需要满足的约束
- 所依赖的依赖以及类别（Phase 4）
- 一段粗略示例代码作为约束的具象 — 不是提案，只是让约束具象

把这个交给用户后，立刻进入下一步（用户读时 sub-agents 并行工作）。

### 5.2 并行孵化 ≥3 个子代理

每个 sub-agent 必须产出**根本不同**的 interface。各自给独立的技术 brief（文件路径、耦合细节、依赖类别、seam 后内容），并附 §1 词表 + `CONTEXT.md` 词表。给不同的设计约束：

若当前环境不支持 sub-agents，当前代理串行产出 ≥3 个方案；每个方案仍必须使用不同约束，不得把同一方案微调成三个版本。

- Agent 1：最小化接口 — 1–3 个 entry points 上限。最大化每个 entry point 的杠杆。
- Agent 2：最大灵活性 — 支持多种用例与扩展。
- Agent 3：最常见调用者优先 — 默认场景几乎不需思考。
- Agent 4（可选）：围绕 ports & adapters 设计跨 seam 依赖。

每个 sub-agent 输出：

1. Interface（types / methods / params + invariants / ordering / error modes）
2. 调用者使用示例
3. seam 后实现隐藏什么
4. 依赖策略与 adapters
5. trade-offs：哪里杠杆高，哪里薄

### 5.3 对比并推荐

按顺序展示，让用户读完一个再下一个；之后用 prose 比较。维度：

- depth（接口处的杠杆）
- locality（变更集中在哪）
- seam placement
- implementation efficiency
- ease of correct use vs ease of misuse

最后给推荐 — 哪一个最强，为什么；如果不同设计的元素能融合，提出 hybrid。要有立场。

---

## 阶段 6 — 安全重构序列

候选已由用户选择或明确授权 AI-DRI 采用推荐候选时，把 deepening 方向转成小步可验证序列。

每一步必须满足：

- 系统仍可工作
- 要么保留行为，要么把一个 caller / test 移到新 seam 上

每一步格式：

```markdown
### Step `<n>`: <action>

- Change: <最小一致编辑>
- Protection: <test / typecheck / lint / 手动检查>
- Rollback: <暴露错误假设时如何回退>

```

推荐序列形态：

```text

introduce seam
  → add adapter / test coverage
  → route one caller
  → route remaining callers
  → delete old path

```

不要直接给整体重写计划。

---

## 阶段 7 — 交付与接续

输出：

```markdown
## 架构审计报告 (Architecture Audit Report)

## 候选方案 (Candidates)

- [架构摩擦与浅模块候选 1]

## 工作流状态 (Workflow State)

- State: /architecture-audit:<STATE>; common examples: /architecture-audit:SPECS_WRITE_HANDOFF_READY | /architecture-audit:DONE | /architecture-audit:DOMAIN_CONFLICT

## 审计结论 (Outcome)

- <No candidate | User declined | Specs-write handoff ready | Domain conflict routed>

## 选定方案 (Selected Candidate)

- [已选定的深化重构候选]

## 依赖类型 (Dependency Category)

- [依赖类型，如 In-process / Ports & Adapters]

## 接口设计决策 (Interface Decision)

- <selected design or hybrid>

## 权威信息与事实源 (Authority / Fact Source)

- 候选事实依据 (Candidate evidence):
- 接口决策来源 (Interface decision source): <user-selected | low-risk AI-DRI authorization>
- 可执行合同 (Executable contract): not executable until encoded by /specs-write

## 授权边界 / 交接范围 (Authorization Boundary / Handoff Scope)

- 路由动作 (Route Action): <REPORT_AND_STOP | WAIT_FOR_USER | CONFIRMED_ACTION>
- 交接涵义 (Handoff meaning): advisory route input only
- 完工涵义 (Done meaning): architecture audit loop closed only
- 未授权范围 (Not authorized): code refactor / spec write / domain doc write / downstream execution

## 重构序列 (Refactor Sequence)

- 步骤 1 (Step 1) [引入 Seam]
- 步骤 2 (Step 2) [添加测试覆盖/实现具体 Adapter]

## 规格提报交付 Payload (Specs Write Handoff Payload)

- 所需规格锚点 (Required spec anchors):
- 必须转化为 DSN/INV 的风险 (Risks that must become DSN / INV):
- 已解决 (Resolved):
- 仍未解决 (Still unresolved):
- 未授权 (Not authorized):
- 恢复事实源 (Resume source):

## 推荐领域文档更新 (Recommended Domain Doc Updates)

- 提议 CONTEXT.md 更新章节 (Proposed CONTEXT.md sections):
- 提议 ADR 更新候选 (Proposed ADR candidates):

## 推荐下一步路由 (Recommended Next Route)

- /specs-write  （把重构序列固化为 spec 合同）
- /grill-with-docs（如果还有领域语言未澄清）

```

报告后若推荐 `/specs-write`，状态记为 `/architecture-audit:SPECS_WRITE_HANDOFF_READY`，并明确 `This is not executable until encoded by /specs-write`；若无候选或用户不推进，状态记为 `/architecture-audit:DONE`，并明确该状态不表示重构已执行。

---

## 8. 禁用行为

- 不用 component / service / API / boundary 这些含糊词
- 不在 Phase 2 候选阶段就提接口设计
- 不在没有 deletion test 证据时把模块判为浅
- 不引入 single-adapter seam
- 不重新定义 SSOT 已定义的契约
- 不把建议性 interface / refactor sequence 当成可直接执行的合同
- 不直接重写代码 — 重构落地走 `/specs-write` + `/specs-execute`
- 不直接创建或修改 `CONTEXT.md` / ADR — 领域文档落地走 `/grill-with-docs`
- 不批量给重构步骤；一步一可回滚
- 不静默修改 Authoritative SSOT

## 9. 快速自检清单

报告前自检：

- [ ] 是否在领域语言下排查了架构摩擦，并使用了规范词表（Module, Seam, Depth等）？
- [ ] 针对浅模块，是否通过 Deletion Test 评估了其复杂度是否只是“搬家”？
- [ ] 是否在 Phase 2 完成前避免了接口设计？
- [ ] 决定 Seam 形态时，是否确认避免了引入“单 Adapter Seam”？
- [ ] 产出的重构序列是否能够实现“每一步系统均可工作，且具备明确回滚步骤”？
- [ ] 是否已向用户声明，本审计产出的设计仅作为建议（非直接执行合同）？

## 支撑资源

- [decision-matrix.md](./references/decision-matrix.md)
