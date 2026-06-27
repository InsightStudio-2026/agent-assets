---
description: "仓库级代理运行环境初始化工作流（/repo-agent-setup）专属的触发判定、状态转换路由、状态权威与动作决策矩阵"
---

# 代理环境初始化决策矩阵（/repo-agent-setup）

## 0. 触发与临界路由决策表

| ID | 前置条件 | 匹配动作 | 下一步/目标路由 | 源 / 备注 |
| ---- | ---------- | ---------- | ----------------- | ----------- |
| R-ROUTE-RAS-1 | 用户显式 `/repo-agent-setup` | 启用 workflow | 进入 Phase 1 (Intake) | 显式入口 |
| R-ROUTE-RAS-2 | 目标项目的 issue tracker、协作标签词表、或基础领域文档布局缺失 | 启用 workflow | 进入 Phase 1 (Intake) | 环境基础缺失 |
| R-ROUTE-RAS-3 | 其他上游流程在执行时，无法确认 issue tracker 或目标 domain docs 位置 | 启用 workflow | 进入 Phase 1 (Intake) | 流程堵塞引流 |
| R-ROUTE-RAS-4 | 触发了初始化，但当前仓库存在 `.github/skills` + `.github/workflows` 且拥有 `AGENTS.md`（仓库元资产契约） | 启用本 workflow (保护模式) | 进入 Phase 1，不写任何 `docs/agents/*`，仅报告元资产上下文缺口 | 资产仓库保护拦截 (特例) |
| R-ROUTE-RAS-5 | 系统状态不清、下一步推进方向不明 | 停止并重定向 | 路由至 `/project-steward` | 临界状态 1 |
| R-ROUTE-RAS-6 | 缺失母本或 L1 SSOT | 停止并重定向 | 路由至 `/project-inception` | 临界状态 2 |
| R-ROUTE-RAS-7 | 属于纯缺陷根因诊断（局部、具体 bug） | 停止并重定向 | 路由至 `diagnose` 技能 | 临界状态 3 |
| R-ROUTE-RAS-8 | 属于新功能、新需求开发、大重构落地 | 停止并重定向 | 路由至 `/specs-write` 与 `/specs-execute` | 临界状态 4 |
| R-ROUTE-RAS-9 | 逻辑简单明确且适合 TDD 验证 | 停止并重定向 | 路由至 `tdd` 技能或直接执行 | 临界状态 5 |
| R-ROUTE-RAS-10 | 以上皆不满足，且无代理运行上下文初始化需求 | 不启用 workflow | 不启用本 workflow | 默认退出 |

## 0.1 状态与路由汇总 (State / Route Summary)

| 状态 (State) | 判定 | 下一步 | Gate / DAG ID 映射 |
| ------- | ------ | -------- | --------------------- |
| `/repo-agent-setup:ASSET_REPO_DETECTED` | 当前仓库是 agent assets 仓库 | 只报告缺口，不写 `docs/agents/*` | `S-HG-1 GATE_NOT_REQUIRED`（受限只读） |
| `/repo-agent-setup:REPORT_ASSET_CONTEXT_GAPS` | agent assets 仓库存在索引、路由或维护契约缺口 | 输出缺口与推荐修订，不进入普通项目初始化 | 路由到 `/project-steward:AGENT_ASSET_MAINTENANCE_NEEDED` |
| `/repo-agent-setup:NOOP_ASSET_REPO` | agent assets 仓库上下文已足够健康 | 报告无需写入 | — |
| `/repo-agent-setup:ALREADY_CONFIGURED` | issue tracker、标签词表和领域文档读取规则已存在且健康 | 返回 `/project-steward` | — |
| `/repo-agent-setup:AGENT_CONTEXT_MISSING` | issue tracker / 标签 / 领域文档规则缺失 | 进入 Phase 2-4 | 预装配 `HG-OPS-{repo}-context`（仓库级配置变更）；packet F-HG-1~8 必齐 |
| `/repo-agent-setup:WAITING_TRACKER_DECISION` | issue tracker provider 或写入方式未确认 | 等用户确认 | `S-HG-3 GATE_PACKET_INCOMPLETE`（F-HG-4 作用范围未定） |
| `/repo-agent-setup:WAITING_LABEL_DECISION` | category / state label 真实字符串未确认 | 等用户确认 | `S-HG-3`（F-HG-4 待补） |
| `/repo-agent-setup:WAITING_DOMAIN_LAYOUT_DECISION` | domain docs 布局未确认 | 等用户确认 | `S-HG-3`（F-HG-4 待补） |
| `/repo-agent-setup:WAITING_CLAUDE_MIGRATION_DECISION` | `AGENTS.md` 迁移或保留方式未确认 | 等用户确认 | `S-HG-3` + 如涉迁移历史 → 预装配 `HG-IRREV-*`（git 历史 / 文件迁移） |
| `/repo-agent-setup:READY_TO_WRITE` | 待写内容已展示并获确认 | 进入 Phase 6 | `S-HG-4 WAITING_GATE_APPROVAL` + `HG-OPS-{repo}-context` 已确认；packet F-HG-1~8 齐；F-HG-6 含回滚 |
| `/repo-agent-setup:WRITE_BLOCKED` | 写入 `AGENTS.md` 或 `docs/agents/*` 被权限、冲突或环境阻止 | 停下报告阻塞，等待用户裁决 | `S-HG-9 GATE_FAILED`（写入失败） |
| `/repo-agent-setup:PARTIAL_WRITTEN` | 部分目标文件已写入，剩余文件失败或未确认 | 报告已写 / 未写清单，等待用户裁决 | 部分 `S-HG-8`、部分 `S-HG-9`；packet F-HG-5 前置证据不全 |
| `/repo-agent-setup:MIGRATION_BLOCKED` | `AGENTS.md` 迁移或处置失败，且可能造成代理说明漂移 | 停下报告迁移风险 | `S-HG-9 GATE_FAILED` + `FA-HG-4`（涉文件迁移） |
| `/repo-agent-setup:DONE` | 代理上下文已写入或确认无需写入 | 报告 `/repo-agent-setup:DONE` 后返回 `/project-steward` | `S-HG-8 GATE_PASSED`（如有 HG-OPS-* 触发）或 `S-HG-1`（如 NOOP） |

## 0.2 状态权威与路由动作 (State Authority / Route Action)

- **State Authority**：普通目标项目中，`AGENTS.md` 与 `docs/agents/*` 写入后才是权威事实源；agent assets 仓库中，`AGENTS.md`、`.github/workflows/*`、`.github/skills/*` 与索引一致性是权威事实源；本表 State 只用于初始化调度。
- **Route Action**：`进入 Phase` = `CONTINUE_IN_WORKFLOW`；`等用户确认 / 裁决` = `WAIT_FOR_USER`；`返回 / 分流 / 写入阻塞 / 部分写入 / 迁移阻塞` = `REPORT_AND_STOP`，除非用户明确要求继续；`/repo-agent-setup:READY_TO_WRITE` = `CONFIRMED_ACTION`，但只授权已展示的 `AGENTS.md` / `docs/agents/*` / 迁移范围写入，不授权业务代码、feature spec、tracker 外部写入或下游 workflow 执行。

## 0.3 写入确认门与资产仓库路由

进入 `/repo-agent-setup:READY_TO_WRITE` 前，确认内容必须覆盖：目标仓库类型、待写文件列表、每个文件内容草案、tracker provider、标签词表、domain docs 布局、`AGENTS.md` 迁移策略（如适用）与放弃 / 回滚方式。缺任一项则保持对应 `WAITING_*`。

### 0.4 Asset Repo Route

检测到 `/repo-agent-setup:ASSET_REPO_DETECTED` 后，只执行 Phase 1 的资产上下文读取与缺口报告。若上下文健康 → `/repo-agent-setup:NOOP_ASSET_REPO`；若存在缺口 → `/repo-agent-setup:REPORT_ASSET_CONTEXT_GAPS`。agent assets 仓库的实际修复走 `/project-steward` 的 direct asset maintenance；除非用户明确说明“当前仓库是目标项目而非 agent assets 仓库”，不得进入 Phase 2-6，不得创建 `docs/agents/*`。

## 0.5 Resume Source（中断恢复事实源）

| Resume Need | 事实源 | 下一步判定 |
| ------------- | -------- | ------------ |
| asset repo 检测后中断 | Asset repo findings + 缺口清单 | 报告缺口或停止 |
| tracker 决策未确认 | Provider 草案 + 用户偏好 | 等确认或修草案 |
| label / domain 决策未确认 | 标签词表草案 + domain docs layout 草案 | 等确认或修草案 |
| 写入待确认 | 待写文件列表 + 文件内容草案 + 迁移策略 | 进入 Phase 6 或等待 |
| 写入部分失败 | Written / Not Written 清单 + 错误输出 | 停止并等待裁决 |
