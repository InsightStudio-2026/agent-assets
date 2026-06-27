---
description: "Issue 分流与状态机管理工作流（/issue-triage）专属的触发判定、状态转换路由、状态权威与动作决策矩阵"
---

# Issue 分流决策矩阵（/issue-triage）

## 0. 触发判定

| ID | 前置条件 | 动作 | 下一步 | 源 |
| ---- | ---------- | ------ | -------- | ------ |
| R-IT-ENTRY-1 | 用户显式 `/issue-triage` | 启动分流 | Phase 1 | 本文件 §0 |
| R-IT-ENTRY-2 | 用户要创建 / 整理 / 关闭 / 标记 issue | 启动分流 | Phase 1 | 本文件 §0 |
| R-IT-ENTRY-3 | 用户报告 bug 且要求诊断、修复或影响面判断 | 优先分流 | `/bug-audit` | 本文件 §9 |
| R-IT-ENTRY-4 | 用户报告 bug 但只是需要记录到 tracker | 启动 intake | Phase 1 | 本文件 §4 |
| R-IT-ENTRY-5 | `/project-steward` 推荐 issue 分流 | 启动分流 | Phase 1 | 本文件 §0 |
| R-IT-ENTRY-6 | 不涉及 issue tracker 状态管理 | 不启用 | direct | 本文件 §10 |
| R-IT-ENTRY-7 | 系统状态不清、下一步推进方向不明 | 停止并重定向 | 路由至 `/project-steward` | 临界状态 1 |
| R-IT-ENTRY-8 | 缺失母本或 L1 SSOT | 停止并重定向 | 路由至 `/project-inception` | 临界状态 2 |
| R-IT-ENTRY-9 | 属于纯缺陷根因诊断（局部、具体 bug） | 停止并重定向 | 路由至 `diagnose` 技能 | 临界状态 3 |
| R-IT-ENTRY-10 | 属于新功能、新需求开发、大重构落地 | 停止并重定向 | 路由至 `/specs-write` 与 `/specs-execute` | 临界状态 4 |
| R-IT-ENTRY-11 | 逻辑简单明确且适合 TDD 验证 | 停止并重定向 | 路由至 `tdd` 技能或直接执行 | 临界状态 5 |

## 0.1 状态与路由汇总 (State / Route Summary)

| 状态 (State) | 判定 | 下一步 | Gate / DAG ID 映射 |
| ------- | ------ | -------- | --------------------- |
| `/issue-triage:NO_TRACKER_CONFIG` | 缺 `docs/agents/issue-tracker.md` 或标签词表 | 分流 `/repo-agent-setup` | 预装配 `HG-OPS-{repo}-context`（仓库级配置缺失） |
| `/issue-triage:ATTENTION_QUEUE_PRESENTED` | 已展示需处理 issue 队列，等待用户选择 | 等用户选择 | 读取 `DAG-N-TASK-*` 状态判 ready / blocked（详 PRJ-6） |
| `/issue-triage:NEW_ISSUE_DRAFT_READY` | 从对话生成的新 bug / enhancement issue 草案已完成 | 等用户确认创建 | 草案 issue body 必须显式列 owner Node ID（`DAG-N-TASK-*`）+ Gate Required 字段（PRJ-6） |
| `/issue-triage:CONFIRMED_TO_CREATE` | 用户已确认 issue 标题、正文、标签和写入目标 | 仅按确认内容创建 issue，并回读 tracker 编号 / URL | 写入 issue 时 body 必含 DAG-N-TASK-*引用；不让 issue 成为第二事实源 |
| `/issue-triage:ISSUE_CREATED` | issue 已创建并返回 tracker 编号 / URL，尚未完成后续状态判定 | 若标签齐全则进入 `/issue-triage:TRIAGE_APPLIED`，否则进入 `/issue-triage:NEEDS_TRIAGE` | issue 投影到 `DAG-N-TASK-*`；issue 编号 / URL 写入 F-N-5 Outputs |
| `/issue-triage:CREATE_FAILED` | issue 创建失败或无法确认创建结果 | 报告失败与恢复建议，不重复写入 | — |
| `/issue-triage:NEEDS_TRIAGE` | issue 未分类或缺 state label | 进入 Phase 5 | DAG-N-TASK-* 缺 F-N-9 Gate Required 字段 → 进入分类 |
| `/issue-triage:NEEDS_INFO` | 复现、期望或影响面信息不足 | 生成追问草案；回复后进入 Phase 8 | DAG-N-TASK-*标记 blocked（DAG-E-BLK：issue blocked by reporter info） |
| `/issue-triage:REPORTER_REPLIED` | `needs-info` 后 reporter 有新回复 | 进入 Phase 8 | F-N-5 += reporter 回复 |
| `/issue-triage:READY_FOR_AGENT` | 范围、验收和边界清楚，可交给执行者；bug 类必须复现信息、影响面和复杂度排除项清楚，影响面未知不得进入此状态；不表示执行者已领取或下游已开始 | 生成 agent brief / label / comment 草案后进入 `/issue-triage:TRIAGE_RECOMMENDED` | DAG-N-TASK-* 满足：F-N-6 Depends On 已解析、F-N-9 Gate Required 已锁定；仅 ready，不代表 in-progress |
| `/issue-triage:READY_FOR_HUMAN` | 需要产品、权限、生产或外部裁决 | 生成人工处理草案 | 涉权限 / 生产 / 外部 → 标注 `HG-OPS-*` / `HG-IRREV-*` 相关候选 |
| `/issue-triage:WONTFIX` | 明确不做或超范围 | 生成关闭说明草案 | DAG-N-TASK-*标 Closed (wontfix)；DAG-E-SUP 指向上游决策 |
| `/issue-triage:TRIAGE_RECOMMENDED` | label / comment / close 草案已展示但外部写入未确认 | 等用户确认 | tracker 写入草案；不直接更改 DAG-N-* 状态 |
| `/issue-triage:CONFIRMED_TO_APPLY` | 用户已确认具体 tracker 写入 | 仅应用已确认 label / comment / close 动作 | tracker 写入 = 受限授权；不传递为 HG-*/ DAG-* 跨 workflow 授权 |
| `/issue-triage:TRIAGE_APPLIED` | label / comment / close 已执行 | 返回 `/project-steward` | DAG-N-TASK-* 状态同步（ready / blocked / closed）；F-N-10 += 已应用动作 |

## 0.2 状态权威与路由动作 (State Authority / Route Action)

- **State Authority**：issue tracker 的 labels / comments / close 状态是权威事实源；本表 State 用于决定下一次 triage 动作。Enhancement `wontfix` 产生的 `.out-of-scope/*` 是 scope decision log，不是 feature spec 或 bug audit 记录。
- **Route Action**：`进入 Phase` = `CONTINUE_IN_WORKFLOW`；`生成草案 / 等用户确认 / 等用户选择` = `WAIT_FOR_USER`；`CONFIRMED_TO_CREATE / CONFIRMED_TO_APPLY` = `CONFIRMED_ACTION`，但只授权本次已展示的 tracker 写入，不授权代码修改、spec 修改、下游 workflow 写入或任何真实世界副作用；`分流 / 返回 / 创建失败` = `REPORT_AND_STOP`，除非用户明确要求继续。

## 0.3 中断恢复事实源 (Resume Source)

| 恢复需求 (Resume Need) | 事实源 | 下一步判定 |
| ------------- | -------- | ------------ |
| 等用户选择 issue | Attention Queue 输出 | 进入 Phase 5 或停止 |
| 新 issue 草案待确认 | Draft issue body + labels + target tracker | 创建、修改草案或放弃 |
| 新 issue 已创建 | tracker issue 编号 / URL + 创建时 labels / body | 判定 `/issue-triage:TRIAGE_APPLIED` 或 `/issue-triage:NEEDS_TRIAGE` |
| 现有 issue 待写入 | Triage Recommendation + 待设置 labels / comment / close | 等确认或进入 Phase 6 |
| needs-info 后 reporter 回复 | issue comments + prior triage notes | 进入 Phase 8 |
| tracker 写入失败 | provider 输出 + 已确认的写入动作 | 报告失败，不重复写入 |

## 1. Companion Documents

| 文档 | 角色 | 何时读 |
| ------ | ------ | -------- |
| `../protocols/risk-triage-protocol.md` | AFK/HITL 风险判定、ready-for-agent 必备字段、风险标签冲突处理 | Phase 5 / 6 / 7 |
| `../../tasks-to-issues/protocols/risk-label-protocol.md` | risk:*/ needs:* / afk-* 标签事实源 | Phase 5 / 6 |
