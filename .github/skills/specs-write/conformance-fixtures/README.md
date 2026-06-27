# Conformance Fixtures · /specs-write 应失败的最小 spec 样例

> **本文是 `/specs-write` 方法论 conformance fixtures 的事实源索引**。所有 fixture 在此登记；新加 / 重构 / 废弃 fixture 必须同步本文。
> 本文档自身遵循结构化规则表 + ID 体系格式规范（入口骨架 + 支撑文档分离 + 零 ASCII 流程图）。

---

## 0. 定位与索引

### 0.1 文档定位

- 应失败的最小 spec 样例索引；与 `../protocols/methodology-kernel.md` conformance-fixtures 定义字面零漂移。
- 与 `../examples/` 互补：examples 表达"应通过"，fixtures 表达"应失败"+ 期望错误类型。
- 用于 `/asset-quality-gates` `R-CHK-EX-1` spec conformance 检查 + 未来 `skill-eval` skill 训练样本。

### 0.2 ID 命名空间

- `F-FIX-1~3`：第一轮交付的最小三类失败 fixture（满足 §4.6 DoD"至少三类失败 fixture"）。
- `F-FIX-4~7`：第二轮交付补全 R-CHK-EX-1.4 ~ 1.7 子规则的代表性 fixture。
- `F-FIX-8`：第三轮交付（§4.6 第 8 项 NFR 扩展）覆盖 R-CHK-EX-1.8 NFR 完整性；含双子 fixture（A: Greenfield NFR 留空；B: Brownfield NFR 缺 Delta Op）。
- `F-FIX-9+`：后续轮次可补占位（Spec Repair 路径异常 / DAG 环依赖等）。
- 每个 fixture 在自己目录下放最小可解析 spec + `expected-failure.md` 期望错误描述。

---

## 1. 应失败 fixture 清单

| Fixture ID | 名称 | 失败模式 | 期望识别错误 | 引用的 example | 状态 |
| ----------- | ------ | --------- | ------------- | --------------- | ------ |
| `F-FIX-1` | 缺 delta operation | Brownfield spec 中 EXIST-REQ-*没有标记 `Add / Modify / Replace / Deprecate / Preserve / Merge Back / Archive Only` 之一 | `R-CHK-EX-1.1 missing delta operation` | 伪 `EX-B-1`（删除 Delta Operation 列） | ✅ 已交付 |
| `F-FIX-2` | 缺 traceability | requirements.md 的 REQ-* 没有 `Derived From: SRC-### + REQ-###` 链 | `R-CHK-EX-1.2 missing traceability chain` | 伪 `EX-M-1`（删除 Derived From 字段） | ✅ 已交付 |
| `F-FIX-3` | Archive / merge 边界不清 | 已 Done 的 feature spec 同时声明 `Archive Only` 和 `Merge Back`，或两者都不声明 | `R-CHK-EX-1.3 archive/merge boundary unclear` | 伪 `EX-B-1`（archive.md 矛盾标记） | ✅ 已交付 |

**第二轮交付 (R-CHK-EX-1.4~1.7)**：

| Fixture ID | 名称 | 失败模式 | 期望识别错误 | 引用的 example | 状态 |
| ----------- | ------ | --------- | ------------- | --------------- | ------ |
| `F-FIX-4` | active / done 状态漂移 | tasks `Status: Done` 与 verification 结果 FAIL 矛盾；或 spec close-out Status `Done` 但 task `Pending` | `R-CHK-EX-1.4 active/done 状态漂移` | 伪 `EX-M-1` | ✅ 已交付 |
| `F-FIX-5` | INV-BAN-* 违反 | design / requirements 引入 charter §5 INV-BAN 显式禁止的列 / 依赖 / 模式 | `R-CHK-EX-1.5 architectural invariants violation` | 伪 `EX-G-1`（加 oauth_access_token 列） | ✅ 已交付 |
| `F-FIX-6` | Out-of-Charter 越界 | tasks `Touches` / `Description` 引入 charter §4 显式 out-of-charter 的功能 | `R-CHK-EX-1.6 out-of-charter scope violation` | 伪 `EX-G-1`（加 GitHub OAuth task） | ✅ 已交付 |
| `F-FIX-7` | Verification 缺失 | Done Task 无 `Verification:` 字段 / `Artifacts:` 空白 / Artifacts 路径不存在 | `R-CHK-EX-1.7 verification missing` | 伪 `EX-G-1`（TASK-3/4/5 三种缺失模式） | ✅ 已交付 |

后续可补的 fixture（未分配 ID）：

| Fixture ID（占位） | 名称 | 失败模式 |
| ------------------ | ------ | --------- |
| `F-FIX-9` | Spec Repair 路径异常 | First-pass intake 跳过 SSOT Health Check 直接进 Phase 1；或 Repair PR 未获用户批准即派生 charter |
| `F-FIX-10` | DAG 环依赖 | tasks.md DAG 中出现 Task A 依赖 B 同时 B 依赖 A |

---

## 2. 每个 fixture 的最小目录约定

每个 `<fixture-id>/` 目录至少包含：

| 文件 | 必填 | 内容 |
| ------ | ------ | ------ |
| `README.md` | 必 | fixture 角色 / 失败模式 / 期望识别错误代码 / 修复建议 |
| `<spec-files>` | 必 | 真实可解析但故意失败的最小 spec 文件子集（按引用 example 的目录约定） |
| `expected-failure.md` | 必 | 期望 `/asset-quality-gates` 报告的失败类型 + 严重性 + 可能的 R-CHK-EX-* 命中 |

---

## 3. 失败识别期望（`R-CHK-EX-1.*` 已启用子检查体系）

`../../asset-quality-gates/references/checks-catalog.md §3.1 R-CHK-EX-1.1~1.8` **已启用**，展开为：

| Sub-rule | 检查 | F-FIX-*命中 | 严重性 |
| ---------- | ------ | -------------- | -------- |
| `R-CHK-EX-1.1` | EXIST-REQ-* 必有 delta operation 标记 | F-FIX-1 | High |
| `R-CHK-EX-1.2` | REQ-* 必有 Derived From 链 | F-FIX-2 | High |
| `R-CHK-EX-1.3` | archive 状态 + merge 决策必显式且不矛盾 | F-FIX-3 | Critical |
| `R-CHK-EX-1.4` | tasks Status 与 verification 结果 / spec close-out Status 一致 | F-FIX-4 | High |
| `R-CHK-EX-1.5` | design / requirements 不违反 charter Architectural Invariants | F-FIX-5 | Critical |
| `R-CHK-EX-1.6` | tasks Touches / Description 不越 charter Scope | F-FIX-6 | Critical |
| `R-CHK-EX-1.7` | Done Task 必有 Verification + Artifacts 且 Artifacts 路径存在 | F-FIX-7 | Critical |
| `R-CHK-EX-1.8` | NFR 完整性：High-Risk 表必填 + High 类必有 Active + Low 类显式 N/A + Active 必有 Verification + Brownfield 必有 Delta Op + 路由表一致 + tasks 引用 | F-FIX-8 | High |

每个 sub-rule 命中后按 `../../asset-quality-gates/references/checks-catalog.md §4` 严重性 → 失败动作映射处理。

---

## 4. 与 `/asset-quality-gates` 集成路径

`/asset-quality-gates` Phase 3.6 已接入本套件作为必跑检查（详 `.github/skills/asset-quality-gates/SKILL.md §2 Phase 3.6`）：

| Phase | 动作 | 启用状态 |
| ------- | ------ | ---------- |
| Phase 3.6 examples PASS | 对 `../examples/EX-G-1/` / `EX-B-1` / `EX-M-1` / `EX-R-1` / `EX-A-1` 跑全 `R-CHK-EX-1.1~1.8`（含 NFR 完整性）：必须全 PASS | ✅ 启用 |
| Phase 3.6 fixtures HIT | 对 `F-FIX-1~8/` 跑对应 sub-rule：必须命中各自 `expected-failure.md` 声明的错误 | ✅ 启用 |
| 任一 example FAIL / 任一 fixture 漏识别 | `CHECKS_FAILED_NEEDS_REVISION` + 报告漂移点（后者是 checker 缺陷，修 checker 不修 fixture） | ✅ 启用 |
| 自动 checker 实现 | 解析 examples / fixtures + 判定 8 子规则 | ⏳ pending（未落地前以人工对照模式运行） |

---

## 5. 修订规则

- 本文修订必须同 PR 修订 `../examples/README.md`（保持 example ↔ fixture 引用一致）+ `../../asset-quality-gates/references/checks-catalog.md §3`（启用对应 R-CHK-EX-1.* sub-rule）。
- `F-FIX-*` ID 一旦分配不得复用；废弃改 deprecated。
- 新增 fixture 必须先在 `../protocols/methodology-kernel.md` 同步事实源。
- fixture 必须**真实失败**：不允许"看起来失败但实际能 hack 通过"的样例；fixture 失败方式与真实项目最常见漂移对齐。
