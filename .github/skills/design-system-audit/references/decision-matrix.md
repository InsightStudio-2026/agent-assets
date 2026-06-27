---
description: "设计系统与 UX 审计工作流（/design-system-audit）专属的触发判定、状态转换路由、状态权威与动作决策矩阵"
---

# 设计系统与 UX 审计决策矩阵（/design-system-audit）

## 0. 触发判定

| ID | 前置条件 | 动作 | 下一步 | 源 |
| ---- | ---------- | ------ | -------- | ------ |
| R-DSA-ENTRY-1 | 用户显式 `/design-system-audit` | 启动审计 | Phase 1 | 本文件 §0 |
| R-DSA-ENTRY-2 | `NFR-UX-*` Active 或 DSN-UI-* 新增关键 UI 模式 | 启动 UX/A11y 审计 | Phase 1 | `../../specs-write/templates/requirements.md §10.5` |
| R-DSA-ENTRY-3 | 组件系统漂移、tokens 不一致、响应式缺口、A11y 风险 | 启动系统审计 | Phase 2 | 本文件 §1 |
| R-DSA-ENTRY-4 | UI 看起来模板化、AI 味、信息架构空洞、文案泛化 | 启动 Anti-AI Taste Gate | Phase 4 | `../protocols/anti-ai-taste-gate.md` |
| R-DSA-ENTRY-5 | 纯后端 / CLI / 无用户界面 | 不启用 | direct | 本文件 §4 |
| R-DSA-ENTRY-6 | 系统状态不清、下一步推进方向不明 | 停止并重定向 | 路由至 `/project-steward` | 临界状态 1 |
| R-DSA-ENTRY-7 | 缺失母本或 L1 SSOT | 停止并重定向 | 路由至 `/project-inception` | 临界状态 2 |
| R-DSA-ENTRY-8 | 属于纯缺陷根因诊断（局部、具体 bug） | 停止并重定向 | 路由至 `diagnose` 技能 | 临界状态 3 |
| R-DSA-ENTRY-9 | 属于新功能、新需求开发、大重构落地 | 停止并重定向 | 路由至 `/specs-write` 与 `/specs-execute` | 临界状态 4 |
| R-DSA-ENTRY-10 | 逻辑简单明确且适合 TDD 验证 | 停止并重定向 | 路由至 `tdd` 技能或直接执行 | 临界状态 5 |

## 0.1 状态与路由汇总 (State / Route Summary)

| 状态 (State) | 判定 | 下一步 | 路由动作 (Route Action) |
| ------- | ------ | -------- | -------------- |
| `/design-system-audit:DESIGN_SOURCE_MISSING` | 缺设计源、截图、组件清单或关键路径 | 报告缺口 | `REPORT_AND_STOP` |
| `/design-system-audit:COMPONENT_INVENTORY_READY` | 组件、tokens、状态面清单已完成 | Phase 2 | `CONTINUE_IN_WORKFLOW` |
| `/design-system-audit:TOKEN_DRIFT_FOUND` | 颜色、字号、间距、圆角、阴影、动效漂移 | 输出 finding | `/specs-execute` 或 `/specs-write` |
| `/design-system-audit:A11Y_RISK_FOUND` | keyboard / focus / contrast / aria / screen reader 风险 | 输出 finding | `/specs-execute` |
| `/design-system-audit:INTERACTION_CONFLICT_FOUND` | loading / error / empty / success / disabled / confirm 状态冲突 | 输出 finding | `/specs-write` 或 `/specs-execute` |
| `/design-system-audit:VISUAL_QA_PENDING` | 缺多 viewport 截图或复验截图 | Phase 3 | `CONTINUE_IN_WORKFLOW` |
| `/design-system-audit:ANTI_AI_TASTE_BLOCKED` | 模板化、空洞、假精致、泛文案、无领域语义 | Phase 4 finding | `REPORT_AND_STOP` |
| `/design-system-audit:DESIGN_SPEC_REQUIRED` | 发现需要新增 / 改写 UX spec | 分流 `/specs-write` | `REPORT_AND_STOP` |
| `/design-system-audit:DESIGN_SYSTEM_READY` | 组件、tokens、A11y、视觉 QA、Taste Gate 均 PASS | 输出 report | `REPORT_AND_STOP` |

## 0.2 状态权威与路由动作 (State Authority / Route Action)

| 事项 | 权威事实源 | 路由动作 (Route Action) |
| ------ | ------------ | -------------- |
| UX / A11y 契约 | `NFR-UX-*` + DSN-UI-* | `CONTINUE_IN_WORKFLOW` |
| 视觉证据 | screenshot / Playwright / Storybook / fixture | `CONTINUE_IN_WORKFLOW` |
| 审美偏好 | 用户明确选择 + SSOT 批准 | `WAIT_FOR_USER` if authoritative |
| 修复实现 | `/specs-execute` Task | `REPORT_AND_STOP` |
| 规格缺口 | `/specs-write` | `REPORT_AND_STOP` |

## 1. 伴生文档 (Companion Documents)

| 文档 | 角色 | 何时读 |
| ------ | ------ | -------- |
| `../protocols/component-token-a11y-protocol.md` | 组件清单、token drift、交互状态、A11y 基线 | Phase 1 / 2 |
| `../protocols/visual-qa-protocol.md` | 多 viewport 截图、视觉 finding、复验证据 | Phase 3 |
| `../protocols/anti-ai-taste-gate.md` | Design Anti-AI Taste Gate、领域感、信息密度、文案质量 | Phase 4 |
| `../templates/design-system-report-template.md` | readiness report 与 finding 模板 | Phase 5 |
