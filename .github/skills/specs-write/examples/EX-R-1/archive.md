# Archive · 用户数据批量导出（EX-R-1 Spec repair）

> **EX-R-1 canonical example · archive 阶段**。本文展示 Spec Repair 完成后的 archive 决策；除常规 Archive Only 决策外，**额外记录 Repair 历史**作为权利链证据。
> 与 `../../protocols/methodology-kernel.md` archive vs merge back 边界 + Repair 路径字面零漂移。

---

## 1. Archive 元数据

| 字段 | 值 |
| ------ | --- |
| Spec ID | `EX-R-1` 用户数据批量导出 |
| Archive 时间 | 2026-07-15T18:00（spec close-out；Phase 2-5 走通后归档） |
| Spec 阶段 | Done |
| Archive 决策 | **Archive Only**（spec close-out 时上游已修，本 spec 无需 Merge Back） |
| Long-living spec 候选 | 建议建立 `.github/instructions/pii-export.md`（承载 INV-BAN-PII-EXPORT-1 + INV-LIM-PII-EXPORT-2 的长期版本，独立于 `data-handling.md §6`）；不在本 spec scope，作为 stewardship suggestion |
| Repair 历史 | 见 §3 |

---

## 2. Merge Back 决策矩阵

| 决策维度 | 判定 | 结论 |
| --------- | ------ | ------ |
| 是否存在 long-living spec？ | 否（修复时只补了 `data-handling.md §6`，未建独立 long-living spec） | → Archive Only |
| 当前 feature 是否需要长期演进？ | 是（PII 导出 INV 会被未来"用户行为分析导出" / "BI 分析数据下载"等 feature 引用） | Archive Only + 后续通过 EXIST-REQ 引用 |
| 修复后新增 INV 是否已沉淀长期？ | ✅（`.github/instructions/data-handling.md §6` 长期承载） | 不需要本 archive 重复 |

**最终决策**：`Status: Archive Only`。本 spec 不 Merge Back；新增 INV 已通过 Repair PR 沉淀到 instructions 文档；后续 PII 导出类 feature 直接引用 instructions 文档而非本 archive。

---

## 3. Repair 历史（权利链证据）

### 3.1 Phase 0 三段式 intake

| 阶段 | 时间 | 决策 | 锚点 |
| ------ | ------ | ------ | ------ |
| First-pass intake | 2026-06-20T10:00 | `NO_HEALTHY_SSOT_BLOCKED` | `maturity-intake.md §1` |
| Repair Plan | 2026-06-20T11:00 → 2026-06-22T15:00 | 修 1 + 修 2 用户批准 | `maturity-intake.md §2` |
| Second-pass intake | 2026-06-22T16:00 | `PROCEED_TO_CHARTER` | `maturity-intake.md §3` |

### 3.2 Repair PR

| PR ID | 状态 | 改动文件 | 批准人 |
| ------- | ------ | --------- | -------- |
| `PR-REPAIR-EX-R-1-001` | Merged 2026-06-22T15:00 | `docs/product-brief.md` + `.github/instructions/data-handling.md` | 用户 + security-team-lead |

### 3.3 新增 INV 沉淀位置

| INV ID | 来源 | 长期承载 |
| -------- | ------ | --------- |
| `INV-BAN-PII-EXPORT-1` | 本 spec Repair PR | `.github/instructions/data-handling.md §6` |
| `INV-LIM-PII-EXPORT-2` | 本 spec Repair PR | `.github/instructions/data-handling.md §6` |

未来扩展 PII 导出类 feature（如"用户行为分析导出"）直接引用 `.github/instructions/data-handling.md §6` 即可，无需重新引用本 archive。

---

## 4. 与 `R-CHK-EX-1.3 archive / merge 边界` 期望对齐

| Sub-rule | 本 archive 状态 |
| ---------- | ---------------- |
| 是否显式声明 Archive Only 或 Merge Back？ | ✅ §1 显式声明 `Archive Only` |
| 是否同时声明 Archive Only 和 Merge Back？ | ✅ 否（不矛盾） |
| 是否给出决策理由？ | ✅ §2 决策矩阵 |
| 是否记录 Repair 历史？ | ✅ §3（Spec Repair 类 archive 必须记录此项作为权利链证据） |

---

## 5. 关键复用模板

本 archive 是未来 Spec Repair 类 archive 的模板：

| 模板段落 | 强制 / 可选 | 用途 |
| --------- | ------------ | ------ |
| Repair 历史 §3.1 三段式 intake | **强制** | reviewer 可一目了然知道 Phase 0 何时阻塞、何时修复、何时通过 |
| Repair PR §3.2 | **强制** | 权利链证据（哪些上游文档被改、谁批准） |
| 新增 INV 沉淀位置 §3.3 | **强制** | 后续 feature 知道去哪儿引用，避免重复造 INV |
| Merge Back 决策矩阵 §2 | **强制** | 与其他 archive 一致，命中 `R-CHK-EX-1.3` |
