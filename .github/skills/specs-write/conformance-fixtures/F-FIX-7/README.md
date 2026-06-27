# F-FIX-7 · Verification 缺失

> **角色**：应失败 fixture #7。模拟 Done Task 没有 `Verification:` 字段或 `Artifacts:` 缺对应文件；期望 `R-CHK-EX-1.7 verification missing` 命中。
> 来源：基于 `EX-G-1` 伪化（删除 TASK-3 / TASK-5 的 Verification 字段；TASK-4 的 Artifacts 路径不存在）。

---

## 1. Fixture 元数据

| 字段 | 值 |
| ------ | --- |
| Fixture ID | `F-FIX-7` |
| 引用 example | `EX-G-1`（伪化变体） |
| 失败模式 | Done Task 缺 `Verification:` 字段 / `Artifacts:` 字段 / 引用文件不存在 |
| 期望识别错误 | `R-CHK-EX-1.7 verification missing` |
| 严重性 | **Critical** |
| 状态 | ✅ canonical fixture |

---

## 2. 失败定义

| 子模式 | 位置 | 失败方式 |
| -------- | ------ | --------- |
| Mode A：缺 Verification 字段 | `tasks.md` TASK-3 | `Verification:` 列空白或字段被删除 |
| Mode B：缺 Artifacts 字段 | `tasks.md` TASK-5 | `Artifacts:` 列空白 |
| Mode C：Artifacts 路径不存在 | `tasks.md` TASK-4 | Artifacts 引用 `artifacts/oauth-callback-test.log` 但 fixture 目录无此文件 |

`R-CHK-EX-1.7` severity = Critical：Verification 是 Done Task 的硬证据；缺失 = 无法验证项目是否真实交付，等于伪 Done。

---

## 3. 文件清单

| 文件 | 角色 | 与 EX-G-1 差异 |
| ------ | ------ | --------------- |
| `README.md` | 本文 | 新增 |
| `tasks.md` | 伪化 EX-G-1 tasks 段 | TASK-3/4/5 三种缺失模式 |
| `expected-failure.md` | 期望识别报告 | 新增 |

---

## 4. 修复建议

| 步骤 | 动作 |
| ------ | ------ |
| 1 | Mode A 修：TASK-3 Verification 列填入实际命令（如 `pnpm test src/...`） |
| 2 | Mode B 修：TASK-5 Artifacts 列填入实际产物路径（如 `artifacts/test.log`） |
| 3 | Mode C 修：在 fixture 目录创建对应 artifacts 文件 OR 修改 Artifacts 路径指向真实文件 |
| 4 | 重跑 `/asset-quality-gates` Phase 3.6，期望 `R-CHK-EX-1.7` PASS |

---

## 5. 与 R-CHK-EX-1.7 期望对齐

| 检查点 | 期望 fixture 状态 |
| -------- | ------------------ |
| 每个 Done Task 有 Verification 字段？ | ❌ TASK-3 缺 |
| 每个 Done Task 有 Artifacts 字段？ | ❌ TASK-5 缺 |
| Artifacts 引用的文件实际存在？ | ❌ TASK-4 引用不存在文件 |
| 期望 `R-CHK-EX-1.7` 命中？ | ✅ 命中三个子模式，severity = Critical |
