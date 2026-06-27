# 监控信号与 Runbook 协议 (Signals & Runbook Protocol) · /observability-incident Setup 主线事实源

> **本文是 `/observability-incident` workflow Setup 主线的 13 信号面 + 事故材料面 + runbook 模板字典**。所有 R-OBS-* 规则在此定义；入口 workflow 按 ID 引用，不重复事实。
> 本文档自身遵循结构化规则表 + ID 体系格式规范（入口骨架 + 支撑文档分离 + 零 ASCII 流程图）。

---

## 0. 定位与索引

### 0.1 文档定位

- 13 信号面 + 事故材料面 + runbook 字段规范；与 `observability-incident` SKILL.md 最低信号面 + 事故材料面项零漂移。
- 不是工具教程；不绑定特定平台（Datadog / Grafana / NewRelic / Sentry / 自建）；只规定每类信号 / 字段 / runbook 必须满足的语义。
- 三大命名空间：R-OBS-SIG-*信号面；R-OBS-MAT-* 事故材料面；R-OBS-RBK-* runbook 字段。

### 0.2 ID 命名空间

- `R-OBS-SIG-1~13`：13 类最低信号面。
- `R-OBS-MAT-1~10`：事故材料面字段。
- `R-OBS-RBK-1~7`：runbook 必填字段。

---

## 1. 13 类最低信号面（R-OBS-SIG-*）

| 规则 ID (Rule ID) | 信号 | 必采条件 | 默认严重性（缺漏后果） | 工具示例（不绑定） |
| --------- | ------ | --------- | --------------------- | ------------------- |
| `R-OBS-SIG-1` | Latency | 所有公开 endpoint + 关键内部调用 p50 / p95 / p99 | High | APM / metrics |
| `R-OBS-SIG-2` | Traffic | 请求量 / RPS / 业务事件量按时间序列 | High | APM / metrics |
| `R-OBS-SIG-3` | Errors | 4xx / 5xx 比率 / 异常 stack 数 / unhandled rejection | Critical | error tracking |
| `R-OBS-SIG-4` | Saturation | CPU / mem / disk / FD / 连接池 / 队列长度 | High | infra metrics |
| `R-OBS-SIG-5` | 业务指标 | 注册成功率 / 支付成功率 / 任务完成率 / 同步成功率 / 崩溃率 | Critical | business metrics |
| `R-OBS-SIG-6` | Request ID | 每请求 trace id / span id 贯穿全链路 | High | tracing / log correlation |
| `R-OBS-SIG-7` | 脱敏 User ID | hashed user id / opaque id；不允许直传 email / phone | Critical | log + tracing |
| `R-OBS-SIG-8` | Tenant ID | 多租户系统必采；不允许跨租户日志混淆 | High | log + tracing |
| `R-OBS-SIG-9` | Error Code | 业务错误码字典化；不允许仅依赖 message 字符串 | High | log |
| `R-OBS-SIG-10` | 关键链路 Tracing | 注册 / 支付 / 同步 / 上传 / 长耗时调用 | High | tracing |
| `R-OBS-SIG-11` | Liveness Check | 进程存活检查 endpoint | High | health check |
| `R-OBS-SIG-12` | Readiness Check | 依赖就绪检查（DB / cache / 队列 / 配置） | High | health check |
| `R-OBS-SIG-13` | Dependency Check | 关键外部依赖（第三方 API / OAuth / 支付）健康 | High | health check / synthetic |

---

## 2. 事故材料面（R-OBS-MAT-*）

`alert-rules.md` 与 `incident-report.md` 必填字段。

| 规则 ID (Rule ID) | 字段 | 必填 | 范例 | 缺失后果 |
| --------- | ------ | ------ | ------ | --------- |
| `R-OBS-MAT-1` | 告警阈值 | 必填 | `p95 > 800ms 持续 5min` / `5xx > 1% 1min` / `支付成功率 < 95% 5min` | 阈值未定 → 告警噪音 / 漏报 |
| `R-OBS-MAT-2` | 告警窗口 | 必填 | `1min` / `5min` / `15min`；按业务定 | 窗口太短 → 抖动；太长 → 滞后 |
| `R-OBS-MAT-3` | 严重性分级 | 必填 | `P0` 全站 / `P1` 核心路径 / `P2` 局部 / `P3` 边缘 | 分级缺 → 响应优先级混乱 |
| `R-OBS-MAT-4` | 通知对象 | 必填 | on-call 角色 / 邮件组 / IM 群 / 电话；按严重性分级 | 通知缺 → 延迟响应 |
| `R-OBS-MAT-5` | 抑制策略 | 必填 | dedup / silence / dependency-based suppression | 抑制缺 → 告警风暴 |
| `R-OBS-MAT-6` | Runbook 链接 | 必填 | 每告警配 runbook 路径（详 §3） | 缺则 `RUNBOOK_REQUIRED` 阻塞 |
| `R-OBS-MAT-7` | 事故时间线 | 必填（事故） | 检测 / 声明 / 通知 / 止血开始 / 止血完成 / 解决 | 缺则 postmortem 不可信 |
| `R-OBS-MAT-8` | 影响面 | 必填（事故） | 影响用户数 / 区域 / 功能 / 业务损失估算 | 缺则严重性误判 |
| `R-OBS-MAT-9` | 根因 | 必填（postmortem） | 技术 / 流程 / 人为；分层多根因 | 单一根因 = 简化思维 |
| `R-OBS-MAT-10` | 修复项 + 防复发 | 必填（postmortem） | 立即 mitigation + 长期改进 + owner + 截止 | 无防复发 = postmortem 失败 |

---

## 3. Runbook 模板（R-OBS-RBK-*）

每个告警必须配 runbook；缺 runbook 的告警不得进入生产。

| 规则 ID (Rule ID) | 字段 | 必填 | 范例 |
| --------- | ------ | ------ | ------ |
| `R-OBS-RBK-1` | Trigger | 必填 | 哪个告警 / 阈值 / 窗口触发 |
| `R-OBS-RBK-2` | Quick Diagnosis | 必填 | 3-5 步初步诊断（看哪些 dashboard / log / trace） |
| `R-OBS-RBK-3` | Mitigation Steps | 必填 | 降级 / rollback / 重启 / 限流；按优先级排序；每步含明确命令或 dashboard 操作 |
| `R-OBS-RBK-4` | Hard-gate Steps | 必填（如适用） | 用户通知 / 状态页 / 生产降级 / rollback；每步必须用户原话批准（详入口 workflow §0.3） |
| `R-OBS-RBK-5` | Rollback Criteria | 必填 | 何时进入 ROLLBACK_REQUIRED；触发条件 + 二次确认人 |
| `R-OBS-RBK-6` | Communication Plan | 必填（高严重性） | 用户通知文案模板 / 状态页文案 / 内部 IM 模板；同时标注谁批准 |
| `R-OBS-RBK-7` | Post-incident | 必填 | postmortem 触发条件（P0/P1 强制）+ 时限（24h / 72h）+ owner |

### 3.1 Runbook 反模式

- ❌ "看一下日志"（无具体路径 / 命令）
- ❌ "联系负责人"（无 owner / 通知方式）
- ❌ Mitigation 仅一种方案（应有 fallback）
- ❌ Hard-gate 步骤合并到普通 mitigation（必须独立批准点）
- ❌ Rollback 没有触发条件（依赖个人判断）
- ❌ Communication Plan 留空（高严重性必填）

---

## 4. DoD（与入口 workflow §4 Forbidden Actions 对齐）

观测性建设 4 项 DoD（缺任一 → `OBSERVABILITY_GATE_BLOCKED`）：

| DoD 项 | 检查 |
| -------- | ------ |
| 核心用户路径有日志 + 错误率指标 | R-OBS-SIG-3 + R-OBS-SIG-5 + R-OBS-SIG-6 全过 |
| 关键外部依赖有 timeout / retry / fallback | R-OBS-SIG-13 + 实现侧（归 `/specs-execute`） |
| P0/P1 事故有响应流程 | R-OBS-MAT-3 + R-OBS-MAT-4 + R-OBS-MAT-7 全过 |
| 每个告警有 runbook | R-OBS-MAT-6 + R-OBS-RBK-1~7 全过 |

---

## 5. 边界与不替代

| 类别 | 是否在本文 | 委托对象 |
| ------ | ----------- | --------- |
| 监控 SDK 接入 / 工具配置 | 不规定 | `/specs-execute` 实现 |
| 性能基线 / 容量规划 | 不替代 | `/performance-reliability-audit` |
| 安全告警（异常登录 / 越权） | 部分（R-OBS-SIG-3 + 业务定义） | `/security-privacy-audit` 主导 |
| 法务 / 合规通报（数据泄露通报） | 不替代 | 法务 + `/security-privacy-audit` |

---

## 6. 修订规则

- 本文修订必须同 PR 修订 `observability-incident.md` Phase 2-5 骨架与 §0.3 Hard-gate 表（如涉通信 / 降级）。
- R-OBS-* ID 一旦分配不得复用；废弃改 deprecated。
- DoD 4 项（§4）任何放宽必须先在 `observability-incident` SKILL.md 同步并经用户裁决。
- 不引入平台特定查询语法；保持平台无关的语义层规范。
