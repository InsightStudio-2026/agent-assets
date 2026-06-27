---
name: repo-safety-setup
description: 仓库安全基线初始化；配置危险 git 操作拦截、pre-commit 校验、格式化、typecheck 与测试入口，并验证保护链路有效。Use when setting up repo safety baseline, configuring git hooks/pre-commit/typecheck, or says 安全基线/仓库保护/代码门禁/Git hooks。
---


# /repo-safety-setup · 仓库安全初始化

**定位**：为仓库建立本地开发安全基线，降低误推送、破坏性 git 操作、未格式化代码、未跑类型检查或测试的风险。

**边界**：只配置本地/仓库级开发保护；不改业务代码，不替代 CI，不保证拦截所有 destructive git 命令，不强制提交，除非用户明确要求。任何文件写入、依赖安装、package script 修改或 hook 合并前，必须先展示待写文件 / 命令 / 回滚方式并获得用户确认。

**斜杠命令**：`/repo-safety-setup`

---

## 懒加载契约

- **MUST read**: `./decision-matrix.md`
- 开始判定或执行 Phase 流程前，必须完整懒加载上述细节。

---

## 1. 阶段 1 — 安全条件评估

确认目标范围：

- **Git guardrails**：是否配置 Git hooks 拦截高风险 push / destructive 操作提示。
- **Pre-commit**：是否启用 formatting、typecheck、tests。
- **Scope**：project only 或 global。
- **Package manager**：npm / pnpm / yarn / bun。

输出：

```markdown
## Safety Intake

- Guardrails scope:
- Pre-commit needed:
- Package manager:
- Existing config:
- User decisions needed:

```

---

## 2. 阶段 2 — 探测既有安全配置

读取：

- `.git/hooks/`
- `.husky/`
- `package.json`
- `package-lock.json` / `pnpm-lock.yaml` / `yarn.lock` / `bun.lockb`
- `.lintstagedrc` / `lint-staged.config.*`
- `.prettierrc` / `prettier.config.*`
- CI config, if present

不得覆盖既有 hooks；只能合并或追加。

---

## 3. 阶段 3 — 配置 Git 安全卡口

### 3.1 询问配置范围

询问安装范围：

- Project：仓库级 `.git/hooks/` 或 `.husky/`
- Global：只在用户明确要求时，记录为手动步骤；本 workflow 默认不做 global 安装

### 3.2 配置 Pre-push 卡口

推荐优先配置 `pre-push`，阻止误推送到受保护分支。为了解决 Windows 11 与 Unix/macOS 本地 Shell（CMD.exe 与 Git Bash）路径及脚本关联的天然错配，必须将 pre-push 写入为 **双栖 Polyglot 兼容模板**（在 Windows 下通过 MINGW bash 执行，在 Unix 下由原生 bash 执行，两端同名且免修改）：

```bash
: << 'CMDBLOCK'
@echo off
REM Windows CMD 自动定位并调起 Git Bash 运行本脚本
if exist "C:\Program Files\Git\bin\bash.exe" (
    "C:\Program Files\Git\bin\bash.exe" "%~dp0%~nx0" %*
    exit /b %ERRORLEVEL%
)
where bash >nul 2>nul
if %ERRORLEVEL% equ 0 (
    bash "%~dp0%~nx0" %*
    exit /b %ERRORLEVEL%
)
REM 未找到 bash 环境时静默放行，不阻塞 Windows 本地操作
exit /b 0
CMDBLOCK

#!/bin/bash
## Unix/Linux/macOS 或者是 Git Bash 环境下的执行体
protected='^(main|master|production|release)$'
current_branch="$(git rev-parse --abbrev-ref HEAD)"

if echo "$current_branch" | grep -Eq "$protected"; then
  echo "BLOCKED: direct push from protected branch '$current_branch'." >&2
  exit 2
fi

exit 0
```

### 3.3 Hook 安装

Project 安装策略：

```text

IF 项目已有 Husky → 写入 `.husky/pre-push` 或合并到既有 pre-push
ELIF 用户接受本地 Git hook → 写入 `.git/hooks/pre-push`
ELSE → 只输出建议，不写 hook

```

合并规则：

- 保留既有 hook 内容。
- 已有同等保护时不重复添加。
- `.git/hooks/` 不进入版本控制；若需要团队共享，优先使用 Husky。

### 3.4 个性化定制

询问用户是否添加或移除危险模式。默认不扩大拦截范围。

---

## 4. 阶段 4 — 配置 Pre-Commit 本地门禁

### 4.1 包管理器校验

检测顺序：

- `pnpm-lock.yaml` → pnpm
- `yarn.lock` → yarn
- `bun.lockb` → bun
- `package-lock.json` → npm
- 不明确 → 询问用户；不要猜测安装命令。

### 4.2 依赖安全校验

安装依赖前必须列出命令并等待用户批准。

按 package manager 安装 dev dependencies：

```text

husky lint-staged prettier

```

### 4.3 部署 Husky

初始化 Husky，并确保 package script 中存在 prepare hook。

Pre-commit 内容根据 package manager 调整：

```bash
npx lint-staged
npm run typecheck
npm run test
```

若 `package.json` 没有 `typecheck` 或 `test`，省略对应行，并在报告中说明。

### 4.4 配置 lint-staged

若无既有配置，创建：

```json
{
  "*": "prettier --ignore-unknown --write"
}
```

若已有配置，只报告，不覆盖，除非用户要求合并。

### 4.5 配置 Prettier

若无既有 Prettier config，创建保守默认：

```json
{
  "useTabs": false,
  "tabWidth": 2,
  "printWidth": 80,
  "singleQuote": false,
  "trailingComma": "es5",
  "semi": true,
  "arrowParens": "always"
}
```

---

## 5. 阶段 5 — 运行验证

只有 State = `/repo-safety-setup:CONFIGURED_PENDING_VERIFY` 或 `/repo-safety-setup:VERIFY_FAILED_CONFIG_REGRESSION` 重验时才进入本 Phase。

必须验证：

- Guardrails hook 可执行。
- Guardrails smoke test 返回阻止信号。
- `.husky/pre-commit` 存在。
- `lint-staged` 可运行。
- typecheck/test 若接入则可被调用。

Guardrails smoke test：

```bash
<path-to-pre-push>
```

期望：exit code `2`，stderr 包含 `/repo-safety-setup:BLOCKED`。

PowerShell 调用时不使用 `cd`；由调用方指定 cwd，直接执行 hook 路径并读取 `$LASTEXITCODE`。

任一验证失败时，不得进入 `/repo-safety-setup:DONE`。先判断失败属于本 workflow 写入回归、既有项目失败还是环境阻塞：本 workflow 写入回归进入 `/repo-safety-setup:VERIFY_FAILED_CONFIG_REGRESSION`，修配置并重验；不可恢复则回滚写入；既有项目失败进入 `/repo-safety-setup:VERIFY_FAILED_EXISTING_PROJECT` 并报告；工具缺失、需安装、联网或权限不足进入 `/repo-safety-setup:VERIFY_BLOCKED_ENVIRONMENT`，停下等待用户裁决。

---

## 6. 阶段 6 — 完工汇报

输出：

```markdown
## 本地安全基线配置报告 (Repo Safety Setup Report)

## 工作流状态 (Workflow State)

- State: /repo-safety-setup:<STATE>; common examples: /repo-safety-setup:DONE | /repo-safety-setup:PARTIAL_CONFIGURED | /repo-safety-setup:VERIFY_FAILED_EXISTING_PROJECT | /repo-safety-setup:INSTALL_BLOCKED | /repo-safety-setup:VERIFY_BLOCKED_ENVIRONMENT | /repo-safety-setup:ROLLED_BACK

## 配置结论 (Outcome)

- <Configured and verified | Partial configured | Rolled back | Existing project failure | Environment blocked>

## 权威信息与事实源 (Authority / Fact Source)

- 配置项事实依据 (Config authority): <hooks / package scripts / lint-staged / formatter config>
- 授权批准来源 (Confirmation source): <user approval quote or N/A>
- 验证证据 (Verification evidence): <commands and output>
- 回滚证据 (Rollback evidence): <N/A or rollback output>

## 授权边界 (Authorization Boundary)

- 路由动作 (Route Action): <WAIT_FOR_USER | CONFIRMED_ACTION | REPORT_AND_STOP | CONTINUE_IN_WORKFLOW>
- 授权范围 (Authorized scope): <exact files / install commands / package scripts / hook merge / rollback plan>
- 未授权范围 (Not authorized): <commit / push / global install / business code / downstream workflow execution>

## 已配置安全项 (Configured)

- 分支推送强护栏 (Git guardrails): <yes | no>
- 提交前校验 (Pre-commit): <yes | no>
- 代码格式化 (Formatting): <yes | no>
- 类型校验钩子 (Typecheck hook): <yes | no>
- 测试校验钩子 (Test hook): <yes | no>

## 变动文件清单 (Files Changed)

- <paths>

## 功能验证 (Verification)

- <checks and result>

## 后续手动行动 (Follow-up)

- <manual actions if any>

## 推荐下一步路由 (Recommended Next Route)

- /project-steward

```

---

## 7. 禁用行为

- 不覆盖已有 hook 配置。
- 不默认 global 安装。
- 不默认拦截更多命令而不告知用户。
- 不强制提交配置变更。
- 不在无 package manager 证据时安装依赖。
- 不把本地安全基线当成 CI 替代品。
- 不跳过 smoke test。
- 不引入当前仓库主目标之外 of the 工具专属配置路径。

## 8. 快速自检清单

报告前自检：

- [ ] 是否正确获取了开发安全基线安装范围及包管理器？
- [ ] 检查本地是否已有 Husky 或 Git Hooks 配置（防止静默覆盖）？
- [ ] 写入的 pre-push 是否为双栖 Polyglot 兼容模板？
- [ ] 依赖安装与 package script 修改前是否取得了用户明确授权？
- [ ] 是否执行了 smoke test，并验证了 exit code 为 2 的阻断信号？

## 支撑资源

- [decision-matrix.md](./references/decision-matrix.md)
