# 快速自检清单（指针化 · 不复述规则）

> **When to read**: 在 `/specs-write` 每个 Phase 出口执行自检时读取对应小节。

## 1. Phase 0 自检（maturity-intake）

- [ ] `templates/maturity-intake.md §Phase 0 判定硬规则` Project Maturity 判定结论与证据
- [ ] `templates/maturity-intake.md §Phase 0 判定硬规则` Audit Profile 与 Project Mode 一致
- [ ] `templates/maturity-intake.md §Phase 0 判定硬规则` Hybrid / Brownfield 不跳过 Phase 1.5；Seed / Greenfield 不跳过 Baseline / Greenfield Survey
- [ ] `templates/maturity-intake.md §3` SSOT Health 九维已完成
- [ ] `templates/maturity-intake.md §Phase 0 判定硬规则` `Needs Repair` / `Unfit As Source` 未继续派生
- [ ] `cross-cutting.md §2.2` Blocking Issues 已分 Gate A / Gate B / N/A，命中项给强推荐 + ≤ 2 备选 + 代价
- [ ] §0.5 Critical Assumptions Summary（`templates/maturity-intake.md §6.5`；maturity-intake 可 N/A 但需说明原因）
- [ ] `cross-cutting.md §2.3` Decision = PROCEED_TO_CHARTER 时 Approval 留痕（用户 Gate 批准原话或 AI-DRI auto-approved）
- [ ] `forbidden-actions.md §Phase 0 校验` Format Validation Gate 通过
- [ ] `forbidden-actions.md §Phase Exit Gate` 三件套通过（Format Gate PASS + self-check [x] + _status 已创建/更新）

## 2. Charter 自检

- [ ] `templates/charter.md §1` Sources 含 SRC-### + timestamp
- [ ] `templates/charter.md §3.5 / §4 / §6` Opening Questions / Decisions Required / Derivation Constraints / Out of Charter 已列
- [ ] `cross-cutting.md §1.4-B` Derivation Constraints 已列
- [ ] `cross-cutting.md §5.3` Architectural Invariants 已列（INV-BAN-*/ INV-LIM-* 必须；INV-SEC-* 涉凭据 / 交易项目至少 1 条，否则在 §6 Out of Charter 明言"无 INV-SEC 适用"）
- [ ] §0.5 Critical Assumptions Summary（charter 可填 N/A 但需说明原因）
- [ ] `cross-cutting.md §2.1` Approval.Status = Acknowledged
- [ ] **`stop-conditions.md §3` Out-of-Charter 反降级**：Out of Charter 中每条已核查——不存在上游 SSOT 明确要求但被静默排除的项；凡命中 Gate B 升级条件的项均附 Exclusion Justification + Gate B 标注
- [ ] `forbidden-actions.md §Phase 1 校验` Format Validation Gate 通过
- [ ] `forbidden-actions.md §Phase Exit Gate` 三件套通过（Format Gate PASS + self-check [x] + _status 已更新）

## 3. Audit 自检（Phase 1.5 末尾，仅 Hybrid / Brownfield）

- [ ] `templates/audit.md §1 / §2` Scope of Audit + Audit Coverage Matrix 14 面已覆盖
- [ ] `templates/audit.md §Phase 1.5 审计硬规则` 真实数据库面已用 PostgreSQL MCP / SQLite MCP 或等价工具 readback
- [ ] `templates/audit.md §Phase 1.5 审计硬规则` 文档 SSOT 面已深读 L1 SSOT / .github/standards / active or done specs / `delivery-log.md` / artifacts
- [ ] `templates/audit.md §Phase 1.5 审计硬规则` Audit Depth Gate = PASS_TO_REQUIREMENTS；Overall Confidence ≥ 80%；两个强证据面各 ≥ 80%；Blocking Unknowns = none 或已说明不影响 Phase 2
- [ ] `appendix.md §A.4` DB / API / UI / FS 类 EXIST `Verified By:` 4 项 + evidence_file 首行 4 桶分类
- [ ] `appendix.md §A.4` audit.md 未出现超 2 句原文 dump
- [ ] §0.5 Critical Assumptions Summary
- [ ] `cross-cutting.md §2` Decision Gate 判定（用户 Gate 批准或 AI-DRI auto-approved 留痕）
- [ ] `forbidden-actions.md §Phase 1.5 校验` Format Validation Gate 通过（若适用）
- [ ] `forbidden-actions.md §Phase Exit Gate` 三件套通过（Format Gate PASS + self-check [x] + _status 已更新）

## 4. Requirements 自检

- [ ] `cross-cutting.md §3.1` 每条 REQ ≥ 1 条 EARS AC
- [ ] `cross-cutting.md §3.2` 每条 REQ ≥ 1 条 BDD Scenario；命中外部调用 / 写入 / 跨进程 / 批量场景含失败分支 Scenario
- [ ] `cross-cutting.md §3.3` EARS / BDD 互查无孤立
- [ ] `cross-cutting.md §3.2` BDD Given 引用 Fixture / Factory / Seed 锚点（非平凡数据态必须）
- [ ] 每条 REQ 至少关联一个 US；无孤立 US 或孤立 AC
- [ ] AC 主语为系统 / 服务 / 存储；行为可观察、不含模糊词
- [ ] `cross-cutting.md §1.4-A` 每条 REQ 填 `Derived From` + `Relation to Existing`；Net New 附 Justification
- [ ] `cross-cutting.md §1.4-B` 不复述 SSOT 已定义事实
- [ ] **`stop-conditions.md §2` SSOT 覆盖率门禁**：charter Sources 表的每个 SRC-### 节均已核查——每条都有 ≥1 条 REQ 通过 Derived From 覆盖，或已在 charter Out of Charter 中排除并附 Justification
- [ ] 主 workflow §2.3.3 Hybrid / Brownfield：`templates/requirements.md §5` Existing Coverage + `§8` Derivation Map；Seed / Greenfield 引用 maturity-intake Baseline / Greenfield Survey
- [ ] `templates/requirements.md` Non-Goals 已写；未出现技术选型句
- [ ] §0.5 Critical Assumptions Summary
- [ ] `cross-cutting.md §2` Decision Gate 判定
- [ ] `forbidden-actions.md §Phase 2 校验` Format Validation Gate 通过
- [ ] `forbidden-actions.md §Phase Exit Gate` 三件套通过（Format Gate PASS + self-check [x] + _status 已更新）

## 5. Design 自检

- [ ] `cross-cutting.md §1.1` / `§1.2` 每个 DSN 有 `DSN-`<domain>`-###` ID
- [ ] `cross-cutting.md §1.4-D` 每个 DSN 有 `Linked Requirements`；无孤立设计
- [ ] `cross-cutting.md §1.4-A` 每个 DSN 填 `Derived From` + `Relation to Existing`；Net New 附 Justification
- [ ] `cross-cutting.md §1.4-B` 不重新定义 SSOT 已定义契约
- [ ] `cross-cutting.md §5.3` 不违反 INV-BAN-*/ INV-LIM-* / INV-SEC-*
- [ ] `design-rules.md §1` 涉凭据 DSN 复述适用 INV-SEC-* 原文；明言凭据读取路径，不含真实凭据
- [ ] `design-rules.md §1` 跨边界 DSN 已填 `Failure Strategy`（三类 × 四元素）
- [ ] `design-rules.md §1` 并发 / 共享资源 / 异步 IPC / LLM 配额 命中场景的 DSN 已填 `Concurrency & Lock`
- [ ] `design-rules.md §1` DSN-LLM-* 三件防御齐全
- [ ] `design-rules.md §1` 跨端通讯 DSN 声明 Type SSOT + Generated Side + Regen + Drift Check
- [ ] `design-rules.md §1` DSN-UI-* 推荐附视觉锚点（软约束）
- [ ] `design-rules.md §1` DSN-DB Replaces 命中条件者填 `Migration Strategy:` 三选一 + business_data_safety_proof
- [ ] `design-rules.md §1` Hybrid / Brownfield：§1.5 Reuse vs New；Seed / Greenfield 不伪造 EXIST-*
- [ ] `design-rules.md §1` Alternatives Considered ≥ 1 条 + Risks
- [ ] `plan-delta-merge-protocol.md §1` Plan Artifacts Register 已判定 research / data-model / contracts / migration-plan / devex-note 是否需要，Required=Yes 的产物有 target path + verification
- [ ] `plan-delta-merge-protocol.md §2` DSN delta 与上游 REQ / NFR delta 一致；Replace / Deprecate 命中者有迁移、兼容窗口或清理条件
- [ ] §0.5 Critical Assumptions Summary
- [ ] `cross-cutting.md §2` Decision Gate 判定
- [ ] `forbidden-actions.md §Phase 3 校验` Format Validation Gate 通过（若适用）
- [ ] `forbidden-actions.md §Phase Exit Gate` 三件套通过（Format Gate PASS + self-check [x] + _status 已更新）

## 6. Tasks 自检

- [ ] `task-rules.md §1` 每个 Task 有 22 字段（Phase / Type / Priority / Status / Implements / Depends On / Design Refs / Derived From / Relation to Existing / Touches / Existing Touches / Reuse Notes / Effort / Test Anchors / Verification Commands / Artifacts / Revert Command / Revert Conflict Risk / Anti-Invariants / Resume Strategy / Context Required / Reflections）；Status ∈ `{Pending, In Progress, Done, Blocked, Blocked(Suspended)}`，机读 token 无空格
- [ ] `task-rules.md §1` 字段二分（A 类 [ ] 强制 / B 类禁用 [ ]）已遵守；自检脚本 grep 命中数自洽
- [ ] `task-rules.md §1` `Verification Commands / Touches / Existing Touches / Artifacts` 全部 `- [ ]`
- [ ] `task-rules.md §1` `Test Anchors / Revert Command / Revert Conflict Risk / Context Required / Reuse Notes / Anti-Invariants / Resume Strategy / Reflections` 普通 `-`
- [ ] `appendix.md §A.1` 双源单写：Markdown 表头加 <!-- generated-from: handoff-payload.yaml#traceability -->；YAML `traceability` 节枚举全量 Task
- [ ] `appendix.md §A.2` Test Anchors：除纯文档 / 纯配置外列出测试文件路径（sha256 留空，Phase 4 Red 后补）
- [ ] `appendix.md §A.3` Revert Conflict Risk：填了非 N/A `Revert Command` 且与先行 Done Task 共享 `Existing Touches` 者已逐对列 `shared_with` + `shared_files`
- [ ] `appendix.md §A.5` Context Required P0/P1 二分：P0 ≤ 5 条（跨边界 / 动凭据 ≤ 7 条）；跨边界 Task P0 含适用 INV-* + Failure Strategy + Concurrency & Lock
- [ ] `task-rules.md §1` Secret-Scan：Task 适用 INV-SEC-* 且涉凭据 / 第三方 API / .env / 遥测 / 凭据轮转 → `Verification Commands` 含 secret-scan 命令；豁免者 `Test Plan` 注明理由
- [ ] `task-rules.md §1` Hybrid / Brownfield：每个 Task 填 `Existing Touches` + `Reuse Notes`；Seed / Greenfield 可填 N/A 但需引用 maturity-intake 的空白基线证据
- [ ] `task-rules.md §1` DB Test Isolation（命中场景）：先选档（Tier 1/2/3 / N/A）+ tier_reason；Tier 3 必述"为何不能用 Tier 1/2"+ reset+seed 配套；再答三要素
- [ ] `templates/tasks.md` 模板说明 #6 项目层若启用 `Goal / Steps / Task DoD` 三扩展：A/B 类二分严守（`Steps` / `Task DoD` 用 `[ ]`，`Goal` 用 `-` 普通）
- [ ] `plan-delta-merge-protocol.md §2` Task Delta Projection 与上游 REQ / DSN / NFR 不冲突；Deprecate Task 有 owner / 删除条件 / 验证方式 / 清理 Task
- [ ] `cross-cutting.md §1.2` `<domain>` 子域枚举：DSN-*/ EXIST-DSN-* 全在 16 项内；使用 `OTHER` 者已在该 DSN Notes 登记理由 + 转正方向
- [ ] §0.5 Critical Assumptions Summary（可 N/A 但需说明原因）
- [ ] `templates/tasks.md` Test Plan / DoD / Rollback 已写
- [ ] `cross-cutting.md §2` Decision Gate 判定
- [ ] `forbidden-actions.md §Phase 4 校验` Format Validation Gate 通过
- [ ] `forbidden-actions.md §Phase Exit Gate` 三件套通过（Format Gate PASS + self-check [x] + _status 已更新）

## 7. Handoff 自检（Phase 5）

- [ ] `cross-cutting.md §4.3` schema_version + project_mode + audit_profile 与 maturity-intake.md 一致
- [ ] `cross-cutting.md §4.3` `invariants` 节复制 charter §5 全文（rule + scope）
- [ ] `cross-cutting.md §4.3` `traceability` 节枚举全量 Task；Markdown 表格从 YAML 重生
- [ ] `cross-cutting.md §4.3` `first_task` 节复制目标 Task 全部字段
- [ ] `cross-cutting.md §4.3` `critical_contracts` 包含 tasks.md 全量 Task 触及的所有跨边界 DSN（非仅 first_task）
- [ ] `cross-cutting.md §4.3` `implementation_reflections.active` 存活 ≤ 10；超限走 `appendix.md §A.7` GC + 归档
- [ ] `cross-cutting.md §4.3` `severity: high` 且 `kind: spec_drift` 阻塞项已处理（不得带阻塞推进新 feature）
- [ ] `plan-delta-merge-protocol.md §3` Merge Queue 已装配；folded_into_ssot / promoted_to_ssot_patch 未获用户批准前只保留候选，不静默改 Authoritative SSOT
- [ ] 主 workflow §2.6 人读简报建议 `/specs-execute` 切换 + first_task ID + 风险/迁移要点提示
- [ ] `forbidden-actions.md §Phase 5 校验` Format Validation Gate 通过
- [ ] `forbidden-actions.md §Phase Exit Gate` 三件套通过（Format Gate PASS + self-check [x] + _status 已更新）
