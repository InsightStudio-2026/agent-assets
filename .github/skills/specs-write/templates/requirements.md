# requirements.md 模板

> **When to read**: 在 `/specs-write` Phase 2 落 requirements.md 时读取本文.

## Requirements — `<Feature Name>`

Mode: Large | Medium (design skipped: `<reason>`) | Medium (single-file: `<reason>`)
Project Mode: Seed / Init | Greenfield | Hybrid | Brownfield
Feature Slug: `<feature-slug>`
Charter Ref: charter.md
Audit Ref: audit.md (Approved @ `<date>`) | N/A (Seed / Greenfield; see maturity-intake.md)
Created: `<YYYY-MM-DD>`

## 1. Summary

<一段话：这个需求是什么，服务谁，解决什么问题>

## 2. Background / Context

<现状、动机、触发事件、关联的既有系统>

## 3. Goals

- G1: ...

## 4. Non-Goals

- NG1: ...

## 5. Existing Coverage（仅 Hybrid / Brownfield）

- EXIST-REQ-007（现有能力 X）：已覆盖基础能力，本 Spec 在其上扩展 Y
- EXIST-DSN-DB-003（现有表）：复用，仅追加字段 Z
- EXIST-DSN-API-012（现有接口）：将被 DSN-API-001 替换

> Seed / Greenfield 本节填 `N/A`，并引用 maturity-intake.md 的 Baseline / Greenfield Survey 证据。

## 6. User Stories（认知对齐）

- US-001:
  - 作为 <角色>，
  - 我希望 <能力>，
  - 以便 <价值>。

## 7. Behavior Scenarios（BDD · 必填，每条 REQ ≥ 1）

> 命名 `<REQ-###>.S<n>`，便于 §9 各条 REQ 内通过 `Behavior Scenarios:` 字段引用。

```gherkin
Scenario REQ-001.S1: <场景标题> — 关联 US-001 / AC-001.1
  Given <可观测当前状态：含具体行数 / 字段值 / 表存在性>
    And <附加前置 · 非平凡数据态必须引用 <Fixture:路径> / <Factory:符号> / <Seed:脚本>>
  When <单一可执行触发：脚本命令 / API 调用 / 用户动作 / migration apply>
  Then <可断言结果：SQL 谓词 / HTTP 状态码 / 文件存在 / 字段值>
    And <附加断言>
```

## 8. Derivation Map（必填）

| Spec ID | Derived From | Relation to Existing |
| --------- | -------------- | ---------------------- |
| REQ-001 | SRC-001#<章节> | Extends EXIST-REQ-007 |
| REQ-002 | SRC-002#<章节> | Net New |

> Greenfield 模式 Relation to Existing 统一填 `Net New`。

## 9. Requirements

### REQ-001: <标题>

- Linked User Stories: US-001
- Derived From: SRC-001#<章节>
- Relation to Existing: Extends EXIST-REQ-007 | Replaces EXIST-DSN-*| Conflicts EXIST-DSN-* | Depends EXIST-DSN-* | Net New
- Justification: <仅当 Net New 必填>
- Description: ...
- Rationale: ...
- Acceptance Criteria（EARS · 目标态契约 · `cross-cutting.md §3.1`）:
  - AC-001.1: WHEN <用户触发动作> THEN the <系统> SHALL <可观察响应>.
  - AC-001.2: IF <条件> THEN the <系统> SHALL <可观察响应>.
  - AC-001.5: The <DB / table / view> SHALL satisfy <state predicate>.（Stateful 数据变体）
- Behavior Scenarios（BDD · 行为路径契约 · 必填 ≥ 1）:
  - REQ-001.S1（覆盖 AC-001.1, AC-001.5）
  - REQ-001.S2（覆盖 AC-001.2 失败回滚分支）

## 10. Non-Functional Requirements（NFR-* · 6 类槽位 · 必填或显式 N/A）

> NFR 不是后期检查项；spec 阶段必须显式声明，让 `/specs-execute` 不需要临时猜测质量门，让专项 workflow 能从 spec 上游取契约。事实源详 `../protocols/methodology-kernel.md` NFR 段。

### 10.0 High-Risk Assessment（必填 · 决定哪些 NFR 类必声明 Active）

| Risk Trigger | 命中？ | 触发的 NFR 类必填 |
| -------------- | ------- | ------------------ |
| 涉外部 API / OAuth / token / PII / 密钥 / 审计 | High / Low | NFR-SEC |
| 涉关键路径性能 / 大数据量 / 高并发 / 冷启动 | High / Low | NFR-PERF |
| 涉生产副作用 / migration / rollback / feature flag | High / Low | NFR-REL |
| 涉用户可见 UI 或键盘 / 屏幕阅读器 / i18n | High / Low | NFR-UX |
| 涉桌面 / 多平台 / 浏览器版本兼容 | High / Low | NFR-PLAT |
| 涉新观测信号 / SLO / alert / runbook | High / Low | NFR-OBS |

**规则**：

- 任一 Risk Trigger = High → 对应 NFR 类**必有 ≥ 1 条 `Status: Active` NFR**（不允许整类 N/A）。
- 全部 = Low → 仍必须每类有显式声明（Active 或 `Status: N/A: <理由>`），**不允许整段空**。
- 留空（既不是 Active 也不是显式 N/A） = Spec 漂移，被 `R-CHK-EX-1.8` 命中。

### 10.1 NFR-SEC-* （Security · 权限 / PII / 密钥 / 审计 / 加密 / 输入校验 / 供应链）

```text

NFR-SEC-001: <Title 一句话>
  Concern: authz | PII | secrets | audit | encryption-in-transit | encryption-at-rest | input-validation | supply-chain
  Description: <具体威胁 / 边界 / 假设>
  Threat Model Ref: <charter.md §X.Y or /security-privacy-audit#锚点 or N/A>
  Acceptance: <可观测可验证条件，如 "无明文 token 写入 DB / log">
  Verification: <command or Routed to: /security-privacy-audit#NFR-SEC-001>
  Routed to: /security-privacy-audit | `<other>` | N/A
  Status: Active | N/A: <理由>
  Delta Operation（仅 Brownfield）: Add | Modify | Replace | Deprecate | Preserve

```

或整类 N/A：

```text

NFR-SEC: N/A — <理由：本 feature 不涉外部权限 / PII / 密钥 / 审计；High-Risk 表对应行 Low>

```

### 10.2 NFR-PERF-* （Performance Budget · latency / memory / bundle / cold-start / throughput）

```text

NFR-PERF-001: `<Title>`
  Metric: latency-p95 | latency-p99 | memory | bundle-size | cold-start | API-throughput | DB-query-count | LCP | INP | CLS
  Budget: <具体数字 + 单位，如 "p95 < 200ms" / "bundle gzip < 200KB" / "cold start < 1.5s">
  Measure Command: <复现命令，如 `pnpm bench:auth`>
  Baseline Ref: <baseline 文件锚点 or /performance-reliability-audit#锚点 or N/A: 新路径无 baseline>
  Routed to: /performance-reliability-audit | `<other>` | N/A
  Status: Active | N/A: <理由>
  Delta Operation（仅 Brownfield）: Add | Modify | Replace | Deprecate | Preserve

```

### 10.3 NFR-OBS-* （Observability · logs / metrics / traces / alerts / dashboards / runbooks）

```text

NFR-OBS-001: `<Title>`
  Signal Type: log | metric | trace | alert | dashboard | runbook
  Description: <信号语义>
  Schema: <结构化字段 / metric label / trace tag / log keyword>
  Alert Threshold: <触发条件，如 "p95 > 500ms 持续 5 分钟" / N/A：仅 dashboard>
  Runbook Ref: <runbook 锚点 or /observability-incident#锚点 or N/A>
  Dashboard Ref: <dashboard 锚点 or N/A>
  Routed to: /observability-incident | `<other>` | N/A
  Status: Active | N/A: <理由>
  Delta Operation（仅 Brownfield）: Add | Modify | Replace | Deprecate | Preserve

```

### 10.4 NFR-REL-* （Release Constraints · feature flag / migration / rollback / canary）

```text

NFR-REL-001: `<Title>`
  Type: feature-flag | migration | rollback | canary | blue-green | dark-launch
  Description: <发布动作 / 边界 / 时间窗口>
  Rollback Plan: <具体步骤 / 命令，如 "禁 flag → 重启 → 验证 user_session 表无 google_oauth_id 列读">
  Migration Plan Ref: </data-migration-safety#锚点 or N/A：无 schema 变更>
  Routed to: /release-deploy | /data-migration-safety | `<other>` | N/A
  Status: Active | N/A: <理由>
  Delta Operation（仅 Brownfield）: Add | Modify | Replace | Deprecate | Preserve

```

### 10.5 NFR-UX-* （UX / A11y · keyboard / screen-reader / contrast / focus / aria / responsive / errors / loading / i18n）

```text

NFR-UX-001: `<Title>`
  Concern: keyboard-nav | screen-reader | contrast | focus | aria | responsive | error-states | loading-states | i18n
  Standard: WCAG-2.1-AA | WCAG-2.2-AA | <自定义>
  Description: <具体要求>
  Acceptance: <可验证条件，如 "axe scan: 0 critical violations on /login route">
  Verification: <command or Routed to: /design-system-audit#NFR-UX-001>
  Routed to: /design-system-audit | `<other>` | N/A
  Status: Active | N/A: <理由>
  Delta Operation（仅 Brownfield）: Add | Modify | Replace | Deprecate | Preserve

```

### 10.6 NFR-PLAT-* （Platform Constraints · OS / browser / device / network）

```text

NFR-PLAT-001: `<Title>`
  Platform: web | desktop-windows | desktop-macos | desktop-linux | mobile-ios | mobile-android | `<specific>`
  Constraint: <OS 版本 / 浏览器版本 / 设备能力 / 网络条件，如 "Chrome ≥ 110 / Safari ≥ 15">
  Description: <具体兼容性要求 / 不兼容时的降级>
  Verification: <command or 兼容性测试矩阵锚点>
  Routed to: /desktop-release | /release-deploy | `<other>` | N/A
  Status: Active | N/A: <理由>
  Delta Operation（仅 Brownfield）: Add | Modify | Replace | Deprecate | Preserve

```

### 10.7 NFR ↔ Verification ↔ Workflow Routing Table（必填 · 总览）

| NFR ID | Type | Status | Acceptance / Budget | Verification | Routed to |
| -------- | ------ | -------- | --------------------- | -------------- | ----------- |
| NFR-SEC-001 | Security | Active | <条件> | `<command>` or `/security-privacy-audit#锚点` | `/security-privacy-audit` |
| NFR-PERF-001 | Performance | Active | `p95 < 200ms` | `pnpm bench:<feature>` | `/performance-reliability-audit` |
| NFR-OBS-001 | Observability | Active | `alert: p95>500ms 5min` | runbook `../runbooks/<feature>.md` | `/observability-incident` |
| NFR-REL-001 | Release | Active | feature flag + rollback | `/release-deploy#锚点` | `/release-deploy` |
| NFR-UX-001 | UX/A11y | Active or N/A | WCAG-2.1-AA | `axe scan` | `/design-system-audit` or N/A |
| NFR-PLAT-001 | Platform | Active or N/A | <平台清单> | <兼容性矩阵> | `/desktop-release` or `/release-deploy` or N/A |

### 10.8 NFR DoD（Definition of Done · 必满足）

- [ ] §10.0 High-Risk Assessment 表已填（每行标 High / Low），且与 charter Goals / Out-of-Charter / Architectural Invariants 一致。
- [ ] 每个 High 行对应类至少 1 条 `Status: Active` NFR。
- [ ] 每个 Low 行对应类显式 `N/A: <理由>`，不留空。
- [ ] §10.7 路由表与 §10.1~§10.6 各条 NFR 一致（无遗漏 / 无外溢）。
- [ ] 高风险 NFR 已分流到对应专项 workflow（NFR-SEC → `/security-privacy-audit` 等），分流锚点存在或显式 `Routed to: N/A` + 理由。
- [ ] 每条 Active NFR 的 `Verification` 字段非空（命令、专项 workflow 锚点或 verification report 锚点之一）。
- [ ] Brownfield 模式下，每条 NFR 必有 `Delta Operation` 字段（Add / Modify / Replace / Deprecate / Preserve）；Greenfield 不强制此字段。
- [ ] `tasks.md` 至少有 1 个 Task 引用每条 Active NFR 作为 Verification 输入或 Routed-to 触发。

`R-CHK-EX-1.8` 校验本节完整性；详 `../../asset-quality-gates/references/checks-catalog.md §3.1`。

## 11. Constraints

- 必须 / 不得 / 受限于 ...

## 12. Open Questions

- Q1: ...

## 13. Critical Assumptions Summary

- A1: <假设> · Confidence: high|mid|low · Validation: <如何验证>
- 或填 `N/A: <说明>`

## 14. Approval

- Status: Draft | Approved | Needs Changes
- Notes: <用户原话 或 AI-DRI auto-approved 留痕，详 `cross-cutting.md §2.3`>
- Timestamp: <ISO 8601>
