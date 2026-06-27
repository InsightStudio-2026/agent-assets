# Charter · Google OAuth 登录（F-FIX-5 复制基线）

> **F-FIX-5 conformance fixture · charter 基线**。本文复制 `EX-G-1/charter.md` §5 Architectural Invariants 段作为 INV 守护基线（保留 INV-BAN-3）；其他段精简。
> 与 `EX-G-1/charter.md` 的关键差异：本 charter **不变**；伪化点在下游 `requirements.md` §3.1 DSN-1。

---

## 1. Sources

| Source ID | 内容 |
| ----------- | ------ |
| `SRC-1` | 用户原话："加 Google OAuth 登录" |

---

## 2. Scope

- 用户在登录页可点击 "Continue with Google" 完成 OAuth 流程并建立 session。

---

## 3. Out of Charter

- 不接 GitHub / Microsoft / Apple OAuth。
- 不实现 OAuth 注销 / 解绑 UI。

---

## 4. Derivation Constraints

- 必须复用现有 `users` 表 + 新增 `users.google_sub` 列。
- 必须复用现有 authn middleware + session store。

---

## 5. Architectural Invariants（**INV 守护基线，不可被下游违反**）

| Invariant ID | 类型 | 内容 |
| -------------- | ------ | ------ |
| `INV-SEC-2` | 必须 | OAuth state 随机 16+ bytes + 5 分钟 TTL + 回调时校验 |
| `INV-SEC-3` | 必须 | redirect_uri 走 server-side allowlist |
| `INV-SEC-4` | 必须 | ID Token 走 Google JWKS 校验 |
| `INV-BAN-3` | **禁止** | **不得在数据库 / 日志 / 前端 bundle 存 Google access_token / refresh_token / id_token 原文** |
| `INV-LIM-3` | 限制 | OAuth callback 必须走 HTTPS（dev 例外） |

**INV-BAN-3 是本 fixture 失败检查的关键**：requirements.md §3.1 违反它即触发 `R-CHK-EX-1.5`。

---

## 6. Mode 判定

- Project Mode = Greenfield
- Spec Mode = Medium
