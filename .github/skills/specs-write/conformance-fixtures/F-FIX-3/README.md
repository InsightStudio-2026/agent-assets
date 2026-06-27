# F-FIX-3 · archive / merge 边界不清

> **角色**：应失败 fixture #3。模拟 spec archive 阶段**同时声明** `Archive Only` 和 `Merge Back`（互斥矛盾），或两者都不声明（缺失）；期望 `R-CHK-EX-1.3 archive/merge boundary unclear` 命中。
> 来源：基于 `EX-B-1/archive.md` 伪化（同时声明矛盾）；同时给一个"两者都不声明"的二级变体。

---

## 1. Fixture 元数据

| 字段 | 值 |
| ------ | --- |
| Fixture ID | `F-FIX-3` |
| 引用 example | `EX-B-1`（伪化变体，不修改原 example） |
| 失败模式 | archive.md 同时声明 `Archive Only` 和 `Merge Back: yes`（矛盾），或两者都不声明（缺失） |
| 期望识别错误 | `R-CHK-EX-1.3 archive/merge boundary unclear` |
| 严重性 | Critical |
| 状态 | ✅ canonical fixture |

---

## 2. 失败定义

`F-FIX-3` 演示**两种**失败子模式（一个 fixture 内并存）：

| 子模式 | 文件 | 失败方式 |
| -------- | ------ | --------- |
| Mode A：矛盾 | `archive.md` §1 元数据表 | 同时填 `Archive 决策 = Archive Only` 和 `Merge Back 目标 = notifications-spec`（互斥并存） |
| Mode B：缺失 | `archive.md` §2 决策矩阵 | 决策矩阵表存在但**没有给出最终决策行**（既不说 Archive Only 也不说 Merge Back） |

`R-CHK-EX-1.3` 严重性 = Critical（不像 1.1 / 1.2 是 High）：archive 边界一旦混乱，下游 long-living spec 维护、deprecation ledger、PR merge back 路径全部失去事实源；属于"会污染整个项目长期 spec 体系"的级别错误。

---

## 3. 文件清单

| 文件 | 角色 | 与 EX-B-1 差异 |
| ------ | ------ | --------------- |
| `README.md` | 本文 | 新增 |
| `archive.md` | 伪化 EX-B-1/archive.md | §1 同时填 Archive Only + Merge Back（Mode A）；§2 决策矩阵无最终决策行（Mode B） |
| `expected-failure.md` | 期望识别报告 | 新增 |

不复制 charter.md / requirements.md（archive/merge 边界检查只关心 archive.md；上游 spec 文件不在 1.3 子规则范围内）。

---

## 4. 修复建议（fixture 不修复，但说明应如何修）

| 步骤 | 动作 |
| ------ | ------ |
| 1 | §1 元数据表中**二选一**：要么 `Archive 决策 = Archive Only`（删除 Merge Back 相关行），要么 `Archive 决策 = Merge Back`（保留 long-living spec 目标 + Merge Back PR 信息） |
| 2 | §2 决策矩阵尾部加"最终决策"行：明确写 `Status: Archive Only` 或 `Status: Merge Back`，并给决策理由 |
| 3 | 重跑 `/asset-quality-gates` Phase 3.6，期望 `R-CHK-EX-1.3` PASS |

---

## 5. 与 R-CHK-EX-1.3 期望对齐

| 检查点 | 期望 fixture 状态 |
| -------- | ------------------ |
| 是否显式声明 Archive Only **或** Merge Back（恰好一个）？ | ❌ 否（同时声明两个 + 决策矩阵无最终决策） |
| 是否同时声明 Archive Only 和 Merge Back？ | ✅ 是（矛盾） |
| 是否决策矩阵给出最终决策行？ | ❌ 否（缺失） |
| 期望 `R-CHK-EX-1.3` 命中？ | ✅ 命中，severity = Critical |
| 期望 `/asset-quality-gates` 报告？ | `CHECKS_FAILED_NEEDS_REVISION` + 列出 archive.md §1 矛盾 + §2 缺最终决策 |
