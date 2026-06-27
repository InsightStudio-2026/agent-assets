# 健康数据采集协议 (Collection Protocol)

## 1. 命令发现 (Command Discovery)

| 规则 ID (Rule ID) | 事实源 (Source) | 查找内容 | 运行成功 (PASS) | 运行失败 (FAIL) |
| --------- | -------- | ---------- | ------ | ------ |
| COL-R1 | package.json | lint / typecheck / test / coverage scripts | scripts listed | missing scripts |
| COL-R2 | Makefile / taskfile | quality targets | targets listed | missing targets |
| COL-R3 | CI config | workflow jobs / required checks | jobs listed | no CI config |
| COL-R4 | docs | documented verification commands | commands listed | docs drift |
| COL-R5 | specs tasks | Verification Commands | task commands listed | task verification missing |

## 2. 证据分类 (Evidence Buckets)

| 数据分类 (Bucket) | 含义 (Meaning) | 看板状态 (Dashboard Status) |
| -------- | --------- | ------------------ |
| `actual_pass` | 命令运行且通过 (command ran and passed) | PASS |
| `actual_fail` | 命令运行且失败 (command ran and failed) | FAIL |
| `missing_command` | 命令未定义 (command not defined) | UNKNOWN + 路由至 `/repo-safety-setup` |
| `env_error` | 工具 / 依赖 / 环境阻断 (tool / dependency / environment blocked) | UNKNOWN + 环境阻断器 (environment blocker) |
| `permission` | 权限 / 凭证不可用 (permission / credential unavailable) | UNKNOWN + 用户动作 (user action) |
| `not_run` | 命令存在但未执行 (command exists but was not executed) | UNKNOWN + 需要运行 (run needed) |

## 3. 采集记录 (Collection Record)

| 字段 (Field) | 值 (Value) |
| ------- | ------- |
| Signal ID | CHD-S* |
| Command | <command or N/A> |
| Working Directory | `<path>` |
| Timestamp | ISO 8601 |
| Exit Code | <code or N/A> |
| Bucket | actual_pass / actual_fail / missing_command / env_error / permission / not_run |
| Output Path | `<artifact path>` |
| Interpretation | `<one sentence>` |

## 4. 证据保留 (Evidence Retention)

| 验证证据 (Evidence) | 目标路径 (Target Path) |
| ---------- | ------------- |
| command output | `<feature>/artifacts/code-health/<signal>.log` or local dashboard artifact |
| coverage report | `<feature>/artifacts/code-health/coverage.*` |
| dependency audit | `<feature>/artifacts/code-health/dependency-audit.*` |
| dashboard | `<feature>/artifacts/code-health/dashboard.md` or repo health artifact |

## 5. 采集规则 (Collection Rules)

| 规则 ID (Rule ID) | 检查项 | PASS 标准 | FAIL 信号 |
| --------- | -------- | ----------- | ----------- |
| COL-R6 | No invented output | 只引用真实命令输出或现有 artifact | 手写“通过”无证据 |
| COL-R7 | Environment honesty | env_error / permission 不转写成 FAIL/PASS | 环境问题伪装健康 |
| COL-R8 | Artifact path | release/spec 相关采集落 artifacts | 散落 reports/tmp/output |
| COL-R9 | Trend source | 趋势来自历史 dashboard / CI / release artifact | 凭记忆说变好变坏 |

## 6. 判定

| 条件 | 状态 (State) |
| ------ | ------- |
| 至少核心 signals 有 evidence | `/code-health-dashboard:HEALTH_EVIDENCE_COLLECTED` |
| 核心 command surface 缺失 | `/code-health-dashboard:COMMAND_SURFACE_MISSING` |
| 工具 / 权限阻断 | `/code-health-dashboard:HEALTH_BLOCKED_ENVIRONMENT` |
