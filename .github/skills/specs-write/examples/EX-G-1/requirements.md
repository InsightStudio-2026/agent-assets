# Requirements · Google OAuth 登录（EX-G-1 Greenfield happy path）

> **EX-G-1 canonical example · Phase 2 Requirements + Phase 3 Design + Phase 4 Tasks + Phase 5 Verification**。本文展示 Greenfield 项目 happy path：REQ + AC + BDD + Derived From + Design 段嵌入末尾 + Tasks + Verification。
> 与 `../../protocols/methodology-kernel.md` Phase 2-5 字面零漂移。

---

## 1. Requirements 表

### 1.1 REQ-1：OAuth 授权流程（State 防 CSRF）

- **Derived From**：`SRC-2` + `SRC-3` + `SRC-4` → `REQ-1`
- **Relation to Existing**：N/A（Greenfield 全新 flow，复用现有 session store）
- **AC-1.1**（EARS 格式）：
  > **WHEN** 未登录用户点击 "Continue with Google"，**THE SYSTEM SHALL**生成 16 bytes 随机 state、存入 session（5 分钟 TTL）、redirect 到 Google authorize URL。

-**AC-1.2**：
  > **WHEN** Google 回调 `/auth/google/callback?code=...&state=...`，**THE SYSTEM SHALL**校验 state 匹配 session 中的值；不匹配则返回 400 + `OAUTH_STATE_MISMATCH`。
-**AC-1.3**：
  > **IF** state 校验通过，**THEN THE SYSTEM SHALL**用 code 向 Google token endpoint 换取 ID Token + access_token，仅保留 ID Token（不存 access/refresh token，符合 INV-BAN-3）。
-**BDD Scenario 1**：
  > **Given**用户 A 点击 "Continue with Google" 按钮
  >**When**A 完成 Google 授权回调，且 state 匹配
  >**Then**系统校验 ID Token 签名（INV-SEC-4） + 取出 sub / email / email_verified claims
  >**And**access_token / refresh_token 不写入数据库 / 日志（INV-BAN-3）
-**Status**：Active

### 1.2 REQ-2：新用户首次 OAuth 自动建账号（Add）

- **Derived From**：`SRC-2` → `REQ-2`
- **Relation to Existing**：复用 `users` 表 + 新增 `users.google_sub` 列
- **AC-2.1**：
  > **WHEN** OAuth 流程返回 ID Token，且 `users` 表中无 `google_sub` 匹配 + 无 `email` 匹配，**THE SYSTEM SHALL**在 `users` 表 INSERT 新行（email + google_sub + 默认 username = email 前缀），并建立 session。

-**AC-2.2**：
  > **WHEN** Google 返回的 `email_verified = false`，**THE SYSTEM SHALL**拒绝建账号（返回 `OAUTH_EMAIL_NOT_VERIFIED`），不写入数据库。
-**Status**：Active

### 1.3 REQ-3：已注册邮箱账号合并（Critical Design Gate）

- **Derived From**：`SRC-2` → `REQ-3`；触发 Critical Design Gate（用户已批准"自动合并"策略）
- **Relation to Existing**：复用 `users` 表；新增 `users.google_sub` UPDATE 路径
- **AC-3.1**：
  > **WHEN** OAuth 流程返回 ID Token，且 `users` 表中无 `google_sub` 匹配但 `email` 匹配现有 user A，**THE SYSTEM SHALL**UPDATE `users[A].google_sub = <Google sub>`，并建立 session（自动合并）。

-**AC-3.2**：
  > **WHEN** 自动合并发生，**THE SYSTEM SHALL**写 audit log（事件类型 `oauth_account_merged`，含 user_id / 旧 auth method / 新增 provider）。
-**AC-3.3**：
  > **WHEN** OAuth 流程返回 ID Token，且 `users.google_sub` 已匹配现有 user A，**THE SYSTEM SHALL**直接建立 session（重复登录）。
-**BDD Scenario 2**（合并路径关键场景）：
  > **Given**user B 邮箱 = `b@example.com`，已注册（username/password），`users[B].google_sub = NULL`
  >**When**B 第一次走 Google OAuth 登录，Google 返回 sub=`g_xyz` + email=`b@example.com` + email_verified=true
  >**Then**`users[B].google_sub` 更新为 `g_xyz`
  >**And**session 建立指向 B
  >**And**audit log 写入 1 条 `oauth_account_merged` 事件
-**Status**：Active（已通过 Critical Design Gate 用户批准）

### 1.4 REQ-4：双登录方式并存

- **Derived From**：`SRC-2` → `REQ-4`
- **Relation to Existing**：不修改现有 username/password 登录路径（继承）
- **AC-4.1**：
  > **WHEN** 用户访问 `/login` 页面，**THE SYSTEM SHALL**同时显示 username/password 表单 + "Continue with Google" 按钮。

-**AC-4.2**：
  > **WHEN** user A 已合并 Google（`users[A].google_sub != NULL`），**THE SYSTEM SHALL**仍允许用户走 username/password 登录（不强制 OAuth）。
-**Status**：Active

---

## 2. Existing Coverage

N/A（Greenfield；本 spec archive 后由长期规格 `.github/instructions/auth-providers.md`（建议项）继续承载，但本 archive 不 Merge Back）。

---

## 3. Design 段（Medium 路径压缩，嵌入本文）

### 3.1 DSN-1 数据契约

| 列 / 表 | Schema | 备注 |
| --------- | -------- | ------ |
| `users.google_sub` | `VARCHAR(64) NULL UNIQUE` | 新增列；migration `2026-05-30-add-google-sub.sql`；可回滚（DROP COLUMN） |
| `users.username` | unchanged | OAuth 新建用户默认 = email 前缀；冲突时加 `_<random4>` 后缀 |
| Session store | unchanged | 复用现有 redis session；OAuth state 用 session key `oauth_state` 临时存 |

### 3.2 DSN-2 接口契约

| Endpoint | Method | Auth | 描述 |
| ---------- | -------- | ------ | ------ |
| `/auth/google` | `GET` | None | 生成 state + redirect 到 Google authorize URL |
| `/auth/google/callback` | `GET` | None | 接收 code + state；校验 state；换 ID Token；建账号 / 合并 / 登录 |
| `/auth/google/error` | `GET` | None | 错误显示页（state 不匹配 / email_verified=false 等） |

### 3.3 DSN-3 失败策略

| 失败场景 | 错误码 | HTTP Status | 用户可见 |
| --------- | -------- | ------------ | --------- |
| state 不匹配 | `OAUTH_STATE_MISMATCH` | 400 | 错误页 + 重试按钮 |
| email_verified=false | `OAUTH_EMAIL_NOT_VERIFIED` | 403 | "请先在 Google 验证邮箱" |
| Google JWKS 拉取失败 | `OAUTH_JWKS_UNAVAILABLE` | 503 | "登录服务暂不可用，请稍后再试" |
| code 换 token 失败 | `OAUTH_TOKEN_EXCHANGE_FAILED` | 502 | "Google 登录失败，请重试" |
| 数据库写失败 | `OAUTH_PERSIST_FAILED` | 500 | 通用错误页（不暴露 SQL stack） |

### 3.4 Reuse vs New

- **Reuse**：`users` 表、authn middleware、session store、audit log 服务、`/login` 页面框架。
- **New**：`users.google_sub` 列、`/auth/google` + `/auth/google/callback` + `/auth/google/error` endpoint、`<GoogleLoginButton>` UI 组件、Google JWKS 缓存逻辑。

### 3.5 INV 守护对齐

| INV | Design 段防御 |
| ----- | -------------- |
| `INV-SEC-2` State 防 CSRF | DSN-1 session 存 state + DSN-3 OAUTH_STATE_MISMATCH 处理 |
| `INV-SEC-3` redirect_uri allowlist | callback handler 启动时读 `OAUTH_REDIRECT_ALLOWLIST` 环境变量；不在 list 内的 redirect_uri 拒绝 |
| `INV-SEC-4` ID Token 签名校验 | DSN-1 JWKS 本地缓存 1 小时 + 启动时 fail-fast 检查 JWKS 可达 |
| `INV-BAN-3` 不存 token | DSN-1 schema 不含 token 列；TASK-3 测试用例显式断言 `users` 表 schema 无 access_token / refresh_token |
| `INV-LIM-3` HTTPS only | callback handler middleware 检查 `req.protocol === 'https'`（local dev 跳过） |

---

## 4. Tasks 段

| Task ID | Description | Status | Touches | Verification | Artifacts | Revert | Anti-Invariants |
| --------- | ------------ | -------- | --------- | -------------- | ----------- | -------- | ----------------- |
| `TASK-1` | migration: 新增 `users.google_sub` UNIQUE 列 | Done | `migrations/2026-05-30-add-google-sub.sql` | `pnpm migrate up && psql -c "\d users"` 输出含新列 + UNIQUE 约束 | `artifacts/migrate-up.log` | `pnpm migrate down`（DROP COLUMN） | `INV-BAN-3` |
| `TASK-2` | OAuth state 生成 + session 存储 + redirect 到 Google | Done | `src/auth/google/start.ts` | `pnpm test src/auth/__tests__/oauth-start.test.ts` | `artifacts/oauth-start-test.log` | `git revert <sha>` | `INV-SEC-2` |
| `TASK-3` | OAuth callback handler（state 校验 + token exchange + JWKS 验证 + INV-BAN-3 断言） | Done | `src/auth/google/callback.ts` + `src/auth/google/jwks-cache.ts` | `pnpm test src/auth/__tests__/oauth-callback.test.ts`（含 INV-BAN-3 schema 断言） | `artifacts/oauth-callback-test.log` | `git revert <sha>` | `INV-SEC-3` + `INV-SEC-4` + `INV-BAN-3` |
| `TASK-4` | 新用户自动建账号 + 已注册邮箱合并逻辑 | Done | `src/auth/google/account-resolver.ts` | `pnpm test src/auth/__tests__/account-resolver.test.ts`（含 BDD Scenario 2 合并路径） | `artifacts/account-resolver-test.log` | `git revert <sha>` | - |
| `TASK-5` | `<GoogleLoginButton>` UI + 接入 `/login` 页面 | Done | `src/features/auth/GoogleLoginButton.tsx` + `src/features/auth/LoginPage.tsx` | `pnpm test:e2e tests/e2e/google-oauth-flow.spec.ts`（mock Google IdP） | `artifacts/e2e-screenshot.png` + `artifacts/e2e-flow.log` | `git revert <sha>` | - |
| `TASK-6` | audit log 写入路径（合并事件 `oauth_account_merged`） | Done | `src/lib/audit.ts` 扩展 + `src/auth/google/account-resolver.ts` 调用 | `pnpm test src/lib/__tests__/audit-oauth-merge.test.ts` | `artifacts/audit-oauth-test.log` | `git revert <sha>` | - |
| `TASK-7` | HTTPS 强制 middleware（staging / prod 启用 INV-LIM-3） | Done | `src/middleware/https-required.ts` | `pnpm test src/middleware/__tests__/https-required.test.ts` | `artifacts/https-test.log` | env 变量 `HTTPS_REQUIRED=false` 临时禁用 | `INV-LIM-3` |

DAG：`TASK-1` → `TASK-2` → `TASK-3` → `TASK-4` → `TASK-5`；`TASK-6` 跟 `TASK-4`；`TASK-7` 独立并行（部署期生效）。

---

## 5. Verification

### 5.1 整体 Verification 命令

```powershell
pnpm typecheck
pnpm lint
pnpm test
pnpm test:e2e -- tests/e2e/google-oauth-flow.spec.ts
pnpm migrate up
psql -c "\d users" | grep google_sub
```

### 5.2 DoD

- TASK-1~7 全部 `Status: Done` + `Verification:` 字段填写。
- `artifacts/` 包含 7 个 task 的执行证据。
- INV-BAN-3 schema 断言 PASS（`users` 表无 token 列）。
- INV-SEC-4 JWKS 启动 fail-fast 测试 PASS。
- 三类 Gate 决策已记录（charter §6 + Real-World Side Effect Gate 转交 release-deploy）。

### 5.3 Verification 结果

| 检查 | 结果 | Evidence |
| ------ | ------ | --------- |
| typecheck | PASS | `artifacts/typecheck.log` |
| lint | PASS | `artifacts/lint.log` |
| unit + integration | PASS（54 个测试，含 OAuth 全流程 + 合并路径 + INV 断言） | `artifacts/test.log` |
| e2e | PASS（mock Google IdP，全流程跑通） | `artifacts/e2e-screenshot.png` + `artifacts/e2e-flow.log` |
| migration up/down | PASS | `artifacts/migrate-up.log` + `artifacts/migrate-down.log` |

---

## 6. Non-Functional Requirements（NFR-* · 6 类槽位 · 详 templates/requirements.md §10 + methodology-kernel.md §1.1）

### 6.0 High-Risk Assessment（必填）

| Risk Trigger | 命中？ | 触发 NFR 类必填 |
| -------------- | ------- | ---------------- |
| 涉外部 API / OAuth / token / PII / 密钥 / 审计 | **High** | NFR-SEC |
| 涉关键路径性能 / 大数据量 / 高并发 / 冷启动 | **High** | NFR-PERF |
| 涉生产副作用 / migration / rollback / feature flag | **High** | NFR-REL |
| 涉用户可见 UI 或键盘 / 屏幕阅读器 / i18n | **High** | NFR-UX |
| 涉桌面 / 多平台 / 浏览器版本兼容 | Low | NFR-PLAT |
| 涉新观测信号 / SLO / alert / runbook | **High** | NFR-OBS |

### 6.1 NFR-SEC-* （Security · High）

```text

NFR-SEC-001: OAuth state 防 CSRF
  Concern: authz | input-validation
  Description: /auth/google/callback 必须校验 state 与 session 中的值一致；state 必须 cryptographic random (≥ 128 bit entropy)；过期 5 分钟后失效
  Threat Model Ref: charter.md §5 INV-SEC-3 (state 必校验)
  Acceptance: state 不匹配 → 返回 OAUTH_STATE_MISMATCH (HTTP 400)，不进入 token 交换
  Verification: pnpm test:auth:oauth-state-csrf (覆盖 REQ-1.S2 + REQ-1.S3)
  Routed to: /security-privacy-audit#NFR-SEC-001
  Status: Active

NFR-SEC-002: token 不持久化
  Concern: secrets | PII
  Description: access_token / refresh_token 不写入数据库 / 日志 / metrics；只在内存中用 ID Token 验证签名后丢弃；users 表只存 google_sub (subject ID)
  Threat Model Ref: charter.md §5 INV-BAN-3
  Acceptance: psql 全表扫描 + log 全文 grep 无 token 字符串
  Verification: pnpm test:auth:no-token-persistence (扫描 users 表 + logs/)
  Routed to: /security-privacy-audit#NFR-SEC-002
  Status: Active

```

### 6.2 NFR-PERF-* （Performance · High）

```text

NFR-PERF-001: OAuth callback 路径 p95 latency
  Metric: latency-p95
  Budget: /auth/google/callback p95 < 800ms (含 Google JWKS 抓取缓存命中 / token 交换 / DB 写入)
  Measure Command: k6 run scripts/perf/oauth-callback.js
  Baseline Ref: N/A: 新路径无 baseline，首发后由 /performance-reliability-audit 建立基线
  Routed to: /performance-reliability-audit#oauth-baseline-required
  Status: Active

NFR-PERF-002: JWKS 缓存与服务冷启动
  Metric: cold-start
  Budget: 服务冷启动后首次 OAuth callback < 1.5s (含 JWKS 首次抓取)；JWKS 缓存命中后 < 800ms (回到 NFR-PERF-001)
  Measure Command: pnpm bench:auth:cold-start
  Baseline Ref: N/A: 新路径
  Routed to: /performance-reliability-audit
  Status: Active

```

### 6.3 NFR-OBS-* （Observability · High）

```text

NFR-OBS-001: OAuth 失败率 alert
  Signal Type: alert
  Description: OAuth callback 失败率短期飙升时触发 alert (state 不匹配 / token 交换失败 / DB 写入失败 / email_verified=false 拒绝)
  Schema: metric `oauth.callback.failed` with labels `error_code` ∈ {state_mismatch, token_exchange_failed, persist_failed, email_not_verified}
  Alert Threshold: 5 分钟窗口内失败率 > 10% 持续 2 个评估周期
  Runbook Ref: /observability-incident#oauth-failure-runbook
  Dashboard Ref: dashboards/auth-oauth.json
  Routed to: /observability-incident#NFR-OBS-001
  Status: Active

NFR-OBS-002: OAuth audit log（合规 + 取证）
  Signal Type: log
  Description: 每次成功登录 / 账号合并 / state 不匹配 / email_verified=false 拒绝 必产 audit log
  Schema: event_type ∈ {oauth_login_success, oauth_account_merged, oauth_state_mismatch, oauth_email_not_verified}; 含 user_id (登录后) / google_sub_prefix (前 8 位) / ip / user_agent_hash; 不含 token 任何字段
  Alert Threshold: N/A: 仅记录，不直接 alert（由 NFR-OBS-001 监控失败率）
  Runbook Ref: N/A
  Dashboard Ref: dashboards/auth-audit.json
  Routed to: /observability-incident
  Status: Active

```

### 6.4 NFR-REL-* （Release · High）

```text

NFR-REL-001: feature flag 灰度上线
  Type: feature-flag
  Description: 上线时 `feature_flags.oauth_google_login = false`；按用户 ID hash 分桶逐步放量（0% → 1% → 10% → 100%）
  Rollback Plan: 设 feature flag = false → `<GoogleLoginButton>` 不渲染（前端） + /auth/google* endpoint 返回 404 (后端) → 验证现有 username/password 登录路径不受影响
  Migration Plan Ref: NFR-REL-002 (schema 迁移独立)
  Routed to: /release-deploy#oauth-google-flag
  Status: Active

NFR-REL-002: schema 迁移 users.google_sub
  Type: migration
  Description: ALTER TABLE users ADD COLUMN google_sub VARCHAR(255) NULL UNIQUE; 上线前应用，可独立于 feature flag
  Rollback Plan: feature flag 关闭 → 24h 观察无 google_sub 写入 → 备份 users 表 → ALTER TABLE users DROP COLUMN google_sub (无外键约束，安全)
  Migration Plan Ref: /data-migration-safety#users-google-sub
  Routed to: /release-deploy + /data-migration-safety
  Status: Active

```

### 6.5 NFR-UX-* （UX / A11y · High）

```text

NFR-UX-001: GoogleLoginButton 可访问性
  Concern: keyboard-nav | screen-reader | contrast | focus
  Standard: WCAG-2.1-AA
  Description: 按钮可键盘 Tab 聚焦；聚焦态有可见 outline；屏幕阅读器读出 "Sign in with Google"；Google 图标 + 文字对比度 ≥ 4.5:1
  Acceptance: axe scan: 0 critical violations on /login route; 手动 NVDA / VoiceOver 测试通过
  Verification: pnpm test:e2e:auth:a11y (使用 @axe-core/playwright)
  Routed to: /design-system-audit (P1，未来如启用)
  Status: Active

NFR-UX-002: OAuth 错误页 i18n
  Concern: error-states | i18n
  Standard: 项目 i18n 框架（en / zh-CN 双语）
  Description: /auth/google/error 页面错误码可本地化为用户友好文案；不暴露内部错误码（OAUTH_TOKEN_EXCHANGE_FAILED → "Google 登录失败，请重试"）
  Acceptance: en / zh-CN 双语 e2e 测试通过；错误码不出现在最终 DOM
  Verification: pnpm test:e2e:auth:error-i18n
  Routed to: N/A (设计系统 P1，本切片不分流)
  Status: Active

```

### 6.6 NFR-PLAT-* （Platform · Low → 整类 N/A）

```text

NFR-PLAT: N/A — 本 feature 仅 web，标准浏览器（Chrome/Edge/Firefox/Safari 现代版本）兼容性继承项目 baseline；不涉桌面应用 / mobile native / 特殊 OS 版本；High-Risk 表对应行 = Low；如未来引入 native 客户端 OAuth flow 需新建 NFR-PLAT-001。

```

### 6.7 NFR ↔ Verification ↔ Workflow Routing Table

| NFR ID | Type | Status | Acceptance / Budget | Verification | Routed to |
| -------- | ------ | -------- | --------------------- | -------------- | ----------- |
| NFR-SEC-001 | Security | Active | state 不匹配 → 400 OAUTH_STATE_MISMATCH | `pnpm test:auth:oauth-state-csrf` | `/security-privacy-audit#NFR-SEC-001` |
| NFR-SEC-002 | Security | Active | psql + logs grep token = 0 | `pnpm test:auth:no-token-persistence` | `/security-privacy-audit#NFR-SEC-002` |
| NFR-PERF-001 | Performance | Active | callback p95 < 800ms | `k6 run scripts/perf/oauth-callback.js` | `/performance-reliability-audit#oauth-baseline-required` |
| NFR-PERF-002 | Performance | Active | cold start < 1.5s | `pnpm bench:auth:cold-start` | `/performance-reliability-audit` |
| NFR-OBS-001 | Observability | Active | 失败率 > 10% 5min alert | runbook `/observability-incident#oauth-failure-runbook` | `/observability-incident#NFR-OBS-001` |
| NFR-OBS-002 | Observability | Active | 4 类 audit event 必产 | log schema 自检 (TASK-7) | `/observability-incident` |
| NFR-REL-001 | Release | Active | feature flag 灰度 0→100% | `/release-deploy#oauth-google-flag` | `/release-deploy#oauth-google-flag` |
| NFR-REL-002 | Release | Active | google_sub 加列 + drop column rollback | `/data-migration-safety#users-google-sub` | `/release-deploy` + `/data-migration-safety` |
| NFR-UX-001 | UX/A11y | Active | axe 0 critical | `pnpm test:e2e:auth:a11y` | `/design-system-audit` (P1) |
| NFR-UX-002 | UX/A11y | Active | en/zh-CN 双语错误页 | `pnpm test:e2e:auth:error-i18n` | N/A |
| NFR-PLAT | Platform | N/A | 仅 web，继承 baseline | N/A | N/A |

### 6.8 NFR DoD（自检）

- [x] §6.0 High-Risk 表已填（5 类 High + 1 类 Low），与 charter §3 Goals + §5 INV 一致。
- [x] 每个 High 类有 ≥ 1 条 Active NFR（SEC: 2; PERF: 2; OBS: 2; REL: 2; UX: 2）。
- [x] Low 类 NFR-PLAT 显式 N/A 含理由。
- [x] §6.7 路由表与 §6.1~§6.6 一致，10 条 Active + 1 条 N/A 全列。
- [x] 高风险 NFR 全分流：SEC → `/security-privacy-audit`；PERF → `/performance-reliability-audit`；OBS → `/observability-incident`；REL → `/release-deploy` (+ `/data-migration-safety` for NFR-REL-002)；UX-001 → `/design-system-audit` (P1)。
- [x] 每条 Active NFR 的 `Verification` 字段非空（命令或专项 workflow 锚点）。
- [x] Greenfield 模式不强制 Delta Operation 字段（本 example 故意省略以体现 Greenfield 简化）。
- [x] tasks.md TASK-1~7 已引用相关 NFR：TASK-1 ↔ NFR-SEC-001 (state); TASK-2 ↔ NFR-SEC-002 (token 不写表); TASK-5 ↔ NFR-OBS-002 (audit log); TASK-6 ↔ NFR-PERF-001/002 (perf); TASK-7 ↔ NFR-REL-001/002 + NFR-UX-001/002。

`R-CHK-EX-1.8` 校验本节完整性；详 `../../../asset-quality-gates/references/checks-catalog.md §3.1`。

---

## 7. Status

- spec 阶段：Done
- archive 决策：见 `archive.md`（Archive Only；后续多 provider 扩展 = Brownfield delta spec）
