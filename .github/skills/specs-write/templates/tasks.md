# tasks.md 模板

> **When to read**: 在 `/specs-write` Phase 4 落 tasks.md 时读取本文。

**模板说明**（落 spec 时不要复制本块进 spec）：

1. 头部 6 行（Feature Slug / Project Mode / Mode / Charter Ref / Audit Ref / Requirements Ref / Design Ref）必填，缺一项即视为模板违规。
2. `## 1. Traceability Matrix` 必出现在 Task List 之前，且加 `<!-- generated-from: handoff-payload.yaml#traceability -->`（详 `appendix.md §A.1`）。
3. `## 2. Execution Order` 必给出执行顺序与依赖说明。
4. `## 3. Task List` 中每个 Task 头部 22 字段详 `task-rules.md §1` 字段清单（主体）；字段二分 / checkbox 强制规则严格遵守。
5. `## 4. Test Plan / ## 5. Definition of Done / ## 6. Rollback Plan / ## 7. Execution Notes / ## 8. Critical Assumptions / ## 9. Approval` 不可省。
6. **项目级扩展字段（可选 · 非协议主体）**：项目实践中常补 `Goal` / `Steps` / `Task DoD` 三项以便 `/specs-execute` 实时跟踪——
   - `Goal`：一句话执行目标（**B 类 · `-` 普通**）
   - `Steps`：执行步骤序列（**A 类 · `- [ ]` checkbox**）
   - `Task DoD`：单 Task 验收点（**A 类 · `- [ ]` checkbox**）
   项目层若启用，必须遵守 `task-rules.md §1` 字段二分硬规则，不替换协议主体 22 字段；启用与否由 `project-adapter.md §1` 决定。示例见下方 Task 头部"项目级扩展示例"块。

## Tasks — `<Feature Name>`

Feature Slug: `<feature-slug>`
Project Mode: Seed / Init | Greenfield | Hybrid | Brownfield
Mode: Large | Medium (design skipped: `<reason>`) | Medium (single-file: `<reason>`)
Charter Ref: charter.md
Audit Ref: audit.md (Approved @ `<date>`) | N/A (Seed / Greenfield; see maturity-intake.md)
Requirements Ref: requirements.md (Approved @ `<date>`)
Design Ref: design.md (Approved @ `<date>`) | N/A (Medium mode)

## 1. Traceability Matrix

<!-- generated-from: handoff-payload.yaml#traceability -->
<!-- DO NOT EDIT CELLS BY HAND. Update YAML first, then regenerate this table in full. -->

| Task | Implements | Design Refs | Existing | Anti-Invariants | BDD Scenarios Owned | Artifacts |
| ------ | ------------ | ------------- | ---------- | ----------------- | --------------------- | ----------- |
| TASK-001 | REQ-001 (AC-001.1, AC-001.2) | DSN-DB-001, DSN-API-001 | Replaces EXIST-DSN-DB-003 | INV-LIM-001 | REQ-001.S1 | docs/specs/`<feature-slug>`/artifacts/reports/TASK-001_plan.json |
| TASK-002 | REQ-002 | DSN-API-002 | Net New | INV-SEC-001 | REQ-002.S1 | docs/specs/`<feature-slug>`/artifacts/reports/cost_ledger.jsonl |
| TASK-003 | constraint-verification | N/A (constraint-verification) | N/A (mode=Greenfield) | none (no applicable INV-* in scope) | — | docs/specs/`<feature-slug>`/artifacts/reports/verify_003.json |

## 2. Execution Order

1. TASK-001
2. TASK-002
3. TASK-003

（说明顺序依赖原因，例如 DB → Repository → API → UI）

## 3. Task List

### TASK-001: <动词 + 对象>

- Phase: 1 of N
- Type: feature | refactor | migration | hotfix | docs
- Priority: P0 | P1 | P2
- Status: Pending | In Progress | Done | Blocked | Blocked(Suspended)    # 5 选 1；`Blocked(Suspended)` 仅 P-SIBLING / P-CROSS 抢占现场使用，与 `suspended_state` 节配套（§A.6.2 / §A.7.4）；机读 token 无空格
- Implements:
  - REQ-001
  - （或 `N/A (Medium mode)` / `constraint-verification`）
- Depends On: TASK-000
- Design Refs:
  - DSN-API-001
  - （或 `N/A (Medium mode)` / `N/A (constraint-verification)`）
- Derived From: SRC-002#<章节>
- Relation to Existing: Replaces EXIST-DSN-DB-003 | Extends EXIST-REQ-007 | Net New
- Touches（新建文件 · A 类 · 必须 `- [ ]`）:
  - [ ] migrations/0NNN_<名称>.sql
  - [ ] backend/models/<新模块>.py
- Existing Touches（修改 / 替换 / 删除既有锚点 · A 类 · 必须 `- [ ]`）:
  - [ ] backend/models/order.py（替换 EXIST-DSN-DB-003）
  - [ ] backend/repositories/order_repo.py（适配新 Schema）
  - 或 `N/A (mode=Greenfield)`
- Reuse Notes（B 类 · 普通 `-`）:
  - 沿用 EXIST-DSN-API-007 的中间件链
- Effort: 0.5d
- Test Anchors（B 类 · §A.2 · sha256 锁定时机详 §A.2.3）:
  - path: tests/test_order_create.py
    sha256: <Phase 4 Red 末锁定 · 64 位十六进制>
  - path: tests/contract/test_order_api.py
    sha256: <Phase 4 Red 末锁定 · 64 位十六进制>
- Verification Commands（A 类 · 必须 `- [ ]`）:
  - [ ] pytest -k "test_order_create"
  - [ ] python tools/verify_constraints.py
- Artifacts（执行期产物声明 · 写作端最小集 · 必须 `- [ ]`）:
  - [ ] docs/specs/`<feature-slug>`/artifacts/reports/plan_001.json (planner 输出)
  - [ ] docs/specs/`<feature-slug>`/artifacts/reports/verify_001.json (verify 报告)
  - [ ] docs/specs/`<feature-slug>`/artifacts/reports/cost_ledger.jsonl (LLM 调用账本，append-only)
  - [ ] docs/specs/`<feature-slug>`/artifacts/reports/quarantine_001.jsonl (隔离样本，可空)
  - 或 `N/A (no execution artifacts)` (纯重构 / 纯文档 Task)
- Revert Command:
  - 业务可回示例: python tools/migrations/cutover_rollback.py --task TASK-001 --window 7d
  - 纯新增示例: git rm `<file>` + git checkout HEAD -- `<related>`
  - N/A 示例: N/A (无副作用)
- Revert Conflict Risk（§A.3）:
  - shared_with: TASK-000  (or `N/A (no shared files with prior Done tasks)`)
  - shared_files:
    - backend/models/order.py
- Anti-Invariants（§A.5）:
  - INV-LIM-001 (charter.md `## 5` 复述: ...)
  - 或 `none (no applicable INV-* in scope)`
- Resume Strategy（条件化 · §A.6）:
  - mode: lightweight_wip_commit | wip_branch_reset
- Context Required Before Execution（P0/P1 严格二分 · §A.5）:
  - P0 Essential（上限 5 条 · 跨边界 / 动凭据 Task 上限 7 条）: DSN-API-001 (request schema 全文复述); INV-SEC-001 (charter.md `## 5` 复述); Failure Strategy (DSN-API-001: 超时=... · 进程崩溃=... · 数据层错误=...); Concurrency & Lock (DSN-API-001: ...)
  - P1 Reference: SRC-002#<章节>; audit.md#EXIST-DSN-DB-003; design.md#DSN-DB-002 Migration Strategy
- Reflections（执行端写入 · 详 §A.7）:
  - <Task Done 后由执行端补四问简版 + 任务时间区间 + 写作端裁决预期>

> **项目级扩展示例（可选 · 非协议主体 · 详本文模板说明 #6）**：项目层若启用 `Goal / Steps / Task DoD` 三扩展字段，落地形式如下，**必须**遵守 `task-rules.md §1` 字段二分硬规则：
>
> - Goal（项目扩展 · B 类 · 普通 `-`）:
>   - 把 `<feature>` 的 ORM SSOT 与真实 DB schema 对齐，并通过 12 防线
> - Steps（项目扩展 · A 类 · 必须 `- [ ]`）:
>   - [ ] 步骤 1: ORM SSOT 同步
>   - [ ] 步骤 2: 写 forward migration
>   - [ ] 步骤 3: drift 12 防线复查
> - Task DoD（项目扩展 · A 类 · 必须 `- [ ]`）:
>   - [ ] 验收点 1: 4 表存在于真实 DB（PostgreSQL MCP readback）
>   - [ ] 验收点 2: drift 12 防线 ALL GREEN
>   - [ ] 验收点 3: ORM ↔ schema.sql ↔ 真实 DB 字段名零漂移
>
> **协议自检**：项目层启用本扩展时，落 spec 后 grep `\[ \]` 命中数 = `len(Touches) + len(Existing Touches) + len(Verification Commands) + len(Artifacts) + len(Steps) + len(Task DoD)`；A 类扩展未用 `[ ]` 或 B 类扩展（如 `Goal`）误用 `[ ]` = 协议违规。

## 4. Test Plan

- 测试金字塔: 单元 / 契约 / 集成 / E2E 占比
- 工具与运行命令: pytest / vitest / playwright / ...
- DB Test Isolation（条件化必填，详 `task-rules.md §1` 三档优先级 + 三要素）:
  - tier: Tier 1 (首选 · pytest db_session rollback fixture) | Tier 2 (裸 SQL BEGIN-ROLLBACK) | Tier 3 (整库 reset · 必述为何不能用 Tier 1/2) | N/A (no DB state)
  - tier_reason: <为何选此档；Tier 3 必证为何 Tier 1/2 不可用>
  - 隔离机制: 每个测试用 SAVEPOINT + 测试结束 ROLLBACK（Tier 1 落地）
  - 副作用边界: 不动用户级生产路径；本地缓存使用 tmp_path fixture
  - 收尾断言: 测试结束 DB 状态 = 初始态；磁盘临时目录已清理

## 5. Definition of Done

- 所有 Task = Done
- 所有 Test Anchors 绿
- 所有 BDD Scenarios 通过
- INV-* 自动化校验绿（详 §A.5）
- handoff-payload.yaml 与 tasks.md 字段一致（详 §A.1）

## 6. Rollback Plan

- 数据迁移: 调用各 Task 的 `Migration Strategy` down 路径，而非 `git checkout` 物理回滚
- 部署版: 每个 Task `Revert Command` 顺序执行
- WIP 分支: 详 §A.6 wip_branch_reset

## 7. Execution Notes

- 各 Task 的开工 / 完工 / 阻塞备注；执行端 Phase 4-8 推进时增量写入
- 跨 Task 上下文复用提示
- 与 `/specs-execute` 协作时的特别注意点

## 8. Critical Assumptions Summary

- A1: <假设> · Confidence: high|mid|low · Validation: <如何验证>
- 或填 `N/A: <说明>`

## 9. Approval

- Status: Draft | Approved | Needs Changes
- Notes: <用户原话 或 AI-DRI auto-approved 留痕，详 §3.2.3>
- Timestamp: <ISO 8601>
