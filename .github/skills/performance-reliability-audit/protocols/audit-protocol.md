# 性能与可靠性审计协议 (Performance & Reliability Audit Protocol)

> 本文是 `/performance-reliability-audit` 的 8 Phase 执行细则；workflow 入口仅留控制流骨架，所有判定 / 字段 / 模板细节在本文。事实源详 performance-reliability-audit SKILL.md §0.1 State 表 + `../../specs-write/protocols/gate-dag-protocol.md`。

---

## 0. Phase 总览

| Phase | 标题 | 输入 | 输出 | 跳过条件 |
| ------- | ------ | ------ | ------ | --------- |
| 1 | Scope & Trigger Detection | spec NFR-PERF / 触发上下文 | `<slug>/perf-audit/charter.md` + `trigger-mode.md` | NFR-PERF 全 N/A 且无关键路径变更 → 不启用 workflow |
| 2 | Baseline Establish or Refresh | charter.md + baseline-store-protocol | `baseline.json`（双部位）+ `baseline-changelog.md` | trigger=`bug-handoff` / `canary-feedback` 用现有 baseline 跳过 |
| 3 | Budget vs Measure | NFR-PERF measure command | `measure-report.md` | 无 |
| 4 | Load Test | NFR-PERF 标载荷场景 | `load-test-report.md` | NFR-PERF 未标 concurrency / throughput / sustained-load |
| 5 | Capacity Planning | NFR-PERF 标 capacity 场景 | `capacity-plan.md` | NFR-PERF 未标 capacity / 多区 / 多租户 |
| 6 | SLA Review | NFR-PERF 标 SLA 场景 | `sla-record.md` | NFR-PERF 未标 SLA / 外部承诺 |
| 7 | Regression Diff + Canary Feedback Sync | baseline + measure-report + 可选 canary metric | `regression-report.md` + `canary-feedback-log.md` | 无 |
| 8 | Gate Packet 装配 + Approval + Closeout | 上述全部 artifacts | `perf-gate-packet.md` | 无 |

跳过哪些 Phase 由 §1 Trigger Mode Matrix 决定。

---

## 1. Trigger Mode 判定（Phase 1 核心规则）

### 1.1 Trigger Mode 类型

| Mode ID | 触发源 | 检测信号 |
| --------- | -------- | --------- |
| `spec-gate` | `/specs-write` close-out 前 | spec NFR-PERF Active 且 R-RDY-10 缺事实源 |
| `scheduled` | 周期任务 | `baseline-store-protocol.md §3 周期表` 到期 |
| `bug-handoff` | `/bug-audit` 分流性能 bug | bug-audit packet 含 `route_to: /performance-reliability-audit` |
| `canary-feedback` | `/release-deploy` canary 期实时 metric 倒序 | canary metric > budget × `canary-feedback-protocol.md §阈值` |
| `release-gate` | `/release-deploy` 装配 R-RDY-10 时 | release-deploy 报告 R-RDY-10 缺 packet |
| `user-explicit` | 用户显式 `/performance-reliability-audit` | 用户原话 |

### 1.2 Trigger Mode 判定流程

```text

1. 读取触发上下文（用户原话 / spec close-out / release-deploy 调用 / bug-audit handoff / canary feedback / scheduled）
2. 写入 <slug>/perf-audit/trigger-mode.md（mode + 触发源 + 时间戳 + 上游 packet 引用）
3. 按 §0.4 Trigger Mode Matrix 决定本次 audit 跳哪些 Phase
4. 输出：trigger-mode.md + audit Phase 清单
5. State 切换：TRIGGER_MODE_DETERMINED

```

### 1.3 Trigger Mode 决策树

```text
IF user-explicit
  → 全 Phase（建议 baseline refresh + 询问 load test / capacity / SLA 是否跑）
ELIF spec-gate AND NFR-PERF-* 仅含 latency/memory/bundle
  → Phase 1-3 + Phase 7-8（跳过 4/5/6）
ELIF spec-gate AND NFR-PERF-* 含 concurrency / throughput / sustained-load
  → Phase 1-4 + Phase 7-8（跳过 5/6 除非另有 capacity / SLA NFR）
ELIF spec-gate AND NFR-PERF-* 含 capacity / 多区 / 多租户
  → Phase 1-5 + Phase 7-8
ELIF spec-gate AND NFR-PERF-* 含 SLA / 外部承诺
  → Phase 1-6 + Phase 7-8（全跑）
ELIF scheduled
  → Phase 1 + Phase 2 (refresh) + Phase 3 + Phase 7 + Phase 8 (refresh-only packet)
ELIF bug-handoff
  → Phase 1 + Phase 3 (仅相关路径) + Phase 7 + Phase 8（用现有 baseline）
ELIF canary-feedback
  → Phase 1 + Phase 3 + Phase 7 (高速增量) + Phase 8 (CANARY_FEEDBACK_REGRESSION packet)
ELIF release-gate
  → Phase 1 + Phase 2 (确认未过期) + Phase 3 + Phase 7 + Phase 8 + 按需 4/5/6
```

### 1.4 Trigger Mode 互斥与升级

- **互斥**：同一次 audit 只能有一个 primary trigger mode；多源触发取最高优先级（user-explicit > canary-feedback > release-gate > spec-gate > bug-handoff > scheduled）。
- **升级**：审计中途若发现 canary-feedback 或新 bug-handoff → `POST_AUDIT_REGRESSION_DETECTED` 重置当前 audit cycle，重跑 Phase 2-7 增量。
- **降级**：若 trigger mode = scheduled 但发现关键路径有 spec-gate 级 NFR-PERF 变更 → 升级到 spec-gate（确保覆盖完整 Phase）。

---

## 2. Phase 1 — Scope & Trigger Detection 细则

### 2.1 输入

- 触发上下文（用户原话 / 上游 packet / spec close-out 信号）
- spec requirements §10.2 NFR-PERF-* 全部条目
- spec design 性能假设（cache / batch / shard / async）
- charter Architectural Invariants（INV-PERF-* 类）
- 上游 packet（若有）：bug-audit / release-deploy / specs-write

### 2.2 必填字段（charter.md）

```yaml
audit_id: PERF-{slug}-{YYYY-MM-DD}-{seq}
trigger_mode: spec-gate | scheduled | bug-handoff | canary-feedback | release-gate | user-explicit
trigger_source:
  upstream_packet: <packet ref or N/A>
  user_quote: "<用户原话引用>" 或 N/A
  scheduled_cycle: <cycle id> 或 N/A
feature_slug: <feature-slug or global-scope>
audit_scope:
  critical_paths: [<list of API / page / job / queue path>]
  excluded_paths: [<明确排除>]
nfr_perf_contract:

  - id: NFR-PERF-001
    metric: latency-p95 | latency-p99 | memory | bundle-size | cold-start | API-throughput | DB-query-count | LCP | INP | CLS
    budget: <具体数字 + 单位>
    measure_command: <复现命令>
    baseline_ref: <path or N/A>
    routed_to: /performance-reliability-audit#<anchor>

phases_to_run: [1, 2, 3, 7, 8]  # 按 §1.3 决策树
phases_to_skip: [4, 5, 6]
estimated_duration: <时长估算>
```

### 2.3 验收（DoD）

- [ ] `trigger_mode` 已识别并写入 `trigger-mode.md`
- [ ] `nfr_perf_contract` 至少 1 条（否则 `PERF_SCOPE_MISSING` 回 `/specs-write`）
- [ ] `phases_to_run` 与 §1.3 决策树一致
- [ ] `audit_scope.critical_paths` 非空
- [ ] State 切换到 `TRIGGER_MODE_DETERMINED`

### 2.4 失败模式

| 失败 | 状态 (State) | 回切 |
| ------ | ------- | ------ |
| NFR-PERF 全无或全 N/A | `PERF_SCOPE_MISSING` | 回 `/specs-write` 修 §10.0 High-Risk Assessment + §10.2 NFR-PERF |
| measure_command 缺失 | `PERF_SCOPE_MISSING` | 回 `/specs-write` 补 §10.2 measure command 字段 |
| baseline_ref 指向不存在路径 | 进入 Phase 2 + 标记 `BASELINE_REQUIRED` | 不阻塞，Phase 2 处理 |

---

## 3. Phase 2 — Baseline Establish or Refresh 细则

### 3.1 决策树

```text

1. 读 charter.md NFR-PERF[*].baseline_ref
2. FOR EACH NFR-PERF:
   IF baseline_ref == N/A AND new path
     → 新建 baseline（跑 measure command N=5 取中位数 + 标准差）
   ELIF baseline_ref 存在 AND last_refreshed < 周期表阈值
     → 用现有 baseline（不跑 measure）
   ELIF baseline_ref 存在 AND last_refreshed >= 周期表阈值
     → 刷新 baseline（跑 measure 与旧对比）
     IF diff < 5%
       → 更新 timestamp，不写新版本
     ELIF diff < 20%
       → 写新版本（v(N+1)），保留旧版本
     ELIF diff >= 20%
       → 触发 HG-AUDIT-PERF-BL-OVERWRITE → 等用户裁决（覆盖 / 新增版本 / 调查 regression）
   ELIF baseline_ref 存在 AND 路径变更（Brownfield Replace）
     → 标 deprecated（保留 30 天）+ 新建当前版本
3. 写入双部位：
   - `<slug>`/perf-audit/baseline.json（spec artifact）
   - perf-baseline/`<scope>`/baseline-v`<N>`.json（集中）
4. 写 baseline-changelog.md（版本 / 时间 / 变更原因 / 操作者）

```

### 3.2 baseline.json 格式

```json
{
  "audit_id": "PERF-oauth-google-login-2026-05-24-001",
  "feature_slug": "oauth-google-login",
  "baseline_version": "v3",
  "established_at": "2026-05-24T10:00:00Z",
  "last_refreshed_at": "2026-05-24T10:00:00Z",
  "next_refresh_due": "2026-08-24T10:00:00Z",
  "measure_environment": {
    "node_version": "20.10.0",
    "deps_lockfile_hash": "abc123...",
    "data_volume": "10k users / 1M sessions",
    "hardware": "Linode 4GB"
  },
  "metrics": {
    "NFR-PERF-001": {
      "metric": "latency-p95",
      "measure_command": "k6 run scripts/perf/oauth-callback.js",
      "samples": [780, 795, 810, 805, 790],
      "median": 795,
      "stddev": 11.5,
      "budget": 800,
      "verdict_at_baseline": "PASS"
    }
  }
}
```

### 3.3 双部位同步规则

| 操作 | spec artifact (`<slug>/perf-audit/`) | 集中 (`perf-baseline/<scope>/`) |
| ------ | -------------------------------------- | -------------------------------- |
| 新建 baseline | 写 `baseline.json` | 写 `baseline-v1.json` |
| Refresh diff < 5% | 更新 `last_refreshed_at` | 更新 `last_refreshed_at`（不写新版本） |
| Refresh diff 5%~20% | 覆盖 `baseline.json` | 写 `baseline-v(N+1).json`（保留 v(N)） |
| Refresh diff >= 20% | 等用户裁决 | 等用户裁决 |
| Brownfield Replace 路径 | deprecated 30 天后删 | 标 `deprecated-v(N)` 保留 90 天 |
| Spec close-out | 不动 | sync 一份到 `perf-baseline/<scope>/closed/<feature-slug>-v(N).json` |
| Spec archive | 不动 | 保留 |
| Spec merge back | 不动 | 升级到 long-living: `perf-baseline/<scope>/long-living/<scope>-v(N).json` |

### 3.4 验收（DoD）

- [ ] 每条 NFR-PERF 对应一份 baseline 数据（spec artifact + 集中 双部位齐）
- [ ] `baseline-changelog.md` 记录本次操作
- [ ] State 切换到 `BASELINE_REFRESHED`
- [ ] 若 trigger=`bug-handoff` / `canary-feedback`：跳过本 Phase 但确认现有 baseline 未过期

详细细节见 `baseline-store-protocol.md`。

---

## 4. Phase 3 — Budget vs Measure 细则

### 4.1 流程

```text

FOR EACH NFR-PERF in charter.nfr_perf_contract:

  1. 跑 measure_command N=3 次（避免一次性偶发干扰）
  2. 计算 median / p95 / p99 / stddev
  3. 与 budget 对比：
     IF measured <= budget × 1.0 → PASS
     ELIF measured <= budget × 1.2 → BUDGET_VIOLATED-MINOR
     ELIF measured <= budget × 1.5 → BUDGET_VIOLATED-MAJOR
     ELSE → BUDGET_VIOLATED-CRITICAL
  4. 记录到 measure-report.md

不立即阻塞 Phase 7 综合判定再决定 verdict。

```

### 4.2 measure-report.md 模板

```markdown
## 性能测绘报告 (Measure Report) — PERF-{slug}-{date}-{seq}

## NFR-PERF-001

- 指标类型 (Metric): latency-p95
- 指标预算 (Budget): 800ms
- 测绘样本 - 3轮 (Samples - 3 runs): [795, 810, 802]
- 中位数 (Median): 802ms
- p95 测绘值 (p95): 808ms
- p99 测绘值 (p99): 810ms
- 标准差 (StdDev): 7.5ms
- 结论 (Verdict): PASS（小于预算值 budget × 1.0）

## NFR-PERF-002

- ...

```

### 4.3 验收（DoD）

- [ ] 每条 NFR-PERF 都跑了 measure command 至少 3 次
- [ ] 每条都有 verdict（PASS / VIOLATED-MINOR / VIOLATED-MAJOR / VIOLATED-CRITICAL）
- [ ] State 切换：若有任何 VIOLATED → 标记 `BUDGET_VIOLATED`（但继续后续 Phase）

---

## 5. Phase 4-6 — Load Test / Capacity / SLA 细则

详细见各自 protocol：

- Phase 4：`load-test-protocol.md`
- Phase 5：`capacity-planning-protocol.md`
- Phase 6：`sla-protocol.md`

各 Phase 的 RWSE Gate 触发条件已在 workflow 入口 §0.3 列出。本文不重复，只列共同行为：

### 5.1 RWSE Gate 通用流程

```text

1. 检测命中条件（生产 load test / SLA 上下调 / capacity 上限下调）
2. 切换到对应 PENDING_APPROVAL state
3. 装配 packet F-HG-1~8（事实 / 影响 / 范围 / 撤销 / 监控 / 通知 / 替代方案 / 用户原话）
4. 展示给用户 + 等明确批准
5. 用户批准（CONFIRMED_ACTION 仅限本次 packet 范围）→ 执行
6. 用户拒绝 → REPORT_AND_STOP + 路由到 mitigation

```

### 5.2 跳过条件

| Phase | 跳过条件 |
| ------- | --------- |
| 4 Load Test | NFR-PERF 未标 concurrency / throughput / sustained-load 字段 |
| 5 Capacity | NFR-PERF 未标 capacity / 多区 / 多租户 字段 |
| 6 SLA | NFR-PERF 未标 SLA / 外部承诺 字段 |

跳过时 `phases_to_skip` 对应记录；不在 packet 中标 N/A 而是显式 skip。

---

## 6. Phase 7 — Regression Diff + Canary Feedback Sync 细则

### 6.1 Regression 计算

```text

FOR EACH NFR-PERF:
  diff_pct = (measured - baseline.median) / baseline.median × 100%
  
  按 perf-checks-catalog.md §regression 阈值表分类：
  IF diff_pct <= 5% AND measured <= budget → NO_REGRESSION
  ELIF diff_pct <= 15% AND measured <= budget → REGRESSION_MINOR
  ELIF diff_pct <= 30% OR measured > budget × 1.2 → REGRESSION_MAJOR
  ELIF diff_pct > 30% OR measured > budget × 1.5 OR 代际退化 → REGRESSION_CRITICAL

```

### 6.2 严重性 → 处置映射

| 严重性 | 处置 | 状态 (State) |
| ------- | ------ | ------- |
| `NO_REGRESSION` | 无 mitigation 需求 | 进入 Phase 8（PASS 候选） |
| `REGRESSION_MINOR` | 进入 Phase 8（risk acceptance 候选） | `WAITING_PERF_RISK_ACCEPTANCE` |
| `REGRESSION_MAJOR` | 出 mitigation task | `MITIGATION_REQUIRED` |
| `REGRESSION_CRITICAL` | 阻塞 release | `BENCHMARK_BLOCKED` + `FA-HG-2` |

### 6.3 Canary Feedback Sync（若 trigger=canary-feedback）

```text

1. 拉 release-deploy canary 期实时 metric（按 `<pra>`/canary-feedback-protocol.md §metric source）
2. 与 baseline 对比 → 高速增量比对（不重跑 measure command）
3. 写入 canary-feedback-log.md（trigger time / threshold / 实际值 / verdict）
4. 升级 state 到 CANARY_FEEDBACK_REGRESSION
5. 进入 Phase 8 装配 CANARY_FEEDBACK packet（不沿用旧 packet）

```

### 6.4 验收（DoD）

- [ ] 每条 NFR-PERF 都有 regression verdict
- [ ] regression-report.md 完整（含每条严重性 + 处置建议）
- [ ] 若 trigger=canary-feedback：canary-feedback-log.md 完整
- [ ] State 切换：根据最高严重性 → 对应 state

---

## 7. Phase 8 — Gate Packet 装配 + Approval + Closeout 细则

### 7.1 Packet 字段（F-HG-1~8 全齐）

| Slot | 字段 | 内容 |
| ------ | ------ | ------ |
| F-HG-1 | Facts | 本次 audit 的 trigger / scope / NFR-PERF / baseline / measure / regression 全部事实 |
| F-HG-2 | Impact | regression 影响面（用户 / 租户 / 关键路径 / 性能预算） |
| F-HG-3 | User quote | 若命中 RWSE Gate / risk acceptance：用户原话引用 |
| F-HG-4 | Scope limit | 本次 packet 仅授权本次 audit 范围 |
| F-HG-5 | Monitoring | 装配后的监控锚点（NFR-OBS-* 路由） |
| F-HG-6 | Rollback | 若执行了 RWSE 操作（生产 load test / SLA 调整 / capacity 下调）：回滚步骤 |
| F-HG-7 | Alternatives | 已考虑的替代方案 + 拒绝理由 |
| F-HG-8 | Verification | 修复后如何验证 + 重审触发条件 |

### 7.2 Packet 类型

| Packet 类型 | 触发 | 文件名 |  |  |
| ------------- | ------ | -------- |  |  |
| `PERF_APPROVED` packet | 全 PASS / risk accepted | `perf-gate-packet.md` |  |  |
| `BENCHMARK_BLOCKED` packet | 高危 regression | `perf-block-report.md` |  |  |
| `MITIGATION_REQUIRED` packet | 中危需修 | `perf-mitigation-tasks.md` |  |  |
| `CANARY_FEEDBACK_REGRESSION` packet | canary 倒序触发 | `perf-canary-regression-packet.md` |  |  |
| `RWSE Gate` packet | load test / SLA / capacity 命中 | `perf-rwse-{lt | sla | cap}-packet.md` |

### 7.3 Approval 流程

```text

1. 装配 packet（F-HG-1~8 全齐）
2. 展示给用户 + 列出 RWSE Gate / risk acceptance 待批项
3. 等用户原话明确批准（CONFIRMED_ACTION 仅限本次 packet 范围）
4. 批准后切换 PERF_APPROVED 或对应 RWSE 执行 state
5. 拒绝 → REPORT_AND_STOP + 分流 mitigation
6. 写入 packet 到 `<slug>`/perf-audit/perf-gate-packet.md（或对应类型文件名）

```

### 7.4 Closeout & Handoff

```text

1. 同步 packet 给 /release-deploy R-RDY-10（perf-gate-packet.md 路径）
2. mitigation task 路由到 /specs-write 创建 + /specs-execute 执行
3. 性能 regression 根因路由到 /bug-audit
4. 容量 / SLA / 架构调整路由到 /architecture-audit
5. canary 反馈环：注册到 release-deploy canary 期监控（按 canary-feedback-protocol.md §reg）
6. DAG-N-AUDIT-{slug}-perf 标 Done
7. baseline 同步到 perf-baseline/`<scope>`/closed/（若 spec close-out）

```

### 7.5 验收（DoD）

- [ ] packet F-HG-1~8 全齐
- [ ] 命中 RWSE Gate 时 F-HG-3 含用户原话 + F-HG-6 含撤销步骤
- [ ] 路由 handoff 已记录（哪些 task 给哪个 workflow）
- [ ] DAG node Done
- [ ] State 切换到 `PERF_APPROVED` / `BENCHMARK_BLOCKED` / `MITIGATION_REQUIRED`

---

## 8. NFR-PERF Routed-to 锚点约定

spec NFR-PERF-* `Routed to:` 字段引用本 workflow 时使用约定锚点；锚点不是物理 markdown anchor，而是**路由意图标识**：本 workflow 通过 §1 Trigger Mode + Phase 2 决策树处理。

### 8.1 当前已使用的锚点

| 锚点 | 含义 | 触发本 workflow 的 Phase 行为 | 示例引用 |
| ------ | ------ | -------------------------------- | --------- |
| `#`<feature>`-baseline-required` | 新路径首次建立 baseline 请求 | trigger=spec-gate → Phase 2 第一次写 baseline（`baseline-store-protocol.md §1.4 事件 1`） | `/performance-reliability-audit#oauth-baseline-required` |
| `#`<feature>`-baseline` | 已建立 baseline 引用 | trigger=spec-gate → Phase 2 refresh 决策（`baseline-store-protocol.md §1.4 事件 2/3/4`） | `/performance-reliability-audit#mailgun-baseline` |
| `#NFR-PERF-`<NNN>`-replace` | Brownfield Replace 路径，旧 NFR-PERF deprecated + 新建 baseline | trigger=spec-gate → Phase 2 deprecated/ 移动 + 新 baseline（`baseline-store-protocol.md §1.4 事件 5`） | `/performance-reliability-audit#NFR-PERF-001-replace` |
| 无锚点（仅 `/performance-reliability-audit`） | 通用入口 | trigger 由上下文决定（spec-gate / scheduled / canary-feedback） | `/performance-reliability-audit` |

### 8.2 锚点命名规则

新 spec 写 NFR-PERF `Routed to:` 时按下表选锚点：

```text

IF NFR-PERF Status = Active AND Greenfield AND Baseline Ref = N/A (新路径)
  → Routed to: /performance-reliability-audit#`<feature-slug>`-baseline-required

ELIF NFR-PERF Status = Active AND Brownfield Delta Op = Replace
  → Routed to: /performance-reliability-audit#NFR-PERF-`<NNN>`-replace

ELIF NFR-PERF Status = Active AND Brownfield Delta Op = Modify
  → Routed to: /performance-reliability-audit#NFR-PERF-`<NNN>`-modify

ELIF NFR-PERF Status = Active AND Brownfield Delta Op = Add
  → Routed to: /performance-reliability-audit#NFR-PERF-`<NNN>`-add

ELIF NFR-PERF Status = Active AND 已有 baseline
  → Routed to: /performance-reliability-audit#`<feature-slug>`-baseline (引用现有 baseline)

ELSE （通用 / 不需特殊 Phase 行为）
  → Routed to: /performance-reliability-audit

```

### 8.3 锚点 → Phase 行为路由表

本 workflow 收到 `Routed to:` 引用时按锚点决定首选 Phase 行为：

| 锚点模式 | 首次进入本 workflow 的 Phase | 首选 Trigger Mode |
| --------- | ----------------------------- | ------------------ |
| `#`<feature>`-baseline-required` | Phase 1 + Phase 2 (新建) + Phase 3 + Phase 7 + Phase 8 | spec-gate |
| `#`<feature>`-baseline` | Phase 1 + Phase 2 (refresh 检查) + Phase 3 + Phase 7 + Phase 8 | spec-gate |
| `#NFR-PERF-`<NNN>`-replace` | Phase 1 + Phase 2 (deprecated/ + 新建) + Phase 3 + Phase 7 + Phase 8 | spec-gate |
| `#NFR-PERF-`<NNN>`-modify` | Phase 1 + Phase 2 (refresh) + Phase 3 + Phase 7 + Phase 8 | spec-gate |
| `#NFR-PERF-`<NNN>`-add` | Phase 1 + Phase 2 (新建) + Phase 3 + Phase 7 + Phase 8 | spec-gate |
| 无锚点 | 按 trigger context 决定 | 由 trigger 上下文判定 |

锚点不存在 / 不识别 → 默认按"通用入口"处理（无锚点路径）+ 在 audit-charter.md 标注"unrecognized anchor: <锚点>"以备后续命名收敛。

---

## 9. 与其他 workflow 的边界

### 9.1 与 `/observability-incident`

| 事项 | 归属 |
| ------ | ------ |
| baseline / budget / regression 检测 | `/performance-reliability-audit`（本 workflow） |
| alert / runbook / dashboard / SLO violation 响应 | `/observability-incident` |
| alert 阈值由 perf budget 推导 | 边界：本 workflow 出 budget；obs 推导 alert 阈值（NFR-PERF → NFR-OBS 路由） |
| 事故响应中性能根因 | `/observability-incident` 触发 + 分流到本 workflow + `/bug-audit` |

### 9.2 与 `/bug-audit`

| 事项 | 归属 |
| ------ | ------ |
| 性能 regression 模式识别 | 本 workflow（Phase 7） |
| 性能 bug 根因（cache miss / N+1 / GC / 锁） | `/bug-audit` |
| 用户报告"慢" → 分流 | `/bug-audit` 接 → handoff 到本 workflow（trigger=bug-handoff） |

### 9.3 与 `/release-deploy`

| 事项 | 归属 |
| ------ | ------ |
| R-RDY-10 Performance Gate 事实源 | 本 workflow（输出 perf-gate-packet.md） |
| canary 期实时 metric | `/release-deploy` 监控 + 本 workflow canary feedback |
| BENCHMARK_BLOCKED 阻塞 release | 本 workflow 决定 + release-deploy 接收阻塞 |
| canary perf 超阈值倒序触发 | `/release-deploy` → 本 workflow（trigger=canary-feedback） |

### 9.4 与 `/architecture-audit`

| 事项 | 归属 |
| ------ | ------ |
| 架构层性能取舍（cache / shard / batch / async） | `/architecture-audit` |
| 性能 NFR 落地验证 | 本 workflow |
| capacity 上限决策 | 本 workflow（capacity-plan.md）+ 重大调整路由到 `/architecture-audit` |

### 9.5 与 `/specs-write` / `/specs-execute`

| 事项 | 归属 |
| ------ | ------ |
| NFR-PERF-* 契约定义 | `/specs-write`（spec §10.2） |
| measure command / budget / baseline ref 字段填写 | `/specs-write` |
| mitigation task 创建 | `/specs-write` 接本 workflow handoff |
| mitigation task 执行 | `/specs-execute` |
| 修复后 verification | `/specs-execute` + 重跑本 workflow Phase 2-7 |

---

## 10. 失败模式速查

| 失败 | 原因 | 处置 |
| ------ | ------ | ------ |
| `PERF_SCOPE_MISSING` | NFR-PERF 全无 / measure command 缺 / 关键路径未定义 | 回 `/specs-write` 修 §10 NFR + §10.2 measure command |
| `BASELINE_REQUIRED` | 新路径无 baseline 或 baseline 过期 | Phase 2 建立或刷新 |
| `BUDGET_VIOLATED` | measure > budget | 进入 Phase 7 综合判定 |
| `LOAD_TEST_PENDING_APPROVAL` | 生产 load test RWSE Gate | 等用户批准 |
| `CAPACITY_DOWNGRADE_PENDING_APPROVAL` | capacity 下调 RWSE Gate | 等用户批准 |
| `SLA_CHANGE_PENDING_APPROVAL` | SLA 上下调 RWSE Gate | 等用户批准 |
| `BENCHMARK_BLOCKED` | 高危 regression 阻塞 release | 阻塞 + 分流 mitigation |
| `MITIGATION_REQUIRED` | 中危 regression | 出 mitigation task |
| `WAITING_PERF_RISK_ACCEPTANCE` | 低危 regression / risk acceptance 候选 | 等用户原话 |
| `CANARY_FEEDBACK_REGRESSION` | canary 倒序触发 | 重跑 Phase 3-7 增量 |
| `POST_AUDIT_REGRESSION_DETECTED` | 审计后变更引入新 regression | 重跑 Phase 2-7 |

---

## 11. 修订规则

- 本文修订必须同 PR 修订 workflow 入口 `performance-reliability-audit.md` §0.1 State 表 + `../references/perf-checks-catalog.md`（保持规则字典一致）。
- 新增 Phase / Trigger Mode → 同步更新 `../references/perf-checks-catalog.md` + workflow 入口 §0.4 Trigger Mode Matrix + `../../specs-write/protocols/gate-dag-protocol.md`（若新增 Gate / DAG）。
- 新增 RWSE Gate 类型 → 同步更新 workflow 入口 §0.3 Hard-gate 命中条件 + `../../specs-write/protocols/gate-dag-protocol.md` HG-IRREV-*/ HG-AUDIT-* 命名空间。
- baseline 存储格式变更 → 同步 `baseline-store-protocol.md` §schema。
