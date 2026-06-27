# Maturity Intake · 用户数据批量导出（EX-R-1 Spec repair）

> **EX-R-1 canonical example · Phase 0 Maturity Intake**。本文展示 SSOT 不健康时的 **三段式 intake**：First-pass（`NO_HEALTHY_SSOT_BLOCKED`）→ Repair Plan → Second-pass（`PROCEED_TO_CHARTER`）。
> 与 `../../protocols/methodology-kernel.md` Phase 0 路径 + `R-PHASE0-3~5` + `R-AUDIT-3~5` 字面零漂移。

---

## 1. First-pass Intake（2026-06-20T10:00）

### 1.1 项目状态识别

| 字段 | 值 |
| ------ | --- |
| Project Maturity | Hybrid（项目第二年；已有 product brief + 部分 .github/standards 但不完整） |
| Audit Profile | Scoped Full-Surface Audit（数据导出涉 PII，必须完整 14 面审计） |
| 用户请求 | "给后台加用户数据批量导出，下载 CSV 含基本资料 + 最近 30 天行为日志" |

### 1.2 SSOT Health Check

| 检查项 | 状态 | 详情 |
| -------- | ------ | ------ |
| product brief 存在 | ✅ | `docs/product-brief.md` line 47 提"批量导出 Q3 目标" |
| product brief 范围明确 | ❌ | 仅写"批量导出"目标，**未定义**导出字段范围（哪些字段可导出？是否含 PII？） |
| `.github/instructions/data-handling.md` 存在 | ✅ | 有现网文档 |
| `.github/instructions/data-handling.md` PII 导出段 | ❌ | **无 PII 导出 Architectural Invariant**（INV 缺失：是否允许导出 email / phone / id_card？谁批准？） |
| 现网代码 PII 处理基线 | ⚠️ | `src/lib/pii-mask.ts` 存在但仅用于日志脱敏，未覆盖导出场景 |

### 1.3 First-pass Decision

| 字段 | 值 |
| ------ | --- |
| SSOT Health | **Needs Repair** |
| Confidence | High（已确认上游缺失项） |
| Decision | **`NO_HEALTHY_SSOT_BLOCKED`** |
| 触发规则 | `R-PHASE0-3 SSOT Health = Needs Repair` |
| Blocking Issues | 1) product brief 未定义导出字段范围；2) `.github/instructions/data-handling.md` 缺 PII 导出 INV |
| 路由动作 | **分流到 `/grill-with-docs`** 修上游 SSOT；触发规则 = `R-PHASE0-4 分流到 /grill-with-docs` |

**关键**：本 spec 在 First-pass intake 阶段**不允许进入 Phase 1 Charter**；必须先修上游。

---

## 2. Repair Plan（2026-06-20T11:00 → 2026-06-22T15:00）

### 2.1 修复目标

| 修复项 | 修复内容 | Owner | 验证方式 |
| -------- | --------- | ------- | --------- |
| 修 1 | 在 `docs/product-brief.md` line 47 后追加 1 段：导出字段范围（基本资料 = name/email/created_at；行为日志 = action_type/timestamp 不含 IP/UA）；明确不导出 password_hash / phone / id_card | product-team | reviewer + 用户批准 |
| 修 2 | 在 `.github/instructions/data-handling.md` 新增 §6 PII Export，引入 INV：`INV-BAN-PII-EXPORT-1` 不允许导出 password_hash 等敏感字段；`INV-LIM-PII-EXPORT-2` 导出操作必须写 audit log + 必须 admin role + 必须批量上限（每次 ≤ 1000 user） | security-team | reviewer + 用户批准 |
| 修 3 | 在 `src/lib/pii-mask.ts` 增 `maskForExport()` 函数（不修，但作为 INV-BAN-PII-EXPORT-1 实现守护点声明） | 后续 spec 处理（不在 Repair scope） | N/A |

修 1 + 修 2 = 必须在本 spec 进入 Phase 1 之前完成；修 3 = 下游实现细节，不阻塞 Phase 0。

### 2.2 Repair PR

| PR ID | 描述 | Status | Approved By |
| ------- | ------ | -------- | ------------- |
| `PR-REPAIR-EX-R-1-001` | docs/product-brief.md + .github/instructions/data-handling.md 修复（修 1 + 修 2） | Merged 2026-06-22T15:00 | 用户 + security-team-lead |

### 2.3 触发规则

- `R-AUDIT-3 上游 SSOT 修复需用户批准` → 命中：用户已批准 PR-REPAIR-EX-R-1-001
- `R-AUDIT-4 INV 新增 = 设计级硬闸` → 命中：新增 INV-BAN-PII-EXPORT-1 / INV-LIM-PII-EXPORT-2 触发 Critical Design Gate（在 charter §5 处理）
- `R-AUDIT-5 修复后必须重新 Phase 0` → 命中：进入 Second-pass intake

---

## 3. Second-pass Intake（2026-06-22T16:00，PR Merge 后 1 小时）

### 3.1 重新 SSOT Health Check

| 检查项 | 状态 | 详情 |
| -------- | ------ | ------ |
| product brief 范围明确 | ✅ | line 47-52 已明确导出字段（修 1 完成） |
| `.github/instructions/data-handling.md` PII 导出段 | ✅ | §6 新增（修 2 完成），含 INV-BAN-PII-EXPORT-1 + INV-LIM-PII-EXPORT-2 |
| 上游修复 PR 链 | ✅ | `PR-REPAIR-EX-R-1-001` Merged + 用户批准 |

### 3.2 Second-pass Decision

| 字段 | 值 |
| ------ | --- |
| SSOT Health | **OK** |
| Confidence | High |
| Decision | **`PROCEED_TO_CHARTER`** |
| 触发规则 | `R-PHASE0-5 Second-pass intake → PROCEED_TO_CHARTER` |
| Blocking Issues | 无 |
| SSOT Stewardship Suggestions | 建议在 spec close-out 后建立 `.github/instructions/pii-export.md` 长期文档（不在本 spec scope） |

### 3.3 转交 charter

charter.md 必须：

- §1 Sources 引用 `PR-REPAIR-EX-R-1-001` 作为 `SRC-3`（保证 Repair 历史可追溯，命中 `R-CHK-EX-1.2`）
- §5 Architectural Invariants 显式列入新增的 `INV-BAN-PII-EXPORT-1` + `INV-LIM-PII-EXPORT-2`（命中 `R-CHK-EX-1.5`）
- §6 Mode 判定中标 Critical Design Gate `PROCEED_AFTER_REVIEW`（INV 新增 = 设计级硬闸；用户批准 PR 时已隐式批准 INV 内容，但 charter 复述时必须再次显式标）

---

## 4. Phase 0 总耗时

| 阶段 | 时长 | 备注 |
| ------ | ------ | ------ |
| First-pass intake | 1 小时 | 检测出 SSOT 不健康 |
| Repair Plan + 上游修复 PR | 2 天 | product-team + security-team 协同 |
| Second-pass intake | 1 小时 | 验证修复 + 重新派生路径 |
| **合计** | **2 天 + 2 小时** | 阻塞期由 Repair 主导，spec 在阻塞期间不前进 |

**重要观察**：Spec Repair 不是"延误"而是"前置投资"；如果在 Phase 0 不阻塞而直接进 Phase 1，charter 会缺 INV-BAN-PII-EXPORT-1 + INV-LIM-PII-EXPORT-2，下游 design / tasks 会在 INV 守护上裸奔，最终 close-out 时被 `R-CHK-EX-1.5` 命中或更糟（生产 PII 泄漏）。

---

## 5. 与 `R-PHASE0-* / R-AUDIT-*` 命中记录

| 规则 ID | 触发位置 | 命中状态 |
| --------- | --------- | --------- |
| `R-PHASE0-3 SSOT Health = Needs Repair` | §1.3 First-pass Decision | ✅ 命中 → BLOCKED_SSOT_REPAIR |
| `R-PHASE0-4 分流到 /grill-with-docs` | §1.3 路由动作 | ✅ 命中 → 路由动作记录 |
| `R-PHASE0-5 Second-pass intake` | §3 Second-pass | ✅ 命中 → PROCEED_TO_CHARTER |
| `R-AUDIT-3 上游 SSOT 修复需用户批准` | §2.3 | ✅ 命中 → 用户已批准 PR |
| `R-AUDIT-4 INV 新增 = 设计级硬闸` | §3.3 转交 charter | ✅ 命中 → Critical Design Gate `PROCEED_AFTER_REVIEW` |
| `R-AUDIT-5 修复后必须重新 Phase 0` | §3 Second-pass 触发 | ✅ 命中 → 三段式 intake 闭环 |
