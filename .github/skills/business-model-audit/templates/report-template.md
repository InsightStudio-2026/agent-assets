# 商业模式生死审计报告模板 (Business Model Audit Report Template)

> **使用说明**：本文件是 `/business-model-audit` 工作流最终产出报告的标准结构模板。生成的审计报告必须严格遵循以下字段与要求。

---

## 商业模式生死审计报告 (Business Model Audit Report)

## 工作流状态 (Workflow State)

- State: /business-model-audit:`<STATE>`; common examples: /business-model-audit:ROUTE_HANDOFF_READY | /business-model-audit:VALIDATION_PENDING | /business-model-audit:VERDICT_APPROVAL_PENDING | /business-model-audit:REAL_WORLD_VALIDATION_APPROVAL_PENDING

## 证据账本 (Evidence Ledger)

- [请在此填入已确认/未确认的商业 Claim 证据账本]

## 行业原型与非对称差审计 (Archetype Mapping)

- 行业典型原型 (Industry Archetype):
- 行业基准对齐校验 (Industry Manual Validation): [必须注明对 industry-manual.md 中特定定量指标的匹配结果]
- 信息不对称差与能力圈 (Informational Edge & Circle of Competence):
- 企业消失测试与客户依赖度 (Disappearance Test & Client Dependency): [必须包含企业消失测试与刚需/半刚需/可选定位]
- 特定红旗警告 (Specific Red Flags):

## 红队事前尸检 (Red Team Pre-mortem)

- [请在此填入红队事前尸检的 3 大致死原因]

## 商业闭环与单位经济模型 (Commercial Loop & Unit Economics)

- 目标受众 (Audience):
- 付费主体 (Buyer):
- 竞品与替代方案 (Alternatives & Competitors): [列出所有已识别的竞品与替代方案]
- 竞品调查报告链接 (Competitor Research Reports): [对每个竞品，必须提供对应的 `<crt>` 报告链接或嵌入内容；若使用 Gemini Deep Research 提示词，在此列出生成的提示词内容]
- 痛点属性与行业时机 (Pain nature & Timing):
- 付费模型与变现、完税后 LTV 测算 (Monetization & LTV - Post-tax margin):
- 分发渠道与获客成本、人才成本测算 (Distribution & CAC - incl. Talent cost):
- 增量利润转化率与维持性资本开支 (Incremental Profit Conversion & Maintenance CapEx): [必须核算营收增长时的利润转化率，及用于维持业务防守所必须的资本开支占比]
- 首笔付费耗时与能量 ROI (Time-to-First-Dollar - Energy ROI):
- ToB 账期与垫资坏账风险 (ToB Cash Conversion Cycle & Accounts Receivable Risk): [如有 B 端国企/大客户，详述垫资风险与账期危机]
- 关键人才独占与股权激励成本 (Talent Monopoly & Equity Incentive Cost): [核算服务型/人员主导型企业中，抢夺或挽留关键人才的真实成本代价与股东利益侵蚀风险]
- 用户留存与边际架构成本 (Retention & Marginal Architecture Cost):
- 结构性护城河防伪审计 (Moat Defensibility Audit): [必须对照无形资产、转换成本、网络效应、成本优势四大结构性来源进行防伪审查，排除虚假护城河]
- 护城河阻力衰退半衰期 (Moat Decay Half-life - under LLM evolution):

## 公司治理与资本属性审计 (Governance & Capital Audit)

- 股权结构与控制权排雷 (Equity & Control Risk):
- 资本属性错位与退出路径 (Capital Nature & Exit Path):
- 扩张动机与盲目多元化折腾 (Growth Motivation & Diworsification Risk): [评估扩张计划是否因核心业务放缓导致的焦虑性跨界折腾]
- 反身性崩溃与低估值再融资困境 (Reflexivity & Re-financing Threat): [评估对外部资本的依赖度及低估值下的反身性崩溃风险]

## 工程与组织 ROI (Engineering & Org ROI)

- 保留 — 核心20% (Keep):
- 立即砍掉 (Cut):
- 延期执行 (Defer):
- 极致简化 (Simplify):

## 关键设想与假设 (Critical Assumptions)

- CA-001 [CA 详细描述]

## 验证实验与决策计划 (Validation Plan)

- 验证实验 1 (Experiment 1):
- 最低所需证据 (Minimum evidence):
- 实验判定/决策规则 (Decision rule):

## 审计裁定与评分 (Verdict)

- 裁决决策 (Decision): <Kill / Pivot / Validate First / Amputate then Proceed / Proceed to Spec>
- 细分与综合评分 (Score): <1-10>
- 定级依据与理由 (Why):

## 审计结论 (Outcome)

- <Kill | Pivot | Validate first | Amputate then proceed | Proceed to spec | Waiting for approval>

## 权威信息与事实源 (Authority / Fact Source)

- 事实证据账本依据 (Evidence authority): <Evidence Ledger + user evidence + validation results>
- 规格母本依据 (SSOT authority): <approved SSOT path or N/A>
- 用户授权批准依据 (Approval source): <N/A | user approval quote>

## 授权边界 (Authorization Boundary)

- 路由动作 (Route Action): <CONTINUE_IN_WORKFLOW | WAIT_FOR_USER | REPORT_AND_STOP | CONFIRMED_ACTION>
- 授权范围 (Authorized scope): <commercial verdict text / MVP boundary decision / named downstream entry / validation handoff scope>
- 未授权范围 (Not authorized): <SSOT rewrite / feature spec writing / code changes / real-world validation execution / production account action / downstream workflow internal actions>

## 推荐下一步路由 (Recommended Next Route)

- 推荐路由 (Route):
- 准入输入 (Entry input):
- 暂缓执行/不可跨界动作 (Do not do yet):
- 权威事实源依据 (Authority / fact source):
- 本轮已执行动作 (Action taken now): <report only | downstream entry only | validation handoff only>

## 恢复/返航契约 (Return Contract)

- 目标路由 (Target route):
- 已解决商业风险 (Resolved commercial risk):
- 仍受阻 (Still blocked):
- 未授权范围 (Not authorized):
- 恢复事实源 (Resume source):

## 质量门禁 (Gate)

- <N/A 或需用户批准的问题>
