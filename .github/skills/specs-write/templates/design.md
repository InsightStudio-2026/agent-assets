# design.md 模板

> **When to read**: 在 `/specs-write` Phase 3 落 design.md 时读取本文。Medium 路径①可跳过。

## Design — `<Feature Name>`

Feature Slug: `<feature-slug>`
Project Mode: Seed / Init | Greenfield | Hybrid | Brownfield
Charter Ref: charter.md
Audit Ref: audit.md (Approved @ `<date>`) | N/A (Seed / Greenfield; see maturity-intake.md)
Requirements Ref: requirements.md (Approved @ `<date>`)

## 1. Context Summary

<3-5 句：本设计承接的目标 / 上游契约 / 关键非目标>

## 1.5 Reuse vs New（仅 Hybrid / Brownfield）

| 既有元素 | 决策 | 新元素 ID | 备注 |
| ---------- | ------ | ----------- | ------ |
| EXIST-DSN-DB-003 | Reuse | — | 字段足够 |
| EXIST-DSN-API-012 | Replace | DSN-API-001 | 错误码对齐 SRC-002#<章节> |

## 2. Architectural Invariants Inheritance

> 复述 charter.md `## 5` 中所有 INV-* 与本设计的绑定关系；任一冲突必须停下并回 Phase 1。

| INV ID | Type | Rule (复述 charter 原文) | 本设计如何遵守 |
| -------- | ------ | -------------------------- | ---------------- |
| INV-BAN-001 | Ban | <复述> | <DSN-API-001 不得引入 ...> |
| INV-LIM-001 | Limit | <复述> | <DSN-DB-001 限定 ...> |
| INV-SEC-001 | Security | <复述> | <DSN-API-001 凭据从 KMS / Vault / keyring 读取，写入 audit log> |

## 3. Proposed Design Overview

- Boundary: <模块 / 服务 / 进程 / 跨端边界>
- Modules: <列出新增 / 修改的模块>
- Data Flow: <主路径 + 失败路径 + 异步边界>

## 4. Architecture

### DSN-ARCH-001: <标题>

- Linked Requirements: REQ-001, REQ-003
- Derived From: SRC-001#<章节>
- Relation to Existing: Net New | Extends EXIST-DSN-ARCH-* | ...
- Justification: <仅当 Net New 必填>
- Content: ...
- Failure Strategy（跨边界必填）:
  - 超时: 检测=<SLA 或 exception> · 重试=<N 次 指数退避 幂等与否> · 最终态=<错误提示 / 降级> · 补偿=<事件 / 表 / N/A>
  - 进程崩溃: ...
  - 数据层错误: ...
- Concurrency & Lock（条件化必填）:
  - 并发模型 / 退避与排队 / 用户可见兜底 / 检测信号

## 5. Data Model

### DSN-DB-001: <表 / 字段 / 约束>

- Linked Requirements: REQ-001
- Derived From: SRC-002#<章节>
- Relation to Existing: Net New | Reuse EXIST-DSN-DB-*| Replaces EXIST-DSN-DB-*
- Justification: <仅当 Net New 必填>
- Schema:

```sql
-- DDL
```

- Migration Strategy（`Replaces` 且命中 `design-rules.md §1` 条件时必填 · 三选一 · 加性变更可 N/A）:
  - strategy: shadow_write | backward_compatible_stepwise | downgrade_script | N/A (additive only)
  - shadow_write 示例: dual_write_window: 2026-05-15 → 2026-05-29; consistency_check: <项目脚本，详见 `project-adapter.md §1`>; cutover_condition: 连续 72h diff=0 且业务报警 0; rollback_window: 切流后 7 天内可一键切回
  - backward_compatible_stepwise 示例: step1: add column <新列> nullable（PR-A · 独立可部署）; step2: backfill via <项目脚本>（独立可重跑）; step3: switch reads to <新列>（PR-B）; step4: drop <旧列>（PR-C · 上一阶段上线 ≥ 7 天）
  - downgrade_script 示例: down_script: database/migrations/`<rev>`_down.sql; mirror_table: <旧结构镜像表名>（保留 ≥ 30 天）
  - business_data_safety_proof: <1–2 句说明为何业务数据无损转回>

## 6. API / Interface Contract

### DSN-API-001: <endpoint / method>

- Linked Requirements: REQ-002
- Derived From: SRC-002#<章节>
- Relation to Existing: Replaces EXIST-DSN-API-012 | Net New | ...
- Justification: <理由>
- Request: ...
- Response: ...
- Error Cases: ...
- Failure Strategy（跨边界必填）: 超时 / 进程崩溃 / 数据层错误（同上四元素结构）
- Concurrency & Lock（多端并发 / 共享资源 / LLM 配额共池 命中时必填）:
  - 并发模型 / 退避与排队 / 用户可见兜底 / 检测信号

## 7. UI / UX State Model

### DSN-UI-001: <页面 / 组件>

- Linked Requirements: REQ-004
- States: loading / empty / error / success
- 跨端类型契约（详见 `project-adapter.md §1`）:
  - Type SSOT: <例 backend/schemas/payment.py::PaymentRequest>
  - Generated Side: <例 frontend/types/generated/payment.ts>
  - Regen Command: <项目脚本 contract_regen 槽位>
  - Drift Check: <项目脚本 contract_drift 槽位>
- Visual Refs（推荐 · 软约束）:
  - figma_node: `<node-id>`
  - design_hash: `<SHA>`
  - storybook: `<story-id>`
- Anti-patterns: ...

## 7.5 LLM Design（仅当涉及 AI/LLM）

### DSN-LLM-001: <Agent / Prompt 管道 / 工具调用>

- Linked Requirements / Derived From / Relation to Existing
- Input/Output Contract / Cost / Audit
- Prompt Boundaries（注入防御 · 必填）: 用户内容隔离 / 脱逃检测
- Deterministic Fallback（保底静态逻辑 · 必填）: 触发条件 / 保底路径
- Context Truncation Strategy（上下文裁剪优先级 · 必填）: 必留 / 可压缩 / 可舍 / 裁剪后是否需用户确认
- Failure Strategy（跨边界必填）: 超时 / 进程崩溃 / 数据层错误
- Concurrency & Lock（条件化必填）

## 8. State Machines / Background Jobs

### DSN-OBS-001: <任务 / 状态机>

- Idempotency / Retry / Logging / Metrics
- Failure Strategy（跨边界必填）
- Concurrency & Lock（条件化必填）

## 9. Security & Permissions

### DSN-SEC-001: <权限模型 / 凭据流 / 隔离边界>

- Linked Requirements: ...
- INV-SEC Compliance（必填 · 涉凭据 / API Key / PII / 跨网域 / 交易必填）:
  - 适用 INV-SEC-*（charter.md `## 5`）原文复述: ...
  - 凭据读取路径: KMS / Vault / keyring / env / config secrets manager
  - 凭据流转: <谁→谁，是否加密，是否 redacted in logs>

## 10. Compatibility & Migration

- Backward Compatibility: <对既有调用方 / 数据 / 部署的兼容性策略>
- Migration Plan: <如何分阶段切流 / 灰度 / 回滚窗口>

## 11. Alternatives Considered

- 方案 A vs B vs C：差异 / 权衡 / 选择理由

## 12. Risks

- R1: ...

## 13. Open Questions

- Q1: ...

## 14. Critical Assumptions Summary

- A1: <假设> · Confidence: high|mid|low · Validation: <如何验证>
- 或填 `N/A: <说明>`

## 15. Approval

- Status: Draft | Approved | Needs Changes
- Notes: <用户原话 或 AI-DRI auto-approved 留痕，详 §3.2.3>
- Timestamp: <ISO 8601>
