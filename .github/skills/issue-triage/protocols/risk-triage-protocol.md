# 风险分流协议 (Risk Triage Protocol)

## 1. 目的

`/issue-triage` 使用本文判断 issue 是否可进入 `ready-for-agent`，或必须进入 `ready-for-human` / 专项工作流 (workflow)。风险标签来自 `locales/zh-CN/.github/skills/tasks-to-issues/risk-label-protocol.md`，但分流 (triage) 结果仍由跟踪器标签 (tracker label) 与分流评阅 (triage comment) 表达；issue 不是规格说明书 (spec) 的第二事实源。

## 2. AFK / HITL 判定规则

| 规则 ID (Rule ID) | 条件 | 跟踪器状态 (Tracker State) | 必需标签 (Required Labels) | 必需路由 (Required Route) |
| --------- | ------ | --------------- | ----------------- | ---------------- |
| R-ITR-AFK-1 | 上下文完整、验收清楚、无外部权限、无未决裁决、无真实世界副作用 | `ready-for-agent` | `afk-safe` | 不适用 (N/A) |
| R-ITR-AFK-2 | 信息不足、复现不足、验收不可测 | `needs-info` | `afk-unsafe` | 报告人 / 维护者 (reporter / maintainer) |
| R-ITR-AFK-3 | 需要产品、架构、法律、品牌或审美裁决 | `ready-for-human` | `needs:human-decision`, `afk-unsafe` | 人工裁决 (human decision) |
| R-ITR-AFK-4 | 需要生产权限、真实账号、证书、商店后台、付费资源 | `ready-for-human` | `needs:production-access`, `afk-unsafe` | 人工 / 发布负责人 (human / release owner) |
| R-ITR-AFK-5 | 涉安全、权限、认证、PII、secrets、外部攻击面 | 除非安全信息包已存在，否则为 `ready-for-human` (unless security packet exists) | `risk:security`, `afk-unsafe` | `/security-privacy-audit` |
| R-ITR-AFK-6 | 涉 schema、migration、backfill、批量删除、数据修复 | 除非数据门禁包存在且任务仅限本地，否则为 `ready-for-human` (unless data gate packet exists and task is local-only) | `risk:data`, `afk-unsafe` | `/data-migration-safety` |
| R-ITR-AFK-7 | 涉 deploy、rollback、feature flag、用户可见发布 | `ready-for-human` | `risk:release`, `afk-unsafe` | `/release-deploy` |
| R-ITR-AFK-8 | 涉性能预算、容量、benchmark、bundle、冷启动 | 有条件 (conditional) | `risk:perf` | 若高风险路由至 (if high risk) `/performance-reliability-audit` |
| R-ITR-AFK-9 | 涉关键 UI、A11y、响应式、设计系统、视觉裁决 | 有条件 (conditional) | `risk:ux` | 若设计未确定路由至 (if design not settled) `/design-system-audit` |

## 3. ready-for-agent 必备字段

| 审核项 (Field) | 合格标准 (PASS 标准) |
| ------- | ----------- |
| 信息源/上下文 (Source / context) | issue body 或 agent brief 可定位到上游任务 / 需求 / 复现事实 |
| 验收条件/AC (Acceptance criteria) | 可验证，不依赖主观判断 |
| 不做的范围 (Out of scope) | 明确不做什么 |
| 风险标签 (Risk labels) | 至少有 `afk-safe`，且无未解释的 `risk:*` / `needs:*` |
| 触发门禁要求 (Gate Required) | `N/A` 或专项 gate packet 已存在且引用明确 |
| 权限与资源限制 (Permissions) | 不需要生产、真实账号、证书或外部付费资源 |

## 4. Agent Brief 风险段模板

```markdown
**风险标签 (Risk labels):** <risk:* / needs:* / afk-*>

### 人机协同与自决判定依据 (AFK/HITL rationale):
<为什么能或者不能由 AFK 代理人独立执行该任务 (why this can or cannot be handled by an AFK agent)>

### 强控制品质门禁要求 (Gate Required):
<所需专项工作流路由，若无则写 N/A (specialized workflow route or N/A)>
```

## 5. 冲突处理

| 冲突 (Conflict) | 动作 (Action) |
| ---------- | -------- |
| `ready-for-agent` + `afk-unsafe` | 报告冲突；除非维护者确认覆盖，否则推荐 `ready-for-human` (report conflict; recommend `ready-for-human` unless maintainer confirms override) |
| `ready-for-agent` + `needs:production-access` | 阻断；生产权限不能是 AFK-safe (block; production access cannot be AFK-safe) |
| `ready-for-agent` + unresolved `risk:security` / `risk:data` / `risk:release` | 在就绪前路由至专项工作流 (route to specialized workflow before ready) |
| 存在多个状态标签 (Multiple state labels) | 写入前停止并询问维护者 (stop and ask maintainer before write) |
| 用户显式覆盖 (User explicit override) | 应用前显示风险冲突并要求确认 (show risk conflict and require confirmation before applying) |

## 6. 禁止项

| 禁止项 | 原因 |
| -------- | ------ |
| 不用 `ready-for-agent` 绕过专项 workflow | 风险标签不是审计结论 |
| 不把 `afk-safe` 当生产授权 | AFK readiness 只代表执行适配性 |
| 不让 issue brief 覆盖 spec / task 权威 | issue 只投影事实源 |
