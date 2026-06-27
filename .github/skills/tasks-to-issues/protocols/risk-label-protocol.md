# 任务风险与发布标签协议 (Risk Label Protocol)

## 1. 规范风险标签 (Canonical Risk Labels)

| 标签 (Label) | 涵义 (Meaning) | 触发条件 (Trigger) | 推荐路由 (Required Route) |
| ------- | --------- | --------- | ---------------- |
| `risk:security` | 权限、认证、密钥、PII、外部攻击面风险 | NFR-SEC-*/ DSN-SEC-* / secrets / OAuth / webhook | `/security-privacy-audit` |
| `risk:data` | schema、migration、backfill、数据修复、批量删除风险 | NFR-REL migration / DSN-DB-*/ migration task | `/data-migration-safety` |
| `risk:release` | deploy、feature flag、rollback、用户可见发布风险 | NFR-REL-* / release task / rollback complexity | `/release-deploy` |
| `risk:perf` | 性能、容量、冷启动、bundle、查询路径风险 | NFR-PERF-* / benchmark / budget | `/performance-reliability-audit` |
| `risk:ux` | 关键 UI、A11y、响应式、设计系统风险 | NFR-UX-*/ DSN-UI-* / visual QA | `/design-system-audit` |
| `needs:human-decision` | 需要产品、架构、法律、审美或范围裁决 | unresolved decision / user preference / legal ambiguity | `ready-for-human` |
| `needs:production-access` | 需要生产权限、真实账号、证书、付费资源或外部副作用 | production env / store publish / signing / secrets | `ready-for-human` |
| `afk-safe` | 可由 AFK agent 独立完成 | context complete + no external decision + no real-world side effect | `ready-for-agent` |
| `afk-unsafe` | 不适合 AFK 独立完成 | missing context / high-risk gate / external access / human decision | `ready-for-human` |

## 2. 标注规则 (Labeling Rules)

| 规则 ID (Rule ID) | 条件 | 标签 (Labels) | 备注 (Notes) |
| --------- | ------ | -------- | ------- |
| R-TTI-RISK-1 | Task 触及 NFR-SEC-* / secrets / auth / PII | `risk:security`, `afk-unsafe` unless gate packet exists | 标签不替代 `/security-privacy-audit` |
| R-TTI-RISK-2 | Task 触及 migration / schema / backfill / destructive data | `risk:data`, `afk-unsafe` unless packet exists and task is local-only | 标签不替代 `/data-migration-safety` |
| R-TTI-RISK-3 | Task 触及 deploy / rollback / feature flag / release config | `risk:release`, `afk-unsafe` if user-visible | 标签不授权 release |
| R-TTI-RISK-4 | Task 触及 perf budget / benchmark / capacity / cold start | `risk:perf` | 需要 perf gate 时标 `afk-unsafe` |
| R-TTI-RISK-5 | Task 触及关键 UI / A11y / visual QA | `risk:ux` | 设计裁决未定时标 `needs:human-decision` |
| R-TTI-RISK-6 | Task 需要生产账号、证书、商店后台、真实 API 写入 | `needs:production-access`, `afk-unsafe` | 不允许 AFK 自行获取权限 |
| R-TTI-RISK-7 | Task 有未决产品 / 架构 / legal / 品牌审美裁决 | `needs:human-decision`, `afk-unsafe` | 先 HITL |
| R-TTI-RISK-8 | Task 上下文完整、无外部权限、无未决裁决、验证明确 | `afk-safe` | 可配 `ready-for-agent` |

## 3. Issue 标签组合模板 (Issue Label Set Template)

| 源任务 (Source Task) | 风险标签 (Risk Labels) | 自动/人工模式 (AFK/HITL) | 决策依据 (Rationale) | 触发门禁/路由 (Required Gate / Route) |
| ------------- | ------------- | ---------- | ----------- | ----------------------- |
| TASK-### | `risk:*`, `needs:*`, `afk-*` | AFK / HITL | `<why>` | <workflow or N/A> |

## 4. 验收条件 (DoD)

| 检查项 (Check) | 合格标准 (PASS) |
| ------- | ------ |
| Risk labels | 每个 issue 至少有 `afk-safe` 或 `afk-unsafe`，风险命中时有 `risk:*` |
| AFK/HITL rationale | 每个 HITL / AFK 判定有一句依据 |
| Gate Required | 命中专项风险时 issue body 明示 required gate / route |
| Source authority | Issue body 引用源 Task，不把 label 当第二事实源 |

## 5. 禁止项

| 禁止项 | 原因 |
| -------- | ------ |
| 风险标签不替代专项 workflow | 标签只是路由信号，不是审计结果 |
| `afk-safe` 不授权真实世界副作用 | 生产、权限、签名、发布仍需用户批准 |
| 不用 `risk:*` 模糊阻塞所有任务 | 标签必须有触发依据 |
