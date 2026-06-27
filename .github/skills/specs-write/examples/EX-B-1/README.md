# EX-B-1 · Brownfield delta canonical example

> **角色**：展示 Brownfield 项目下 spec 的 **delta operation** 显式化路径；覆盖 `Add / Modify / Replace / Deprecate / Preserve` 5 种 delta（`Merge Back` / `Archive Only` 在 `archive.md` 段额外标）。
> 与 `../../protocols/methodology-kernel.md` §4 七种 delta operation 规范字面零漂移。

---

## 1. Example 元数据

| 字段 | 值 |
| ------ | --- |
| Example ID | `EX-B-1` |
| Project Mode | Brownfield |
| Spec Mode | Medium（多文件：charter / requirements / design / tasks） |
| 引用对应 fixture | `F-FIX-1` 缺 delta operation；`F-FIX-3` archive / merge 边界不清 |
| 覆盖语义层 | EXIST-REQ-* + Derivation Map + Existing Coverage + 5 种 delta operation 标记 |
| 状态 | ✅ canonical reference |

---

## 2. 模拟场景

**用户原话**：
> 我们已经上线的 SaaS 通知偏好功能，现在要扩展支持多类邮件（营销 / 交易 / 系统）独立开关，原来那个总开关要保留为兼容期开关；同时把"实时邮件批发"改用新的 Mailgun 通道（替换原来直连 SMTP）；废弃 6 个月前那个 `email_unsubscribe_token` 字段（已经没人用了，且有 PII 风险）；保持现有 `users.marketing_emails_enabled` 列继续存活但只读（migration 期不删除）。

**判定结果**：

- Project Mode = Brownfield（既有上线 feature `EX-M-1` 已 archive）
- Spec Mode = Medium（涉及多个表 / 多个接口，但语义边界清晰，不需要 Large）
- Delta 操作覆盖：5 种（Add / Modify / Replace / Deprecate / Preserve）

---

## 3. 文件清单

| 文件 | 角色 | 状态 |
| ------ | ------ | ------ |
| `README.md` | 本文 | ✅ |
| `charter.md` | Phase 1 Charter（含 EXIST-REQ-* 列） | ✅ |
| `requirements.md` | Phase 2 Requirements（含 Derivation Map + Existing Coverage + 5 种 delta） | ✅ |
| `tasks.md` | Phase 4 Tasks（含 Touches / Verification / Revert / Anti-Invariants） | 简化为 README 中说明，避免文件过多 |
| `archive.md` | feature 完成后追加（含 Merge Back 决策） | ✅ |

为控制 example 体量，本目录不附 `design.md` / `tasks.md` 单独文件；这些段落以最小段落形式嵌入 `requirements.md` 末尾。完整文件结构按 `../../protocols/methodology-kernel.md` 规范，真实项目中应分文件承载。

---

## 4. 与 `R-CHK-EX-1.*` 期望对齐

| Sub-rule | 期望 |
| ---------- | ------ |
| `R-CHK-EX-1.1` Delta operation | 5 种全覆盖（Add / Modify / Replace / Deprecate / Preserve） |
| `R-CHK-EX-1.2` Traceability | EXIST-REQ-*必带 `Source Spec: EX-M-1` 锚点；新 REQ-* 必带 `Derived From: SRC-### + EXIST-REQ-###` 链 |
| `R-CHK-EX-1.3` Archive / merge | archive.md 显式标 Merge Back 决策（多类邮件主开关回并到 long-living `notifications-spec`，不再 Archive Only） |

---

## 5. 与 `F-FIX-*` 应失败 fixture 引用

| Fixture | 失败模式（基于本 example 的伪化） |
| --------- | -------------------------------- |
| `F-FIX-1` | 删除本 example 所有 `Delta Operation` 列 → 期望 `R-CHK-EX-1.1` 命中 |
| `F-FIX-3` | 在 `archive.md` 同时标 `Status: Archive Only` 和 `Merge Back: yes` 矛盾 → 期望 `R-CHK-EX-1.3` 命中 |
