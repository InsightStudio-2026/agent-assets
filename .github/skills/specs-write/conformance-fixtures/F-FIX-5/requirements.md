# Requirements · Google OAuth 登录（F-FIX-5 伪化版本，故意失败）

> **F-FIX-5 conformance fixture · 故意失败的 requirements.md**。基于 `EX-G-1/requirements.md` 在 §3.1 DSN-1 中引入违反 charter §5 INV-BAN-3 的列；不可作为真实 spec 模板使用。
> 期望 `/asset-quality-gates` `R-CHK-EX-1.5 architectural invariants violation` 命中（severity = Critical）。

---

## 1. Requirements 表（精简）

### 1.1 REQ-1：OAuth 授权流程

- **Derived From**：`SRC-1` → `REQ-1`
- **AC-1.1**：**WHEN** 用户点击 "Continue with Google"，**THE SYSTEM SHALL**完成 OAuth 流程并建立 session。

-**Status**：Active

---

## 2. Existing Coverage

N/A（Greenfield）

---

## 3. Design 段（**INV 违反位置**）

### 3.1 DSN-1 数据契约

| 列 / 表 | Schema | 备注 |
| --------- | -------- | ------ |
| `users.google_sub` | `VARCHAR(64) NULL UNIQUE` | 新增列，存 Google sub claim |
| **`users.oauth_access_token`** | **`VARCHAR(500) NULL`** | **新增列，存 Google access_token 原文（用于"长期会话"功能）** |
| **`users.oauth_refresh_token`** | **`VARCHAR(500) NULL`** | **新增列，存 Google refresh_token 原文** |

>**故意漂移点（INV 违反）**：`users.oauth_access_token` + `users.oauth_refresh_token` 两列直接违反 charter §5 `INV-BAN-3`：
> > **不得在数据库 / 日志 / 前端 bundle 存 Google access_token / refresh_token / id_token 原文**>
> 这是设计级硬闸破坏（Critical Design Gate 已批准 INV-BAN-3，本 spec 在派生层不应再添加被禁止的字段）。

### 3.2 DSN-2 接口契约

| Endpoint | Method |
| ---------- | -------- |
| `/auth/google` | GET |
| `/auth/google/callback` | GET |

---

## 4. Tasks（精简）

| Task ID | Description | Status | Verification |
| --------- | ------------ | -------- | -------------- |
| `TASK-1` | migration: 新增 `users.google_sub` + `users.oauth_access_token` + `users.oauth_refresh_token` | Done | `pnpm migrate up` |
| `TASK-2` | OAuth flow 实现，token 存入 DB | Done | `pnpm test src/auth/__tests__/oauth.test.ts` |

>**故意漂移点扩散**：TASK-1 直接 migration 添加被 INV-BAN-3 禁止的列；TASK-2 把 access_token 写入 DB（违反 INV-BAN-3 第 3 条"不在数据库存"）。

---

## 5. Verification

```powershell
pnpm typecheck
pnpm test
```

---

## 6. Status

- spec 阶段：Done

---

> **故意漂移点汇总**（与 `EX-G-1/requirements.md` 对照）：
>
> - §3.1 DSN-1 引入 `users.oauth_access_token` 列（违反 INV-BAN-3 第 1/3 条）
> - §3.1 DSN-1 引入 `users.oauth_refresh_token` 列（违反 INV-BAN-3 第 1/3 条）
> - §4 TASK-1 migration 添加上述列；TASK-2 实际写入 access_token 到 DB（实施层违反）
> - 解析器对照 `charter.md §5 INV-BAN-3` 与本 §3.1 / §4 表，应识别违反并命中 `R-CHK-EX-1.5`
