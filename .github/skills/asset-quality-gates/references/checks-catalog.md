# Checks Catalog · /asset-quality-gates 检查项规则表

> **本文是 `/asset-quality-gates` workflow 的检查项事实源**。所有 R-CHK-* 规则在此定义，入口 workflow 与报告模板按 ID 引用，不重复事实。
> 检查分两组：R-CHK-1~9 **内部资产健康检查**（适用所有 scope）+ R-CHK-10~16 **外部 intake 增量检查**（仅 SCOPE_DEFINED_EXTERNAL_INTAKE）。
> 本文档自身遵循结构化规则表 + ID 体系格式规范（入口骨架 + 支撑文档分离 + 零 ASCII 流程图）。

---

## 0. 定位与索引

### 0.1 文档定位

- 检查项规则字典，不是流程指南；流程见 `asset-quality-gates.md` Phase 骨架。
- 每条 R-CHK-*给：触发范围 / 检查动作 / 失败模式 / 失败动作 FA-HG-* / 源锚点。
- 与 `asset-quality-gates.md` Phase 3.6 检查项清单零漂移；本文是检查项的字典化展开。

### 0.2 ID 命名空间

- `R-CHK-1~9`：内部资产健康检查规则。
- `R-CHK-10~16`：外部 intake 增量检查规则。
- `FA-HG-1~4`：本 workflow 引用 `gate-dag-protocol.md §1.5` 失败动作子集。
  - `FA-HG-1`：结构性失败（frontmatter / 入口骨架 / 目录契约破裂）→ patch 修订。
  - `FA-HG-2`：license / provenance 失败 → 强制返回 quarantine 或 EXTERNAL_INTAKE_DECLINED。
  - `FA-HG-3`：索引漂移 → 报告 INDEX_SYNC_GAP_REPORTED，不直接修。
  - `FA-HG-4`：启用路径污染 → ACTIVATION_BLOCKED_BY_PATH_VIOLATION，触发 IRREV 等级反弹。

---

## 1. 内部资产健康检查（R-CHK-1~9）

适用范围：`SCOPE_DEFINED_INTERNAL` / `SCOPE_DEFINED_EXTERNAL_INTAKE`（intake 通过 quarantine 后也跑）/ Phase 6 写入后验证。

| 规则 ID (Rule ID) | 触发范围 | 检查动作 | 失败模式 | 失败动作 | 源锚点 |
| --------- | --------- | --------- | --------- | --------- | --------- |
| `R-CHK-1` | 所有 `.github/workflows/*.md` | 文件首部存在 YAML frontmatter + 一句话 `description` 字段 | 无 frontmatter / 缺 `description` / `description` 多行 / `description` 与文件实际定位漂移 | `FA-HG-1` | `asset-quality-gates.md` Phase 3.6 |
| `R-CHK-2` | 所有 `.github/workflows/*.md` | 入口文件保持"控制流骨架"：State 表 + Phase 骨架 + Companion Documents 索引；过长 / 过细的方法论细节抽到 `.github/workflow-docs/<name>/` | 入口超 12,000 字符且未抽支撑文档 / 方法论细节直接堆在入口 / Companion Documents 索引缺失 | `FA-HG-1` | `AGENTS.md` "Workflow 规则" + `asset-quality-gates.md` Phase 3.6 |
| `R-CHK-3` | `.github/workflows/` 目录 | 该目录只含 `.md` 文件，无任何子目录 | `.github/workflows/<name>/` 出现子目录（Windsurf 会把嵌套 markdown 识别为独立 workflow） | `FA-HG-1` | `AGENTS.md` "目录契约" |
| `R-CHK-4` | 所有支撑文档 | 支撑文档位于 `.github/workflow-docs/<workflow-name>/`，不在 `docs/` 也不在 `.github/workflows/<workflow-name>/` | 支撑文档落在 `docs/` / `.github/workflows/<name>/` / 仓库根目录 | `FA-HG-1` | `AGENTS.md` "目录契约" |
| `R-CHK-5` | `AGENTS.md` 启用 Skill / Workflow 索引 | 所有启用中 workflow / skill 都在 AGENTS.md 索引中登记，且链接到真实存在的 `.md` 文件 | 启用资产未登记 / 索引指向不存在的文件 / 索引项已废弃但未删除 | `FA-HG-3` | `AGENTS.md` "Workflow 索引规则" + "Skill 规则" |
| `R-CHK-6` | 所有 `.github/workflows/*.md` | 定义状态表的 workflow 必须同时定义 `State Authority / Route Action`；可中断流程必须定义 `Resume Source` 或明确说明无需恢复事实源 | 仅 State 表无 Authority / Action 表 / 可中断流程缺 Resume Source | `FA-HG-1` | `AGENTS.md` "Workflow 规则" |
| `R-CHK-7` | 所有 `.github/workflows/*.md` | Route Action 使用统一语义：`CONTINUE_IN_WORKFLOW` / `WAIT_FOR_USER` / `REPORT_AND_STOP` / `CONFIRMED_ACTION`；`CONFIRMED_ACTION` 不得传递为下游 workflow 或真实世界副作用授权；受限 safe-write 必须满足 exact target / existing slot / no authority escalation / no downstream authorization / report scope after write | 自创动作名 / `CONFIRMED_ACTION` 跨 workflow 越界 / 受限 safe-write 缺要素 | `FA-HG-1` | `AGENTS.md` "Workflow 规则" + `gate-dag-protocol.md §4.3` |
| `R-CHK-8` | 所有 `.github/workflows/*.md` | workflow 文件不得在非合法语境中混用 "skill" / "skills" 一词；workflow 与 skill 是不同资产类型 | workflow 文件用 "skill" 指代自身或 workflow 类别 | `FA-HG-1` | `AGENTS.md` "Workflow 规则" |
| `R-CHK-9` | 所有引用了内部别名的 workflow（如 `<sw>` / `<se>` / `<aqg>`） | 别名指向真实存在的支撑文档目录；定义点（"`<sw>` = `.github/workflow-docs/specs-write`"）在文件可读位置；引用与定义零漂移 | 别名指向不存在目录 / 定义缺失 / 引用拼写漂移（如 `<sw>` vs `<spec-write>`） | `FA-HG-1` | `AGENTS.md` "验证清单" |

---

## 2. 外部 intake 增量检查（R-CHK-10~15）

适用范围：`SCOPE_DEFINED_EXTERNAL_INTAKE` 且已在 Phase 2.5 完成 quarantine。

| 规则 ID (Rule ID) | 触发范围 | 检查动作 | 失败模式 | 失败动作 | 源锚点 |
| --------- | --------- | --------- | --------- | --------- | --------- |
| `R-CHK-10` | `.github/.quarantine/<source-slug>/` 下所有外部资产 | `provenance.md` 完整：来源 URL / commit SHA / 抓取时间 / 抓取者 / 原始 license 副本 / 原始 frontmatter | 缺任一字段 / 来源不可验证 / commit SHA 漂移 | `FA-HG-2` | `intake-protocol.md §2` |
| `R-CHK-11` | `.github/workflows/` + `.github/skills/` 当前 git diff | 启用路径未出现绕过 quarantine 的新增项（即所有新增启用资产都能在 `.github/.quarantine/<slug>/` 找到 provenance）；如有新增项未经 quarantine → 启用路径污染 | 启用路径新增项缺对应 quarantine 来源 / `git status` 显示 `.github/workflows/` 直接被外部资产污染 | `FA-HG-4`（强制 `ACTIVATION_BLOCKED_BY_PATH_VIOLATION`） | `asset-quality-gates.md §0.4` |
| `R-CHK-12` | quarantine 中外部资产的 license | license 与本仓库 license 兼容（MIT / Apache-2.0 / CC0 / BSD 类）；GPL / AGPL / 无 license / "all rights reserved" 必须用户裁决 | license 冲突 / 缺失 / 用户未确认承担合规风险 | `FA-HG-2` | `intake-protocol.md §3` |
| `R-CHK-13` | quarantine 中资产 frontmatter | 已按本仓库 §0.2 与 AGENTS.md 规则适配 frontmatter；workflow 有一句话 `description`；skill 用 kebab-case 目录名 + `SKILL.md` 入口 | frontmatter 缺失 / `description` 漂移 / skill 不符合扁平目录契约 | `FA-HG-1` + `FA-HG-2` | `intake-protocol.md §4` + `R-CHK-1` |
| `R-CHK-14` | quarantine 中所有 skill | 已定义 skill eval 起点：≥ 1 个 expected behavior 场景 + ≥ 1 个 anti-trigger 场景 + 验证记录占位 | 缺 eval 起点 / 仅描述触发词不定义可验证行为 | `FA-HG-2` | `asset-quality-gates.md` Phase 3.6 skill eval 要求 |
| `R-CHK-15` | `AGENTS.md` 启用索引 | 启用 patch 草案已生成，包含资产中文名 / 名称 / 角色（Active / Personal / Experimental）/ 描述；草案未直接写入（仍在 `CHECKS_PASSED_PENDING_USER_APPROVAL`） | 启用 patch 缺索引 / 角色未定 / 中文名缺 / 描述与 `description` 漂移 | `FA-HG-3` | `AGENTS.md` "Skill 规则" / "Workflow 索引规则" |
| `R-CHK-16` | quarantine 下所有外部资产文件 | 静态扫描外部搬迁源码或文档内容，阻断 `.claude`、`mcp__*`、`gstack-upgrade`、外部 telemetry 上报等跨工具残留与潜在远程溢出指令 | 源码或文档中匹配到 `.github/skills`、`mcp__claude-in-chrome`、`telemetry` 等特定敏感字符串 | `FA-HG-2` | `intake-protocol.md §I-2` + `security-checks-catalog.md` |

---

## 3. Spec Conformance 检查（R-CHK-EX-1.1~1.8 已启用，待 checker 实现）

Spec conformance 检查项源于 `../../specs-write/conformance-fixtures/README.md` 的 8 类应失败 fixture 套件：`../../specs-write/examples/`（5 类 canonical examples）+ `../../specs-write/conformance-fixtures/`（8 类应失败 fixtures，含 NFR 留空 fixture）已交付；本节展开 8 个子规则作为 Phase 3.6 默认检查。

### 3.1 R-CHK-EX-1.* 子规则定义

| 规则 ID (Rule ID) | 触发范围 | 检查动作 | 失败模式 | 严重性 | 失败动作 | 强制命中夹具 (Must-hit fixture) | 源锚点 |
| --------- | --------- | --------- | --------- | ------- | --------- | ----------------- | -------- |
| `R-CHK-EX-1.1` | Brownfield spec 的 `charter.md` §2 EXIST-REQ 表 + `requirements.md` Derivation Map / REQ 段 | 每个 EXIST-REQ-*/ REQ-* 必有 `Add / Modify / Replace / Deprecate / Preserve / Merge Back / Archive Only` 任一标记；Greenfield 项目（无 EXIST-REQ）不触发 | EXIST-REQ-*缺 delta operation 列；REQ 缺 `Delta Operation` 字段；Derivation Map 缺关系类型列 | High | `FA-HG-2` | `../../specs-write/conformance-fixtures/F-FIX-1/` | `../../specs-write/protocols/methodology-kernel.md` 7 种 delta operation |
| `R-CHK-EX-1.2` | spec.md / requirements.md 中所有 REQ-* | 每个 REQ-*必有 `Derived From: SRC-### → REQ-###` 字段；锚点能回链到 §1 Sources；Brownfield 允许 `Derived From: EXIST-REQ-### → REQ-###` 形式 | REQ-* 缺 `Derived From`；锚点不存在；SRC ↔ REQ 链断裂 | High | `FA-HG-2` | `../../specs-write/conformance-fixtures/F-FIX-2/` | `../../specs-write/protocols/methodology-kernel.md` traceability 追溯协议 |
| `R-CHK-EX-1.3` | feature spec 的 `archive.md` | 显式声明 `Archive Only` 或 `Merge Back`（恰好一个）；不允许同时声明矛盾或两者都不声明；REQ-level 复合决策必须每个 REQ 独立标且不交叉 | §1 元数据同时含 Archive Only + Merge Back 段；§2 决策矩阵缺最终决策行；REQ-level 决策有矛盾 | **Critical** | `FA-HG-1` + 阻塞 long-living spec merge back PR | `../../specs-write/conformance-fixtures/F-FIX-3/` | `../../specs-write/protocols/methodology-kernel.md` archive vs merge back 边界 |
| `R-CHK-EX-1.4` | feature spec 的 `tasks.md` Status / Verification 结果 / spec close-out Status | tasks Status / verification 结果 / spec close-out Status 三者一致；Done task 不得 verification FAIL；spec Done 不得有 Pending task | Done task verification FAIL；spec Done 但 task Pending；Status 与 archive.md 状态矛盾 | High | `FA-HG-2` | `../../specs-write/conformance-fixtures/F-FIX-4/` | `../../specs-write/protocols/methodology-kernel.md` active/done 状态机契约 |
| `R-CHK-EX-1.5` | charter §5 Architectural Invariants vs requirements / design / tasks 的 schema / 列 / 依赖 / 模式 | design / requirements / tasks 不得引入 INV-BAN-*显式禁止的字段、依赖、模式；INV 修改必须先经 charter §5 + Critical Design Gate 用户批准 | DSN-*引入被 INV-BAN 禁止的列 / 表 / endpoint；TASK 实施层违反 INV-LIM-* | **Critical** | `FA-HG-1` + REQUIRE charter INV revisit + RWSE Gate 用户批准 | `../../specs-write/conformance-fixtures/F-FIX-5/` | `../../specs-write/protocols/methodology-kernel.md` Critical Design Gate |
| `R-CHK-EX-1.6` | charter §3 Scope + §4 Out-of-Charter vs tasks `Touches` / `Description` | tasks 不得引入 charter §4 显式 out-of-charter 列出的功能；扩展必须先在 charter §3 Scope 加入 + Strategy Gate 用户批准 | TASK Description / Touches 引入 out-of-charter keyword 匹配 | **Critical** | `FA-HG-1` + REQUIRE charter scope revisit | `../../specs-write/conformance-fixtures/F-FIX-6/` | `../../specs-write/protocols/methodology-kernel.md` Strategy Gate |
| `R-CHK-EX-1.7` | tasks.md 中所有 `Status: Done` 的 Task | Done task 必有：(1) 非空 `Verification:` 命令字段；(2) 非空 `Artifacts:` 字段；(3) Artifacts 引用文件实际存在（fixture 目录或 spec 目录可访问）。Pending / In Progress / Blocked task 不强制 | Done task `Verification:` 空白；`Artifacts:` 空白；Artifacts 路径不存在 | **Critical** | `FA-HG-1` + 阻塞 spec close-out | `../../specs-write/conformance-fixtures/F-FIX-7/` | `../../specs-write/protocols/methodology-kernel.md` Verification 硬约束 |
| `R-CHK-EX-1.8` | requirements.md §10 NFR 段（或 examples/EX-*/requirements.md NFR 等价段） | (1) §10.0 High-Risk Assessment 表存在且每行标 High / Low；(2) 每个 High 类必有 ≥ 1 条 `Status: Active` NFR；(3) Low 类必显式 `N/A: <理由>` 不留空；(4) 每条 Active NFR 必有 `Verification` 字段非空；(5) Brownfield 模式（charter 标 Project Mode = Brownfield/Hybrid）每条 NFR 必有 `Delta Operation` 字段；(6) §10.7 路由表与 §10.1~§10.6 各条 NFR 一致；(7) tasks.md 至少有 1 个 Task 引用每条 Active NFR | High-Risk 表缺失或留空；High 类无 Active NFR；Low 类整段空白；Active NFR 缺 Verification；Brownfield NFR 缺 Delta Operation；路由表与各类不一致；Active NFR 在 tasks.md 无引用 | **High** | `FA-HG-2` + 阻塞 spec close-out（高风险 NFR 不可静默忽略） | `../../specs-write/conformance-fixtures/F-FIX-8/` | `../../specs-write/templates/requirements.md §10` + `../../specs-write/protocols/methodology-kernel.md §1.1` |

### 3.2 启用与执行模式

-**启用状态**：✅ 已启用（examples + fixtures 已交付）；checker 实现仍 pending（仅规则 / fixture 套件就位，自动检测器待编码）。

- **Phase 3.6 接入路径**：`/asset-quality-gates` Phase 3.6 跑 `../../specs-write/examples/EX-*/` 全部 R-CHK-EX-1.1~1.8 检查 → 必须全 PASS；跑 `../../specs-write/conformance-fixtures/F-FIX-1~8/` 全部 → 必须命中对应 sub-rule 且报告"期望失败已识别"。
- **任一失败 / 漏识别**：`CHECKS_FAILED_NEEDS_REVISION` + 报告漂移点；阻塞 spec close-out / long-living spec merge back PR。
- **checker 实现提示**：见每个 fixture 的 `expected-failure.md §4 checker 实现提示`。

### 3.3 与 examples / fixtures 三角对照

| Sub-rule | 正确边 example | 错误边 fixture | 双正确边 / 三角对照 |
| ---------- | --------------- | --------------- | ------------------- |
| 1.1 delta operation | `EX-B-1`（5 种 delta 全用） | `F-FIX-1`（删 delta 列） | - |
| 1.2 traceability | `EX-M-1` / `EX-G-1`（Derived From 闭环） | `F-FIX-2`（删 Derived From） | - |
| 1.3 archive/merge | `EX-M-1`（Archive Only） + `EX-B-1`（Merge Back） + `EX-A-1`（REQ-level 复合） | `F-FIX-3`（spec-level 矛盾） | 三角：双正确边（spec-level + REQ-level） + 错误边 |
| 1.4 active/done | `EX-G-1`（Status 一致） | `F-FIX-4`（Mode A/B 矛盾） | - |
| 1.5 INV-BAN | `EX-G-1`（INV-BAN-3 守护） | `F-FIX-5`（引入 oauth_access_token） | - |
| 1.6 out-of-charter | `EX-G-1`（仅 Google） | `F-FIX-6`（加 GitHub OAuth） | - |
| 1.7 verification | `EX-G-1`（7 task 全有 Verification） | `F-FIX-7`（三种缺失模式） | - |
| 1.8 NFR 完整性 | `EX-G-1`（6 类 NFR：5 High 全有 Active + 1 Low N/A） + `EX-B-1`（Brownfield NFR 包含 5 种 Delta Op） | `F-FIX-8`（高风险 feature NFR 留空 + Brownfield NFR 缺 Delta Op） | 双正确边（Greenfield NFR + Brownfield NFR delta） + 错误边 |

---

## 4. 边界与不检查项

| 类别 | 是否检查 | 理由 |
| ------ | --------- | ------ |
| 业务 spec 正确性 | 不检查 | 归 `/specs-write` / `review` |
| 代码逻辑 / 实现质量 | 不检查 | 归 `/repo-safety-setup` typecheck / test |
| 长文档可读性 | 不检查 | 只检查"是否抽到 workflow-docs"，不评判风格 |
| skill 实际行为质量 | 不检查 | 归未来 `skill-eval` skill / 人工评测 |
| 人工 license 合规判定 | 不替代 | R-CHK-12 只做兼容性候选判定 + 强制用户裁决 |
| 设计审查 | 不替代 | 检查项只能发现结构问题，不能发现设计漏洞 |

---

## 5. 修订规则

- 本文修订必须同 PR 修订 `asset-quality-gates.md` 入口（State 表 / Phase 骨架 / 报告模板）。
- R-CHK-* ID 一旦分配不得复用；废弃改用 deprecated 标记，不删除。
- 新增 R-CHK-* 必须先在 `asset-quality-gates.md` Phase 3.6 检查项清单同步事实源。
- 失败动作必须复用 `gate-dag-protocol.md §1.5 FA-HG-*` 体系，不另创命名。
