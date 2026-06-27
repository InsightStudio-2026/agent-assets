# F-FIX-1 · 缺 delta operation

> **角色**：应失败 fixture #1。模拟 Brownfield spec 在 EXIST-REQ / REQ 表里**漏标 delta operation** 的最常见漂移；期望 `R-CHK-EX-1.1 missing delta operation` 命中。
> 来源：基于 `EX-B-1` 伪化（删除所有 `Delta Operation` 列）。

---

## 1. Fixture 元数据

| 字段 | 值 |
| ------ | --- |
| Fixture ID | `F-FIX-1` |
| 引用 example | `EX-B-1`（伪化变体，不修改原 example） |
| 失败模式 | Brownfield spec 中 EXIST-REQ-*/ REQ-* 没有 `Add / Modify / Replace / Deprecate / Preserve` 任一 delta operation 标记 |
| 期望识别错误 | `R-CHK-EX-1.1 missing delta operation` |
| 严重性 | High |
| 状态 | ✅ canonical fixture |

---

## 2. 失败定义

`F-FIX-1` **真实失败**而非"看起来失败"：

- 真实失败维度 1：requirements.md 的 REQ-1~5 表格中 `Delta Operation` 列**整列被删除**，违反 `../../protocols/methodology-kernel.md` Brownfield 七种 operation 必须显式标注规则。
- 真实失败维度 2：charter.md 的 §2 EXIST-REQ 表格中 `本 feature delta operation` 列**整列被删除**。
- 真实失败维度 3：requirements.md §1 Derivation Map 的 `关系类型` 列也被删除（因为 Add/Modify 等就是关系类型）。

不允许"看起来失败但能 hack 通过"：本 fixture 即使 `R-CHK-EX-1.1` 解析逻辑放宽到模糊匹配，也无法从 charter / requirements 文本中重建 5 种 delta operation 信息。

---

## 3. 文件清单

| 文件 | 角色 | 与 EX-B-1 差异 |
| ------ | ------ | --------------- |
| `README.md` | 本文 | 新增 |
| `requirements.md` | 伪化 EX-B-1/requirements.md | 删除 §1 表 `关系类型` 列 + §2 各 REQ 的 `Delta Operation` 字段 |
| `expected-failure.md` | 期望识别报告 | 新增 |

不复制 charter.md（仅 requirements.md 即可触发失败检查；charter.md 的 EXIST-REQ delta 列删除作为 `expected-failure.md` 描述对象，不实际伪化文件以控制 fixture 体量）。

---

## 4. 修复建议（fixture 不修复，但说明应如何修）

| 步骤 | 动作 |
| ------ | ------ |
| 1 | 在 requirements.md §1 Derivation Map 表恢复 `关系类型` 列，按 `EX-B-1` 原始内容填 Add / Modify / Replace / Deprecate / Preserve |
| 2 | 在 §2 各 REQ 的字段中恢复 `Delta Operation` 字段（每个 REQ 一行） |
| 3 | 在 charter.md §2 EXIST-REQ 表恢复 `本 feature delta operation` 列 |
| 4 | 重跑 `/asset-quality-gates` Phase 3.6，期望 `R-CHK-EX-1.1` PASS |

---

## 5. 与 R-CHK-EX-1.1 期望对齐

| 检查点 | 期望 fixture 状态 |
| -------- | ------------------ |
| 是否每个 EXIST-REQ-*都标了 delta operation？ | ❌ 否（charter.md 表缺列） |
| 是否每个 REQ-* 都标了 delta operation？ | ❌ 否（requirements.md §2 各 REQ 缺字段） |
| 是否 Derivation Map 表显式给出关系类型？ | ❌ 否（requirements.md §1 缺列） |
| 期望 `R-CHK-EX-1.1` 命中？ | ✅ 命中，severity = High |
| 期望 `/asset-quality-gates` 报告？ | `CHECKS_FAILED_NEEDS_REVISION` + 详细列出 5 个 REQ + 5 个 EXIST-REQ 缺 delta 标记 |
