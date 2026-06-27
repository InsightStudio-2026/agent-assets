# 规格计划、增量与合并协议 (Plan / Delta / Merge Protocol)

## 0. 定位

本文件把 `/specs-write` 的三条能力落成可执行检查：计划审查、Brownfield delta 表达、长期规格回并。它不替代 `methodology-kernel.md` 的定义，也不替代 `appendix.md §A.7` 的 Reflections GC 规则；只提供 Phase 3 / Phase 4 / Phase 5 的审查入口。

## 1. Plan Review（Phase 3 Design）

| 规则 ID (Rule ID) | 检查项 | PASS 标准 | FAIL 信号 | 处理 |
| --------- | -------- | ----------- | ----------- | ------ |
| PR-R1 | Plan Artifacts Register | design 明确列出本 feature 需要 / 不需要的 plan artifact | research / contracts / migration / devex 类产物散落或隐含 | 补 design 计划表 |
| PR-R2 | Research Boundary | 选型研究只回答当前 DSN 决策，不扩展为项目级调研 | 为未批准未来能力做大范围调研 | 回 charter / Gate B |
| PR-R3 | Data Model Plan | 涉 schema / data contract 时列出数据模型、迁移、回滚、验证锚点 | schema 变更只在实现期发现 | 补 DSN-DB / DSN-DATA |
| PR-R4 | Contract Plan | 涉 API / event / SDK / UI contract 时列出 contract source 与 drift check | 前后端 / 外部接口分别手写 | 补 DSN-API / DSN-UI / type_ssot |
| PR-R5 | Migration Plan | `Relation to Existing: Replaces` 或 `DSN-DB Migration Strategy` 非 N/A 时有 migration plan | 只写“迁移数据”无 dry-run / rollback | 回 design-rules |
| PR-R6 | DevEx Plan Artifact | 若需要上手或运行说明，只登记为独立的 plan artifact | 新增教程化 spec | 路由 `/developer-experience-audit` |

### 1.1 Plan Artifacts Register 格式

| 交付产物 (Artifact) | 是否必需 (Required) | 所有者阶段 (Owner Phase) | 目标路径 (Target Path) | 验证依据 (Verification) |
| ---------- | ---------- | ------------- | ------------- | -------------- |
| research | Yes / No | Phase 3 | `<feature>/artifacts/research/*.md` | decision linked to DSN-* |
| data-model | Yes / No | Phase 3 | `<feature>/artifacts/data-model/*.md` | drift / migration check |
| contracts | Yes / No | Phase 3 | `<feature>/artifacts/contracts/*.md` | contract test / type drift |
| migration-plan | Yes / No | Phase 3 | `<feature>/artifacts/migration/*.md` | dry-run / rollback |
| devex-note | Yes / No | Phase 5 | `<feature>/artifacts/devex/*.md` | `/developer-experience-audit` if needed |

## 2. Delta Review（Phase 2-4）

| 规则 ID (Rule ID) | 检查项 | PASS 标准 | FAIL 信号 | 处理 |
| --------- | -------- | ----------- | ----------- | ------ |
| DR-R1 | Delta Operation 明确 | REQ / NFR / DSN / TASK 均能落到 Add / Modify / Replace / Deprecate / Preserve / Merge Back / Archive Only | “优化 / 改一下 / 兼容一下”无枚举 | 补字段 |
| DR-R2 | Existing Anchor | Modify / Replace / Deprecate / Preserve 均引用 EXIST-* 或 SSOT 锚点 | Brownfield 写成 Greenfield | 回 Phase 1.5 |
| DR-R3 | Conflict Resolution | `Conflicts EXIST-*` 有解决方向并转成正式 delta | 只罗列冲突 | Gate B 或回 audit |
| DR-R4 | Deprecation Window | Deprecate 有 owner、删除条件、验证方式、清理 Task | 兼容层无退出条件 | 拒绝 Approved |
| DR-R5 | Preserve Justification | Preserve 说明为什么不动及其验证边界 | “保持不变”无原因 | 补 audit/design |
| DR-R6 | Task Delta Projection | tasks.md 每个 Task 的 Relation to Existing 与上游 REQ / DSN delta 不冲突 | REQ Replace 但 Task 写 Net New | 修 tasks / traceability |

### 2.1 Delta Projection 表

| 事实源类型 (Source) | 增量操作 (Delta) | 必需下游投影 (Required Downstream Projection) |
| -------- | ------- | -------------------------------- |
| REQ Add | Add | Task 可 Net New；Design 可 Net New |
| REQ Modify | Modify | Task 必引用 Existing Touches 或 Reuse Notes |
| REQ Replace | Replace | Design 必有 migration / failure strategy；Task 必有 Revert Command |
| REQ Deprecate | Deprecate | Task 必有 cleanup / validation；兼容窗口必须可删除 |
| REQ Preserve | Preserve | Task 不得改对应 EXIST-*，除非回 Gate B 改 delta |
| Reflection Merge Back | Merge Back | Phase 0 / Phase 5 进入 merge-back queue |

## 3. Long-Term Spec Merge（Phase 5 Handoff + 下一轮 Phase 0）

| 规则 ID (Rule ID) | 检查项 | PASS 标准 | FAIL 信号 | 处理 |
| --------- | -------- | ----------- | ----------- | ------ |
| MB-R1 | Merge Queue | handoff-payload 中 implementation_reflections.active 可进入 merge-back queue | reflection 存活但无 resolution 候选 | 补 Reflections |
| MB-R2 | Resolution 明确 | 每条候选 reflection 有 resolution、target、approval requirement | 只写“后续优化” | 拒绝 closeout |
| MB-R3 | Authoritative Boundary | folded_into_ssot / promoted_to_ssot_patch 未获批准前只写候选 | 静默改母本 / L1 SSOT | Gate A/B |
| MB-R4 | Archive Separation | feature 内 reflections-archive 不反流全局；delivery-log.md 只引用概要 | 归档内容反向成为新事实源 | 纠正归档 |
| MB-R5 | Active Cleanup | 已裁决 reflection 同 PR 从 YAML 物理删除并追加 archive | 只改 status 或 YAML/archive 同 ID 重复 | 回滚 GC |
| MB-R6 | Next Feature Preflight | 下一轮 Phase 0 先扫未裁决 high / medium+ reflection | 带阻塞反流继续开新 feature | BLOCKED |

### 3.1 Merge Queue 表

| Reflection ID | Kind | Severity | Resolution Candidate | Target | Approval Required | Next Action |
| --------------- | ------ | ---------- | ---------------------- | -------- | ------------------- | ------------- |
| REF-### | implementation_choice / new_invariant_candidate / reusable_pattern / spec_drift / audit_debt / ssot_stewardship | low / medium / high | promoted_to_invariant / distilled_to_standards / folded_into_spec / folded_into_ssot / promoted_to_ssot_patch / dismissed | `<path>#<anchor>` | Yes / No | Gate / patch / archive |

## 4. Phase 挂接表

| Phase | 必跑规则 | 输出 |
| ------- | ---------- | ------ |
| Phase 2 Requirements | DR-R1 / DR-R2 / DR-R3 / DR-R4 / DR-R5 | REQ / NFR delta 不漂移 |
| Phase 3 Design | PR-R1~PR-R6 + DR-R1~DR-R5 | Plan Artifacts Register + DSN delta |
| Phase 4 Tasks | DR-R6 + Delta Projection | Task delta 与上游一致 |
| Phase 5 Handoff | MB-R1~MB-R6 | Merge Queue + handoff / closeout 风险提示 |

## 5. 禁止动作

| 禁止项 | 原因 |
| -------- | ------ |
| 不用 plan artifact 绕过 `artifacts/` 路径 | 执行期副产物必须落 spec artifacts |
| 不把兼容层写成 Preserve | 兼容层是迁移窗口，必须有退出条件 |
| 不静默回并 Authoritative SSOT | folded_into_ssot / promoted_to_ssot_patch 必须用户批准 |
| 不把 delivery-log.md / done/ 当新 SSOT | 归档只读，不反流 |
