# Requirements — Brownfield Notification (F-FIX-8 B · 故意失败：Brownfield NFR 缺 Delta Op)

> ⚠️ **本文件是 conformance fixture**，**故意**违反 R-CHK-EX-1.8。Brownfield 模式下部分 NFR 缺 `Delta Operation` 字段；不是真实 spec。

Mode: Medium
Project Mode: Brownfield
Feature Slug: notification-multi-category-broken-B
Charter Ref: charter.md (Project Mode = Brownfield)
Audit Ref: audit.md (Approved @ 2026-05-24)
Created: 2026-05-24

## 1. Summary

Brownfield 改造：单开关订阅 → 多类订阅。本 fixture 用于测试 R-CHK-EX-1.8 对"Brownfield NFR 缺 Delta Operation"的识别。

## 2. Existing Coverage

- EXIST-REQ-1（marketing 开关）：Modify
- EXIST-REQ-2（PATCH endpoint）：Replace

## 3. Requirements

### REQ-1: 多类订阅（Modify）

- Delta Operation: Modify
- Derived From: SRC-1 → REQ-1; EXIST-REQ-1
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

```yaml
NFR-SEC-001: 订阅变更 audit log 扩展 category
  Delta Operation: Modify (extends EXIST-NFR-SEC-005)
  Concern: audit
  Description: 现有 audit log 扩展加 category 字段
  Acceptance: 每次 PATCH 必产 audit log 含 category 列
  Verification: pnpm test:notif:audit-category-extended
  Routed to: /security-privacy-audit
  Status: Active

NFR-SEC-002: authn middleware 行为保留
  Concern: authz
  Description: authn middleware 行为完全不变
  Acceptance: 现有 authn 测试套件 PASS
  Verification: pnpm test:auth:middleware
  Routed to: N/A
  Status: Active
  ⚠️ 故意：缺 'Delta Operation' 字段（Brownfield 必填）
```

### 10.2 NFR-PERF-* （Performance · High）

```yaml
NFR-PERF-001: 邮件发送 p95 latency budget
  Metric: latency-p95
  Old Budget: SMTP 直发 p95 < 5s
  New Budget: Mailgun adapter p95 < 1s
  Measure Command: k6 run scripts/perf/notification-send.js
  Routed to: /performance-reliability-audit
  Status: Active
  ⚠️ 故意：缺 'Delta Operation' 字段（Brownfield 必填，应为 Replace）
```

### 10.3~10.6

<!-- 简化省略：与 EX-B-1 §7.3-7.6 类似，Brownfield delta op 全填，本 fixture 不测试这些 -->

NFR-OBS-001: Delta Operation: Add（占位，本 fixture 不测）
NFR-REL-001: Delta Operation: Add（占位）
NFR-UX-001: Delta Operation: Modify（占位）
NFR-PLAT: N/A — Brownfield 继承 baseline

### 10.7 路由表（部分）

| NFR ID | Delta Op | Type | Status |
| -------- | ---------- | ------ | -------- |
| NFR-SEC-001 | Modify | Security | Active |
| NFR-SEC-002 | **MISSING** | Security | Active |
| NFR-PERF-001 | **MISSING** | Performance | Active |

### 10.8 DoD

- [x] §10.0 High-Risk 表已填
- [x] 每个 High 类有 ≥ 1 条 Active NFR
- [ ]**Brownfield 模式：每条 NFR 必有 Delta Operation 字段** ← 故意未通过

---

## 11. Status

- spec 阶段：Draft（不应通过 R-CHK-EX-1.8）
