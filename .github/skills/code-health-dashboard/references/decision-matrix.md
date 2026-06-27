---
description: "代码健康仪表盘工作流（/code-health-dashboard）专属的触发判定、状态转换路由、状态权威与动作决策矩阵"
---

# 代码健康仪表盘决策矩阵（/code-health-dashboard）

## 0. 触发判定

| ID | 前置条件 | 动作 | 下一步 | 源 |
| ---- | ---------- | ------ | -------- | ------ |
| R-CHD-ENTRY-1 | 用户显式 `/code-health-dashboard` | 启动健康采集 | Phase 1 | 本文件 §0 |
| R-CHD-ENTRY-2 | release 前需要质量总览 / trend / maturity evidence | 采集 dashboard | Phase 1 | `/release-deploy` |
| R-CHD-ENTRY-3 | 多次失败测试、flaky、coverage 下滑、依赖风险分散 | 采集趋势并路由 | Phase 2 | 本文件 §1 |
| R-CHD-ENTRY-4 | 需要配置 hooks / CI / quality gates | 不在本 workflow 实施，分流 | `/repo-safety-setup` 或 `/ci-quality-gates` | 本文件 §4 |
| R-CHD-ENTRY-5 | 单个 bug 根因诊断 | 不启用 | `diagnose` / `/bug-audit` | 本文件 §4 |
| R-CHD-ENTRY-6 | 系统状态不清、下一步推进方向不明 | 停止并重定向 | 路由至 `/project-steward` | 临界状态 1 |
| R-CHD-ENTRY-7 | 缺失母本或 L1 SSOT | 停止并重定向 | 路由至 `/project-inception` | 临界状态 2 |
| R-CHD-ENTRY-8 | 属于纯缺陷根因诊断（局部、具体 bug） | 停止并重定向 | 路由至 `diagnose` 技能 | 临界状态 3 |
| R-CHD-ENTRY-9 | 属于新功能、新需求开发、大重构落地 | 停止并重定向 | 路由至 `/specs-write` 与 `/specs-execute` | 临界状态 4 |
| R-CHD-ENTRY-10 | 逻辑简单明确且适合 TDD 验证 | 停止并重定向 | 路由至 `tdd` 技能或直接执行 | 临界状态 5 |

## 0.1 状态与路由汇总 (State / Route Summary)

| 状态 (State) | 判定 | 下一步 | 路由动作 (Route Action) |
| ------- | ------ | -------- | -------------- |
| `/code-health-dashboard:HEALTH_SCOPE_DEFINED` | 仓库、命令、指标、时间窗口已识别 | Phase 2 | `CONTINUE_IN_WORKFLOW` |
| `/code-health-dashboard:COMMAND_SURFACE_MISSING` | package scripts / test / typecheck / lint 入口缺失 | 分流 `/repo-safety-setup` | `REPORT_AND_STOP` |
| `/code-health-dashboard:HEALTH_EVIDENCE_COLLECTED` | 质量命令与 artifacts 已采集 | Phase 3 | `CONTINUE_IN_WORKFLOW` |
| `/code-health-dashboard:QUALITY_REGRESSION_FOUND` | lint/typecheck/test/coverage/complexity 任一退化 | 输出 route | `/specs-execute` / `/bug-audit` |
| `/code-health-dashboard:TREND_BASELINE_MISSING` | 无历史或 baseline，不可判趋势 | 建立 baseline packet | `CONTINUE_IN_WORKFLOW` |
| `/code-health-dashboard:DASHBOARD_READY` | health dashboard 可消费 | 输出报告 | `REPORT_AND_STOP` |
| `/code-health-dashboard:HEALTH_BLOCKED_ENVIRONMENT` | 工具缺失 / 权限 / 环境导致不可采集 | 报告阻塞 | `WAIT_FOR_USER` |

## 0.2 状态权威与路由动作 (State Authority / Route Action)

| 事项 | 权威事实源 | 路由动作 (Route Action) |
| ------ | ------------ | -------------- |
| 命令存在性 | package scripts / Makefile / CI config / docs | `CONTINUE_IN_WORKFLOW` |
| 命令结果 | 实际命令输出或已保留 artifact | `CONTINUE_IN_WORKFLOW` |
| 趋势 | previous dashboard / CI history / release artifacts | `CONTINUE_IN_WORKFLOW` |
| 缺基础设施 | `/repo-safety-setup` / `/ci-quality-gates` | `REPORT_AND_STOP` |

## 1. 伴生文档 (Companion Documents)

| 文档 | 角色 | 何时读 |
| ------ | ------ | -------- |
| `metrics-catalog.md` | health 指标、红绿判定、路由 | Phase 1 / 2 |
| `../protocols/collection-protocol.md` | 命令发现、证据采集、环境失败分类 | Phase 2 |
| `../templates/dashboard-template.md` | dashboard / trend / route 输出模板 | Phase 3 |
