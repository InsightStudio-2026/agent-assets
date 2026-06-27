# Tasks · Google OAuth 登录（F-FIX-6 伪化版本，故意失败）

> **F-FIX-6 conformance fixture · 故意失败的 tasks.md**。基于 `EX-G-1` tasks 增加越过 charter §3 Out-of-Charter "不接 GitHub OAuth" 的越界 task。
> 期望 `/asset-quality-gates` `R-CHK-EX-1.6 out-of-charter scope violation` 命中（severity = Critical）。

---

## 1. Tasks 表

| Task ID | Description | Status | Touches | Verification | Anti-Invariants |
| --------- | ------------ | -------- | --------- | -------------- | ----------------- |
| `TASK-1` | migration: 新增 `users.google_sub` 列 | Done | `migrations/2026-05-30-add-google-sub.sql` | `pnpm migrate up` | - |
| `TASK-2` | OAuth Google flow 实现 | Done | `src/auth/google/*.ts` | `pnpm test src/auth/__tests__/oauth-google.test.ts` | INV-SEC-2 |
| `TASK-3` | `<GoogleLoginButton>` UI | Done | `src/features/auth/GoogleLoginButton.tsx` | `pnpm test:e2e` | - |
| **`TASK-X`** | **GitHub OAuth provider 接入（添加 `<GitHubLoginButton>` + `/auth/github/*` endpoint + `users.github_sub` 列）** | **Done** | **`src/auth/github/*.ts` + `migrations/2026-06-15-add-github-sub.sql`** | **`pnpm test src/auth/__tests__/oauth-github.test.ts`** | - |

>**故意漂移点（Out-of-Charter 越界）**：`TASK-X` 引入 GitHub OAuth provider；charter §3 Out-of-Charter 第 1 项明确写 "不接 GitHub OAuth"。
>
> 这是 Strategy Gate 边界破坏（用户在 charter 阶段已批准"仅 Google"，本 spec 在派生层不应再添加被排除的功能）。

---

## 2. DAG

`TASK-1` → `TASK-2` → `TASK-3`；**`TASK-X` 独立并行**（违规但完成）

---

> **故意漂移点汇总**（与 `EX-G-1/requirements.md` §4 Tasks 对照）：
>
> - 新增 `TASK-X` GitHub OAuth provider，违反 `charter.md §3 Out-of-Charter` 第 1 项
> - `TASK-X` 的 Touches 包括 `src/auth/github/*.ts` + `users.github_sub` 列 = 引入 charter 显式禁止的功能
> - 解析器对照 `charter.md §3 Out-of-Charter` 与本表 `Description` / `Touches`，应识别越界并命中 `R-CHK-EX-1.6`
