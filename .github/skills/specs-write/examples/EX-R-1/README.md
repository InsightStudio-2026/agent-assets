# EX-R-1 · Spec repair canonical example

> **角色**：展示上游 SSOT（product brief / 母本 charter / .github/standards）**不健康**时的 spec repair 路径：Phase 0 Maturity Intake 检测出 `NO_HEALTHY_SSOT` → 触发 `R-PHASE0-3~5` 路径分流到 `/grill-with-docs` → 上游修复后回到本 spec 重新 Phase 1 派生。
> 与 `../../protocols/methodology-kernel.md` §3 maturity intake 规范字面零漂移。

---

## 1. Example 元数据

| 字段 | 值 |
| ------ | --- |
| Example ID | `EX-R-1` |
| Project Mode | Hybrid（项目早期已有 product brief + 部分 .github/standards，但 charter / brief 中关于 PII 的 INV 缺失） |
| Spec Mode | Medium（多文件；maturity-intake.md 单独承载 Repair 历史） |
| 引用对应 fixture | 暂无对应 fixture（Spec Repair 失败模式过于多样，难标准化为单一 fixture；后续可补 `F-FIX-8` 占位） |
| 覆盖语义层 | maturity-intake / NO_HEALTHY_SSOT 检测 / R-PHASE0-3~5 / R-AUDIT-3~5 / Repair Plan / Second-pass Intake |
| 状态 | ✅ canonical reference |

---

## 2. 模拟场景

**用户原话**：
> 给后台加一个"用户数据批量导出"功能，运营让用户填一个 user_id 列表然后下载 CSV，包含基本资料和最近 30 天行为日志。

**Phase 0 检测出的 SSOT Health 问题**：

- product brief（`docs/product-brief.md`）只提"批量导出"目标，未定义 **导出范围**（哪些字段可导出？PII 是否包含？）
- 现有 `.github/instructions/data-handling.md` 缺 PII 导出 Architectural Invariant（`INV-BAN-PII-EXPORT`）
- `charter` 阶段直接派生会让 spec 在 INV 守护上裸奔；属于 `R-PHASE0-3 SSOT Health = Needs Repair` 必须先修上游

**判定结果**：

- Phase 0 Decision = `NO_HEALTHY_SSOT_BLOCKED`
- 分流路径 = `/grill-with-docs`（修 product brief + 补 `.github/instructions/data-handling.md` PII 段）
- 上游 PR Approved 后 → 重新 Phase 0 Second-pass → `PROCEED_TO_CHARTER`

---

## 3. 文件清单

| 文件 | 角色 | 状态 |
| ------ | ------ | ------ |
| `README.md` | 本文 | ✅ |
| `maturity-intake.md` | Phase 0：First-pass intake (`NO_HEALTHY_SSOT_BLOCKED`) + Repair Plan + Second-pass intake (`PROCEED_TO_CHARTER`) | ✅ |
| `charter.md` | Phase 1 修复后派生的 charter（引用上游修复 PR + 新建 INV-BAN-PII-EXPORT） | ✅ |
| `archive.md` | Phase 6 Archive（小段落，含 Repair 历史 + Archive Only 决策） | ✅ |

不附 `requirements.md` / `tasks.md`（Spec Repair 的演示焦点是 **Phase 0 → Repair → 重新 Phase 0/1**，不在 happy path 主流程；Phase 2-5 走通后行为与 `EX-G-1` 类似，不重复演示）。

---

## 4. 与 `R-PHASE0-* / R-AUDIT-*` 期望对齐

| 规则 ID | 触发位置 | 期望状态 |
| --------- | --------- | --------- |
| `R-PHASE0-3 SSOT Health = Needs Repair` | First-pass maturity-intake §2 检测 | 命中 → BLOCKED_SSOT_REPAIR |
| `R-PHASE0-4 分流到 /grill-with-docs` | First-pass maturity-intake §3 Repair Plan | 命中 → 路由动作记录 |
| `R-PHASE0-5 Second-pass intake` | Second-pass maturity-intake §5 | 命中 → `PROCEED_TO_CHARTER` |
| `R-AUDIT-3 上游 SSOT 修复需用户批准` | Repair Plan §4 用户批准记录 | 命中 → 用户已批准修复 PR |
| `R-AUDIT-4 INV 新增 = 设计级硬闸` | charter §5 新增 INV-BAN-PII-EXPORT | 命中 → Critical Design Gate `PROCEED_AFTER_REVIEW` |

---

## 5. 与 `R-CHK-EX-1.*` 期望对齐

| Sub-rule | 期望 |
| ---------- | ------ |
| `R-CHK-EX-1.2` Traceability | charter §1 Sources 引用上游修复 PR（`SRC-3 = 修复 PR / commit hash`），保证 Repair 历史可追溯 |
| `R-CHK-EX-1.5` Architectural Invariants | charter §5 新增 `INV-BAN-PII-EXPORT`（来自上游修复 PR），下游 design 不得违反 |
| `R-CHK-EX-1.3` Archive / merge | archive.md 显式标 `Archive Only`（spec close-out 时上游已修，本 spec 不需 Merge Back） |

---

## 6. 复用注意

- 本 example 的 **Spec Repair 决策路径**（Phase 0 阻塞 → 修上游 → 重新 Phase 0/1）可作为新项目首次遇到 SSOT 不健康时的标准模板。
- 修上游路径必须显式记录：First-pass 阻塞 → Repair Plan → 用户批准 → 上游 PR → Second-pass intake，缺一不可。
- Spec Repair 不允许"先派生再补 INV"的逆序；必须先修上游再派生（`R-AUDIT-3` 严格要求）。
