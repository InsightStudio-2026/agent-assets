# Plan Completion Audit · /release-deploy 计划完成度审计

## 1. 定位

Plan Completion Audit 是 `/release-deploy` Phase 3 的条件化子闸口，用于证明 release candidate 的 spec / task / artifacts / diff / deferred work 已闭环。它不替代 `/specs-execute` 执行任务，只检查 release 前是否存在伪 Done、漏验证、artifact 外溢或 scope 越界。

## 2. 审计规则

| 规则 ID (Rule ID) | 检查项 | PASS 标准 | FAIL 信号 | 路由 |
| --------- | -------- | ----------- | ----------- | ------ |
| PCA-R1 | Task completion | release scope 内 required Task 全部 `Status: Done` | Pending / In Progress / Blocked / Deferred / Unverifiable | `/specs-execute` |
| PCA-R2 | Verification evidence | 每个 Done Task 有命令、结果、时间或 artifact 证据 | 只写“已验证”无输出 | `/specs-execute` |
| PCA-R3 | Artifacts alignment | tasks.md `Artifacts:` 声明与实际文件一致，无项目根 `reports/` 外溢 | 缺文件 / 多余散落产物 | `/specs-execute` |
| PCA-R4 | Scope diff | release diff 只包含 spec / tasks / approved docs 覆盖内容 | 越 scope 文件或公共契约未批准 | `/specs-write` 或 `/specs-execute` |
| PCA-R5 | Gate packet completeness | security / migration / observability / performance 等 required packet 齐 | R-RDY-* required packet 缺失 | 对应专项 workflow |
| PCA-R6 | Deferred work honesty | deferred 项有 owner、理由、风险和非阻塞依据 | 用 TODO / 后续优化掩盖 blocker | `READINESS_BLOCKED` |
| PCA-R7 | Version / changelog scope | release notes / changelog 只覆盖本 release candidate | 混入未来功能或历史重写 | Phase 4 Documentation Sync |

## 3. Required / Optional 判定

| 条件 | 子闸口状态 |
| ------ | ------------ |
| 用户明确要求 release / deploy / tag / publish | Plan Completion Audit required |
| release candidate 含 approved spec tasks | Plan Completion Audit required |
| 纯本地原型 / 无 release candidate | Plan Completion Audit N/A |
| 只生成草稿 release notes，不发布 | Plan Completion Audit optional，但不得宣称 release ready |

## 4. 输出模板

```markdown
## 发版计划完工度审计 (Plan Completion Audit)

|  | 审计检查项 (Check) | 运行状态 (Status) | 事实依据 (Evidence) | 质量缺口 (Gap) | 跟踪路由 (Route) |  |
|  | ------- | -------- | ---------- | ----- | ------- |  |
|  | PCA-R1 任务完工状态 (Task completion) | PASS / FAIL | <tasks.md> | <gap> | <route> |  |
|  | PCA-R2 完工验证证据 (Verification evidence) | PASS / FAIL | <commands/artifacts> | <gap> | <route> |  |
|  | PCA-R3 交付产物对齐 (Artifacts alignment) | PASS / FAIL | <artifacts path> | <gap> | <route> |  |
|  | PCA-R4 代码差异范围 (Scope diff) | PASS / FAIL | <diff summary> | <gap> | <route> |  |
|  | PCA-R5 门禁归档信息包 (Gate packets) | PASS / FAIL | <packet list> | <gap> | <route> |  |
|  | PCA-R6 延期工作规整 (Deferred work) | PASS / FAIL | <deferred list> | <gap> | <route> |  |
|  | PCA-R7 变更日志范围 (Changelog scope) | PASS / FAIL | <release notes> | <gap> | <route> |  |

综合结论 (Aggregate): 全部通过 (PASS) → 推进至步进 4 (continue Phase 4) / 任意失败 (FAIL) → `/release-deploy:PLAN_COMPLETION_AUDIT_FAILED`
```

## 5. 判定

| 条件 | Workflow State |
| ------ | ---------------- |
| PCA-R1~R7 全 PASS | `/release-deploy:READINESS_DASHBOARD_GREEN` 可继续 Phase 4 |
| 任一 FAIL 且可由执行修复 | `/release-deploy:PLAN_COMPLETION_AUDIT_FAILED` → `/specs-execute` |
| scope / spec 契约缺陷 | `/release-deploy:PLAN_COMPLETION_AUDIT_FAILED` → `/specs-write` |
| required gate packet 缺失 | `/release-deploy:READINESS_BLOCKED` → 对应专项 workflow |

## 6. 禁止项

| 禁止项 | 原因 |
| -------- | ------ |
| 不把部分 Done 当 release ready | release candidate 必须可证据化 |
| 不用 release notes 掩盖未完成 Task | release notes 不是 task 状态事实源 |
| 不把 artifact 缺失降级成 warning | release 证据链缺口会破坏回滚与审计 |
| 不允许 “known issue but ship anyway” 绕过 Gate | 必须有 Gate 批准或显式非阻塞依据 |
