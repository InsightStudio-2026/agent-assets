# F-FIX-8 · 高风险 feature NFR 留空 + Brownfield 缺 Delta Operation

**Fixture ID**: `F-FIX-8`
**Sub-rule**: `R-CHK-EX-1.8`（NFR 完整性）
**严重性**: High
**应失败动作**: `FA-HG-2` + 阻塞 spec close-out

---

## 1. Fixture 定位

模拟两种 NFR 漂移失败叠加：

1. **Greenfield 高风险 feature NFR 留空**：High-Risk Assessment 表标多类 High，但对应 NFR 类整段空白（既不是 Active 也不是显式 N/A），违反 §10.0 规则 + R-CHK-EX-1.8 失败模式 (1)(2)。
2. **Brownfield NFR 缺 Delta Operation 字段**：Brownfield 模式下 NFR 段存在但部分 NFR 缺 `Delta Operation` 字段，违反 R-CHK-EX-1.8 失败模式 (5)。

本 fixture 在 §11~§14 提供两段子 fixture（A: Greenfield 留空；B: Brownfield 缺 delta），让 checker 必须同时识别两类失败。

---

## 2. 应失败的位置

### 子 fixture A：Greenfield NFR 留空（参考 EX-G-1，但 NFR 全空）

文件 `requirements-A.md`（伪化版）：

- §10.0 High-Risk Assessment 表填了：SEC=High / PERF=High / OBS=High / REL=High / UX=High / PLAT=Low
- §10.1~§10.6 **整段空白**（无任何 NFR-* 条目，无 N/A 声明）
- §10.7 路由表为空表头

### 子 fixture B：Brownfield NFR 缺 Delta Operation（参考 EX-B-1，但部分 NFR 缺 delta）

文件 `requirements-B.md`（伪化版）：

- charter Project Mode = Brownfield
- §10.0 High-Risk Assessment 已填
- §10.1 含 2 条 NFR-SEC：NFR-SEC-001 有 `Delta Operation: Modify`；**NFR-SEC-002 缺 `Delta Operation` 字段**
- §10.2 NFR-PERF-001 也**缺 `Delta Operation` 字段**---

## 3. checker 期望识别

`R-CHK-EX-1.8` 必须报告以下 4 类失败：

| 失败类型 | 子 fixture | checker 期望报告 |
| --------- | ----------- | ----------------- |
| High 类无 Active NFR | A | `NFR-SEC / NFR-PERF / NFR-OBS / NFR-REL / NFR-UX 五类标 High 但整段空白` |
| Low 类未显式 N/A | A | `NFR-PLAT 标 Low 但既不是 Active 也无 'N/A: <理由>' 声明` |
| 路由表空 | A | `§10.7 路由表无任何 NFR 条目，与 §10.1~§10.6 不一致` |
| Brownfield NFR 缺 Delta Op | B | `NFR-SEC-002 / NFR-PERF-001 缺 'Delta Operation' 字段（charter 标 Brownfield 必填）` |

漏识别任一类 = checker 缺陷 = `CHECKS_FAILED_NEEDS_REVISION`（修 checker 不修 fixture）。

---

## 4. 修复建议（如真实 spec 命中本类失败）

-**A 类**：参考 `../../examples/EX-G-1/requirements.md §6` 模板，每个 High 类至少 1 条 Active NFR；Low 类显式 `Status: N/A: <理由>`。

- **B 类**：参考 `../../examples/EX-B-1/requirements.md §7` 模板，Brownfield 每条 NFR 必加 `Delta Operation: Add | Modify | Replace | Deprecate | Preserve`。

---

## 5. 与对照 example 关系

| 维度 | F-FIX-8 (本 fixture) | EX-G-1 (正确边 1) | EX-B-1 (正确边 2) |
| ------ | --------------------- | ------------------- | ------------------- |
| Greenfield NFR | A 类全空白 | §6 完整：5 High Active + 1 Low N/A | N/A (Brownfield) |
| Brownfield NFR delta | B 类部分缺 Delta Op | N/A (Greenfield) | §7 完整：5 种 delta 全覆盖 |
| 整段空白识别 | ✓ 必识别 | - | - |
| Delta Op 缺失识别 | ✓ 必识别 | - | - |

---

## 6. 维护规则

- 本 fixture 修订必须同 PR 修订 `../../../asset-quality-gates/references/checks-catalog.md §3.1 R-CHK-EX-1.8` + `../../examples/EX-G-1/requirements.md §6` + `../../examples/EX-B-1/requirements.md §7`。
- 不允许"看似失败但 checker 能 hack 通过"：失败位置必须真实违反 §10 / §1.1 硬规则。
- 新增 NFR 失败模式（如某类专项 workflow 路由错配）→ 新建 `F-FIX-9` 或本 fixture 加子 fixture C，不在 A/B 上扩展。
