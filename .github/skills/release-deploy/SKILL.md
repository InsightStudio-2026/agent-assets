---
name: release-deploy
description: 发布部署闭环：从"代码完成"到"目标环境可用"的发布、smoke、canary、回滚闸口；生产 / 用户可见 / 付费 / 迁移 / 外部副作用必须用户批准，不伪装 Done。
argument-hint: "要发布什么版本到哪个环境？"
disable-model-invocation: true
---


# /release-deploy · 发布部署闭环

**定位**：把"代码已实现"到"目标环境真实可用"之间的全部副作用（version bump / changelog / migration / deploy / smoke / canary / 文档同步 / rollback）当作一个可追溯、可审计、不可绕过的闸口流程。

**边界**：只管发布层副作用与可追溯证据；不替代 `/specs-execute` 实现验证、不替代 `/security-privacy-audit` 安全门、不替代 `/data-migration-safety` 数据闸口、不替代 `/observability-incident` 事故响应；这四个 workflow 的 gate packet 是本 workflow 的**前置 readiness 信号**而非内部子任务。

**斜杠命令**：`/release-deploy`

**配对前置 workflow**：`/specs-execute`、`review` skill、`/security-privacy-audit`、`/data-migration-safety`、`/observability-incident`、`/asset-quality-gates`（如发布资产层变更）。

---

## 懒加载契约

- **MUST read**: `./decision-matrix.md`
- 开始判定或执行 Phase 流程前，必须完整懒加载上述细节。

---

## 1. 伴随文档

| 文档 | 角色 | 何时读 |
| ------ | ------ | -------- |
| `references/readiness-dashboard.md` | Readiness 10 类信号 + 阅读事实源 + 红绿判定 | Phase 2 |
| `protocols/plan-completion-audit.md` | required tasks / Verification / artifacts / diff scope / deferred work 审计 | Phase 3 |
| `protocols/deploy-protocol.md` | dry-run / deploy / smoke / canary / rollback 命令规范 + 证据要求 | Phase 5-7 |
| `protocols/documentation-sync.md` | Diataxis 覆盖 + CHANGELOG 边界 + 文档生成边界 | Phase 4 |
| `protocols/browser-qa.md` | Web / WebView 真实浏览器 smoke、viewport、console、network、A11y 证据 | Phase 7（条件化） |
| `../specs-write/protocols/gate-dag-protocol.md` | Gate / DAG ID 横切协议事实源 | State 表 + Phase 5 装配 packet |
| `../specs-write/protocols/entry-decision-tree.md §7.5 / §7.6` | R-AUDIT-*/ R-RETURN-* 路由 | State 表分流 / Phase 3 失败回切 |

---

## 2. 阶段骨架（细节见伴随文档）

每个 Phase 入口的 **MUST read**指令是硬规则——不读 = 视为违反该 Phase 的部署与发布质量防御。

### 阶段 1 — 版本分支探测**MUST read**`references/readiness-dashboard.md`

识别 release candidate；判定 `/release-deploy:NO_RELEASE_CANDIDATE` / `/release-deploy:RELEASE_CANDIDATE_DETECTED`。

### 阶段 2 — 发布就绪大盘评估**MUST read**`references/readiness-dashboard.md`

按 `readiness-dashboard.md` 收集 10 类信号；任一红灯 → `/release-deploy:READINESS_BLOCKED` 分流上游。

### 阶段 3 — 发布计划完整度审计**MUST read** `protocols/plan-completion-audit.md`

按 `protocols/plan-completion-audit.md` 核验 required Task Done + Verification + Artifacts 一致性 + diff 不越 scope + deferred work 诚实性 + gate packet completeness；**运行并核验 Frontmatter 物理完整性**（运行 `powershell -ExecutionPolicy Bypass -File .\verify-completeness.ps1 -Update`，若不通过则直接阻断）；失败 → `/release-deploy:PLAN_COMPLETION_AUDIT_FAILED` 回切 `/specs-execute` / `/specs-write` 或对应专项 workflow（按 `R-RETURN-*` 与 R-RDY-*）。

### 阶段 4 — 部署与发版文档同步

**MUST read**`protocols/documentation-sync.md`。

按 `documentation-sync.md` 检查 Diataxis 覆盖 + README / AGENTS / CHANGELOG / release notes / 架构图 / 运行手册漂移；事实更新可自动；叙事 / 哲学 / 安全模型 / 大段删除升级 `DOCUMENTATION_SYNC_BLOCKED_BY_NARRATIVE`。

### 阶段 5 — 方案起草与演练（Dry-run）**MUST read** `protocols/deploy-protocol.md`

草拟 release-plan / deploy-checklist / rollback-plan / smoke 计划 + 装配 `HG-RELEASE-*` packet（F-HG-1~8）；首次真实发布 / 全新环境 / 关键平台变更必须 dry-run；按 `deploy-protocol.md`。

### 阶段 6 — 发布执行与部署

**MUST read**`protocols/deploy-protocol.md`。

仅在 `/release-deploy:APPROVED_TO_DEPLOY` 后执行；按 `deploy-protocol.md` 命令规范；不扩范围；失败 → `/release-deploy:DEPLOY_FAILED` 或 `/release-deploy:ROLLBACK_REQUIRED`。

### 阶段 7 — 冒烟测试与金丝雀观测**MUST read**`protocols/deploy-protocol.md` + `protocols/browser-qa.md`（条件化）

按 `deploy-protocol.md` post-deploy 段执行 health / smoke / canary；如 release diff 影响 Web / WebView / 可视化关键路径，另按 `protocols/browser-qa.md` 执行条件化 Browser QA；性能数据 vs baseline 必须可比较；失败 → `/release-deploy:SMOKE_FAILED` / `/release-deploy:CANARY_REGRESSION_DETECTED`。

### 阶段 8 — 发布回滚（条件触发）**MUST read**`protocols/deploy-protocol.md`

仅按已展示 rollback-plan 执行；`migration` 不可回滚必须前置告知用户；执行后 `/release-deploy:ROLLED_BACK` + 决定是否启 `/observability-incident`。

### 阶段 9 — 发版总结报告与收口**MUST read** `protocols/deploy-protocol.md`

生成 release-report.md（含 plan + dry-run + deploy + smoke + canary + 文档 sync + rollback 状态 + Readiness 快照）；进入 `/release-deploy:RELEASE_DONE` 或 `/release-deploy:POST_DEPLOY_REGRESSION_NEEDS_INCIDENT`。

---

## 3. 输出格式

```markdown
## 发布与部署报告 (Release Deploy Report)

## 工作流状态 (Workflow State)

- State: /release-deploy:`<state>`

## 发布候选版本 (Release Candidate)

- 版本 / Tag / 分支 (Version / tag / branch):
- 目标环境 (Target environment):
- 规格 Feature Slug + 任务节点 (Spec slug + Task DAG node):

## 门禁/节点状态 (Gate / DAG Status)

- HG-RELEASE-{slug}-{env}-{version}: <S-HG-* 状态>
- HG-IRREV-* 命中: <列出激活的 IRREV 子项 或 N/A>
- HG-SEC-* / HG-INCIDENT-* candidate: <如适用>
- DAG-N-RELEASE-{slug}-{version}: <node 状态>
- DAG-E-RBK: <未激活 / 激活 → DAG-N-ROLLBACK-RELEASE-*>

## 就绪度仪表盘 (Readiness Dashboard)

- 规格 / 任务完工 / 审查 / 测试 / 安全 / 迁移 / 可观测性 / 文档 / 回滚 / 性能 (spec / task completion / review / test / security / migration / observability / documentation / rollback / performance): <每项绿 / 红 + 缺项详情>

## 计划完工情况审计 (Plan Completion Audit)

- 必需任务完工 (required Task Done): <PASS / FAIL>
- 验证情况 (Verification): <PASS / FAIL>
- 交付产物一致性 (Artifacts vs Artifacts 声明): <PASS / FAIL>
- 差异越权 (diff 越 scope): <无 / 列文件>
- 暂缓/无法本地验证的工作 (deferred / unverifiable work): <无 / 列项 + route>
- 必需门禁信息包 (required gate packets): <PASS / FAIL + 缺项>

## 文档同步状态 (Documentation Sync)

- Diataxis 覆盖: <reference / how-to / tutorial / explanation 各项>
- CHANGELOG / README / AGENTS / 运行手册 / 架构图: <已同步 / 漂移 + 文件>
- 战略级变更触发: <无 / 列叙事 / 哲学 / 安全模型 / 大段删除项>

## 部署方案 (Deploy Plan)

- 平台 / URL / 健康检查端点 (platform / URL / health endpoint):
- 部署 / 状态查询命令 (deploy / status 命令):
- 预演状态 (dry-run 状态): <PASS / FAIL / N/A>
- 回滚方案 (rollback-plan) 摘要 + 不可回滚声明:

## 部署结果 (Deploy Result)

- 命令输出:
- 状态过渡: DEPLOYING → <DEPLOYED_PENDING_SMOKE / DEPLOY_FAILED>

## 冒烟测试/金丝雀验证 (Smoke / Canary)

- 健康检查结果 (health check):
- 冒烟测试关键路径 (smoke 关键路径):
- 浏览器 QA 验证 (browser QA - if required): <PASS / FAIL / N/A + evidence>
- 金丝雀指标 vs 基线 (canary metric vs baseline) (p95 / LCP / CLS / INP / 资源数 / 总传输量):
- 控制台/网络请求错误 (console / network errors):

## 部署回滚 (Rollback - 如适用)

- 触发条件 + rollback 命令输出 + 是否数据可回滚

## 授权边界 (Authorization Boundary)

- 路由动作 (Route Action): <CONTINUE_IN_WORKFLOW | WAIT_FOR_USER | CONFIRMED_ACTION | REPORT_AND_STOP>
- 授权来源 (Confirmation source): <用户原话 或 N/A>
- 授权范围 (Authorized scope): <本次目标环境 + version + 命令 + rollback-plan>
- 未授权范围 (Not authorized): <其他环境 / 其他版本 / 后续外部副作用 / 下游 workflow>

## 推荐下一步路由 (Recommended Next Route)

- <continue Phase | /specs-execute | /specs-write | /security-privacy-audit | /data-migration-safety | /observability-incident | /project-steward>

## 恢复/返航契约 (Return Contract)

- 目标路由 (Target route):
- 准入输入 (Entry input):
- 未决就绪缺口/未填满信息包字段 (Outstanding Readiness gaps / open packet fields):

```

---

## 4. 禁用行为

- 不在 `/release-deploy:READINESS_BLOCKED` / `/release-deploy:PLAN_COMPLETION_AUDIT_FAILED` / `/release-deploy:DRY_RUN_FAILED` / 未 `/release-deploy:APPROVED_TO_DEPLOY` / 未前置告知不可回滚 migration 时执行真实 deploy。
- 不把 `/release-deploy:APPROVED_TO_DEPLOY` 继承到其他环境 / 版本 / 后续外部副作用；canary 扩量同样需新批准。
- 不把 `deploy succeeded` 当 `/release-deploy:RELEASE_DONE`；性能数据必须可比较，不是单次截图。
- 不在 CHANGELOG 重写 / 删除 / 重排历史 entry；只做事实修正和措辞润色。
- 不在 `docs/` 顶层滥增；不写泛泛教程；不绕过用户裁决自动改叙事 / 哲学 / 安全模型 / 大段删除。
- 不替代 `/security-privacy-audit` / `/data-migration-safety` / `/observability-incident` 内部判断；只消费它们的 gate packet 作为 Readiness 信号。
- 不修改 spec / task / L1 SSOT / standards；只读消费它们；如发现需求 / 实现 / 架构缺陷 → 按 `R-RETURN-*` 回切。

## 5. 快速自检清单

报告前自检：

- [ ] 是否确认并读取了正确的 Release Candidate（版本、分支、环境）？
- [ ] 收集的 10 类 Readiness 信号是否已全部为绿灯（无未决红灯）？
- [ ] 计划审计是否核验通过了所有 Task、Verification 以及 Artifacts 一致性？
- [ ] 部署方案（含 dry-run、smoke、canary、rollback-plan）是否已装配完整，并获得了用户批准？
- [ ] 部署后是否执行了 Smoke/Canary 验证，并核对了性能数据基线？
- [ ] 若发生异常需要 Rollback，是否完全按照已批准的回滚方案执行？
- [ ] 所有物理文档和资产文件的 Frontmatter 物理完整性是否已刷新校验（跑 `verify-completeness.ps1 -Update` 且通过）？

## 支撑资源

- [browser-qa.md](./protocols/browser-qa.md)
- [decision-matrix.md](./references/decision-matrix.md)
- [deploy-protocol.md](./protocols/deploy-protocol.md)
- [documentation-sync.md](./protocols/documentation-sync.md)
- [plan-completion-audit.md](./protocols/plan-completion-audit.md)
- [readiness-dashboard.md](./references/readiness-dashboard.md)
