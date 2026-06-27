# Archive · Google OAuth 登录（EX-G-1 Greenfield happy path）

> **EX-G-1 canonical example · archive 阶段**。本文展示 Greenfield happy path 完成后的 **Archive Only**决策（与 EX-M-1 同侧，但场景更复杂：涉外部 OAuth client 注册 + 多 provider 扩展未来回并到 long-living spec）。
> 与 `../../protocols/methodology-kernel.md` archive vs merge back 边界字面零漂移。

---

## 1. Archive 元数据

| 字段 | 值 |
| ------ | --- |
| Spec ID | `EX-G-1` Google OAuth 登录 |
| Archive 时间 | 2026-06-12T18:00 |
| Spec 阶段 | Done（TASK-1~7 全 Done + verification PASS + 三类 Gate 全过） |
| Archive 决策 | **Archive Only** |
| Long-living spec 候选 | 建议未来建立 `.github/instructions/auth-providers.md`（OAuth provider 通用 spec，会接 GitHub / Microsoft 等）；本 archive 不直接 Merge Back，只标"建议项" |
| 后续扩展 | 新增 OAuth provider（GitHub / Microsoft）= Brownfield delta spec，按 `EXIST-REQ-G-1.*` 引用本 archive 的 REQ-1~4 + INV-SEC-2~4 + INV-BAN-3 + INV-LIM-3 |

---

## 2. Merge Back 决策矩阵

| 决策维度 | 判定 | 结论 |
| --------- | ------ | ------ |
| 是否存在 long-living spec？ | 否（`auth-providers.md` 仅作为建议项，未建立） | → Archive Only（不强制建 long-living spec） |
| 当前 feature 是否需要长期演进？ | 是（未来会接 GitHub / Microsoft / Apple）但**演进路径**通过新 spec 引用 EXIST-REQ 而非回并本 archive | → Archive Only |
| 是否会出现引用本 REQ 的新 feature？ | 是（GitHub OAuth provider 扩展会引用 `EXIST-REQ-G-1.1~4`） | 引用即可，**不需回并** |
| 是否有 Architectural Invariants 需长期守护？ | 是（INV-SEC-2/3/4 + INV-BAN-3 + INV-LIM-3）但这些 INV 已通过 `.github/instructions/oauth-baseline.md`（建议在 stewardship suggestion 中提）外化 | → Archive Only（INV 守护由 instructions 文档承担） |

**最终决策**：`Status: Archive Only`，原因 = 当前 feature MVP 范围明确（仅 Google），long-living spec 尚未建立；future Brownfield 扩展按 `EXIST-REQ-G-1.*` 引用本 archive 即可，不需要回并。同时建议在 archive 后期建立 `.github/instructions/auth-providers.md` + `.github/instructions/oauth-baseline.md` 承载长期 INV / 通用 schema，但**该建立动作不属于本 spec scope**，作为 stewardship suggestion 转交 charter 阶段。

---

## 3. 与 EX-M-1 / EX-B-1 archive 的对照

| 维度 | EX-M-1 | EX-B-1 | EX-G-1 |
| ------ | -------- | -------- | -------- |
| Project Mode | Greenfield | Brownfield | Greenfield |
| Spec Mode | Medium single-file | Medium 多文件 | Medium 多文件 |
| Archive 决策 | **Archive Only** | **Merge Back** | **Archive Only** |
| 三类 Gate | 仅 Strategy | Strategy + CD + RWSE | Strategy + CD + RWSE 三类全过 |
| Real-World Side Effect | 无（migration 可回滚） | 有（DROP COLUMN Day 30） | 有（OAuth client 注册 + client_secret 生产 secrets） |
| 后续扩展通过 | 直接被 EX-B-1 EXIST-REQ 引用 | Merge Back 到 long-living | 由 future Brownfield delta spec 通过 EXIST-REQ-G-1.* 引用 |
| Long-living spec | 不建立 | 借此首次建立 | 不建立但建议（stewardship） |

EX-G-1 与 EX-M-1 同样是 Archive Only，但 **场景复杂度更高**（三类 Gate 全过 + 外部副作用 + 多 INV 守护）；与 EX-B-1 形成的差异是：本 spec **不**借机建立 long-living，而是把 long-living spec 建立任务作为 stewardship suggestion 转交未来。

---

## 4. 三类 Gate 决策记录

| Gate | charter 阶段决策 | spec close-out 阶段确认 | 后续动作 |
| ------ | ---------------- | ----------------------- | --------- |
| Strategy Gate | `PROCEED`（product brief 已批准） | ✅ 无变化 | N/A |
| Critical Design Gate | `PROCEED_AFTER_REVIEW`（账号合并策略） | ✅ 用户已在 requirements REQ-3 阶段批准"自动合并" | audit log 已落地 |
| Real-World Side Effect Gate | `PROCEED_AFTER_REVIEW`（OAuth client 注册） | ⏳ Deferred 到 release-deploy | release-deploy 时由 `/release-deploy` workflow 二次确认 + 用户批准 client_secret 写入生产 secrets manager |

Real-World Side Effect Gate 的"deferred"意味着：本 spec close-out 时 OAuth client 尚未在 Google Cloud Console 注册；只在 release-deploy 阶段 provider 注册 + secret 写入 + 切换流量；用户在 `/release-deploy` workflow 阶段做最终批准。

---

## 5. 数据保留

| 项 | 保留位置 |
| ---- | --------- |
| spec 文件（charter / requirements / archive） | 同目录（不动） |
| migration | `migrations/2026-05-30-add-google-sub.sql`（已应用，不回滚） |
| 测试 mock IdP | `tests/mocks/google-oauth-server.ts`（保留，作为后续 GitHub OAuth provider 的 mock 参考） |
| audit log 历史 | `audit_log` 表持续保留（含 `oauth_account_merged` 事件） |
| artifacts/ | 全部保留（7 个 task 的 verification 证据 + e2e screenshot） |

---

## 6. 与 `R-CHK-EX-1.3 archive / merge 边界` 期望对齐

| Sub-rule | 本 archive 状态 |
| ---------- | ---------------- |
| 是否显式声明 Archive Only 或 Merge Back？ | ✅ §1 显式声明 `Archive Only` |
| 是否同时声明 Archive Only 和 Merge Back？ | ✅ 否（不矛盾；§2 决策矩阵给出唯一最终决策） |
| 是否给出决策理由（决策矩阵）？ | ✅ §2 4 维度决策矩阵 |
| 是否说明 long-living spec 关系？ | ✅ §1 元数据 + §2 决策矩阵 + §3 对照表 |
| 是否记录三类 Gate 决策（含 deferred）？ | ✅ §4 三类 Gate 决策记录表，含 RWSE deferred 到 release-deploy 的转交说明 |

应通过 `R-CHK-EX-1.3` + `R-CHK-EX-1.5`（INV 守护）+ `R-CHK-EX-1.7`（Verification）三项检查；不应被 `R-CHK-EX-1.1`（delta operation，不适用 Greenfield）误命中。
