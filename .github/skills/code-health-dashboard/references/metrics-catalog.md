# 健康指标目录 (Metrics Catalog)

## 1. 健康度信号 (Health Signals)

| 信号 ID (Signal ID) | 信号类型 (Signal) | 事实源 | 运行成功 (PASS) | 运行失败 (FAIL) | 未知状态 (UNKNOWN) |
| ----------- | -------- | -------- | ------ | ------ | --------- |
| CHD-S1 | lint | lint command / CI artifact | exit 0 | non-zero / violations | command missing / not run |
| CHD-S2 | typecheck | typecheck command | exit 0 | type errors | command missing / not run |
| CHD-S3 | unit tests | test command | all pass | failing tests | command missing / not run |
| CHD-S4 | integration / e2e | integration / e2e command | all pass | failing tests | not configured / not run |
| CHD-S5 | coverage | coverage report | above project threshold | below threshold / drop | no threshold / no history |
| CHD-S6 | dependency risk | audit / lockfile / security packet | no blocking risk | critical vuln / license risk | audit missing |
| CHD-S7 | flaky | rerun history / CI history | no recurring flaky | recurring nondeterministic failure | no history |
| CHD-S8 | complexity / churn | static metrics / diff | within budget | hotspot increasing | no metric |
| CHD-S9 | performance health | perf packet / benchmark | within budget | regression | no baseline |
| CHD-S10 | release gates | release readiness packets | required gates PASS | required gate FAIL | gate not run |

## 2. 路由规则 (Routing Rules)

| 规则 ID (Rule ID) | 条件 | 目标路由 (Route) |
| --------- | ------ | ------- |
| CHD-R1 | lint / typecheck fail | `/specs-execute` |
| CHD-R2 | test fail with unknown impact | `/bug-audit` or `diagnose` |
| CHD-R3 | command surface missing | `/repo-safety-setup` |
| CHD-R4 | CI gate missing | `/ci-quality-gates` |
| CHD-R5 | performance regression | `/performance-reliability-audit` |
| CHD-R6 | dependency / license / secret risk | `/security-privacy-audit` or `/authorship-copyright-readiness` |
| CHD-R7 | release packet fail | `/release-deploy` or corresponding gate workflow |

## 3. 状态语义 (Status Semantics)

| 状态 (Status) | 含义 (Meaning) | 是否允许存在于 READY 看板 (Allowed in READY dashboard) |
| -------- | --------- | ---------------------------- |
| PASS | 证据存在且通过 (Evidence exists and passes) | 是 (Yes) |
| FAIL | 证据存在且失败 (Evidence exists and fails) | 是，但若为强控阻断信号，看板最终结论为 BLOCKED (Yes, but dashboard verdict BLOCKED if blocking signal) |
| UNKNOWN | 证据缺失、命令缺失或历史缺失 (Evidence missing, command absent, or history absent) | 仅在有显式路由或理由时允许 (Yes only with explicit route / reason) |
| N/A | 有证据表明信号不适用 (Signal not applicable with evidence) | 是 (Yes) |

## 4. 默认强控阻断信号 (Blocking Defaults)

| 信号类型 (Signal) | 默认是否强控阻断 (Blocking by default) |
| -------- | --------------------- |
| lint | Yes |
| typecheck | Yes |
| unit tests | Yes |
| integration / e2e | Yes if configured / release critical |
| coverage | Project-defined |
| dependency risk | Yes if critical |
| flaky | Yes if affects release path |
| complexity / churn | No, unless coupled with failures |
| performance health | Yes if NFR-PERF Active |
| release gates | Yes |
