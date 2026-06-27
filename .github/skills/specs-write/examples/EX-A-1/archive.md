# Archive · 头像上传 + CDN 切换（EX-A-1 复合 archive 决策）

> **EX-A-1 canonical example · archive 阶段**。本文展示 spec close-out 时的**复合 archive 决策**：同 spec 内 REQ-1 走 `Archive Only`、REQ-2 走 `Merge Back`，互不矛盾。
> 与 `../../protocols/methodology-kernel.md` archive vs merge back 边界字面零漂移；演示 EX-M-1 / EX-B-1 之外的第三种决策形态。

---

## 1. Archive 元数据

| 字段 | 值 |
| ------ | --- |
| Spec ID | `EX-A-1` 头像上传 + CDN 切换 |
| Archive 时间 | 2026-09-25T18:00（spec close-out；TASK-DEPRECATE-1 单独 Day 30 处理） |
| Spec 阶段 | Done |
| Archive 决策 | **复合**：REQ-1 = `Archive Only` / REQ-2 = `Merge Back` |
| Long-living spec 引用 | `.github/instructions/cdn-strategy.md`（接收 REQ-2 合入） |

---

## 2. REQ-level Archive 决策矩阵

| REQ | 决策 | 决策维度 1 long-living spec | 决策维度 2 长期演进 | 决策维度 3 引用预期 | 决策维度 4 INV 守护 |
| ----- | ------ | --------------------------- | -------------------- | -------------------- | --------------------- |
| REQ-1 头像上传 | **Archive Only** | 不需要新建 long-living | 一次性 feature；未来 GIF / 裁剪是新 spec | 未来 feature 不需要回引 REQ-1 详情 | INV-BAN-4 / INV-LIM-4 / INV-SEC-6 已沉淀，无需 REQ-1 长期承载 |
| REQ-2 CDN 路由 + 缓存 | **Merge Back** | `.github/instructions/cdn-strategy.md`（已存在草案占位） | 长期能力（多 region / 缓存调优 / 边缘节点扩展） | 未来 CDN 扩展需引用 REQ-2 lazy migration 模式 | 长期 INV 需跟随（CDN 命中率 SLO / 多 region 一致性等） |

**最终复合决策**：spec close-out 时同步执行：

- REQ-1 + 相关 TASK-1 / TASK-2 / 相关 INV → 标 `Archive Only`，归档不反流
- REQ-2 + 相关 TASK-3 / TASK-4 / TASK-5 / TASK-DEPRECATE-1 → 标 `Merge Back`，合入 `.github/instructions/cdn-strategy.md`

---

## 3. Merge Back 操作（仅针对 REQ-2）

### 3.1 合入目标

| 来源（本 spec） | 合入位置（`cdn-strategy.md`） | Status 变更 |
| -------------- | --------------------------- | ------------- |
| `REQ-2` Cloudflare Images 路由 + 缓存策略 | §2 Active CDN Architecture | Active |
| `AC-2.1~2.4` lazy migration + fallback 模式 | §3 Migration Patterns | Active |
| `TASK-DEPRECATE-1` Day 30 下线（计划） | §5 Deprecation Ledger（pending entry，Day 30 关闭） | Pending → Done（Day 30 由 release-deploy 关闭） |
| INV：CDN API token 走 secrets / fallback 24h 只读 | §1 Architectural Invariants | Active |

### 3.2 合入边界（不合入）

| 项 | 原因 |
| ---- | ------ |
| REQ-1 头像上传 endpoint / UI | 一次性 feature 实现细节，不属于长期 CDN 策略范畴 |
| `users.avatar_url` 列 schema | 数据契约属于 user 模型领域，不在 CDN 策略范畴 |
| Cloudflare Images account_id（具体值） | 配置项，不写入 long-living spec 文档 |

### 3.3 合入 PR

- 合入 PR = `merge-back/cdn-strategy-from-EX-A-1`
- 合入 PR 必须经过 Strategy Gate（首次为 `cdn-strategy.md` 注入实质内容 = 战略级决策，需用户批准）
- 合入完成后，本 archive.md 不修改；`cdn-strategy.md` 顶部 Sources 段引用 `EX-A-1/archive.md` 作为 SRC

---

## 4. Archive Only 操作（仅针对 REQ-1）

| 项 | 保留位置 |
| ---- | --------- |
| spec 文件（spec.md / archive.md / README.md） | 同目录（不动） |
| REQ-1 / TASK-1 / TASK-2 内容 | 仅在本 archive 内被引用，不合入任何 long-living spec |
| 测试用例 | `src/api/__tests__/avatar.test.ts` + e2e 保留 |
| artifacts/ | 全部保留 |

未来如果需要扩展 GIF 头像 / 裁剪 / 头像选择器等：新建 spec → `EXIST-REQ-A-1.1`（即本 archive 的 REQ-1）作为引用锚点 → Brownfield delta 派生。**不需要**修改本 archive。

---

## 5. 与 `R-CHK-EX-1.3 archive / merge 边界` 期望对齐

| Sub-rule | 本 archive 状态 |
| ---------- | ---------------- |
| 是否每个 REQ 独立标 archive 决策？ | ✅ §2 REQ-level 决策矩阵显式标 |
| 是否同时声明 Archive Only **和** Merge Back？ | ✅ 是，**但不矛盾**（REQ-1 = Archive Only / REQ-2 = Merge Back，作用对象不同） |
| 复合声明是否可被 checker 区分？ | ✅ 是（每个决策绑定到具体 REQ ID，而非整 spec） |
| 是否给出每个决策的理由（决策矩阵）？ | ✅ §2 4 维度矩阵 |
| 是否给出合入边界（合入什么 / 不合入什么）？ | ✅ §3.1 + §3.2 |
| 是否给出 Archive Only 部分的数据保留？ | ✅ §4 |

复合声明在 `R-CHK-EX-1.3` checker 实现时是关键测试点：必须区分 "整 spec 级"声明（EX-M-1 / EX-B-1 形态）与 "REQ 级"声明（本 example 形态）；后者**不**应被误识别为"同时声明矛盾"。

---

## 6. 与 EX-M-1 / EX-B-1 / EX-G-1 archive 的对照

| 维度 | EX-M-1 | EX-B-1 | EX-G-1 | EX-A-1 |
| ------ | -------- | -------- | -------- | -------- |
| Archive 决策 | Archive Only（spec 级） | Merge Back（spec 级） | Archive Only（spec 级 + RWSE deferred） | **复合**（REQ-1 Archive Only / REQ-2 Merge Back） |
| Decision 粒度 | spec 级 | spec 级 | spec 级 | **REQ 级** |
| Long-living spec 关系 | 不建立 | 借机首次建立 | 不建立但建议 stewardship | 已存在草案占位，本 spec 注入首个实质内容 |
| Repair 历史 | N/A | N/A | N/A | N/A |
| 适用 fixture | N/A | N/A | F-FIX-7（伪化） | F-FIX-3（复杂边界对照） |

四个 archive examples 形成完整对照矩阵：spec-level Archive Only / spec-level Merge Back / spec-level + RWSE deferred / REQ-level 复合。

---

## 7. checker 实现提示

`R-CHK-EX-1.3` checker 在面对 EX-A-1 类 archive.md 时应：

| 检测点 | 检测方式 |
| -------- | --------- |
| 区分 spec-level vs REQ-level 决策 | 解析 §1 元数据表 `Archive 决策` 字段：值含 `复合` / `mixed` / 直接给出 REQ-level 矩阵时进入 REQ-level 模式 |
| REQ-level 矩阵存在性 | 必须有"REQ-level Archive 决策矩阵"段，每个 REQ 一行，标明决策 + 理由 |
| 互斥性检查（REQ-level） | 同一个 REQ 不允许同时标 Archive Only + Merge Back；不同 REQ 之间互不约束 |
| 合入操作 vs 归档操作分离 | Merge Back 段（§3）只描述 Merge Back REQ；Archive Only 段（§4）只描述 Archive Only REQ；不允许交叉 |
| PASS 条件 | spec-level 决策 OR REQ-level 决策矩阵；每个 REQ 都能找到唯一决策；合入 / 归档操作不交叉 |
