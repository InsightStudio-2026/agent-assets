# 性能检查项规则表 (Performance Checks Catalog)

> 性能检查项规则字典；`/performance-reliability-audit` Phase 2-7 跑这些规则；规则 ID 命名空间 `R-CHK-PERF-*`，与 `../../asset-quality-gates/references/checks-catalog.md` R-CHK-* 平行不冲突。

---

## 0. 规则总览

| 规则组 | 范围 | 跑在哪 Phase |
| ------- | ------ | ------------- |
| §1 Baseline 完整性（R-CHK-PERF-BL-*） | baseline 文件 / 双部位同步 / 版本化 | Phase 2 |
| §2 Budget vs Measure（R-CHK-PERF-BUDGET-*） | measure command / budget 对比 / 样本数 | Phase 3 |
| §3 Load Test 完整性（R-CHK-PERF-LT-*） | 环境 / RWSE Gate / saturation point | Phase 4 |
| §4 Capacity Plan 完整性（R-CHK-PERF-CAP-*） | 容量上限 / 扩容触发 / 下调 RWSE | Phase 5 |
| §5 SLA Record 完整性（R-CHK-PERF-SLA-*） | SLA 定义 / 上下调 RWSE / 外部承诺 | Phase 6 |
| §6 Regression 检测（R-CHK-PERF-REG-*） | baseline diff / 严重性分级 / 阈值 | Phase 7 |
| §7 Canary Feedback 完整性（R-CHK-PERF-CANARY-*） | 实时 metric / 倒序触发 / 增量审计 | Phase 7 |
| §8 Packet 完整性（R-CHK-PERF-PKT-*） | F-HG-1~8 / RWSE 字段 / handoff | Phase 8 |

---

## 1. Baseline 完整性（R-CHK-PERF-BL-*）

### R-CHK-PERF-BL-1：双部位齐全

**检查**：每条 NFR-PERF 必须有：

- spec artifact: `<slug>/perf-audit/baseline.json`
- 集中: `perf-baseline/<scope>/baseline-v<N>.json`

任一缺 → FAIL。

**严重性**：High。

**失败动作**：`FA-HG-1`（阻塞 Phase 3）。

### R-CHK-PERF-BL-2：baseline 字段完整

**检查**：`baseline.json` 必含字段：

- `audit_id` / `feature_slug` / `baseline_version`
- `established_at` / `last_refreshed_at` / `next_refresh_due`
- `measure_environment`（node version / deps lockfile hash / data volume / hardware）
- `metrics[*]`（含 metric / measure_command / samples / median / stddev / budget）

任一缺 → FAIL。

**严重性**：High。

**失败动作**：`FA-HG-1`。

### R-CHK-PERF-BL-3：baseline 未过期

**检查**：`now() < next_refresh_due`。

过期 → 标记 `BASELINE_REQUIRED`（不直接 FAIL，进 Phase 2 refresh）。

**严重性**：Medium。

### R-CHK-PERF-BL-4：覆盖审批

**检查**：若 Phase 2 决定覆盖 baseline（diff >= 20%）：

- `HG-AUDIT-PERF-BL-OVERWRITE` 必须命中
- 用户原话引用必须在 packet F-HG-3
- changelog 必须记录 before/after 数字

任一缺 → FAIL。

**严重性**：High。

**失败动作**：`FA-HG-2`（阻塞 baseline 写入）。

### R-CHK-PERF-BL-5：版本保留

**检查**：旧版本 baseline 必须保留：

- 仓库内 `perf-baseline/<scope>/baseline-v<N>.json` 至少保留最近 3 个版本
- deprecated（Brownfield Replace 路径）保留 90 天后才能删

任一缺 → FAIL。

**严重性**：Medium。

---

## 2. Budget vs Measure（R-CHK-PERF-BUDGET-*）

### R-CHK-PERF-BUDGET-1：measure command 可执行

**检查**：每条 NFR-PERF 的 `measure_command` 必须：

- 在当前仓库可执行（命令存在）
- 输出可解析（含 latency / throughput / memory 数字）
- 退出码 0

任一缺 → FAIL。

**严重性**：High。

**失败动作**：`FA-HG-1` + 路由到 `/specs-execute` 修 measure command。

### R-CHK-PERF-BUDGET-2：样本数充足

**检查**：每条 NFR-PERF 必须跑 measure command **至少 3 次**（避免一次性偶发）。

样本数 < 3 → FAIL。

**严重性**：Medium。

### R-CHK-PERF-BUDGET-3：budget 字段格式

**检查**：spec §10.2 NFR-PERF[*].budget 必须是具体数字 + 单位（如 `p95 < 200ms` / `bundle gzip < 200KB`），不允许模糊词（`快` / `不影响性能`）。

模糊 → FAIL。

**严重性**：High。

**失败动作**：`FA-HG-1` + 回 `/specs-write` 修 §10.2。

### R-CHK-PERF-BUDGET-4：verdict 完整

**检查**：每条 NFR-PERF 都有 verdict（PASS / VIOLATED-MINOR / VIOLATED-MAJOR / VIOLATED-CRITICAL）。

缺 verdict → FAIL。

**严重性**：High。

### R-CHK-PERF-BUDGET-5：环境一致性

**检查**：本次 measure 的环境（node / deps / data volume / hardware）必须与 baseline 环境一致；若不一致需在 measure-report.md 标注差异。

不一致且未标注 → FAIL。

**严重性**：High。

**失败动作**：`FA-HG-1`。

---

## 3. Load Test 完整性（R-CHK-PERF-LT-*）

### R-CHK-PERF-LT-1：环境标识

**检查**：load-test-report.md 必须明确 `Environment: preprod | staging | production`。

缺 → FAIL。

**严重性**：High。

### R-CHK-PERF-LT-2：生产 RWSE Gate

**检查**：若 `Environment: production`：

- 必须命中 `HG-IRREV-LT` + `HG-AUDIT-PERF-LT`
- 必须有用户原话批准（packet F-HG-3）
- 必须有撤销步骤（packet F-HG-6）

任一缺 → FAIL。

**严重性**：Critical。

**失败动作**：`FA-HG-2`（不允许 risk acceptance 替代）。

### R-CHK-PERF-LT-3：saturation point 定义

**检查**：load test 必须报告：

- throughput curve（RPS vs 响应时间）
- saturation point（系统饱和的并发 / RPS）
- failure mode（饱和后是 timeout / 5xx / 内存崩 / 连接耗尽）

任一缺 → FAIL。

**严重性**：High。

### R-CHK-PERF-LT-4：测试工具版本固定

**检查**：load test 工具（k6 / artillery / locust）版本必须 pinned；测试脚本必须在 git 中。

未 pinned 或脚本不在 git → FAIL。

**严重性**：Medium。

---

## 4. Capacity Plan 完整性（R-CHK-PERF-CAP-*）

### R-CHK-PERF-CAP-1：当前上限定义

**检查**：capacity-plan.md 必须明确：

- 当前容量上限（数字 + 单位，如 "100k DAU / 10k QPS"）
- 当前使用率（实测，如 "65k DAU / 6.5k QPS"）
- 计算依据（公式 / 测量 / 估算）

任一缺 → FAIL。

**严重性**：High。

### R-CHK-PERF-CAP-2：扩容触发条件

**检查**：必须定义扩容触发条件（如 "使用率 > 80% 持续 1 周 → 扩容"）。

缺 → FAIL。

**严重性**：High。

### R-CHK-PERF-CAP-3：增长曲线预测

**检查**：必须有增长曲线预测（数据来源 / 预测模型 / forecasted exhaustion 时间）。

缺 → FAIL。

**严重性**：Medium。

### R-CHK-PERF-CAP-4：上限下调 RWSE Gate

**检查**：若 capacity-plan.md 决定下调上限：

- 必须命中 `HG-IRREV-CAP` + `HG-AUDIT-PERF-CAP`
- 必须有用户原话批准
- 必须有影响评估（哪些用户 / 租户 / 功能受限）

任一缺 → FAIL。

**严重性**：Critical。

**失败动作**：`FA-HG-2`。

---

## 5. SLA Record 完整性（R-CHK-PERF-SLA-*）

### R-CHK-PERF-SLA-1：SLO ↔ SLA 区分

**检查**：sla-record.md 必须明确区分：

- 内部 SLO（target / 测量方式 / 团队承诺）
- 外部 SLA（合约 / 承诺方 / 违约赔偿条款）

不区分 → FAIL。

**严重性**：High。

### R-CHK-PERF-SLA-2：SLA 上调 RWSE Gate

**检查**：若 SLA 上调（提高承诺）：

- 必须命中 `HG-IRREV-SLA` + `HG-AUDIT-PERF-SLA`
- 必须评估代码 / 架构负担
- 必须有用户原话批准
- 外部承诺方必须同步通知（如未通知则 packet F-HG-6 标记待办）

任一缺 → FAIL。

**严重性**：Critical。

### R-CHK-PERF-SLA-3：SLA 下调 RWSE Gate

**检查**：若 SLA 下调（降低承诺）：

- 必须命中 `HG-IRREV-SLA` + `HG-AUDIT-PERF-SLA`
- 必须有降级原因（架构限制 / 资源限制 / 误承诺更正）
- 必须有用户原话批准
- 外部承诺方必须同步通知（违反原合约可能触发赔偿）

任一缺 → FAIL。

**严重性**：Critical。

### R-CHK-PERF-SLA-4：SLO 与 budget 一致

**检查**：内部 SLO 必须与 NFR-PERF budget 一致或更严格（不允许 SLO 比 budget 宽松，否则 spec 说一套实际另一套）。

不一致 → FAIL。

**严重性**：High。

---

## 6. Regression 检测（R-CHK-PERF-REG-*）

### R-CHK-PERF-REG-1：阈值表

| 差异百分比 (diff_pct) | 测量值与预算对比 (measured vs budget) | 严重性 | 状态 (State) |
| --------- | ------------------- | -------- | ------- |
| `<= 5%` | `<= budget` | NO_REGRESSION | PASS 候选 |
| `5%~15%` | `<= budget` | REGRESSION_MINOR | `WAITING_PERF_RISK_ACCEPTANCE` |
| `15%~30%` 或 `> budget × 1.2` | - | REGRESSION_MAJOR | `MITIGATION_REQUIRED` |
| `> 30%` 或 `> budget × 1.5` 或 代际退化 | - | REGRESSION_CRITICAL | `BENCHMARK_BLOCKED` + `FA-HG-2` |

### R-CHK-PERF-REG-2：每条 NFR-PERF 都有 verdict

**检查**：regression-report.md 中每条 NFR-PERF 都有严重性分类。

缺 → FAIL。

**严重性**：High。

### R-CHK-PERF-REG-3：CRITICAL 不允许 risk acceptance

**检查**：`REGRESSION_CRITICAL` 严重性不允许 `WAITING_PERF_RISK_ACCEPTANCE`；必须修。

若发现 CRITICAL 标 risk accepted → FAIL。

**严重性**：Critical。

**失败动作**：`FA-HG-2`。

### R-CHK-PERF-REG-4：代际退化识别

**检查**：若 measured 比 baseline 慢 1 个数量级（10× 以上）→ 自动 CRITICAL（即使 diff_pct 计算 < 30%，因为基数差异）。

未识别 → FAIL（checker 缺陷）。

**严重性**：Critical。

---

## 7. Canary Feedback 完整性（R-CHK-PERF-CANARY-*）

### R-CHK-PERF-CANARY-1：实时 metric 来源

**检查**：若 trigger=canary-feedback：

- canary-feedback-log.md 必须有 metric source URL（release-deploy canary 监控）
- 必须有 trigger time / threshold / 实际值

任一缺 → FAIL。

**严重性**：High。

### R-CHK-PERF-CANARY-2：增量审计而非全量

**检查**：canary-feedback 触发时不重跑 measure command（避免影响 canary 期生产环境）；只与现有 baseline 高速增量比对。

跑了 measure command（除非用户显式批准）→ FAIL。

**严重性**：High。

### R-CHK-PERF-CANARY-3：倒序触发不沿用旧 packet

**检查**：canary 倒序触发后必须装配新 packet（`perf-canary-regression-packet.md`），不沿用 spec-gate 期的 `perf-gate-packet.md`。

沿用旧 packet → FAIL。

**严重性**：High。

### R-CHK-PERF-CANARY-4：阈值定义

**检查**：canary feedback 倒序触发的阈值必须在 `../protocols/canary-feedback-protocol.md §阈值表` 中定义；不允许临时设阈值。

未定义 → FAIL。

**严重性**：Medium。

---

## 8. Packet 完整性（R-CHK-PERF-PKT-*）

### R-CHK-PERF-PKT-1：F-HG-1~8 全齐

**检查**：perf-gate-packet.md（或对应类型 packet）必须含 F-HG-1~8 全部 slot。

任一缺 → FAIL。

**严重性**：High。

**失败动作**：`FA-HG-1`。

### R-CHK-PERF-PKT-2：RWSE Gate 字段

**检查**：若命中 RWSE Gate（`LOAD_TEST_PENDING_APPROVAL` / `SLA_CHANGE_PENDING_APPROVAL` / `CAPACITY_DOWNGRADE_PENDING_APPROVAL`）：

- F-HG-3 必含用户原话引用
- F-HG-6 必含撤销步骤
- F-HG-4 必含 Authorized scope（限本次 packet）+ Not authorized（不继承）

任一缺 → FAIL。

**严重性**：Critical。

**失败动作**：`FA-HG-2`。

### R-CHK-PERF-PKT-3：handoff 路由记录

**检查**：packet 必须记录：

- mitigation task → `/specs-write` + `/specs-execute`
- 性能根因 → `/bug-audit`
- 架构调整 → `/architecture-audit`
- release gate → `/release-deploy` R-RDY-10

未记录 → FAIL。

**严重性**：High。

### R-CHK-PERF-PKT-4：DAG node 状态

**检查**：`DAG-N-AUDIT-{slug}-perf` 必须在 packet 装配后切换到对应 status（Done / Blocked / Waiting）。

未切换 → FAIL。

**严重性**：Medium。

---

## 9. 严重性 → 失败动作映射

| 严重性 | 失败动作 |
| ------- | --------- |
| Critical | `FA-HG-2` 阻塞 + 路由到 mitigation；不允许 risk acceptance |
| High | `FA-HG-1` 报告 + 等修复；可路由到 `/specs-execute` 修 |
| Medium | 报告 + 警告；不阻塞但需 changelog 记录 |
| Low | 仅报告 |

详 `../../asset-quality-gates/references/checks-catalog.md §4` FA-HG-* 失败动作通用规则。

---

## 10. 修订规则

- 本文修订必须同 PR 修订 `../protocols/audit-protocol.md`（保持 Phase 与规则字典一致）。
- 新增规则 → 同步更新 workflow 入口 §0.1 State 表（若引入新 state）。
- 阈值调整（如 R-CHK-PERF-REG-1 阈值表）→ 必须命中 `HG-AUDIT-PERF-THRESHOLD`（建议用户批准）。
- 不允许在 fixture / example 中弱化检查规则；规则字典是字面事实源。
