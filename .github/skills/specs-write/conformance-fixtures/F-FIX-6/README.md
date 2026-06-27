# F-FIX-6 · Out-of-Charter 越界

> **角色**：应失败 fixture #6。模拟 tasks.md 的 `Touches` 越出 charter §3 Scope / §4 Out-of-Charter 边界；期望 `R-CHK-EX-1.6 out-of-charter scope violation` 命中。
> 来源：基于 `EX-G-1` 伪化（charter 显式 out-of-charter "不接 GitHub OAuth"，但 tasks 添加 GitHub OAuth provider）。

---

## 1. Fixture 元数据

| 字段 | 值 |
| ------ | --- |
| Fixture ID | `F-FIX-6` |
| 引用 example | `EX-G-1`（伪化变体） |
| 失败模式 | tasks `Touches` / `Description` 引入 charter §4 显式 out-of-charter 的功能 |
| 期望识别错误 | `R-CHK-EX-1.6 out-of-charter scope violation` |
| 严重性 | **Critical** |
| 状态 | ✅ canonical fixture |

---

## 2. 失败定义

| 失败位置 | 内容 |
| --------- | ------ |
| `charter.md` §4 | "不接 GitHub / Microsoft / Apple OAuth"（显式 out-of-charter） |
| `tasks.md` TASK-X | 新增 task：`GitHub OAuth provider 接入`（直接越界） |

`R-CHK-EX-1.6` severity = Critical：scope 越界 = Strategy Gate 边界破坏。

---

## 3. 文件清单

| 文件 | 角色 | 与 EX-G-1 差异 |
| ------ | ------ | --------------- |
| `README.md` | 本文 | 新增 |
| `charter.md` | 仿 EX-G-1 charter（保留 §4 out-of-charter 列表） | 不变 |
| `tasks.md` | 伪化 EX-G-1 tasks | 新增 TASK-X "GitHub OAuth provider"（越界） |
| `expected-failure.md` | 期望识别报告 | 新增 |

---

## 4. 修复建议

| 步骤 | 动作 |
| ------ | ------ |
| 1 | 删除 tasks.md 新增的越界 TASK-X；GitHub OAuth 走单独 spec |
| 2 | 如确实需要本 spec 接 GitHub OAuth：先在 charter §3 Scope 加入 + §4 删除对应 out-of-charter 项（需 Strategy Gate 用户重新批准） |
| 3 | 重跑 `/asset-quality-gates` Phase 3.6，期望 `R-CHK-EX-1.6` PASS |

---

## 5. 与 R-CHK-EX-1.6 期望对齐

| 检查点 | 期望 fixture 状态 |
| -------- | ------------------ |
| charter §3 Scope / §4 Out-of-Charter 是否定义？ | ✅ 是 |
| tasks.md 是否有 task 越界？ | ❌ 是（TASK-X = GitHub OAuth） |
| 期望 `R-CHK-EX-1.6` 命中？ | ✅ 命中，severity = Critical |
