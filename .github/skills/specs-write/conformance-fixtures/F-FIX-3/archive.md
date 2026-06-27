# Archive · 多类通知偏好（F-FIX-3 伪化版本，故意失败）

> **F-FIX-3 conformance fixture · 故意失败的 archive.md**。基于 `EX-B-1/archive.md` 同时声明 `Archive Only` 与 `Merge Back`（矛盾），并删除决策矩阵的最终决策行。
> 期望 `/asset-quality-gates` `R-CHK-EX-1.3 archive/merge boundary unclear` 命中（severity = Critical）。

---

## 1. Archive 元数据（Mode A 失败：同时声明 Archive Only + Merge Back）

| 字段 | 值 |
| ------ | --- |
| Spec ID | `F-FIX-3 / 多类通知偏好` |
| Archive 时间 | 2026-08-30T18:00 |
| Spec 阶段 | Done |
| Archive 决策 | **Archive Only** |
| Merge Back 目标 | `docs/specs/notifications-spec.md`（long-living；本 feature 是其首次实质 contribution） |
| Merge Back PR | `merge-back/notifications-spec-from-EX-B-1`（已计划合入） |
| 后续扩展 | 邮件 / 短信 / 推送扩展均回并到 `notifications-spec` |

>**故意漂移点 1（Mode A）**：本表同时存在 `Archive 决策 = Archive Only` 与 `Merge Back 目标` / `Merge Back PR`。这两者**互斥**：Archive Only 表示不并入 long-living spec，但本表又给出了具体合入目标和 PR，逻辑矛盾。

---

## 2. Merge Back 决策矩阵（Mode B 失败：缺最终决策行）

| 决策维度 | 判定 |
| --------- | ------ |
| 是否存在 long-living spec？ | 否（首次建立；EX-M-1 是 Archive Only，未建 long-living） |
| 当前 feature 是否需要长期演进？ | 是（多类邮件 → 未来短信 / 推送 / Lark 渠道扩展） |
| 是否会出现引用本 REQ 的新 feature？ | 是（短信通道扩展将引用 REQ-1 多类语义） |
| 是否有 Architectural Invariants 需长期守护？ | 是（INV-BAN-2 / INV-LIM-2 / INV-SEC-1） |

> **故意漂移点 2（Mode B）**：本决策矩阵列出了 4 个判定维度，但**缺最终决策行**（`EX-B-1/archive.md` 原本在 §2 末尾有 `**最终决策**：Status: Merge Back，目标 = ...` 一行，本 fixture 整段删除）。结果是：reader 看到 4 维判定后无法直接得出 archive 决策结论；checker 无法定位最终状态。

---

## 3. Merge Back 操作（保留以便混淆）

### 3.1 合入目标

| 来源（本 spec） | 合入位置 | Status 变更 |
| -------------- | --------- | ------------- |
| `REQ-1` 多类邮件订阅 | `notifications-spec.md` §2 REQ-NOTIF-1 | Active in long-living spec |
| `REQ-2` 多类 endpoint schema | `notifications-spec.md` §3 DSN-NOTIF-1 | Active |
| `REQ-3` Mailgun 批发 | `notifications-spec.md` §3 DSN-NOTIF-2 | Active |

> **附加混淆**：本段 §3 的存在与 §1 `Archive 决策 = Archive Only` 进一步矛盾。Archive Only 不应有"合入目标"段，但本 fixture 故意保留以制造典型漂移姿态。

---

## 4. 数据保留

| 项 | 保留位置 |
| ---- | --------- |
| spec 文件 | 同目录（不动） |
| migrations | `migrations/2026-08-15-add-notification-preferences.sql`（已应用） |
| audit log 历史 | `audit_log` 表持续保留 |

---

## 5. 与 `R-CHK-EX-1.3 archive / merge 边界` 期望对齐（自查表，故意全错）

| Sub-rule 检查点 | 本 archive 状态 |
| ---------------- | ---------------- |
| 是否显式声明 Archive Only **或**Merge Back（恰好一个）？ | ❌ 否（§1 同时声明两个） |
| 是否同时声明 Archive Only 和 Merge Back？ | ✅ 是（矛盾，§1 字段并存 + §3 合入目标段保留） |
| 是否给出决策理由（决策矩阵）？ | ⚠️ 部分（§2 矩阵存在但缺最终决策行） |
| 是否说明合入边界？ | ⚠️ 部分（§3 合入目标存在但与 Archive Only 决策矛盾） |
| 期望 `R-CHK-EX-1.3` 命中？ | ✅ 命中，severity = Critical |

---

>**故意漂移点汇总**（与 `EX-B-1/archive.md` 对照可见的失败位置）：
>
> - §1 元数据表同时填 `Archive 决策 = Archive Only` 与 `Merge Back 目标` / `Merge Back PR`（Mode A 矛盾）
> - §2 决策矩阵尾部**整体删除**最终决策行（原 EX-B-1 archive.md 的 `**最终决策**：Status: Merge Back，目标 = ...`）
> - §3 合入目标段保留 → 与 §1 Archive Only 进一步矛盾
> - 解析器从 §1 + §2 + §3 任一处都无法得出唯一一致的 archive 决策结论
