# 容量规划协议 (Capacity Planning Protocol)

> 容量规划规则；`/performance-reliability-audit` Phase 5 跑这些规则。决策来源：第 4 问"capacity 上限下调命中 RWSE Gate"。

---

## 1. 触发条件

进入 Phase 5 Capacity Planning 的条件（任一命中）：

- spec NFR-PERF-* 含 `capacity` 字段（如 "支持 100k DAU"）
- spec NFR-PERF-* 含 `multi-region` / `multi-tenant` 隔离需求
- spec NFR-REL-* 含 `failover` / `disaster-recovery` 容量场景
- 用户增长曲线预测显示当前容量将在 6 个月内耗尽
- 用户 explicit 请求 capacity planning
- bug-audit 报告容量耗尽相关 bug（429 / OOM / connection refused）

不触发：单 feature 内不涉及容量上限的 NFR-PERF。

---

## 2. 容量维度

| 维度 | 单位 | 测量方式 |
| ------ | ------ | --------- |
| **DAU / MAU** | 用户数 | 业务 metric |
| **QPS / RPS** | 请求 / 秒 | API gateway / load balancer metric |
| **DB connections** | 连接数 | DB pool monitor |
| **DB storage** | GB / TB | DB monitoring |
| **Storage IOPS** | IO / 秒 | 云存储 metric |
| **Memory** | GB | 进程 / 容器 metric |
| **Compute (vCPU)** | core-hours | 云资源 metric |
| **Network bandwidth** | GB/s | 出向 / 入向 monitor |
| **External API quota** | calls / 时间窗 | 外部服务 dashboard |
| **Tenant isolation** | tenant 数 | 多租户场景 |

每个维度独立评估；瓶颈往往在最先饱和的维度。

---

## 3. capacity-plan.md 模板

```markdown
## 容量规划与扩容对齐报告 (Capacity Plan) — PERF-<slug>-<date>-<seq>

## 审计范围 (Audit Scope)

- 审计特征/服务 (Feature / Scope): <slug or scope>
- 已评估容量维度 (Capacity dimensions assessed): [DAU, QPS, DB, Memory, External API quota]
- 预测周期 (Forecast horizon): <例如：未来 12 个月 (next 12 months)>

## 当前容量状态 (Current State)
|  | 容量维度 (Dimension) | 容量上限 (Ceiling) | 当前使用量 (Current usage) | 容量水位 (Utilization) |  |
|  | ----------- | --------- | --------------- | ------------- |  |
|  | 每日活跃用户数 (DAU) | 100k | 65k | 65% |  |
|  | QPS 峰值 (QPS peak) | 10k | 6.5k | 65% |  |
|  | 数据库连接数 (DB connections) | 200 (pool) | 120 avg / 180 peak | 60% / 90% |  |
|  | 数据库存储空间 (DB storage) | 500 GB | 380 GB | 76% |  |
|  | 节点内存开销 (Memory per node) | 8 GB | 5.5 GB avg / 7.2 GB peak | 69% / 90% |  |
|  | 外部 API 频次 (External API) | 100M/month quota | 80M/month | 80% |  |

## 测算方法论 (Computation Methodology)

- DAU: 业务 dashboard 30 天滑动窗口
- QPS: load balancer p95 RPS metric
- DB connections: pool monitor + connection age
- DB storage: 实测 + 1.5x 物理安全缓冲 (safety margin)
- Memory: container resource usage + GC overhead
- External API: 外部服务 dashboard

## 业务增长预测 (Growth Forecast)
|  | 容量维度 (Dimension) | 3 个月后 (3 month) | 6 个月后 (6 month) | 12 个月后 (12 month) | 预测方法依据 (Method) |  |
|  | ----------- | --------- | --------- | ---------- | -------- |  |
|  | DAU | 80k | 100k | 130k | 历史增长率 + 营销计划 |  |
|  | QPS | 8k | 10k | 13k | DAU × 平均 RPM/user |  |
|  | DB storage | 460 GB | 540 GB | 700 GB | 写入速率 × 时间 + 数据保留期 |  |
|  | External API | 96M | 120M | 156M | DAU × OAuth 调用率 |  |

## 预计耗尽点 (Forecasted Exhaustion)

- DAU: 6 个月后达到 100% 负荷
- QPS: 6 个月后达到 100% 负荷
- DB storage: 4 个月后达到 100% 负荷 ← 最先饱和
- External API: 3 个月后耗尽额度（**最紧迫**）

## 弹性扩容触发阈值 (Scaling Triggers)

- DAU > 80k → 启动水平扩展评估 (horizontal scaling)
- QPS > 8k → 启动缓存与批量处理优化 (caching / batch)
- DB storage > 80% → 启动冷数据归档与分表分库 (archival / partitioning)
- DB connections peak > 90% → 增加连接池上限 pool 上限
- External API > 70% quota → 提前与供应商（如 Google）协调配额升级

## 推荐改善行动 (Recommended Actions)
|  | 优先级 (Priority) | 行动项内容 (Action) | 责任人 (Owner) | 截止日期 (Due) |  |
|  | ---------- | -------- | ------- | ----- |  |
|  | 致命 (Critical) | 与 Google 协调 OAuth quota 升级到 200M/month | infra | 2 weeks |  |
|  | 高 (High) | DB partitioning（按 tenant_id 分区） | data | 4 weeks |  |
|  | 中 (Medium) | Add caching layer for /auth endpoint | backend | 8 weeks |  |
|  | 低 (Low) | 评估 multi-region 部署 | architecture | 12 weeks |  |

## 真实世界副作用门禁状态 (RWSE Gate Status)

- 容量上限限制 (Capacity ceiling) 调整: <下调？上调？维持？>
- 若下调：HG-IRREV-CAP + HG-AUDIT-PERF-CAP 命中 (HIT)
- 用户原话授权 (User quote): <留白等用户填>
- 受影响的用户/租户 (Affected users / tenants): <列出>
- 故障回滚方案 (Rollback): <恢复原有容量上限的步骤>

```

---

## 4. RWSE Gate 流程（仅 capacity 上限下调）

### 4.1 触发条件

capacity 上限**下调**触发 RWSE Gate；上调或维持不触发（上调通常是好事，维持是默认）。

下调场景：

- 资源费用控制 → 缩减实例数 / 套餐降级
- 架构重构 → 临时容量限制
- 安全 / 隔离要求 → 限制单租户上限
- 误标定 → 修正过高的 ceiling 标识

### 4.2 流程

```text

1. capacity-plan.md 决议下调 ceiling
2. State 切换：CAPACITY_DOWNGRADE_PENDING_APPROVAL
3. 装配 RWSE packet（perf-rwse-cap-packet.md）:
   F-HG-1 Facts:
     - Dimension: <DAU | QPS | DB connections | ...>
     - Old ceiling: <数字 + 单位>
     - New ceiling: <数字 + 单位>
     - Reduction: <% 下调>
     - Reason: <资源 / 架构 / 安全 / 修正>
   F-HG-2 Impact:
     - Affected users: <预估范围>
     - Affected tenants: <列出>
     - Service degradation: <如何被用户感知>
     - Revenue impact: <如适用>
   F-HG-3 User quote: <留白>
   F-HG-4 Authorized scope: 仅本次 capacity 调整，本次 packet 范围内
   F-HG-5 Monitoring: <下调后监控锚点 + alert 阈值同步调整>
   F-HG-6 Rollback: <恢复 ceiling 步骤 + 资源恢复时长>
   F-HG-7 Alternatives:
     - 不下调（拒绝理由）
     - 部分下调（拒绝理由）
     - 临时下调（拒绝理由）
   F-HG-8 Verification: <下调后如何验证服务正常 + 监控阈值>

4. 展示给用户 + 等明确批准
5. 用户批准 → 执行下调
   - 通知受影响用户 / 租户（如适用）
   - 同步更新 monitoring / alert / SLA 文档
   - 通知 on-call
6. 用户拒绝 → REPORT_AND_STOP + 路由到 architecture-audit

```

---

## 5. Multi-region / Multi-tenant 容量

### 5.1 Multi-region

跨区域容量必须独立计算每个 region：

- region 内总容量 = 该 region 计算 / 存储 / 网络上限
- failover 时 region 之间是否能承接对方流量？
- 区域间数据同步带宽是否成为瓶颈？

每个 region 一份 capacity-plan；汇总到一个 multi-region-capacity-plan.md。

### 5.2 Multi-tenant 隔离

| 隔离层级 | 容量计算 |
| --------- | --------- |
| **Shared infrastructure** | 总容量 / 租户数 = 平均；但需考虑 noisy neighbor |
| **Logical isolation**（per-tenant DB schema） | 每租户上限独立 |
| **Physical isolation**（per-tenant cluster） | 每租户独立计算 |

跨租户容量上限调整必须考虑：

- 是否影响其他租户（共享资源）
- 单租户上限调整是否需用户批准（合约义务）

---

## 6. 容量监控锚点

| 维度 | 监控信号 | Alert 阈值 |
| ------ | --------- | ---------- |
| DAU | 业务 dashboard | > 80% ceiling |
| QPS | LB p95 metric | > 80% ceiling |
| DB connections | pool monitor | peak > 90% |
| DB storage | DB monitoring | > 80% |
| Memory | container | peak > 85% |
| External API quota | dashboard polling | > 70% monthly |

NFR-OBS-* 路由 → `/observability-incident` 写 alert / runbook。

---

## 7. 修订规则

- 本文修订必须同 PR 修订 `audit-protocol.md` Phase 5 + `../references/perf-checks-catalog.md` §4。
- 容量维度新增 → 同步 baseline.json schema（measure_environment / metrics）。
- 增长预测方法变更 → 必须文档化（数据来源 / 模型）；不允许"凭直觉"预测。
- 多 region / 多 tenant 容量计算变更 → 必须同步 architecture-audit 验证一致性。
