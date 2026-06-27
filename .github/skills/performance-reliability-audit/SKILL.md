---
name: performance-reliability-audit
description: 性能与可靠性审计：建立 baseline、设定 budget、检测 regression、跑 load test、规划 capacity、定义 SLA；从 NFR-PERF-* 取 spec 上游契约，作为 release-deploy 双向门 + canary 反馈环；产出 perf gate packet；生产 load test / SLA 变更 / capacity 上限下调必须用户批准。
argument-hint: "要审计哪个系统的性能与可靠性？"
disable-model-invocation: true
---


# /performance-reliability-audit · 性能与可靠性审计

**定位**：把 latency / throughput / memory / bundle-size / cold-start / DB-query-count / capacity / SLA 的审计串成可追溯证据链；产出 perf gate packet，作为 `/release-deploy` `R-RDY-10 Performance Gate` 的事实源；与 release canary 形成反馈环（生产 perf metric 倒序触发本 workflow 重审）。

**边界**：只做性能 / 可靠性 baseline / budget / regression / load test / capacity / SLA 审计；不替代 `/specs-execute` 实现验证、不替代 `/observability-incident` runbook / alert 响应、不替代 `/release-deploy` 发布动作、不替代 `/bug-audit` 性能 bug 根因分析；性能修复本身归 `/specs-execute` 或 `/bug-audit`，本 workflow 只识别 + 出 mitigation task。

**斜杠命令**：`/performance-reliability-audit`

**配对前置 / 下游**：上游消费 spec NFR-PERF-* 契约 / requirements §10.2 / design 性能假设 / architecture-audit 性能取舍；下游产出 perf gate packet 给 `/release-deploy` R-RDY-10、mitigation task 给 `/specs-write` / `/specs-execute`、性能 regression 处置给 `/bug-audit`、容量 / SLA 调整给 `/architecture-audit`。

---

## 懒加载契约

- **MUST read**: `./decision-matrix.md`
- 开始判定或执行 Phase 流程前，必须完整懒加载上述细节。

---

## 1. 伴随文档

| 文档 | 角色 | 何时读 |
| ------ | ------ | -------- |
| `protocols/audit-protocol.md` | 8 Phase 细节 + Trigger Mode 判定 + Phase 跳过规则 | Phase 1 全程 |
| `references/perf-checks-catalog.md` | 性能检查项规则字典（R-CHK-PERF-*：baseline / budget / regression / cold-start / DB-query / bundle） | Phase 2-7 |
| `protocols/baseline-store-protocol.md` | 双部位存储（spec artifacts + 集中 perf-baseline/）+ 版本化 + 同步 + 跨 release 比对 | Phase 2 |
| `protocols/load-test-protocol.md` | 生产 / preprod / staging load test + RWSE Gate + k6 / artillery / locust 模板 | Phase 4 |
| `protocols/capacity-planning-protocol.md` | 容量上限定义 / 扩容触发 / 上限下调 RWSE Gate / 多区 / 多租户隔离容量 | Phase 5 |
| `protocols/sla-protocol.md` | SLA 定义 / 上调下调 RWSE Gate / 外部承诺同步 / SLO ↔ SLA 区分 | Phase 6 |
| `protocols/canary-feedback-protocol.md` | 与 `/release-deploy` canary 期实时 metric 反馈环 + 倒序触发本 workflow 规则 | Phase 7 + Phase 8 |
| `protocols/bug-audit-handoff-protocol.md` | 与 `/bug-audit` 性能 regression 联调（接 + 出 mitigation task）+ 倒序触发 | Phase 1 + Phase 7 |
| `../specs-write/protocols/gate-dag-protocol.md` | Gate / DAG ID 横切协议事实源 | State 表 + Phase 8 装配 packet |
| `../specs-write/protocols/entry-decision-tree.md §7.6` | R-RETURN-* 路由（mitigation 回切） | Phase 8 closeout |

---

## 2. 阶段骨架（细节见伴随文档）

每个 Phase 入口的 **MUST read**指令是硬规则——不读 = 视为违反该 Phase 的性能与可靠性防御。

### 阶段 1 — 审计范围与触发器探测**MUST read** `protocols/audit-protocol.md`

对齐审计范围；按 §0.4 Trigger Mode Matrix 判定触发模式（spec-gate / scheduled / bug-handoff / canary-feedback / release-gate / user-explicit）；从 spec §10.2 拉 NFR-PERF-* 契约（metric / budget / measure command / baseline ref / routed-to）；输出 `<slug>/perf-audit/trigger-mode.md` + `<slug>/perf-audit/charter.md`。Trigger Mode 缺契约 → `/performance-reliability-audit:PERF_SCOPE_MISSING` 回 `/specs-write`。

### 阶段 2 — 性能基线建立与刷新

**MUST read**`protocols/baseline-store-protocol.md`。

按 `protocols/baseline-store-protocol.md` 决定 baseline 是新建（新路径）还是刷新（已有路径）；

- 新建：跑 measure command N 次取中位数 → 写入 `<slug>/perf-audit/baseline.json` + 同步到集中 `perf-baseline/<scope>/baseline-vN.json`；
- 刷新：检查现有 baseline 是否过期（按 protocol §3 周期表）；过期则跑 measure → 与旧 baseline 对比 → 决定覆盖 or 新增版本（覆盖触发 `HG-AUDIT-PERF-BL-OVERWRITE`）；
- 输出 `baseline.json` 双部位齐全。

### 阶段 3 — 性能预算与实测核对**MUST read** `references/perf-checks-catalog.md`

跑每条 NFR-PERF-* 的 measure command（spec 字段 `Measure Command:`）；记录实际值 → 与 spec budget 对比；超 budget → `/performance-reliability-audit:BUDGET_VIOLATED` 标记（不立即阻塞，待 Phase 7 综合判定）；输出 `<slug>/perf-audit/measure-report.md`。

### 阶段 4 — 负载测试（按需）

**MUST read**`protocols/load-test-protocol.md`。

若 NFR-PERF 标载荷场景（concurrency / throughput / sustained-load）→ 按 `protocols/load-test-protocol.md` 跑 load test：

- preprod / staging 直接跑；

-**生产环境**命中 `HG-IRREV-LT` → `/performance-reliability-audit:LOAD_TEST_PENDING_APPROVAL` 等用户批准；

- 输出 `<slug>/perf-audit/load-test-report.md`（含 throughput curve / saturation point / failure mode）。

### 阶段 5 — 容量规划（按需）

**MUST read**`protocols/capacity-planning-protocol.md`。

若 NFR-PERF 标 capacity 场景（用户增长 / 数据增长 / 多区扩展）→ 按 `protocols/capacity-planning-protocol.md` 计算容量上限 + 扩容触发；

-**上限下调**命中 `HG-IRREV-CAP` → `/performance-reliability-audit:CAPACITY_DOWNGRADE_PENDING_APPROVAL` 等用户批准；

- 输出 `<slug>/perf-audit/capacity-plan.md`。

### 阶段 6 — 服务等级协议（SLA）复核（按需）

**MUST read**`protocols/sla-protocol.md`。

若 NFR-PERF 标 SLA 场景（外部承诺 / 内部 SLO）→ 按 `protocols/sla-protocol.md` 审 SLA 定义 / 与 SLO 边界 / 外部承诺：

-**SLA 上调或下调**命中 `HG-IRREV-SLA` → `/performance-reliability-audit:SLA_CHANGE_PENDING_APPROVAL` 等用户批准；

- 输出 `<slug>/perf-audit/sla-record.md`。

### 阶段 7 — 性能回归对比与金丝雀反馈同步

**MUST read**`references/perf-checks-catalog.md §regression` + `protocols/canary-feedback-protocol.md`。

按 `references/perf-checks-catalog.md §regression` 计算与 baseline 的 diff；按严重性分类（Critical / High / Medium / Low）；

- 若 trigger mode = `canary-feedback`：拉 `protocols/canary-feedback-protocol.md` 获取 release-deploy 实时 metric → 高速增量比对；
- 若发现高危 regression（关键路径 p95 > budget × 1.5 或代际退化）→ `/performance-reliability-audit:BENCHMARK_BLOCKED` + `FA-HG-2`；
- 中危 → `/performance-reliability-audit:MITIGATION_REQUIRED`；低危 → `/performance-reliability-audit:WAITING_PERF_RISK_ACCEPTANCE`；
- 输出 `<slug>/perf-audit/regression-report.md` + `<slug>/perf-audit/canary-feedback-log.md`（若适用）。

### 阶段 8 — 关卡归档装配、批准与收口**MUST read** `protocols/audit-protocol.md`

装配 `HG-AUDIT-PERF-*` packet（F-HG-1~8 齐）+ 命中 RWSE Gate 时升级对应 `HG-IRREV-*`；展示给用户 → 各类 `*_PENDING_APPROVAL` / `/performance-reliability-audit:WAITING_PERF_RISK_ACCEPTANCE`；用户原话批准后 → `/performance-reliability-audit:PERF_APPROVED` 输出 `<slug>/perf-audit/perf-gate-packet.md` 给 `/release-deploy` R-RDY-10；mitigation task 交给 `/specs-write` / `/specs-execute`；性能 regression 根因调查交给 `/bug-audit`；记录 audit cycle 到 `DAG-N-AUDIT-{slug}-perf` Done。

---

## 3. 输出格式

```markdown
## 性能与可靠性审计报告 (Performance & Reliability Audit Report)

## 工作流状态 (Workflow State)

- State: /performance-reliability-audit:`<state>`
- 触发模式 (Trigger Mode): <spec-gate | scheduled | bug-handoff | canary-feedback | release-gate | user-explicit>

## 审计范围 (Audit Scope)

- Feature slug + version + 关键路径:
- 非功能性性能契约 NFR-PERF (from spec §10.2):
  - NFR-PERF-001: <metric / budget / measure command / baseline ref / routed-to>
  - NFR-PERF-002: <...>

## 门禁/节点状态 (Gate / DAG Status)

- HG-AUDIT-PERF-{slug}-{scope}: <S-HG-* 状态>
- HG-IRREV-LT / SLA / CAP 命中: <列出激活子项 或 N/A>
- HG-AUDIT-PERF-REG（高危回归锁）: <未触发 / BENCHMARK_BLOCKED>
- DAG-N-AUDIT-{slug}-perf: <node 状态>

## 性能基线 (Baseline)

- 规格包路径 (Spec artifact path): <slug>/perf-audit/baseline.json
- 全局基线路径 (Central path): perf-baseline/<scope>/baseline-v<N>.json
- 最近刷新时间 (Last refreshed): <date>
- 本轮刷新动作 (Refresh action this run): <new / refreshed / unchanged / overwrite-with-approval>

## 指标预算 vs 实际测绘 (Budget vs Measure)
|  | 性能指标契约 (NFR-PERF-*) | 监控指标 (Metric) | 预算 (Budget) | 测绘值 (Measured) | 结论 (Verdict) |  |
|  | ------------ | -------- | -------- | ---------- | --------- |  |
|  | NFR-PERF-001 | <metric> | <budget> | <measured> | PASS / VIOLATED |  |

## 负载测试 (Load Test - 如适用)

- 测试环境 (Environment): <preprod / staging / production>
- 吞吐率曲线 (Throughput curve): <link to report>
- 饱和临界点 (Saturation point): <RPS / concurrent users>
- 故障失效表现 (Failure mode): <列出>
- RWSE 真实世界副作用门禁 (RWSE Gate): <N/A / LOAD_TEST_PENDING_APPROVAL / APPROVED-本次范围>

## 容量规划 (Capacity Plan - 如适用)

- 当前容量天花板 (Current capacity ceiling): <数字 + 单位>
- 预计耗尽日期 (Forecasted exhaustion): <date based on growth curve>
- 推荐改善动作 (Recommended action): <扩容 / 维持 / 下调>
- RWSE 真实世界副作用门禁 (RWSE Gate): <N/A / CAPACITY_DOWNGRADE_PENDING_APPROVAL / APPROVED-本次范围>

## 服务等级承诺 (SLA Record - 如适用)

- 内部 SLO (Internal SLO): <metric + target>
- 外部 SLA 承诺 (External SLA commitment): <metric + target + 合约方>
- 本轮变动 (Change this run): <N/A / 上调 / 下调 / 维持>
- RWSE 真实世界副作用门禁 (RWSE Gate): <N/A / SLA_CHANGE_PENDING_APPROVAL / APPROVED-本次范围>

## 性能回归发现 (Regression Findings)

- 致命 (Critical): <列出 + 影响面 + mitigation 状态>
- 高危 (High): <...>
- 中危 (Medium): <...>
- 低危 (Low): <...>

## 金丝雀反馈同步 (Canary Feedback Sync - 如触发器=canary-feedback)

- 实时指标事实源 (Real-time metric source): <release-deploy canary URL>
- 逆转触发阈值 (Trigger threshold): <metric > budget × N>
- 反向熔断触发时间 (Inverse trigger time): `<timestamp>`
- 增量审计结论 (Increment audit verdict): <列出>

## 缓解/削减计划 (Mitigation Plan)

- 待修补任务 (Required Tasks): <列出待 /specs-write + /specs-execute 修复项>
- 已签署的风险接受承诺 (Risk Acceptance Recorded): <用户原话引用 + 范围限定>

## 授权边界 (Authorization Boundary)

- 路由动作 (Route Action): <CONTINUE_IN_WORKFLOW | WAIT_FOR_USER | CONFIRMED_ACTION | REPORT_AND_STOP>
- 授权来源 (Confirmation source): <用户原话 或 N/A>
- 授权范围 (Authorized scope): <本次 packet 范围内 RWSE Gate / risk acceptance>
- 未授权范围 (Not authorized): <下次审计 / 其他 release / 其他外部副作用 / 下游 workflow>

## 推荐下一步路由 (Recommended Next Route)

- <continue Phase | /specs-write mitigation | /specs-execute fix | /bug-audit 根因 | /architecture-audit 架构调整 | /release-deploy R-RDY-10 handoff>

## 恢复/返航契约 (Return Contract)

- 目标路由 (Target route):
- 准入输入 (Entry input):
- 未决性能回归/未填满信息包字段 (Outstanding regressions / open packet fields):

```

---

## 4. 禁用行为

- **不在**`/performance-reliability-audit:BENCHMARK_BLOCKED` / 高危 regression 未修 / Hard-gate 未批 / RWSE Gate 未批时输出 `/performance-reliability-audit:PERF_APPROVED`。

-**不把**`/performance-reliability-audit:WAITING_PERF_RISK_ACCEPTANCE` 用户裁决继承到下次审计 / 其他 release / 其他范围；每次新 regression 都需新批准。
-**不替代**`/specs-execute` 修性能 bug；本 workflow 只识别 + 出 mitigation task；修复完成后必须重跑 Phase 2-7 增量审计。
-**不替代**`/observability-incident` 写 alert / runbook；本 workflow 只设定 budget 让 obs 推导 alert 阈值（NFR-PERF → NFR-OBS 路由）。
-**不替代**`/bug-audit` 性能 bug 根因分析；本 workflow 只识别 regression 模式；根因（cache miss / N+1 / GC 抖动 / 锁竞争）归 `/bug-audit`。
-**不在**`/performance-reliability-audit:LOAD_TEST_PENDING_APPROVAL` / `/performance-reliability-audit:SLA_CHANGE_PENDING_APPROVAL` / `/performance-reliability-audit:CAPACITY_DOWNGRADE_PENDING_APPROVAL` 未批时跑生产 load test / 改 SLA / 下调 capacity；这三类强制 RWSE Gate（`HG-IRREV-LT/SLA/CAP`），不允许 risk acceptance 替代用户批准。
-**不修** spec / standards / 代码；只读消费它们；如发现需求 / 实现 / 架构缺陷 → 按 `R-RETURN-*` 回切。

- **不把**baseline 跨版本静默覆盖；覆盖必须触发 `HG-AUDIT-PERF-BL-OVERWRITE` + changelog；漏覆盖率不为零，需配合 baseline-store-protocol §4 历史保留规则。

-**不把**audit 后的代码 / 数据量 / 依赖变更视为"已审计"；变更引入新 regression → `/performance-reliability-audit:POST_AUDIT_REGRESSION_DETECTED` + 重跑增量。
-**不把**canary 反馈 metric 视为完整 audit 替代物；canary 数据是"早警信号"而非完整证据；倒序触发后必须重跑 Phase 3-7 而非直接出 packet。
-**不把**SLO（内部目标）与 SLA（外部承诺）混淆；SLA 调整必须同步外部承诺方；SLO 调整不一定需 RWSE Gate 但需文档化。
-**不在** trigger mode 不明时硬启动；`/performance-reliability-audit:PERF_SCOPE_MISSING` 必须回 `/specs-write` 修 §10.2 NFR-PERF 契约。

## 5. 快速自检清单

报告前自检：

- [ ] 是否已确认本次性能审计的触发模式并获取了 NFR-PERF-* 契约？
- [ ] 性能 Baseline 是否已建立或安全刷新（无未授权跨版本静默覆盖）？
- [ ] 测试所得的各项性能指标是否已与 Spec Budget 完成了如实比对？
- [ ] 生产环境 Load Test、SLA 调整或容量下调等高风险操作，是否获得了用户明确批准？
- [ ] 审计中发现的 Regression 退化是否已归类并输出至对应的报告文件？
- [ ] 是否已将装配的 Performance Gate Packet 成功同步给 `/release-deploy`？

## 支撑资源

- [audit-protocol.md](./protocols/audit-protocol.md)
- [baseline-store-protocol.md](./protocols/baseline-store-protocol.md)
- [bug-audit-handoff-protocol.md](./protocols/bug-audit-handoff-protocol.md)
- [canary-feedback-protocol.md](./protocols/canary-feedback-protocol.md)
- [capacity-planning-protocol.md](./protocols/capacity-planning-protocol.md)
- [decision-matrix.md](./references/decision-matrix.md)
- [load-test-protocol.md](./protocols/load-test-protocol.md)
- [perf-checks-catalog.md](./references/perf-checks-catalog.md)
- [sla-protocol.md](./protocols/sla-protocol.md)
