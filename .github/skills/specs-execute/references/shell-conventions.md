# Specs Execute  Shell Conventions

> **When to read**: The main workflow instructs Cascade to load this file before drafting any shell command inside Phase 3 Plan, Phase 7 Verify, Phase 8 Update, or any rollback step.

---

## 1. Shell 运行纪律

### 1.1 PowerShell（Windows · 默认目标平台）

- **脚本内容必须全英文**：中文字面量在某些 PowerShell 版本会触发编码报错；中文输出走文件或 `Write-Host -ForegroundColor` 控制台，不进入脚本字面量。
- **写文件 cmdlet 必须显式 `-Encoding UTF8`**：`Set-Content` / `Out-File` / `Add-Content` 默认编码可能为 GBK / UTF-16 → 大面积乱码与 grep 失效；所有 spec 内 Verification / Revert 命令产生的文件必须 UTF-8 BOM-less。
- **不使用 `&&` 作为命令分隔符**：PowerShell 5/7 早期版本不识别（7.x 兼容但项目模板不假定）；改用 `;`（无短路）或 `if ($LASTEXITCODE -eq 0) { ... }`（带短路 + 显式判定）。
- **路径含空格强制单/双引号包裹**：避免 `C:\Program Files\...` 类路径解析错位。
- **`cd` 不得作为 run_command 的一部分**：应通过 cwd 参数声明工作目录；多步操作内 `cd` 仅作为脚本内部跳转，不污染外层 run_command 调用。
- **`$LASTEXITCODE` 判定优于隐式短路**：跨 cmdlet 与外部进程混调时显式判定，避免 `if ($?) { ... }` 在 native exe 场景下误判。

### 1.2 bash / zsh（仅当写端 `project-adapter.md §1` 的 `shell` 槽位改值时）

- Verification Commands / Revert Command 给等价命令；不得假设 PowerShell-only cmdlet（`Get-Content` / `Set-Content` / `Get-ChildItem`）跨 shell 可用。
- 命令行 OS / shell 头按写端 `project-adapter.md §3` 标注（`[bash]` / `[macOS zsh]`）；混用时须分行给两套命令。
- 文件写入注意 `printf` vs `echo` 在 bash / zsh 行尾换行差异；脚本内固定使用 `printf '%s\n'` 模式生成稳定输出。

### 1.3 跨 shell 通用纪律

- **命令必须可复现**：Verification Commands 不得依赖未声明的环境变量 / shell 别名 / 用户 PATH 顺序；`tasks.md` 内必须列出最小可跑前置（venv 激活 / 依赖版本 / cwd）。
- **错误退出码必须可机读**：任何 wrapper 脚本必须将子进程 exit code 透传到顶层（`exit $LASTEXITCODE` / `set -e` 之类），避免 wrapper 吞错。
- **输出落点遵守 spec 边界**：脚本产物路径优先按 tasks.md `Artifacts:` 声明落到 `<feature-slug>/artifacts/`；落入项目根 `reports/` / `tmp/` / `output/` 通用目录视为越界（§11 第 9 条 + 写端 §1.6 artifacts 子目录硬约束）。
