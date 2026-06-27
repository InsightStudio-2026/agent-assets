# 团队协作就绪协议 (Collaboration Readiness Protocol)

## 1. 目标

验证新 agent / 新开发者不仅能首次跑通，还能在多人、多 agent、长期协作场景中安全接手、恢复上下文、理解质量门、识别风险标签，并知道何时使用 CI / code health / scope guard / operational learnings。

## 2. Readiness Signals

| 信号 ID (Signal ID) | 信号 (Signal) | 事实源 | PASS 标准 | FAIL 信号 | 路由 (Route) |
| ----------- | -------- | -------- | ----------- | ----------- | ------- |
| CR-R1 | CI Gate Awareness | `/ci-quality-gates` / CI config / README | 新 agent 能找到 required checks 与失败分类 | 不知道 PR 必跑哪些检查 | `/ci-quality-gates` |
| CR-R2 | Code Health Awareness | `/code-health-dashboard` / health artifact | 能找到 lint / typecheck / test / coverage / trend 状态 | 质量信号分散且无 dashboard | `/code-health-dashboard` |
| CR-R3 | Issue Risk Labels | `../../tasks-to-issues/protocols/risk-label-protocol.md` + issue template | issue 明示 `risk:*` / `needs:*` / `afk-*` | AFK/HITL 判定无依据 | `/tasks-to-issues` / `/issue-triage` |
| CR-R4 | Session Recovery | `session-context` skill / artifacts | 能保存和恢复目标、文件、决策、阻塞、验证状态 | 中断后只能靠聊天记忆 | `session-context` |
| CR-R5 | Operational Learnings | `operational-learnings` skill / artifacts | 环境坑、测试坑、命令差异可记录、prune、promote | 同一坑反复出现无沉淀 | `operational-learnings` |
| CR-R6 | Scope Guard | `scope-guard` skill / task plan | Allowed / Forbidden Paths 与扩边门清楚 | 简单任务顺手扩 scope | `scope-guard` |
| CR-R7 | Windows / PowerShell Continuity | README / scripts / TTHW output | 命令不用 `&&`，写文件指定 UTF-8，路径可在 Windows 表达 | shell 方言混用 | direct docs fix / `/repo-safety-setup` |

## 3. Collaboration Matrix

| 角色 (Persona) | 首要需求 (First Need) | 必需证据 (Required Evidence) | 判定通过标准 (PASS) |
| --------- | ------------ | ------------------- | ------ |
| New AFK agent | 接 issue 后执行 | issue risk labels + agent brief + scope guard | 知道可改范围与 gate |
| New developer | clone 后跑通 | TTHW + CI required checks + troubleshooting | 能本地复现 CI 基线 |
| Maintainer | 中断恢复 | session context + operational learnings | 能判断下一步与历史坑 |
| Release owner | 发布前质量确认 | code health + CI + release readiness | 知道缺口 route |

## 4. Output Table

| 检查项 (Check) | 状态 (Status) | 事实依据 (Evidence) | 质量缺口 (Gap) | 路由 (Route) |
| ------- | -------- | ---------- | ----- | ------- |
| CI Gate Awareness | PASS / FAIL / N/A | `<path>` | `<gap>` | `<route>` |
| Code Health Awareness | PASS / FAIL / N/A | `<path>` | `<gap>` | `<route>` |
| Issue Risk Labels | PASS / FAIL / N/A | `<path>` | `<gap>` | `<route>` |
| Session Recovery | PASS / FAIL / N/A | `<path>` | `<gap>` | `<route>` |
| Operational Learnings | PASS / FAIL / N/A | `<path>` | `<gap>` | `<route>` |
| Scope Guard | PASS / FAIL / N/A | `<path>` | `<gap>` | `<route>` |
| Windows / PowerShell Continuity | PASS / FAIL / N/A | `<path>` | `<gap>` | `<route>` |

## 5. 判定

| 条件 | 状态与路由 (State / Route) |
| ------ | --------------- |
| CR-R1~R7 全 PASS 或有明确 N/A | `/developer-experience-audit:COLLABORATION_READINESS_VERIFIED` |
| CI / local command surface 缺口 | `/ci-quality-gates` 或 `/repo-safety-setup` |
| risk labels / AFK-HITL 缺口 | `/tasks-to-issues` 或 `/issue-triage` |
| recovery / learnings / scope 缺口 | 对应 skill 或 direct asset maintenance |

## 6. 禁止项

| 禁止项 | 原因 |
| -------- | ------ |
| 不把 collaboration readiness 当 CI 绿灯 | CI 结果归 `/ci-quality-gates` |
| 不把 session context 当权威事实源 | 只恢复会话，不替代 spec / issue |
| 不把 operational learnings 直接升级为规则 | promote 需用户批准 |
| 不把 scope guard 当 spec | 只约束本轮编辑边界 |
