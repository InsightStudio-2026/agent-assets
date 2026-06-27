---
description: "CI 质量门工作流（/ci-quality-gates）专属的触发判定、状态转换路由、状态权威与动作决策矩阵"
---

# CI 质量门决策矩阵（/ci-quality-gates）

## 0. 触发判定

| ID | 前置条件 | 动作 | 下一步 | 源 |
| ---- | ---------- | ------ | -------- | ------ |
| R-CIQ-ENTRY-1 | 用户显式 `/ci-quality-gates` | 启动 CI 门禁审计 | Phase 1 | 本文件 §0 |
| R-CIQ-ENTRY-2 | `/code-health-dashboard` 报 CI gate missing | 启动 CI 设计 | Phase 1 | `../../code-health-dashboard/references/metrics-catalog.md` |
| R-CIQ-ENTRY-3 | release / PR 需要 required checks | 审计 CI 与 branch protection | Phase 1 | `/release-deploy` |
| R-CIQ-ENTRY-4 | CI 红灯、flaky、artifact 缺失、coverage gate 缺失 | 审计失败分类 | Phase 2 | 本文件 §1 |
| R-CIQ-ENTRY-5 | 只是单次本地命令失败 | 不启用 | `/specs-execute` / `diagnose` | 本文件 §4 |
| R-CIQ-ENTRY-6 | 系统状态不清、下一步推进方向不明 | 停止并重定向 | 路由至 `/project-steward` | 临界状态 1 |
| R-CIQ-ENTRY-7 | 缺失母本或 L1 SSOT | 停止并重定向 | 路由至 `/project-inception` | 临界状态 2 |
| R-CIQ-ENTRY-8 | 属于纯缺陷根因诊断（局部、具体 bug） | 停止并重定向 | 路由至 `diagnose` 技能 | 临界状态 3 |
| R-CIQ-ENTRY-9 | 属于新功能、新需求开发、大重构落地 | 停止并重定向 | 路由至 `/specs-write` 与 `/specs-execute` | 临界状态 4 |
| R-CIQ-ENTRY-10 | 逻辑简单明确且适合 TDD 验证 | 停止并重定向 | 路由至 `tdd` 技能或直接执行 | 临界状态 5 |

## 0.1 状态与路由汇总 (State / Route Summary)

| 状态 (State) | 判定 | 下一步 | 路由动作 (Route Action) |
| ------- | ------ | -------- | -------------- |
| `/ci-quality-gates:CI_SCOPE_DEFINED` | CI provider、目标分支、质量命令、保护目标已识别 | Phase 2 | `CONTINUE_IN_WORKFLOW` |
| `/ci-quality-gates:CI_PROVIDER_MISSING` | 无 CI provider 或配置事实源 | 输出建议或分流 `/repo-safety-setup` | `REPORT_AND_STOP` |
| `/ci-quality-gates:QUALITY_GATE_DRAFTED` | required jobs、命令、artifact、失败分类已草拟 | Phase 3 | `CONTINUE_IN_WORKFLOW` |
| `/ci-quality-gates:WAITING_CI_CHANGE_APPROVAL` | 写 CI config / branch protection / secrets / runner 设置需批准 | 等用户批准 | `WAIT_FOR_USER` |
| `/ci-quality-gates:CI_GATE_READY` | CI 门禁配置与验证证据齐 | 输出 report | `REPORT_AND_STOP` |
| `/ci-quality-gates:CI_GATE_BLOCKED` | CI 配置、权限、runner、secrets 或 flaky 风险阻塞 | 输出 route | `REPORT_AND_STOP` |
| `/ci-quality-gates:CI_SECURITY_RISK_FOUND` | pull_request_target、untrusted input、secrets 暴露等风险 | 分流 `/security-privacy-audit` | `REPORT_AND_STOP` |

## 0.2 状态权威与路由动作 (State Authority / Route Action)

| 事项 | 权威事实源 | 路由动作 (Route Action) |
| ------ | ------------ | -------------- |
| CI provider | `.github/workflows/` / provider config / docs | `CONTINUE_IN_WORKFLOW` |
| 本地命令对齐 | package scripts / Makefile / Verification Commands | `CONTINUE_IN_WORKFLOW` |
| branch protection | GitHub / provider settings 或用户确认 | `WAIT_FOR_USER` |
| secrets / runners | provider settings / security audit | `/security-privacy-audit` if risky |

## 1. 伴生文档 (Companion Documents)

| 文档 | 角色 | 何时读 |
| ------ | ------ | -------- |
| `../protocols/ci-provider-protocol.md` | provider 探测、workflow inventory、required checks 映射 | Phase 1 |
| `quality-gates-catalog.md` | lint / typecheck / test / coverage / security / dependency / license / bundle / migration gates | Phase 2 |
| `../protocols/flaky-artifact-protocol.md` | artifact 上传、失败分类、flaky 隔离、rerun 规则 | Phase 2 / 3 |
| `../templates/ci-gate-report-template.md` | CI gate report 与 branch protection 建议模板 | Phase 3 |
