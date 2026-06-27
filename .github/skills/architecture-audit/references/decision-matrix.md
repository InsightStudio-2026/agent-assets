---
description: "架构审计工作流（/architecture-audit）专属的触发判定、状态转换路由、状态权威与动作决策矩阵"
---

# 架构审计决策矩阵（/architecture-audit）

## 0. 触发与临界路由决策表

| ID | 前置条件 | 匹配动作 | 下一步/目标路由 | 源 / 备注 |
| ---- | ---------- | ---------- | ----------------- | ----------- |
| R-ROUTE-ARCH-1 | 用户显式 `/architecture-audit` | 启用 workflow | 进入 Phase 1 (Explore) | 显式入口 |
| R-ROUTE-ARCH-2 | 用户要做架构审查、寻找重构机会、深化模块或解决复杂跨模块接口摩擦 | 启用 workflow | 进入 Phase 1 (Explore) | 架构诉求 |
| R-ROUTE-ARCH-3 | `/project-steward` 决策推荐架构审计 | 启用 workflow | 进入 Phase 1 (Explore) | 管家引流 |
| R-ROUTE-ARCH-4 | 系统状态不清、下一步推进方向不明 | 停止并重定向 | 路由至 `/project-steward` | 临界状态 1 |
| R-ROUTE-ARCH-5 | 缺失母本或 L1 SSOT | 停止并重定向 | 路由至 `/project-inception` | 临界状态 2 |
| R-ROUTE-ARCH-6 | 属于纯缺陷根因诊断（局部、具体 bug） | 停止并重定向 | 路由至 `diagnose` 技能 | 临界状态 3 |
| R-ROUTE-ARCH-7 | 属于新功能、新需求开发、大重构落地（而非纯架构设计与重构路线设计） | 停止并重定向 | 路由至 `/specs-write` 与 `/specs-execute` | 临界状态 4 |
| R-ROUTE-ARCH-8 | 逻辑简单明确且适合 TDD 验证 | 停止并重定向 | 路由至 `tdd` 技能或直接执行 | 临界状态 5 |
| R-ROUTE-ARCH-9 | 以上皆不满足且非架构审计诉求 | 不启用 workflow | 不启用本 workflow | 默认退出 |

## 0.1 状态与路由汇总 (State / Route Summary)

| 状态 (State) | 判定 | 下一步 | Gate / DAG ID 映射 |
| ------- | ------ | -------- | --------------------- |
| `/architecture-audit:NO_CANDIDATE` | 未发现真实架构摩擦 | 输出无候选报告后收束为 `/architecture-audit:DONE` | `S-HG-1 GATE_NOT_REQUIRED` |
| `/architecture-audit:CANDIDATE_RECOMMENDED_WAITING_DECISION` | 有候选且 AI 已给唯一推荐，但尚未确认推进对象 | 等用户选择 | 创建 `DAG-N-AUDIT-{slug}-arch` 节点（status: Recommending）；候选 = 设计级决策候选 |
| `/architecture-audit:CANDIDATE_AUTO_SELECTED_BY_AUTHORIZATION` | 用户明确授权 AI-DRI 采用已展示的推荐候选 | 进入 Phase 3 Grilling Loop | `S-HG-5 GATE_APPROVED`（候选选择级）；不继承给最终接口决策 |
| `/architecture-audit:CANDIDATE_SELECTED` | 用户已选候选 | 进入 Phase 3 Grilling Loop | `S-HG-5`（候选选择级）；F-N-5 += 选择记录 + 用户原话 |
| `/architecture-audit:ARCHITECTURE_QUESTION_PENDING` | Grilling Loop 中一个架构约束、依赖或 seam 问题已抛出，等待用户回答 | 不继续追问 | — |
| `/architecture-audit:ARCHITECTURE_ANSWER_RECEIVED` | 用户已回答架构问题但尚未复判候选约束、依赖类别或接口风险 | 回 Phase 3 复判 | F-N-5 += 用户回答 |
| `/architecture-audit:DEPENDENCY_CLASSIFICATION_NEEDED` | 候选约束已澄清但依赖类别与 seam 形态未判定 | 进入 Phase 4 | DAG-N-AUDIT-*进 Dependency Classification 子任务 |
| `/architecture-audit:DEPENDENCY_CLASSIFIED` | 候选依赖类别与 seam 形态已判定，接口形态低风险或唯一明显，且推进对象已确认或已授权 AI-DRI | 进入 Phase 6 | F-N-5 += 依赖类别表 + seam 形态；S-HG-1（接口低风险，无 HG-DESIGN-* 触发） |
| `/architecture-audit:INTERFACE_EXPLORATION_NEEDED` | 用户要比较接口方案，或接口高风险、多调用方、跨 ownership seam、存在 ≥2 个可行设计 | 进入 Phase 5 Design It Twice | 预装配 `HG-DESIGN-{slug}-interface` packet（接口 = 设计级硬闸） |
| `/architecture-audit:INTERFACE_DECISION_REQUIRES_USER` | 进入 Phase 5 前已判定接口涉及公共 API、多调用方、ownership seam 或高风险设计；后续方案展示后必须由用户选择 | 进入 Phase 5，但不得 AI-DRI 自动采纳最终接口 | `HG-DESIGN-{slug}-interface` 标记 user-required；不允许 AI-DRI 自决 |
| `/architecture-audit:INTERFACE_OPTIONS_PRESENTED` | 已展示多个接口方案、推荐方案和风险门说明，但尚无用户选择 | 等用户选择 | `S-HG-4 WAITING_GATE_APPROVAL` + `HG-DESIGN-*`；R-INH-2 继承 Gate B；packet F-HG-1~8 必齐 |
| `/architecture-audit:INTERFACE_AUTO_SELECTED_BY_AUTHORIZATION` | 用户明确授权 AI-DRI 采用已展示的推荐接口，且未命中高风险接口条件 | 进入 Phase 6 | `S-HG-5 GATE_APPROVED`（仅当未触发 user-required 条件）；不继承给真实重构 |
| `/architecture-audit:INTERFACE_DECISION_ACCEPTED` | 用户已选择接口方案 | 进入 Phase 6 | `S-HG-5 GATE_APPROVED`；HG-DESIGN-* Approved；F-N-10 Done Evidence += 接口决策 + 用户原话 |
| `/architecture-audit:REFACTOR_SEQUENCE_READY` | 小步重构序列已产出但尚未交接 | 进入 Phase 7 Handoff | 创建 `DAG-N-SPEC-{slug}-refactor-001~###`（重构 Task 候选）；F-N-6 Depends On 反映顺序 |
| `/architecture-audit:SPECS_WRITE_HANDOFF_READY` | 重构序列已作为 `/specs-write` 输入准备好，但尚未成为执行合同 | 报告后停止 | DAG-N-AUDIT-{slug}-arch Done；route input 传递给 `/specs-write`；不继承重构执行授权 |
| `/architecture-audit:USER_DECLINED_CANDIDATES` | 用户拒绝候选且给出 load-bearing 理由 | 建议 ADR 或返回 `/project-steward` | `S-HG-6 GATE_REJECTED` + `FA-HG-2`；建议产 ADR 走 `/grill-with-docs` |
| `/architecture-audit:DOMAIN_CONFLICT` | 术语 / ADR / SSOT 冲突 | 分流 `/grill-with-docs` | `R-AUDIT-3`（`../../specs-write/protocols/entry-decision-tree.md §7.5`） |
| `/architecture-audit:DONE` | 无候选收束、拒绝记录或本 workflow 路由建议已交付；不表示重构、spec 或领域文档已执行 | 报告 `/architecture-audit:DONE` 后返回 `/project-steward` | DAG-N-AUDIT-{slug}-arch Done；F-N-10 += 结论 + Recommended Next Route |

本表 `State` 为本 workflow 的 local suffix；任何报告、handoff 或 route 建议必须输出为 workflow-qualified state，例如 `/architecture-audit:SPECS_WRITE_HANDOFF_READY`。

## 0.2 状态权威与路由动作 (State Authority / Route Action)

- **State Authority**：本表 State 只用于架构审计调度；interface / refactor sequence 只有被 `/specs-write` 编入合同后才成为执行权威。
- **Route Action**：`进入 Phase / 回 Phase` = `CONTINUE_IN_WORKFLOW`；`等用户选择 / 等用户回答` = `WAIT_FOR_USER`；`分流 / 返回 / 退出` = `REPORT_AND_STOP`，除非用户明确要求继续；用户明确说“你来选 / 直接推进推荐方案”时，低风险候选或接口选择 = `CONFIRMED_ACTION`，但只确认本 workflow 内的审计选择，不授权代码重构、spec 写入、领域文档写入或下游 workflow 执行。授权必须点名已展示候选 / 接口或明确采用推荐方案；模糊“看着办”不得授权公共 API、多调用方、ownership seam 或高风险接口。Phase 6 只能在推进对象已确认或已授权后进入。

### 0.2.1 流程合同 (Flow Contract)

唯一主线：Candidate decision → Grilling → Dependency classification → Interface decision → Refactor sequence → `/specs-write` handoff。`/architecture-audit:SPECS_WRITE_HANDOFF_READY` 只是 advisory input；只有被 `/specs-write` 编入 `design.md` / `tasks.md` 后，才可由 `/specs-execute` 执行。`/architecture-audit:DONE` 只关闭本审计循环，不代表任何重构已经落地。

接口决策序列：`/architecture-audit:INTERFACE_EXPLORATION_NEEDED` → Phase 5；若命中公共 API、多调用方、ownership seam 或高风险接口，先标记 `/architecture-audit:INTERFACE_DECISION_REQUIRES_USER` 作为风险门；方案展示后统一进入 `/architecture-audit:INTERFACE_OPTIONS_PRESENTED`；用户选择后进入 `/architecture-audit:INTERFACE_DECISION_ACCEPTED`。低风险且已获明确授权时，才可进入 `/architecture-audit:INTERFACE_AUTO_SELECTED_BY_AUTHORIZATION`。

### 0.2.2 规格编写交接数据 (Specs Write Handoff Payload)

进入 `/architecture-audit:SPECS_WRITE_HANDOFF_READY` 时，必须输出 `/specs-write` 可消费的 advisory payload：Candidate、Dependency Category、Interface Decision、Refactor Sequence、Required spec anchors、必须转成 DSN / INV 的风险、Resolved、Still unresolved、Not authorized、Resume source。缺任一项，只能停留在 `/architecture-audit:REFACTOR_SEQUENCE_READY` 或对应阻塞状态。

## 0.3 中断恢复事实源 (Resume Source)

| 恢复需求 (Resume Need) | 事实源 | 下一步判定 |
| ------------- | -------- | ------------ |
| 候选未确认 | Candidate 列表 + 唯一推荐 | 等用户选择或授权 |
| Grilling 中断 | 最近一个 load-bearing 问题 + 用户回答 | 回 Phase 3 复判 |
| 接口决策未定 | Dependency Category + Interface Options | 等用户选择或低风险授权 |
| 重构序列已出 | Refactor Sequence + Recommended Next Route | 报告 `/architecture-audit:SPECS_WRITE_HANDOFF_READY` |
