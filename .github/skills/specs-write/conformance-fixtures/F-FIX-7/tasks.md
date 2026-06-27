# Tasks · Google OAuth 登录（F-FIX-7 伪化版本，故意失败）

> **F-FIX-7 conformance fixture · 故意失败的 tasks.md**。基于 `EX-G-1` tasks 段制造三种 Verification 缺失模式。
> 期望 `/asset-quality-gates` `R-CHK-EX-1.7 verification missing` 命中（severity = Critical）。

---

## 1. Tasks 表

| Task ID | Description | Status | Touches | Verification | Artifacts |
| --------- | ------------ | -------- | --------- | -------------- | ----------- |
| `TASK-1` | migration: 新增 `users.google_sub` 列 | Done | `migrations/2026-05-30-add-google-sub.sql` | `pnpm migrate up && psql -c "\d users"` | `artifacts/migrate-up.log` |
| `TASK-2` | OAuth state 生成 + redirect | Done | `src/auth/google/start.ts` | `pnpm test src/auth/__tests__/oauth-start.test.ts` | `artifacts/oauth-start-test.log` |
| **`TASK-3`** | OAuth callback handler | **Done** | `src/auth/google/callback.ts` | **(空白)** | `artifacts/oauth-callback-test.log` |
| **`TASK-4`** | Account resolver（合并逻辑） | **Done** | `src/auth/google/account-resolver.ts` | `pnpm test src/auth/__tests__/account-resolver.test.ts` | **`artifacts/account-resolver-NONEXISTENT.log`** |
| **`TASK-5`** | `<GoogleLoginButton>` UI | **Done** | `src/features/auth/GoogleLoginButton.tsx` | `pnpm test:e2e tests/e2e/google-oauth-flow.spec.ts` | **(空白)** |

>**故意漂移点 1（Mode A：缺 Verification）**：TASK-3 标 `Status: Done` 但 `Verification:` 列空白；无法验证 callback handler 是否真实测试通过。
>
> **故意漂移点 2（Mode C：Artifacts 路径不存在）**：TASK-4 `Artifacts:` 列引用 `artifacts/account-resolver-NONEXISTENT.log`；该文件在 fixture 目录不存在 → checker 应能 stat 检查识别。
>
> **故意漂移点 3（Mode B：缺 Artifacts）**：TASK-5 标 `Status: Done` 但 `Artifacts:` 列空白；无 e2e screenshot / 测试日志 → 无法验证 UI 真实交付。

---

## 2. DAG

`TASK-1` → `TASK-2` → `TASK-3` → `TASK-4` → `TASK-5`

---

> **故意漂移点汇总**（与 `EX-G-1/requirements.md` §4 Tasks 对照）：
>
> - TASK-3 缺 Verification 字段（Mode A）
> - TASK-4 Artifacts 引用不存在文件（Mode C）
> - TASK-5 缺 Artifacts 字段（Mode B）
> - 三个 Done task 中 Verification / Artifacts 完整性断裂；checker 应在三个子模式中任一命中即报错
