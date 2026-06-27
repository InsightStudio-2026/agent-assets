# Readiness Dashboard · /release-deploy 发布就绪信号事实源

> **本文是 `/release-deploy` workflow 的 Readiness Dashboard 信号字典**。所有 R-RDY-* 信号在此定义；入口 workflow 与报告模板按 ID 引用，不重复事实。
> 本文档自身遵循结构化规则表 + ID 体系格式规范（入口骨架 + 支撑文档分离 + 零 ASCII 流程图）。

---

## 0. 定位与索引

### 0.1 文档定位

- 10 类 readiness 信号字典；与 `release-deploy.md` Phase 2 Readiness Dashboard 项零漂移。
- 不是流程指南；流程见 `release-deploy.md` Phase 2 Readiness。
- 每个 R-RDY-* 给：信号名 / 事实源 / 红绿判定 / 缺口分流路由 / 严重性。

### 0.2 ID 命名空间

- `R-RDY-1~10`：10 类 readiness 信号。
- 红绿判定二值；不允许"中间色"伪装通过。
- 任一红 → `release-deploy:READINESS_BLOCKED` + 路由对应上游 workflow。
- 全部绿 → `release-deploy:READINESS_DASHBOARD_GREEN`，进入 Phase 3。

---

## 1. 10 类 Readiness 信号

| 规则 ID (Rule ID) | 信号名 | 事实源 | 红判定 | 缺口分流路由 | 严重性 |
| --------- | -------- | -------- | -------- | -------------- | -------- |
| `R-RDY-1` | Spec Completion | `docs/specs/<feature-slug>/tasks.md` Status 列；feature 必须全 Done | 任一 Task 非 Done / Blocked / Deferred / Unverifiable | `/specs-execute` 或 `/specs-write` 修订 | High |
| `R-RDY-2` | Task Verification | 每个 Done Task 的 `Verification:` 字段 + `artifacts/` 实际文件 | Verification 缺 / 命令未跑 / 输出未保留 | `/specs-execute` 重跑验证 | High |
| `R-RDY-3` | Review Outcome | `review` skill 报告 / PR review 结论 | review 报告缺 / 有未解决 blocker / Standards / Spec / Verification 三轴有红灯 | 让 reviewer 复核或回 `/specs-execute` | High |
| `R-RDY-4` | Test Result | `../protocols/deploy-protocol.md §2. Post-deploy Smoke（P-SMK-*）` 命令输出 | 任一 lint / typecheck / unit / integration / e2e 红 / flaky 不可解 | `/repo-safety-setup` 或 `/specs-execute` 修复 | High |
| `R-RDY-5` | Security Gate | `/security-privacy-audit` 输出的 security gate packet | secret 残留 / 依赖高危 CVE / PII 处理违规 / threat model 未签 | `/security-privacy-audit` 阻塞 release | Critical |
| `R-RDY-6` | Migration Gate | `/data-migration-safety` 输出的 migration gate packet | dry-run 缺 / backup 缺 / restore 未演练 / 不可回滚未明示 | `/data-migration-safety` 阻塞 release | Critical |
| `R-RDY-7` | Observability Gate | `/observability-incident` 输出的 observability gate packet | log / metric / trace / alert / runbook 信号面缺 | `/observability-incident` 补足后再放行 | High |
| `R-RDY-8` | Documentation Sync Status | README / AGENTS / CHANGELOG / release notes / 架构图 / 运行手册 vs diff | public surface 暴露但文档漂移 | 进入 Phase 4 Documentation Sync 修订 | Medium |
| `R-RDY-9` | Rollback Plan | `../protocols/deploy-protocol.md §4. Rollback（P-RBK-*）` + 本次 release 的 rollback-plan.md | rollback 步骤缺 / 命令未验证 / 不可回滚未前置告知用户 | 草拟 + 用户确认；不可回滚必须升级 `WAITING_DEPLOY_APPROVAL` 包含明示 | Critical |
| `R-RDY-10` | Performance Gate | `/performance-reliability-audit` 输出的 `<feature>/perf-audit/perf-gate-packet.md` | NFR-PERF-* Active 但 perf gate packet 缺 / baseline 缺 / budget violation 未 mitigation / BENCHMARK_BLOCKED / RWSE Gate（load test / SLA / capacity）未批 | `/performance-reliability-audit` 阻塞 release；canary 期超阈值倒序触发本 workflow 后必须重出 packet | High |

条件化 Browser QA 不新增 R-RDY 编号；当 release diff 影响 Web / WebView / 可视化关键路径时，它作为 Phase 7 smoke 子闸口读取 `../protocols/browser-qa.md`，失败映射到 `/release-deploy:SMOKE_FAILED`。

---

## 2. 红绿判定原则

| 原则 | 说明 |
| ------ | ------ |
| 二值判定 | 每个 R-RDY-* 只能 PASS / FAIL；不允许"基本通过"、"已知问题不影响"、"先发后补"等灰色状态 |
| 事实源唯一 | 每个信号引用唯一事实源（文件路径或 workflow 报告）；不读取过期快照 |
| 跨 workflow 不替代 | `R-RDY-5/6/7/10` 的 Critical / High 信号必须由对应专项 workflow 产出 packet；本 workflow 不替代判定 |
| 缺事实源 = 红 | 找不到事实源（文件不存在 / workflow 未跑）一律 FAIL，不能因"猜测合规"放行 |
| 文档同步可在本 workflow 内修 | `R-RDY-8` 是唯一可在本 workflow Phase 4 内修复的信号 |

---

## 3. 报告格式（Phase 2 输出）

```markdown
## 就绪度仪表盘 (Readiness Dashboard)

|  | 信号类型 (Signal) | 运行状态 (Status) | 事实依据 (Evidence) | 质量缺口 (Gap if any) | 跟踪路由 (Route) |  |
|  | -------- | -------- | ---------- | -------------- | ------- |  |
|  | R-RDY-1 规格完备度 (Spec Completion) | PASS / FAIL | <事实源路径或快照> | <缺项> | <路由> |  |
|  | R-RDY-2 任务完工验证 (Task Verification) | ... | ... | ... | ... |  |
|  | R-RDY-3 审查意见结论 (Review Outcome) | ... | ... | ... | ... |  |
|  | R-RDY-4 单元与集成测试 (Test Result) | ... | ... | ... | ... |  |
|  | R-RDY-5 安全隐私门禁 (Security Gate) | ... | ... | ... | ... |  |
|  | R-RDY-6 结构与数据迁移 (Migration Gate) | ... | ... | ... | ... |  |
|  | R-RDY-7 系统可观测性 (Observability Gate) | ... | ... | ... | ... |  |
|  | R-RDY-8 文档手册同步 (Documentation Sync) | ... | ... | ... | ... |  |
|  | R-RDY-9 发版回滚方案 (Rollback Plan) | ... | ... | ... | ... |  |
|  | R-RDY-10 性能可靠性门禁 (Performance Gate) | ... | ... | ... | ... |  |

## 综合就绪度结论 (Aggregate Verdict)

- 全项通过 (All PASS) → `/release-deploy:READINESS_DASHBOARD_GREEN`
- 任意失败 (Any FAIL) → `/release-deploy:READINESS_BLOCKED`
- 致命失败 (Critical FAIL) → 强制阻塞，必须先解决（不允许加注释跳过）

```

---

## 4. 边界与不检查项

| 类别 | 是否检查 | 理由 |
| ------ | --------- | ------ |
| 业务逻辑正确性 | 不检查 | 归 `/specs-execute` Verification + `review` |
| 代码风格 | 不检查 | 归 `/repo-safety-setup` |
| 用户体验细节 | 不检查 | 归 `review` skill / 设计审查 |
| 性能基准 | 部分（仅 R-RDY-4 e2e 性能；canary 比较归 Phase 7） | Readiness 只确认基线存在，不做 canary 比较 |
| 法律合规 / license | 不替代 | 归 `/security-privacy-audit` 或专项审计 |

---

## 5. 修订规则

- 本文修订必须同 PR 修订 `release-deploy.md` State 表（`READINESS_BLOCKED` / `READINESS_DASHBOARD_GREEN` 状态行）。
- R-RDY-* ID 一旦分配不得复用；废弃改 deprecated 标记。
- 新增 R-RDY-* 必须先在 `release-deploy.md` Phase 2 Readiness Dashboard 项同步事实源。
- 不引入"Warning"中间状态；保持二值红绿。
