---
description: "安全隐私审计工作流（/security-privacy-audit）专属的触发判定、状态转换路由、状态权威与动作决策矩阵"
---

# 安全隐私审计决策矩阵（/security-privacy-audit）

## 0. 触发与临界路由决策表

| ID | 前置条件 | 匹配动作 | 下一步/目标路由 | 源 / 备注 |
| ---- | ---------- | ---------- | ----------------- | ----------- |
| R-ROUTE-SPA-1 | 用户显式 `/security-privacy-audit` | 启用 workflow | 进入 Phase 1 (Intake) | 显式入口 |
| R-ROUTE-SPA-2 | 涉及 `authn` / `authz` / `OAuth` / `MFA` 或用户账号及凭据恢复机制变更 | 启用 workflow | 进入 Phase 1 (Intake) | 身份与鉴权门 |
| R-ROUTE-SPA-3 | 涉及 `PII` (个人身份信息) 采集、存储、对外展示、数据导出或生命周期保留变更 | 启用 workflow | 进入 Phase 1 (Intake) | 隐私保护门 |
| R-ROUTE-SPA-4 | 涉及 `secrets`、密钥、加密证书、API token、生产环境变量等的改动 | 启用 workflow | 进入 Phase 1 (Intake) | 凭证泄露防护 |
| R-ROUTE-SPA-5 | 涉及外部攻击面，包括新增公开 API endpoint、webhook、未授权 file upload、或 admin 管理路由 | 启用 workflow | 进入 Phase 1 (Intake) | 外部边界防护 |
| R-ROUTE-SPA-6 | 涉及支付、收费、邀请邀请码、或高价值/敏感的易滥用核心路径 | 启用 workflow | 进入 Phase 1 (Intake) | 业务风控门 |
| R-ROUTE-SPA-7 | 涉及 `CI/CD secrets`、GitHub Actions、或仓库级 agent 供应链安全审计 | 启用 workflow | 进入 Phase 1 (Intake) | 基础设施供应链 |
| R-ROUTE-SPA-8 | `/release-deploy` 报告 `R-RDY-5` 安全门未通过且缺少事实源证明 | 启用 workflow | 进入 Phase 1 (Intake) | 发布就绪联动 |
| R-ROUTE-SPA-9 | 纯内部代码重构，无任何安全边界、权限模型或数据流变化的局部常规实现 | 停止并忽略 | 不启用本 workflow | 安全无感变更 |
| R-ROUTE-SPA-10 | 系统状态不清、下一步推进方向不明 | 停止并重定向 | 路由至 `/project-steward` | 临界状态 1 |
| R-ROUTE-SPA-11 | 缺失母本或 L1 SSOT | 停止并重定向 | 路由至 `/project-inception` | 临界状态 2 |
| R-ROUTE-SPA-12 | 属于纯缺陷根因诊断（局部、具体 bug） | 停止并重定向 | 路由至 `diagnose` 技能 | 临界状态 3 |
| R-ROUTE-SPA-13 | 属于新功能、新需求开发、大重构落地 | 停止并重定向 | 路由至 `/specs-write` 与 `/specs-execute` | 临界状态 4 |
| R-ROUTE-SPA-14 | 逻辑简单明确且适合 TDD 验证 | 停止并重定向 | 路由至 `tdd` 技能或直接执行 | 临界状态 5 |

## 0.1 状态与路由汇总 (State / Route Summary)

| 状态 (State) | 判定 | 下一步 | Gate / DAG ID 映射 |
| ------- | ------ | -------- | --------------------- |
| `/security-privacy-audit:SECURITY_SCOPE_MISSING` | 触发但范围 / 资产 / 数据流 / 权限模型未定义 | 与用户对齐范围 + 资产清单 | `S-HG-3 GATE_PACKET_INCOMPLETE`（packet 装配缺前置） |
| `/security-privacy-audit:ASSET_INVENTORY_READY` | attack surface census 完成（endpoint / auth boundary / admin / webhook / job / queue / WS / upload） | 进入 Phase 3 威胁建模 | 创建 `DAG-N-AUDIT-{slug}-security`（status: Asset-Inventoried） |
| `/security-privacy-audit:THREAT_MODEL_DRAFTED` | STRIDE / kill-chain / 滥用场景威胁建模草拟 | 进入 Phase 4 authz / privacy 矩阵 | `HG-STRAT-{slug}-threat-model`（威胁建模 = 战略级，需用户裁决） |
| `/security-privacy-audit:AUTHZ_MATRIX_DRAFTED` | 资源 × 操作 × 角色 / 租户隔离矩阵草拟 | 进入 Phase 5 PII flow | DAG-N-AUDIT-*F-N-5 += authz matrix |
| `/security-privacy-audit:PRIVACY_FLOW_DRAFTED` | PII source / storage / sink / retention / 删除路径草拟 | 进入 Phase 6 secrets / dep / 滥用 | DAG-N-AUDIT-* F-N-5 += privacy flow |
| `/security-privacy-audit:SECRET_HANDLING_BLOCKED` | secrets 硬编码 / 进日志 / 进前端 bundle / 进 git 历史 / unpinned CI/CD action 检出 | 修复 + 撤销暴露密钥 → 重审；不进入 SECURITY_APPROVED | `S-HG-9 GATE_FAILED` + `FA-HG-2`（密钥泄露 = Critical） |
| `/security-privacy-audit:VULNERABILITY_FOUND` | 高 / 中 / 低风险漏洞 / 依赖 CVE / 滥用场景命中 | 按严重性 → MITIGATION_REQUIRED 或 WAITING_RISK_ACCEPTANCE | DAG-N-AUDIT-* F-N-5 += vulnerability list；高危 → `S-HG-9` 阻塞 |
| `/security-privacy-audit:MITIGATION_REQUIRED` | 高 / 中危发现需 mitigation task；不允许风险接受 | 创建 `/specs-write` mitigation task → 路由到 `/specs-execute` 修复 | `S-HG-3 GATE_PACKET_INCOMPLETE`（待 mitigation 完成） |
| `/security-privacy-audit:WAITING_RISK_ACCEPTANCE` | 低危或 mitigation 成本不合理；用户原话裁决可接受 | 等用户原话 + 写入 risk-acceptance 记录 | `S-HG-4 WAITING_GATE_APPROVAL` + `HG-SEC-{slug}-{scope}` packet（F-HG-3 必含原话） |
| `/security-privacy-audit:PROD_AUTH_CHANGE_PENDING_APPROVAL` | 权限模型 / 认证流程 / 密钥 / 证书 / token / 生产权限变更命中 Hard-gate | 等用户批准；packet F-HG-1~8 全齐 | `S-HG-4` + `HG-IRREV-004` + `HG-SEC-*`；R-INH-3 不继承 spec 批准 |
| `/security-privacy-audit:SECURITY_APPROVED` | 所有高 / 中危已 mitigation 或显式风险接受；Hard-gate 已批；security gate packet 完整 | 输出 security-gate-packet.md → `/release-deploy` R-RDY-5 | `S-HG-8 GATE_PASSED`；DAG-N-AUDIT-{slug}-security Done |
| `/security-privacy-audit:SECURITY_BLOCKED` | 高危未修 / Hard-gate 未批 / mitigation 不可行 | 阻塞 release；分流 `/specs-write` 或 `/architecture-audit` 或 `/bug-audit` | `S-HG-9 GATE_FAILED` + `FA-HG-2`；阻塞 `/release-deploy` |
| `/security-privacy-audit:POST_AUDIT_REGRESSION_DETECTED` | 审计后代码变更引入新攻击面 / 新 PII / 新 secrets | 重跑 Phase 2-6 增量审计；不沿用旧 packet | DAG-N-AUDIT-{slug}-security 重置；`HG-SEC-*` 重新装配 |

## 0.2 状态权威与路由动作 (State Authority / Route Action)

- **State Authority**：threat-model.md / authz-matrix.md / privacy-flow.md / secret-handling-report.md / dependency-risk-report.md / security-regression-checklist.md / security-gate-packet.md 是权威事实源；本表 State 只用于审计调度。
- **Route Action**：`进入 Phase / 修复 + 撤销暴露密钥 + 重审` = `CONTINUE_IN_WORKFLOW`；`等用户裁决威胁模型 / 风险接受 / Hard-gate 批准` = `WAIT_FOR_USER`；`分流 / 报告并停止 / SECURITY_BLOCKED` = `REPORT_AND_STOP`，除非用户明确要求继续；`/security-privacy-audit:SECURITY_APPROVED` 与 `/security-privacy-audit:WAITING_RISK_ACCEPTANCE` 用户裁决 = `CONFIRMED_ACTION`，但只授权本次 packet 范围内的风险接受 / Hard-gate；不继承到下次审计、其他 release、其他外部副作用。

## 0.3 Hard-gate 命中条件（自动升级到 HG-IRREV-004）与 Resume Source

| 条件 | 命中 Gate |
| ------ | ---------- |
| 权限模型变更（角色定义 / 资源粒度 / 租户隔离边界） | `HG-IRREV-004` + `HG-SEC-{slug}-authz` |
| 认证流程变更（登录 / 会话 / refresh token / OAuth / MFA / 账号恢复） | `HG-IRREV-004` + `HG-SEC-{slug}-authn` |
| 密钥 / 证书 / token 操作（轮换 / 撤销 / 新建 / 跨环境复用） | `HG-IRREV-004` + `HG-SEC-{slug}-secrets` |
| PII 流向变化（采集 / 存储 / 展示 / 导出 / 删除 / 保留期变更） | `HG-IRREV-004` + `HG-SEC-{slug}-privacy` |
| 生产权限修改（DB role / cloud IAM / admin endpoint 暴露） | `HG-IRREV-004` + `HG-SEC-{slug}-prod-authz` |
| Agent supply chain（新 MCP / tool / external skill 引入） | `HG-SEC-{slug}-agent-supply`（同时启 `/asset-quality-gates` external intake） |
| Public webhook / unauthenticated endpoint 新增 | `HG-SEC-{slug}-attack-surface`；高风险 → 升级 `HG-IRREV-004` |

## 0.4 中断恢复事实源 (Resume Source)

| 恢复需求 (Resume Need) | 事实源 | 下一步判定 |
| ------------- | -------- | ------------ |
| 审计是否已立项 | `docs/specs/<slug>/security/` 或 `<slug>/audit-charter.md` | 缺则 `/security-privacy-audit:SECURITY_SCOPE_MISSING` |
| Asset Inventory 是否完成 | `<slug>/asset-inventory.md` | 缺则回 Phase 2 |
| Threat Model 是否草拟 | `<slug>/threat-model.md` | 缺则回 Phase 3 |
| Authz / Privacy / Secrets 矩阵状态 | `<slug>/authz-matrix.md` / `privacy-flow.md` / `secret-handling-report.md` | 任一缺则按对应 Phase 续跑 |
| 漏洞清单 | `<slug>/vulnerability-list.md` | 决定 MITIGATION_REQUIRED / WAITING_RISK_ACCEPTANCE |
| Risk Acceptance 用户原话 | 同一轮用户原话 + F-HG-3 引用 | 缺则保持 `/security-privacy-audit:WAITING_RISK_ACCEPTANCE` |
