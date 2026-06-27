# Charter · Google OAuth 登录（EX-G-1 Greenfield happy path）

> **EX-G-1 canonical example · Phase 0 Maturity Intake + Phase 1 Charter**。本文展示 Greenfield 项目第一个 spec 的 charter 写法：完整 Sources / Scope / Out-of-Charter / Derivation Constraints / Architectural Invariants 五段，外加 Mode 判定 + 三类 Gate 决策。
> 与 `../../protocols/methodology-kernel.md` Greenfield 路径字面零漂移。

---

## 0. Maturity Intake

| 字段 | 值 |
| ------ | --- |
| Project Maturity | Greenfield（项目第一年；已有 username/password 认证基础设施作为 baseline，但首次接入第三方 OAuth） |
| Audit Profile | Baseline Survey（Greenfield 不需 Scoped Full-Surface Audit；只需基础设施勘察） |
| SSOT Health | OK（项目立项已批准 product brief 含"接入第三方登录"为 Q3 目标，作为 SRC-1） |
| Confidence | High（场景边界清晰；技术栈已选定） |
| Decision | `PROCEED_TO_CHARTER` |
| Blocking Issues | 无 |
| SSOT Stewardship Suggestions | 建议 feature Done 后将 OAuth 配置 schema 沉淀到 `.github/instructions/auth-providers.md`（不属于本 spec scope） |

---

## 1. Sources

| Source ID | 类型 | 内容 | Timestamp |
| ----------- | ------ | ------ | ----------- |
| `SRC-1` | Product Brief | "Q3 接入第三方登录，首先 Google" | 2026-04-01 |
| `SRC-2` | 用户原话 | "MVP 只接 Google；新用户自动建账号；已注册邮箱走 OAuth 时账号合并" | 2026-05-30T09:00 |
| `SRC-3` | 技术调研 | Google OAuth 2.0 Authorization Code Flow + ID Token 验证标准；现有 authn middleware 兼容 session-based auth | 2026-05-30 |
| `SRC-4` | 安全审查 | OAuth state 参数防 CSRF + redirect_uri allowlist + ID Token 签名验证（必须本地缓存 Google JWKS） | 2026-05-30 |

---

## 2. Scope

- 用户在登录页可点击 "Continue with Google" 按钮，跳转 Google 完成 OAuth 授权。
- 授权返回后系统校验 ID Token 并建立 session（沿用现有 authn middleware）。
- 新邮箱 → 自动建账号；已注册邮箱 → 账号合并（链接 Google sub claim 到现有 user record）。
- OAuth 配置（client_id / client_secret / redirect_uri）从环境变量读取，不写代码。

---

## 3. Out of Charter

- 不接 GitHub / Microsoft / Apple OAuth（MVP 只接 Google）。
- 不实现 OAuth 注销（仅删 session；Google 端 token revoke 后续 spec）。
- 不实现 OAuth 账号解绑 UI（建账号后无法解除 Google 关联）。
- 不实现 first-login 用户名设置向导（沿用 email 前缀作为默认 username）。
- 不修改现有 username/password 登录入口（双登录方式并存）。

---

## 4. Derivation Constraints

- **必须**复用现有 `users` 表 + 新增 `users.google_sub`（Google 用户唯一 ID，可空，UNIQUE 约束）。
- **必须**复用现有 authn middleware + session store（不引入新 session 机制）。
- **不得**在数据库中存 Google access_token / refresh_token（只存 `google_sub` 关联，重新授权按需走完整 OAuth 流程）。
- **必须**在生产部署前在 Google Cloud Console 注册 OAuth client（Real-World Side Effect Gate）。

---

## 5. Architectural Invariants

| Invariant ID | 类型 | 内容 | 适用 |
| -------------- | ------ | ------ | ------ |
| `INV-SEC-2` | 必须 | OAuth state 参数随机 16+ bytes + 存 session 5 分钟 + 回调时校验匹配 | OAuth 流程全程 |
| `INV-SEC-3` | 必须 | redirect_uri 走 server-side allowlist（环境变量 `OAUTH_REDIRECT_ALLOWLIST`） | `/auth/google/callback` |
| `INV-SEC-4` | 必须 | ID Token 签名校验走 Google JWKS（`https://www.googleapis.com/oauth2/v3/certs`），本地缓存 1 小时 | ID Token 验证 |
| `INV-BAN-3` | 禁止 | 不得在数据库 / 日志 / 前端 bundle 存 Google access_token / refresh_token / id_token 原文 | 全 feature |
| `INV-LIM-3` | 限制 | OAuth callback 必须走 HTTPS（local dev 例外，但 staging / prod 强制） | `/auth/google/callback` |

---

## 6. Mode 判定

- Project Mode = Greenfield
- Spec Mode = Medium（多文件 charter + requirements + archive；design 嵌入 requirements 末尾，不独立 design.md）
- 三类 Gate 决策（按 `../../references/cross-cutting.md`）：

| Gate | 判定 | 决策 | 用户批准时机 |
| ------ | ------ | ------ | ------------ |
| Strategy Gate | OAuth 接入 = product brief 已批准的 Q3 目标 | `PROCEED` | charter 阶段已隐式（product brief 已批准） |
| Critical Design Gate | 账号合并策略（已注册邮箱第一次 OAuth 时自动合并 vs 拒绝） | `PROCEED_AFTER_REVIEW` | requirements.md REQ-3 显式审查 → 用户批准"自动合并"策略 |
| Real-World Side Effect Gate | Google Cloud Console 注册 OAuth client（外部依赖建立 + client_secret 写入生产 secrets manager） | `PROCEED_AFTER_REVIEW` | release-deploy 时再次确认（不在本 spec close-out 范围内，但 spec 必须列入 deferred decisions） |

---

## 7. 与 `R-CHK-EX-1.*` 期望对齐

| Sub-rule | Charter 段对齐 |
| ---------- | ---------------- |
| `R-CHK-EX-1.2` Traceability | §1 Sources 锚点（SRC-1~4）；下游 requirements.md REQ-* 通过 `Derived From: SRC-### → REQ-###` 闭环 |
| `R-CHK-EX-1.5` Architectural Invariants | §5 五条 INV 显式（INV-SEC-2/3/4 + INV-BAN-3 + INV-LIM-3）；下游 design 不得违反 |
| `R-CHK-EX-1.6` Out-of-Charter | §3 显式 5 项 out-of-charter 边界 |
