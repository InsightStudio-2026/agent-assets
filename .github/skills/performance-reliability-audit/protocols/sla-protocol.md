# SLA 协议 (SLA Protocol)

> SLA 定义 / 上调下调 RWSE Gate / 外部承诺同步规则；`/performance-reliability-audit` Phase 6 跑这些规则。

---

## 1. SLO ↔ SLA 区分（关键术语）

| 术语 | 定义 | 受众 | 调整权限 |
| ------ | ------ | ------ | --------- |
| **SLI**（Service Level Indicator） | 可观测的性能指标（latency / availability / error rate） | 内部团队 | 自由调整测量方式 |
| **SLO**（Service Level Objective） | 内部目标（如 99.9% 可用性 / p95 < 200ms） | 内部团队 | 团队决定，不需外部批准 |
| **SLA**（Service Level Agreement） | 外部承诺（合约 / 公开 API doc / 用户协议） | 客户 / 合约方 | ✅ **必须 RWSE Gate** |

**核心区别**：

- SLO 调整 = 内部决策，不影响外部
- SLA 调整 = 外部承诺变更，可能违约 / 影响合约 / 触发赔偿

### 1.1 典型 SLA 示例

```yaml
service: oauth-google-login
sla_commitments:
  availability:
    target: 99.5%
    measurement_window: monthly
    exclusions: [scheduled maintenance, force majeure]
    contractual_party: enterprise customers via service agreement
    breach_remedy: 1% credit per 0.1% below target
  
  latency_p95:
    target: < 1500ms
    measurement_window: weekly
    contractual_party: public API documentation
    breach_remedy: status page incident
  
  data_durability:
    target: 99.999999999% (11 9's)
    measurement_window: yearly
    contractual_party: data processing agreement (GDPR Art 28)
    breach_remedy: regulatory disclosure + data recovery
```

---

## 2. 触发条件

进入 Phase 6 SLA Review 的条件（任一命中）：

- spec NFR-PERF-*/ NFR-REL-* 含 `SLA` / `SLO` / `external commitment` 字段
- 用户 explicit 请求 SLA 审核
- 合约 / 服务协议变更 → 需要重审 SLA
- 多次违反 SLO → 评估是否需要调整 SLO 或 SLA
- bug-audit 报告 SLA 违约
- 新增外部客户 / 合约 → 评估 SLA 影响

---

## 3. sla-record.md 模板

```markdown
## 服务等级协议变动备案 (SLA Record) — PERF-<slug>-<date>-<seq>

## 审计范围 (Audit Scope)

- 特征/服务标识 (Feature / Service): <slug or service>
- SLA 审核触发条件 (SLA review trigger): 新增商业合约 (new contract) | 故障违约回溯 (breach review) | 例行刷新 (scheduled refresh) | 架构变更 (architecture change)

## 内部服务等级目标 (Internal SLOs)
|  | 指标名称 (SLI) | 目标值 (Target) | 测绘窗口 (Measurement Window) | 测绘事实源方法 (Method) |  |
|  | ----- | -------- | ------------------- | -------- |  |
|  | 可用性 (availability) | 99.95% | 按月 (monthly) | uptime 探针监控 |  |
|  | p95 延迟 (latency-p95) | < 1500ms | 按周 (weekly) | 负载均衡指标 LB metric |  |
|  | 接口错误率 (error-rate) | < 0.5% | 按小时 (hourly) | API 网关 gateway |  |

## 对外服务等级协议承诺 (External SLAs)
|  | 协议项 (SLA) | 协议指标 (Target) | 周期窗口 (Window) | 合约签署方 (Contractual Party) | 违约赔偿/救济方案 (Breach Remedy) | 最近审核日期 (Last Reviewed) |  |
|  | ----- | -------- | -------- | ------------------- | -------------- | --------------- |  |
|  | 可用性 (availability) | 99.5% | 按月 (monthly) | 企业客户 Enterprise customers | 降 0.1% 赔 1% credit (1% credit per 0.1% below) | 2026-01-15 |  |
|  | p95 延迟 (latency-p95) | < 2000ms | 按周 (weekly) | 公开 API 文档 Public API doc | 状态页登记故障 (Status page incident) | 2026-01-15 |  |
|  | 数据持久性 (data_durability) | 99.999999999% | 按年 (yearly) | 隐私合规协议 DPA (GDPR) | 依规向监管机构披露 (Regulatory disclosure) | 2025-12-01 |  |

## SLO ↔ SLA 偏差与一致性校验 (SLO ↔ SLA Consistency Check)
|  | 指标 (SLI) | 内部 SLO 目标 | 对外 SLA 承诺 | 缓冲裕度 (Margin) | 一致性结论 (Verdict) |  |
|  | ----- | ----------- | ----------- | -------- | --------- |  |
|  | 可用性 (availability) | 99.95% | 99.5% | 0.45% 安全裕度 | ✅ SLO 比 SLA 严格 |  |
|  | p95 延迟 (latency-p95) | < 1500ms | < 2000ms | 500ms 裕度 | ✅ SLO 比 SLA 严格 |  |
|  | 接口错误率 (error-rate) | < 0.5% | N/A | - | 仅设内部 SLO |  |

**关键不变量**：SLO 必须比 SLA 更严格（margin > 0），否则 spec 说一套实际另一套，违反 INV-PERF-SLA-1。

## 历史履约审计 (Compliance History)
|  | 周期 (Period) | 对外 SLA 承诺指标 | 实际测绘值 | 是否达标 (Met?) | 违约执行记录 (Breach Action) |  |
|  | -------- | ----------- | -------- | ------ | -------------- |  |
|  | 2026-04 | 可用性 99.5% | 99.92% | ✅ | - |  |
|  | 2026-03 | 可用性 99.5% | 99.45% | ❌ | 已发放 1% 违约 credit |  |
|  | 2026-02 | p95 延迟 < 2000ms | 1850ms | ✅ | - |  |

## 本轮 SLA 变动 (Change This Run)

- 变动类型 (Type): 不变 (unchanged) | 升级收紧 (upgrade) | 降级放宽 (downgrade)
- 旧承诺 (Old commitment): <old SLA>
- 新承诺 (New commitment): <new SLA>
- 变更原因 (Reason): <new contract | architecture change | breach correction>

## 真实世界副作用门禁状态 (RWSE Gate Status)

- SLA 收紧 (SLA upgrade): <N/A | HIT HG-IRREV-SLA + HG-AUDIT-PERF-SLA>
- SLA 放宽 (SLA downgrade): <N/A | HIT HG-IRREV-SLA + HG-AUDIT-PERF-SLA>
- 用户原话授权 (User quote): <留白等用户填>
- 外部通知发送状态 (External party notification): <未通知 / 已通知 / 待办>

## 推荐改善行动 (Recommended Actions)

- ...

```

---

## 4. RWSE Gate 流程（SLA 上调或下调）

### 4.1 SLA 上调（提高承诺）

**风险**：

- 倒逼代码 / 架构负担（达成更高承诺需投入）
- 测试基础设施成本上升
- 监控 / alert 阈值收紧
- 失败概率增加 → 违约赔偿风险

```text

1. 提议 SLA upgrade（新合约 / 客户要求 / 主动提升）
2. State 切换：SLA_CHANGE_PENDING_APPROVAL
3. 装配 RWSE packet（perf-rwse-sla-packet.md）:
   F-HG-1 Facts:
     - SLI: `<metric>`
     - Old SLA: <target + window>
     - New SLA: <target + window>
     - Improvement: <% / 数字差>
     - Contractual party: <列出>
     - Effective date: `<date>`
   F-HG-2 Impact:
     - Code/Architecture changes required: <列出>
     - Cost impact: <infra / monitoring / on-call>
     - Risk of breach increase: <评估>
     - Cascading effect on SLO: <SLO 必须更严>
   F-HG-3 User quote: <留白>
   F-HG-4 Authorized scope: 仅本次 SLA 调整
   F-HG-5 Monitoring: <新阈值 + alert 调整>
   F-HG-6 Rollback: <如何回退到旧 SLA + 通知合约方>
   F-HG-7 Alternatives:
     - 维持旧 SLA（拒绝理由）
     - 部分指标升级（拒绝理由）
     - 试运行期（拒绝理由）
   F-HG-8 Verification:
     - 升级后如何验证达成
     - 试运行期监控
4. 展示用户 + 等批准
5. 用户批准 → 执行升级
   - 更新公开文档 / 合约 / API doc
   - 通知合约方
   - 更新 monitoring 阈值
   - 更新 SLO（必须比新 SLA 更严格）
6. 用户拒绝 → REPORT_AND_STOP

```

### 4.2 SLA 下调（降低承诺）

**风险**：

- 违反原合约 → 赔偿 / 法律风险
- 客户信任度下降
- 隐藏服务质量退位（用户可能未察觉但实际降级）
- 合规风险（如 GDPR 数据可用性下调）

```text

1. 提议 SLA downgrade（架构限制 / 资源限制 / 误承诺更正）
2. State 切换：SLA_CHANGE_PENDING_APPROVAL
3. 装配 RWSE packet（perf-rwse-sla-packet.md）:
   F-HG-1 Facts:
     - SLI: `<metric>`
     - Old SLA: `<target>`
     - New SLA: `<target>`
     - Reduction: <% / 数字差>
     - Reason: <architecture | resource | correction | regulatory>
   F-HG-2 Impact:
     - Affected customers: <列出>
     - Contract breach risk: <列出 + 法律评估>
     - Compensation owed: <估算>
     - User experience degradation: <如何被感知>
     - Regulatory disclosure required: <yes/no + 时限>
   F-HG-3 User quote: <留白>
   F-HG-4 Authorized scope: 仅本次 SLA 调整
   F-HG-5 Monitoring: <新阈值 + alert 调整>
   F-HG-6 Rollback: <恢复旧 SLA 步骤>
   F-HG-7 Alternatives:
     - 不下调 + 投入资源达标（拒绝理由）
     - 仅对部分客户下调（拒绝理由）
     - 临时下调（拒绝理由）
   F-HG-8 Verification: <下调后监控>
4. 展示用户 + 等批准
5. 用户批准 → 执行下调
   - 更新合约 / API doc / 公开文档
   - 通知所有受影响合约方（**法律义务**）
   - 法律 / 合规审核
   - 准备赔偿（如适用）
   - 监控阈值同步调整
6. 用户拒绝 → REPORT_AND_STOP + 路由到 architecture-audit / 资源升级

```

---

## 5. 违约处置流程

### 5.1 检测违约

```text

监控信号 → SLI 实际 < SLA target → 触发 alert → /observability-incident
  → 经过事故响应 / 复盘 → 引用 sla-record.md
  → 决定：违约赔偿 + 触发 SLA review（spec-gate trigger）

```

### 5.2 违约处置 checklist

- [ ] 违约时段记录（开始 / 结束 / 持续）
- [ ] 违约影响范围（哪些客户 / 数据 / 区域）
- [ ] 赔偿计算（按合约 breach_remedy）
- [ ] 客户通知（按合约通知期）
- [ ] 监管披露（如适用）
- [ ] postmortem 关联到 sla-record.md
- [ ] 评估是否需要 SLA review（频繁违约 → 重新评估目标）

---

## 6. SLA 与其他 workflow 边界

| Workflow | 关系 |
| ---------- | ------ |
| `/performance-reliability-audit` | 主审计；定义 SLO；监督 SLA 达成 |
| `/observability-incident` | 监控 SLI；触发违约 alert；事故响应 |
| `/security-privacy-audit` | 安全相关 SLA（如数据可用性 / 加密） |
| `/release-deploy` | release 期 SLA 影响评估（canary 是否影响 SLA） |
| `/architecture-audit` | 重大 SLA 调整对架构的影响 |
| `/specs-write` | NFR-PERF / NFR-REL 中 SLA 字段定义 |

---

## 7. Invariants

| Invariant | 描述 |
| ----------- | ------ |
| INV-PERF-SLA-1 | SLO 必须比 SLA 更严格（safety margin > 0） |
| INV-PERF-SLA-2 | SLA 调整必须有合约方通知证据（packet F-HG-6） |
| INV-PERF-SLA-3 | SLA 下调必须有法律 / 合规审核记录 |
| INV-PERF-SLA-4 | SLA 违约必须触发 sla-record.md 更新（compliance history） |
| INV-PERF-SLA-5 | 不允许在 SLA review 外私下调整 SLA（必须走本 workflow） |

任一违反 → `R-CHK-PERF-SLA-*` FAIL。

---

## 8. 修订规则

- 本文修订必须同 PR 修订 `audit-protocol.md` Phase 6 + `../references/perf-checks-catalog.md` §5。
- 新增 SLA 类型（如 data residency / privacy SLA）→ 同步更新 sla-record.md 模板。
- breach_remedy 计算公式变更 → 必须法律审核 + 客户通知。
- SLO ↔ SLA 边界规则不允许变更（INV-PERF-SLA-1 是硬规则）。
