# CLAUDE.md — Cross-Agent Compatibility Bridge

> 本文件为 Claude Code / Cursor / Windsurf 等多 Agent 环境提供与 VS Code Copilot 等价的项目规范入口。
> 权威 SSOT 始终为 `.github/instructions/` 目录下的指令文件。本文件仅作桥接引用，不重复定义。

## 核心协议

你是项目主要推进者、缺省 DRI 与缺省决策者。凡未列入 Pause-and-Ask 白名单的决策，自行调查、拍板、执行、验证。

开工前过四问：

1. 是否 L-STRAT / L-DESIGN？不是就自决。
2. 是否只需最小改动？
3. 是否只触及目标代码？
4. 是否有可验证完成标准？

## 规范引用

| 领域 | 权威 SSOT |
| ------ | ----------- |
| 完整开发协议（DRI、三 Gate、14 面审计、路由表、DoD） | `.github/instructions/rules.instructions.md` |
| 前端 React/TypeScript | `.github/instructions/frontend.instructions.md` |
| 后端 Python/FastAPI | `.github/instructions/backend.instructions.md` |
| 数据库 Schema/Migration | `.github/instructions/database.instructions.md` |
| 文档编写 | `.github/instructions/documentation.instructions.md` |
| PowerShell 脚本 | `.github/instructions/powershell.instructions.md` |
| TDD 与 DoD 门禁 | `.github/instructions/test-driven.instructions.md` |
| 代码审查 | `.github/instructions/code-review.instructions.md` |
| 版权合规（手动附加） | `.github/instructions/compliance.instructions.md` |

## 路由表

| 场景 | 路由 |
| ------ | ------ |
| 项目状态不清 | `/project-steward` |
| 新功能/重构 | `/specs-write` |
| 执行 Task | `/specs-execute` |
| Bug | `diagnose` |
| 审查 | `review` |

## 工程标准

- **Git**：频繁暂存、不自动提交、原子粒度、中文标题+双语描述
- **Windows PowerShell**：UTF-8 with BOM 编码、禁用 `&&`、禁用 `cd`
- **Lint**：`npx markdownlint-cli2 "**/*.md"`（0 errors）

## 智能体

| Agent | 用途 |
| ------- | ------ |
| `@planner` | 四阶迭代规划、spec 合同对齐 |
| `@implementer` | specs-execute 纪律执行、DoD 门禁 |
| `@code-reviewer` | 只读审查、结构化报告 |
