# EX-M-1 · Medium single-file canonical example

> **角色**：展示 Medium Mode 下 spec 可压到单文件，但**仍保留**proposal / behavior / plan / tasks / verification 五段最小语义层。文件数 ≠ 方法论。
> 与 `../../protocols/methodology-kernel.md` §3 复杂度分级规范字面零漂移。

---

## 1. Example 元数据

| 字段 | 值 |
| ------ | --- |
| Example ID | `EX-M-1` |
| Project Mode | Greenfield |
| Spec Mode | Medium |
| 承载文件 | `spec.md`（单文件合并 maturity-intake / charter / requirements / tasks / verification）+ `archive.md`（feature 完成后追加） |
| 引用对应 fixture | `F-FIX-2` 缺 traceability（删 `Derived From` 字段） |
| 覆盖语义层 | proposal / behavior / plan / tasks / verification 全段最小段落 |
| 状态 | ✅ canonical reference |

---

## 2. 模拟场景**用户原话**
>
> 给我们的 SaaS 应用加一个"我的设置 → 通知偏好"页面，让用户能选择要不要收营销邮件。MVP 范围内，不接第三方邮件 SDK，先存数据库就行。

**判定结果**：

- Project Mode = Greenfield（项目早期）
- Spec Mode = Medium（功能边界清楚 / 影响一两个表 + UI / 不需独立 design.md）
- 文件数 = 单 `spec.md` + 后续 `archive.md`

---

## 3. 文件清单

| 文件 | 角色 | 状态 |
| ------ | ------ | ------ |
| `README.md` | 本文 | ✅ |
| `spec.md` | 单文件合并 5 段最小语义层 | ✅ |
| `archive.md` | feature 完成后追加（occured at 2026-05-24） | ✅ |

---

## 4. 与 `R-CHK-EX-1.*` 期望对齐

| Sub-rule | 期望 |
| ---------- | ------ |
| `R-CHK-EX-1.1` Delta operation | N/A（Greenfield 全 `Add`，但仍需在 archive.md 显式标） |
| `R-CHK-EX-1.2` Traceability | `Derived From` 字段在每个 REQ 都填 SRC + AC 链 |
| `R-CHK-EX-1.3` Archive / merge | archive.md 显式标 `Status: Archive Only`（无回并 long-living spec 需求） |
| `R-CHK-EX-1.7` Verification | 每个 Done Task 有 `Verification:` 字段 + `artifacts/` 列表 |

---

## 5. 复用注意

- 本 example 的"通知偏好"是真实业务场景（SaaS 常见），不是 hello-world。
- traceability 链可直接在新项目中按 SRC-1 / REQ-1 / AC-1 模板套用。
- 如复用为 Brownfield，必须改造为 `EX-B-1` 模板（含 EXIST-REQ-* + Derivation Map）。
