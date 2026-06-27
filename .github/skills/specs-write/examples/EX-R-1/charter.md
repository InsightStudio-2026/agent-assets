# Charter · 用户数据批量导出（EX-R-1 修复后派生）

> **EX-R-1 canonical example · Phase 1 Charter（Repair 后派生）**。本文展示在 Phase 0 三段式 intake 完成、上游 SSOT 修复 PR Merged 后，charter 如何**显式引用修复 PR + 沉淀新增 INV**。
> 与 `../../protocols/methodology-kernel.md` Phase 1 + `R-AUDIT-3~5` + `R-CHK-EX-1.2/1.5/1.6` 字面零漂移。

---

## 1. Sources

| Source ID | 类型 | 内容 | Timestamp |
| ----------- | ------ | ------ | ----------- |
| `SRC-1` | Product Brief（修复后） | "批量导出 Q3 目标；导出字段 = 基本资料（name/email/created_at）+ 行为日志（action_type/timestamp，不含 IP/UA）；不导出 password_hash / phone / id_card" | 2026-06-22（修复后版本，原版本 2026-04-01） |
| `SRC-2` | 用户原话 | "给后台加用户数据批量导出，下载 CSV，运营填 user_id 列表" | 2026-06-20T10:00 |
| `SRC-3` | Repair PR | `PR-REPAIR-EX-R-1-001` Merged 2026-06-22T15:00（用户 + security-team-lead 批准）；含 product-brief 修 + `.github/instructions/data-handling.md §6 PII Export` 新增 | 2026-06-22 |
| `SRC-4` | 修复后 instructions | `.github/instructions/data-handling.md §6 PII Export`（new section） | 2026-06-22 |

`SRC-3` 是 Repair 历史的可追溯锚点：未来任何 reviewer / agent 看到本 charter，都能通过 PR commit hash 回溯整个修复过程，命中 `R-CHK-EX-1.2 traceability`。

---

## 2. Existing Requirements

N/A（Hybrid 项目但本 feature 是数据导出能力的首次实现；无 EXIST-REQ-* 引用）。

---

## 3. Scope

- 后台运营页面提供"批量导出"按钮 + 文本框（粘贴 user_id 列表）。
- 系统校验 user_id 列表（数量上限 1000；admin role 必填）。
- 异步生成 CSV 文件（基本资料 + 最近 30 天行为日志），完成后下载链接通过 audit log 通知。
- 导出字段严格按 `SRC-1`（修复后）定义；不允许扩展。

---

## 4. Out of Charter

- 不导出 `password_hash` / `phone` / `id_card`（INV-BAN-PII-EXPORT-1 强制守护）。
- 不允许非 admin role 触发导出（INV-LIM-PII-EXPORT-2 强制守护）。
- 不实现自定义字段勾选（仅固定字段集）。
- 不支持 > 1000 user 批量（一次最多 1000；超出走分批 spec，未来 feature）。
- 不在客户端做 CSV 生成（仅服务端，避免前端拿到完整 PII）。

---

## 5. Architectural Invariants（含修复后新增）

| Invariant ID | 类型 | 内容 | 来源 | 适用 |
| -------------- | ------ | ------ | ------ | ------ |
| `INV-BAN-PII-EXPORT-1` | 禁止 | 不允许导出 password_hash / phone / id_card / oauth_tokens 等敏感字段 | **新增**（来自 `SRC-3` Repair PR） | 全 feature |
| `INV-LIM-PII-EXPORT-2` | 限制 | 导出操作必须满足：admin role + audit log + 单次 ≤ 1000 user | **新增**（来自 `SRC-3` Repair PR） | 全 feature |
| `INV-SEC-5` | 必须 | CSV 文件存于 S3 + 链接签名 24 小时过期 + 不写持久存储 | 沿用 `.github/instructions/data-handling.md §3` | 文件分发路径 |
| `INV-LIM-1` | 限制 | 后台 API 必须走现有 admin authn middleware | baseline | 全 feature |
| `INV-SEC-1` | 必须 | 操作必须写 audit log（user_id / 导出范围 / 成功失败） | baseline | 全 feature |

`INV-BAN-PII-EXPORT-1` + `INV-LIM-PII-EXPORT-2` 是 Repair 后**新沉淀**的 INV；它们的存在让本 spec 在 design / tasks 阶段有明确的硬守护点，避免裸奔。

---

## 6. Mode 判定 + 三类 Gate 决策

- Project Mode = Hybrid
- Spec Mode = Medium（多文件 charter + maturity-intake；本 example 不展开 requirements/design/tasks，因为演示焦点是 Phase 0 Repair）

| Gate | 判定 | 决策 |
| ------ | ------ | ------ |
| Strategy Gate | 批量导出 = product brief 修复后已批准的 Q3 目标 | `PROCEED` |
| Critical Design Gate | INV-BAN-PII-EXPORT-1 / INV-LIM-PII-EXPORT-2 = 新增 INV → **设计级硬闸**（`R-AUDIT-4`） | `PROCEED_AFTER_REVIEW`（用户批准 Repair PR 时隐式批准 INV 内容；charter 此处复述以满足 Phase 1 显式要求） |
| Real-World Side Effect Gate | S3 bucket 配置 + admin role 数据库变更 = 外部副作用 | `PROCEED_AFTER_REVIEW`（deferred 到 release-deploy） |

---

## 7. Repair 历史复述

charter 必须**显式复述** Repair 历史，避免未来 reviewer 误以为 INV-BAN-PII-EXPORT-1 是凭空出现：

| 阶段 | 输出 | 锚点 |
| ------ | ------ | ------ |
| First-pass intake | 检测 SSOT 不健康 → BLOCKED_SSOT_REPAIR | `maturity-intake.md §1.3` |
| Repair Plan | 修 1 + 修 2 修复方案 + 用户批准 | `maturity-intake.md §2` |
| Repair PR | `PR-REPAIR-EX-R-1-001` Merged | `SRC-3` |
| Second-pass intake | SSOT Health = OK → PROCEED_TO_CHARTER | `maturity-intake.md §3` |
| Charter（本文） | 引用 SRC-3 + 沉淀新 INV | §1 + §5 |

---

## 8. 与 `R-CHK-EX-1.*` 期望对齐

| Sub-rule | Charter 段对齐 |
| ---------- | ---------------- |
| `R-CHK-EX-1.2` Traceability | §1 Sources 锚点（SRC-1~4 含 Repair PR） |
| `R-CHK-EX-1.5` Architectural Invariants | §5 五条 INV，含修复后新增 2 条 |
| `R-CHK-EX-1.6` Out-of-Charter | §4 显式 5 项 out-of-charter 边界 |
