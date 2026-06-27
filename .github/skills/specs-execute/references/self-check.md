# Specs Execute  Per-Phase Self-Check Lists

> **When to read**: The main workflow instructs Cascade to load and tick this file's checklist at the end of each Phase (Locate / Hydrate / Plan / Red-Green-Refactor / Verify / Update).
>
> Cross-references point to local companion documents unless explicitly marked as main workflow.

---

## 1. 自检清单（每 Phase 结束前自检）

### 1.1 Locate 自检

- [ ] 目标 TASK-ID 已确认
- [ ] 若用户提供失败测试、CI 红灯、bug-audit handoff 或专项 workflow mitigation task，已读取 `specialized-triggers.md` 并完成 Failure Readback；未读失败原文不得改代码
- [ ] 上游 Spec 全部 Approved
- [ ] **上游 Spec 的 Approval Notes 均包含有效批准留痕**（2 型二选一 · 详 `phase-rules.md §1.1` 第 10 项）：用户 Gate 型 = `>` 引用块 + 原话明示同意 + 时间戳；AI-DRI auto-approved 型 = 4 行结构（`AI-DRI auto-approved` / `Gate Check` / `Evidence` / `Timestamp` 全备）。仅状态字符串 / 仅 1 行 auto-approved 字串缺其他三行 / 用户话未含明示同意词 → 均视为伪留痕，拒推进
- [ ] maturity-intake.md 已通过：Decision = PROCEED_TO_CHARTER；SSOT Health 不为 Needs Repair / Unfit As Source；Seed / Greenfield 有 Baseline / Greenfield Survey evidence 与 Future Audit Trigger
- [ ] Hybrid/Brownfield audit.md 已通过 Audit Depth Gate：14 面覆盖完整、12 个基础面的细项证据逐项列出、真实数据库 readback 存在、文档 SSOT Survey 存在、Overall Confidence ≥ 80%、**两个强证据面（真实数据库面 / 文档 SSOT 面）confidence 各自 ≥ 80%**、Blocking Unknowns = none（任一项失守即拒进 Hydrate，回切 `blocking-and-rollback.md §1.3`）
- [ ] handoff-payload.yaml 存在则已读取作为 Context 注入起点，并已查看 `traceability` 节并与 tasks.md 顶部 Markdown 表格交叉核对（冲突以 YAML 为准）
- [ ] **`audit.md#EXIST-DSN-*` 的 `Verified By:` 时间戳起 ≤ 7 天**；超期 → 调用运行时工具重检现状（走 4 项格式 + audit-evidence/ · 防 4）后再推进
- [ ] **attention_budget_check（防 5）**：已估算 Prompt 总 token 数（0-200k → 可P1；200k-300k → 仅 P0；>300k → 超载告警 + Intake 明言）；P0 节超上限（普通 5 / 跨边界·动凭据 7）→ 停下报告建议拆 Task
- [ ] 前序依赖已 Done
- [ ] Task 头部七项执行必需字段齐全（`phase-rules.md §1.1` 第 9 项：Implements / Design Refs / Touches / Existing Touches / Reuse Notes / Verification Commands / Context Required Before Execution；Seed / Greenfield 可 N/A 的字段除外；完整 22 项字段清单详写端 `task-rules.md §1`）
- [ ] **`suspended_state` 节存在性检查(`blocking-and-rollback.md §1.6`)**:若 handoff-payload.yaml 含 `suspended_state` 节 → **跳过常规 Locate**,直接走 `blocking-and-rollback.md §1.6.3` Resume 三件套(Locate · Restore · Resume);Status=Blocked(Suspended) 但 `suspended_state` 缺失 → 视为非法中断,停下追问用户

### 1.2 Hydrate 自检

- [ ] **P0 / P1 分级读取完成（防 5）**：p0_essential / p1_reference 二者都加载进上下文（除非 attention_budget 超载启动 P0-only）；P0 逐条复述原文 ≥ 1 句；P1 在后续 Phase 补读者在 Execution Notes 记录原因
- [ ] 所有 `Context Required` 锚点均已复述原文
- [ ] 复述后能说出任务与需求 / 设计的对应关系
- [ ] **跨边界 Task 复述中包含对应 DSN 的 Failure Strategy 原文**（超时 / 崩溃 / 数据层错误三类中与本 Task 相关的条目）
- [ ] **跨边界 DSN 填了 `Concurrency & Lock` 的 Task 复述了该节原文**（并发模型 + 退避参数 + 检测信号 1-2 句）
- [ ] **涉及依赖选型 / 部署形态 / 跨进程 / 跨网络 / 跨服务 / 跨 LLM 的 Task 复述了适用 INV-BAN-* / INV-LIM-* / INV-SEC-***的 rule + scope 原文 1 句；**涉凭据 / API Key / PII / 跨网域 / 交易类 Task 必复述适用 INV-SEC-* 原文**- [ ] 无锚点失效或语义模糊

### 1.3 Plan 自检

- [ ] 子步骤分解清晰
- [ ] Touches 在 Spec 范围内
- [ ] Verification Commands 已展开为可执行命令
- [ ] Verification Commands 中脚本输出参数已传 spec artifacts 路径，不依赖默认值（tasks.md `Artifacts:` 声明路径作为唯一输出目的地）
- [ ]**DB Test Isolation 三要素与 tasks.md `## 4. Test Plan` 节声明一致**：(a) 隔离机制 / (b) 副作用边界 / (c) 不再测后留垃圾，实际命令与 spec 声明不一致 → 停下追问是修命令还是修 Spec（详写端 `task-rules.md §1`）
- [ ] **Concurrency & Lock 的 DSN 均实际存在验证命令 或 Execution Notes 说明豁免理由**
- [ ] Pause-and-Ask 白名单命中项已获用户明确批准；未命中则 AI-DRI 已自决推进

### 1.4 Red-Green-Refactor 自检

- [ ] Red 测试已写并确认失败
- [ ] 若已有失败测试作为 Red，已按 `specialized-triggers.md §3` 分类并确认与 REQ / AC / DSN / EXIST / INV 锚点一致；unrelated / env failure 未被当作 Red
- [ ] Green 实现最小化
- [ ] 每行 diff 可追溯到 REQ / DSN / EXIST-*/ INV-*
- [ ] **diff 中无任何截断 / 占位标记**：grep `// \.\.\.|# \.\.\.|<填入|<原有|rest unchanged|existing code` 均为空
- [ ] **未引入 charter.md §5 INV-BAN-* 禁用依赖**（import / package.json / requirements.txt / docker-compose / nssm 服务定义等需走查）
- [ ] **`phase-rules.md §4.2` [TDD-Lock] 声明已输出且 hash 已回填两处（防 2）**：tasks.md `Test Anchors` + handoff-payload `first_task.test_anchors` 均填入 64 位 SHA-256；例外走 N/A 者在 Execution Notes 明言
- [ ] **`phase-rules.md §5.2` 测试冻结令（防 2）**：Phase 5 Green 未动 Test Anchors 所列测试文件；主 workflow §5.1 后重算 hash 与 `phase-rules.md §4.2` 锁定值一致
- [ ] **`phase-rules.md §6.1` Refactor 改测试重锁（防 2）**：如本 Phase 动了测试 → 同步重算 hash + tasks.md/payload 两处同步 + `Reflections` 以 `kind: test_modified` 留痕三项全
- [ ] Refactor（如有）未改变行为
- [ ] 全量测试 PASS

### 1.5 Verify 自检

- [ ] Verification Commands 全部 PASS
- [ ] DoD 三闭环（ATDD / BDD / TDD）均满足
- [ ] **Secret-scan（条件化）**：如 charter §5 中适用于本 Task 的 `INV-SEC-*` 非空且本 Task 动凭据/第三方 API 客户端/.env/遥测路径/凭据轮转 → tasks.md `Verification Commands` 已列出 secret-scan 命令且 0 告警；tasks.md 未列出 → 视为写端 `task-rules.md §1` 契约违规，回切 `blocking-and-rollback.md §1.3`；豁免者在 Test Plan + Execution Notes 双点明言理由
- [ ] **Migration Strategy 一致性验证（条件化）**：如 design.md 对应 `DSN-DB-*` 的 `Migration Strategy` 非 N/A → 已按策略走一致性校验（双写 diff / 阶段验证 / down dry-run + 表行数不变）且 PASS；本 Task `Revert Command` 是业务可回路径而非纯物理丢数据型
- [ ] **Test Anchors hash 校验（防 2）**：对 Test Anchors 所列文件重算 SHA-256 与 `phase-rules.md §4.2` 锁定值一致；不一致且 `Reflections:` 未以 `kind: test_modified` 声明 → 拒 PASS
- [ ] **失败契约 readback（防 5）**：凡本 Task 动了跨边界 DSN 者已逐字复述 critical_contracts[本 Task DSN].failure_strategy 三类故障原文 + 以 `<file>:<line>` 指到实现代码；冷路径/本地 Task 豁免者在 Execution Notes 明言
- [ ] tasks.md Artifacts: 声明的路径全部存在且无外溢；项目根通用目录无本 spec 散落产物
- [ ] **跨端类型契约 drift check（条件化）**：如 handoff-payload.yaml `type_ssot` 非空且本 Task 动了任一 DSN 的 type SSOT / generated_side / regen 脚本 → tasks.md `Verification Commands` 已列出 `drift_check` 命令且 0 告警；tasks.md 未列出 drift_check 命令但本 Task 命中场景 → 视为写端 `design-rules.md §1` 契约违规（"严禁两端分别手写结构体"），回切 `blocking-and-rollback.md §1.3` `/specs-write` 补 drift_check 命令后重启 Phase；`type_ssot` 节为空时本项 N/A
- [ ] 回归测试未破坏

### 1.6 Update 自检

- [ ] tasks.md Status 已更新
- [ ] Execution Notes 已追加
- [ ] Execution Notes 已记录本次 Artifacts Generated 路径清单
- [ ] **`tasks-md-schema.md §3` 实现反流闭环必答六问已交卷**：implementation_choice / new_invariant_candidate / reusable_pattern / spec_drift / audit_debt / ssot_stewardship 逐项走过；本 Task 有反流产出 → tasks.md `Reflections:` 与 handoff-payload `implementation_reflections:` 同 PR 同步写入；本 Task 无产出 → `Reflections: N/A` + Execution Notes 一句说明
- [ ] **Existing Touches 扩展回流子结构（`tasks-md-schema.md §3.1` 第 5 问子场景）**：若本 Task 因 `Existing Touches` AI-DRI 自动追加 ≥ 2 个公共契约相关文件触发 → 对应反思 `kind=audit_debt` 已填 `extension_payload` 子结构（task / added_files / reason / public_contract_impact 四字段齐备；`added_files` ≥ 2 项；与写端 §A.7.5 schema 严格对齐）；缺该子结构 → 拒进 Phase 9
- [ ] **硬触发回切检查（`tasks-md-schema.md §3.4`）**：若出现 `kind: spec_drift` 且 `severity: high` / `kind: audit_debt` 且 `severity ∈ {medium, high}` 或缺失真实数据库面 / 文档 SSOT 面证据 / `kind: ssot_stewardship` 且 `severity: high` 或需改 Authoritative SSOT 才能继续 / `kind: new_invariant_candidate` 且推荐上升为 INV-BAN-*/ INV-SEC-* / `Existing Touches` AI-DRI 自动追加 ≥ 2 个公共契约相关文件（伴 extension_payload 子结构） / Task 失败因“原 Spec 不可行”—— 不走 Phase 9 常规 Handoff，改走 `blocking-and-rollback.md §1.3` 回切 `/specs-write`
- [ ] **Traceability Matrix 双源同步·脚本单向生成（防 1）**：覆盖关系变动 → 先改 `handoff-payload.yaml#traceability`，走项目层注入的脚本槽位 `traceability_regen_script` 重生 tasks.md §1 表格，补跑 `traceability_check_script` 验证同步。手改单元格 · 脚本未跑 · check 返回非 0 都 → 拒进 Phase 9
- [ ] **Conditional Revert 预检（防 3）**：如本 Task 需跳 Revert，已先跑 `git diff --quiet<revert_target>..HEAD -- <shared_files>` 预检；exit code != 0 → 未自动 Revert，Status 改 Blocked 升级全局 Rollback Plan
- [ ] 如 Pause-and-Ask 白名单命中，已获用户明确批准；未命中则已记录 AI-DRI 自决依据
