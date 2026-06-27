# Archive · 通知偏好（EX-M-1）

> **EX-M-1 canonical example · archive 阶段**。本文展示 Greenfield Medium spec 完成后的 **Archive Only**决策（无回并 long-living spec）。
> 与 `../../protocols/methodology-kernel.md` archive vs merge back 边界字面零漂移。

---

## 1. Archive 元数据

| 字段 | 值 |
| ------ | --- |
| Spec ID | `EX-M-1` 通知偏好 |
| Archive 时间 | 2026-05-24T18:00 |
| Spec 阶段 | Done（5 段全 Done + verification PASS） |
| Archive 决策 | **Archive Only**（不 Merge Back） |
| Long-living spec 候选 | 无（项目早期，尚未建立 `notifications-spec` 长期规格） |
| 后续扩展 | `EX-B-1` 多类邮件分类，作为 **Brownfield delta** 派生，非本 spec 续写 |

---

## 2. Merge Back 决策矩阵

| 决策维度 | 判定 | 结论 |
| --------- | ------ | ------ |
| 是否存在 long-living spec？ | 否 | → Archive Only |
| 当前 feature 是否需要长期演进？ | 否（MVP 单开关） | → Archive Only |
| 后续是否会出现引用本 REQ 的新 feature？ | 是（`EX-B-1`） | 后续 spec 用 `EXIST-REQ-*` 引用，但本 spec **不并入**新 spec |

**最终决策**：`Status: Archive Only`，原因 = MVP 早期，long-living `notifications-spec` 尚未建立；future Brownfield 扩展按 `EXIST-REQ-*` 引用本 spec 的 REQ-1 即可，不需要回并。

---

## 3. 与 `EX-B-1` 的关系

- `EX-B-1` Brownfield delta 在 Phase 2 通过 `EXIST-REQ-1`（指向本 archive 的 REQ-1）进行 `Modify` / `Replace` 操作。
- 本 archive 的 REQ-1 / TASK-1~3 / DSN-1~3 全部冻结；`EX-B-1` 不修改本 archive 任何字段，只声明 delta operation。
- 本 archive 是 `EX-B-1` 的**事实源**，不是它的"待修改基线"。

---

## 4. 数据保留

| 项 | 保留位置 |
| ---- | --------- |
| spec.md 原文 | 同目录 `../EX-M-1/spec.md`（不动） |
| migration | `migrations/2026-05-24-add-mail-pref.sql`（已应用，不回滚） |
| audit log 历史 | `audit_log` 表持续保留 |
| artifacts/ | `artifacts/migrate-up.log` / `api-test-output.log` / `e2e-screenshot.png` 等不删除（作为权利链证据） |

---

## 5. 与 `R-CHK-EX-1.3 archive / merge 边界` 期望对齐

| Sub-rule | 本 archive 状态 |
| ---------- | ---------------- |
| 是否显式声明 Archive Only 或 Merge Back？ | ✅ §1 显式声明 `Archive Only` |
| 是否同时声明 Archive Only 和 Merge Back？ | ✅ 否（不矛盾） |
| 是否给出决策理由（决策矩阵）？ | ✅ §2 决策矩阵 |
| 是否说明 long-living spec 关系？ | ✅ §1 + §3 显式说明 |

应通过 `R-CHK-EX-1.3` 检查；对应"应失败" fixture 是 `F-FIX-3`（同时声明两者或两者都不声明）。
