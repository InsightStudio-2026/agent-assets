# audit.md 模板

> **When to read**: 在 `/specs-write` Phase 1.5 落 Spec Derivation Audit `audit.md` 时读取本文（仅 Hybrid / Brownfield）。Verified By 4 项字段适用所有 DB / API / UI / FS 类 EXIST；按 EXIST-DSN-* 类型选择 tool 与 command（详 `appendix.md §A.4` 工具差异表）。

## Phase 1. 审计硬规则（落 audit.md 前必读）

- **职责限定**：本审计是 Spec Derivation Audit，只证明本 feature 的 REQ / DSN / TASK 能安全派生；不是项目级架构审计、缺陷审计、商业审计或 SSOT 修复入口。
- **14 面审计固定**：代码入口 / 架构与模块 / 数据 / 真实数据库 / 契约与接口 / UI / 运行与部署 / 测试 / 依赖关系 / 历史 / 文档 SSOT / 安全与隐私 / 可观测性 / 合规与版权 必与下方 Audit Coverage Matrix 一一对应，不得自行替换或合并面数。
- **Scoped / Full 区分**：`Hybrid` 可按 feature 影响范围裁剪审计深度，但必须在 `## 1. Scope of Audit` 写明裁剪理由与排除面；`Brownfield` 必须在本 feature 影响面内 14 面全审，不等于项目全仓审计。
- **范围限定**：反向标识 `EXIST-*` 仅围绕本 feature-slug 范围，不做无关考古；每个现状决策必须写明 `Reuse / Extend / Replace / Deprecate` 之一，`Conflict` 必附解决方向。
- **外部审计分流**：若发现问题超出本 feature 派生范围，只记录阻塞证据与推荐 route；架构 deepening → `/architecture-audit`，复杂缺陷 → `/bug-audit`，术语 / ADR 冲突 → `/grill-with-docs`，项目定位 / 母本缺陷 → `/project-inception`，商业生死问题 → `/business-model-audit`。
- **运行时校验留痕**：DB / API / UI / FS 类 EXIST 必须填 `Verified By:` 四项（tool / command / evidence_file / interpretation），原文外置到 `audit-evidence/`，并遵守 `appendix.md §A.4` 的四桶分类。
- **禁止审计偷懒**：禁止把 grep 命中当审计完成；禁止只读 1–2 个文件即进入 design；禁止用"看起来是"写 EXIST-*；禁止未验证真实 DB / API / UI / FS 状态就写成事实；禁止省略 unknowns。
- **细项不得折叠**：Audit Coverage Matrix 每一面都必须在对应 evidence_file 中逐项列出"已查 / N/A / 未决"状态；不得只写"已扫描"、"已核对"、"无问题"等总括词。
- **Audit Depth Gate 双层门**：进入 Phase 2 前必须同时满足：14 面均有覆盖判定；真实数据库面与文档 SSOT 面不可 N/A；Overall Confidence ≥ 80%；真实数据库面 / 文档 SSOT 面各自 confidence ≥ 80%；所有 Unknowns 要么清零，要么写明不影响 Phase 2 的理由与后续验证点。任一不达标 = `BLOCKED_AUDIT_DEBT`。
- **强制真实工具**：数据库面必须用 PostgreSQL MCP / SQLite MCP 或等价工具 readback 真实 schema、约束、索引、行数与示例行；文档 SSOT 面必须深读 L1 SSOT、`.github/instructions/`、active / done specs、Project Archives、artifacts，不得只用关键词 grep。
- **质量优先**：Phase 1.5 中 AI-DRI 优先保证审计质量；不得为节省时间跳读；未通过 Audit Depth Gate 不得 AI-DRI 自动批准。

## Spec Derivation Audit — `<Feature Name>`

Feature Slug: `<feature-slug>`
Mode: Brownfield | Hybrid
Charter Ref: charter.md

## 1. Scope of Audit

<围绕本 feature-slug 的领域范围；列出审计覆盖的模块 / 表 / 接口边界>

## 2. Audit Coverage Matrix（Feature-Scoped 14 面审计深度门 · 五阶全景 分层）

> **MUST read**: `@/.github/skills/project-steward/protocols/unified-14-surface-audit.md`
> 本 Feature 的派生必须严格按统一 14 面审计准则，对以下表格进行 14 面扫描（并在 evidence 目录下提供证据），确保不遗漏未知数。

Audit Depth Gate:

- Overall Confidence: <0-100%>
- Strong Evidence Confidence: Real Database <0-100%>；Document SSOT <0-100%>
- Blocking Unknowns: none | <列表 + 不影响 Phase 2 的理由 / 后续验证点>
- Decision: PASS_TO_REQUIREMENTS | BLOCKED_AUDIT_DEBT

## 3. Existing Implementations

### EXIST-REQ-###: <现有功能标题>

- Code Anchors:
  - `<path>::<symbol>`
- Coverage: 已实现 X，未实现 Y，半成品 Z
- Linked SSOT: SRC-###@<章节>
- Status: Active | Deprecated | Half-baked

### EXIST-DSN-DB-###: <现有表 / 字段 / 约束>

- Anchors:
  - `migrations/<file>` / `<orm>/<model>::<class>`
- Schema 摘要: ...
- Linked SSOT: SRC-###@<章节>
- Verified By（4 项 · 原文外置 · 详见 `appendix.md §A.4`）:
  - tool: <PostgreSQL-MCP / sqlite-MCP / 等同等价工具>
  - command: `SELECT column_name, data_type, is_nullable FROM information_schema.columns WHERE table_name='<表>'`
  - evidence_file: `audit-evidence/EXIST-DSN-DB-003.txt` · 首行 `# tool=... ; cmd=... ; ts=2026-MM-DDTHH:MM:SS+08:00 ; bucket=actual_state`
  - interpretation: 1–2 句结论

### EXIST-DSN-API-###: <现有接口>

- Anchors: `<router>::<handler>`
- 契约摘要: `<method>` `<path>` | request | response | error codes
- Linked SSOT: SRC-###@<章节>
- Verified By（4 项）:
  - tool: curl / httpx / OpenAPI fetch
  - command: ``curl -sS -X<METHOD> <baseURL>/<path> -H 'Authorization: `<REDACTED>`' -d '@`<sample.json>`'``
  - evidence_file: `audit-evidence/EXIST-DSN-API-012.txt`
  - interpretation: 1–2 句结论

### EXIST-DSN-UI-###: <现有页面 / 组件>

- Anchors: `<file>::<component>`
- 契约摘要: 路由 / props / 关键 state
- Linked SSOT: SRC-###@<章节>
- Verified By（4 项）:
  - tool: Playwright snapshot / accessibility inspector / Storybook render
  - command: <项目脚本路径，详见 `project-adapter.md §1`>
  - evidence_file: `audit-evidence/EXIST-DSN-UI-007.txt`
  - interpretation: 1–2 句结论
- Visual Refs（推荐）: Figma node ID / 设计稿哈希 / Storybook story

## 4. Reuse / Extend / Replace 决策

| 现有元素 | 决策 | 新元素 ID | 理由 |
| ---------- | ------ | ----------- | ------ |
| EXIST-DSN-DB-003 | Reuse | — | 字段足够 |
| EXIST-REQ-007 | Extend | REQ-001 | 加批量 + 失败回滚 |
| EXIST-DSN-API-012 | Replace | DSN-API-001 | 错误码不规范 |
| EXIST-DSN-OBS-005 | Deprecate | — | 已无消费者 |

## 5. Conflicts / Risks

- C1: 现有 `<X>` 与本 Spec 的 `<Y>` 冲突 → 解决方向: ...
- R1: 数据迁移可能影响 N 万行存量数据 → 缓解: ...

## 6. SSOT Gap（候选回流）

- Gap-1: SRC-001 未定义 `<X>`，建议在 SRC-001#<章节> 增补

> 仅记录候选，不在本 Spec 内回流；超 Charter §5 范围的回流按 `/specs-write` 主 workflow §1.3.1 分流。

## 7. Real Database Readback（真实数据库勘察）

- PostgreSQL MCP:
  - endpoints/databases inspected: <端口 / database>
  - queries: <只读 SQL 摘要>
  - evidence_file: `audit-evidence/db_readback_postgresql.txt`
- SQLite MCP:
  - db files inspected: <路径>
  - tables/indexes/schema inspected: <摘要>
  - evidence_file: `audit-evidence/db_readback_sqlite.txt`
- Interpretation: <真实 DB 与 schema/ORM/migration 是否一致；差异如何影响本 spec>

## 8. SSOT Survey（文档 SSOT 深读）

| SSOT / 文档 | 章节 | 与本 feature 关系 | 结论 | Gap / Conflict |
| ------------- | ------ | ------------------ | ------ | ---------------- |
| `.github/instructions/<file>.md` | §`<n>` | 数据契约 | 引用，不复述 | none |
| `docs/specs/done/<feature>/...` | §`<n>` | 历史实现 | 复用 EXIST-* | none |
| `docs/specs/project archives/<file>.md` | Part `<x>` | 交付事实 | 约束新方案 | Gap-1 |

## 9. Critical Assumptions Summary

- 至少 1 条，最多 3 条；或填 `N/A: <说明>`

## 10. Approval

- Status: Draft | Approved | Needs Changes
- Notes: <用户原话 或 AI-DRI auto-approved 留痕，详 `cross-cutting.md §2.3`>
- Timestamp: <ISO 8601>

## 11. Audit Refresh Log（增量勘察留痕 · append-only）

> 本节仅在 audit.md 已 Approved 后，因下游执行端反流的 `kind: audit_debt · severity: low` 反思（详 `appendix.md §A.7` 第 5 条）需要在不重过 Audit Depth Gate 的前提下补一笔最小勘察记录时使用。每行一条，append-only，不修改历史记录。
>
> 触发条件升级到 `severity: medium / high` 或出现新 conflict 者，**禁止**写入本节，应回 Phase 1.5 按 §A.7 第 5 条流程补 EXIST-* 锚点并重过 Audit Depth Gate。

| 日期 | 反思 ID | missing_audit_face | 增量勘察证据 | 解释 |
| ------ | --------- | -------------------- | -------------- | ------ |
| <ISO 8601> | REF-### | 代码入口 / 数据 / ... 14 面之一 | `audit-evidence/<EXIST-id>.txt` | 1–2 句结论 |
