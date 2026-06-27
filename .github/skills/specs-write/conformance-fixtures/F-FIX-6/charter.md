# Charter · Google OAuth 登录（F-FIX-6 复制基线）

> **F-FIX-6 conformance fixture · charter 基线**。复制 `EX-G-1/charter.md` §3 Scope + §4 Out-of-Charter 段作为 scope 边界基线（保留显式 out-of-charter "不接 GitHub OAuth"）；其他段精简。
> 与 `EX-G-1/charter.md` 关键差异：本 charter **不变**；伪化点在下游 `tasks.md`。

---

## 1. Sources

| Source ID | 内容 |
| ----------- | ------ |
| `SRC-1` | 用户原话："加 Google OAuth 登录" |

---

## 2. Scope（**正面边界**）

- 用户在登录页可点击 "Continue with Google" 完成 OAuth 流程并建立 session。
- OAuth provider 仅 **Google**。

---

## 3. Out of Charter（**反面边界，下游不可越**）

- **不接 GitHub OAuth**（MVP 仅 Google；GitHub 接入走单独 spec）
- **不接 Microsoft OAuth**-**不接 Apple OAuth**- 不实现 OAuth 注销 / 解绑 UI**§3 第 1 项是本 fixture 失败检查的关键**：tasks.md 越过此边界即触发 `R-CHK-EX-1.6`。

---

## 4. Architectural Invariants

| INV ID | 内容 |
| -------- | ------ |
| `INV-SEC-2` | OAuth state 防 CSRF |
| `INV-LIM-3` | OAuth callback 走 HTTPS |

---

## 5. Mode 判定

- Project Mode = Greenfield
- Spec Mode = Medium
