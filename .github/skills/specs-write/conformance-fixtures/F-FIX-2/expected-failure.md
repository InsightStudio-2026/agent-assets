# Expected Failure · F-FIX-2

> **F-FIX-2 conformance fixture · 期望失败报告**。本文给出 `/asset-quality-gates` 在 Phase 3.6 spec conformance 检查阶段对本 fixture 的**期望识别结果**。
> 任何"漏识别"或"误识别"均视为 `<aqg>` 检查器自身缺陷，需要修 checker 而非修 fixture。

---

## 1. 期望失败信号

| 字段 | 期望值 |
| ------ | -------- |
| Final state | `CHECKS_FAILED_NEEDS_REVISION` |
| 命中规则 | `R-CHK-EX-1.2 missing traceability chain` |
| 严重性 | High |
| 失败位置 | `spec.md` §2.1 |
| 失败行为 | 阻止 spec 通过；阻止下游 `/specs-execute` 启动 |

---

## 2. 期望报告内容（`reports/asset-quality-gates/<run-id>/spec-conformance.md` 段落示例）

```markdown
## R-CHK-EX-1.2 missing traceability chain · F-FIX-2

- **严重程度 (Severity)**: High
- **文件路径 (Path)**: .github/skills/specs-write/conformance-fixtures/F-FIX-2/spec.md
- **审计发现 (Findings)**:
  - §2.1 REQ-1 缺 `Derived From: SRC-### → REQ-###` 字段
  - §1.1 Sources `SRC-1` 在下游 §2 无任何 REQ 引用，导致 SRC ↔ REQ 锚点链断裂
  - §2.1 BDD Scenario 1 不通过 `SRC-* / REQ-* / AC-*` 锚点回引
- **预期要求 (Expected)**: 每个 REQ-* 必有 `Derived From: SRC-### → REQ-###` 字段（参 EX-M-1 canonical example）；SRC ↔ REQ 锚点闭环
- **处置动作 (Action)**: BLOCK feature spec until traceability chain restored

```

---

## 3. 误识别（不应命中）

`R-CHK-EX-1.2` **不应**误命中以下规则（避免 noise）：

| 规则 | 不应误命中原因 |
| ------ | --------------- |
| `R-CHK-EX-1.1 missing delta operation` | 本 fixture 是 Greenfield，无 EXIST-REQ-*；delta operation 不适用（全 Add 默认） |
| `R-CHK-EX-1.3 archive/merge boundary unclear` | 本 fixture 不复制 archive.md；archive 维度不参与判定 |
| `R-CHK-EX-1.5 architectural invariants violation` | INV-BAN-1 / INV-LIM-1 / INV-SEC-1 在本 fixture 都正常出现，不被违反 |
| `R-CHK-EX-1.7 verification missing` | TASK-1~3 各有 Verification 字段，PASS |

---

## 4. checker 实现提示

`R-CHK-EX-1.2` 检查器应支持：

| 检测点 | 检测方式 |
| -------- | --------- |
| `Derived From` 字段缺失 | 在每个 REQ-*段内匹配 `**Derived From**:` 或同义字段（如 `Source:` `From:`）；缺失即命中 |
| 锚点回链验证 | 解析 `Derived From: SRC-### → REQ-###` 中的 SRC ID，回查 §1.1 Sources 表确认存在；锚点不存在视为更严重失败 |
| 报告精度 | 必须列出每个具体 REQ-* 缺锚点的位置 + 缺的具体字段 |
| 误命中防御 | Brownfield 项目允许 `Derived From: EXIST-REQ-### → REQ-###` 形式（不强制 SRC 锚点）；Greenfield 项目要求 SRC 锚点闭环 |

---

## 5. 与 `../../../asset-quality-gates/references/checks-catalog.md` 集成

本 fixture 启用条件：

- `../../../asset-quality-gates/references/checks-catalog.md §3 R-CHK-EX-*` 占位规则正式启用 → 加入 `R-CHK-EX-1.2` 子规则
- `/asset-quality-gates` Phase 3.6 跑 conformance fixture 套件 → 本 fixture 作为"必须命中"用例
