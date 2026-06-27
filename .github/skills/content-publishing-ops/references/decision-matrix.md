---
description: "内容发布运营工作流（/content-publishing-ops）专属的触发判定、状态转换路由、状态权威与动作决策矩阵"
---

# 内容发布运营决策矩阵（/content-publishing-ops）

## 0. 触发判定

| ID | 前置条件 | 动作 | 下一步 | 源 |
| ---- | ---------- | ------ | -------- | ------ |
| R-CPO-ENTRY-1 | 用户显式 `/content-publishing-ops` | 启动内容发布流程 | Phase 1 | 本文件 §0 |
| R-CPO-ENTRY-2 | 用户要把 Markdown / 教程 / 宣发内容发布到平台 | 启动适配与确认 | Phase 1 | 本文件 §0 |
| R-CPO-ENTRY-3 | 用户只要改文章内容、不涉及发布 | 分流写作能力 | `writing-shape` / `writing-fragments` | 本文件 §4 |
| R-CPO-ENTRY-4 | 用户要立即真实发布 / 定时发布 / 多平台同步发布 | 装配发布确认包 | Phase 4 | `../protocols/publishing-approval-protocol.md` |
| R-CPO-ENTRY-5 | 涉版权主体、第三方图片、平台素材授权 | 分流权利链审计 | `/authorship-copyright-readiness` | 本文件 §4 |
| R-CPO-ENTRY-6 | 系统状态不清、下一步推进方向不明 | 停止并重定向 | 路由至 `/project-steward` | 临界状态 1 |
| R-CPO-ENTRY-7 | 缺失母本或 L1 SSOT | 停止并重定向 | 路由至 `/project-inception` | 临界状态 2 |
| R-CPO-ENTRY-8 | 属于纯缺陷根因诊断（局部、具体 bug） | 停止并重定向 | 路由至 `diagnose` 技能 | 临界状态 3 |
| R-CPO-ENTRY-9 | 属于新功能、新需求开发、大重构落地 | 停止并重定向 | 路由至 `/specs-write` 与 `/specs-execute` | 临界状态 4 |
| R-CPO-ENTRY-10 | 逻辑简单明确且适合 TDD 验证 | 停止并重定向 | 路由至 `tdd` 技能或直接执行 | 临界状态 5 |

## 0.1 状态与路由汇总 (State / Route Summary)

| 状态 (State) | 判定 | 下一步 | 路由动作 (Route Action) |
| ------- | ------ | -------- | -------------- |
| `/content-publishing-ops:CONTENT_SCOPE_DEFINED` | 内容源、目标平台、受众、目标动作已明确 | Phase 2 | `CONTINUE_IN_WORKFLOW` |
| `/content-publishing-ops:CONTENT_SOURCE_MISSING` | 缺内容源或发布目标 | 报告缺口 | `REPORT_AND_STOP` |
| `/content-publishing-ops:PLATFORM_ADAPTATION_READY` | 平台格式、长度、链接、图片、标签、合规边界已适配 | Phase 3 | `CONTINUE_IN_WORKFLOW` |
| `/content-publishing-ops:PREVIEW_READY` | 预览稿、封面 / 信息图 brief、差异摘要已生成 | Phase 4 | `WAIT_FOR_USER` |
| `/content-publishing-ops:WAITING_PUBLISH_APPROVAL` | 发布确认包已展示，等待用户批准真实发布 | 等用户批准 | `WAIT_FOR_USER` |
| `/content-publishing-ops:APPROVED_TO_PUBLISH` | 用户明确批准平台、账号、版本、时间与撤回路径 | 可按批准动作执行 | `CONFIRMED_ACTION` |
| `/content-publishing-ops:PUBLISHING_BLOCKED` | 平台、权利、账号、素材、外部副作用边界不清 | 分流或等待 | `REPORT_AND_STOP` |
| `/content-publishing-ops:PUBLISH_DONE` | 发布证据已归档 | 输出报告 | `REPORT_AND_STOP` |

## 0.2 状态权威与路由动作 (State Authority / Route Action)

| 事项 | 权威事实源 | 路由动作 (Route Action) |
| ------ | ------------ | -------------- |
| 内容源 | 用户提供文本 / 文件 / approved article | `CONTINUE_IN_WORKFLOW` |
| 平台适配 | `../protocols/platform-adaptation-protocol.md` | `CONTINUE_IN_WORKFLOW` |
| 真实发布授权 | 用户原话 + `../protocols/publishing-approval-protocol.md` | `WAIT_FOR_USER` / `CONFIRMED_ACTION` |
| 发布证据 | `../templates/publishing-evidence-template.md` | `REPORT_AND_STOP` |
| 权利链风险 | `/authorship-copyright-readiness` | `REPORT_AND_STOP` |

## 1. 伴生文档 (Companion Documents)

| 文档 | 角色 | 何时读 |
| ------ | ------ | -------- |
| `../protocols/content-brief-protocol.md` | 内容目标、受众、平台、口径边界、不可发布项 | Phase 1 |
| `../protocols/platform-adaptation-protocol.md` | 公众号 / 小红书 / 微博 / 通用平台的格式与适配规则 | Phase 2 |
| `../protocols/publishing-approval-protocol.md` | 真实发布确认包、外部副作用、撤回 / 更正路径 | Phase 4 |
| `../templates/publishing-evidence-template.md` | 发布证据归档、URL、截图、版本、时间、账号记录 | Phase 5 |
