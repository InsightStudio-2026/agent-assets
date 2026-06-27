# F-FIX-5 · INV-BAN-* 违反

> **角色**：应失败 fixture #5。模拟 spec design 段引入了被 charter §5 Architectural Invariants 显式禁止的依赖 / 模式；期望 `R-CHK-EX-1.5 architectural invariants violation` 命中。
> 来源：基于 `EX-G-1` 伪化（charter 标 INV-BAN-3 不存 OAuth token，但 design DSN-1 引入 `users.oauth_access_token` 列）。

---

## 1. Fixture 元数据

| 字段 | 值 |
| ------ | --- |
| Fixture ID | `F-FIX-5` |
| 引用 example | `EX-G-1`（伪化变体） |
| 失败模式 | charter §5 INV-BAN-3 显式禁止某项；design 段直接违反 |
| 期望识别错误 | `R-CHK-EX-1.5 architectural invariants violation` |
| 严重性 | **Critical**（INV 违反 = 设计级硬闸破坏） |
| 状态 | ✅ canonical fixture |

---

## 2. 失败定义

`F-FIX-5` 是单子模式失败：

| 失败位置 | 内容 |
| --------- | ------ |
| `charter.md` §5（保留 EX-G-1 原文） | INV-BAN-3：禁止存 Google access_token / refresh_token / id_token 原文 |
| `requirements.md` §3.1 DSN-1 数据契约（伪化） | **新增**`users.oauth_access_token VARCHAR(500)` 列，违反 INV-BAN-3 |

`R-CHK-EX-1.5` 严重性 =**Critical**，因为 INV 是 charter 阶段经过用户批准的设计级硬闸，下游违反等于绕过 Critical Design Gate。

---

## 3. 文件清单

| 文件 | 角色 | 与 EX-G-1 差异 |
| ------ | ------ | --------------- |
| `README.md` | 本文 | 新增 |
| `charter.md` | 仿 EX-G-1 charter（保留 INV-BAN-3） | 不变（基线） |
| `requirements.md` | 伪化 EX-G-1 requirements | §3.1 DSN-1 新增 `users.oauth_access_token` 列 |
| `expected-failure.md` | 期望识别报告 | 新增 |

---

## 4. 修复建议

| 步骤 | 动作 |
| ------ | ------ |
| 1 | requirements.md §3.1 删除 `users.oauth_access_token` 列；OAuth 流程不持久化 token，每次重新走完整 OAuth |
| 2 | 如确实需要长期保存 token：先在 charter §5 修改 INV-BAN-3（需 Critical Design Gate 用户重新批准）后再添加列 |
| 3 | 重跑 `/asset-quality-gates` Phase 3.6，期望 `R-CHK-EX-1.5` PASS |

---

## 5. 与 R-CHK-EX-1.5 期望对齐

| 检查点 | 期望 fixture 状态 |
| -------- | ------------------ |
| charter §5 是否定义 INV-BAN-*/ INV-LIM-*？ | ✅ 是（INV-BAN-3 保留） |
| requirements / design 是否违反某 INV？ | ❌ 是（DSN-1 引入被 INV-BAN-3 禁止的列） |
| 期望 `R-CHK-EX-1.5` 命中？ | ✅ 命中，severity = Critical |
