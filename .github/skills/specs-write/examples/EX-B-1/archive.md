# Archive · 多类通知偏好（EX-B-1 Brownfield delta）

> **EX-B-1 canonical example · archive 阶段**。本文展示 Brownfield feature 完成后的 **Merge Back**决策路径（与 `EX-M-1` 的 Archive Only 形成对照）。
> 与 `../../protocols/methodology-kernel.md` archive vs merge back 边界字面零漂移。

---

## 1. Archive 元数据

| 字段 | 值 |
| ------ | --- |
| Spec ID | `EX-B-1` 多类通知偏好 |
| Archive 时间 | 2026-08-30T18:00（feature Done 时；`TASK-DEPRECATE-1` 单独 Day 30 执行） |
| Spec 阶段 | Done（TASK-1~7 全 Done + verification PASS；TASK-DEPRECATE-1 = Pending Day 30） |
| Archive 决策 | **Merge Back**（不是 Archive Only） |
| Long-living spec 候选 | 新建 `docs/specs/notifications-spec.md`（long-living；本 feature 是其首次实质 contribution） |
| 后续扩展 | 未来邮件 / 短信 / 推送扩展均回并到 `notifications-spec` |

---

## 2. Merge Back 决策矩阵

| 决策维度 | 判定 | 结论 |
| --------- | ------ | ------ |
| 是否存在 long-living spec？ | 否（首次建立；`EX-M-1` 是 Archive Only，未建 long-living） | 本次借机建立 → **Merge Back**起步 |
| 当前 feature 是否需要长期演进？ | 是（多类邮件 → 未来短信 / 推送 / Lark / WeChat 渠道扩展） | → Merge Back |
| 是否会出现引用本 REQ 的新 feature？ | 是（短信通道 / 推送通道扩展将引用 REQ-1 多类语义） | → Merge Back |
| 是否有 Architectural Invariants 需长期守护？ | 是（INV-BAN-2 不存 PII / INV-LIM-2 dry-run 模式 / INV-SEC-1 audit log） | → Merge Back（不变量必须长期跟随） |

**最终决策**：`Status: Merge Back`，目标 = 新建 `docs/specs/notifications-spec.md` 作为 long-living spec；本 archive 的 REQ-1~5 + DSN-1~3 + INV-BAN-2 / INV-LIM-2 一次性合入。

---

## 3. Merge Back 操作

### 3.1 合入目标

| 来源（本 spec） | 合入位置（`notifications-spec.md`） | Status 变更 |
| -------------- | ----------------------------------- | ------------- |
| `REQ-1` 多类邮件订阅 | §2 Requirements REQ-NOTIF-1 | Active in long-living spec |
| `REQ-2` 多类 endpoint schema | §3 DSN-NOTIF-1（合并为接口契约段落） | Active |
| `REQ-3` Mailgun 批发 | §3 DSN-NOTIF-2（外部依赖段落） | Active |
| `REQ-4` 废弃 `email_unsubscribe_token` | §5 Deprecation Ledger（合入"已废弃事项"段，记录 DROP 完成日 = Day 30） | Pending → Done（Day 30 后由 `TASK-DEPRECATE-1` 关闭并写入） |
| `REQ-5` audit log Preserve | §1 Architectural Invariants INV-SEC-NOTIF-1 | Active（继承 INV-SEC-1） |
| `INV-BAN-2` 不存 PII | §1 Architectural Invariants | Active |
| `INV-LIM-2` Mailgun dry-run | §1 Architectural Invariants | Active |

### 3.2 合入边界（不合入）

| 项 | 原因 |
| ---- | ------ |
| `EX-M-1` REQ-1（单开关旧语义） | 已被 `REQ-1` Modify 覆盖；`marketing_emails_enabled` 列保留为只读 fallback，不作为新 spec 的 Requirement |
| `EXIST-REQ-3` SMTP 直连 | 已被 `REQ-3` Replace 删除；不合入新 spec（已不存在） |
| `EXIST-REQ-4` `email_unsubscribe_token` | 仅以"Deprecation Ledger"形式归档，不作为 long-living Requirement |
| 现网 `<NotificationPrefsSection>` UI 实现细节 | 实现属于代码层，long-living spec 不承载组件实现 |

### 3.3 合入 PR

- 合入 PR = `merge-back/notifications-spec-from-EX-B-1`
- 合入 PR 必须经过 Strategy Gate（建立 long-living spec = 战略级决策，需用户批准）
- 合入完成后，本 archive.md 不修改（archive 不可反流），但在 `notifications-spec.md` 顶部 `Sources` 段引用 `EX-B-1/archive.md` + `EX-M-1/archive.md` 作为来源 SRC

---

## 4. 数据保留

| 项 | 保留位置 |
| ---- | --------- |
| spec 文件（charter / requirements / archive） | 同目录（不动） |
| migrations | `migrations/2026-08-15-add-notification-preferences.sql` + `2026-08-15-add-mailgun-messages.sql`（已应用，不回滚） |
| `migrations/2026-09-15-drop-email-unsubscribe-token.sql` | Day 30 用户批准后执行；执行前保留（不动） |
| 删除的旧代码 | `src/lib/smtp-direct.ts` 删除点 = 本 feature 末次 commit；可通过 git history 追溯 |
| audit log 历史 | `audit_log` 表持续保留（INV-SEC-1） |
| artifacts/ | 全部保留（7 个 task 的 verification 证据） |

---

## 5. 与 `R-CHK-EX-1.3 archive / merge 边界` 期望对齐

| Sub-rule | 本 archive 状态 |
| ---------- | ---------------- |
| 是否显式声明 Archive Only 或 Merge Back？ | ✅ §1 显式声明 `Merge Back`（与 EX-M-1 形成对照） |
| 是否同时声明 Archive Only 和 Merge Back？ | ✅ 否（不矛盾） |
| 是否给出决策理由（决策矩阵）？ | ✅ §2 4 维度决策矩阵 |
| 是否说明合入边界（合入什么 / 不合入什么）？ | ✅ §3.1 + §3.2 |
| 是否定义合入 PR + Gate 路径？ | ✅ §3.3 |

应通过 `R-CHK-EX-1.3` 检查；对应"应失败" fixture = `F-FIX-3`（同时声明 Archive Only + Merge Back，或两者都不声明）。

---

## 6. 与 `EX-M-1` 形成的对照表

| 维度 | `EX-M-1` archive | `EX-B-1` archive |
| ------ | ----------------- | ------------------ |
| Project Mode | Greenfield | Brownfield |
| Spec Mode | Medium single-file | Medium 多文件（charter + requirements + archive） |
| Archive 决策 | **Archive Only** | **Merge Back** |
| long-living spec | 不建立 | 借此首次建立 `notifications-spec` |
| Delta operation 覆盖 | N/A（全 Add） | 5 种全覆盖（Add / Modify / Replace / Deprecate / Preserve） |
| 不可逆操作 | 无（可回滚 migration） | 有（Day 30 DROP COLUMN，需 Real-World Side Effect Gate 批准） |

两个 example 共同覆盖 `../../protocols/methodology-kernel.md` archive 边界四象限的两个最常见象限；剩下 `EX-A-1` Archive / merge edge case 后续轮次补充。
