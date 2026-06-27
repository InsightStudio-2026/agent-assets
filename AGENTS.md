# Agent Instructions, Prompts, Skills & Workflows Index

> VS Code Copilot 智能体自定义体系中央注册表。

---

## 📋 指令 (Instructions)

> 自动注入 Copilot 对话上下文的项目级规范。三种加载机制：`applyTo` 文件模式匹配、`description` 语义任务匹配、手动附加。

### 始终加载（Always-On）

| 指令 | 加载条件 | 说明 |
| ------ | ---------- | ------ |
| [copilot-instructions.md](.github/copilot-instructions.md) | VS Code 自动检测 | 项目核心协议——快速自检 + 规范引用 + 路由表 |
| [rules.instructions.md](.github/instructions/rules.instructions.md) | `applyTo: '**'` | 完整开发协议——DRI、三 Gate、14 面审计 |

### 文件模式匹配（Pattern-Based）

| 指令 | 加载条件 | 说明 |
| ------ | ---------- | ------ |
| [frontend.instructions.md](.github/instructions/frontend.instructions.md) | `applyTo: '**/*.{tsx,ts,jsx,js}'` | 前端 React/TypeScript 代码规范 |
| [backend.instructions.md](.github/instructions/backend.instructions.md) | `applyTo: '**/*.py'` | 后端 Python/FastAPI 代码规范 |
| [database.instructions.md](.github/instructions/database.instructions.md) | `applyTo: '**/*.sql'` | SQL Schema 与 Migration 规范 |
| [documentation.instructions.md](.github/instructions/documentation.instructions.md) | `applyTo: '**/*.md'` | 文档编写与分层规范 |
| [powershell.instructions.md](.github/instructions/powershell.instructions.md) | `applyTo: '**/*.{ps1,psm1}'` | PowerShell 脚本代码规范 |

### 语义任务匹配（Task-Based）

| 指令 | 触发场景 | 说明 |
| ------ | ---------- | ------ |
| [test-driven.instructions.md](.github/instructions/test-driven.instructions.md) | 测试编写、TDD、测试策略 | TDD 循环与测试门禁 |
| [code-review.instructions.md](.github/instructions/code-review.instructions.md) | 代码审查、PR review、diff 审计 | 审查三维度规范 |

### 手动附加（Manual Attach）

| 指令 | 说明 |
| ------ | ------ |
| [compliance.instructions.md](.github/instructions/compliance.instructions.md) | 版权合规、软著准备、AI 残留清理 |

---

## 📝 提示 (Prompts)

> 可复用模板提示，通过 `/prompt-name` 或语义匹配触发。

| 提示 | 用途 | 路径 |
| ------ | ------ | ------ |
| specs-write | 规格编写——需求→Spec 合同 | [specs-write.prompt.md](.github/prompts/specs-write.prompt.md) |
| specs-execute | 规格执行——按 Task TDD 实现 | [specs-execute.prompt.md](.github/prompts/specs-execute.prompt.md) |
| project-steward | 项目首席责任人——诊断与分流 | [project-steward.prompt.md](.github/prompts/project-steward.prompt.md) |
| code-review | 代码审查——结构化审查报告 | [code-review.prompt.md](.github/prompts/code-review.prompt.md) |
| bug-diagnose | 缺陷诊断——根因定位与修复 | [bug-diagnose.prompt.md](.github/prompts/bug-diagnose.prompt.md) |

---

## 🛠️ 技能 (Skills)

> 语义自动命中或手动触发的知识包。置于 `.github/skills/` 下由 Copilot 自动发现。

| Skill Name | Reference Link |
| --- | --- |
| browser-flow-codifier | [browser-flow-codifier](.github/skills/browser-flow-codifier/SKILL.md) |
| caveman | [caveman](.github/skills/caveman/SKILL.md) |
| diagnose | [diagnose](.github/skills/diagnose/SKILL.md) |
| doc-coauthoring | [doc-coauthoring](.github/skills/doc-coauthoring/SKILL.md) |
| engineering-retro | [engineering-retro](.github/skills/engineering-retro/SKILL.md) |
| frontend-design | [frontend-design](.github/skills/frontend-design/SKILL.md) |
| grill-me | [grill-me](.github/skills/grill-me/SKILL.md) |
| gsap-core | [gsap-core](.github/skills/gsap-core/SKILL.md) |
| gsap-frameworks | [gsap-frameworks](.github/skills/gsap-frameworks/SKILL.md) |
| gsap-performance | [gsap-performance](.github/skills/gsap-performance/SKILL.md) |
| gsap-plugins | [gsap-plugins](.github/skills/gsap-plugins/SKILL.md) |
| gsap-react | [gsap-react](.github/skills/gsap-react/SKILL.md) |
| gsap-scrolltrigger | [gsap-scrolltrigger](.github/skills/gsap-scrolltrigger/SKILL.md) |
| gsap-timeline | [gsap-timeline](.github/skills/gsap-timeline/SKILL.md) |
| gsap-utils | [gsap-utils](.github/skills/gsap-utils/SKILL.md) |
| handoff | [handoff](.github/skills/handoff/SKILL.md) |
| internal-comms | [internal-comms](.github/skills/internal-comms/SKILL.md) |
| mcp-builder | [mcp-builder](.github/skills/mcp-builder/SKILL.md) |
| migrate-to-shoehorn | [migrate-to-shoehorn](.github/skills/migrate-to-shoehorn/SKILL.md) |
| obsidian-vault | [obsidian-vault](.github/skills/obsidian-vault/SKILL.md) |
| operational-learnings | [operational-learnings](.github/skills/operational-learnings/SKILL.md) |
| postmortem | [postmortem](.github/skills/postmortem/SKILL.md) |
| prototype | [prototype](.github/skills/prototype/SKILL.md) |
| release-notes | [release-notes](.github/skills/release-notes/SKILL.md) |
| review | [review](.github/skills/review/SKILL.md) |
| scaffold-exercises | [scaffold-exercises](.github/skills/scaffold-exercises/SKILL.md) |
| scope-guard | [scope-guard](.github/skills/scope-guard/SKILL.md) |
| session-context | [session-context](.github/skills/session-context/SKILL.md) |
| skill-eval | [skill-eval](.github/skills/skill-eval/SKILL.md) |
| tdd | [tdd](.github/skills/tdd/SKILL.md) |
| webapp-testing | [webapp-testing](.github/skills/webapp-testing/SKILL.md) |
| write-a-skill | [write-a-skill](.github/skills/write-a-skill/SKILL.md) |
| writing-fragments | [writing-fragments](.github/skills/writing-fragments/SKILL.md) |
| writing-shape | [writing-shape](.github/skills/writing-shape/SKILL.md) |
| zoom-out | [zoom-out](.github/skills/zoom-out/SKILL.md) |

| architecture-audit | [architecture-audit](.github/skills/architecture-audit/SKILL.md) |
| asset-quality-gates | [asset-quality-gates](.github/skills/asset-quality-gates/SKILL.md) |
| authorship-copyright-readiness | [authorship-copyright-readiness](.github/skills/authorship-copyright-readiness/SKILL.md) |
| bug-audit | [bug-audit](.github/skills/bug-audit/SKILL.md) |
| business-model-audit | [business-model-audit](.github/skills/business-model-audit/SKILL.md) |
| ci-quality-gates | [ci-quality-gates](.github/skills/ci-quality-gates/SKILL.md) |
| code-health-dashboard | [code-health-dashboard](.github/skills/code-health-dashboard/SKILL.md) |
| content-publishing-ops | [content-publishing-ops](.github/skills/content-publishing-ops/SKILL.md) |
| data-migration-safety | [data-migration-safety](.github/skills/data-migration-safety/SKILL.md) |
| database-drift-defense | [database-drift-defense](.github/skills/database-drift-defense/SKILL.md) |
| design-system-audit | [design-system-audit](.github/skills/design-system-audit/SKILL.md) |
| desktop-release | [desktop-release](.github/skills/desktop-release/SKILL.md) |
| developer-experience-audit | [developer-experience-audit](.github/skills/developer-experience-audit/SKILL.md) |
| issue-triage | [issue-triage](.github/skills/issue-triage/SKILL.md) |
| observability-incident | [observability-incident](.github/skills/observability-incident/SKILL.md) |
| performance-reliability-audit | [performance-reliability-audit](.github/skills/performance-reliability-audit/SKILL.md) |
| project-inception | [project-inception](.github/skills/project-inception/SKILL.md) |
| project-steward | [project-steward](.github/skills/project-steward/SKILL.md) |
| release-deploy | [release-deploy](.github/skills/release-deploy/SKILL.md) |
| repo-agent-setup | [repo-agent-setup](.github/skills/repo-agent-setup/SKILL.md) |
| repo-safety-setup | [repo-safety-setup](.github/skills/repo-safety-setup/SKILL.md) |
| security-privacy-audit | [security-privacy-audit](.github/skills/security-privacy-audit/SKILL.md) |
| specs-execute | [specs-execute](.github/skills/specs-execute/SKILL.md) |
| specs-write | [specs-write](.github/skills/specs-write/SKILL.md) |
| tasks-to-issues | [tasks-to-issues](.github/skills/tasks-to-issues/SKILL.md) |

---

## 🤖 自定义智能体 (Custom Agents)

> 持久角色 + 工具限制 + 模型偏好。通过 `@agent-name` 切换。

| Agent | 用途 | 路径 |
| ------- | ------ | ------ |
| planner | 项目规划——四阶迭代、spec 合同对齐 | [planner.agent.md](.github/agents/planner.agent.md) |
| code-reviewer | 代码审查——只读工具、三维度审查 | [code-reviewer.agent.md](.github/agents/code-reviewer.agent.md) |
| implementer | 代码实现——specs-execute 纪律执行 | [implementer.agent.md](.github/agents/implementer.agent.md) |

---

## 🪝 钩子 (Hooks)

> 生命周期自动化——安全拦截、审计日志、格式化。

| Hook | 事件 | 用途 | 路径 |
| ------ | ------ | ------ | ------ |
| safety-guard | PreToolUse | 拦截危险命令（rm -rf、DROP TABLE 等） | [safety-guard.json](.github/hooks/safety-guard.json) |
| audit-log | PostToolUse | 记录工具执行审计日志 | [audit-log.json](.github/hooks/audit-log.json) |
