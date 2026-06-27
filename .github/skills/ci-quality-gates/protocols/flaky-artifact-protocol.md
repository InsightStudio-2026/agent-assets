# Flaky 与产物协议 (Flaky / Artifact Protocol)

## 1. 产物要求 (Artifact Requirements)

| 规则 ID (Rule ID) | 交付产物 (Artifact) | 适用场景 (Required For) | 启用基准/合格 (PASS) | 阻断信号/不合格 (FAIL) |
| --------- | ---------- | -------------- | ------ | ------ |
| FAP-A1 | raw logs | all jobs | log retained with job id / timestamp | only summary exists |
| FAP-A2 | test reports | unit / integration / e2e | JUnit / JSON / equivalent uploaded | failures not inspectable |
| FAP-A3 | coverage reports | coverage gate | coverage artifact retained | threshold shown without report |
| FAP-A4 | build artifacts | build / release candidate | artifact hash + retention | artifact overwritten |
| FAP-A5 | screenshots / traces | browser / e2e | trace / screenshot retained | UI failure not reproducible |

## 2. 失败分类 (Failure Classification)

| 失败分类 (Bucket) | 含义 (Meaning) | 必需路由 (Required Route) |
| -------- | --------- | ---------------- |
| `actual_failure` | 确定性的产品 / 测试失败 (deterministic product / test failure) | `/specs-execute` 或 `diagnose` |
| `flaky_failure` | 伴随重新运行证据的非确定性失败 (nondeterministic failure with rerun evidence) | 隔离 / 负责人 / 过期时间 (quarantine / owner / expiry) |
| `env_error` | 运行器、缓存、网络或工具安装失败 (runner, cache, network, tool install failure) | CI 基础设施修复 / 重新运行 (CI infra fix / rerun) |
| `permission` | Token / 权限 / 受保护资源问题 (token / permission / protected resource issue) | 用户 / 安全路由 (user / security route) |
| `misconfiguration` | 任务命令错误 / 路径错误 / 缺失依赖 (job wrong command / wrong path / missing dependency) | `/ci-quality-gates` 修复计划 (fix plan) |

## 3. Flaky 规则 (Flaky Rules)

| 规则 ID (Rule ID) | 检查项 | PASS 标准 | FAIL 信号 |
| FAP-R1 | Rerun evidence | flaky 判定至少有 pass/fail 交替证据 | 单次失败就标 flaky |
| FAP-R2 | Owner | flaky quarantine 有 owner | 无 owner |
| FAP-R3 | Expiry | quarantine 有过期日期 / cleanup task | 永久 quarantine |
| FAP-R4 | Release critical | release critical path 不得因 flaky 降低 gate | 直接移出 required checks |
| FAP-R5 | Isolation | flaky tests 可单独标记，不污染全套测试 | 全局跳过测试套件 |

## 4. 隔离记录 (Quarantine Record)

| 字段 (Field) | 值 (Value) |
| ------- | ------- |
| Test / Job | `<name>` |
| Failure bucket | flaky_failure |
| Evidence | <links / artifacts> |
| Owner | `<owner>` |
| Expiry | `<date>` |
| Release critical | Yes / No |
| Required cleanup route | /specs-execute / diagnose / bug-audit |

## 5. 判定

| 条件 | 状态 (State) |
| ------ | ------- |
| artifacts retained and failures classified | `/ci-quality-gates:CI_GATE_READY` candidate |
| missing logs / reports for required gate | `/ci-quality-gates:CI_GATE_BLOCKED` |
| flaky lacks owner / expiry | `/ci-quality-gates:CI_GATE_BLOCKED` |
| permission / secrets risk | `/security-privacy-audit` |
