---
name: tasks-to-issues
description: 将已批准的任务清单发布到 issue tracker；优先消费 /specs-write 的 tasks.md，按依赖顺序创建可独立领取的 issue。Use when user wants to publish tasks as issues, convert task list to GitHub issues, or says 发布Issue/任务转Issue/创建Issue。
---


# /tasks-to-issues · 任务发 Issue

**定位**：把已批准的任务清单导出到 issue tracker，便于外部协作与 AFK 执行者领取。

**边界**：只发布 issue，并在源任务明确允许时可回填 external references；不重新设计需求、不重拆项目范围、不替代 `/specs-write` 的任务拆分权威，不管理 issue 后续状态，不改任务执行状态或 Execution Notes。

**斜杠命令**：`/tasks-to-issues`

---

## 懒加载契约

- **MUST read**: `./decision-matrix.md`
- 开始判定或执行 Phase 流程前，必须完整懒加载上述细节。

---

## 伴随文档

| 文档 | 角色 | 何时读 |
| ------ | ------ | -------- |
| `protocols/risk-label-protocol.md` | risk:*/ needs:* / afk-* 标签、AFK/HITL 判定依据、Gate Required 映射 | Phase 2-5 |

---

## 1. 阶段 1 — 数据源评估

**MUST read**`protocols/risk-label-protocol.md`。

优先输入：

- `/specs-write` 产出的 `docs/specs/active/<feature>/tasks.md`。
- 已批准的 handoff payload。
- 用户提供的 approved plan。

用户提供的 approved plan 只有同时包含批准来源、父范围 / 目标、可发布 work items、验收或 Verification、依赖或顺序、tracker 目标时才算源任务。缺任一项则为 `/tasks-to-issues:SOURCE_MISSING`。

如果只有模糊想法、未批准需求或不满足最低事实源的 plan，分流到 `/specs-write`，不得直接发布 issue。

必须确认：

```markdown
## Source

- Source path / URL:
- Approval status:
- Feature / parent scope:
- Issue tracker config:

```

若 `docs/agents/issue-tracker.md` 或 `docs/agents/triage-labels.md` 缺失，状态为 `/tasks-to-issues:NO_TRACKER_CONFIG`，先分流到 `/repo-agent-setup`。

若源任务已有 external references，或 tracker 中能确认已有对应 issue，状态为 `/tasks-to-issues:ALREADY_PUBLISHED`，只报告映射并收束到 `/tasks-to-issues:DONE`，不重复创建。若存在疑似重复但无法确认，状态为 `/tasks-to-issues:DUPLICATE_RISK`，停下让用户裁决。

---

## 2. 阶段 2 — 任务项解析**MUST read**`protocols/risk-label-protocol.md`

从任务源提取：

- ID。
- 标题。
- 目标行为。
- 上游 requirement / design anchors。
- dependencies。
- touched domains。
- verification commands。
- artifacts。
- rollback notes。
- risk anchors / NFR / Gate Required。
- current status。
- existing external references。

只发布 `Pending` 或用户指定的任务。默认不发布 `Done`。

---

## 3. 阶段 3 — 切片质量核验**MUST read**`protocols/risk-label-protocol.md`

每个 issue 必须是可独立领取的纵向切片。

合格标准：

- 有用户可见或系统可验证的完成结果。
- 有明确验收标准。
- 依赖关系明确。
- 不只是“改 DB”、“写 API”、“做 UI”这种水平层切片。
- 不依赖执行者读取整套背景才能知道做什么。

若任务过大：建议回 `/specs-write` Phase 4 拆分，而不是在本 workflow 私自重拆权威任务。

若任务过小：可以建议合并，但必须回源文件确认，不在 issue tracker 里另起事实源。

---

## 4. 阶段 4 — 草拟 Issue 集合**MUST read** `protocols/risk-label-protocol.md`

按依赖顺序草拟 issue。

每项展示：

```markdown
## Draft Issue `<n>`

- Source task:
- Title:
- Type: <AFK | HITL>
- Risk labels: <risk:* / needs:* / afk-*>
- AFK/HITL rationale:
- Gate Required: <workflow or N/A>
- Blocked by:
- Summary:
- Acceptance criteria:
- Verification:

```

分类规则：

- **AFK**：上下文完整、验收清楚、无外部权限、无重大裁决。
- **HITL**：需要产品、架构、UI、生产、账号、外部协调或高风险判断。
- Risk labels 按 `protocols/risk-label-protocol.md` 判定；每个 issue 至少标 `afk-safe` 或 `afk-unsafe`，命中安全 / 数据 / 发布 / 性能 / UX 风险时必须同时标 `risk:*`，需要人类裁决或生产权限时必须标 `needs:*`。

让用户确认粒度、依赖、AFK/HITL 标记。未经确认不发布；确认后进入 `/tasks-to-issues:CONFIRMED_TO_PUBLISH`。

---

## 5. 阶段 5 — 发布 Issue

**MUST read** `protocols/risk-label-protocol.md`。

按 blockers first 顺序创建 issue。

发布前必须重新执行 duplicate guard：若源任务已有 external references，或 tracker 中出现疑似重复 issue，立即进入 `/tasks-to-issues:ALREADY_PUBLISHED` 或 `/tasks-to-issues:DUPLICATE_RISK`，不得继续批量创建。

Issue body 模板：

```markdown
## Parent
<parent spec / epic / issue reference>

## Source (2)
<source task ID and approved spec path>

## Risk Labels

- <risk:* / needs:* / afk-*>

## AFK/HITL Rationale
<why this is AFK-safe or AFK-unsafe>

## Gate Required
<specialized workflow route or N/A>

## What to build
<end-to-end behavior, not layer-by-layer instructions>

## Acceptance criteria

- [ ] <criterion>
- [ ] <criterion>

## Verification

- <command or manual check>

## Blocked by

- <issue reference or None>

## Out of scope

- <boundaries>

```

发布后只应用初始协作元数据：

- category label。
- initial state label：`ready-for-agent` 或 `ready-for-human`；后续状态流转归 `/issue-triage`。
- parent / dependency references。

---

## 6. 阶段 6 — 反填 Issue 引用关联

**MUST read** `protocols/risk-label-protocol.md`。

如果源任务明确允许记录 external references，且回填位置可确认，进入 `/tasks-to-issues:BACKFILL_SAFE_TO_APPLY`，把创建出的 issue URL 回填到任务的 External References / References 区域。

回填前必须确认源文件允许记录 external references；不能确认时进入 `/tasks-to-issues:BACKFILL_CONFIRMATION_REQUIRED`，不改源文件，只在报告中列映射，除非用户明确确认回填位置。不得改 `Status` / `Execution Notes`。

若源任务没有规定回填位置，不改源文件，只在对话报告中列出映射。

映射格式：

```markdown
## Issue Mapping

- TASK-001 → #123
- TASK-002 → #124

```

---

## 7. 阶段 7 — 完工汇报

输出：

```markdown
## 任务发布至 Issue 报告 (Tasks To Issues Report)

## 工作流状态 (Workflow State)

- State: /tasks-to-issues:<STATE>; common examples: /tasks-to-issues:DONE | /tasks-to-issues:PARTIAL_PUBLISHED | /tasks-to-issues:BACKFILL_CONFIRMATION_REQUIRED | /tasks-to-issues:PUBLISH_FAILED

## 发布结论 (Outcome)

- <Published | Already published | Partial published | Backfill skipped | Publish failed>

## 已发布任务 (Published)

- <issue list>

## 风险标签汇总 (Risk Label Summary)

- <风险标签数量统计，以及 afk-safe / afk-unsafe 统计>

## 未发布任务 (Not Published)

- <跳过的任务及原因>

## 事实源完整性 (Source Integrity)

- 源文件是否改变 (Source changed): <yes | no>
- 是否已回填关联信息 (Backfilled references): <yes | no>

## 权威信息与事实源 (Authority / Fact Source)

- 源任务授权依据 (Source task authority): <tasks.md / handoff / approved plan>
- 追踪系统发布依据 (Tracker issue authority): <provider issue IDs / URLs>
- 追踪系统状态维护 (Tracker state owner): /issue-triage

## 授权边界 (Authorization Boundary)

- 路由动作 (Route Action): <WAIT_FOR_USER | CONFIRMED_ACTION | REPORT_AND_STOP | CONTINUE_IN_WORKFLOW>
- 授权来源 (Confirmation source): <N/A for report only | user approval quote>
- 授权范围 (Authorized scope): <exact issue creation set and optional backfill target>
- 未授权范围 (Not authorized): <task Status / Execution Notes changes / issue state management / downstream workflow execution>

## 推荐下一步路由 (Recommended Next Route)

- /project-steward

```

---

## 8. 禁用行为

- 不从模糊需求直接发布执行 issue。
- 不重写 `/specs-write` 的任务权威拆分。
- 不把水平层任务发布为可独立领取的 issue。
- 不在未确认依赖顺序时批量创建 issue。
- 不关闭或修改 parent issue，除非用户明确要求。
- 不在无法确认源文件允许 external references 时回填源任务。
- 不把 `/tasks-to-issues:CONFIRMED_TO_PUBLISH` 继承为回填授权。
- 不改源任务的 `Status` / `Execution Notes`。
- 不用易过期行号作为执行依据。
- 不让 issue body 成为与源 spec 冲突的第二事实源。
- 不把 `risk:*` / `afk-safe` / `afk-unsafe` 标签当专项 workflow 审计结果或真实世界副作用授权。

## 9. 快速自检清单

报告前自检：

- [ ] 是否已确认任务清单的审批状态及 Tracker 目标配置？
- [ ] 提取的任务字段（ID、依赖、验收等）是否完整正确？
- [ ] 导出的每一个 Issue 是否符合纵向切片的合格标准？
- [ ] 是否已向用户展示草稿，并确认了 AFK/HITL 及风险标签判定？
- [ ] 若进行了外链回填，是否确保该行为已获源任务的明确授权？

## 支撑资源

- [decision-matrix.md](./references/decision-matrix.md)
- [risk-label-protocol.md](./protocols/risk-label-protocol.md)
