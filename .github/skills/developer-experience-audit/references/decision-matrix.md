---
description: "开发体验审计工作流（/developer-experience-audit）专属的触发判定、状态转换路由、状态权威与动作决策矩阵"
---

# 开发体验审计决策矩阵（/developer-experience-audit）

## 0. 触发判定

| ID | 前置条件 | 动作 | 下一步 | 源 |
| ---- | ---------- | ------ | -------- | ------ |
| R-DEA-ENTRY-1 | 用户显式 `/developer-experience-audit` | 启动审计 | Phase 1 | 本文件 §0 |
| R-DEA-ENTRY-2 | 用户要求验证 quickstart / TTHW / onboarding / 首次跑通体验 | 启动审计 | Phase 1 | 本文件 §0 |
| R-DEA-ENTRY-3 | 用户要求证明新 agent 可完成首个 Medium spec | 启动 spec onboarding 审计 | Phase 3 | `../protocols/onboarding-path-protocol.md` |
| R-DEA-ENTRY-4 | 用户要求验证 canonical examples 是否可复现 | 启动 example 审计 | Phase 4 | `../protocols/canonical-example-protocol.md` |
| R-DEA-ENTRY-5 | 仅是单条命令报错 / 环境安装失败 | 分流 | `/repo-safety-setup` 或 direct diagnose | 本文件 §4 |
| R-DEA-ENTRY-6 | 资产结构 / frontmatter / AGENTS 索引问题 | 分流 | `/asset-quality-gates` | `../../asset-quality-gates/references/checks-catalog.md` |
| R-DEA-ENTRY-7 | 系统状态不清、下一步推进方向不明 | 停止并重定向 | 路由至 `/project-steward` | 临界状态 1 |
| R-DEA-ENTRY-8 | 缺失母本或 L1 SSOT | 停止并重定向 | 路由至 `/project-inception` | 临界状态 2 |
| R-DEA-ENTRY-9 | 属于纯缺陷根因诊断（局部、具体 bug） | 停止并重定向 | 路由至 `diagnose` 技能 | 临界状态 3 |
| R-DEA-ENTRY-10 | 属于新功能、新需求开发、大重构落地 | 停止并重定向 | 路由至 `/specs-write` 与 `/specs-execute` | 临界状态 4 |
| R-DEA-ENTRY-11 | 逻辑简单明确且适合 TDD 验证 | 停止并重定向 | 路由至 `tdd` 技能或直接执行 | 临界状态 5 |

## 0.1 状态与路由汇总 (State / Route Summary)

| 状态 (State) | 判定 | 下一步 | 路由动作 (Route Action) |
| ------- | ------ | -------- | -------------- |
| `/developer-experience-audit:DX_SCOPE_DEFINED` | 已确定审计对象：setup / TTHW / spec onboarding / examples / Windows 命令 | 进入 Phase 2 | `CONTINUE_IN_WORKFLOW` |
| `/developer-experience-audit:DX_SCOPE_MISSING` | 仓库入口、目标 persona 或首个成功 definition 缺失 | 报告缺口 | `REPORT_AND_STOP` |
| `/developer-experience-audit:TTHW_MEASURED` | 已记录从入口到首个可运行结果的时间、命令与失败点 | 进入 Phase 3 | `CONTINUE_IN_WORKFLOW` |
| `/developer-experience-audit:SPEC_ONBOARDING_VERIFIED` | 新上手路径可完成首个 Medium spec | 进入 Phase 4 | `CONTINUE_IN_WORKFLOW` |
| `/developer-experience-audit:CANONICAL_EXAMPLES_VERIFIED` | canonical examples 可定位、可解释、可被 fixture 复检 | 进入 Phase 5 | `CONTINUE_IN_WORKFLOW` |
| `/developer-experience-audit:COLLABORATION_READINESS_VERIFIED` | CI gate、code health、issue risk labels、session recovery、operational learnings、scope guard 可定位并有路由 | 进入 Phase 6 | `CONTINUE_IN_WORKFLOW` |
| `/developer-experience-audit:DX_BLOCKED` | README 命令失真、Windows 命令不可用、密钥边界不清或失败无自救路径 | 输出修订建议并分流 | `REPORT_AND_STOP` |
| `/developer-experience-audit:DX_APPROVED` | TTHW、上手路径、examples、collaboration readiness、失败自救均通过 | 输出 DevEx audit packet | `REPORT_AND_STOP` |

本表 `State` 为 local suffix；报告必须写 workflow-qualified state，例如 `/developer-experience-audit:DX_APPROVED`。

## 0.2 状态权威与路由动作 (State Authority / Route Action)

| 事项 | 事实源 | 规则 |
| ------ | -------- | ------ |
| TTHW 事实 | `../protocols/tthw-protocol.md` 输出表 | 必须记录命令、耗时、失败点、最终成功条件 |
| spec 上手路径 | `../protocols/onboarding-path-protocol.md` | 新上手直接使用 `methodology-kernel + entry-decision-tree + cross-cutting §6` |
| canonical examples | `../protocols/canonical-example-protocol.md` + `../../specs-write/examples/` | 示例是契约测试，不是教程文本 |
| collaboration readiness | `../protocols/collaboration-readiness-protocol.md` | CI / code health / risk labels / session recovery / learnings / scope guard 必须有事实源 or 明确 N/A |
| 资产结构缺陷 | `/asset-quality-gates` | 本 workflow 只报告，不替代结构 gate |

## 0.3 中断恢复事实源 (Resume Source)

| 恢复需求 (Resume Need) | 事实源 | 下一步判定 |
| ------------- | -------- | ------------ |
| 审计范围是否确定 | DevEx audit packet 草稿 §Scope | 缺则回 Phase 1 |
| TTHW 是否测完 | TTHW measurement table | 缺则回 Phase 2 |
| spec onboarding 是否验证 | onboarding path table | 缺则回 Phase 3 |
| examples 是否验证 | canonical examples table | 缺则回 Phase 4 |
| collaboration readiness 是否验证 | collaboration readiness table | 缺则回 Phase 5 |
| 是否已有阻碍 | DX_BLOCKED issue list | 先分流，不输出 DX_APPROVED |

## 1. Companion Documents

| 文档 | 角色 | 何时读 |
| ------ | ------ | -------- |
| `../protocols/tthw-protocol.md` | TTHW、README 命令真实性、环境变量、Windows / PowerShell 兼容审计 | Phase 2 |
| `../protocols/onboarding-path-protocol.md` | 新 agent / 新开发者上手路径与标准事实源验证 | Phase 3 |
| `../protocols/canonical-example-protocol.md` | canonical examples 与 conformance fixtures 的复现验证 | Phase 4 |
| `../protocols/collaboration-readiness-protocol.md` | CI gate、code health、risk labels、session recovery、operational learnings、scope guard awareness | Phase 5 |
