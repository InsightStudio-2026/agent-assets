# EX-A-1 · Archive / merge edge case canonical example

> **角色**：展示 spec close-out 时**复合 archive 决策**：同一个 spec 内部，一部分 REQ 走 `Archive Only`、另一部分 REQ 走 `Merge Back`（部分回并）。
> 与 `../../protocols/methodology-kernel.md` §5 archive/merge 规范字面零漂移。

---

## 1. Example 元数据

| 字段 | 值 |
| ------ | --- |
| Example ID | `EX-A-1` |
| Project Mode | Brownfield |
| Spec Mode | Medium single-file（spec.md 单文件 + archive.md；演示焦点是 archive 复合边界） |
| 引用对应 fixture | `F-FIX-3` archive / merge 边界不清；本 example 是 F-FIX-3 的"复杂正确边"（与 EX-M-1 / EX-B-1 双正确边形成三角对照） |
| 覆盖语义层 | spec 内多个 REQ 不同生命周期（一次性 feature vs 长期能力）+ archive.md 复合决策 + 部分回并到 long-living spec |
| 状态 | ✅ canonical reference |

---

## 2. 模拟场景

**用户原话**：
> 给用户加头像上传功能；同时把现有头像分发改用新的全球 CDN（Cloudflare Images），原来的本地 CDN 慢慢迁移过去。

**判定结果**：

- Project Mode = Brownfield（已有头像分发基础设施 = 现网 EXIST-REQ）
- Spec Mode = Medium single-file（紧凑场景，spec.md 单文件 + archive.md）
- 复合 archive：
  - **REQ-1 头像上传 UI + 后端 endpoint**= 一次性 feature，未来不会扩展（除非加多文件类型，那是新 spec）→ `Archive Only`
  -**REQ-2 CDN 路由 + 缓存策略** = 需要长期演进（多地区 CDN / 缓存命中率 / 边缘节点扩展）→ `Merge Back` 到 long-living `.github/instructions/cdn-strategy.md`

---

## 3. 文件清单

| 文件 | 角色 | 状态 |
| ------ | ------ | ------ |
| `README.md` | 本文 | ✅ |
| `spec.md` | 单文件合并 5 段最小语义层；REQ 标记各自 archive 决策路径 | ✅ |
| `archive.md` | 复合 archive 决策（同 spec 内不同 REQ 不同决策） | ✅ |

---

## 4. 与 `R-CHK-EX-1.*` 期望对齐

| Sub-rule | 期望 |
| ---------- | ------ |
| `R-CHK-EX-1.1` Delta operation | Brownfield 项目，REQ 标记 5 种 delta operation 中的 Add / Replace / Deprecate |
| `R-CHK-EX-1.2` Traceability | `Derived From` 字段在每个 REQ 都填 SRC + EXIST-REQ 链 |
| `R-CHK-EX-1.3` Archive / merge | archive.md **每个 REQ 独立标决策**（REQ-1 = Archive Only / REQ-2 = Merge Back），不矛盾且不缺失 |
| `R-CHK-EX-1.7` Verification | 每个 Done Task 有 `Verification:` 字段 |

`R-CHK-EX-1.3` checker 必须支持"REQ-level archive decision"而非仅"spec-level archive decision"——这是本 example 与 EX-M-1 / EX-B-1 在 archive 复杂度上的关键差异。

---

## 5. 与 `F-FIX-*` 应失败 fixture 引用

| Fixture | 失败模式（基于本 example 的伪化） |
| --------- | -------------------------------- |
| `F-FIX-3` | 同 spec 内不同 REQ 互相矛盾（REQ-1 标 Merge Back 但合入目标缺失 / REQ-2 标 Archive Only 但又给出合入 PR）→ 期望 `R-CHK-EX-1.3` 命中（复杂边界变体） |

`F-FIX-3` 的现有版本演示"spec-level"矛盾；本 example archive.md 的复杂结构同时为 checker 提供"REQ-level 正确"的对照基线。

---

## 6. 复用注意

- 本 example 的"复合 archive 决策"是真实项目最常见但最容易出错的 archive 形态。
- 不要把所有 REQ 都强行划入同一 archive 决策；如果一个 spec 同时含一次性 feature + 长期能力，**必须**走复合决策。
- 如果实际 spec 复杂度过高（> 5 个 REQ 各有不同 archive 决策），考虑拆分为多个 spec，避免单 archive.md 过载。
