# Requirements — Greenfield OAuth Login (F-FIX-8 A · 故意失败：NFR 留空)

> ⚠️ **本文件是 conformance fixture**，**故意**违反 R-CHK-EX-1.8。NFR 段 §10 标 5 类 High 但整段空白；不是真实 spec。

Mode: Medium (single-file: 单 feature 简化示例)
Project Mode: Greenfield
Feature Slug: oauth-google-login-broken-A
Charter Ref: charter.md
Created: 2026-05-24

## 1. Summary

Greenfield 项目首次集成 Google OAuth 登录。本 fixture 用于测试 R-CHK-EX-1.8 对"高风险 feature NFR 留空"的识别能力。

## 2. Goals

- G1: 用户可通过 Google 账号登录
- G2: 不影响现有 username/password 登录路径

## 3. Requirements

### REQ-1: OAuth 授权流程

- Derived From: SRC-1 → REQ-1
- Description: 实现 /auth/google → /auth/google/callback 流程
- Acceptance Criteria:
  - AC-1.1: WHEN 用户点击 Google 登录按钮 THEN the SYSTEM SHALL 重定向到 Google OAuth
- Status: Active

### REQ-2: 账号建立

- Derived From: SRC-1 → REQ-2
- Description: 新用户首次 OAuth 自动建账号
- Acceptance Criteria:
  - AC-2.1: WHEN Google 返回有效 ID Token THEN the SYSTEM SHALL 在 users 表写入 google_sub
- Status: Active

---

## 10. Non-Functional Requirements

### 10.0 High-Risk Assessment

| Risk Trigger | 命中？ | 触发 NFR 类必填 |
| -------------- | ------- | ---------------- |
| 涉外部 API / OAuth / token / PII / 密钥 / 审计 | **High** | NFR-SEC |
| 涉关键路径性能 / 大数据量 / 高并发 / 冷启动 | **High** | NFR-PERF |
| 涉生产副作用 / migration / rollback / feature flag | **High** | NFR-REL |
| 涉用户可见 UI 或键盘 / 屏幕阅读器 / i18n | **High** | NFR-UX |
| 涉桌面 / 多平台 / 浏览器版本兼容 | Low | NFR-PLAT |
| 涉新观测信号 / SLO / alert / runbook | **High** | NFR-OBS |

### 10.1 NFR-SEC-* （Security · High）

<!-- ⚠️ 故意空白：5 类标 High 但整段无 NFR-* 条目；无 'Status: N/A' 声明 -->

### 10.2 NFR-PERF-* （Performance · High）

<!-- ⚠️ 故意空白 -->

### 10.3 NFR-OBS-* （Observability · High）

<!-- ⚠️ 故意空白 -->

### 10.4 NFR-REL-* （Release · High）

<!-- ⚠️ 故意空白 -->

### 10.5 NFR-UX-* （UX / A11y · High）

<!-- ⚠️ 故意空白 -->

### 10.6 NFR-PLAT-* （Platform · Low）

<!-- ⚠️ 故意空白：标 Low 但既不是 Active 也无 'N/A: <理由>' 声明 -->

### 10.7 NFR ↔ Verification ↔ Workflow Routing Table

| NFR ID | Type | Status | Acceptance | Verification | Routed to |
| -------- | ------ | -------- | ------------ | -------------- | ----------- |
<!-- ⚠️ 故意空表：与 §10.1~§10.6 不一致 -->

### 10.8 NFR DoD

<!-- ⚠️ 故意空白：未自检 -->

---

## 11. Status

- spec 阶段：Draft（不应通过 R-CHK-EX-1.8）
