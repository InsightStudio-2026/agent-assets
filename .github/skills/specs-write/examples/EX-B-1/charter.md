# Charter · 多类通知偏好（EX-B-1 Brownfield delta）

> **EX-B-1 canonical example · Phase 1 Charter**。本文展示 Brownfield 项目 charter 写法：通过 `EXIST-REQ-*` 锚点引用 long-living spec / archived spec 已有事实，**不重写**全量规格。
> 与 `../../protocols/methodology-kernel.md` Brownfield 路径字面零漂移。

---

## 0. Maturity Intake

| 字段 | 值 |
| ------ | --- |
| Project Maturity | Brownfield（既有上线 feature `EX-M-1` 已 archive；存在 6 个月以上的 production 数据流） |
| Audit Profile | Scoped Full-Surface Audit（仅在通知 / 邮件 / authn / audit log 范围内做完整 14 面） |
| SSOT Health | OK（`docs/specs/EX-M-1/archive.md` + 现网代码作为 EXIST-REQ 事实源） |
| Confidence | High |
| Decision | `PROCEED_TO_CHARTER` |
| Blocking Issues | 无 |
| SSOT Stewardship Suggestions | 建议在本 feature Done 后建立 long-living `notifications-spec`（见 archive.md Merge Back 决策） |

---

## 1. Sources

| Source ID | 类型 | 内容 | Timestamp |
| ----------- | ------ | ------ | ----------- |
| `SRC-1` | 用户原话 | "扩展多类邮件订阅，营销 / 交易 / 系统三类独立开关；老总开关保留兼容期；批发改 Mailgun；废弃 `email_unsubscribe_token`；保留 `users.marketing_emails_enabled` 列只读" | 2026-08-15T09:00 |
| `SRC-2` | 既有 archive | `EX-M-1` 通知偏好（单开关）已 archive；REQ-1 + DSN-1 + DSN-2 全冻结 | 2026-05-24（archive 时间） |
| `SRC-3` | 安全审查 | `email_unsubscribe_token` 6 个月零调用 + PII 风险（明文 token 暴露 email hash）→ 必须废弃 | 2026-08-10 |
| `SRC-4` | 运维事故 | 直连 SMTP 7 月份发生 1 次 deliverability 大规模降级（黑名单）→ 必须切换到第三方批发通道 | 2026-07-22 |

---

## 2. Existing Requirements（来自 `EX-M-1` archive 与现网）

| EXIST-REQ ID | Source Spec | 摘要 | 当前状态 | 本 feature delta operation |
| -------------- | ------------- | ------ | ---------- | --------------------------- |
| `EXIST-REQ-1` | `EX-M-1` REQ-1 | 用户切换营销邮件订阅（单开关 `users.marketing_emails_enabled`） | Active in production | **Modify**（语义扩展为多类） |
| `EXIST-REQ-2` | `EX-M-1` DSN-2 | `GET / PATCH /api/me/notification-preferences` 单字段 schema | Active in production | **Replace**（PATCH 旧 endpoint 替换为多类 PATCH，GET 改 schema = `Modify`） |
| `EXIST-REQ-3` | 现网遗留代码 | 邮件批发走直连 SMTP（`src/lib/smtp-direct.ts`） | Active but degraded | **Replace**（迁移到 Mailgun adapter，旧 SMTP 删除） |
| `EXIST-REQ-4` | 现网遗留代码 | `users.email_unsubscribe_token` 列（6 个月零调用 + PII 风险） | Active but unused | **Deprecate**（迁移窗口 30 天后 DROP COLUMN） |
| `EXIST-REQ-5` | `EX-M-1` INV-SEC-1 | 用户设置变更必须写 audit log | Active in production | **Preserve**（行为不变，扩展到多类后仍写 audit log） |

`EXIST-REQ-*` 是引用锚点，不是本 feature 的修改对象本身；本 feature 通过 `requirements.md` 的 `REQ-*` + `Delta Operation` + `Derivation Map` 表达 delta。

---

## 3. Scope

- 用户可在"我的设置 → 通知偏好"页面分别切换 **marketing / digest / system_alerts**三类邮件订阅开关。
- 老总开关（`users.marketing_emails_enabled`）保留兼容期 30 天，仅作为只读 fallback。
- 实时邮件批发切换到 Mailgun（替换 SMTP 直连）。
- 废弃 `email_unsubscribe_token`（30 天迁移窗口后 DROP COLUMN）。
- 现有 audit log 行为保留不变（多类切换仍写 audit log）。

---

## 4. Out of Charter

- 不引入 in-app push notifications（限定本 feature 仅 email channel）。
- 不实现用户自定义邮件模板（仅 1 个开关 / 类）。
- 不接 SMS / WeChat / Lark 等非 email channel。
- 不重构 `/settings` 页面框架（仅扩展 `<NotificationPrefsSection>` 内部）。
- 不修改 `EX-M-1` 已 archived 的 spec.md（archive 不可反流）。

---

## 5. Derivation Constraints

-**必须**复用 `EX-M-1` 已建立的 `users.marketing_emails_enabled` 列结构（不重新设计）。

- **必须**保留 `audit_log` 写入路径（`EXIST-REQ-5` Preserve）。
- **不得**在新表中重复 PII（email / phone）；新 `notification_preferences` 表只存 `user_id` + `category` + `enabled` + `updated_at`。
- 新 endpoint 必须向后兼容老总开关 `marketing_emails_enabled`（PATCH 同时写新表 + 老列，30 天迁移期）。

---

## 6. Architectural Invariants

| Invariant ID | 类型 | 内容 | 适用 |
| -------------- | ------ | ------ | ------ |
| `INV-BAN-1` | 禁止 | 前端 bundle 不暴露用户邮箱（继承自 `EX-M-1`） | 全 feature |
| `INV-LIM-1` | 限制 | 设置变更 API 必须走现有 authn middleware | 全 feature |
| `INV-SEC-1` | 必须 | 设置变更必须写 audit log（继承自 `EX-M-1`，扩展到多类） | 全 feature |
| `INV-BAN-2` | 禁止 | 不得在新表中存 PII（email / phone） | `notification_preferences` 表 |
| `INV-LIM-2` | 限制 | Mailgun adapter 必须支持 dry-run 模式（避免迁移期发真实邮件） | `mailgun-adapter.ts` |

---

## 7. Mode 判定

- Project Mode = Brownfield
- Spec Mode = Medium（多 endpoint + 多表变更，但边界清晰；不需 Large 独立 design.md，design 段落嵌入 `requirements.md` 末尾）
- Decision Gate（按 `../../references/cross-cutting.md`）：
  - Strategy Gate：`PROCEED`（用户原话明确）
  - Critical Design Gate：`PROCEED_AFTER_REVIEW`（Mailgun 切换 = 外部依赖变更，需用户确认）
  - Real-World Side Effect Gate：`PROCEED_AFTER_REVIEW`（DROP COLUMN + 第三方付费服务接入，需用户批准 release-deploy 时再确认一次）

---

## 8. 与 `R-CHK-EX-1.*` 期望对齐

| Sub-rule | Charter 段对齐 |
| ---------- | ---------------- |
| `R-CHK-EX-1.1` Delta operation | §2 Existing Requirements 表显式给出 5 种 delta operation |
| `R-CHK-EX-1.2` Traceability | §1 Sources 锚点 + §2 EXIST-REQ Source Spec 锚点 |
| `R-CHK-EX-1.6` Out-of-Charter | §4 显式列出 5 项 out-of-charter 边界 |
