# Expected Failure · F-FIX-6

> 期望 `/asset-quality-gates` Phase 3.6 对本 fixture 的识别结果。

---

## 1. 期望失败信号

| 字段 | 期望值 |
| ------ | -------- |
| Final state | `CHECKS_FAILED_NEEDS_REVISION` |
| 命中规则 | `R-CHK-EX-1.6 out-of-charter scope violation` |
| 严重性 | **Critical** |
| 失败位置 | `tasks.md` `TASK-X` |

---

## 2. 期望报告内容

```markdown
## R-CHK-EX-1.6 out-of-charter scope violation · F-FIX-6

-**严重程度 (Severity)**: Critical

- **审计发现 (Findings)**:
  - charter.md §3 Out-of-Charter 第 1 项: "不接 GitHub OAuth（MVP 仅 Google）"
  - tasks.md `TASK-X` Description: "GitHub OAuth provider 接入"，Touches `src/auth/github/*.ts` + `users.github_sub` 列
  - TASK-X 直接引入被 charter §3 排除的功能 → Strategy Gate 边界破坏
- **预期要求 (Expected)**: tasks 不得引入 charter §3 Out-of-Charter 列出的功能；如需扩展，必须先在 charter §2 Scope 加入 + Strategy Gate 用户批准
- **处置动作 (Action)**: BLOCK spec close-out + REQUIRE charter scope revisit

```

---

## 3. 误识别（不应命中）

| 规则 | 不应误命中原因 |
| ------ | --------------- |
| `R-CHK-EX-1.1` | 本 fixture 是 Greenfield；delta operation 不适用 |
| `R-CHK-EX-1.2` | `Derived From` 字段保留 |
| `R-CHK-EX-1.5` | 本 fixture 不违反 INV-BAN-*/ INV-LIM-* |

---

## 4. checker 实现提示

| 检测点 | 检测方式 |
| -------- | --------- |
| Out-of-Charter 解析 | charter.md §4（或同义段名）每条排除项以 keyword + 自然语言提取 |
| 越界检测 | 解析 tasks.md `Description` / `Touches` 字段，对每个 task 与 out-of-charter keyword 做匹配；命中即报错 |
| 严重性 = Critical | scope 越界 = Strategy Gate 边界破坏 |
| 误命中防御 | 如 charter §3 已修订（删除对应 out-of-charter 项）→ 不再触发 |
