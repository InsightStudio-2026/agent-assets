# Agent Assets · VS Code Copilot 智能体定制资产仓库

> **English summary:** A Chinese-first, VS Code-native customization kit that turns GitHub Copilot into a project-level **DRI (Directly Responsible Individual)** with enforceable spec-driven workflows, 14-surface audits, and three-Gate decision governance. Read [`README.en.md`](./README.en.md) for the full English version.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![Made for VS Code](https://img.shields.io/badge/Made%20for-VS%20Code-007ACC.svg)](https://code.visualstudio.com/)
[![Copilot Agent Mode](https://img.shields.io/badge/Copilot-Agent%20Mode-00A4EF.svg)](https://code.visualstudio.com/docs/copilot/copilot-chat)
[![Markdownlint](https://img.shields.io/badge/markdownlint-clean-success.svg)](https://github.com/DavidAnson/vscode-markdownlint)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](./CONTRIBUTING.md)
[![中文协议](https://img.shields.io/badge/语言-中文%20主导-red.svg)](./README.md#-这是什么)

**一句话定位**：把一整套「项目首席责任人开发协议」通过 VS Code 的全部官方扩展点接入 Copilot —— 不是提示词堆砌，而是**可执行、可审计、可回滚**的工程纪律资产。

---

## 📑 目录

- [✨ 这是什么](#-这是什么)
- [🎯 不是什么](#-不是什么)
- [🚀 快速开始](#-快速开始)
- [🧱 项目结构](#-项目结构)
- [🧭 核心方法论](#-核心方法论)
- [🔀 工作流路由表](#-工作流路由表)
- [🛠️ 为什么是 VS Code 原生](#️-为什么是-vs-code-原生)
- [🎁 鸣谢与设计谱系](#-鸣谢与设计谱系)
- [� 诚实声明 · 已知局限](#-诚实声明--已知局限)
- [�🤝 欢迎共建](#-欢迎共建)
- [📄 License](#-license)

---

## ✨ 这是什么

`agent-assets` 是一套**可被 clone 到任何项目的 Markdown + JSON 配置资产**，为 VS Code + GitHub Copilot 量身定制。它把人类工程团队里"项目首席责任人（DRI）"该有的判断力、纪律和回滚边界，**通过 VS Code 的官方 Agent Customization 接入点全部注入 Copilot**。clone 到生产代码仓库后自动生效——无需安装、无需依赖、无需构建。

- **`instructions/`**：按文件模式 `applyTo` 自动加载的领域规范（前端 / 后端 / 数据库 / 文档 / PowerShell / TDD / 代码审查 / 合规 / 总规则）。
- **`skills/`**：60+ 个按语义自动触发的工作流技能（写规格、执行规格、项目诊断、Bug 审计、根因定位 ……）。
- **`agents/`**：3 个持久角色（planner / implementer / code-reviewer），通过 `@name` 切换。
- **`prompts/`**：5 个斜杠命令模板（`/specs-write`、`/specs-execute` 等）。
- **`hooks/`**：PreToolUse 安全拦截（拦 `rm -rf` / `DROP TABLE` / `git push --force` 等）+ PostToolUse 审计日志。
- **`.vscode/settings.json`**：把 Copilot 的 commit / PR / review 生成行为绑定到本仓库规范。

**结果**：Copilot 在本仓库里不是"问什么答什么"的助手，而是会**主动维护项目全貌、按工作流分流、按门禁验证、按 Gate 决策、按 SSOT 不漂移**的项目第一负责人。

## 🎯 不是什么

为了节省你的判断成本，明确边界：

- **不是** Copilot 提示词合集或"魔法咒语"——所有协议都有可执行验证命令（ESLint / Ruff / pytest / 14 层 drift 防线 / TDD-Lock SHA-256）。
- **不是** MCP server、不是 VS Code 扩展、不是脚本工具——**零安装**，clone 即用。
- **不是** 为其他 IDE 适配（Cursor / Cline / Claude Code 有自己的资产目录约定；本仓库仅提供 `CLAUDE.md` 作为跨代理桥接参考）。
- **不是** 强迫你照搬——所有协议以 **DRI 自决** 为底色，你拍板的范围被严格收窄到「战略 / 关键设计 / 不可回滚副作用」三类。
- **不是** 仅适合大团队——单人独立开发者也能享受"自动维护 SSOT、自动审计、自动验证门禁"的红利。

## 🚀 快速开始

**前置**：已安装 [VS Code](https://code.visualstudio.com/) + [GitHub Copilot 扩展](https://marketplace.visualstudio.com/items?itemName=GitHub.copilot) 并登录 Copilot 订阅。

```text
1. Clone 本仓库到你的项目根（或作为子目录）
   git clone https://github.com/<owner>/agent-assets.git
   cd agent-assets

2. 用 VS Code 打开本目录
   code .

3. 替换 LICENSE 占位符
   把 LICENSE 第 3 行的 [Your Name / Your Studio] 改成你的真实署名

4. 开始对话
   在 Copilot Chat 里说："项目状态不清" → Copilot 会自动命中 /project-steward
                  或说："我要做 X 功能" → Copilot 会自动命中 /specs-write
```

打开后 VS Code 会自动检测 `AGENTS.md`、`.github/copilot-instructions.md`、`.github/instructions/`、`.github/skills/`，全部注入 Copilot 上下文。无需任何手动配置。

> 💡 **若要把资产迁移到已有项目**：把 `.github/`、`AGENTS.md`、`CLAUDE.md`、`.vscode/settings.json`、`LICENSE`、`.markdownlint.json` 复制过去即可。`docs/` 目录是 spec 工作流运行时自动创建的，仓库不预置。

## 🧱 项目结构

```text
agent-assets/
├── AGENTS.md                         # 跨代理中央注册表（VS Code 自动检测）
├── CLAUDE.md                         # Claude Code / Cursor / Windsurf 桥接入口
├── LICENSE                           # MIT
├── .markdownlint.json                # Markdown 规则配置
├── .vscode/
│   ├── settings.json                 # Copilot 行为绑定（commit / PR / review / skillTool）
│   └── tasks.json                    # markdownlint 全量检查任务
└── .github/
    ├── copilot-instructions.md       # VS Code 自动加载的核心协议（速查 + 路由表）
    ├── instructions/                 # applyTo 文件模式自动加载的领域规范（9 个）
    │   ├── rules.instructions.md         # 完整开发协议（DRI / 三 Gate / 14 面审计 / DOM）
    │   ├── frontend.instructions.md      # TypeScript / React 风格
    │   ├── backend.instructions.md       # Python / FastAPI 风格
    │   ├── database.instructions.md      # SQL + 14 层 drift 防线
    │   ├── documentation.instructions.md # 文档分层 + 命名纪律
    │   ├── test-driven.instructions.md   # TDD + DoD 门禁
    │   ├── code-review.instructions.md   # 审查三维度
    │   ├── powershell.instructions.md    # Windows PowerShell 风格
    │   └── compliance.instructions.md    # 版权 / AI 残留清理（手动附加）
    ├── skills/                       # 语义自动触发的工作流（60+ 个）
    │   ├── specs-write/SKILL.md          # 模糊需求 → 可审查 Spec 合同
    │   ├── specs-execute/SKILL.md        # 按 Task TDD 执行
    │   ├── project-steward/SKILL.md      # 项目首席责任人诊断与分流
    │   ├── project-inception/SKILL.md    # 0 → 1 立项
    │   ├── review/SKILL.md               # 三轴变更审查
    │   ├── diagnose/SKILL.md             # 反馈回路驱动的根因定位
    │   ├── bug-audit/SKILL.md            # 缺陷影响面与严重性审计
    │   ├── tdd/SKILL.md                  # 局部 TDD Red-Green-Refactor
    │   └── ...                           # 完整列表见 AGENTS.md
    ├── prompts/                      # 斜杠命令模板（5 个）
    │   ├── specs-write.prompt.md
    │   ├── specs-execute.prompt.md
    │   ├── project-steward.prompt.md
    │   ├── code-review.prompt.md
    │   └── bug-diagnose.prompt.md
    ├── agents/                       # 持久角色（3 个）
    │   ├── planner.agent.md              # 四阶规划
    │   ├── implementer.agent.md          # specs-execute 纪律执行
    │   └── code-reviewer.agent.md        # 只读三维度审查
    ├── hooks/                        # 生命周期拦截
    │   ├── safety-guard.json              # PreToolUse 危险命令拦截
    │   ├── pre-tool-guard.ps1             # 安全判定脚本
    │   └── audit-log.json                 # PostToolUse 审计日志
    └── verify-completeness.ps1       # 资产完整性自检
```

## 🧭 核心方法论

本仓库不是"提示词"，而是一套**自洽的工程哲学**。核心术语（均来自 `rules.instructions.md`）：

| 概念 | 一句话 |
| ---- | ---- |
| **DRI（Directly Responsible Individual）** | Copilot 是项目缺省 DRI，主动维护全貌、识别下一步、补齐上下文、执行验证、归档证据 |
| **三 Gate** | Strategy（产品方向）/ Critical Design（架构契约）/ Real-World Side Effect（不可回滚副作用）—— 仅这三类由用户拍板 |
| **决策所有权矩阵 DOM** | L-STRAT 战略级 / L-DESIGN 设计级 / L-IMPL 实现级 / L-ROUTINE 例行级 —— 越往下 Copilot 越自主 |
| **Pause-and-Ask 白名单** | 只有 5 类情形允许阻塞式反问（战略 / 关键设计置信度<70% / 不可回滚 / Spec Breach / 低置信度） |
| **14 面全景审计** | 文档 SSOT / 历史 / 真实数据库 / 数据静态 / 架构 / 契约 / 依赖 / 运行部署 / 代码入口 / UI / 测试 / 安全隐私 / 可观测 / 合规版权 |
| **SSOT 三层文档体系** | L1 战略 SSOT / L2 执行合同 / L3 交付归档 —— 一个事实只定义一次，其他用引用 |
| **开工四问** | 想清楚 → 最小够用 → 外科手术 → 可验证 |
| **三 TDD 闭环** | ATDD（AC→验收测试）/ BDD（US→场景）/ TDD（单测 PASS）—— `/specs-execute` Phase 7 必须全过 |
| **14 层 drift 防线** | 任何 Schema 变更必须 14 层 ALL GREEN：migration 完整性 / ORM 对齐 / 真库读回 / 列类型 / CHECK / 索引 / 触发器 / 视图 / mypy / OpenAPI 契约冻结 …… |

## 🔀 工作流路由表

| 场景 | 命令 / Skill | 一句话 |
| ---- | ---- | ---- |
| 项目状态不清 / 下一步不明 | `/project-steward` | 全局诊断与分流 |
| 无母本 / L1 SSOT | `/project-inception` | 0 → 1 立项 |
| 新功能 / 跨模块重构 | `/specs-write` | 需求 → Spec 合同（七件套） |
| 执行已批准 Task | `/specs-execute TASK-###` | 强制复述 + TDD Red-Green-Refactor |
| 已实现 diff 审查 | `review` | Standards / Spec / Verification 三轴 |
| 根因定位 / 性能回退 | `diagnose` | 反馈回路驱动的纪律化诊断 |
| Bug 影响面未知 | `/bug-audit` | 广度 + 深度缺陷审计 |
| 架构摩擦 / 浅模块 | `/architecture-audit` | seam / interface 重塑 |
| 商业闭环 / MVP 生死 | `/business-model-audit` | 买方 / 替代方案 / ROI |
| 局部小功能 / 简单 bug | `tdd` 或 direct | 局部 Red-Green-Refactor |

> 完整工作流列表与触发条件见 [`AGENTS.md`](./AGENTS.md)。

## 🛠️ 为什么是 VS Code 原生

业界其他智能体方案把规则塞进 `.cursorrules` / `.clinerules` / `CLAUDE.md` 等单文件，本仓库**完全使用 VS Code 官方 Agent Customization 接入点**，对照 [VS Code 官方文档](https://code.visualstudio.com/docs/copilot/copilot-chat)：

| VS Code 接入点 | 本仓库用法 | 优势 |
| ---- | ---- | ---- |
| `AGENTS.md` | 跨代理中央注册表 | VS Code 自动检测，零配置 |
| `.github/copilot-instructions.md` | 核心协议速查 | 项目级 always-on |
| `.github/instructions/*.md` + `applyTo` | 9 个领域规范按文件类型自动加载 | **按需注入**，避免上下文污染 |
| `.github/skills/*/SKILL.md` | 60+ 语义触发工作流 | Copilot 自动识别任务语义并加载 |
| `.github/agents/*.agent.md` | 3 个持久角色 + 工具限制 + 模型偏好 | 角色边界清晰，工具权限隔离 |
| `.github/prompts/*.prompt.md` | 5 个斜杠命令 | `/specs-write` 即可调用 |
| `.github/hooks/*.json` | PreToolUse / PostToolUse | **灾难命令硬拦截** + 审计日志 |
| `.vscode/settings.json` | Copilot commit/PR/review 生成行为绑定 | 让 Copilot 输出符合本仓规范 |
| `chat.useAgentsMdFile` / `chat.skillTool.enabled` | 启用 AGENTS.md 与 Skill 工具 | 一处开关 |

**对照参考**：本仓库的 `CLAUDE.md` 是给 Claude Code / Cursor / Windsurf 的兼容入口；`.github/instructions/` 的 `applyTo` 模式比单文件 `.cursorrules` 更精细（按语言隔离规范，避免上下文膨胀）。

## 🎁 鸣谢与设计谱系

本仓库坚持**诚实标注外部来源**。资产吸收分为四类，每一类都有清晰的来源、模式与凭证记录。

### 1. 直接迁移整合（Direct Vendor · MIT 协议）

下列 skill 是从外部仓库**完整拷贝 + 本地化适配**而来（保留 MIT 协议），均经用户明确批准并记录在项目自带的来源审计凭证中：

- **[greensock/gsap-skills](https://github.com/greensock/gsap-skills)**（GreenSock / Webflow）—— 8 个 GSAP 动画 skill 直接迁移：
  - `gsap-core` · `gsap-timeline` · `gsap-scrolltrigger` · `gsap-plugins` · `gsap-utils` · `gsap-react` · `gsap-performance` · `gsap-frameworks`
  - **批准记录**：用户于 2026-05-29 明确批准（原话：「直接搬迁，做好windsurf及本地适配化即可」）
  - **凭证文件**：[`.github/skills/asset-quality-gates/references/external-provenance-gsap-skills.md`](./.github/skills/asset-quality-gates/references/external-provenance-gsap-skills.md)
  - **本地适配**：每个 skill 添加中文译名、AGENTS.md 索引登记，移除外部平台专属配置（`.claude-plugin` / `.cursor-plugin`）

### 2. 机制吸收与功能覆盖（Mechanism Absorption）

下列工作流的**设计机制**吸收自外部 AI 工程资产仓库，经**机制参考重写**为中文协议（非源码复制）：

- **[garrytan/gstack](https://github.com/garrytan/gstack)** —— 本仓库大量核心工作流的机制源自 gstack，包括：
  - **生命周期闭环**：思考-计划-构建-审查-测试-发布-复盘 → `/project-inception` + `/specs-write` + `/specs-execute` + `review` + `webapp-testing` + `/release-deploy` + `engineering-retro`
  - **发布就绪度仪表盘** → `/release-deploy` 的 readiness-dashboard
  - **会话现场保存与恢复** → `session-context` skill
  - **运行教训账本** → `operational-learnings` skill（Ephemeral / Project Local / Promoted 三层）
  - **浏览器 QA 与视觉证据** → `webapp-testing` skill
  - **安全审计与威胁建模** → `/security-privacy-audit`（STRIDE + OWASP）
  - **范围守卫与编辑锁** → `scope-guard` skill
  - **代码健康度仪表盘** → `/code-health-dashboard`
  - **设计系统与视觉 QA** → `/design-system-audit` + `frontend-design`
  - **工程周期复盘** → `engineering-retro`
  - **浏览器操作流固化** → `browser-flow-codifier` skill
  - **带所有权防线的提问控制** → DOM 决策所有权矩阵 + Pause-and-Ask 豁免名单
  - **凭证文件**：[`.github/skills/asset-quality-gates/references/external-provenance-gstack-main.md`](./.github/skills/asset-quality-gates/references/external-provenance-gstack-main.md)（含完整功能覆盖矩阵）

> gstack 的 `/gstack-upgrade`（静默自更新）、`/setup-gbrain`（向量库守护进程）、`/setup-browser-cookies`（Cookie 解密）等存在安全 / 合规风险的功能**明确排除不导入**，理由见凭证文件。

### 3. 净室吸收设计哲学（Clean-room Philosophy）

下列项目的**设计哲学与目录约定**被净室吸收，本仓库无源码复制：

- **[VS Code Agent Customization 官方文档](https://code.visualstudio.com/docs/copilot/copilot-chat)** —— 本仓库全部接入点的权威依据。目标：**完美贴合官方搭建指南**，所有目录约定（`.github/instructions/`、`.github/skills/`、`.github/agents/`、`.github/prompts/`、`.github/hooks/`、`AGENTS.md`）均严格对齐。
- **[Claude Code](https://docs.anthropic.com/en/docs/claude-code)** / **Claude Design** —— 净室吸收了 Anthropic 推动的「项目级 AI 协议文件」范式（`CLAUDE.md`）。本仓库 `CLAUDE.md` 作为跨代理桥接入口致敬这一范式；同时本仓库的「项目首席责任人（DRI）协议」设计哲学受 Claude Code 的「agentic coding with guardrails」理念影响。
- **[GitHub Spec Kit](https://github.com/github/spec-kit)** / [spec-kit by gistdotdev](https://github.com/gistdotdev/spec-kit) —— `/specs-write` 的「需求 → 可执行合同」分解思想受其启发，改造为中文 EARS / BDD / TDD 三轨配对。

### 4. 方法论引用（书籍与思想）

下列经典著作与思想散见于各 instructions / skills，均为概念引用而非内容复制：

- **[EARS Notation](https://alistairmavin.com/ears/)**（Alistair Mavin）—— 需求语句结构化语法，`/specs-write` 步进 5 引入。
- **[Behavior-Driven Development](https://en.wikipedia.org/wiki/Behavior-driven_development)**（Dan North）—— Gherkin `Given/When/Then` 场景。
- **[Test-Driven Development: By Example](https://www.oreilly.com/library/view/test-driven-development/0321146530/)**（Kent Beck）—— Red-Green-Refactor 与「测试应通过公共接口验证行为」哲学，是 `tdd` 与 `/specs-execute` Phase 4-6 的基石。
- **[Growing Object-Oriented Software, Guided by Tests](https://www.informit.com/store/growing-object-oriented-software-guided-by-tests-9780321503626)**（Steve Freeman & Nat Pryce）—— `tdd` 中「端到端 tracer bullet」「mock 准则」直接源自此书。
- **[Debugging: The 9 Indispensable Rules](https://debuggingrules.com/)**（David J. Agans）—— `diagnose` 的「先建立反馈回路，再假设」纪律受其影响。
- **[The Pragmatic Programmer](https://pragprog.com/titles/tpp20/the-pragmatic-programmer-20th-anniversary-edition/)**（David Thomas & Andrew Hunt）—— DRY、tracer bullet、broken windows 等概念。
- **DRI 文化**（Apple / Tesla 工程实践）—— 「Directly Responsible Individual」概念源自 Apple 工程文化，本仓库把它从人类组织延伸到 Copilot 自主决策模型。
- **[Contributor Covenant](https://www.contributor-covenant.org/)** —— `CODE_OF_CONDUCT.md` 采用此国际通行社区行为准则。

### 外部资产 intake 协议

本仓库通过 `/asset-quality-gates` skill 维护一套严格的**外部资产 intake 协议**（6 步流程 + R-CHK-10~15 检查项）：任何外部资产引入必须经 quarantine 隔离、license 兼容性判定、frontmatter 改造、eval seeding、AGENTS.md 索引登记、用户批准后才能进入启用路径。详见 [`.github/skills/asset-quality-gates/protocols/intake-protocol.md`](./.github/skills/asset-quality-gates/protocols/intake-protocol.md)。这是本仓库「诚实标注外部来源」的制度保障。

### 边界声明

本仓库**不是**以下项目的 fork 或包装：

- 不是 [Cursor](https://cursor.com/) / [Cline](https://github.com/cline/cline) / [Roo Code](https://github.com/RooCodeInc/Roo-Code) / [Aider](https://aider.chat/) 的资产包 —— 那些项目各有自己的资产目录约定（`.cursorrules` / `.clinerules` 等），本仓库是 VS Code 原生方案。
- 不是 MCP server / VS Code 扩展 —— 零安装，纯配置资产。
- 不是 [Continue](https://www.continue.dev/) / [Cody](https://sourcegraph.com/cody) 的替代 —— 本仓库只针对 GitHub Copilot。

### 致贡献者

感谢所有在公开讨论、issue、PR 中提出反馈的开发者。完整贡献者名单见 [`CONTRIBUTING.md`](./CONTRIBUTING.md) 与 GitHub Insights 页面。

## 🪞 诚实声明 · 已知局限

本仓库追求「高自决必须高审计」与「质量优先」，但**坦白承认以下局限**。这是诚实的工程表态，不是营销话术。

### 设计哲学层面

- **仍在演进**：核心方法论（DRI / 三 Gate / DOM / 14 面审计 / 14 层 drift 防线）是单人独立开发实践中提炼的体系，**未经大型团队 / 复杂分布式系统 / 合规严苛行业（金融 / 医疗）的长期验证**。
- **可能过度工程化**：14 面 / 14 层这类「对称美学」的数字，在某些场景下可能带来超出收益的流程开销。小团队 / 个人项目应自行裁剪。
- **术语学习曲线陡**：DRI / DOM / SSOT / Pause-and-Ask / Gate A-B-C 等术语密集，新用户上手成本不低。

### 流程闭环层面

- **验证样本有限**：`/specs-write` → `/specs-execute` 的完整七件套 spec 合同主要在中文个人项目中跑通；**英文项目、跨国协作、多人并发 spec 场景验证不足**。
- **跨代理兼容是单向桥**：`CLAUDE.md` 只是给 Claude Code / Cursor / Windsurf 的入口指引，**不保证**这些代理能完整复现 VS Code Copilot 的 skill 触发、instruction applyTo、hook 拦截等行为。
- **hook 拦截依赖宿主**：`.github/hooks/safety-guard.json` 的 PreToolUse 拦截依赖 VS Code Copilot 的 hook 机制；若用户关闭了 Autopilot 高级评估器，**灾难命令兜底完全依赖本仓库的 PowerShell 脚本**，存在被绕过的理论风险。

### 可用性层面

- **中文主导**：协议正文与大量 skill 是中文，**海外非中文用户使用门槛较高**。`README.en.md` 是翻译参考，多数 skill 仍待翻译。
- **GSAP skills 是直接翻译**：8 个 gsap-* skill 是从 GSAP 官方文档直接迁移，**未做内容层面的本地化创新或中文场景适配**，本质是官方文档的中文搬运 + AGENTS.md 索引登记。
- **Windows / PowerShell 偏好**：大量 DoD 命令默认假设 Windows + PowerShell 环境（如 `.\venv\Scripts\python.exe`），macOS / Linux 用户需自行调整。

### 维护层面

- **单人维护为主**：项目当前由维护者以 AI 协作方式推进，**60+ skill 的覆盖深度不均**，可能存在死链、过期引用、自相矛盾的角落案例。
- **跟随官方演进的压力**：VS Code Copilot Agent Customization 仍在快速演进，接入点 API 可能变动；本仓库的同步速度取决于维护者精力。
- **未提供自动化测试**：**没有针对 skill 触发准确率、instruction 加载正确性的自动化测试套件**（`/skill-eval` skill 提供了人工 eval 框架，但未 CI 化）。

### 我们如何看待这些局限

我们不回避、不粉饰。如果你在使用中遇到上述局限带来的具体问题，**欢迎在 [Issues](../../issues) 开诚布公地反馈**——尤其是「这里过度工程化了」或「这里在大型团队失效」这类**否定性反馈**，对我们最有价值。

## 🤝 欢迎共建

这是一个**长期维护、社区驱动**的开源项目。我们欢迎：

- 🐛 **Bug 报告与建议**：通过 [GitHub Issues](../../issues) 提交，请先搜索是否已存在。
- 🔀 **Pull Request**：协议补充、新 Skill、英文翻译、跨代理兼容性改进。请先读 [`CONTRIBUTING.md`](./CONTRIBUTING.md) 了解规范与提交流。
- 🌐 **国际化**：欢迎把核心协议翻译成英文 / 日文 / 韩文等。本项目是**中文主导**，但欢迎双语并行。
- 💡 **使用案例分享**：在你的项目里用了本仓库？欢迎在 [Discussions](../../discussions) 分享场景与改进建议。
- ⭐ **Star & Fork**：如果本仓库帮到了你，欢迎点 Star 让更多人看到。

**共建原则**（详见 [`CONTRIBUTING.md`](./CONTRIBUTING.md)）：

1. **中文主导，国际开放**：协议正文中文，但 issue / PR / commit message 接受双语。
2. **净室吸收**：吸收外部概念必须改写为中文协议并显式鸣谢，**禁止直接复制他人源码**。
3. **DRI 文化**：每个 PR 必须有明确作者与可验证 DoD。
4. **Spec 优先**：大型变更走 `/specs-write`，不接受"提示词堆砌"式 PR。

**维护节奏**：跟随 VS Code Copilot Agent Customization 官方演进同步迭代；语义版本号见 [`CHANGELOG.md`](./CHANGELOG.md)。

## 📄 License

[MIT License](./LICENSE) © 2026 海口秀英区洞悉人工智能应用软件工作室

> **著作权人 / 登记主体**：海口秀英区洞悉人工智能应用软件工作室
> **统一社会信用代码**：92460000MAK66KH20N
>
> 详细署名规范（自然人作者 vs 著作权人 / 登记主体）见 [`.github/instructions/compliance.instructions.md`](./.github/instructions/compliance.instructions.md) 与 [`NOTICE`](./NOTICE)。

---

**让 Copilot 不只是助手，而是你的项目首席责任人。** 🚀
