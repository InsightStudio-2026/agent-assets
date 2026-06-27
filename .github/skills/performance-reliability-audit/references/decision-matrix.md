---
description: "性能与可靠性审计工作流（/performance-reliability-audit）专属的触发判定、状态转换路由、状态权威与动作决策矩阵"
---

# 性能与可靠性审计决策矩阵（/performance-reliability-audit）

## 0. 触发与临界路由决策表

| ID | 前置条件 | 匹配动作 | 下一步/目标路由 | 源 / 备注 |
| ---- | ---------- | ---------- | ----------------- | ----------- |
| R-ROUTE-PRA-1 | 用户显式 `/performance-reliability-audit` | 启用 workflow | 进入 Phase 1 (Intake) | 显式入口 |
| R-ROUTE-PRA-2 | spec `NFR-PERF-*` 标记为 Active 且 Routed 到 `/performance-reliability-audit` | 启用 workflow | 进入 Phase 1 (Intake) | Spec 门禁触发 |
| R-ROUTE-PRA-3 | spec close-out 前缺失 perf gate packet（即 `R-RDY-10` 缺事实源） | 启用 workflow | 进入 Phase 1 (Intake) | 规格收尾期触发 |
| R-ROUTE-PRA-4 | `/release-deploy` 报告 `R-RDY-10` 缺事实源，或者发布 canary perf 超过性能阈值 | 启用 workflow | 进入 Phase 1 (Intake) | 发布与反馈倒序触发 |
| R-ROUTE-PRA-5 | `/bug-audit` 分流性能回归 Bug 并交接本 workflow | 启用 workflow | 进入 Phase 1 (Intake) | 缺陷审计引流 |
| R-ROUTE-PRA-6 | scheduled refresh 测量更新周期到达 | 启用 workflow | 进入 Phase 1 (Intake) | 定期例行测量 |
| R-ROUTE-PRA-7 | `NFR-PERF-*` 全部标记为 N/A，且无关键路径性能变更 | 停止并忽略 | 不启用本 workflow | 无性能变更 |
| R-ROUTE-PRA-8 | 仅有纯文档、纯测试、或纯配置的局部改动，且 `NFR-PERF` 并未触发 | 停止并忽略 | 不启用本 workflow | 局部无害变更 |
| R-ROUTE-PRA-9 | 系统状态不清、下一步推进方向不明 | 停止并重定向 | 路由至 `/project-steward` | 临界状态 1 |
| R-ROUTE-PRA-10 | 缺失母本或 L1 SSOT | 停止并重定向 | 路由至 `/project-inception` | 临界状态 2 |
| R-ROUTE-PRA-11 | 属于纯缺陷根因诊断（局部、具体 bug） | 停止并重定向 | 路由至 `diagnose` 技能 | 临界状态 3 |
| R-ROUTE-PRA-12 | 属于新功能、新需求开发、大重构落地 | 停止并重定向 | 路由至 `/specs-write` 与 `/specs-execute` | 临界状态 4 |
| R-ROUTE-PRA-13 | 逻辑简单明确且适合 TDD 验证 | 停止并重定向 | 路由至 `tdd` 技能或直接执行 | 临界状态 5 |

## 0.1 状态与路由汇总 (State / Route Summary)

| 状态 (State) | 判定 | 下一步 | Gate / DAG ID 映射 |
| ------- | ------ | -------- | --------------------- |
| `/performance-reliability-audit:PERF_SCOPE_MISSING` | 触发但 NFR-PERF 契约 / 测量命令 / 关键路径未定义 | 与用户对齐契约 + 回 `/specs-write` 修 §10.2 | `S-HG-3 GATE_PACKET_INCOMPLETE`（packet 装配缺前置） |
| `/performance-reliability-audit:TRIGGER_MODE_DETERMINED` | 已识别触发模式（spec-gate / scheduled / bug-handoff / canary-feedback / release-gate） | 进入 Phase 2 baseline | 创建 `DAG-N-AUDIT-{slug}-perf`（status: Trigger-Detected） |
| `/performance-reliability-audit:BASELINE_REQUIRED` | 新路径 / 新 NFR-PERF / refresh 到期 | 进入 Phase 2 baseline 建立 | `HG-AUDIT-PERF-BL`（baseline 缺失锁） |
| `/performance-reliability-audit:BASELINE_REFRESHED` | baseline 已建立或刷新（双部位：spec artifacts + perf-baseline/） | 进入 Phase 3 budget vs measure | DAG-N-AUDIT-*F-N-5 += baseline ref |
| `/performance-reliability-audit:BUDGET_VIOLATED` | measure command 输出超出 budget 上限 | 标记 violation；继续 Phase 4-7 直到全证据齐 | `HG-AUDIT-PERF-BUDGET` + 暂记 `S-HG-9` 候选 |
| `/performance-reliability-audit:LOAD_TEST_PENDING_APPROVAL` | 生产 load test 命中 RWSE Gate | 等用户批准；packet F-HG-1~8 装配 | `S-HG-4` + `HG-IRREV-LT`（生产副作用）+ `HG-AUDIT-PERF-LT` |
| `/performance-reliability-audit:CAPACITY_DOWNGRADE_PENDING_APPROVAL` | capacity 上限下调命中 RWSE Gate | 等用户批准；记录服务能力影响 | `S-HG-4` + `HG-IRREV-CAP` + `HG-AUDIT-PERF-CAP` |
| `/performance-reliability-audit:SLA_CHANGE_PENDING_APPROVAL` | SLA 上调（代码负担）/ 下调（隐藏降级）命中 RWSE Gate | 等用户批准；外部承诺需同步更新 | `S-HG-4` + `HG-IRREV-SLA` + `HG-AUDIT-PERF-SLA` |
| `/performance-reliability-audit:REGRESSION_DETECTED` | 与 baseline 对比超 regression 阈值（按严重性分类） | 按严重性 → MITIGATION_REQUIRED / WAITING_PERF_RISK_ACCEPTANCE / BENCHMARK_BLOCKED | DAG-N-AUDIT-* F-N-5 += regression list |
| `/performance-reliability-audit:BENCHMARK_BLOCKED` | 高危 regression（关键路径 p95 > budget × 1.5 或代际退化）阻塞 release | 阻塞；分流 `/specs-write` 或 `/architecture-audit` | `S-HG-9 GATE_FAILED` + `FA-HG-2`；阻塞 `/release-deploy` R-RDY-10 |
| `/performance-reliability-audit:MITIGATION_REQUIRED` | 中 / 高危 regression 需 mitigation task；不允许风险接受 | 创建 `/specs-write` mitigation task → `/specs-execute` 修复 | `S-HG-3 GATE_PACKET_INCOMPLETE`（待 mitigation） |
| `/performance-reliability-audit:WAITING_PERF_RISK_ACCEPTANCE` | 低危 regression 或 mitigation 成本不合理；用户原话裁决可接受 | 等用户原话 + 写入 risk-acceptance 记录 | `S-HG-4 WAITING_GATE_APPROVAL` + `HG-AUDIT-PERF-{slug}` packet |
| `/performance-reliability-audit:CANARY_FEEDBACK_REGRESSION` | release-deploy canary 期实时 metric 超阈值倒序触发本 workflow | 重跑 Phase 3-7 增量审计；不沿用旧 packet | DAG-N-AUDIT-{slug}-perf 重置；`HG-AUDIT-PERF-CANARY` 升级 |
| `/performance-reliability-audit:PERF_APPROVED` | 所有高 / 中危已 mitigation 或显式风险接受；Hard-gate 已批；perf gate packet 完整 | 输出 `perf-gate-packet.md` → `/release-deploy` R-RDY-10 | `S-HG-8 GATE_PASSED`；DAG-N-AUDIT-{slug}-perf Done |
| `/performance-reliability-audit:POST_AUDIT_REGRESSION_DETECTED` | 审计后代码变更 / 数据量变更 / 依赖升级引入新 regression | 重跑 Phase 2-7 增量审计；不沿用旧 packet | DAG-N-AUDIT-{slug}-perf 重置；`HG-AUDIT-PERF-*` 重新装配 |

## 0.2 状态权威与路由动作 (State Authority / Route Action)

- **State Authority**：`<feature>/perf-audit/baseline.json` + `perf-baseline/<scope>/baseline.json` + `regression-report.md` + `load-test-report.md` + `capacity-plan.md` + `sla-record.md` + `canary-feedback-log.md` + `perf-gate-packet.md` 是权威事实源；本表 State 只用于审计调度。
- **Route Action**：`进入 Phase / 重跑增量` = `CONTINUE_IN_WORKFLOW`；`等用户裁决 RWSE Gate / risk acceptance / 高危 regression` = `WAIT_FOR_USER`；`分流 / 报告并停止 / BENCHMARK_BLOCKED` = `REPORT_AND_STOP`，除非用户明确要求继续；`/performance-reliability-audit:PERF_APPROVED` 与 `/performance-reliability-audit:WAITING_PERF_RISK_ACCEPTANCE` 用户裁决 = `CONFIRMED_ACTION`，但只授权本次 packet 范围内的风险接受 / Hard-gate；不继承到下次审计、其他 release、其他外部副作用、下游 workflow。

## 0.3 Hard-gate 命中条件（自动升级到对应 HG-IRREV-*）

| 条件 | 命中 Gate | 必须用户原话批准？ |
| ------ | ---------- | ------------------- |
| **生产环境 load test**（可能调用真实付费服务 / 影响真实用户 / 触达生产数据库） | `HG-IRREV-LT` + `HG-AUDIT-PERF-LT` | ✅ 必批 |
| **SLA 上调**（提高承诺 → 倒逼代码负担 / 影响外部合约） | `HG-IRREV-SLA` + `HG-AUDIT-PERF-SLA` | ✅ 必批 |
| **SLA 下调**（降低承诺 → 可能隐藏服务质量退位 / 影响用户预期） | `HG-IRREV-SLA` + `HG-AUDIT-PERF-SLA` | ✅ 必批 |
| **Capacity 上限下调**（限制实际服务能力 / 可能导致拒绝服务） | `HG-IRREV-CAP` + `HG-AUDIT-PERF-CAP` | ✅ 必批 |
| **Baseline 跨版本覆盖**（用新 baseline 替换旧 baseline → 可能遮盖渐变 regression） | `HG-AUDIT-PERF-BL-OVERWRITE` | ⚠️ 建议批，至少需 changelog 记录 |
| **Regression 阈值上调**（放宽 regression 判定 → 可能遮盖问题） | `HG-AUDIT-PERF-THRESHOLD` | ⚠️ 建议批 |
| **关键路径 p95 > budget × 1.5**或**代际退化** | `HG-AUDIT-PERF-REG` | ❌ 不允许 risk acceptance；必须修 |

## 0.4 Trigger Mode Matrix（决定 Phase 跳哪些）

| Trigger Mode | Phase 1 | Phase 2 baseline | Phase 3 budget | Phase 4 load test | Phase 5 capacity | Phase 6 SLA | Phase 7 regression | Phase 8 packet |
| -------------- | --------- | ------------------ | ---------------- | ------------------- | ------------------ | ------------- | --------------------- | ---------------- |
| `spec-gate`（spec close-out 前） | ✅ | ✅（新建或 refresh） | ✅ | 按需（NFR-PERF 标载荷场景） | 按需（NFR-PERF 标 capacity 场景） | 按需（NFR-PERF 标 SLA 场景） | ✅ | ✅ |
| `scheduled refresh`（周期触发） | ✅ | ✅（refresh 全部） | ✅ | ❌（除非 NFR 配置） | ❌ | ❌ | ✅ | ✅（仅 refresh 类 packet） |
| `bug-audit handoff`（regression bug） | ✅ | ❌（用现有 baseline） | ✅（仅相关路径） | ❌ | ❌ | ❌ | ✅ | ✅ |
| `canary-feedback`（生产 canary 倒序） | ✅ | ❌（用现有 baseline） | ✅ | ❌ | ❌ | ❌ | ✅（高速增量） | ✅（标 CANARY_FEEDBACK_REGRESSION） |
| `release-gate`（release-deploy 调） | ✅ | ✅（确认未过期） | ✅ | 按需 | 按需 | 按需 | ✅ | ✅ |
| `user explicit`（用户显式调用） | ✅ | ✅（建议 refresh） | ✅ | 按需 + 询问 | 按需 + 询问 | 按需 + 询问 | ✅ | ✅ |

## 0.5 Resume Source（中断恢复事实源）

| Resume Need | 事实源 | 下一步判定 |
| ------------- | -------- | ------------ |
| 审计是否已立项 | `docs/specs/<slug>/perf-audit/` 或 `<slug>/perf-audit/charter.md` | 缺则 `/performance-reliability-audit:PERF_SCOPE_MISSING` |
| Trigger Mode 是否识别 | `<slug>/perf-audit/trigger-mode.md` | 缺则回 Phase 1 |
| Baseline 是否就绪 | `<slug>/perf-audit/baseline.json` + `perf-baseline/<scope>/baseline.json` | 任一缺 → `/performance-reliability-audit:BASELINE_REQUIRED` |
| Budget vs Measure 是否完成 | `<slug>/perf-audit/measure-report.md` | 缺则回 Phase 3 |
| Load Test / Capacity / SLA 是否完成（若需） | `load-test-report.md` / `capacity-plan.md` / `sla-record.md` | 任一缺则按对应 Phase 续跑 |
| Regression Diff 是否计算 | `<slug>/perf-audit/regression-report.md` | 缺则回 Phase 7 |
| RWSE Gate 用户原话 | 同一轮用户原话 + F-HG-3 引用 | 缺则保持对应 PENDING_APPROVAL state |
| Canary Feedback 是否同步 | `<slug>/perf-audit/canary-feedback-log.md` | 若 release-deploy canary 期反馈 → 回 Phase 7 增量 |
