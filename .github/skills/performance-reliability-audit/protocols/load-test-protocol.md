# 负载测试协议 (Load Test Protocol)

> 负载测试规则 / 工具 / RWSE Gate；`/performance-reliability-audit` Phase 4 跑这些规则。

---

## 1. 触发条件

进入 Phase 4 Load Test 的条件（任一命中）：

- spec NFR-PERF-* 含 `concurrency` 字段（如 "100 concurrent users"）
- spec NFR-PERF-* 含 `throughput` 字段（如 "10k RPS"）
- spec NFR-PERF-* 含 `sustained-load` 字段（如 "持续 30 分钟 5k RPS"）
- spec NFR-REL-* 含 `peak-load` / `failover` 场景
- 用户 explicit 请求 load test
- bug-audit 报告负载场景下性能 regression

不触发：仅 latency-p95 / memory / bundle-size / cold-start 单点 NFR（这些走 Phase 3 measure 即可）。

---

## 2. 环境分级

| 环境 | RWSE Gate | 默认运行许可 |
| ------ | ---------- | ------------- |
| **local / dev** | 无 | ✅ 可自动跑 |
| **CI** | 无 | ✅ 可自动跑（PR 验证 / scheduled） |
| **staging** | 无（前提：与生产隔离的数据 / 服务） | ✅ 可自动跑 |
| **preprod** | 无（前提：脱敏数据 + 隔离基础设施） | ✅ 可自动跑 |
| **production** | ✅ `HG-IRREV-LT` + `HG-AUDIT-PERF-LT` | ❌ 必须用户原话批准 |

**生产 load test 的高风险**：

- 调用真实付费服务（云服务 / SMS / email / 支付 gateway → 产生真实账单）
- 影响真实用户（共享基础设施 → 真实用户体验下降）
- 触发真实 alert / on-call（噪声化 SRE 流程）
- 触达真实数据库（写测试数据 → 污染生产）
- 触发外部依赖限流 / 封禁（Google API / Stripe）

---

## 3. RWSE Gate 流程（仅生产 load test）

```text

1. 检测 environment = production
2. State 切换：LOAD_TEST_PENDING_APPROVAL
3. 装配 RWSE packet（perf-rwse-lt-packet.md）:
   F-HG-1 Facts:
     - Test scenario: <场景描述>
     - Target: <production endpoint / service>
     - Duration: <时长>
     - Concurrency: <并发数>
     - RPS target: <目标 RPS>
     - Estimated cost: <服务 / API / 流量费用>
   F-HG-2 Impact:
     - Real users affected: <预估范围>
     - External services billed: <列出 + 预估金额>
     - Database writes: <真实写 vs 隔离 tenant>
     - Alerts triggered: <预期 alerts>
   F-HG-3 User quote: <留白等用户填>
   F-HG-4 Authorized scope: 仅本次 load test，本次 packet 范围内
   F-HG-5 Monitoring: <监控锚点 + on-call 通知>
   F-HG-6 Rollback: <如何提前终止 + 回滚步骤 + 清理测试数据>
   F-HG-7 Alternatives:
     - 已考虑 staging load test（拒绝理由：<具体>）
     - 已考虑 shadow traffic（拒绝理由：<具体>）
     - 已考虑 canary 期被动观测（拒绝理由：<具体>）
   F-HG-8 Verification:
     - 测试完成后如何验证
     - 重审触发条件

4. 展示给用户 + 等明确批准（CONFIRMED_ACTION 仅本次）
5. 用户批准 → 跑 load test
   - 实时监控（按 F-HG-5）
   - 触发 abort 条件 → 立即停止
   - 完成后清理测试数据
6. 用户拒绝 → REPORT_AND_STOP + 路由到 staging / preprod

```

---

## 4. 测试工具与版本

### 4.1 推荐工具

| 工具 | 用途 | 版本 pin |
| ------ | ------ | --------- |
| `k6` | API / endpoint 负载 | k6 v0.50.x |
| `artillery` | 多步骤场景 | artillery v2.x |
| `locust` | Python 友好场景 | locust v2.x |
| `wrk2` | 高 RPS 微基准 | wrk2 v4.x |
| `gatling` | JVM 项目复杂场景 | gatling v3.x |

工具版本必须 pinned；测试脚本必须 git 化。

### 4.2 测试脚本模板（k6）

```javascript
// scripts/perf/<scenario>.js
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '2m', target: 50 },   // ramp up
    { duration: '5m', target: 50 },   // sustained
    { duration: '2m', target: 100 },  // ramp up to peak
    { duration: '5m', target: 100 },  // sustained peak
    { duration: '2m', target: 0 },    // ramp down
  ],
  thresholds: {
    'http_req_duration': ['p(95)<800'],  // 与 NFR-PERF budget 一致
    'http_req_failed': ['rate<0.01'],
  },
};

export default function () {
  const res = http.get('https://staging.example.com/api/<endpoint>');
  check(res, { 'status 200': (r) => r.status === 200 });
  sleep(1);
}
```

测试脚本路径约定：`scripts/perf/<scenario>.js`（k6）/ `scripts/perf/<scenario>.yml`（artillery）/ `scripts/perf/<scenario>.py`（locust）。

---

## 5. 测试场景类型

| 类型 | 目标 | 持续时间 | 关注指标 |
| ------ | ------ | --------- | --------- |
| **Smoke** | 验证基础可用性 | 1-3 分钟 | 错误率 / 200 比例 |
| **Load** | 标定正常负载下行为 | 10-30 分钟 | latency p95/p99 / throughput |
| **Stress** | 找系统极限 / saturation point | 持续到饱和 | saturation point / failure mode |
| **Spike** | 突发流量验证（社交转发 / 营销活动） | 5-10 分钟 | 恢复时间 / 队列堆积 |
| **Sustained** | 长期稳定性（内存泄漏 / 连接池） | 数小时-数天 | memory growth / connection 泄漏 |
| **Soak** | 极长期运行 | 数天-数周 | GC 抖动 / fragment / 累积错误 |

每条 NFR-PERF 决定跑哪些场景：

- `concurrency` → Load + Stress
- `throughput` → Load + Stress + Spike
- `sustained-load` → Sustained + Soak
- `peak-load` → Spike

---

## 6. load-test-report.md 模板

```markdown
## 负载/压力测试报告 (Load Test Report) — PERF-<slug>-<date>-<seq>

## 测试配置 (Test Configuration)

- 场景分类 (Scenario): <负载 (load) | 压力 (stress) | 突发 (spike) | 持续 (sustained) | 浸泡 (soak)>
- 运行环境 (Environment): <本地 (local) | CI | 测试环境 (staging) | 预发环境 (preprod) | 生产环境 (production)>
- 测试工具 (Tool): k6 v0.50.0
- 测试脚本 (Script): scripts/perf/oauth-login.js (git sha: abc123)
- 持续时长 (Duration): 16 minutes
- 递增走势 (Ramp profile): 0 → 50 (2min) → 50 (5min) → 100 (2min) → 100 (5min) → 0 (2min)

## 真实世界副作用门禁状态 (RWSE Gate Status)

- 环境 = 生产环境 (Environment = production): ✅ 命中 (HIT HG-IRREV-LT + HG-AUDIT-PERF-LT)
- 用户原话授权 (User quote): "我批准 2026-05-24 16:00 的 oauth 生产 load test"
- 授权范围 (Authorized scope): 仅本次 load test
- 授权审批时间 (Approval timestamp): 2026-05-24T15:55:00Z
- 预检准备工作 (Pre-flight checks): <列出 + 通过状态>

## 吞吐率性能曲线 (Throughput Curve)

- 50 并发 (50 concurrent): 250 RPS, p95=300ms, errors 0%
- 100 并发 (100 concurrent): 500 RPS, p95=580ms, errors 0%
- 150 并发 (150 concurrent): 700 RPS, p95=820ms, errors 0%
- 200 并发 (200 concurrent): 750 RPS, p95=1500ms, errors 2% ← 达到饱和状态 (saturation)
- 250 并发 (250 concurrent): 750 RPS, p95=3000ms, errors 15% ← 出现性能降级 (degraded)

## 饱和临界点 (Saturation Point)

- RPS 天花板 (RPS ceiling): ~750 RPS
- 饱和时并发用户数 (Concurrent users at saturation): 200
- 故障失效表现 (Failure mode): 当并发用户 > 250 时响应超时 (response > 3s) 并出现 5xx 错误

## 性能非功能需求比对结论 (NFR-PERF Verdict)
|  | 性能契约 (NFR-PERF) | 指标预算 (Budget) | 峰值测绘值 (Measured peak) | 结论 (Verdict) |  |
|  | ---------- | -------- | ----------------- | --------- |  |
|  | NFR-PERF-001 p95 延迟 (latency-p95) | 800ms | 580ms @ 100 concurrent | PASS |  |
|  | NFR-PERF-002 吞吐率 (throughput) | 500 RPS | 750 RPS saturation | PASS |  |

## 测试发现与审计 (Findings)

- 系统在 100 concurrent / 500 RPS 下表现良好（target NFR）
- saturation point 750 RPS 留有 50% 余量
- 250 concurrent 触发 5xx；建议增加 connection pool 上限（已记 mitigation）

## 资源清理与费用开支 (Cleanup)

- 测试数据租户 (测试数据 tenant): load-test-tenant-2026-05-24
- 数据清理状态 (Cleanup status): ✅ 已删除（脚本：scripts/perf/cleanup-tenant.sh）
- 计费开支评估 (Billing impact): ~$2.50（Google API quota / Stripe sandbox）

## 缓解改善任务 (Mitigation Tasks)

- TASK-LT-1: 增加 connection pool 上限（current 50 → recommend 100）
- TASK-LT-2: 添加 connection backoff 策略

```

---

## 7. 失败模式

| 失败模式 | 描述 | 处置 |
| --------- | ------ | ------ |
| **Saturation point < NFR target** | 系统饱和 RPS 低于 spec 要求 | `MITIGATION_REQUIRED` + 路由 `/architecture-audit` |
| **Failure mode = OOM** | 饱和时内存崩溃 | `BENCHMARK_BLOCKED`（OOM 不能 ignore） |
| **Failure mode = connection 泄漏** | sustained 期连接增长不释放 | `MITIGATION_REQUIRED` + 路由 `/bug-audit` |
| **Failure mode = data corruption** | 高并发下数据写错 | `BENCHMARK_BLOCKED` + 路由 `/data-migration-safety` + `/bug-audit` |
| **External rate limited** | 外部依赖限流（Google / Stripe） | 调整 ramp profile + 与依赖方协调 quota |
| **Test infrastructure crash** | k6 / artillery 进程崩 | 工具配置问题，不算被测系统失败 |

---

## 8. 修订规则

- 本文修订必须同 PR 修订 `audit-protocol.md` Phase 4 + `../references/perf-checks-catalog.md` §3。
- 推荐工具版本变更 → 不需 RWSE Gate 但需 changelog 记录 + 测试脚本兼容性验证。
- 新增环境分级（如 staging-prod-shadow）→ 必须明确 RWSE Gate 是否需要。
- 测试脚本模板变更 → 同步现有 scripts/perf/ 全量更新。
