---
name: observability-incident
description: 可观测性与事故响应：让线上异常可发现 / 可分级 / 可止血 / 可复盘；产出 observability gate packet，事故用户通知 / 生产降级 / rollback / 状态页更新必须用户批准。
argument-hint: "什么事故或需要什么可观测性基线？"
disable-model-invocation: true
---


# /observability-incident · 可观测性与事故响应

**定位**：双主线 workflow——

- **Observability Setup 主线**：发布前 / 平时建立可观测性基线（signals / SLO / alerts / runbook），输出 observability gate packet 给 `/release-deploy:R-RDY-7`。
- **Incident Response 主线**：线上事故发生时分级、止血、复盘，配合 `/release-deploy:POST_DEPLOY_REGRESSION_NEEDS_INCIDENT` 下游联动。

**边界**：只做可观测性建设 + 事故响应；不替代 `/specs-execute` 修复实现、不替代 `/bug-audit` 根因诊断、不替代 `/release-deploy` 真实 deploy / rollback 命令、不替代 `/security-privacy-audit` 安全分析；告警系统建设 / SDK 接入归 `/specs-execute` 实现，本 workflow 只规定信号面、阈值、runbook 字段。

**斜杠命令**：`/observability-incident`

**配对前置 / 下游**：上游消费 release report / 用户影响描述 / 日志 / 指标 / trace；下游产出 observability gate packet 给 `/release-deploy`、incident report / postmortem 给 `/specs-write` mitigation task、根因诊断分流 `/bug-audit` 或 `diagnose`。

---

## 懒加载契约

- **MUST read**: `./decision-matrix.md`
- 开始判定或执行 Phase 流程前，必须完整懒加载上述细节。

---

## 1. 伴随文档

| 文档 | 角色 | 何时读 |
| ------ | ------ | -------- |
| `protocols/signals-runbook-protocol.md` | 13 信号面 + 事故材料面 + runbook 模板（R-OBS-*） | Phase 2-5（Setup 主线） |
| `protocols/incident-response-protocol.md` | 事故声明 / 止血 / Hard-gate / postmortem 协议（R-INC-*） | Phase 6-7（Incident 主线） |
| `../specs-write/protocols/gate-dag-protocol.md` | Gate / DAG ID 横切协议事实源 | State 表 + Phase 5/7 装配 packet |
| `../specs-write/protocols/entry-decision-tree.md §7.6` | R-RETURN-* 路由 | mitigation 回切 |

---

## 2. 阶段骨架（细节见伴随文档）

每个 Phase 入口的 **MUST read**指令是硬规则——不读 = 视为违反该 Phase 的可观测性与事故安全防御。

### 阶段 1 — 触发路由

按 §0 触发判定路由 Setup / Incident 主线。

### 阶段 2 — 观测指标清单设置（Setup）**MUST read**`protocols/signals-runbook-protocol.md`

按 `signals-runbook-protocol.md` 收集 13 信号面；输出 `signals-inventory.md`。

### 阶段 3 — 服务等级目标（SLO）起草设置**MUST read**`protocols/signals-runbook-protocol.md`

按核心用户路径定义 SLI + SLO 目标 + 错误预算；输出 `slo.md`。

### 阶段 4 — 告警规则设置（Setup）**MUST read**`protocols/signals-runbook-protocol.md`

草拟告警规则（阈值 / 窗口 / 严重性 / 通知对象 / 抑制策略）；输出 `alert-rules.md`。

### 阶段 5 — 应急手册与关卡文档设置（Setup）**MUST read**`protocols/signals-runbook-protocol.md`

每个告警必须配 runbook；按 `signals-runbook-protocol.md §runbook 模板`；全齐后装配 `HG-OPS-{repo}-observability` packet → 输出 `observability-gate-packet.md` → 交付 `/release-deploy:R-RDY-7`。

### 阶段 6 — 事故响应（事故主线）**MUST read**`protocols/incident-response-protocol.md`

按 `incident-response-protocol.md` 执行声明 / 分级 / 止血 / Hard-gate 触发 / 通信批准 / 监控止血效果。

### 阶段 7 — 事故复盘与消减（事故主线）**MUST read** `protocols/incident-response-protocol.md`

按 `incident-response-protocol.md §postmortem 模板` 草拟时间线 / 影响面 / 根因 / 修复项 / 防复发项；mitigation task handoff 给 `/specs-write` 或 `/bug-audit`；P0/P1 强制；P2/P3 用户裁决。

---

## 3. 输出格式

```markdown
## 可观测性与事故响应报告 (Observability / Incident Report)

## 工作流状态 (Workflow State)

- State: /observability-incident:`<state>`
- 当前主线 (Lane): <Setup / Incident>

## 监控建设主线 (Setup - 如适用)

- 信号源审计清单 (Signals Inventory): <PASS / FAIL + 缺项 13 信号面 列表>
- 服务等级目标 (SLO): <已草拟 / 缺核心路径 + 路径列表>
- 告警规则 (Alert Rules): <已草拟 / 缺规则 + 阈值 / 窗口 / 严重性 / 通知对象>
- 故障排查手册 (Runbooks): <每告警配 runbook PASS / FAIL + 缺项>
- 监控就绪度定义 (Observability DoD): <核心路径有日志 + 错误率指标 / 关键依赖有 timeout-retry-fallback / P0P1 响应流程 / 每告警有 runbook → 4 项 PASS / FAIL>

## 事故响应主线 (Incident - 如适用)

- 事故 ID (Incident ID): 
- 严重级别 (Severity): <P0 / P1 / P2 / P3>
- 关键时刻 (Detected at / Declared at / Mitigated at / Resolved at):
- 影响评估 (Impact): <影响用户数 + 业务指标偏离 + 触发告警列表>
- 已采取的止血措施 (Mitigation Steps Taken): <列出，含 Hard-gate 触发记录>
- 用户通报通知 (User Notification): <已发送 / 待批准 / N/A>
- 服务状态页更新 (Status Page): <已更新 / 待批准 / N/A>

## 门禁/节点状态 (Gate / DAG Status)

- HG-INCIDENT-{slug}-{incident-id}: <S-HG-* 状态>
- HG-IRREV-* 命中: <列出激活子项>
- HG-OPS-{repo}-observability: <S-HG-* 状态 或 N/A>
- DAG-N-INCIDENT-{slug}-{incident-id}: <node 状态>
- DAG-N-AUDIT-{repo}-observability: <node 状态>

## 故障复盘 (Postmortem - 如 P0/P1 或用户要求)

- 复盘时间线 (Timeline): <分钟级时间线>
- 根本原因 (Root Cause): <技术 / 流程 / 人为>
- 诱发/促成因素 (Contributing Factors):
- 改动/行动项 (Action Items): <mitigation tasks + owner + 截止>
- 防复发项 (Prevent Recurrence): <长期改进项>

## 授权边界 (Authorization Boundary)

- 路由动作 (Route Action): <CONTINUE_IN_WORKFLOW | WAIT_FOR_USER | CONFIRMED_ACTION | REPORT_AND_STOP>
- 授权来源 (Confirmation source): <用户原话 或 N/A>
- 授权范围 (Authorized scope): <本次事故范围内 通信 / 降级 / rollback>
- 未授权范围 (Not authorized): <下次事故 / 其他范围 / 后续 release / 下游 workflow>

## 推荐下一步路由 (Recommended Next Route)

- <continue Phase | /specs-write mitigation | /specs-execute hotfix | /bug-audit | /release-deploy rollback | /project-steward>

## 恢复/返航契约 (Return Contract)

- 目标路由 (Target route):
- 准入输入 (Entry input):
- 未决止血措施/复盘缺口 (Outstanding mitigation / postmortem gaps):

```

---

## 4. 禁用行为

- 不在 `/observability-incident:OBSERVABILITY_GATE_BLOCKED` 时输出 `/observability-incident:OBSERVABILITY_READY` 或放行 `/release-deploy:R-RDY-7`。
- 不在 `/observability-incident:INCIDENT_USER_NOTIFICATION_PENDING` / `/observability-incident:PROD_DEGRADATION_PENDING_APPROVAL` 未批准时执行真实通知 / 降级 / rollback；每次都需用户原话引用入 packet。
- 不替代 `/release-deploy` 执行 rollback；本 workflow 只发起 rollback 申请；真正 rollback 命令由 `/release-deploy` 执行并复用其 `P-RBK-*` 协议。
- 不替代 `/bug-audit` / `diagnose` 做根因诊断；本 workflow 只记录"现象 + 影响面"；根因分流。
- 不把 P2/P3 默认免 postmortem；用户裁决；P0/P1 强制不可省。
- 不在事故未止血时跳到 postmortem；先止血后复盘。
- 不把 setup gate packet 重复用于不同 release；每个 release 重新核验 R-RDY-7。
- 不在 hotfix 部署时绕过 `/release-deploy` Hard-gate；紧急路径仍需用户原话批准 + packet 装配。
- 不修代码 / spec / standards；只读消费它们；如发现需求 / 实现 / 架构缺陷 → 按 `R-RETURN-*` 回切。

## 5. 快速自检清单

报告前自检：

- [ ] 是否已根据触发源正确分流至 Setup 建设主线或 Incident 响应主线？
- [ ] Setup 主线中，是否已按 13 信号面完成采集并为所有 Alert 配置了 Runbook？
- [ ] Incident 主线中，是否在止血前避免了启动 Postmortem 复盘程序？
- [ ] 针对事故分级、生产降级、用户通知或回滚，是否均已取得用户明确授权？
- [ ] P0/P1 事故的 Postmortem 是否已产出了完整的时间线、根因分析及 Mitigation Items？

## 支撑资源

- [decision-matrix.md](./references/decision-matrix.md)
- [incident-response-protocol.md](./protocols/incident-response-protocol.md)
- [signals-runbook-protocol.md](./protocols/signals-runbook-protocol.md)
