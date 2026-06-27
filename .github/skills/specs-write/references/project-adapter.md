# Project Adapter（项目级注入槽）

> **When to read**: 在 `/specs-write` 需要项目级槽位、Shell / OS 约定、INV-* 示例库或工具命令默认值时读取本文。

## 1. 项目级槽位

| 槽位 | 用途 | 由项目层填 |
| ------ | ------ | ------------ |
| `shell` | Shell / OS（如 PowerShell 7 / bash 5） | `pwsh` |
| `evidence_dir` | 防 4 工具原文落地目录 | `audit-evidence/` |
| `traceability_regen_script` | 防 1 表格重生命令 | `python tools/traceability_regen.py --feature <slug>` |
| `traceability_check_script` | 防 1 双源对照（不写入 / 仅 exit code 0/4/其他） | `python tools/traceability_check.py --feature <slug>` |
| `bdd_owner_diff_script` | 防 2 BDD 唯一所有权校验 | `python tools/bdd_owner_diff.py --feature <slug>` |
| `revert_dependency_graph_script` | 防 3 共享文件冲突可视化 | `python tools/revert_dependency_graph.py --feature <slug>` |
| `audit_evidence_age_script` | 防 4 EXIST `Verified By` 7 天有效期复检 | `python tools/audit_evidence_age.py --feature <slug>` |
| `inv_violation_check_script` | 防 5 INV-*违反静态扫描 | `python tools/inv_violation_check.py --feature <slug>` |
| `reflection_archive_script` | `appendix.md §A.7` Reflections GC + 归档 | `python tools/reflections_archive.py --feature <slug>` |
| `ui_visual_snapshot_tool` | DSN-UI-* `Verified By` UI 快照工具 | Playwright MCP / Chromatic / etc. |
| `cross_end_type_contract_tool` | 跨端通信类型契约 SSOT 与 autogen | TypeScript codegen / openapi-typescript / etc. |
| `cross_end_drift_check_tool` | CI 检测两端类型不同步 | `pnpm contract:check` / `python tools/api_contract_diff.py` |
| `secret_scan_tool` | INV-SEC-* 凭据/敏感字段扫描（`task-rules.md §1` Secret-Scan 命令条件化必填） | `gitleaks detect --source<repo>--no-banner` / `trufflehog filesystem <path>` / `python tools/secret_scan.py --paths <files>` |
| `attention_budget_p1_ceiling` | 防 5 注意力稀释 P1 Reference 加载上限（token 数 · `/specs-execute` §1.2 #11 attention_budget_check 消费） | `200000`（默认 200k；项目层按实际 LLM context window 调整，如 Claude 200k / GPT-4o 128k / Gemini 2M 可改） |
| `attention_budget_p0_only_ceiling` | 防 5 注意力稀释 P0-only 加载上限（超此阈值进入"仅 payload + first_task 节"超载档位） | `300000`（默认 300k；项目层同步调整，须严格 > `attention_budget_p1_ceiling`） |

## 2. INV-* 项目示例库（项目层注入）

> Global 仅给基础形态；项目层在本文列出本项目实际的 INV-* 示例与红线词典。

示例（项目层填具体值）：

```markdown

- INV-BAN-001: 不引入新一类持久化存储（保持 PostgreSQL 单数据库）
- INV-BAN-002: 不引入消息队列中间件（用 outbox + cron 替代）
- INV-LIM-001: 单 Task 触动文件 ≤ 8 个
- INV-LIM-002: LLM 单次请求成本 ≤ $0.05
- INV-LIM-003: API SLA p95 ≤ 300ms
- INV-SEC-001: 凭据不得 inline 进源码或日志（改 KMS / Vault / keyring 注入）
- INV-SEC-002: 跨网域调用必须 mTLS
- INV-SEC-003: PII 字段不得入应用日志（mask + redaction）

```

## 3. 项目级 Shell / OS 注入

- **默认假设**：Windows + PowerShell（本 workflow 模板与示例采用此默认值）。
- **项目可改**：bash / zsh / WSL / macOS Terminal；项目层在 §1 `shell` 槽位声明后，spec 内 Verification Commands / Revert Command 必须标注 OS / shell 头（如 `[bash]` / `[macOS zsh]`），混用时须分行给两套命令。
- **跨 shell 命令书写**：项目层若把 `shell` 槽位改为 bash / zsh，Verification Commands 给等价命令；不得假设 PowerShell-only cmdlet（如 `Get-Content` / `Set-Content`）跨 shell 可用。
- **具体命令书写纪律**（编码 flag / 命令分隔符 / 路径引用 / `cd` 与 cwd / 文件写入 -Encoding UTF8 / 字面量限定等）详 `/specs-execute §13`。
