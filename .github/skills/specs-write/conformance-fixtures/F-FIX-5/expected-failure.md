# Expected Failure · F-FIX-5

> 期望 `/asset-quality-gates` Phase 3.6 对本 fixture 的识别结果。

---

## 1. 期望失败信号

| 字段 | 期望值 |
| ------ | -------- |
| Final state | `CHECKS_FAILED_NEEDS_REVISION` |
| 命中规则 | `R-CHK-EX-1.5 architectural invariants violation` |
| 严重性 | **Critical** |
| 失败位置 | `requirements.md` §3.1 + §4 |

---

## 2. 期望报告内容

```markdown
## R-CHK-EX-1.5 architectural invariants violation · F-FIX-5

-**严重程度 (Severity)**: Critical

- **审计发现 (Findings)**:
  - charter.md §5 定义 `INV-BAN-3`: 不得在数据库 / 日志 / 前端 bundle 存 Google access_token / refresh_token / id_token 原文
  - requirements.md §3.1 DSN-1 引入 `users.oauth_access_token` + `users.oauth_refresh_token` 列 → 直接违反 INV-BAN-3 第 1 / 第 3 条
  - requirements.md §4 TASK-1 migration 添加被禁止的列；TASK-2 把 token 写入 DB
- **预期要求 (Expected)**: design / tasks 不得引入被 INV-BAN-* 禁止的字段、依赖、模式；如确需变更 INV，必须先在 charter §5 修改 + Critical Design Gate 用户批准
- **处置动作 (Action)**: BLOCK spec close-out + REQUIRE charter INV revisit + RWSE Gate 用户批准

```

---

## 3. 误识别（不应命中）

| 规则 | 不应误命中原因 |
| ------ | --------------- |
| `R-CHK-EX-1.1` | 本 fixture 是 Greenfield；delta operation 不适用 |
| `R-CHK-EX-1.2` | `Derived From` 字段保留 |
| `R-CHK-EX-1.4` | Tasks Status 与 verification 一致（即使 verification 浅薄但不矛盾） |

---

## 4. checker 实现提示

| 检测点 | 检测方式 |
| -------- | --------- |
| INV 解析 | 解析 charter.md §5 表，提取每条 INV-BAN-*/ INV-LIM-* / INV-SEC-* 的内容（自然语言或 keyword） |
| 违反检测（schema 层） | 解析 requirements.md §3.1 DSN-1 / 等价段，对每个新增列 / 表名 / endpoint，与 INV-BAN 内容做 keyword + 语义匹配 |
| 违反检测（实施层） | 解析 §4 Tasks Description / Touches，对涉及"写入 token / 持久化敏感数据 / 暴露 PII"等动作做 keyword 匹配 |
| 严重性 = Critical | INV-BAN 违反 = 设计级硬闸破坏；severity 永远 Critical 不降级 |
| 误命中防御 | charter §5 修改 INV-BAN-3 后（如允许存 hashed token），不再触发本规则；checker 必须以 charter 当前版本作为基线 |
