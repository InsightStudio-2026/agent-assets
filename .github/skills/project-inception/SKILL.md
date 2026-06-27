---
name: project-inception
description: 从 0 到 1 的项目立项与母本生成；通过项目定位、用户/商业/功能/UIUX/架构研判产出可作为 /specs-write 上游的 L1 SSOT 草案。Use when user wants to start a new project, create project blueprint/charter, generate L1 SSOT, or says 项目立项/新建项目/母本生成/项目定位。
argument-hint: "要创建什么项目？"
---


# /project-inception · 项目立项

**定位**：从模糊想法、空白仓库或未成形方向，生成项目级 L1 SSOT（母本）。

**边界**：只做立项、调研、元设计与母本草案；不写业务代码，不拆 feature Task，不替代 `/specs-write` 产出 feature spec，不静默改 Authoritative SSOT。商业判断只做立项级假设，不给 Kill / Pivot / Validate / Proceed 生死裁定；需要生死裁定时分流 `/business-model-audit`。

**斜杠命令**：`/project-inception`

**下游 workflow**：`/project-steward`、`/specs-write`。

**交叉引用**：本 skill 通过 `../specs-write/entry-decision-tree.md §7.5` 引用 R-AUDIT-5；通过 `../specs-write/gate-dag-protocol.md` 引用 HG-STRAT-*/ HG-DESIGN-* / HG-IRREV-*/ S-HG-* / R-INH-1~2 / DAG-N-SPEC-* 等命名空间。

---

## 懒加载契约

- **MUST read**: `./decision-matrix.md`
- 开始判定或执行 Phase 流程前，必须完整懒加载上述细节。

---

## 0. 深钻协议（跨阶段行为准则）

project-inception 的默认模式是**高效推进**——快速覆盖 9 个阶段、产出母本草案。但真正成熟的母本（如 400+ 行裁决的 L1 SSOT）无法靠每阶段 3 个问题问出来。

当以下条件**同时满足**时，你必须从"快速推进"切换为**深钻模式**：

1. §7.5 跨切面信号研判表判定该章节需要"深写"。
2. AI 对该维度的理解置信度 < 70%。

### 深钻模式三纪律

- **一次一问**：每次只提一个具体问题，等用户回答再继续。不批量抛问题列表。
- **附推荐答案**：每个问题必须附上 AI 的推荐答案与理由。用户可以接受、修改或否决。
- **不达共识不前进**：该分支没有明确共识前，不跳到下一个分支或下一个阶段。

### 退出深钻

满足以下任一条件时退出深钻、回到正常推进节奏：

- 该维度的关键决策分支已全部达成共识。
- AI 对该维度的置信度已升至 ≥ 70%。
- 用户明确要求跳过或延后（记录为待验证假设，写入 §15 关键风险）。

### 与 Phase 的关系

深钻不是独立阶段——它是 Phase 1-7 中任何阶段都可能触发的行为模式。AI 在一个阶段内深钻完关键分支后，继续推进到下一阶段。

---

## 1. 阶段 1 — 构想注入与安全评估

### 1.1 输入形态

用户可能提供：

- 一句话项目想法。
- 目标用户或业务机会。
- 已有竞品 / 替代品。
- 技术冲动或原型想法。
- 空白请求：“帮我想个项目”。
- 已有但混乱的文档 / README / 产品说明。

### 1.2 首轮澄清

只问必要问题，优先给出默认假设。最多一次提出 3 个高价值问题：

- 你最想服务谁？
- 这个项目最不能失败的核心价值是什么？
- 你想做商业产品、内部工具、开源项目、作品集，还是实验？

如果用户没有答案，你必须提出 2-3 个候选方向并给推荐，不得卡住。

### 1.3 立项简报（Inception Brief）

形成临时简报：

```markdown
## Inception Brief

- Raw idea:
- Project type:
- Primary user hypothesis:
- Core problem hypothesis:
- Desired outcome:
- Constraints:
- Unknowns:

```

---

## 2. 阶段 2 — 受众与核心痛点探测

### 2.1 用户与服务对象

识别：

- Primary users。
- Secondary users。
- Buyers / decision makers。
- Operators / administrators。
- External stakeholders。

### 2.2 问题强度

评估：

- 频率：问题多久发生一次。
- 痛感：不解决会怎样。
- 现有成本：时间、金钱、错误率、机会损失。
- 替代方案：用户现在怎么解决。
- 切换门槛：为什么愿意换。

### 2.3 输出

```markdown
## Problem / Audience

- Primary audience:
- Job-to-be-done:
- Pain intensity:
- Current alternatives:
- Why now:
- Confidence:
- Validation needed:

```

---

## 3. 阶段 3 — 竞品、替代方案与转换壁垒捕捉

### 3.1 市场与替代

按项目性质评估：

- 直接竞品。
- 间接替代方案。
- 手工流程 / Excel / Notion / ChatGPT / 外包等非软件替代。
- 用户为什么可能不需要新软件。

### 3.2 商业假设采集

评估：

- 付费主体。
- 付费触发点。
- 获客路径。
- 定价假设。
- 留存驱动。
- 成本结构。
- 法务 / 合规 / 数据风险。

若付费主体、替代方案、获客路径或 MVP 投入任一项为 `Low confidence + high impact`，或无法用立项级假设收敛，停止在本 workflow 内深审，分流 `/business-model-audit`。本 Phase 只能输出 `Hypothesis + Confidence + Need Audit?`，不得输出 Kill / Pivot / Proceed 裁定。

### 3.3 非商业项目适配

若项目不是商业产品，改用：

- 学习价值。
- 作品集价值。
- 社区价值。
- 自动化节省价值。
- 内部效率价值。

### 3.4 输出

```markdown
## Hypothesis Capture

- Value model: <commercial | internal | open-source | learning | portfolio>
- Alternatives:
- Differentiation:
- Distribution hypothesis:
- Monetization / value capture:
- Key risks:
- Confidence:

```

---

## 4. 阶段 4 — 产品市场定位

### 4.1 定位

形成：

- 一句话定位。
- 价值主张。
- 目标用户。
- 核心场景。
- 非目标。
- 成功标准。

### 4.2 取舍

必须明确：

- MVP 做什么。
- 暂不做什么。
- 不服务谁。
- 不追求哪些指标。
- 哪些“好想法”应延后。

### 4.3 输出

```markdown
## Product Positioning

- One-liner:
- For:
- Who need:
- The product is:
- Unlike:
- It provides:
- MVP success criteria:
- Non-goals:

```

---

## 5. 阶段 5 — 核心业务功能模型

### 5.1 功能地图

按用户目标组织，不按技术模块堆砌：

- Core workflows。
- Supporting workflows。
- Admin / operations。
- Integrations。
- Data import / export。
- Notifications / automation。

### 5.2 MVP 边界

分层：

- **P0 MVP**：没有它项目不成立。
- **P1 Soon**：MVP 后最可能需要。
- **P2 Later**：有价值但不能污染初版。
- **Out of Scope**：明确不做。

### 5.3 输出

```markdown
## Functional Model
### P0 MVP

- ...

### P1 Soon

- ...

### P2 Later

- ...

### Out of Scope

- ...

```

---

## 6. 阶段 6 — 核心页面与交互体验模型

### 6.1 用户路径

定义关键路径：

- 首次进入。
- 核心任务完成。
- 失败 / 空状态。
- 权限不足。
- 数据为空。
- 错误恢复。

### 6.2 信息架构

定义：

- 主要页面 / 视图。
- 导航模型。
- 对象关系。
- 用户关注的一级信息。
- 需要隐藏或延后暴露的复杂度。

### 6.3 交互原则

至少覆盖：

- 用户如何知道下一步。
- 系统如何反馈成功 / 失败 / 处理中。
- 哪些操作需要确认。
- 哪些状态需要可撤销。
- 移动端 / 桌面端优先级。

### 6.4 视觉方向

不用产出高保真设计，但要定义：

- 风格关键词。
- 密度。
- 信任感 / 专业感 / 趣味性取向。
- 可访问性底线。
- 主要 UI 风险。

### 6.5 输出

```markdown
## UX / UI Model

- Primary user journey:
- Core screens:
- Navigation model:
- Empty / error / loading states:
- Interaction principles:
- Visual direction:
- Accessibility baseline:

```

---

## 7. 阶段 7 — 工程技术与架构方案选型

### 7.1 技术选型研判

提出 1 个推荐方案和最多 2 个备选。比较：

- 实现速度。
- 可维护性。
- 运行成本。
- 部署复杂度。
- 数据模型契合度。
- 团队 / 用户约束。
- 与现有项目规范的兼容性。

### 7.2 系统边界

定义：

- 前端边界。
- 后端边界。
- 数据存储。
- 鉴权 / 权限。
- 外部服务。
- 后台任务。
- 日志 / 监控。
- 安全 / 隐私底线。

### 7.3 风险与验证

列出：

- 技术未知项。
- 需要 prototype 的问题。
- 需要 spike 的问题。
- 不能在立项阶段拍死的设计。

### 7.4 输出

```markdown
## Architecture Seed

- Recommended stack:
- Alternatives considered:
- System boundaries:
- Data model seeds:
- External dependencies:
- Security / privacy baseline:
- Prototype / spike candidates:
- Confidence:

```

---

### 7.5 母本章节深度研判

并非每个项目都需要 18 章全部深写。在进入 Phase 8 生成母本草案前，你应根据以下跨切面信号，判定各章节的深度等级：

- **深写**：该维度是项目成败的核心变量，需要完整裁决与细节。
- **概述**：需要明确立场但一段话足矣。
- **N/A**：对当前项目不适用，标注跳过理由即可。

#### 跨切面信号与章节激活表

| 项目特征信号 | 若命中 → 以下章节需深写 |
| ------------- | ---------------------- |
| 多地区 / 多司法管辖区运营 | §12 合规红线、§5 商业模型（区域定价）、§11 架构（数据隔离） |
| 终端用户之外存在供给方 / 合作方 / 渠道方 | §13 供给侧生态、§7 领域对象（角色与所有权）、§5 商业模型（分成） |
| AI / ML 作为核心产品能力 | §3 护城河（数据飞轮）、§7 领域对象（生成物生命周期）、§12 合规（内容分级） |
| 离线优先 / 多端同步 | §11 架构（冲突解决）、§7 领域对象（状态机与幂等） |
| 内容 / 资产是核心价值载体 | §7 领域对象（资产本体）、§9 分层预留（内容扩展路线）、§13 供给侧 |
| 企业 / B2B 销售动线 | §5 商业模型（席位 / 合同）、§6 增长（企业获客路径）、§13 供给侧 |
| 平台型产品（双边 / 多边市场） | §13 供给侧、§5 商业模型（平台抽成）、§14 运营度量（双边指标） |
| 强监管行业（金融、医疗、教育） | §12 合规红线、§7 领域对象（审计链）、§18 附录（政策假设） |

#### 使用方式

1. 在 Phase 2-3（受众、市场）阶段识别项目命中了哪些信号。
2. 在 Phase 7（架构种子）结束后，用本表交叉校验是否遗漏了关键维度。
3. 在 Phase 8 生成母本草案时，按深度等级决定各章节的篇幅与细节密度。
4. 若某章节被标为 N/A，在母本中保留章节标题并注明跳过理由，避免后续读者误以为遗漏。

---

## 8. 阶段 8 — 项目母本草案生成

### 8.1 推荐文件名

按项目文档体系选择：

- 中文项目：`docs/blueprints/母本.md` 或项目既有 L1 SSOT 路径。
- 英文项目：`docs/project-ssot.md` 或 `docs/product-brief.md`。
- 无 `docs/` 时：建议创建 `docs/`，但需用户确认。

### 8.2 母本结构

母本草案必须包含：

```markdown

- ## 1. 文档身份与演进治理 (SSOT 优先级、冲突处理、时间三维——现行/预留/远期)
- ## 2. 产品本质与战略定位 (一句话定义、核心价值主张、"它不是什么")
- ## 3. 核心护城河与可防御性 (内容/数据/时间/网络效应/复制效率/品牌——竞争壁垒自审)
- ## 4. 受众、核心痛点与替代方案 (用户分层、痛点强度、现有解法、切换成本)
- ## 5. 商业模型与收入引擎 (定价策略、付费触发点、免费层设计、成本结构、单位经济)
- ## 6. 增长、获客与分发假设 (冷启动路径、渠道假设、留存驱动、口碑飞轮)
- ## 7. 核心领域对象与数据契约 (系统的"名词"——关键实体、关系、状态机、所有权边界)
- ## 8. 业务与功能模型 (P0 MVP / P1 Soon / P2 Later / Out of Scope)
- ## 9. 阶段性交付与分层预留 (当前现行层 → 增强层 → 扩张层 → 远期预留；底层抽象一步到位、上层功能分阶段)
- ## 10. 体验与界面交互模型 (核心旅程、信息架构、交互原则、视觉方向、可访问性)
- ## 11. 架构种子与技术选型 (技术栈、系统边界、外部依赖、需验证的技术未知项)
- ## 12. 合规、隐私与安全红线 (法务边界、数据主权、内容分级、地缘合规分线)
- ## 13. 供给侧生态与多角色治理 (若涉及：供给方角色、价值分配、资产归属、关系终止善后)
- ## 14. 运营度量与成功标准 (核心指标、阶段目标、持续验证纪律)
- ## 15. 关键风险与假设校验 (CA-### 核心假设、验证方式、假设被推翻时的应对)
- ## 16. 首批 Spec 候选 (FS-### 优先级、依赖关系、建议模式)
- ## 17. 决策日志 (历史裁决追溯与演进脉络)
- ## 18. 附录 (若涉及：高密度参数表、政策假设、机制推演、大维度矩阵)

```

### 8.3 Critical Assumptions

必须列 3-7 条最可能推翻项目的假设：

```markdown
## Critical Assumptions

- CA-001: <假设>
  - Breaks if:
  - How to validate:
  - If false:

```

### 8.4 First Spec Candidates

输出可交给 `/specs-write` 的候选 feature：

```markdown
## First Spec Candidates

- FS-001: <feature name>
  - Why first:
  - Expected scope:
  - Depends on:
  - Suggested mode: <Seed / Greenfield / Hybrid / Brownfield>

```

---

## 9. 阶段 9 — 关卡审批与开发分流

### 9.1 关卡判定

| Gate | 命中条件 | 动作 | HG-*绑定 |
| ------ | ---------- | ------ | ---------- |
| Gate A Strategy | 项目定位、目标用户、商业模式、MVP 边界需要用户裁决 | 给推荐方案 + ≤2 备选，State = `/project-inception:GATE_APPROVAL_PENDING`，等待批准 | `HG-STRAT-{slug}-001`（母本定位 / MVP）；packet F-HG-1~8 必齐；失败 → `FA-HG-1` 回项目重定位 |
| Gate B Critical Design | 技术栈、数据边界、核心 UX 路径有重大不可逆影响 | 给推荐方案 + 代价，State = `/project-inception:GATE_APPROVAL_PENDING`，等待批准 | `HG-DESIGN-{slug}-001`（架构种子 / 数据边界 / UX 路径）；失败 → `FA-HG-2` 回 Phase 6/7 |
| Gate C Real-World Side Effect | 需要外部发布、真实用户调研、真实付费、生产账号或外部 API 承诺 | State = `/project-inception:REAL_WORLD_SIDE_EFFECT_APPROVAL_PENDING`，停下请求批准 | `HG-IRREV-{slug}-001`（外部副作用）；TTL-HG-6 单次执行不缓存；失败 → `FA-HG-4` 必停问 |
| N/A | 无 Strategy / Critical Design / Real-World Side Effect 裁决；但母本仍未授权 | 输出母本草案并请求权威批准，State = `/project-inception:SSOT_PROPOSED` | `S-HG-1 GATE_NOT_REQUIRED`（所有 HG-* 未触发，但仍需母本权威批准） |

### 9.2 输出格式

```markdown
## 项目孵化与母本确立报告 (Project Inception Report)

## 工作流状态 (Workflow State)

- State: /project-inception:<STATE>; common examples: /project-inception:SSOT_PROPOSED | /project-inception:AUTHORITATIVE_REPAIR_PROPOSED | /project-inception:GATE_APPROVAL_PENDING | /project-inception:REAL_WORLD_SIDE_EFFECT_APPROVAL_PENDING | /project-inception:AUTHORITATIVE_READY_RETURN | /project-inception:AUTHORITATIVE_ROUTE_TO_SPEC_READY

## 已完工项 (Completed)

- L1 权威母本草案 (L1 SSOT draft): <path or proposed path>

## 孵化结论 (Outcome)

- <Draft proposed | Authoritative repair proposed | Approved return | Route ready to spec | Waiting for approval>

## 权威信息与事实源 (Authority / Fact Source)

- 权威母本文件 (Authoritative SSOT): <path or N/A>
- 授权批准来源 (Approval source): <user approval quote or waiting>
- 草案推演依据 (Draft source): <conversation / files / research evidence>

## 关键设想与假设 (Critical Assumptions)

- CA-001 ...

## 质量门禁 (Gate)

- 门禁类型 (Type): <N/A | Gate A/B/C>
- 当前步进阶段 (Current phase):
- 需要裁决的决策 (Decision needed):
- 阻碍性事实源 (Blocking fact source):

## 授权边界 (Authorization Boundary)

- 路由动作 (Route Action): <CONTINUE_IN_WORKFLOW | WAIT_FOR_USER | REPORT_AND_STOP | CONFIRMED_ACTION>
- 授权范围 (Authorized scope): <draft only | approved Authoritative SSOT write / replacement | named downstream entry input>
- 未授权范围 (Not authorized): <feature spec writing / code changes / tracker writes / real-world side effects / downstream workflow internal actions>

## 推荐下一步 (Recommended Next Step)

- 路由动作 (Route Action): <WAIT_FOR_USER | REPORT_AND_STOP>
- 推荐路由 (Recommended route): </project-steward | /specs-write | N/A>
- 授权批准状态 (Authorization): <waiting for user approval | approved by user quote>
- First spec candidate: FS-###

```

### 9.3 批准后

| SSOT State | 含义 | 谁可推进 |
| ------------ | ------ | ---------- |
| `Draft` | AI 生成的母本草案 | AI 可产出 |
| `Proposed` | 等用户批准的权威候选 | 等用户 |
| `Authoritative` | 可作为 `/specs-write` 上游 | 用户批准后 |

用户明确批准后，才能：

- 创建新的 Authoritative SSOT 文件。
- 替换已有母本。
- 将草案标记为 authoritative。
- 在用户明确要求继续派生 feature spec 时，进入 `/specs-write`；否则返回 `/project-steward` 重新判断 next best action。

---

## 10. 禁用行为

- 不把 feature spec 当母本。
- 不把愿望清单当产品定位。
- 不在没定义用户和问题时先选技术栈。
- 不伪造市场调研、竞品事实或用户证据。
- 不静默覆盖已有 Authoritative SSOT。
- 不直接拆 `TASK-###`。
- 不写业务代码。
- 不把所有功能都塞进 MVP。
- 不用“平台化 / 智能化 / 自动化 / 一站式”这类空词替代具体价值。

---

## 11. 快速自检清单

交付前自检：

- [ ] 是否明确了目标用户？
- [ ] 是否明确了核心问题？
- [ ] 是否评估了替代方案？
- [ ] 是否给出商业或非商业价值假设模型？
- [ ] 是否定义了 MVP 与非目标？
- [ ] 是否覆盖功能、UX/UI、架构三条线？
- [ ] 是否标注关键假设和验证计划？
- [ ] 是否产出可作为 `/specs-write` 上游的 L1 SSOT 草案？
- [ ] 是否避免写代码和拆 Task？

## 支撑资源

- [decision-matrix.md](./references/decision-matrix.md)
