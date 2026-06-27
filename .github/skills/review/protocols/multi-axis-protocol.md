# 多轴审查协议 (Multi-Axis Review Protocol)

## 1. 目的

本协议扩展 `review` skill 的审查轴线，但不合并原有 Standards / Spec / Verification 三轴。新增轴线只补足高风险变更、门禁绕过、可维护性和 release readiness 信号。

## 2. 审查轴线 (Review Axes)

| 轴线 (Axis) | 关注点 | 事实源 | 典型阻碍 (Blocker) |
| ------ | -------- | -------- | -------------- |
| Standards | 文档化规范是否被违反 | AGENTS / standards / ADR / configs | 违反硬性仓库约定 |
| Spec | 是否忠实实现上游需求 | issue / PRD / spec / tasks | 缺需求、scope creep、错实现 |
| Verification | 可运行验证信号强弱 | commands / CI / artifacts | required check 未跑或失败 |
| Risk Gates | 是否绕过专项 gate | release / security / data / perf / UX / desktop packets | 高风险变更无 gate packet |
| Architecture | 模块边界、耦合、浅模块、跨层依赖 | ADR / design / diff | 破坏已定义边界 |
| Operability | 日志、错误、rollback、runbook、debuggability | observability / release docs | 生产故障不可诊断或不可回滚 |
| Authorship / Provenance | license、第三方来源、AI 残留、权利主体 | LICENSE / NOTICE / provenance | 来源不明或披露被删除 |

## 3. 轴线触发规则 (Axis Trigger Rules)

| 规则 ID (Rule ID) | 条件 | 触发轴线 (Required Axis) | 异常路由 (Route If Red) |
| --------- | ------ | --------------- | -------------- |
| R-REV-AXIS-1 | diff 触及 auth / secrets / PII / permissions | Risk Gates + Authorship/Provenance | `/security-privacy-audit` |
| R-REV-AXIS-2 | diff 触及 schema / migration / backfill / delete | Risk Gates + Operability | `/data-migration-safety` |
| R-REV-AXIS-3 | diff 触及 deploy / feature flag / release config | Risk Gates + Operability | `/release-deploy` |
| R-REV-AXIS-4 | diff 触及 perf-sensitive path | Risk Gates + Verification | `/performance-reliability-audit` |
| R-REV-AXIS-5 | diff 触及 UI / A11y / design system | Risk Gates + Standards | `/design-system-audit` |
| R-REV-AXIS-6 | diff 触及 installer / signing / update / local data | Risk Gates + Operability | `/desktop-release` |
| R-REV-AXIS-7 | diff 触及 license / NOTICE / README / public delivery | Authorship/Provenance | `/authorship-copyright-readiness` |
| R-REV-AXIS-8 | diff 触及 workflow / skill assets | Standards + Verification + Risk Gates | `/asset-quality-gates` |

## 4. 报告扩展 (Report Extension)

```markdown
## 风险门禁 (Risk Gates)

- 发现问题数 (Findings): <count>
- 最高严重级别 (Highest severity): <Blocker | Must fix | Should fix | Question | Nit | None>
- 对应路由 (Required route): <workflow or N/A>

## 架构边界 (Architecture)

- 发现问题数 (Findings): <count>

## 可运维性 (Operability)

- 发现问题数 (Findings): <count>

## 署名与来源声明 (Authorship / Provenance)

- 发现问题数 (Findings): <count>

```

## 5. 严重程度映射 (Severity Mapping)

| 触发条件 (Condition) | 严重程度 (Severity) |
| ----------- | ---------- |
| 高风险变更缺失必要的门禁信息包 (gate packet) | 阻碍合并 (Blocker) |
| 生产回滚/恢复路径缺失 | 阻碍合并 (Blocker) |
| 发布资产的 License/来源声明不明 | 阻碍合并 (Blocker) |
| 未经批准违反架构边界设计 | 必须修复/阻碍合并 (Must fix / Blocker) |
| 关键路径缺失可观测性/监控指标 | 必须修复 (Must fix) |
| 轻微的可维护性问题 | 建议修复/轻微 (Should fix / Nit) |

## 6. 禁止项

| 禁止项 | 原因 |
| -------- | ------ |
| 不把新增轴线合并进 Standards 或 Spec | 防止一条轴掩盖另一条轴 |
| 不把 review 当专项 gate 的替代品 | review 只能发现缺口，不能替代 gate packet |
| 不用主观偏好冒充规范 | Standards 必须引用文档化来源 |
