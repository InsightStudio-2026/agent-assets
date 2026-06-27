# F-FIX-2 · 缺 traceability

> **角色**：应失败 fixture #2。模拟 spec 在 `requirements.md` 中**漏标 `Derived From`** 的最常见漂移；期望 `R-CHK-EX-1.2 missing traceability chain` 命中。
> 来源：基于 `EX-M-1` 伪化（删除 REQ-1 的 `Derived From` 字段；同时删除 `Sources` 表锚点关联）。

---

## 1. Fixture 元数据

| 字段 | 值 |
| ------ | --- |
| Fixture ID | `F-FIX-2` |
| 引用 example | `EX-M-1`（伪化变体，不修改原 example） |
| 失败模式 | `requirements` 段中 REQ-* 没有 `Derived From: SRC-### → REQ-###` 链 |
| 期望识别错误 | `R-CHK-EX-1.2 missing traceability chain` |
| 严重性 | High |
| 状态 | ✅ canonical fixture |

---

## 2. 失败定义

`F-FIX-2` **真实失败**而非"看起来失败"：

- 真实失败维度 1：spec.md §2 Requirements 段 REQ-1 整段**删除** `**Derived From**` 字段。
- 真实失败维度 2：spec.md §1.1 Sources 表保留 `SRC-1` 行，但 §2.1 不引用 `SRC-1`，导致 SRC ↔ REQ 锚点链断裂；checker 无法回溯 REQ-1 的源头。
- 真实失败维度 3：BDD Scenario 1 不通过任何 `SRC-* / REQ-*` 锚点回引；fixture 文档的 traceability 链只能从场景描述推断而无显式 ID 锚点。

不允许"看起来失败但能 hack 通过"：本 fixture 即使 checker 放宽到模糊匹配（推断 SRC 与 REQ 业务相关），也无法重建锚点链。

---

## 3. 文件清单

| 文件 | 角色 | 与 EX-M-1 差异 |
| ------ | ------ | --------------- |
| `README.md` | 本文 | 新增 |
| `spec.md` | 伪化 EX-M-1/spec.md | §2.1 删除 `Derived From` 字段；§2.2 `Existing Coverage` 段删除（避免误干扰） |
| `expected-failure.md` | 期望识别报告 | 新增 |

不复制 archive.md（archive 不在本 fixture 失败范围内；`R-CHK-EX-1.3` 应保持 PASS 不被误干扰）。

---

## 4. 修复建议（fixture 不修复，但说明应如何修）

| 步骤 | 动作 |
| ------ | ------ |
| 1 | 在 spec.md §2.1 REQ-1 段开头恢复 `**Derived From**：SRC-1 → REQ-1` 字段 |
| 2 | 在 §2.1 BDD Scenario 1 开头加注 `**对应 AC**：AC-1.1 / AC-1.2`（可选增强） |
| 3 | 重跑 `/asset-quality-gates` Phase 3.6，期望 `R-CHK-EX-1.2` PASS |

---

## 5. 与 R-CHK-EX-1.2 期望对齐

| 检查点 | 期望 fixture 状态 |
| -------- | ------------------ |
| 是否每个 REQ-* 都有 `Derived From` 字段？ | ❌ 否（§2.1 REQ-1 缺） |
| 是否每个 REQ 的 `Derived From` 锚点能回链到 §1.1 Sources？ | ❌ 否（无字段，无法回链） |
| 是否每个 AC 都映射到 REQ？ | ✅ 是（AC-1.1 / 1.2 / 1.3 在 REQ-1 内） |
| 期望 `R-CHK-EX-1.2` 命中？ | ✅ 命中，severity = High |
| 期望 `/asset-quality-gates` 报告？ | `CHECKS_FAILED_NEEDS_REVISION` + 列出 REQ-1 缺 traceability 锚点 |
