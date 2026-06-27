# Spec · 通知偏好（F-FIX-2 伪化版本，故意失败）

> **F-FIX-2 conformance fixture · 故意失败的 spec.md**。基于 `EX-M-1/spec.md` 删除 `Derived From` 字段；不可作为真实 spec 模板使用。
> 期望 `/asset-quality-gates` `R-CHK-EX-1.2 missing traceability chain` 命中。

---

## 0. Maturity Intake

| 字段 | 值 |
| ------ | --- |
| Project Maturity | Greenfield |
| Audit Profile | Baseline Survey |
| SSOT Health | OK |
| Confidence | High |
| Decision | `PROCEED_TO_CHARTER` |

---

## 1. Charter

### 1.1 Sources

| Source ID | 类型 | 内容 | Timestamp |
| ----------- | ------ | ------ | ----------- |
| `SRC-1` | 用户原话 | "加一个我的设置 → 通知偏好页面，让用户能选要不要收营销邮件。MVP 范围内，不接第三方邮件 SDK，先存数据库就行。" | 2026-05-24T10:00 |

### 1.2 Scope

- 用户可在"我的设置 → 通知偏好"页面切换营销邮件订阅状态。
- 切换状态持久化到数据库；下次登录可见上次选择。

### 1.3 Out of Charter

- 不接第三方邮件 SDK。
- 不实现实际邮件发送过滤逻辑。

### 1.4 Architectural Invariants

- `INV-BAN-1`：禁止在前端 bundle 暴露用户邮箱。
- `INV-LIM-1`：用户设置变更 API 必须走现有 authn middleware。
- `INV-SEC-1`：变更操作必须写审计日志。

### 1.5 Mode 判定

- Project Mode = Greenfield
- Spec Mode = Medium

---

## 2. Requirements

### 2.1 REQ-1：用户切换通知偏好

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
  >**And**audit log 写入 1 条 `setting_changed` 事件
-**Status**：Active

---

## 3. Plan（Medium 路径压缩）

### 3.1 DSN-1 数据契约

| 字段 | 类型 | 默认值 | 备注 |
| ------ | ------ | ------- | ------ |
| `users.marketing_emails_enabled` | `BOOLEAN NOT NULL` | `TRUE` | 新增列 |

### 3.2 DSN-2 接口契约

| Endpoint | Method | Auth | Body | Response |
| ---------- | -------- | ------ | ------ | ---------- |
| `/api/me/notification-preferences` | `GET` | Required | - | `{ marketing_emails_enabled: boolean }` |
| `/api/me/notification-preferences` | `PATCH` | Required | `{ marketing_emails_enabled: boolean }` | `200 OK` |

---

## 4. Tasks

| Task ID | Description | Status | Touches | Verification | Artifacts |
| --------- | ------------ | -------- | --------- | -------------- | ----------- |
| `TASK-1` | DB migration | Done | `migrations/2026-05-24-add-mail-pref.sql` | `pnpm migrate up` | `artifacts/migrate-up.log` |
| `TASK-2` | API endpoint | Done | `src/api/notification-preferences.ts` | `pnpm test` | `artifacts/api-test.log` |
| `TASK-3` | UI 组件 | Done | `src/features/settings/NotificationPrefs.tsx` | `pnpm test:e2e` | `artifacts/e2e.png` |

---

## 5. Verification

```powershell
pnpm typecheck
pnpm lint
pnpm test
pnpm test:e2e
```

---

## 6. Status

- spec 阶段：Done

---

> **故意漂移点**（与 `EX-M-1/spec.md` 对照可见的失败位置）：
>
> - §2.1 REQ-1 段开头**整段删除** `**Derived From**：SRC-1 → REQ-1` 字段（原 EX-M-1/spec.md line 63）
> - §2.2 `Existing Coverage` 段被一并删除（避免误干扰）
> - §2.1 BDD Scenario 不带任何 SRC-*/ REQ-* / AC-* 锚点回引
> - 解析器无法从 §2 任一处重建 REQ-1 ↔ SRC-1 traceability 锚点链
