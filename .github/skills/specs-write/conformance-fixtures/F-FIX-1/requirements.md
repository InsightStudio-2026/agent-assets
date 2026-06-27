# Requirements · 多类通知偏好（F-FIX-1 伪化版本，故意失败）

> **F-FIX-1 conformance fixture · 故意失败的 requirements.md**。基于 `EX-B-1/requirements.md` 删除所有 delta operation 标记；不可作为真实 spec 模板使用。
> 期望 `/asset-quality-gates` `R-CHK-EX-1.1 missing delta operation` 命中。

---

## 1. Derivation Map（已删除"关系类型"列 → 触发失败）

| 本 feature 锚点 | 来源 | 说明 |
| ---------------- | ------ | ------ |
| `REQ-1` 多类邮件订阅 | `SRC-1` + `EXIST-REQ-1` | 新增 marketing / digest / system_alerts 三类，老总开关变兼容期 fallback |
| `REQ-2` 多类 endpoint schema | `SRC-1` + `EXIST-REQ-2` | GET 返回扩展 schema，PATCH 旧 endpoint 删除 |
| `REQ-3` Mailgun 批发切换 | `SRC-4` + `EXIST-REQ-3` | 引入 mailgun-adapter，删除 smtp-direct |
| `REQ-4` 废弃 `email_unsubscribe_token` | `SRC-3` + `EXIST-REQ-4` | Day 0 停写 + Day 30 DROP COLUMN |
| `REQ-5` audit log 行为保留 | `EXIST-REQ-5` | 多类切换路径仍写 audit log，schema 不变 |

---

## 2. Requirements 表

### 2.1 REQ-1：多类邮件订阅

- **Derived From**：`SRC-1` → `REQ-1`；引用 `EXIST-REQ-1`（EX-M-1 REQ-1）
- **Relation to Existing**：兼容期 30 天双向同步
- **AC-1.1**：**WHEN** 已登录用户访问"通知偏好"页面，**THE SYSTEM SHALL**显示 marketing / digest / system_alerts 三类独立开关。

-**AC-1.2**：**WHEN** 用户切换某一类开关并提交，**THE SYSTEM SHALL**upsert `notification_preferences` 并写 audit log。
-**Status**：Active

### 2.2 REQ-2：多类 endpoint schema

- **Derived From**：`SRC-1` → `REQ-2`；引用 `EXIST-REQ-2`
- **Relation to Existing**：GET 字段扩展（向后兼容），PATCH 旧版本整体替换为新版本
- **AC-2.1**：**WHEN** 调用 GET，**THE SYSTEM SHALL**返回 `{categories, _legacy_marketing_emails_enabled, updated_at}`。

-**AC-2.2**：**WHEN** 调用老 PATCH（仅 `{marketing_emails_enabled}`），**THE SYSTEM SHALL**返回 `400 LEGACY_PATCH_DEPRECATED`。
-**Status**：Active

### 2.3 REQ-3：Mailgun 批发切换

- **Derived From**：`SRC-4` → `REQ-3`；引用 `EXIST-REQ-3`
- **Relation to Existing**：`smtp-direct.ts` Done 时删除
- **AC-3.1**：**WHEN** 系统投递任意类邮件，**THE SYSTEM SHALL**通过 `mailgun-adapter.ts` 走 Mailgun API。

-**Status**：Active

### 2.4 REQ-4：废弃 `email_unsubscribe_token`

- **Derived From**：`SRC-3` → `REQ-4`；引用 `EXIST-REQ-4`
- **Relation to Existing**：Day 0 停写，Day 30 DROP COLUMN
- **AC-4.1**：**WHEN** Day 0 部署完成，**THE SYSTEM SHALL**不再向 `email_unsubscribe_token` 写入新值。

-**AC-4.3**：**WHEN** Day 30 + 调用量 0 + 7 天观察期通过，**THE SYSTEM SHALL**执行 `DROP COLUMN`。
-**Status**：Active（migration 期）

### 2.5 REQ-5：audit log 行为保留

- **Derived From**：`EXIST-REQ-5`（EX-M-1 INV-SEC-1）
- **Relation to Existing**：现有 `audit.write` 调用路径完全保留
- **AC-5.1**：**WHEN** 任意类开关切换，**THE SYSTEM SHALL**调用 `audit.write(user_id, field='notification_preferences.{category}', old, new)`。

-**Status**：Active（unchanged from EX-M-1）

---

> **故意漂移点**（与 `EX-B-1/requirements.md` 对照可见的失败位置）：
>
> - §1 表头删除 `关系类型` 列，整张 Derivation Map 没有 Add / Modify / Replace / Deprecate / Preserve 任一标记
> - §2.1~2.5 各 REQ 字段中**整体删除** `**Delta Operation**` 行（原 EX-B-1 中第一个字段）
> - 解析器无法从 charter.md / requirements.md 任一处重建 5 种 delta operation 信息
