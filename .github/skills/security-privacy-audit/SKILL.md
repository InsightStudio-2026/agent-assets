---
name: security-privacy-audit
description: 安全隐私审计：集中治理威胁建模、权限、隐私、密钥、依赖供应链与滥用场景；产出 security gate packet，阻塞高风险 release，权限 / PII / 密钥 / 生产权限变更必须用户批准。
argument-hint: "要审计哪个系统的安全与隐私？"
disable-model-invocation: true
---


# /security-privacy-audit · 安全隐私审计

**定位**：把 authn / authz / PII / secrets / 依赖供应链 / 攻击面 / 滥用场景的审计串成可追溯证据链；产出 security gate packet，作为 `/release-deploy` `R-RDY-5 Security Gate` 的事实源。

**边界**：只做安全 / 隐私 / 权限 / 依赖审计；不替代 `/specs-execute` 实现验证、不替代 `/data-migration-safety` 数据闸口、不替代 `/release-deploy` 发布动作、不替代法律合规审查；漏洞修复本身归 `/specs-execute` 或 `/bug-audit`，本 workflow 只识别 + 出 mitigation task。

**斜杠命令**：`/security-privacy-audit`

**配对前置 / 下游**：上游消费 spec design / data flow / 权限模型 / 依赖清单；下游产出 security gate packet 给 `/release-deploy`、`/specs-write` / `/specs-execute` mitigation task、`/bug-audit` 漏洞处置、`/architecture-audit` 安全边界修订。

---

## 懒加载契约

- **MUST read**: `./decision-matrix.md`
- 开始判定或执行 Phase 流程前，必须完整懒加载上述细节。

---

## 1. 伴随文档

| 文档 | 角色 | 何时读 |
| ------ | ------ | -------- |
| `references/security-checks-catalog.md` | 最低检查面 + 基础设施安全面 + 滥用场景规则字典（R-SEC-*） | Phase 2-6 |
| `protocols/authz-privacy-protocol.md` | authz matrix 模板 + PII flow 字段 + secrets handling 规范（R-AZP-*） | Phase 4-5 |
| `../specs-write/protocols/gate-dag-protocol.md` | Gate / DAG ID 横切协议事实源 | State 表 + Phase 7 装配 packet |
| `../specs-write/protocols/entry-decision-tree.md §7.6` | R-RETURN-* 路由 | mitigation 回切 |

---

## 2. 阶段骨架（细节见伴随文档）

每个 Phase 入口的 **MUST read**指令是硬规则——不读 = 视为违反该 Phase 的安全与隐私防御。

### 阶段 1 — 审计范围与敏感资产清单**MUST read**`references/security-checks-catalog.md`

对齐审计范围；按 `security-checks-catalog.md §基础设施安全面` 收集 attack surface census；输出 `asset-inventory.md`。

### 阶段 2 — 威胁建模评估**MUST read**`references/security-checks-catalog.md`

按 STRIDE / kill-chain / 滥用场景对每个 asset 做威胁建模；输出 `threat-model.md`；威胁模型 = 战略级，最终发布前需用户裁决。

### 阶段 3 — 权限与授权矩阵核查**MUST read**`protocols/authz-privacy-protocol.md`

按 `authz-privacy-protocol.md` 生成 resource × action × role / tenant matrix；输出 `authz-matrix.md`。

### 阶段 4 — PII 敏感数据流审计**MUST read**`protocols/authz-privacy-protocol.md`

按 `authz-privacy-protocol.md §PII` 字段生成 source / storage / sink / retention / 删除路径；输出 `privacy-flow.md`。

### 阶段 5 — 密钥、供应链与滥用扫描**MUST read**`references/security-checks-catalog.md`

按 `security-checks-catalog.md §最低检查面 + 滥用场景` 跑 secret scan / 依赖 CVE / unpinned CI / agent supply chain / 滥用场景；输出 `secret-handling-report.md` + `dependency-risk-report.md`。

### 阶段 6 — 漏洞分流评估**MUST read**`references/security-checks-catalog.md`

对所有发现按严重性（Critical / High / Medium / Low）分类；决定 MITIGATION_REQUIRED / WAITING_RISK_ACCEPTANCE / SECURITY_BLOCKED；输出 `vulnerability-list.md` + `security-regression-checklist.md`。

### 阶段 7 — 关卡文档装配与批准**MUST read** `../specs-write/protocols/gate-dag-protocol.md`

装配 `HG-SEC-*` packet（F-HG-1~8 齐）+ 命中 Hard-gate 时升级 `HG-IRREV-004`；展示给用户 → `/security-privacy-audit:WAITING_RISK_ACCEPTANCE` / `/security-privacy-audit:PROD_AUTH_CHANGE_PENDING_APPROVAL`；用户原话批准后 → `/security-privacy-audit:SECURITY_APPROVED` 输出 `security-gate-packet.md`。

### 阶段 8 — 完工收口与接续路由

将 packet 交给 `/release-deploy` R-RDY-5；mitigation task 交给 `/specs-write` / `/specs-execute`；记录 audit cycle 到 DAG-N-AUDIT-{slug}-security Done。

---

## 3. 输出格式

```markdown
## 安全与隐私审计报告 (Security & Privacy Audit Report)

## 工作流状态 (Workflow State)

- State: /security-privacy-audit:`<state>`

## 审计范围 (Audit Scope)

- Feature slug + version + 系统范围:
- 资产清单 (Asset Inventory): <文件路径>

## 门禁/节点状态 (Gate / DAG Status)

- HG-SEC-{slug}-{scope}: <S-HG-* 状态>
- HG-IRREV-004 命中: <列出激活子项 或 N/A>
- HG-STRAT-{slug}-threat-model: <S-HG-* 状态>
- DAG-N-AUDIT-{slug}-security: <node 状态>

## 审计发现摘要 (Findings Summary)

- 威胁模型 (Threat Model): <已草拟 / 已裁决 / 缺项>
- 权限矩阵 (Authz Matrix): <资源 × 操作 × 角色 完整 / 缺项>
- 隐私流动路径 (Privacy Flow): <PII source/storage/sink/retention 完整 / 缺项>
- 凭证/密钥处理 (Secrets Handling): <PASS / SECRET_HANDLING_BLOCKED + 列项>
- 依赖项风险 (Dependency Risk): <CVE / 滥用场景 命中清单>
- 潜在滥用场景 (Abuse Scenarios): <撞库 / 刷接口 / 越权爬取 / 付费绕过 / 邀请滥用 命中>

## 漏洞清单 (Vulnerability List)

- 致命 (Critical): <列出 + 影响面 + mitigation 状态>
- 高危 (High): <...>
- 中危 (Medium): <...>
- 低危 (Low): <...>

## 缓解/削减计划 (Mitigation Plan)

- 待修补任务 (Required Tasks): <列出待 /specs-execute 修复项>
- 已签署的风险接受承诺 (Risk Acceptance Recorded): <用户原话引用 + 范围限定>

## 授权边界 (Authorization Boundary)

- 路由动作 (Route Action): <CONTINUE_IN_WORKFLOW | WAIT_FOR_USER | CONFIRMED_ACTION | REPORT_AND_STOP>
- 授权来源 (Confirmation source): <用户原话 或 N/A>
- 授权范围 (Authorized scope): <本次 packet 范围内 risk acceptance / Hard-gate 批准>
- 未授权范围 (Not authorized): <下次审计 / 其他 release / 其他外部副作用 / 下游 workflow>

## 推荐下一步路由 (Recommended Next Route)

- <continue Phase | /specs-write mitigation | /specs-execute fix | /bug-audit | /architecture-audit | /release-deploy R-RDY-5 handoff>

## 恢复/返航契约 (Return Contract)

- 目标路由 (Target route):
- 准入输入 (Entry input):
- 未决漏洞/开放信息包字段 (Outstanding vulnerabilities / open packet fields):

```

---

## 4. 禁用行为

- 不在 `/security-privacy-audit:SECRET_HANDLING_BLOCKED` / `/security-privacy-audit:SECURITY_BLOCKED` / 高危未修 / Hard-gate 未批时输出 `/security-privacy-audit:SECURITY_APPROVED`。
- 不把 `/security-privacy-audit:WAITING_RISK_ACCEPTANCE` 用户裁决继承到下次审计 / 其他 release / 其他范围；每次新风险都需新批准。
- 不替代 `/specs-execute` 修漏洞；本 workflow 只识别 + 出 mitigation task；修复完成后必须重跑 Phase 2-6 增量审计。
- 不把 secret scan 结果当作"无 secrets"证明；漏检率不为零，需配合 secrets archaeology 全量历史扫描。
- 不在 `/security-privacy-audit:WAITING_RISK_ACCEPTANCE` 状态下放过权限模型 / 认证流程 / 密钥 / PII / 生产权限变更；这五类强制 Hard-gate（`HG-IRREV-004`），不允许 risk acceptance 替代用户批准。
- 不修代码 / spec / standards；只读消费它们；如发现需求 / 实现 / 架构缺陷 → 按 `R-RETURN-*` 回切。
- 不把 audit 后的代码变更视为"已审计"；引入新攻击面 / 新 PII / 新 secrets → `/security-privacy-audit:POST_AUDIT_REGRESSION_DETECTED` + 重跑增量。
- 不替代法律合规审查；license 风险归专项依赖审计 + 法务确认；本 workflow 只标注未确认 license。

## 5. 快速自检清单

报告前自检：

- [ ] 是否已明确对齐了本次安全审计的系统与功能边界？
- [ ] 威胁建模（STRIDE等）是否已完成草拟并提请用户裁决？
- [ ] 资源权限矩阵与 PII 隐私流动路径是否已被完整绘制并存入对应 md？
- [ ] 密钥扫描、依赖 CVE 漏洞及供应链安全扫描是否均无 Critical/High 未决项？
- [ ] 发现的所有漏洞是否均已建立 mitigation 修复任务或由用户明确签署了 Risk Acceptance？
- [ ] 涉权限/PII/密钥/生产权限变更的 Hard-gate（HG-IRREV-004），是否获得了用户明确批准？

## 支撑资源

- [authz-privacy-protocol.md](./protocols/authz-privacy-protocol.md)
- [decision-matrix.md](./references/decision-matrix.md)
- [security-checks-catalog.md](./references/security-checks-catalog.md)
