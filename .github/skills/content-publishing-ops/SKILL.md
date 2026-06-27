---
name: content-publishing-ops
description: 内容发布运营：将 Markdown、教程、宣发内容适配到多平台，治理内容 brief、平台格式、预览、发布确认包、撤回 / 更正路径与证据归档；真实发布必须用户批准。
argument-hint: "要发布什么内容到哪些平台？"
disable-model-invocation: true
---


# /content-publishing-ops · 内容发布运营

**定位**：把 Markdown、教程、宣发内容到多平台发布的流程工程化；覆盖内容 brief、平台适配、格式转换、封面 / 信息图 brief、发布前预览、用户确认、发布证据归档。

**边界**：不自动真实发布；不绕过平台规则；不把宣传口径写回 L1 SSOT，除非用户批准；不替代 `/authorship-copyright-readiness` 的权利链审计，不替代 `/release-deploy` 的产品发布放行。

**斜杠命令**：`/content-publishing-ops`

---

## 懒加载契约

- **MUST read**: `./decision-matrix.md`
- 开始判定或执行 Phase 流程前，必须完整懒加载上述细节。

---

## 1. 伴随文档

| 文档 | 角色 | 何时读 |
| ------ | ------ | -------- |
| `protocols/content-brief-protocol.md` | 内容纲要与运营约束协议 | Phase 1 |
| `protocols/platform-adaptation-protocol.md` | 跨平台适配与预览发布规范 | Phase 2, Phase 3 |
| `protocols/publishing-approval-protocol.md` | 发布确认与授权边界协议 | Phase 4 |
| `templates/publishing-evidence-template.md` | 发布凭证与回滚撤回归档模板 | Phase 5 |

---

## 2. 阶段骨架

| Phase | 目标 | MUST read | 输出 |
| ------- | ------ | ----------- | ------ |
| Phase 1 — Content Brief | 明确内容源、受众、目标平台、发布目标、禁止口径 | `protocols/content-brief-protocol.md` | `/content-publishing-ops:CONTENT_SCOPE_DEFINED` |
| Phase 2 — Platform Adaptation | 转换格式、标题、摘要、标签、图片 brief、链接策略 | `protocols/platform-adaptation-protocol.md` | `/content-publishing-ops:PLATFORM_ADAPTATION_READY` |
| Phase 3 — Preview Packet | 输出各平台预览稿与差异摘要 | `protocols/platform-adaptation-protocol.md` | `/content-publishing-ops:PREVIEW_READY` |
| Phase 4 — Approval Gate | 展示发布确认包，等待用户批准 | `protocols/publishing-approval-protocol.md` | `/content-publishing-ops:WAITING_PUBLISH_APPROVAL` / `/content-publishing-ops:APPROVED_TO_PUBLISH` |
| Phase 5 — Evidence Archive | 记录发布 URL / 时间 / 截图 / 版本 / 撤回路径 | `templates/publishing-evidence-template.md` | `/content-publishing-ops:PUBLISH_DONE` |

## 3. 输出格式

```markdown
## 内容宣发与发布报告 (Content Publishing Ops Report)

## 工作流状态 (Workflow State)

- State: /content-publishing-ops:<STATE>

## 宣发内容范围 (Content Scope)

- 事实内容源 (Source):
- 发布目标平台 (Target platforms):
- 目标受众 (Audience):
- 发布目的 (Publish goal):

## 各平台预览稿 (Preview)
|  | 目标平台 (Platform) | 转换版本 (Version) | 预览稿路径 (Preview Path) | 格式/排版缺陷 (Gap) |  |
|  | ---------- | --------- | -------------- | ----- |  |

## 授权边界 (Authorization Boundary)

- 路由动作 (Route Action): <WAIT_FOR_USER | CONFIRMED_ACTION | REPORT_AND_STOP>
- 授权来源 (Confirmation source): <user quote or N/A>
- 授权范围 (Authorized scope): <platform + account + content version + time>
- 未授权范围 (Not authorized): <other platforms / future posts / SSOT edits / real-world side effects outside packet>

## 发布证据 (Evidence)

- <发布 URL / 屏幕截图 / 归档路径 or N/A>

```

## 4. 禁止动作

| 禁止项 | 原因 |
| -------- | ------ |
| 不自动真实发布 | 真实发布是外部副作用，必须用户批准 |
| 不绕过平台规则 | 平台合规与账号安全优先 |
| 不把营销口径静默写回 L1 SSOT | 宣发文案不是产品权威事实源 |
| 不使用 license 不明图片 / 字体 / 素材 | 权利链风险归 `/authorship-copyright-readiness` |
| 不把 preview 当 published | Draft / Preview / Published 状态必须分开 |

## 5. 快速自检清单

报告前自检：

- [ ] 是否明确了发布内容的源文件、目标平台以及发布目标？
- [ ] 跨平台适配（格式、摘要、标签等）是否已按照平台协议转换完成？
- [ ] 是否为所有目标平台生成了预览稿，并排除了排版和样式 Gap？
- [ ] 真实发布前，是否已装配“发布确认包”并取得用户的明确批准？
- [ ] 发布完成后，是否已归档发布 URL、截图以及对应的撤回/更正路径？

## 支撑资源

- [content-brief-protocol.md](./protocols/content-brief-protocol.md)
- [decision-matrix.md](./references/decision-matrix.md)
- [platform-adaptation-protocol.md](./protocols/platform-adaptation-protocol.md)
- [publishing-approval-protocol.md](./protocols/publishing-approval-protocol.md)
- [publishing-evidence-template.md](./templates/publishing-evidence-template.md)
