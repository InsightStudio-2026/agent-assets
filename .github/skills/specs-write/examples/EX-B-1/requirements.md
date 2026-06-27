# Requirements · 多类通知偏好（EX-B-1 Brownfield delta）

> **EX-B-1 canonical example · Phase 2 Requirements**。本文展示 Brownfield spec 的 **delta operation 显式化**+**Derivation Map**+**Existing Coverage**三件套；同时嵌入压缩版 design + tasks 段落（Medium 路径）。
> 与 `../../protocols/methodology-kernel.md` Brownfield delta 七种 operation 字面零漂移。

---

## 1. Derivation Map

| 本 feature 锚点 | 来源 | 关系类型 | 说明 |
| ---------------- | ------ | --------- | ------ |
| `REQ-1` 多类邮件订阅 | `SRC-1` + `EXIST-REQ-1`（EX-M-1 REQ-1） | **Add**（新概念）+ **Modify**（扩展老语义） | 新增 marketing / digest / system_alerts 三类，老总开关变兼容期 fallback |
| `REQ-2` 多类 endpoint schema | `SRC-1` + `EXIST-REQ-2`（EX-M-1 DSN-2） | **Modify**（GET schema）+ **Replace**（PATCH endpoint） | GET 返回 `{ marketing, digest, system_alerts, _legacy_marketing_emails_enabled }`，PATCH 旧 endpoint 删除 |
| `REQ-3` Mailgun 批发切换 | `SRC-4` + `EXIST-REQ-3`（SMTP 直连） | **Replace**（整体替换） | 引入 `mailgun-adapter.ts` + `mailgun_messages` 投递日志表，删除 `smtp-direct.ts` |
| `REQ-4` 废弃 `email_unsubscribe_token` | `SRC-3` + `EXIST-REQ-4` | **Deprecate**（30 天迁移窗口） | Day 0 停写 + Day 30 DROP COLUMN，迁移期监控调用量 |
| `REQ-5` audit log 行为保留 | `EXIST-REQ-5`（INV-SEC-1） | **Preserve**（行为不变） | 多类切换路径仍写 audit log，schema 不变 |

---

## 2. Requirements 表

### 2.1 REQ-1：多类邮件订阅（Add + Modify）

- **Delta Operation**：**Add**（新概念 `notification_categories`）+ **Modify**（扩展 `EXIST-REQ-1` 单开关语义）
- **Derived From**：`SRC-1` → `REQ-1`；引用 `EXIST-REQ-1`（EX-M-1 REQ-1）
- **Relation to Existing**：兼容期 30 天内 `users.marketing_emails_enabled` 与 `notification_preferences[category=marketing].enabled` 双向同步（PATCH 同时写）；30 天后 `marketing_emails_enabled` 仅作为只读历史字段
- **AC-1.1**：**WHEN** 已登录用户访问"通知偏好"页面，**THE SYSTEM SHALL**显示 marketing / digest / system_alerts 三类独立开关，初始状态从 `notification_preferences` 表加载（缺失时回退到 `marketing_emails_enabled` 列值，仅 marketing 类）。

-**AC-1.2**：**WHEN** 用户切换某一类开关并提交，**THE SYSTEM SHALL**在 1 秒内 upsert `notification_preferences(user_id, category, enabled, updated_at)`，并写 1 条 audit log。
-**AC-1.3**：**WHEN** 用户切换 marketing 类开关，**THE SYSTEM SHALL**同步更新 `users.marketing_emails_enabled`（迁移期双写），保证向后兼容。
-**BDD Scenario 1**：
  > **Given**用户 A 在 EX-M-1 时代设置过 `marketing_emails_enabled=FALSE`，且 `notification_preferences` 表无 A 的记录`<br>`
  >**When**A 访问新"通知偏好"页面`<br>`
  >**Then**marketing 开关显示 OFF（从 `marketing_emails_enabled` fallback），digest / system_alerts 显示默认 ON
-**Status**：Active

### 2.2 REQ-2：多类 endpoint schema（Modify + Replace）

- **Delta Operation**：**Modify**（GET schema 扩展）+ **Replace**（PATCH endpoint 替换）
- **Derived From**：`SRC-1` → `REQ-2`；引用 `EXIST-REQ-2`（EX-M-1 DSN-2）
- **Relation to Existing**：`GET /api/me/notification-preferences` 返回字段扩展（向后兼容：保留 `_legacy_marketing_emails_enabled`）；`PATCH /api/me/notification-preferences` 旧版本（仅接受 `{marketing_emails_enabled}`）整体替换为新版本（接受 `{categories: {marketing, digest, system_alerts}}`），不保留旧 PATCH 兼容
- **AC-2.1**：**WHEN** 调用 `GET /api/me/notification-preferences`，**THE SYSTEM SHALL**返回 `{categories: {marketing, digest, system_alerts}, _legacy_marketing_emails_enabled, updated_at}`。

-**AC-2.2**：**WHEN** 调用 `PATCH /api/me/notification-preferences` 老 schema（仅 `{marketing_emails_enabled}`），**THE SYSTEM SHALL**返回 `400 Bad Request` + 错误码 `LEGACY_PATCH_DEPRECATED`（提示客户端升级）。
-**AC-2.3**：**WHEN** 调用新 PATCH，**THE SYSTEM SHALL**走 INV-LIM-1（authn middleware）+ INV-SEC-1（audit log）。
-**Status**：Active

### 2.3 REQ-3：Mailgun 批发切换（Replace）

- **Delta Operation**：**Replace**（`smtp-direct.ts` 整体替换为 `mailgun-adapter.ts`）
- **Derived From**：`SRC-4` → `REQ-3`；引用 `EXIST-REQ-3`
- **Relation to Existing**：`src/lib/smtp-direct.ts` Done 时删除（不保留兼容层，因为 Mailgun adapter 接口与现有 mailer 调用点 1:1 对齐，不需要 shim）
- **AC-3.1**：**WHEN** 系统投递任意类邮件，**THE SYSTEM SHALL** 通过 `mailgun-adapter.ts` 走 Mailgun API；**SHALL NOT**调用 `smtp-direct.ts`。

-**AC-3.2**：**WHEN** Mailgun 返回非 2xx，**THE SYSTEM SHALL**写 `mailgun_messages` 投递日志（status / error / retry_count），并按指数退避重试 3 次。
-**AC-3.3**：**WHEN** 配置环境变量 `MAILGUN_DRY_RUN=true`，**THE SYSTEM SHALL**不真正发送，只写 `mailgun_messages` 表标 `status=dry_run`（满足 INV-LIM-2）。
-**Status**：Active

### 2.4 REQ-4：废弃 `email_unsubscribe_token`（Deprecate）

- **Delta Operation**：**Deprecate**（30 天迁移窗口）
- **Derived From**：`SRC-3` → `REQ-4`；引用 `EXIST-REQ-4`
- **Relation to Existing**：`users.email_unsubscribe_token` 列在 Day 0 停写、Day 30 DROP；监控期 owner = backend-team，删除条件 = 调用量 0 + 7 天观察期；删除任务 = `TASK-DEPRECATE-1`（30 天后执行 `migrations/2026-09-15-drop-email-unsubscribe-token.sql`）
- **AC-4.1**：**WHEN** Day 0 部署完成，**THE SYSTEM SHALL**不再向 `email_unsubscribe_token` 写入新值（所有写路径改为 no-op + 写 deprecation log）。

-**AC-4.2**：**WHEN** Day 0~30 期间检测到任何读 `email_unsubscribe_token` 的调用，**THE SYSTEM SHALL**上报告警并阻止 Day 30 DROP（重启迁移窗口）。
-**AC-4.3**：**WHEN** Day 30 + 调用量 0 + 7 天观察期通过，**THE SYSTEM SHALL**执行 `DROP COLUMN`（不可逆，需用户批准 Real-World Side Effect Gate）。
-**Status**：Active（migration 期）

### 2.5 REQ-5：audit log 行为保留（Preserve）

- **Delta Operation**：**Preserve**（行为完全不变）
- **Derived From**：`EXIST-REQ-5`（EX-M-1 INV-SEC-1）
- **Relation to Existing**：现有 `audit.write(user_id, field, old, new)` 调用路径完全保留；多类切换路径在写 `notification_preferences` 后调用同一 `audit.write`；schema 不扩展
- **AC-5.1**：**WHEN** 任意类开关切换，**THE SYSTEM SHALL**调用 `audit.write(user_id, field='notification_preferences.{category}', old, new)`，与 EX-M-1 时代行为一致（仅 field 命名扩展）。

-**AC-5.2**：**WHEN** Mailgun 投递失败重试，**THE SYSTEM SHALL NOT**触发 audit log（投递失败不是用户操作）。
-**Status**：Active（unchanged from EX-M-1）

---

## 3. Existing Coverage

| EXIST-REQ | 覆盖方式 | 验证 |
| ----------- | --------- | ------ |
| `EXIST-REQ-1` | REQ-1 Modify 覆盖 | `tests/integration/notification-preferences-backcompat.test.ts` 验证 EX-M-1 时代设置在新 UI 仍生效 |
| `EXIST-REQ-2` | REQ-2 Modify + Replace 覆盖 | `tests/api/legacy-patch-rejected.test.ts` 验证老 PATCH 返回 400 |
| `EXIST-REQ-3` | REQ-3 Replace 覆盖 | `tests/integration/no-smtp-direct-import.test.ts` AST 检查无 `smtp-direct` import |
| `EXIST-REQ-4` | REQ-4 Deprecate 覆盖 | Day 0~30 观测 dashboard + Day 30 DROP migration |
| `EXIST-REQ-5` | REQ-5 Preserve 覆盖 | `tests/audit/notification-audit-preserved.test.ts` 验证 audit log schema 不变 |

---

## 4. Design 段（Medium 路径压缩，嵌入本文）

### 4.1 DSN-1 数据契约

| 表 / 列 | Delta | Schema | 备注 |
| --------- | ------- | -------- | ------ |
| `notification_preferences` | **Add** | `(user_id BIGINT FK, category VARCHAR(32), enabled BOOLEAN NOT NULL, updated_at TIMESTAMPTZ, PK(user_id, category))` | 新表，migration `2026-08-15-add-notification-preferences.sql` |
| `mailgun_messages` | **Add** | `(id UUID, user_id BIGINT, category VARCHAR(32), status VARCHAR(16), error TEXT NULL, retry_count INT, created_at TIMESTAMPTZ)` | 投递日志，migration `2026-08-15-add-mailgun-messages.sql` |
| `users.marketing_emails_enabled` | **Preserve**（迁移期） | unchanged | 30 天双写，30 天后只读 fallback |
| `users.email_unsubscribe_token` | **Deprecate** | unchanged Day 0；DROP COLUMN Day 30 | migration `2026-09-15-drop-email-unsubscribe-token.sql`（Day 30 执行） |

### 4.2 DSN-2 接口契约

| Endpoint | Method | Delta | Body / Response |
| ---------- | -------- | ------- | ----------------- |
| `/api/me/notification-preferences` | `GET` | **Modify** | Response: `{categories: {marketing, digest, system_alerts}, _legacy_marketing_emails_enabled, updated_at}` |
| `/api/me/notification-preferences` | `PATCH` | **Replace** | Body: `{categories: {marketing?, digest?, system_alerts?}}`；老 schema → 400 `LEGACY_PATCH_DEPRECATED` |
| `mailer.send()` 内部接口 | - | **Replace**（实现层） | Adapter 从 `smtp-direct` 切换到 `mailgun-adapter`；外部签名不变 |

### 4.3 DSN-3 失败策略

- DB 写失败（`notification_preferences`）→ `500` + 不写 audit log（事务回滚）。
- Mailgun 批发失败 3 次重试后 → 标 `mailgun_messages.status=failed_permanent`；不阻塞用户操作（异步队列）。
- 老 PATCH 调用 → `400` + 错误码 `LEGACY_PATCH_DEPRECATED`；不静默降级。
- Day 30 DROP COLUMN 前必须确认调用量 = 0；否则告警 + 重启窗口。

### 4.4 Reuse vs New

- **Reuse**：authn middleware、audit log 服务、`/settings` 页面框架、`<NotificationPrefsSection>` 组件外壳、`mailer.send()` 调用点。
- **New**：`notification_preferences` 表、`mailgun_messages` 表、`mailgun-adapter.ts`、新 PATCH schema、deprecation 监控 dashboard。
- **Replace**：`smtp-direct.ts`（删除）、老 PATCH endpoint（删除）。
- **Deprecate**：`email_unsubscribe_token`（30 天后 DROP）。

---

## 5. Tasks 段（Medium 路径压缩，嵌入本文）

| Task ID | Description | Status | Touches | Verification | Artifacts | Revert | Anti-Invariants |
| --------- | ------------ | -------- | --------- | -------------- | ----------- | -------- | ----------------- |
| `TASK-1` | migration: 新增 `notification_preferences` + `mailgun_messages` 表 | Done | 2 个 migration sql | `pnpm migrate up` + `psql -c "\d notification_preferences"` | `artifacts/migrate-up.log` | `pnpm migrate down`（DROP TABLE） | `INV-BAN-2` |
| `TASK-2` | 新 GET endpoint schema + 老总开关 fallback 逻辑 | Done | `src/api/notification-preferences.ts` | `pnpm test src/api/__tests__/notification-preferences.test.ts` | `artifacts/api-test.log` | `git revert <sha>` | `INV-LIM-1` |
| `TASK-3` | 替换 PATCH endpoint（删除老 PATCH + 添加新 schema + 双写 marketing 列） | Done | 同上 + `src/api/legacy-patch-rejected.ts` | `pnpm test src/api/__tests__/legacy-patch-rejected.test.ts` | `artifacts/legacy-patch.log` | `git revert <sha>` | `INV-LIM-1` + `INV-SEC-1` |
| `TASK-4` | `<NotificationPrefsSection>` UI 多类切换 | Done | `src/features/settings/NotificationPrefs.tsx` + e2e | `pnpm test:e2e tests/e2e/notification-prefs-multi.spec.ts` | `artifacts/e2e.png` | `git revert <sha>` | `INV-BAN-1` |
| `TASK-5` | `mailgun-adapter.ts` + 删除 `smtp-direct.ts` + dry-run 模式 | Done | `src/lib/mailgun-adapter.ts` + 删除 `src/lib/smtp-direct.ts` | `pnpm test src/lib/__tests__/mailgun-adapter.test.ts` + AST 无 `smtp-direct` import | `artifacts/mailgun-test.log` | `git revert <sha>`（恢复 smtp-direct.ts） | `INV-LIM-2` |
| `TASK-6` | `email_unsubscribe_token` 写路径改 no-op + deprecation log + 监控 dashboard | Done | `src/lib/unsubscribe.ts` + `dashboards/email-unsubscribe-deprecation.json` | `pnpm test src/lib/__tests__/unsubscribe-deprecation.test.ts` + dashboard 上线 | `artifacts/deprecation-monitor.log` | `git revert <sha>`（恢复写路径） | - |
| `TASK-7` | audit log 行为保留验证 | Done | `tests/audit/notification-audit-preserved.test.ts` | `pnpm test tests/audit/notification-audit-preserved.test.ts` | `artifacts/audit-test.log` | N/A（纯测试） | `INV-SEC-1` |
| `TASK-DEPRECATE-1` | Day 30: 执行 DROP COLUMN（用户批准后） | Pending（计划 2026-09-15） | `migrations/2026-09-15-drop-email-unsubscribe-token.sql` | Day 30 调用量 = 0 + 7 天观察 + 用户批准 | `artifacts/drop-column.log`（Day 30 时） | `pnpm migrate down`（30 天内可回滚；30 天后不可逆） | - |

DAG：`TASK-1` → `TASK-2` || `TASK-3` → `TASK-4`；`TASK-5` 独立并行；`TASK-6` 独立并行；`TASK-7` 跟 `TASK-3` / `TASK-4`；`TASK-DEPRECATE-1` 在 Day 30 单独执行（不在本 spec close-out 范围内）。

---

## 6. Verification

### 6.1 整体 Verification 命令

```powershell
pnpm typecheck
pnpm lint
pnpm test
pnpm test:e2e
pnpm migrate up
psql -c "\d notification_preferences" -c "\d mailgun_messages"
```

### 6.2 DoD

- TASK-1~7 全部 `Status: Done` + `Verification:` 字段填写。
- `TASK-DEPRECATE-1` 进入 Pending 状态（计划 Day 30 + 用户批准 Real-World Side Effect Gate）。
- `artifacts/` 包含 7 个 task 的执行证据。
- `tests/integration/no-smtp-direct-import.test.ts` PASS（AST 检查）。
- Mailgun adapter dry-run 模式 PASS（`MAILGUN_DRY_RUN=true` 跑完整 e2e）。

### 6.3 Verification 结果

| 检查 | 结果 | Evidence |
| ------ | ------ | --------- |
| typecheck | PASS | `artifacts/typecheck.log` |
| lint | PASS | `artifacts/lint.log` |
| unit + integration | PASS（92 个测试，含 backcompat / legacy-patch / audit / mailgun） | `artifacts/test.log` |
| e2e | PASS（多类切换 + audit log + Mailgun dry-run） | `artifacts/e2e.png` + `artifacts/e2e.log` |
| migration up/down | PASS | `artifacts/migrate-up.log` + `artifacts/migrate-down.log` |

---

## 7. Non-Functional Requirements（NFR-* · Brownfield delta · 5 种 delta operation 全展示）

> 本节展示 Brownfield 模式下 NFR 必有 `Delta Operation` 字段；下表 11 条 NFR 覆盖 Add / Modify / Replace / Preserve / Deprecate 5 种。详 templates/requirements.md §10 + methodology-kernel.md §1.1。

### 7.0 High-Risk Assessment

| Risk Trigger | 命中？ | 触发 NFR 类必填 |
| -------------- | ------- | ---------------- |
| 涉外部 API / OAuth / token / PII / 密钥 / 审计 | **High** | NFR-SEC |
| 涉关键路径性能 / 大数据量 / 高并发 / 冷启动 | **High** | NFR-PERF |
| 涉生产副作用 / migration / rollback / feature flag | **High** | NFR-REL |
| 涉用户可见 UI 或键盘 / 屏幕阅读器 / i18n | **High** | NFR-UX |
| 涉桌面 / 多平台 / 浏览器版本兼容 | Low | NFR-PLAT |
| 涉新观测信号 / SLO / alert / runbook | **High** | NFR-OBS |

### 7.1 NFR-SEC-* （Security · Modify + Preserve + Add + Deprecate）

```text

NFR-SEC-001: 订阅变更 audit log（扩展 category 字段）
  Delta Operation: Modify (extends EXIST-NFR-SEC-005 from EX-M-1 long-living spec)
  Concern: audit
  Description: 现有 audit log 已记录订阅变更；扩展其 schema 加 `category` 字段（marketing / digest / system_alerts），保留既有事件类型与字段不变
  Threat Model Ref: charter.md §5 INV-SEC-1 (audit log 必产)
  Acceptance: 每次 PATCH 必产 audit log 含 category 列；旧 marketing 切换路径仍写 category=marketing
  Verification: pnpm test:notif:audit-category-extended
  Routed to: /security-privacy-audit#NFR-SEC-001-modify
  Status: Active

NFR-SEC-002: authn middleware 行为保留
  Delta Operation: Preserve (depends EXIST-NFR-SEC-001)
  Concern: authz
  Description: authn middleware 行为完全不变；新 PATCH endpoint 复用现有 middleware；session 验证 / 限流 / IP 检查全继承
  Acceptance: 新 endpoint 通过现有 authn 集成测试套件不修改
  Verification: pnpm test:auth:middleware (现有套件覆盖新 endpoint)
  Routed to: N/A: Preserve 不需新分流
  Status: Active

NFR-SEC-003: Mailgun API key 不持久化
  Delta Operation: Add (Replace 子产物：smtp-direct 无外部 API key，Mailgun 引入新风险面)
  Concern: secrets
  Description: Mailgun API key 仅从环境变量读取；不写入 DB / log / metrics；adapter 内存持有；轮换周期 30 天
  Threat Model Ref: charter.md §5 INV-BAN-3 (extends to Mailgun token)
  Acceptance: psql + logs grep "key-" prefix = 0；Mailgun adapter 单元测试断言无持久化
  Verification: pnpm test:notif:mailgun-key-no-persist
  Routed to: /security-privacy-audit#NFR-SEC-003-add
  Status: Active

NFR-SEC-004: PII unsubscribe_token 列暴露面（30 天后清零）
  Delta Operation: Deprecate (与 REQ-4 Deprecate EXIST-REQ-4 同步)
  Concern: PII
  Description: `users.email_unsubscribe_token` 列承载 PII（可定位用户邮箱）；Day 0 ~ Day 30 双写期保留；Day 30 后 DROP COLUMN 后该 PII 暴露面清零
  Sunset Window: 30 天 (Day 0 = REQ-4 上线日, Day 30 = DROP COLUMN 日)
  Sunset Trigger: Real-World Side Effect Gate 用户批准 + 调用量 = 0 + 7 天观察期通过
  Acceptance: Day 30+ psql `\d users` 不含 `email_unsubscribe_token` 列
  Verification: TASK-DEPRECATE-1 Day 30 验证（psql 检查 + 调用量 dashboard）
  Routed to: /security-privacy-audit#NFR-SEC-004-deprecate + /release-deploy (Real-World Side Effect Gate)
  Status: Active (migration 期)

```

### 7.2 NFR-PERF-* （Performance · Replace）

```text

NFR-PERF-001: 邮件发送 p95 latency budget
  Delta Operation: Replace (replaces EXIST-NFR-PERF-001 from EX-M-1)
  Metric: latency-p95
  Old Budget: SMTP 直发 p95 < 5s (smtp-direct.ts)
  New Budget: Mailgun adapter p95 < 1s (Mailgun 批发更快)
  Measure Command: k6 run scripts/perf/notification-send.js
  Baseline Ref: /performance-reliability-audit#mailgun-baseline (Day 0 + 7 day baseline)
  Routed to: /performance-reliability-audit#NFR-PERF-001-replace
  Status: Active

```

### 7.3 NFR-OBS-* （Observability · Add + Modify）

```text

NFR-OBS-001: deprecation 监控 dashboard
  Delta Operation: Add
  Signal Type: dashboard + metric
  Description: 监控 `users.email_unsubscribe_token` 列读次数 + 老 PATCH endpoint 调用次数；按调用源 IP / user-agent 标 label
  Schema: metric `legacy.unsubscribe_token.read.count` + `legacy.patch_endpoint.call.count` (labels: source_ip_hash, user_agent_class)
  Alert Threshold: Day 30 前任一项调用量 > 0 → 阻塞 DROP COLUMN
  Runbook Ref: /observability-incident#deprecation-runbook
  Dashboard Ref: dashboards/notif-deprecation.json
  Routed to: /observability-incident#NFR-OBS-001-add
  Status: Active

NFR-OBS-002: 邮件发送失败 alert（扩展 provider label）
  Delta Operation: Modify (extends EXIST-NFR-OBS-001)
  Signal Type: alert
  Description: 现有 alert "邮件发送失败 5min > 10%" 保留；扩展 provider label (smtp-direct / mailgun)；smtp-direct 弃用后该 label 调用量必为 0
  Schema: metric `notification.send.failed` with labels `provider` ∈ {smtp-direct, mailgun}, `error_code`
  Alert Threshold: 5 分钟内 mailgun 失败率 > 10% → alert；smtp-direct 调用量 > 0 (Day 0 后) → alert
  Runbook Ref: /observability-incident#mailgun-failure-runbook
  Routed to: /observability-incident#NFR-OBS-002-modify
  Status: Active

```

### 7.4 NFR-REL-* （Release · Add）

```text

NFR-REL-001: 多类订阅 feature flag
  Delta Operation: Add
  Type: feature-flag
  Description: 上线时 `feature_flags.notification_categories_enabled = false`；按用户 ID hash 灰度（0% → 10% → 50% → 100%）；UI 与 PATCH endpoint 全靠此 flag 控制
  Rollback Plan: 设 flag = false → 前端回退单开关；后端老 PATCH 重新可用；30 天双写期保证 fallback 可用
  Migration Plan Ref: NFR-REL-002 (schema 迁移独立)
  Routed to: /release-deploy#notification-categories-flag
  Status: Active

NFR-REL-002: schema 双写期 + DROP COLUMN
  Delta Operation: Add (含 Deprecate 子动作)
  Type: migration
  Description: Day 0 创建 `notification_preferences` 表 + 双写 30 天；Day 30 DROP COLUMN `users.email_unsubscribe_token` (Real-World Side Effect Gate 必批准)
  Rollback Plan: Day 0~Day 29 内 → DROP TABLE notification_preferences + 关 flag；Day 30+ 无法回滚（不可逆，需 Real-World Side Effect Gate 用户批准前 7 天观察期）
  Migration Plan Ref: /data-migration-safety#users-token-deprecate
  Routed to: /release-deploy + /data-migration-safety + /security-privacy-audit (Real-World Side Effect Gate)
  Status: Active (Day 0 已 Done; TASK-DEPRECATE-1 Day 30 待执行)

```

### 7.5 NFR-UX-* （UX / A11y · Modify）

```text

NFR-UX-001: 多类开关 UI 可访问性（保留 + 扩展）
  Delta Operation: Modify (extends EXIST-NFR-UX-002 from EX-M-1)
  Concern: keyboard-nav | screen-reader | error-states
  Standard: WCAG-2.1-AA (继承)
  Description: 单开关 → 三类独立开关；保留 keyboard Tab 顺序 + 屏幕阅读器读出 (扩展为 "Marketing emails toggle / Weekly digest toggle / System alerts toggle")；新增 error-states for PATCH 400 LEGACY_PATCH_DEPRECATED
  Acceptance: axe scan: 0 critical violations on /settings/notifications route; 三开关 keyboard 操作连续；error toast 屏幕阅读器读出
  Verification: pnpm test:e2e:notif:a11y + pnpm test:e2e:notif:legacy-patch-error
  Routed to: /design-system-audit (P1)
  Status: Active

```

### 7.6 NFR-PLAT-* （Platform · Low → N/A）

```text

NFR-PLAT: N/A — Brownfield 继承 EX-M-1 baseline (web only)；本 delta 不引入新平台 / OS / 浏览器版本约束。

```

### 7.7 NFR ↔ Verification ↔ Workflow Routing Table

| NFR ID | Delta Op | Type | Status | Acceptance | Verification | Routed to |
| -------- | ---------- | ------ | -------- | ------------ | -------------- | ----------- |
| NFR-SEC-001 | Modify | Security | Active | audit log 含 category | `pnpm test:notif:audit-category-extended` | `/security-privacy-audit#NFR-SEC-001-modify` |
| NFR-SEC-002 | Preserve | Security | Active | authn 套件不变 PASS | `pnpm test:auth:middleware` | N/A: Preserve |
| NFR-SEC-003 | Add | Security | Active | Mailgun key 无持久化 | `pnpm test:notif:mailgun-key-no-persist` | `/security-privacy-audit#NFR-SEC-003-add` |
| NFR-SEC-004 | Deprecate | Security | Active (migration) | Day 30 列已 DROP | TASK-DEPRECATE-1 验证 | `/security-privacy-audit#NFR-SEC-004-deprecate` + `/release-deploy` |
| NFR-PERF-001 | Replace | Performance | Active | Mailgun p95 < 1s | `k6 run scripts/perf/notification-send.js` | `/performance-reliability-audit#NFR-PERF-001-replace` |
| NFR-OBS-001 | Add | Observability | Active | legacy 调用量监控 | dashboard `dashboards/notif-deprecation.json` | `/observability-incident#NFR-OBS-001-add` |
| NFR-OBS-002 | Modify | Observability | Active | provider label alert | runbook `/observability-incident#mailgun-failure-runbook` | `/observability-incident#NFR-OBS-002-modify` |
| NFR-REL-001 | Add | Release | Active | feature flag 灰度 0→100% | `/release-deploy#notification-categories-flag` | `/release-deploy` |
| NFR-REL-002 | Add | Release | Active (Day 0 done; Day 30 pending) | Day 30 DROP COLUMN | TASK-DEPRECATE-1 + Real-World Side Effect Gate | `/release-deploy` + `/data-migration-safety` + `/security-privacy-audit` |
| NFR-UX-001 | Modify | UX/A11y | Active | axe 0 critical + 三开关 keyboard | `pnpm test:e2e:notif:a11y` | `/design-system-audit` (P1) |
| NFR-PLAT | N/A | Platform | N/A | 继承 baseline | N/A | N/A |

### 7.8 Delta Operation 统计（5 种全覆盖）

| Delta Op | NFR ID | 计数 |
| ---------- | -------- | ------ |
| **Add** | NFR-SEC-003, NFR-OBS-001, NFR-REL-001, NFR-REL-002 | 4 |
| **Modify** | NFR-SEC-001, NFR-OBS-002, NFR-UX-001 | 3 |
| **Replace** | NFR-PERF-001 | 1 |
| **Preserve** | NFR-SEC-002 | 1 |
| **Deprecate** | NFR-SEC-004 | 1 |
| **N/A**(整类) | NFR-PLAT | 1 |

### 7.9 NFR DoD（自检）

- [x] §7.0 High-Risk 表已填（5 类 High + 1 类 Low）。
- [x] 每个 High 类有 ≥ 1 条 Active NFR。
- [x] Low 类 NFR-PLAT 显式 N/A 含理由。
- [x] §7.7 路由表与 §7.1~§7.6 一致，10 条 Active + 1 条 N/A 全列。
- [x]**Brownfield 模式：每条 NFR 必有 `Delta Operation` 字段** ✓ (§7.8 5 种 delta 全覆盖)。
- [x] 每条 Active NFR 的 `Verification` 字段非空。
- [x] tasks.md TASK-1~7 + TASK-DEPRECATE-1 已引用相关 NFR：TASK-2 ↔ NFR-SEC-001/002 (audit + authn); TASK-3 ↔ NFR-SEC-003 + NFR-PERF-001 (Mailgun); TASK-5 ↔ NFR-OBS-001/002; TASK-7 ↔ NFR-REL-001 + NFR-UX-001; TASK-DEPRECATE-1 ↔ NFR-SEC-004 + NFR-REL-002。

`R-CHK-EX-1.8` 校验本节完整性；详 `../../../asset-quality-gates/references/checks-catalog.md §3.1`。

---

## 8. Status

- spec 阶段：Done（除 `TASK-DEPRECATE-1` Day 30 任务外）
- archive 决策：见 `archive.md`（Merge Back 到 long-living `notifications-spec`）
