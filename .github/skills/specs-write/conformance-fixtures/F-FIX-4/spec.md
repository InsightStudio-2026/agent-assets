# Spec · 通知偏好（F-FIX-4 伪化版本，故意失败）

> **F-FIX-4 conformance fixture · 故意失败的 spec.md**。基于 `EX-M-1/spec.md` 制造 active/done 状态漂移；不可作为真实 spec 模板使用。
> 期望 `/asset-quality-gates` `R-CHK-EX-1.4 active/done 状态漂移` 命中。

---

## 0. Maturity Intake

| 字段 | 值 |
| ------ | --- |
| Project Maturity | Greenfield |
| Decision | `PROCEED_TO_CHARTER` |

---

## 1. Charter（精简版，仅承载 Status 漂移检查）

### 1.1 Sources

| Source ID | 内容 |
| ----------- | ------ |
| `SRC-1` | 用户原话："加通知偏好开关" |

### 1.2 Architectural Invariants

- `INV-LIM-1`：用户设置变更必须走 authn middleware
- `INV-SEC-1`：变更操作必须写 audit log

---

## 2. Requirements

### 2.1 REQ-1：用户切换通知偏好

- **Derived From**：`SRC-1` → `REQ-1`
- **AC-1.1**：**WHEN** 已登录用户访问页面，**THE SYSTEM SHALL**显示开关状态。

-**AC-1.2**：**WHEN** 用户切换并提交，**THE SYSTEM SHALL**持久化到数据库。
-**Status**：Active

---

## 3. Plan

### 3.1 DSN-1 数据契约

| 字段 | Schema |
| ------ | -------- |
| `users.marketing_emails_enabled` | `BOOLEAN NOT NULL DEFAULT TRUE` |

### 3.2 DSN-2 接口契约

| Endpoint | Method |
| ---------- | -------- |
| `/api/me/notification-preferences` | GET / PATCH |

---

## 4. Tasks（**Mode A + Mode B 漂移点**）

| Task ID | Description | Status | Verification | Artifacts |
| --------- | ------------ | -------- | -------------- | ----------- |
| `TASK-1` | DB migration | Done | `pnpm migrate up` | `artifacts/migrate-up.log` |
| `TASK-2` | API endpoint | Done | `pnpm test src/api/__tests__/notification-preferences.test.ts` | `artifacts/api-test.log` |
| `TASK-3` | UI 组件 + e2e | **Done** | `pnpm test:e2e tests/e2e/notification-prefs.spec.ts` | `artifacts/e2e-screenshot.png` |
| `TASK-4` | audit log 接入 | **Pending** | `pnpm test src/lib/__tests__/audit-notif.test.ts` | (尚未生成) |

DAG：`TASK-1` → `TASK-2` → `TASK-3` → `TASK-4`

>**故意漂移点 1（Mode B）**：TASK-4 标 `Pending`，但 §6 Status 仍写 spec 阶段 = `Done`（spec 不可能 Done 当还有 Pending Task）

---

## 5. Verification

### 5.1 整体命令

```powershell
pnpm typecheck
pnpm lint
pnpm test
pnpm test:e2e -- tests/e2e/notification-prefs.spec.ts
```

### 5.2 DoD

- 全部 Task `Status: Done`。
- 所有 verification PASS。

### 5.3 Verification 结果（**Mode A 漂移点**）

| 检查 | 结果 | Evidence |
| ------ | ------ | --------- |
| typecheck | PASS | `artifacts/typecheck.log` |
| lint | PASS | `artifacts/lint.log` |
| unit + integration | PASS（38 个测试） | `artifacts/test.log` |
| **e2e** | **FAIL（1 关键路径失败：notification-prefs 切换提交后 audit log 未写入）** | `artifacts/e2e-failure.log` |

>**故意漂移点 2（Mode A）**：TASK-3 表标 `Status: Done`，但本表 e2e 行标 `FAIL`；这是显式互斥矛盾（一个真正 Done 的 task 不可能 Verification 仍然 FAIL）。

---

## 6. Status

- spec 阶段：**Done**- archive 决策：未填写（暂略；本 fixture 不复制 archive.md）

>**故意漂移点 3**：本节标 `Done`，但 §4 TASK-4 仍是 `Pending` + §5.3 e2e 仍 FAIL；spec 阶段不可能在子任务未完成且验证未通过时为 Done。

---

> **故意漂移点汇总**（与 `EX-M-1/spec.md` 对照）：
>
> - §4 TASK-3 `Status: Done` ↔ §5.3 e2e 结果 `FAIL`（Mode A 矛盾）
> - §4 TASK-4 `Status: Pending` ↔ §6 spec Status `Done`（Mode B 矛盾）
> - checker 应在两个子模式中任一命中即报错（不要求两者同时存在才报错）
