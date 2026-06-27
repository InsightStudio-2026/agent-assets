---
name: release-notes
description: 生成发布说明、变更摘要、用户可见变更列表与升级注意事项。Use when user asks for release notes, changelog entry, version notes, launch notes, or says 发布说明 / 版本说明 / CHANGELOG / 发版文案。
---

# Release Notes

## 1. 输入事实源

| Rule ID | 事实源 | 用途 | 缺失处理 |
| --------- | -------- | ------ | ---------- |
| RN-SRC-1 | git diff / commits since fixed point | 识别实际变更 | 不编造；要求基准或报告缺失 |
| RN-SRC-2 | issue / PR / spec / tasks | 识别用户价值与范围 | 无上游时只写实现事实 |
| RN-SRC-3 | release-deploy report | 识别发布状态、rollback、migration、known issues | 缺失时不宣称已发布 |
| RN-SRC-4 | CHANGELOG / README / product docs | 保持文案与既有口径一致 | 缺失时写 standalone notes |

## 2. 输出类型

| Type | 触发 | 输出 |
| ------ | ------ | ------ |
| User-facing | 面向用户、客户、应用商店 | 功能价值、修复、升级注意、已知问题 |
| Developer-facing | 面向开发者 / 内部团队 | technical changes、migration、breaking changes、verification |
| Changelog entry | 更新 CHANGELOG 条目 | Added / Changed / Fixed / Removed / Security |
| Launch note | 产品上线说明 | 目标用户、核心价值、风险边界、支持入口 |

## 3. 写作规则

| Rule ID | 规则 | 禁止 |
| --------- | ------ | ------ |
| RN-R1 | 只写事实源支持的变更 | 编造功能或夸大影响 |
| RN-R2 | 用户可见说明优先写结果，不写实现细节 | 把 refactor 当用户功能 |
| RN-R3 | breaking change / migration / rollback 必须显式 | 把风险藏在脚注 |
| RN-R4 | known issue 必须有影响与缓解 | “有些问题待优化” |
| RN-R5 | 未发布只能写 draft | 把 draft 冒充 released |

## 4. 模板 (Template)

```markdown
## 发布说明 (Release Notes) `<version>`

## 核心亮点 (Highlights)

- <对用户可见的价值说明>

## 新增功能 (Added)

- <新增的能力/功能>

## 行为变更 (Changed)

- <行为或体验变化>

## 问题修复 (Fixed)

- <修复的 Bug 说明>

## 破坏性变更与迁移 (Breaking Changes / Migration)

- <需要用户采取的迁移行动，若无则写 N/A>

## 功能验证 (Verification)

- <验证命令 / 证据支持>

## 已知问题 (Known Issues)

- <问题说明 + 缓解/规避措施，若无则写 None>

```

## 5. 完成检查 (Completion Checklist)

| 检查项 (Check) | 合格标准 (PASS) |
| ------- | ------ |
| 事实确凿 (Facts grounded) | 每条 release note 可追到 diff / issue / spec / report |
| 受众匹配 (Audience matched) | 用户版与开发者版没有混用 |
| 风险明示 (Risk surfaced) | breaking / migration / rollback / known issue 明示 |
| 状态诚实 (Status honest) | draft / released / approval pending 不混淆 |
