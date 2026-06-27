# F-FIX-4 · active / done 状态漂移

> **角色**：应失败 fixture #4。模拟 `tasks` 段 Status 与 `archive` 段状态**矛盾**的常见漂移；期望 `R-CHK-EX-1.4 active/done 状态漂移` 命中。
> 来源：基于 `EX-M-1` 伪化（tasks 表 TASK-3 标 Done，但 archive.md Verification 结果中 e2e 行标 FAIL，且 archive 仍写 spec Done）。

---

## 1. Fixture 元数据

| 字段 | 值 |
| ------ | --- |
| Fixture ID | `F-FIX-4` |
| 引用 example | `EX-M-1`（伪化变体） |
| 失败模式 | tasks 表 TASK-* `Status = Done` 但 archive.md `Verification 结果` 表对应行标 FAIL；或 archive.md 标 spec Done 但仍有 Pending Task |
| 期望识别错误 | `R-CHK-EX-1.4 active/done 状态漂移` |
| 严重性 | High |
| 状态 | ✅ canonical fixture |

---

## 2. 失败定义

`F-FIX-4` 演示两种状态漂移子模式：

| 子模式 | 位置 | 失败方式 |
| -------- | ------ | --------- |
| Mode A：Done vs FAIL | `spec.md` §4 Tasks 表 | TASK-3 `Status: Done`；但 §5.3 Verification 结果表 e2e 行标 `FAIL`（互斥矛盾） |
| Mode B：Done vs Pending | `spec.md` §6 Status | spec 阶段标 `Done`；但 §4 Tasks 表 TASK-3 `Status: Pending`（互斥矛盾） |

`R-CHK-EX-1.4` checker 必须在两个子模式之间任一命中即报错。

---

## 3. 文件清单

| 文件 | 角色 | 与 EX-M-1 差异 |
| ------ | ------ | --------------- |
| `README.md` | 本文 | 新增 |
| `spec.md` | 伪化 EX-M-1/spec.md | §4 TASK-3 Status / §5.3 e2e 结果 / §6 Status 三者构成两组矛盾 |
| `expected-failure.md` | 期望识别报告 | 新增 |

---

## 4. 修复建议

| 步骤 | 动作 |
| ------ | ------ |
| 1 | Mode A 修：要么 §5.3 e2e 改 PASS（如 task 真的 Done），要么 §4 TASK-3 改 `Status: Blocked` 或 `Pending` |
| 2 | Mode B 修：要么 §4 TASK-3 改 `Status: Done`（实际完成），要么 §6 Status 改 `In Progress`（实际未完成） |
| 3 | 重跑 `/asset-quality-gates` Phase 3.6，期望 `R-CHK-EX-1.4` PASS |

---

## 5. 与 R-CHK-EX-1.4 期望对齐

| 检查点 | 期望 fixture 状态 |
| -------- | ------------------ |
| Tasks Status 与 Verification 结果是否一致？ | ❌ Mode A：Done 但 e2e FAIL（矛盾） |
| Tasks Status 与 spec close-out Status 是否一致？ | ❌ Mode B：spec Done 但 TASK Pending（矛盾） |
| 期望 `R-CHK-EX-1.4` 命中？ | ✅ 命中，severity = High |
