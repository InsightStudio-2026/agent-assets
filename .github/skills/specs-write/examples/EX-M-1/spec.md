# Spec · 通知偏好（Medium single-file）

> **EX-M-1 canonical example · Medium single-file**。本文件单文件承载 Greenfield Medium spec 的 5 段最小语义层：proposal / behavior / plan / tasks / verification。
> 不替代真实 spec；新项目复用时按真实业务改 SRC / REQ / DSN / TASK 内容，但**保留段落结构**。

---

## 0. Maturity Intake

| 字段 | 值 |
| ------ | --- |
| Project Maturity | Greenfield |
| Audit Profile | Baseline Survey |
| SSOT Health | OK（项目立项已批准 product brief，作为 SRC-1） |
| Confidence | High |
| Decision | `PROCEED_TO_CHARTER` |
| Blocking Issues | 无 |
| SSOT Stewardship Suggestions | 无 |

---

## 1. Charter（Phase 1 Proposal 段）

### 1.1 Sources

| Source ID | 类型 | 内容 | Timestamp |
| ----------- | ------ | ------ | ----------- |
| `SRC-1` | 用户原话 | "加一个我的设置 → 通知偏好页面，让用户能选要不要收营销邮件。MVP 范围内，不接第三方邮件 SDK，先存数据库就行。" | 2026-05-24T10:00 |

### 1.2 Scope

- 用户可在"我的设置 → 通知偏好"页面切换营销邮件订阅状态。
- 切换状态持久化到数据库；下次登录可见上次选择。

### 1.3 Out of Charter

- 不接第三方邮件 SDK（如 SendGrid / Mailgun）。
- 不实现实际邮件发送过滤逻辑（MVP 阶段只存意图，邮件批发系统后续 spec 接入）。
- 不区分多类邮件（营销 / 交易 / 系统通知）；仅 1 个开关。

### 1.4 Derivation Constraints

- 必须用现有 `users` 表 + 新增 1 列 `marketing_emails_enabled`（不开新表）。
- 必须复用现有"我的设置"页面框架（不独立路由）。

### 1.5 Architectural Invariants

- `INV-BAN-1`：禁止在前端 bundle 暴露用户邮箱（已是 baseline）。
- `INV-LIM-1`：用户设置变更 API 必须走现有 authn middleware。
- `INV-SEC-1`：变更操作必须写审计日志（user_id / 变更字段 / 时间戳）。

### 1.6 Mode 判定

- Project Mode = Greenfield
- Spec Mode = Medium（边界清晰、单表变更 + 单 UI 段；不独立 design.md）

---

## 2. Requirements（Phase 2 Behavior 段）

### 2.1 REQ-1：用户切换通知偏好

- **Derived From**：`SRC-1` → `REQ-1`
- **Relation to Existing**：N/A（Greenfield，无 EXIST-REQ）
- **AC-1.1**（EARS 格式）：
  > **WHEN** 已登录用户访问"我的设置 → 通知偏好"页面，**THE SYSTEM SHALL**显示当前营销邮件订阅状态（默认订阅）。

-**AC-1.2**（EARS 格式）：
  > **WHEN** 已登录用户切换营销邮件订阅开关并提交，**THE SYSTEM SHALL**在 1 秒内持久化到 `users.marketing_emails_enabled`，并显示成功提示。
-**AC-1.3**（EARS 格式）：
  > **IF** 用户未登录，**THEN THE SYSTEM SHALL**重定向到登录页（沿用现有 authn middleware）。
-**BDD Scenario 1**：
  > **Given**一个已登录用户 A，其 `users.marketing_emails_enabled = TRUE`<br/>
  >**When**A 访问"通知偏好"页面并把开关切换为 OFF 提交<br/>
  >**Then**`users.marketing_emails_enabled` 在 1 秒内更新为 `FALSE`<br/>
  >**And**页面显示"设置已保存"提示<br/>
  >**And**audit log 写入 1 条 `setting_changed` 事件（user_id=A, field=marketing_emails_enabled, old=TRUE, new=FALSE）
-**Status**：Active

### 2.2 Existing Coverage

N/A（Greenfield；未来 archive 时若有 long-living `notifications-spec`，本 REQ-1 走 Merge Back）。

---

## 3. Plan（Phase 3 Design 段，Medium 路径压缩）

### 3.1 DSN-1 数据契约

| 字段 | 类型 | 默认值 | 备注 |
| ------ | ------ | ------- | ------ |
| `users.marketing_emails_enabled` | `BOOLEAN NOT NULL` | `TRUE` | 新增列；migration `2026-05-24-add-marketing-emails-enabled`；可回滚（`DROP COLUMN`） |

### 3.2 DSN-2 接口契约

| Endpoint | Method | Auth | Body | Response |
| ---------- | -------- | ------ | ------ | ---------- |
| `/api/me/notification-preferences` | `GET` | Required | - | `{ marketing_emails_enabled: boolean }` |
| `/api/me/notification-preferences` | `PATCH` | Required | `{ marketing_emails_enabled: boolean }` | `200 OK` 或 `400 / 401 / 500` |

### 3.3 DSN-3 失败策略

- DB 写失败 → 返回 `500`，前端显示通用错误提示，不暴露 SQL stack。
- Auth 缺 → `401`（middleware 处理）。
- 并发写（同用户多 tab）→ 后到先得；不实现 ETag。

### 3.4 Reuse vs New

- **Reuse**：`/settings` 路由框架、authn middleware、audit log 服务。
- **New**：`/api/me/notification-preferences` endpoint、`marketing_emails_enabled` 列、`<NotificationPrefsSection>` UI 组件。

---

## 4. Tasks（Phase 4 段）

| Task ID | Description | Status | Touches | Verification | Artifacts | Revert | Anti-Invariants |
| --------- | ------------ | -------- | --------- | -------------- | ----------- | -------- | ----------------- |
| `TASK-1` | DB migration 新增 `marketing_emails_enabled` 列 | Done | `migrations/2026-05-24-add-mail-pref.sql` | `pnpm migrate up && psql -c "\d users"` 输出含新列 | `artifacts/migrate-up.log` | `pnpm migrate down`（DROP COLUMN） | `INV-LIM-1` |
| `TASK-2` | API endpoint GET/PATCH `/api/me/notification-preferences` + audit log 写入 | Done | `src/api/notification-preferences.ts` + `src/lib/audit.ts` | `pnpm test src/api/__tests__/notification-preferences.test.ts` 全 PASS | `artifacts/api-test-output.log` | `git revert <sha>` | `INV-SEC-1` |
| `TASK-3` | `<NotificationPrefsSection>` UI 组件 + 接入 `/settings` 页面 | Done | `src/features/settings/NotificationPrefs.tsx` + `src/features/settings/SettingsPage.tsx` | `pnpm test src/features/settings/__tests__/NotificationPrefs.test.tsx` 全 PASS + Playwright smoke `tests/e2e/notification-prefs.spec.ts` | `artifacts/e2e-screenshot.png` + `artifacts/ui-test.log` | `git revert <sha>` | `INV-BAN-1` |

DAG：`TASK-1` → `TASK-2` → `TASK-3`（线性，无并行）。

---

## 5. Verification

### 5.1 整体 Verification 命令

```powershell
pnpm typecheck
pnpm lint
pnpm test
pnpm test:e2e -- tests/e2e/notification-prefs.spec.ts
```

### 5.2 DoD

- 全部 Task `Status: Done` + `Verification:` 字段填写。
- `artifacts/` 包含 migrate-up.log / api-test-output.log / ui-test.log / e2e-screenshot.png。
- audit log 测试用例 PASS（验证 `INV-SEC-1`）。
- 前端 bundle 不暴露用户 email（验证 `INV-BAN-1`，由 `pnpm bundle:analyze` 抽查）。

### 5.3 Verification 结果

| 检查 | 结果 | Evidence |
| ------ | ------ | --------- |
| typecheck | PASS | `artifacts/typecheck.log` |
| lint | PASS | `artifacts/lint.log` |
| test (unit + integration) | PASS（38 个测试） | `artifacts/test.log` |
| e2e | PASS（1 关键路径） | `artifacts/e2e-screenshot.png` |

---

## 6. Status

- spec 阶段：Done
- archive 决策：见 `archive.md`
