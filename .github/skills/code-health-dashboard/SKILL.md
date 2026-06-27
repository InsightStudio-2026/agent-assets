---
name: code-health-dashboard
description: 代码健康仪表盘：汇总 lint、typecheck、test、coverage、依赖、复杂度、flaky、性能与 release gate 信号，形成可追踪趋势；不替代 CI，不伪造健康分。
context: fork
argument-hint: "要生成哪个项目的健康面板？"
disable-model-invocation: true
---


# /code-health-dashboard · 代码健康仪表盘

**定位**：把零散质量命令、测试结果、coverage、依赖风险、复杂度、flaky、性能与 release gate 信号汇总成可追踪健康面板；用于项目管家、release 前审查、技术债治理和成熟度证据沉淀。

**边界**：不替代 `/repo-safety-setup` 配置本地安全基线，不替代 `/ci-quality-gates` 持续门禁，不替代 `/performance-reliability-audit` 做基准，不替代 `/security-privacy-audit` 做漏洞审计。命令没跑不得打绿，环境失败不得伪装 PASS。

**斜杠命令**：`/code-health-dashboard`

---

## 懒加载契约

- **MUST read**: `./decision-matrix.md`
- 开始判定或执行 Phase 流程前，必须完整懒加载上述细节。

---

## 1. 伴随文档

| 文档 | 角色 | 何时读 |
| ------ | ------ | -------- |
| `references/metrics-catalog.md` | 质量指标字典及定义 | Phase 1 |
| `protocols/collection-protocol.md` | 质量数据收集与分析协议 | Phase 2 |
| `templates/dashboard-template.md` | 仪表盘输出模板 | Phase 3 |

---

## 2. 阶段骨架

| Phase | 目标 | MUST read | 输出 |
| ------- | ------ | ----------- | ------ |
| Phase 1 — Scope & Command Discovery | 找到 lint/typecheck/test/coverage/dependency/perf 等入口 | `references/metrics-catalog.md` | `/code-health-dashboard:HEALTH_SCOPE_DEFINED` 或 `/code-health-dashboard:COMMAND_SURFACE_MISSING` |
| Phase 2 — Evidence Collection | 采集命令输出、coverage、依赖、复杂度、flaky、gate packet | `protocols/collection-protocol.md` | `/code-health-dashboard:HEALTH_EVIDENCE_COLLECTED` |
| Phase 3 — Dashboard & Trend | 计算 PASS / FAIL / UNKNOWN，不伪造分数 | `templates/dashboard-template.md` | `/code-health-dashboard:DASHBOARD_READY` 或 blocking state |

## 3. 输出格式

```markdown
## 代码健康度看板 (Code Health Dashboard)

## 工作流状态 (Workflow State)

- State: /code-health-dashboard:<STATE>

## 健康度摘要 (Health Summary)
|  | 信号类型 (Signal) | 运行状态 (Status) | 事实依据 (Evidence) | 跟踪路由 (Route) |  |
|  | -------- | -------- | ---------- | ------- |  |
|  | 语法及风格检查 (lint) | PASS / FAIL / UNKNOWN | <path> | <route> |  |
|  | 类型检查 (typecheck) | PASS / FAIL / UNKNOWN | <path> | <route> |  |
|  | 单元与集成测试 (test) | PASS / FAIL / UNKNOWN | <path> | <route> |  |
|  | 测试覆盖率 (coverage) | PASS / FAIL / UNKNOWN | <path> | <route> |  |

## 看板结论 (Verdict)

- 看板就绪状态 (Dashboard): READY / BLOCKED
- 阻碍性缺陷 (Blocking gaps): <None or list>

```

## 4. 禁止动作

| 禁止项 | 原因 |
| -------- | ------ |
| 不伪造 health score | 没跑命令只能 UNKNOWN |
| 不把环境失败当 PASS | 必须分类 env_error / permission / missing_command |
| 不修改 CI / hooks | 配置归 `/repo-safety-setup` 或 `/ci-quality-gates` |
| 不用单次截图替代趋势 | trend 必须有历史来源 or 声明 baseline missing |
| 不把 dashboard 当 release approval | release 放行归 `/release-deploy` |

## 5. 内建 Lint 工具集

> 仓库级 Markdown lint 自动修复与分析工具，位于 `.github/tools/lint/`。
> 统一入口：`.github/tools/lint/lint.ps1`

| 命令 | 功能 | 对应脚本 |
| ------ | ------ | ---------- |
| `lint.ps1 check` | 运行 markdownlint-cli2 全量检查 | — |
| `lint.ps1 fix [目录]` | 运行全部三款自动修复 | fix_md033/040/060.py |
| `lint.ps1 fix-md033 [目录]` | 模板占位符 `<tag>` → `` `<tag>` `` | fix_md033.py |
| `lint.ps1 fix-md040 [目录]` | 围栏代码块添加 `text` 语言 | fix_md040.py |
| `lint.ps1 fix-md060 [目录]` | 表格管道两侧空格补齐 | fix_md060.py |
| `lint.ps1 compress <json>` | 压缩 VS Code Problems JSON | compress_problems.py |
| `lint.ps1 analyze <json>` | 分析问题分类 + 完整性 | analyze_problems.py |
| `lint.ps1 sample<json><code>` | 抽样查看指定规则违规 | analyze_problems.py |

### 在健康仪表盘中集成

Phase 2 (Evidence Collection) 中，lint 信号采集建议：

```powershell
## 1. 生成全量问题报告
npx markdownlint-cli2 "**/*.md" 2>&1 > lint_raw.txt

## 2. 转为 VS Code Problems JSON 格式后压缩
.\.github\tools\lint\lint.ps1 compress problems.json

## 3. 分析问题分布
.\.github\tools\lint\lint.ps1 analyze 问题_压缩.json
```

三款自动修复脚本均内置安全措施（跳过代码块、备份兼容），可安全用于批量修复。

## 6. 快速自检清单

报告前自检：

- [ ] 是否确认了当前项目的代码健康指标审计范围？
- [ ] 收集的测试、Lint 与 Coverage 证据是否均有真实的命令行输出支撑？
- [ ] 在计算健康分时，是否对环境失败或未跑命令做出了 UNKNOWN 标注（无伪造得分）？
- [ ] 趋势分析是否具有历史源基线（而非单次截图）？
- [ ] 是否明确说明了本 Dashboard 并不等同于 Release 放行？

## 支撑资源

- [collection-protocol.md](./protocols/collection-protocol.md)
- [dashboard-template.md](./templates/dashboard-template.md)
- [decision-matrix.md](./references/decision-matrix.md)
- [metrics-catalog.md](./references/metrics-catalog.md)
