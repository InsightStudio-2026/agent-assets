---
description: "商业模式审计工作流（/business-model-audit）专属的触发判定、状态转换路由、状态权威与动作决策矩阵"
---

# 商业模式审计决策矩阵（/business-model-audit）

## 0. 触发与临界路由决策表

| ID | 前置条件 | 匹配动作 | 下一步/目标路由 | 源 / 备注 |
| ---- | ---------- | ---------- | ----------------- | ----------- |
| R-ROUTE-BMAU-1 | 用户显式 `/business-model-audit` | 启用 workflow | 进入 Phase 1 (Evidence Intake) | 显式入口 |
| R-ROUTE-BMAU-2 | 用户要求对项目进行商业模式审计、APP 计划压力测试或商业生死判断 | 启用 workflow | 进入 Phase 1 (Evidence Intake) | 商业诉求 |
| R-ROUTE-BMAU-3 | 用户向 AI 咨询付费意愿、盈利模型、获客渠道、替代方案及 Pivot/Kill 等问题 | 启用 workflow | 进入 Phase 1 (Evidence Intake) | 商业模型追问 |
| R-ROUTE-BMAU-4 | `/project-steward` 或 `/project-inception` 在前置检查或 Phase 3 发现高商业闭环风险 | 启用 workflow | 进入 Phase 1 (Evidence Intake) | 上游风险引流 |
| R-ROUTE-BMAU-5 | 系统状态不清、下一步推进方向不明 | 停止并重定向 | 路由至 `/project-steward` | 临界状态 1 |
| R-ROUTE-BMAU-6 | 缺失母本或 L1 SSOT | 停止并重定向 | 路由至 `/project-inception` | 临界状态 2 |
| R-ROUTE-BMAU-7 | 属于纯缺陷根因诊断 | 停止并重定向 | 路由至 `diagnose` 技能 | 临界状态 3 |
| R-ROUTE-BMAU-8 | 商业生死风险已审计验证通过，需要具体的新功能开发与 specs 编写 | 停止并重定向 | 路由至 `/specs-write` 与 `/specs-execute` | 临界状态 4 |
| R-ROUTE-BMAU-9 | 逻辑简单明确且适合 TDD 验证 | 停止并重定向 | 路由至 `tdd` 技能或直接执行 | 临界状态 5 |
| R-ROUTE-BMAU-10 | 以上皆不满足且非商业模型审计场景 | 不启用 workflow | 不启用本 workflow | 默认退出 |

## 0.1 主路径

```text
Phase 1 Evidence Intake
  → Phase 2 Red Team Pre-mortem
  → Phase 3 Audience / Alternative / Switching Audit
  → Phase 4 Revenue / Distribution / Moat Audit
  → Phase 5 Engineering ROI & MVP Amputation
  → Phase 6 Critical Assumptions & Validation Plan
  → Phase 7 Verdict & Route
```

## 0.1.1 状态与路由汇总 (State / Route Summary)

| 状态 (State) | 判定 | 下一步 | Gate / DAG ID 映射 |
| ------- | ------ | -------- | --------------------- |
| `/business-model-audit:EVIDENCE_INTAKE` | 证据、用户、替代方案或付费主体仍在收集 | 继续 Phase 1 | 创建 `DAG-N-AUDIT-{slug}-business` 节点（status: Intake） |
| `/business-model-audit:PREMORTEM_DONE` | 商业失败预演已完成，但替代方案 / 切换成本未审清 | 进入 Phase 3 | F-N-5 Outputs += Pre-mortem 证据项 |
| `/business-model-audit:SWITCHING_AUDIT_DONE` | 用户、买方、替代方案与切换成本已审清 | 进入 Phase 4 | F-N-5 += Audience / Alternative / Switching 证据 |
| `/business-model-audit:COMMERCIAL_LOOP_DONE` | 收入、分发、留存、扩张与成本结构已审清 | 进入 Phase 5 | F-N-5 += Commercial Loop 证据 |
| `/business-model-audit:MVP_AMPUTATION_DONE` | 工程 ROI 与 MVP 截肢已完成 | 进入 Phase 6 | F-N-5 += MVP Amputation List |
| `/business-model-audit:VALIDATION_PENDING` | 关键假设未验证，需访谈、concierge、prototype 或付费试点 | 输出验证计划，等待证据回来 | DAG-N-AUDIT-*被 Validation Plan blocked；如需真实动作 → 独立 `HG-IRREV-*` packet |
| `/business-model-audit:VALIDATION_EVIDENCE_RETURNED` | 验证证据已返回但尚未重判 | 回 Phase 1 更新 Evidence Ledger；若证据影响 buyer / alternative / WTP / distribution / ROI，则回对应 Phase 复审，否则进入 Phase 7 | F-N-5 += Validation Evidence |
| `/business-model-audit:READY_FOR_VERDICT` | 证据足以给 Kill / Pivot / Validate / Proceed 裁定 | 进入 Phase 7；无 Gate 命中则报告 `/business-model-audit:ROUTE_HANDOFF_READY` | 裁定预装配 Verdict packet（详 §7.2） |
| `/business-model-audit:VERDICT_APPROVAL_PENDING` | 主裁定、MVP 边界、路线或真实验证动作命中 Gate A/B/C | 等待批准，不路由 | `S-HG-4 WAITING_GATE_APPROVAL` + `HG-STRAT-{slug}-verdict`（Pivot/Amputate 类）或 `HG-IRREV-*`（真实验证类） |
| `/business-model-audit:VERDICT_APPROVED` | 用户已批准主裁定文本、MVP 边界或 Strategy / Critical Design Gate；真实验证动作仍需独立确认 | 产出 `/business-model-audit:ROUTE_HANDOFF_READY` 路线 | `S-HG-5 GATE_APPROVED`；DAG-N-AUDIT-* Done；F-N-10 Done Evidence 填入裁定 + 用户原话 |
| `/business-model-audit:ROUTE_HANDOFF_READY` | 已给唯一主裁定、下游路线和 entry input，但尚未执行下游 workflow 或真实验证动作 | 报告后停止 | DAG-N-AUDIT-{slug}-business Done；route 作为 F-N-5 输出传递给下游 |
| `/business-model-audit:DOWNSTREAM_ENTRY_CONFIRMED` | 用户明确要求继续进入某条下游 workflow 入口，且该入口动作本身无真实外部副作用 | 进入已确认 route 的入口；下游 workflow 必须重新执行自己的 Gate | route input 传递；不继承 HG-*/ DAG-* 授权 |
| `/business-model-audit:REAL_WORLD_VALIDATION_APPROVAL_PENDING` | 真实用户调研、付费试点、外部发布、生产账号或对外承诺尚未获得独立 Gate C 确认 | 等待批准；不得执行真实动作 | `S-HG-4` + `HG-IRREV-{slug}-validation`；TTL-HG-6 单次执行不缓存；失败 → `FA-HG-4` |
| `/business-model-audit:REAL_WORLD_VALIDATION_CONFIRMED` | 真实验证动作、范围、停止条件、记录方式和风险边界均获独立 Gate C 确认 | 只输出验证执行交接并停止；本 workflow 不执行真实动作 | `S-HG-5` + `HG-IRREV-*` Approved；验证执行交接传递给独立执行者 |

## 0.2 状态权威与路由动作 (State Authority / Route Action)

- **State Authority**：本表 State 只用于本 workflow 调度；权威事实源仍是用户证据、验证结果和已批准 SSOT。
- **Route Action**：`继续 / 回 Phase` = `CONTINUE_IN_WORKFLOW`；`等待证据 / 等批准 / VERDICT_APPROVAL_PENDING / REAL_WORLD_VALIDATION_APPROVAL_PENDING` = `WAIT_FOR_USER`；`路由 / 推荐 Route / ROUTE_HANDOFF_READY` = `REPORT_AND_STOP`，除非用户明确要求继续；`/business-model-audit:VERDICT_APPROVED` = `CONFIRMED_ACTION`，但只授权主裁定文本、MVP 边界或 Strategy / Critical Design 决策，必须先生成 `/business-model-audit:ROUTE_HANDOFF_READY`；`/business-model-audit:DOWNSTREAM_ENTRY_CONFIRMED` = `CONFIRMED_ACTION`，但只授权进入已点名的下游 workflow 入口，下游必须重新执行自己的 Gate；`/business-model-audit:REAL_WORLD_VALIDATION_CONFIRMED` = `CONFIRMED_ACTION` for validation handoff scope + `REPORT_AND_STOP` for workflow action：只授权验证执行交接，不授权本 workflow 直接执行真实用户调研、付费试点、外部发布或生产账号动作。

## 0.3 中断恢复事实源 (Resume Source)

| 恢复需求 (Resume Need) | 事实源 | 下一步判定 |
| ------------- | -------- | ------------ |
| 证据未齐 | Evidence Ledger | 继续 Phase 1 或等待证据 |
| 商业闭环未清 | Audience / Alternative / Revenue 输出 | 回对应审计 Phase |
| MVP 边界未定 | MVP Amputation List | 等 Strategy / Critical Design 决策 |
| 验证未完成 | Critical Assumptions + Validation Plan | 等验证证据返回 |
| 真实验证动作待批 | Validation Plan + Gate C 风险边界 | 等批准或改为只报告计划 |
| 裁定已出 | Verdict + Recommended Next Route | 报告 `/business-model-audit:ROUTE_HANDOFF_READY`，不自动执行下游 |

## 0.4 审计纪律

1. **证据分层**：所有判断必须标为 `Observed` / `User-claimed` / `Inferred` / `Unknown`。
2. **不伪造市场事实**：没有外部资料或用户证据时，只能写待验证假设。
3. **替代方案优先**：先问用户为什么不用 Excel、Notion、ChatGPT、成熟竞品、人工服务或外包。
4. **付费主体优先于功能清单**：不知道谁付钱、为什么现在付钱，不允许推荐进入 `/specs-write`。
5. **工程服务商业**：技术复杂度必须能解释为获客、留存、转化、成本下降、信任或差异化；否则默认砍掉。
6. **Kill 是有效产出**：判定放弃不是失败；避免继续烧工程资源就是交付价值。
7. **SSOT 修改需批准**：发现母本需要修订时，只给修订建议和路线，不静默改 Authoritative SSOT。
