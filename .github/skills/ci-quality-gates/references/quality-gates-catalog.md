# 质量门禁目录 (Quality Gates Catalog)

## 1. 门禁目录 (Gate Catalog)

| 门禁 ID (Gate ID) | 门禁类型 (Gate) | 输入数据 (Inputs) | 启用基准/合格 (PASS) | 阻断信号/不合格 (FAIL) | 推荐路由 (Route) |
| --------- | ------ | -------- | ------ | ------ | ------- |
| QG-1 | lint | lint job output | exit 0 | violations / non-zero | `/specs-execute` |
| QG-2 | typecheck | typecheck job output | exit 0 | type errors | `/specs-execute` |
| QG-3 | unit tests | test job output | all pass | failures | `/specs-execute` or `diagnose` |
| QG-4 | integration / e2e | integration job output | all pass | failures | `/bug-audit` if impact unknown |
| QG-5 | build | build artifact / log | artifact produced | build fail | `/specs-execute` |
| QG-6 | coverage | coverage report | threshold met | threshold miss | `/specs-write` if threshold absent |
| QG-7 | secret scan | scanner output | no secrets | secret found | `/security-privacy-audit` |
| QG-8 | dependency audit | audit output | no critical risk | critical vuln | `/security-privacy-audit` |
| QG-9 | license check | license report | compatible or approved | unknown / incompatible | `/authorship-copyright-readiness` |
| QG-10 | bundle size | bundle report | within budget | over budget | `/performance-reliability-audit` |
| QG-11 | migration check | migration dry-run / drift | pass | drift / migration fail | `/data-migration-safety` |
| QG-12 | asset conformance | workflow / skill asset checks | pass | structure/index/eval fail | `/asset-quality-gates` |

## 2. 必需与可选策略 (Required / Optional Policy)

| 适用条件 (Condition) | 必需门禁 (Required Gates) |
| ----------- | ---------------- |
| 任何代码 PR (Any code PR) | QG-1, QG-2 如果适用 (if applicable), QG-3, QG-5 如果可构建 (if buildable) |
| 用户界面 (User-facing UI) | QG-1~5 + 浏览器 / 端到端测试如果已配置 (browser/e2e if configured) |
| 依赖项变更 (Dependency change) | QG-7, QG-8, QG-9 |
| Schema / 数据迁移变更 (Schema / migration change) | QG-11 |
| 性能敏感路径 (Performance-sensitive path) | QG-10 |
| 工作流 / 技能资产变更 (Workflow / skill asset change) | QG-12 |

## 3. 门禁降低策略 (Lowering Gate Policy)

| 规则 ID (Rule ID) | 适用条件 (Condition) | 允许动作 (Allowed Action) |
| --------- | ----------- | ---------------- |
| QGP-R1 | 门禁由于真实缺陷失败 (Gate fails due real defect) | 修复缺陷；绝不降低门禁 (Fix defect; do not lower gate) |
| QGP-R2 | 门禁由于 Flaky 测试失败 (Gate fails due flaky test) | 标记为 flaky，配置负责人进行隔离，若属发布关键路径则保留必需 (Mark flaky, quarantine with owner, keep required if release critical) |
| QGP-R3 | 门禁由于环境异常失败 (Gate fails due environment) | 分类为 env_error，修复基础设施或重新运行；不视为合格 (Classify env_error, fix infra or rerun; no PASS) |
| QGP-R4 | 门禁不适用 (Gate not applicable) | 标记为 N/A 并提供证据 (Mark N/A with evidence) |
| QGP-R5 | 申请临时跳过 (Temporary skip requested) | 需要用户批准 + 设定过期时间 + 安排清理任务 (Requires user approval + expiry + cleanup task) |

## 4. 判定

| 条件 | 状态 (State) |
| ------ | ------- |
| required gates defined with evidence plan | `/ci-quality-gates:QUALITY_GATE_DRAFTED` |
| required gate missing | `/ci-quality-gates:CI_GATE_BLOCKED` |
| security-sensitive CI pattern found | `/ci-quality-gates:CI_SECURITY_RISK_FOUND` |
