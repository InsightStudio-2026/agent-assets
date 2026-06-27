# Expected Failure · F-FIX-1

> **F-FIX-1 conformance fixture · 期望失败报告**。本文给出 `/asset-quality-gates` 在 Phase 3.6 spec conformance 检查阶段对本 fixture 的**期望识别结果**。
> 任何"漏识别"或"误识别"均视为 `<aqg>` 检查器自身缺陷，需要修 checker 而非修 fixture。

---

## 1. 期望失败信号

| 字段 | 期望值 |
| ------ | -------- |
| Final state | `CHECKS_FAILED_NEEDS_REVISION` |
| 命中规则 | `R-CHK-EX-1.1 missing delta operation` |
| 严重性 | High |
| 失败位置 | `requirements.md` §1 + §2.1~2.5 |
| 失败行为 | `/asset-quality-gates` 不允许该 spec 通过；阻止下游 `/specs-execute` 启动 |

---

## 2. 期望报告内容（`reports/asset-quality-gates/<run-id>/spec-conformance.md` 段落示例）

```markdown
## R-CHK-EX-1.1 missing delta operation · F-FIX-1

- **严重程度 (Severity)**: High
- **文件路径 (Path)**: .github/skills/specs-write/conformance-fixtures/F-FIX-1/requirements.md
- **审计发现 (Findings)**:
  - §1 Derivation Map 表缺 `关系类型` 列；无法定位 REQ-1~5 的 delta operation
  - §2.1 REQ-1 缺 `Delta Operation` 字段
  - §2.2 REQ-2 缺 `Delta Operation` 字段
  - §2.3 REQ-3 缺 `Delta Operation` 字段
  - §2.4 REQ-4 缺 `Delta Operation` 字段
  - §2.5 REQ-5 缺 `Delta Operation` 字段
- **预期要求 (Expected)**: 每个 REQ 必有 Add / Modify / Replace / Deprecate / Preserve 任一标记（参 EX-B-1 canonical example）
- **处置动作 (Action)**: BLOCK feature spec until delta operations explicitly declared

```

---

## 3. 误识别（不应命中）

`R-CHK-EX-1.1` **不应**误命中以下规则（避免 noise）：

| 规则 | 不应误命中原因 |
| ------ | --------------- |
| `R-CHK-EX-1.2 missing traceability chain` | 本 fixture 保留 `Derived From` 字段；traceability 链完整 |
| `R-CHK-EX-1.3 archive/merge boundary unclear` | 本 fixture 不涉 archive.md 文件，不在 archive/merge 维度判定 |
| `R-CHK-EX-1.7 verification missing` | 本 fixture 仅伪化 requirements.md；tasks.md 未变化或不在伪化范围（fixture 不复制 tasks.md，但这不应被 1.7 误命中） |

---

## 4. checker 实现提示

`R-CHK-EX-1.1` 检查器应支持：

| 检测点 | 检测方式 |
| -------- | --------- |
| Brownfield 项目识别 | 通过 charter.md `Project Maturity = Brownfield` 字段（fixture 中假设上层 charter 仍标 Brownfield；如不存 charter，从 requirements.md 出现 `EXIST-REQ-*` 锚点判定） |
| Delta operation 列 / 字段缺失 | 表格列名匹配 + 字段名 `Delta Operation` 子串 + 关系类型枚举值（Add/Modify/Replace/Deprecate/Preserve）匹配 |
| 报告精度 | 必须列出每个具体 REQ-*缺标记的位置（行号 / 段落引用） |
| 误命中防御 | Greenfield 项目（无 EXIST-REQ-*）不触发本规则；Greenfield 全 Add 可隐式默认 |

---

## 5. 与 `../../../asset-quality-gates/references/checks-catalog.md` 集成

本 fixture 启用条件：

- `../../../asset-quality-gates/references/checks-catalog.md §3 R-CHK-EX-*` 占位规则正式启用 → 加入 `R-CHK-EX-1.1` 子规则
- `/asset-quality-gates` Phase 3.6 跑 conformance fixture 套件 → 本 fixture 作为"必须命中"用例
- 启用前可通过 `../../../asset-quality-gates/references/checks-catalog.md` 在 placeholder 状态下登记本 fixture 路径，等 checker 实现后自动接入
