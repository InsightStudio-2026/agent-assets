# Expected Failure · F-FIX-3

> **F-FIX-3 conformance fixture · 期望失败报告**。本文给出 `/asset-quality-gates` 在 Phase 3.6 spec conformance 检查阶段对本 fixture 的**期望识别结果**。
> 任何"漏识别"或"误识别"均视为 `<aqg>` 检查器自身缺陷，需要修 checker 而非修 fixture。

---

## 1. 期望失败信号

| 字段 | 期望值 |
| ------ | -------- |
| Final state | `CHECKS_FAILED_NEEDS_REVISION` |
| 命中规则 | `R-CHK-EX-1.3 archive/merge boundary unclear` |
| 严重性 | **Critical**（archive 边界一旦混乱，下游 long-living spec / deprecation ledger / merge back PR 全部失去事实源） |
| 失败位置 | `archive.md` §1 + §2 |
| 失败行为 | 阻止 spec close-out；阻止 long-living spec merge back PR；阻止下游 feature 引用本 archive 作为 EXIST-REQ 来源 |

---

## 2. 期望报告内容（`reports/asset-quality-gates/<run-id>/spec-conformance.md` 段落示例）

```markdown
## R-CHK-EX-1.3 archive/merge boundary unclear · F-FIX-3

- **严重程度 (Severity)**: Critical
- **文件路径 (Path)**: .github/skills/specs-write/conformance-fixtures/F-FIX-3/archive.md
- **审计发现 (Findings)**:
  - **Mode A (contradiction)**: §1 元数据表同时声明 `Archive 决策 = Archive Only` 与 `Merge Back 目标 = notifications-spec` / `Merge Back PR = ...`（互斥并存）
  - **Mode A 续**: §3 `Merge Back 操作 / 合入目标` 段存在 → 与 §1 Archive Only 决策矛盾
  - **Mode B (missing)**: §2 决策矩阵列出 4 个维度但缺最终决策行（既不说 `Archive Only` 也不说 `Merge Back`）
- **预期要求 (Expected)**: §1 二选一 + §2 末尾必有 `**最终决策**: Status: Archive Only` 或 `**最终决策**: Status: Merge Back, 目标 = ...`（参 EX-M-1/archive.md §2 与 EX-B-1/archive.md §2 两个 canonical 决策样式）
- **处置动作 (Action)**: BLOCK spec close-out + BLOCK merge back PR + BLOCK downstream EXIST-REQ 引用

```

---

## 3. 误识别（不应命中）

`R-CHK-EX-1.3` **不应**误命中以下规则（避免 noise）：

| 规则 | 不应误命中原因 |
| ------ | --------------- |
| `R-CHK-EX-1.1 missing delta operation` | 本 fixture 不复制 charter.md / requirements.md，不在 delta operation 维度判定 |
| `R-CHK-EX-1.2 missing traceability chain` | 本 fixture 不复制 spec.md / requirements.md，不在 traceability 维度判定 |
| `R-CHK-EX-1.7 verification missing` | 本 fixture 不涉 tasks.md，不在 verification 维度判定 |

---

## 4. checker 实现提示

`R-CHK-EX-1.3` 检查器应支持：

| 检测点 | 检测方式 |
| -------- | --------- |
| Mode A 矛盾 | 解析 archive.md §1 元数据表，提取 `Archive 决策` 字段值 + 检查 `Merge Back 目标` / `Merge Back PR` 段是否存在；任一同时存在 `Archive Only` 字段值与 Merge Back 段，命中 |
| Mode B 缺失 | 解析 archive.md 全文，匹配 `**最终决策**` / `Status: Archive Only` / `Status: Merge Back` 任一字面；都不存在则命中 |
| 严重性升级 | Critical（不像其他 R-CHK-EX-1.* High），因为 archive 决策是下游 long-living spec / deprecation / merge back PR 的事实源，污染半径大 |
| 误命中防御 | 如果 archive.md 仅给出 Archive Only 且无任何 Merge Back 段（如 EX-M-1）→ PASS；如果 archive.md 仅给出 Merge Back 且 §1 不矛盾且 §2 有最终决策行（如 EX-B-1）→ PASS |

---

## 5. 与 `../../../asset-quality-gates/references/checks-catalog.md` 集成

本 fixture 启用条件：

- `../../../asset-quality-gates/references/checks-catalog.md §3 R-CHK-EX-*` 占位规则正式启用 → 加入 `R-CHK-EX-1.3` 子规则（severity 默认 Critical）
- `/asset-quality-gates` Phase 3.6 跑 conformance fixture 套件 → 本 fixture 作为"必须命中"用例
- 启用前可由 reviewer 人工对照 EX-M-1 / EX-B-1 与 F-FIX-3 archive.md 三方差异，作为 checker 实现的回归测试基线

---

## 6. 与 EX-M-1 / EX-B-1 archive 的对照（checker 校准用）

| 维度 | EX-M-1/archive.md | EX-B-1/archive.md | F-FIX-3/archive.md |
| ------ | ------------------ | ------------------ | -------------------- |
| §1 Archive 决策字段 | `Archive Only` | `Merge Back` | `Archive Only`（但同时有 Merge Back 目标，矛盾） |
| Merge Back 目标段 | 无 | 有 + 与 §1 一致 | **有 + 与 §1 矛盾** |
| §2 最终决策行 | `Status: Archive Only` 显式 | `Status: Merge Back` 显式 | **缺失** |
| `R-CHK-EX-1.3` 期望结果 | PASS | PASS | **FAIL Critical** |

EX-M-1 / EX-B-1 是双正确边（Archive Only 一种正解 + Merge Back 一种正解）；F-FIX-3 是错误边的代表。三者一起为 checker 提供完整对照样本。
