# Documentation Sync · /release-deploy 文档同步事实源

> **本文是 `/release-deploy` workflow Phase 4 文档同步规则字典**。所有 R-DOC-* 规则在此定义；入口 workflow 按 ID 引用，不重复事实。
> 本文档自身遵循结构化规则表 + ID 体系格式规范（入口骨架 + 支撑文档分离 + 零 ASCII 流程图）。

---

## 0. 定位与索引

### 0.1 文档定位

- 发布前文档同步规则字典；与 `release-deploy.md` Phase 4 Documentation Sync / Generate Boundary 项零漂移。
- 不是文档写作教程；只规定哪些文档必须随发布更新、哪些边界不可逾越、哪些情形必须升级到用户裁决。
- 与 Diataxis 文档分类法对齐：reference / how-to / tutorial / explanation。

### 0.2 ID 命名空间

- `R-DOC-1~7`：覆盖 / 边界 / 事实更新 / 升级判定 / CHANGELOG 规则 / 生成边界 / 顶层禁滥增。

---

## 1. 文档同步规则（R-DOC-*）

| 规则 ID (Rule ID) | 规则 | 触发范围 | 自动 / 用户裁决 | 严重性 |
| --------- | ------ | --------- | ---------------- | -------- |
| `R-DOC-1` | Diataxis 覆盖检查 | 任何 release diff 暴露 public surface | 自动检查 4 类（reference / how-to / tutorial / explanation）覆盖；缺则报告 | Medium |
| `R-DOC-2` | README / AGENTS / 运行手册 / 架构图同步 | diff 影响入口 / 命令 / 架构 | 事实更新（命令、配置、文件路径）= 自动；架构图、运行流程叙事 = 用户裁决 | High |
| `R-DOC-3` | CHANGELOG 规则 | 任何 release | 只做事实修正和措辞润色；**绝不**重写、删除、重排历史 entry；新 entry 严格按版本顺序追加 | Critical |
| `R-DOC-4` | Release Notes | 用户可见发布 | 自动起草；用户审阅 + 确认后才发；不得把内部代号 / spec 路径暴露 | High |
| `R-DOC-5` | 叙事 / 哲学 / 安全模型 / 大段删除 | 文档结构性变更 | 升级 `DOCUMENTATION_SYNC_BLOCKED_BY_NARRATIVE` + `S-HG-4` + `HG-STRAT-{slug}-doc-narrative`；等用户裁决 | Critical |
| `R-DOC-6` | 文档生成边界 | release diff 暴露 public surface 但文档缺失 | 可生成缺口文档；必须先读真实代码 + 现有文档；引用真实命令、文件、配置；不写泛泛教程；不在 `docs/` 顶层滥增 | Medium |
| `R-DOC-7` | 顶层禁滥增 | 任何新文档 | feature 文档进 `docs/specs/<slug>/` 或 `../`；工程规范进 `.github/instructions/`；元协议进 `docs/Assets/`；`docs/` 顶层 .md 仅限 L1 SSOT 主文档 | Critical |

---

## 2. 事实更新 vs 战略级修订（R-DOC-2 / R-DOC-5 判定矩阵）

| 修订类型 | 示例 | 判定 | 动作 |
| --------- | ------ | ------ | ------ |
| 事实更新 | 命令名变更（`pnpm dev` → `pnpm start`）；配置项重命名；文件路径迁移；版本号 / 依赖号更新；API endpoint 路径调整；CLI flag 增减 | **R-DOC-2 自动** | 直接 patch；写入 release-report 已做项 |
| 措辞润色 | 拼写、语病、排版、表格修复 | **自动** | 直接 patch |
| 叙事 / 哲学 | 项目定位声明、产品哲学、设计原则、开发协议宣言 | **R-DOC-5 升级** | 等用户裁决；不自动改 |
| 安全模型 | threat model / 数据流分级 / PII 处理边界 / 密钥管理叙事 | **R-DOC-5 升级** | 等用户裁决；同时启 `/security-privacy-audit` 复审 |
| 大段删除 | ≥ 50 行连续删除 / 整章删除 / 整文档删除 | **R-DOC-5 升级** | 等用户裁决；记录删除原因 |
| 架构图 | 系统组件图、数据流图、部署拓扑图 | **R-DOC-5 升级** | 事实变更 = 用户确认后改；纯美化 = 自动 |
| 运行手册流程 | 部署 / 回滚 / 事故响应 / 数据恢复 步骤叙事 | **R-DOC-5 升级** | 步骤变更 = 用户确认 + `/observability-incident` 复审；命令名替换 = 自动 |

---

## 3. CHANGELOG 不可逾越的边界（R-DOC-3 详则）

| 操作 | 允许 | 禁止 |
| ------ | ------ | ------ |
| 追加新 release entry | ✅ 严格按版本顺序 | ❌ 不允许在已发版本前插队 |
| 修正旧 entry 中的事实错误 | ✅ 例：错写的命令 / 路径 / 版本号 | ❌ 不允许重写整条 entry |
| 措辞润色 | ✅ 不改变事实和语义 | ❌ 不允许改变 entry 含义 |
| 删除已发布 entry | ❌ | ❌ 即使该 release 被 yank 也只能新增 yank entry，不删原 entry |
| 合并多条 entry | ❌ | ❌ 不允许"整理历史" |
| 重新排序 | ❌ | ❌ 即使时间记错也只能加注释 |

CHANGELOG 是信任凭证；任何改动必须可被旧版本读者识别。

---

## 4. 文档生成边界（R-DOC-6 详则）

| 允许场景 | 必须满足条件 |
| --------- | ------------- |
| 新公共 API 缺 reference | 先读真实实现 + 既有文档；引用真实签名、参数、错误码；不臆造示例 |
| 新 CLI 命令缺 how-to | 实际跑通命令 + 复制真实输出；不写"通常这样"等泛泛 |
| 新模块缺 explanation | 引用 ADR / spec design.md / CONTEXT.md；不另起一套术语 |
| 教程类（tutorial） | 默认不自动生成；用户明确要求才草拟 + 用户审阅 |

| 禁止场景 |
| --------- |
| 写"一般来说"、"通常情况下"等泛泛教程 |
| 引用不存在的命令 / 配置 / 文件 |
| 在 `docs/` 顶层新增非 L1 SSOT 主文档 |
| 复制粘贴 README 内容到多处造成漂移 |
| 自创术语而不引用 `../../specs-write/references/terminology.md` |

---

## 5. 报告格式（Phase 4 输出）

```markdown
## 文档手册同步审计 (Documentation Sync)

### 覆盖率评估 - Diataxis (Coverage)

- 参考手册 (reference): <PASS / FAIL + 缺项>
- 操作指南 (how-to): <PASS / FAIL + 缺项>
- 教程示例 (tutorial): <PASS / FAIL / N/A>
- 深度原理说明 (explanation): <PASS / FAIL + 缺项>

### 文档漂移检测 (Drift Detection)

- README 说明文件: <已同步 / 漂移 + 文件 + 行号>
- AGENTS.md 代理索引: <...>
- CHANGELOG 变更日志: <...>
- 运行维护手册: <...>
- 系统架构图: <...>

### 自动应用的变动 (Auto-applied)

- <列出 R-DOC-2 自动 patch 的项>

### 待用户批准项 (Pending User Decision - 战略级)

- <列出 R-DOC-5 升级的项 + 升级原因>

### 违规拦截拦截记录 (Forbidden Detected - 如有)

- <列出违反 R-DOC-3 / R-DOC-7 尝试 + 已拒绝>

### 综合审计结论 (Aggregate Verdict)

- 战略级决策项已解决 (All Pending User Decision resolved) + 自动更新已完成 (auto-applied complete) → 可进入步进 5 (continue Phase 5)
- 存在未解决的战略级项 (Any unresolved) → `/release-deploy:DOCUMENTATION_SYNC_BLOCKED_BY_NARRATIVE`

```

---

## 6. 修订规则

- 本文修订必须同 PR 修订 `release-deploy.md` Phase 4 骨架与 State 表 `DOCUMENTATION_SYNC_PENDING` 行。
- R-DOC-* ID 一旦分配不得复用；废弃改 deprecated。
- CHANGELOG 边界（R-DOC-3）任何放宽必须先在 `release-deploy.md` Phase 4 同步并经用户裁决。
- 顶层禁滥增（R-DOC-7）与 `.github/instructions/documentation.instructions.md` SSOT 字面零漂移；任何调整必须先改文档体系 SSOT。
