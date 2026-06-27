# Forbidden Actions Table

> **When to read**: 在 `/specs-write` 任意阶段做违规自检，或出现禁止动作风险时读取本文并按处置锚点回切。

| Phase | 严禁动作 | 处置锚点 |
| ------- | ---------- | ---------- |
| Phase 0 maturity intake | 跳过 Project Maturity 判定或 SSOT Health Check | `templates/maturity-intake.md §Phase 0 判定硬规则` 停下补 `maturity-intake.md` |
| Phase 0 maturity intake | 将 `Needs Repair` / `Unfit As Source` 的 SSOT 继续派生为 charter / requirements / design | `templates/maturity-intake.md §Phase 0 判定硬规则` 执行 SSOT Repair 或 Gate A 用户裁决 |
| Phase 0 maturity intake | Seed / Greenfield 的 N/A 无 evidence 或无 Future Audit Trigger | `templates/maturity-intake.md` §2 补 Baseline / Greenfield Survey 证据 |
| 任意阶段 | 未经用户明确批准直接修改 Authoritative SSOT（母本 / L1 SSOT / .github/standards 权威章节） | `cross-cutting.md §1.4-B` 改写为 `SSOT Stewardship Suggestions` / `Repair Draft` 并请求 Gate A/B 批准 |
| 任意阶段 | 写业务代码 / 跑迁移 / 改真实 DB | 主 workflow §1.3 与 §2.6.3 workflow 边界 |
| 任意阶段 | 无 Decision Gate 留痕伪造 `Approval.Status = Approved` | `cross-cutting.md §2.3` 防伪追问 |
| 任意阶段 | 越阶段产出（一次产多件文件） | 主 workflow §0.3 节奏一次一件 |
| 任意阶段 | 复述 SSOT 已定义事实 | `cross-cutting.md §1.4-B` 改 `@<路径>#<章节>` 引用 |
| 任意阶段 | 行号区间定位 spec 内引用 | `cross-cutting.md §1.3` 改 ID 锚点 |
| Phase 1.5 audit | grep 命中当审计 / 只读 1–2 文件即推进 / "看起来是" 写 EXIST-*/ DB-API-UI-FS 状态未真实校验 / 省略 unknowns | `templates/audit.md §Phase 1.5 审计硬规则` 五条审计偷懒禁令 |
| Phase 1.5 audit | DB / API / UI / FS 类 EXIST 缺 `Verified By:` 4 项 / 原文 dump 超 2 句 / evidence_file 首行 4 桶分类缺失 | `appendix.md §A.4` 防 4 工具原文外置三铁律 |
| Phase 1.5 audit | Audit Depth Gate 未达 PASS_TO_REQUIREMENTS 即推进 Phase 2 | `templates/audit.md §Phase 1.5 审计硬规则` 必须同时满足 14 面覆盖 + Overall Confidence ≥ 80% + 两个强证据面（真实数据库面 / 文档 SSOT 面）各自 confidence ≥ 80% + Blocking Unknowns = none |
| Phase 2 requirements | REQ 缺 EARS AC 或缺 BDD Scenario | `cross-cutting.md §3.3` 强制配对 |
| Phase 2 requirements | 失败分支 BDD 缺失（涉及外部调用 / 写入 / 跨进程 / 批量作业） | `cross-cutting.md §3.2` 补失败分支场景 |
| Phase 3 design | 引入 INV-BAN-* 禁用依赖 | `cross-cutting.md §5.3` 停下回 Phase 1 修 charter |
| Phase 3 design | 重新定义 SSOT 已定义契约 | `cross-cutting.md §1.4-B` 改 `@<路径>#<章节>` 引用 |
| Phase 3 design | 跨边界 DSN 漏 Failure Strategy | `design-rules.md §1` 拒推进 Phase 4 |
| Phase 3 design | DSN-LLM 三件防御不全 | `design-rules.md §1` 补全 Prompt Boundaries / Deterministic Fallback / Context Truncation |
| Phase 3 design | 跨端通信两端手写结构体 | `design-rules.md §1` 改单端 SSOT + autogen |
| Phase 3 design | DSN-DB Replaces 漏 Migration Strategy（命中条件时） | `design-rules.md §1` 补三选一策略 |
| Phase 4 tasks | Task 头部缺必填字段 | `task-rules.md §1` 拒推进 Phase 5 |
| Phase 4 tasks | Traceability Matrix 手改单元格 | `appendix.md §A.1` 走 `traceability_regen` 脚本 |
| Phase 4 tasks | P0 Essential 超 5 条（跨边界 / 动凭据 超 7 条） | `appendix.md §A.5` Task 裁切不够细，回 Phase 4 拆 |
| Phase 4 tasks | A 类字段（Touches / Existing Touches / Verification Commands / Artifacts）未用 `[ ]` checkbox / B 类字段误用 `[ ]` | `task-rules.md §1` 字段二分硬规则 |
| Phase 4 tasks | Revert Conflict Risk 漏检共享文件 | `appendix.md §A.3` 防 3 强制声明 shared_with + shared_files |
| Phase 4 tasks | 修改既有源码 / 改既有 DB schema 已部署版 / 改既有 ORM 模型 / 改进程拓扑 / 写本地非源码状态 但 Revert Command 填 N/A | `task-rules.md §1` 五条铁律必填非 N/A |
| Phase 4 tasks | DSN-DB Replaces 命中迁移策略时，Revert Command 填 `git checkout` 物理回滚 | `task-rules.md §1` 必须改业务可回路径 |
| Phase 4 tasks | DB Test Isolation 命中时缺三要素任一 | `task-rules.md §1` 补隔离机制 / 副作用边界 / 收尾断言 |
| Phase 4 tasks | DB Test Isolation 缺 tier 档位选择 / Tier 3 缺"为何不能用 Tier 1/2"的豁免理由 / Tier 3 缺 reset + seed 配套 | `task-rules.md §1` 三档优先级反模式 |
| Phase 4 tasks | 项目层启用 `Goal / Steps / Task DoD` 扩展但未遵守 `task-rules.md §1` 字段二分（A 类未用 `[ ]` / B 类误用 `[ ]`） | `templates/tasks.md` 模板说明 #6 协议自检公式 |
| Phase 3 design / Phase 4 tasks | 使用枚举外 `<domain>` 但未在 charter / audit Notes 登记 `OTHER` 理由 + 转正方向 | `cross-cutting.md §1.2` 子域枚举硬规则 |
| Phase 4 tasks | Task 适用 INV-SEC-* 且 Touches 涉凭据 / 第三方 API / .env / 遥测 / 凭据轮转，但 Verification Commands 缺 secret-scan 命令 | `task-rules.md §1` Secret-Scan 命令条件化必填规则 |
| Phase 5 handoff | handoff-payload.yaml 缺 invariants 全文 / first_task 全量字段 / critical_contracts 全量 Task 跨边界 DSN 摘要 | `cross-cutting.md §4.3` schema 硬约束 |
| Phase 5 handoff | implementation_reflections 存活 > 10 未走 GC | `appendix.md §A.7` GC 流程 |
| 任意阶段 | 项目根 reports / tmp / output 散落 spec 副产物 | 主 workflow §1.6 artifacts/ 子目录硬约束；spec Done 时执行 cleanup_manifest |
