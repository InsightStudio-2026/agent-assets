---
description: "项目管家工作流（/project-steward）专属的触发判定、状态转换路由、状态权威与动作决策矩阵"
---

# 项目管家决策矩阵（/project-steward）

## 0. 触发与临界路由决策表

| ID | 前置条件 | 匹配动作 | 下一步/目标路由 | 源 / 备注 |
| ---- | ---------- | ---------- | ----------------- | ----------- |
| R-ROUTE-STWD-1 | 用户请求 matches 显式命令 `/project-steward` | 启用 workflow | 进入 Phase 1 (Scope & Safety Intake) | 显式入口 |
| R-ROUTE-STWD-2 | 用户说“继续 / 下一步 / 推进 / 项目现在怎么样” | 启用 workflow | 进入 Phase 1 (Scope & Safety Intake) | 推进性意图 |
| R-ROUTE-STWD-3 | 当前任务不清楚，且仓库已有 `docs/specs/` 或母本迹象 | 启用 workflow | 进入 Phase 1 (Scope & Safety Intake) | 缺省管家 |
| R-ROUTE-STWD-4 | 系统状态不清、下一步推进方向不明 | 留在本 workflow | 进入 Phase 1 (Steward 状态诊断决策) | 临界状态 1 |
| R-ROUTE-STWD-5 | 缺失母本（L1 SSOT），且请求涉及项目整体立项 / 规划 | 停止并重定向 | 路由至 `/project-inception` | 临界状态 2 |
| R-ROUTE-STWD-6 | 用户反馈已知具体 Bug，或执行测试失败，属于纯缺陷根因诊断 | 停止并重定向 | 路由至 `diagnose` 技能 | 临界状态 3 |
| R-ROUTE-STWD-7 | 用户请求属于新功能开发、复杂变更、大重构落地或契约变更 | 停止并重定向 | 路由至 `/specs-write` 与 `/specs-execute` | 临界状态 4 |
| R-ROUTE-STWD-8 | 逻辑简单明确（单模块/单函数、不涉契约/Schema），且适合测试先行 | 停止并重定向 | 路由至 `tdd` 技能或直接执行 | 临界状态 5 |
| R-ROUTE-STWD-9 | 以上皆不满足且用户仅进行一般问答或常识性咨询 | 不启用 workflow | 按一般指令/直接回答处理 | 默认退出 |

## 0.1 主路径

```text
Phase 1   Scope & Safety Intake
  → Phase 1.5 Idea Anchor & Alignment Check   (仅在用户投 idea 时激活)
  → Phase 2   Project Surface Scan
  → Phase 3   State Classification
  → Phase 4   Gap / Risk / Blocker Analysis
  → Phase 5   Next Best Action Decision
  → Phase 6   Handoff or Route
```

## 0.1.1 Router Snapshot（快速路由快照）

> **[防漂移声明]**：本表仅作为 `project-steward.md` 3.1 节的状态机快速人读参考索引。其核心控制流及权威判定依据唯一属于主文件 `project-steward.md`。若有冲突，以主文件为准。

| 用户意图 / 现状 | 优先判定 |
| ----------------- | ---------- |
| workflow / skill / `AGENTS.md` / 代理规则维护或审查 | AssetMaintenance / direct asset maintenance |
| 无母本、母本不健康或新 feature 派生 | SSOT / `/project-inception` / `/specs-write` |
| active spec、Pending Task、执行中断或交付收尾 | `/specs-write` / `/specs-execute` lifecycle |
| 发布候选、上线、回滚、readiness、canary 或 smoke | `/release-deploy` |
| 权限、密钥、PII、OAuth、支付、依赖供应链或外部攻击面 | `/security-privacy-audit` |
| 生产事故、用户影响、告警、runbook、log / metric / trace 缺口 | `/observability-incident` |
| bug、失败测试、回归或影响面未知 | `/bug-audit`；根因定位再用 `diagnose` |
| issue tracker、approved tasks 发布、仓库代理上下文或安全基线 | `/issue-triage` / `/tasks-to-issues` / setup workflows |
| 已实现 diff 待审查、简单查询或 Small fix | `review` / direct answer / `tdd` or direct small fix |

## 0.2 工作原则

1. **缺省负责**：用户没有指定下一步时，你必须主动判断下一步，而不是把选择题倒回给用户。
2. **贴合 Idea**：用户投 the idea / vision 一旦被锁定为 Anchor，后续所有推荐、路由、生成动作都要贴合原始话语；不额外 grilling，但在每次路由前做一次贴合自检。
3. **证据先行**：所有状态判断必须引用已读到的文件、目录、命令输出或用户原话。
4. **只推荐一个主路径**：可以列备选，但必须给唯一推荐动作。
5. **不越权执行**：推荐进入另一个 workflow 不等于已经执行；除非用户请求本身明确是“继续执行”，否则先报告推荐。
6. **SSOT 优先**：有健康母本 / L1 SSOT 时，按 SSOT 派生下游，不重复创建；发现母本不健康时，优先修上游，不得继续派生下游 spec。
7. **闭环优先**：未完成归档、review、verification、artifact 核验时，不急着开新 feature。
8. **小事小办**：明显 Small 任务不强行上 workflow。
