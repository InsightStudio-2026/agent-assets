---
name: repo-agent-setup
description: 仓库级代理运行环境初始化；建立 issue tracker、流程标签词表与领域文档读取规则，让后续项目流程拥有统一上下文。Use when setting up agent runtime for a repo, initializing issue tracker/labels, establishing doc reading rules, or says 代理初始化/环境搭建/仓库配置/Issue 初始化。
---


# /repo-agent-setup · 代理环境初始化

**定位**：为一个仓库建立代理运行所需的基础上下文。

**边界**：只初始化仓库协作约定、`AGENTS.md` 与 `docs/agents/` 说明文件；不写业务代码，不创建 feature spec，不替代 `/project-inception`、`/specs-write` 或 `/project-steward`。

**斜杠命令**：`/repo-agent-setup`

---

## 懒加载契约

- **MUST read**: `./decision-matrix.md`
- 开始判定或执行 Phase 流程前，必须完整懒加载上述细节。

---

## 1. 阶段 1 — 探索

读取现状，不假设：

- `git remote -v` 与 `.git/config`：判断远端平台。
- `AGENTS.md` / `AGENTS.md`：Windsurf 原生 always-on rule 文件（**首选权威**）。
- `AGENTS.md`：仅作向后兼容信号；存在时需要迁移到 `AGENTS.md`。
- `CONTEXT.md` / `CONTEXT-MAP.md`：判断领域文档布局；缺失不自动等于错误，agent assets 仓库尤其不要求存在。
- `docs/adr/` 与各子域 `docs/adr/`：判断 ADR 位置；缺失不自动等于错误。
- `docs/agents/`：判断是否已有配置。
- `.scratch/`：判断是否已有本地 markdown issue 约定。

输出现状摘要：

```markdown
## Setup Findings

- Agent instruction file: <AGENTS.md exists | only AGENTS.md exists | neither>
- Issue tracker evidence:
- Existing label vocabulary:
- Domain docs layout:
- Missing files:

```

若仅检测到 `AGENTS.md` 而无 `AGENTS.md`，在 Findings 下加一条 `Migration needed: AGENTS.md → AGENTS.md`。

---

## 2. 阶段 2 — 决定 Issue 追踪工具

一次只处理一个决策。

默认规则：

- GitHub remote → 推荐 GitHub Issues。
- GitLab remote → 推荐 GitLab Issues。
- 无远端或用户偏好本地 → 推荐 local markdown。
- Jira / Linear / 其他 → 让用户用一段话描述实际流程。

候选：

- **GitHub**：issues 在 GitHub Issues，通常用 `gh`。
- **GitLab**：issues 在 GitLab Issues，通常用 `glab`。
- **Local markdown**：issues 是仓库内 `.scratch/<area>/` 的 markdown 文件。
- **Other**：按用户描述记录为自由文本。

写入草案：

```markdown
## Issue Tracker

## Provider
<GitHub | GitLab | Local markdown | Other>

## Read
<how to list and read issues>

## Write
<how to create, comment, label, close>

## Safety
<actions requiring confirmation>
```

---

## 3. 阶段 3 — 制定标签词表

标准角色分两类。

Category：

- `bug`
- `enhancement`

State：

- `needs-triage`
- `needs-info`
- `ready-for-agent`
- `ready-for-human`
- `wontfix`

要求用户确认真实标签字符串。若仓库没有既有标签，使用标准名。

写入草案：

```markdown
## Triage Labels

## Category Labels

- bug: <actual label>
- enhancement: <actual label>

## State Labels

- needs-triage: <actual label>
- needs-info: <actual label>
- ready-for-agent: <actual label>
- ready-for-human: <actual label>
- wontfix: <actual label>

## Conflict Rule
Each issue should have exactly one category label and one state label.
```

---

## 4. 阶段 4 — 部署领域文档目录

确认或建议领域文档模式：

- **Single-context**：仓库根可有一个 `CONTEXT.md`，ADR 可放在 `docs/adr/`。
- **Multi-context**：根可有 `CONTEXT-MAP.md`，指向各子域 `CONTEXT.md` 与 ADR 目录。
- **None yet**：尚无领域词表或 ADR；记录为未建立，不自动创建，后续由 `/grill-with-docs` 按需产出。

写入草案：

```markdown
## Domain Docs

## Layout
<single-context | multi-context | none-yet>

## Glossary Sources

- <paths>

## ADR Sources

- <paths>

## Read Rule
Read the relevant glossary and ADRs before proposing domain or architecture changes.

## Update Rule
Do not rewrite authoritative domain docs without explicit approval.
```

---

## 5. 阶段 5 — 变更核实

展示即将写入的内容：

- 代理说明文件中的 `## Agent operating context` 区块（写入 `AGENTS.md`）。
- `docs/agents/issue-tracker.md`。
- `docs/agents/triage-labels.md`。
- `docs/agents/domain.md`。

若存在迁移动作，单独列出：

- `AGENTS.md → AGENTS.md` 内容迁移与 `AGENTS.md` 处置（删除 / 保留为 stub link）。

让用户确认后再写。

代理说明区块模板：

```markdown
## Agent operating context

### Issue tracker
<one-line summary>. See `docs/agents/issue-tracker.md`.

### Triage labels
<one-line summary>. See `docs/agents/triage-labels.md`.

### Domain docs
<one-line summary>. See `docs/agents/domain.md`.
```

---

## 6. 阶段 6 — 写入执行

### 6.1 代理说明文件选择

`AGENTS.md` 是 Windsurf 原生 always-on rule（仓库根的 `AGENTS.md` 自动注入到每条消息的系统 prompt）。固定优先级：

1. 若 `AGENTS.md` 存在 → 原地更新它。
2. 若仅 `AGENTS.md` 存在 → **迁移**：把 `AGENTS.md` 内容搬到新建的 `AGENTS.md`，再按用户偏好决定 `AGENTS.md` 处置：
   - **删除**：默认选项；最干净。
   - **保留为 stub**：`AGENTS.md` 替换为单行 `See AGENTS.md.`，方便仍用 Claude Code 直连仓库的人。
3. 若两者都不存在 → 选择 `AGENTS.md` 作为目标文件，不再询问目标文件选择；仍须先经过 §0.3 的 `/repo-agent-setup:READY_TO_WRITE` 确认门后才能创建。
4. 若两者同时存在 → 以 `AGENTS.md` 为权威；提示用户 `AGENTS.md` 可能漂移，建议同上处置。

### 6.2 写入规则

- 已有 `## Agent operating context` 时原地更新，不追加重复区块。
- 不覆盖周边用户内容。
- 创建或更新 `docs/agents/issue-tracker.md`、`docs/agents/triage-labels.md`、`docs/agents/domain.md`。
- 对 Other issue tracker，把用户描述保留为权威文本。
- 任一写入失败时，立刻停止后续写入并判定 `/repo-agent-setup:WRITE_BLOCKED` 或 `/repo-agent-setup:PARTIAL_WRITTEN`；不得追加重复区块补救。
- `AGENTS.md` 迁移或处置失败时，判定 `/repo-agent-setup:MIGRATION_BLOCKED`，不得同时维护两份互相漂移的代理说明。

---

## 7. 阶段 7 — 完工汇报

输出：

```markdown
## 代理运行上下文配置报告 (Repo Agent Setup Report)

## 工作流状态 (Workflow State)

- State: /repo-agent-setup:<STATE>; common examples: /repo-agent-setup:DONE | /repo-agent-setup:REPORT_ASSET_CONTEXT_GAPS | /repo-agent-setup:PARTIAL_WRITTEN | /repo-agent-setup:WRITE_BLOCKED | /repo-agent-setup:MIGRATION_BLOCKED

## 配置结论 (Outcome)

- <Asset repo no-op | Asset context gaps | Written | Partial written | Blocked>

## 权威信息与事实源 (Authority / Fact Source)

- 代理指令事实依据 (Agent instruction authority): <AGENTS.md / asset repo files>
- 追踪系统配置依据 (Tracker config authority): <docs/agents/issue-tracker.md or N/A>
- 标签词表配置依据 (Label vocabulary authority): <docs/agents/triage-labels.md or N/A>
- 领域文档配置依据 (Domain docs authority): <CONTEXT.md / docs/adr / N/A>

## 授权边界 (Authorization Boundary)

- 路由动作 (Route Action): <WAIT_FOR_USER | CONFIRMED_ACTION | REPORT_AND_STOP>
- 授权来源 (Confirmation source): <N/A for asset repo no-op | user approval quote>
- 授权范围 (Authorized scope): <exact AGENTS.md / docs/agents/* / AGENTS.md migration writes>
- 未授权范围 (Not authorized): <business code / feature spec / tracker external write / downstream workflow execution>

## 已配置写入 (Written)

- <变动文件清单 (files)>

## 甄别与对齐决策 (Decisions)

- 追踪系统类型 (Issue tracker):
- 标签与词表 (Label vocabulary):
- 领域文档布局 (Domain docs layout):

## 下一步推荐路由 (Next Recommended Route)

- /project-steward

```

---

## 8. 禁用行为

- 不把 `AGENTS.md` 当作权威代理说明文件；它只是向后兼容信号。
- 不在已有 `AGENTS.md` 时同时维护一份独立 `AGENTS.md`（避免漂移）。
- 不追加重复代理上下文区块。
- 不创建 issue tracker 标签，除非用户要求。
- 不猜测 Jira / Linear 等外部流程。
- 不静默修改 Authoritative SSOT。
- 不把仓库初始化扩展成 feature 规划。

## 9. 快速自检清单

报告前自检：

- [ ] 是否已读取并明确了现有的 `AGENTS.md` / `AGENTS.md` 及领域文档布局？
- [ ] 针对 Issue Tracker 的选型与分发是否提供了合理论证与默认规则？
- [ ] 流程标签（Category 与 State）是否与项目实际词表相匹配？
- [ ] 写入 `AGENTS.md` 前，是否已向用户展示了待写入的 Agent Operating Context 差异？
- [ ] 若存在 `AGENTS.md` 迁移，是否已确认旧文件的删除或 stub 保留方式？

## 支撑资源

- [decision-matrix.md](./references/decision-matrix.md)
