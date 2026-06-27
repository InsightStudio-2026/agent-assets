# Canonical Examples · /specs-write 标准示例集

> **本文是 `/specs-write` 方法论 canonical examples 的事实源索引**。所有 example 在此登记；新加 / 重构 / 废弃 example 必须同步本文。
> 本文档自身遵循结构化规则表 + ID 体系格式规范（入口骨架 + 支撑文档分离 + 零 ASCII 流程图）。

---

## 0. 定位与索引

### 0.1 文档定位

- 5 类 canonical examples 的索引 + 角色定义；与 `../protocols/methodology-kernel.md` 字面零漂移。
- 不是教程；是**契约测试**：每个 example 都是真实可被 `/asset-quality-gates` + `conformance-fixtures` 引用的最小完整 spec。
- example 不只是教学样本：它们是 `../protocols/methodology-kernel.md` 的可执行验证。

### 0.2 ID 命名空间

- `EX-G-1` Greenfield happy path
- `EX-B-1` Brownfield delta
- `EX-M-1` Medium single-file
- `EX-R-1` Spec repair
- `EX-A-1` Archive / merge

每个 example 在自己目录下用真实 spec 文档结构呈现：`<example-id>/maturity-intake.md` + `<example-id>/charter.md` + `<example-id>/requirements.md` 等（按对应 Mode 裁剪）。

---

## 1. 5 类 canonical examples（角色定义）

| Example ID | 名称 | 角色 | 覆盖语义层 | 状态 |
| ----------- | ------ | ------ | ------------ | ------ |
| `EX-G-1` | Greenfield happy path | 全新项目第一个 spec 走通；展示 Phase 0-5 完整路径，Strategy / Critical Design / Real-World Side Effect 三类 Gate 全过 | proposal / behavior / plan / tasks / verification / archive 全段 | ✅ 已交付 |
| `EX-B-1` | Brownfield delta | 改既有功能；展示 Add / Modify / Replace / Deprecate / Preserve 5 种 delta operation；不重写全量规格 | EXIST-REQ-* + Derivation Map + Existing Coverage | ✅ 已交付 |
| `EX-M-1` | Medium single-file | 单文件 spec（裁剪后但保留最小语义层）；展示文件数 ≠ 方法论 | proposal + behavior + plan + tasks + verification 在同一文件最小段落 | ✅ 已交付 |
| `EX-R-1` | Spec repair | 上游 SSOT 不健康时的 Spec Health Check / Repair 路径；展示 NO_HEALTHY_SSOT → 修上游 → 重派生 | maturity-intake + 阻塞路径 + R-PHASE0-3~5 + R-AUDIT-3/4/5 | ✅ 已交付 |
| `EX-A-1` | Archive / merge | feature 完成后归档 + 回并到长期规格；展示 Archive Only vs Merge Back **复合边界**（REQ-level 决策） | archive + spec merge 语义 + REQ-level archive decision | ✅ 已交付 |

5 类 canonical examples 全部交付完成。`R-CHK-EX-1.1~1.8` **8 个子规则**定义已在 `../../asset-quality-gates/references/checks-catalog.md §3.1` 启用（含 R-CHK-EX-1.8 NFR 完整性）；`/asset-quality-gates` Phase 3.6 已接入 examples + fixtures 套件作为 must-pass / must-hit 用例。后续轮次目标 = 实现自动 checker（在 checker 未落地前，Phase 3.6 以人工对照模式运行）。

**EX-G-1 / EX-B-1 已含 NFR 示范**：EX-G-1 §6 展示 Greenfield 6 类 NFR（含 5 类 High Active + 1 类 Low N/A + 路由表 + DoD）；EX-B-1 §7 展示 Brownfield NFR delta（8 条 NFR + 5 种 Delta Operation 全覆盖）。

---

## 2. Examples ↔ Fixtures 引用关系

| Example | 应通过验证 | 应失败的对应 fixture |
| --------- | ----------- | --------------------- |
| `EX-M-1` Medium single-file | `R-CHK-EX-1.*` 全过 | `F-FIX-2` 缺 traceability（伪 EX-M-1 删 Derived From 字段）；`F-FIX-4` active/done 状态漂移 |
| `EX-B-1` Brownfield delta | `R-CHK-EX-1.*` 全过；§2 × 5 种 REQ delta + §7 × 5 种 NFR delta operation 必含 | `F-FIX-1` REQ 缺 delta operation；`F-FIX-3` archive / merge 边界不清；`F-FIX-8 B` Brownfield NFR 缺 Delta Op |
| `EX-G-1` Greenfield happy path | `R-CHK-EX-1.*` 全过；三类 Gate 全过；§6 NFR 6 类（５ High Active + 1 Low N/A） | `F-FIX-5` INV-BAN-* 违反；`F-FIX-6` Out-of-Charter 越界；`F-FIX-7` Verification 缺失；`F-FIX-8 A` Greenfield NFR 留空 |
| `EX-R-1` Spec repair | `R-CHK-EX-1.2/1.5/1.3` 全过；NO_HEALTHY_SSOT + Repair PR 路径必含 | （暂无专属 fixture；Repair 失败模式过于多样，留 `F-FIX-9` 占位） |
| `EX-A-1` Archive / merge edge case | `R-CHK-EX-1.3` 全过（含 REQ-level 复合决策） | `F-FIX-3` archive / merge 边界不清（spec-level 矛盾对照本 example REQ-level 正确） |

`R-CHK-EX-1.1~1.8` 在 `../../asset-quality-gates/references/checks-catalog.md §3.1` **已启用**（examples + 8 个 fixtures 已交付，启用依赖满足）；`/asset-quality-gates` Phase 3.6 **已接入**。

---

## 3. 每个 example 的最小目录约定

每个 `<example-id>/` 目录至少包含：

| 文件 | Mode 适用 | 最小内容 |
| ------ | ----------- | --------- |
| `README.md` | 全部 | 角色 / 覆盖语义 / 与 fixture 引用 / 已知裁剪 |
| `maturity-intake.md` | 全部 | Project Maturity / Audit Profile / SSOT Health / Decision |
| `charter.md` | 全部 | Sources / Scope / Out-of-Charter / Derivation Constraints / Architectural Invariants |
| `requirements.md` | Medium / Large（Small 可合并） | REQ + AC + BDD + Derived From + Relation to Existing |
| `design.md` | Large（Medium 可跳） | DSN-* / 接口 / 数据契约 / 失败策略 / Reuse vs New |
| `tasks.md` | 全部 | Task Status / Verification / Artifacts / DAG / Revert |
| `archive.md` 或 `verification.md` | 适用阶段 | 交付证据 / Spec Merge 决策（如 archive） |

Mode 裁剪规则：与 `../protocols/methodology-kernel.md` 字面对齐；example 即使 Single-file（如 EX-M-1 / EX-A-1）也必须保留每段最小段落，不允许跳段。多文件结构（如 EX-G-1 / EX-R-1 / EX-B-1）按 spec 实际复杂度选择独立 charter / requirements / tasks / archive 文件。

---

## 4. 修订规则

- 本文修订必须同 PR 修订 `methodology-kernel.md`（如新增 example 类型）+ `../../asset-quality-gates/references/checks-catalog.md §3 R-CHK-EX-*`（如启用 spec conformance 检查）。
- `EX-*` ID 一旦分配不得复用；废弃改 deprecated。
- 新增 example 必须先在 `../protocols/methodology-kernel.md` 同步事实源。
- example 不许内嵌"假数据"反讽真实结构；用真实命名 + 真实 traceability + 真实命令。
