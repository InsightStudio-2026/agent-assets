# EX-G-1 · Greenfield happy path canonical example

> **角色**：展示 Greenfield 项目第一个 spec 走通 **Phase 0-5 完整路径**：Maturity Intake → Charter → Requirements → Design → Tasks → Verification → Archive，三类 Gate（Strategy / Critical Design / Real-World Side Effect）全过。
> 与 `../../protocols/methodology-kernel.md` §10 完整路径规范字面零漂移。

---

## 1. Example 元数据

| 字段 | 值 |
| ------ | --- |
| Example ID | `EX-G-1` |
| Project Mode | Greenfield |
| Spec Mode | Medium（多文件：charter / requirements / archive；design + tasks 嵌入 requirements 末尾） |
| 三类 Gate 通过 | Strategy `PROCEED` + Critical Design `PROCEED_AFTER_REVIEW` + Real-World Side Effect `PROCEED_AFTER_REVIEW`（OAuth client 注册 = 外部副作用） |
| 引用对应 fixture | `F-FIX-7` Verification 缺失（伪 EX-G-1，删 Done Task 的 Verification 字段） |
| 覆盖语义层 | proposal / behavior / plan / tasks / verification / archive 全段 |
| 状态 | ✅ canonical reference |

---

## 2. 模拟场景

**用户原话**：
> 给我们的 SaaS 加一个 Google OAuth 登录入口；新用户首次登录时自动建账号；已注册邮箱第一次走 OAuth 时账号合并。MVP 只接 Google 一家，先不接 GitHub / Microsoft。

**判定结果**：

- Project Mode = Greenfield（项目早期；已有 username/password 认证基础设施 baseline，但本 feature 是首次接入第三方 OAuth）
- Spec Mode = Medium（多文件 charter + requirements + archive；不需 Large 独立 design.md，design 嵌入 requirements 末尾）
- 三类 Gate 全过：Strategy（OAuth 是产品定型功能）+ Critical Design（账号合并策略 = 关键设计）+ Real-World Side Effect（向 Google Cloud Console 注册 OAuth client = 外部副作用，需用户批准）

---

## 3. 文件清单

| 文件 | 角色 | 状态 |
| ------ | ------ | ------ |
| `README.md` | 本文 | ✅ |
| `charter.md` | Phase 0 Maturity Intake + Phase 1 Charter | ✅ |
| `requirements.md` | Phase 2 Requirements + 嵌入 Phase 3 Design + Phase 4 Tasks + Phase 5 Verification | ✅ |
| `archive.md` | Phase 6 Archive（Archive Only 决策，与 EX-M-1 同侧但场景更复杂） | ✅ |

---

## 4. 与 `R-CHK-EX-1.*` 期望对齐

| Sub-rule | 期望 |
| ---------- | ------ |
| `R-CHK-EX-1.1` Delta operation | N/A（Greenfield 全 `Add`，但 archive.md 显式标 `Archive Only`） |
| `R-CHK-EX-1.2` Traceability | `Derived From` 字段在每个 REQ 都填 SRC + AC 链 |
| `R-CHK-EX-1.3` Archive / merge | archive.md 显式标 `Status: Archive Only`（与 EX-M-1 同侧；后续 OAuth 多 provider 扩展由 Brownfield delta spec 派生） |
| `R-CHK-EX-1.5` Architectural Invariants | charter §6 INV-SEC-2 / INV-LIM-3 在 design 段未被违反 |
| `R-CHK-EX-1.6` Out-of-Charter | charter §4 显式列 5 项 out-of-charter 边界，tasks 不越界 |
| `R-CHK-EX-1.7` Verification | 每个 Done Task 有 `Verification:` 字段 + `artifacts/` 列表 |

---

## 5. 与 `F-FIX-*` 应失败 fixture 引用

| Fixture | 失败模式（基于本 example 的伪化） |
| --------- | -------------------------------- |
| `F-FIX-7` | 删除本 example tasks 表的 `Verification` 列 → 期望 `R-CHK-EX-1.7` 命中（severity = Critical） |

`F-FIX-5 / F-FIX-6` 也可基于本 example 伪化（INV 违反 / Out-of-Charter 越界），见各 fixture README。

---

## 6. 复用注意

- 本 example 的 OAuth login 是真实业务场景，非 hello-world。
- 三类 Gate 决策路径可作为新项目首个 spec 的模板：Strategy（产品定型）/ Critical Design（合并策略）/ Real-World Side Effect（OAuth client 注册）。
- 如复用为 Brownfield 扩展（如新增 GitHub OAuth provider），必须改造为 `EX-B-1` 模板（含 EXIST-REQ-* + Derivation Map + delta operation）。
