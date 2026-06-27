---
description: "可观测性与事故响应工作流（/observability-incident）专属的触发判定、状态转换路由、状态权威与动作决策矩阵"
---

# 可观测性与事故响应决策矩阵（/observability-incident）

## 0. 触发与临界路由决策表

| ID | 前置条件 | 匹配动作 | 下一步/目标路由 | 源 / 备注 |
| ---- | ---------- | ---------- | ----------------- | ----------- |
| R-ROUTE-OBS-1 | 用户显式 `/observability-incident` | 启用 workflow | 进入 Phase 1（含主线分流） | 显式入口 |
| R-ROUTE-OBS-2 | 线上告警、真实用户受影响、生产错误率上升、核心功能路径不可用 | 启用 workflow | 进入 Incident Response 主线 | 生产事故响应 |
| R-ROUTE-OBS-3 | `/release-deploy:POST_DEPLOY_REGRESSION_NEEDS_INCIDENT` 信号触发 | 启用 workflow | 进入 Incident Response 主线 | 发布回归联动 |
| R-ROUTE-OBS-4 | 缺失 runbook、缺失 SLO 或缺失告警规则 | 启用 workflow | 进入 Observability Setup 主线 | 建设期触发 |
| R-ROUTE-OBS-5 | 应用发布上线后，需要观察窗口（feature flag / canary）进行指标监控 | 启用 workflow | 进入 Observability Setup 主线（轻量监控） | 发布观察期 |
| R-ROUTE-OBS-6 | `/release-deploy` 报告 `R-RDY-7` 缺少事实源（可观测性不完备） | 启用 workflow | 进入 Observability Setup 主线 | 发布准备期 |
| R-ROUTE-OBS-7 | 属于纯本地测试失败、或者未上线功能的普通本地 bug（不涉及线上事故或可观测性基础） | 停止并重定向 | 路由至 `/bug-audit` 或 `/specs-execute` | 本地缺陷分流 |
| R-ROUTE-OBS-8 | 系统状态不清、下一步推进方向不明 | 停止并重定向 | 路由至 `/project-steward` | 临界状态 1 |
| R-ROUTE-OBS-9 | 缺失母本或 L1 SSOT | 停止并重定向 | 路由至 `/project-inception` | 临界状态 2 |
| R-ROUTE-OBS-10 | 属于纯缺陷根因诊断（局部、简单、且影响面已知） | 停止并重定向 | 路由至 `diagnose` 技能 | 临界状态 3 |
| R-ROUTE-OBS-11 | 逻辑简单明确且适合 TDD 验证 | 停止并重定向 | 路由至 `tdd` 技能或直接执行 | 临界状态 5 |

## 0.1 状态与路由汇总 (State / Route Summary)

| 状态 (State) | 主线 (Lane) | 判定 | 下一步 | Gate / DAG ID 映射 |
| ------- | ------ | ------ | -------- | --------------------- |
| `/observability-incident:OBSERVABILITY_MISSING` | Setup | 可观测性基线缺；signals 面 / SLO / alerts / runbook 任一未建 | 进入 Phase 2 SIGNALS_INVENTORIED | `S-HG-3 GATE_PACKET_INCOMPLETE`；预装配 `HG-OPS-{repo}-observability` |
| `/observability-incident:SIGNALS_INVENTORIED` | Setup | 13 信号面盘点完成（latency / traffic / errors / saturation / 业务指标 / IDs / tracing / health checks） | 进入 Phase 3 SLO_DRAFTED | DAG-N-AUDIT-{repo}-observability F-N-5 += signals inventory |
| `/observability-incident:SLO_DRAFTED` | Setup | SLO 草拟（按核心用户路径定义 SLI + SLO 目标 + 错误预算） | 进入 Phase 4 ALERT_RULES_DRAFTED | DAG-N-AUDIT-*F-N-5 += SLO |
| `/observability-incident:ALERT_RULES_DRAFTED` | Setup | 告警规则草拟（阈值 / 窗口 / 严重性分级 / 通知对象） | 进入 Phase 5 RUNBOOK_REQUIRED | DAG-N-AUDIT-* F-N-5 += alert rules |
| `/observability-incident:RUNBOOK_REQUIRED` | Setup | 每个告警必须配 runbook（定位 / 降级 / 回滚 / 用户通知步骤）；缺则阻塞 | 草拟 runbook → `/observability-incident:OBSERVABILITY_READY` 或 `/observability-incident:OBSERVABILITY_GATE_BLOCKED` | `S-HG-3`；packet 装配缺 runbook |
| `/observability-incident:OBSERVABILITY_READY` | Setup | signals + SLO + alerts + runbook 全齐；输出 observability gate packet | 交付 `/release-deploy:R-RDY-7` 或返回 `/project-steward` | `S-HG-8 GATE_PASSED`；DAG-N-AUDIT-{repo}-observability Done |
| `/observability-incident:OBSERVABILITY_GATE_BLOCKED` | Setup | release 前 observability 未达 DoD（核心路径无日志 / 错误率指标 / 关键依赖无 timeout-retry-fallback） | 阻塞 release；分流 `/specs-write` 或 `/specs-execute` 补齐 | `S-HG-9 GATE_FAILED`；阻塞 `/release-deploy:R-RDY-7` |
| `/observability-incident:INCIDENT_DECLARED` | Incident | 事故宣告（含严重性 P0~P3 / 影响面 / 起始时间） | 进入 Phase 6 MITIGATION_IN_PROGRESS | 创建 `DAG-N-INCIDENT-{slug}-{incident-id}`（status: Declared）；触发 `HG-INCIDENT-{slug}-{incident-id}` |
| `/observability-incident:INCIDENT_USER_NOTIFICATION_PENDING` | Incident | 事故影响用户 → 必须用户通知 / 状态页更新 | 等用户批准通知文案 + 通道 | `S-HG-4 WAITING_GATE_APPROVAL` + `HG-IRREV-003`（对外通信）+ `HG-INCIDENT-*`；F-HG-3 必含通知文案原话 |
| `/observability-incident:MITIGATION_IN_PROGRESS` | Incident | 正在止血（降级 / 回滚 / feature flag 关 / hotfix 部署） | 监控止血效果；命中 Hard-gate 升级；止血完成 → INCIDENT_RESOLVED_PENDING_POSTMORTEM | DAG-N-INCIDENT-*status: Mitigating |
| `/observability-incident:PROD_DEGRADATION_PENDING_APPROVAL` | Incident | 生产降级 / rollback / 大范围 feature flag 关闭命中 Hard-gate | 等用户批准 | `S-HG-4` + `HG-IRREV-004`（生产权限变更）或 `HG-IRREV-001`（如涉数据）+ `HG-INCIDENT-*`；R-INH-3 不继承 |
| `/observability-incident:INCIDENT_RESOLVED_PENDING_POSTMORTEM` | Incident | 止血完成（核心指标恢复绿）；待复盘 | 进入 Phase 7 POSTMORTEM_REQUIRED | DAG-N-INCIDENT-* status: Resolved |
| `/observability-incident:POSTMORTEM_REQUIRED` | Incident | 必填 postmortem（时间线 / 影响面 / 根因 / 修复项 / 防复发项）；P0/P1 强制 | 草拟 postmortem.md + mitigation task → `/observability-incident:POSTMORTEM_COMPLETE` | `S-HG-3`（packet 装配缺 postmortem 时阻塞 closure） |
| `/observability-incident:POSTMORTEM_COMPLETE` | Incident | postmortem 已批准 + mitigation task 已 handoff（`/specs-write` 或 `/bug-audit`） | 报告 `/observability-incident:POSTMORTEM_COMPLETE` 后返回 `/project-steward` | `S-HG-8 GATE_PASSED`；DAG-N-INCIDENT-* Done；F-N-10 += postmortem + mitigation list |

## 0.2 状态权威与路由动作 (State Authority / Route Action)

- **State Authority**：signals-inventory.md / slo.md / alert-rules.md / runbook-{path}.md / incident-report.md / postmortem.md / observability-gate-packet.md 是权威事实源；本表 State 只用于流程调度。监控系统实际数据流 + 告警平台是运行时事实源。
- **Route Action**：`进入 Phase / 持续止血 / 草拟文档` = `CONTINUE_IN_WORKFLOW`；`等用户批准用户通知 / 生产降级 / postmortem 复审` = `WAIT_FOR_USER`；`分流 / 报告并停止 / OBSERVABILITY_GATE_BLOCKED` = `REPORT_AND_STOP`，除非用户明确要求继续；`/observability-incident:INCIDENT_USER_NOTIFICATION_PENDING` 与 `/observability-incident:PROD_DEGRADATION_PENDING_APPROVAL` 用户批准 = `CONFIRMED_ACTION`，但只授权本次事故范围的对外通信 / 生产降级 / rollback；不继承到下次事故 / 其他范围 / 后续 release。

## 0.3 Hard-gate 命中条件（自动升级到 HG-IRREV-*）

| 条件 | 命中 Gate |
| ------ | ---------- |
| 事故用户通知（邮件 / 短信 / push / 站内信批量发送） | `HG-IRREV-003`（对外通信）+ `HG-INCIDENT-*` |
| 外部状态页更新（status page / 公告） | `HG-IRREV-003` + `HG-INCIDENT-*` |
| 生产降级（流量切流 / 服务降级 / 限流加严） | `HG-IRREV-004` + `HG-INCIDENT-*` |
| 生产 rollback（代码 / 数据 / 配置） | `HG-IRREV-001` 或 `HG-IRREV-002` 或 `HG-IRREV-004`（按操作类型）+ 启 `/release-deploy` rollback 链 |
| Feature flag 大范围关闭 / 启 | `HG-RELEASE-*`（事故场景）+ `HG-INCIDENT-*` |
| 紧急 hotfix 部署（绕过常规 release 流程） | `HG-IRREV-*` 候选；同时启 `/release-deploy` 紧急路径 |

## 0.4 触发模式矩阵 (Trigger Mode Matrix)

详细判定逻辑见 `../protocols/signals-runbook-protocol.md` 极其衍生。

## 0.5 中断恢复事实源 (Resume Source)

| 恢复需求 (Resume Need) | 事实源 | 下一步判定 |
| ------------- | -------- | ------------ |
| 当前主线 | 触发判定上下文 + 已有 artifact | Setup 主线 / Incident 主线 |
| Signals / SLO / Alerts / Runbook 状态 | `<repo>/observability/` 或 `docs/specs/<slug>/observability/` | 任一缺 → 续跑对应 Phase |
| 当前事故是否声明 | DAG-N-INCIDENT-*节点 + incident-report.md | 已声明 → `/observability-incident:INCIDENT_DECLARED` 续跑 |
| 用户通知 / 状态页是否已批 | 同一轮用户原话 + F-HG-3 引用 | 缺则保持 `/observability-incident:INCIDENT_USER_NOTIFICATION_PENDING` |
| 止血是否完成 | 核心指标 + 用户报告 + DAG-N-INCIDENT-* status | 恢复绿 → `/observability-incident:INCIDENT_RESOLVED_PENDING_POSTMORTEM` |
| Postmortem 是否完成 | postmortem.md + mitigation handoff 记录 | 缺则保持 `/observability-incident:POSTMORTEM_REQUIRED` |
