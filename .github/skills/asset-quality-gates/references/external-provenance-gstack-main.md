# 外部来源审计凭证 · garrytan/gstack

## 1. 资产来源

| 属性 | 具体值 |
| ------ | -------- |
| 来源名称 | `garrytan/gstack` |
| 本地参考路径 | `外部参考/gstack-main/` |
| 来源类型 | 外部 AI 工程工作流与 skill 资产仓库 |
| 引入模式 | 机制吸收 + 功能覆盖吸收 |
| 目标策略 | 将合理机制适配合并到本地原生 `.claude` 工作流与 skill 中，不吸收 Claude Code 专属守护进程或安全性存疑的外部依赖 |
| 审计时间 | 2026-05-29 |
| 审计人 | 代理 Cascade（受用户委托） |

## 2. 已吸收机制

| 核心机制 | 本地承载形态 | 吸收状态 |
| ---------- | -------------- | ---------- |
| **思考-计划-构建-审查-测试-发布-复盘生命周期** | `/project-inception` (思考) + `/specs-write` (计划) + `/specs-execute` (构建) + `review` (审查) + `webapp-testing` (测试) + `/release-deploy` (发布) + `engineering-retro`/`operational-learnings` (复盘) | 已完全吸收 |
| **发布就绪度仪表盘** | `/release-deploy` 中的 `../../release-deploy/references/readiness-dashboard.md` | 已完全吸收 |
| **计划完成度审计** | `/release-deploy` 中的 `../../release-deploy/protocols/plan-completion-audit.md` | 已完全吸收 |
| **会话现场保存与恢复** | `session-context` skill (支持上下文状态恢复，且不产生 WIP 垃圾提交污染 Git 历史) | 已完全吸收 |
| **运行教训账本** | `operational-learnings` skill (分为 Ephemeral, Project Local, Promoted 三层并定义 OL-R* 升级规则) | 已完全吸收 |
| **浏览器 QA 与视觉证据** | `webapp-testing` skill (支持 Playwright 并通过 `with_server.py` 实现本地进程树级生命周期托管与 Windows 端口物理回收) | 已完全吸收 |
| **文档发版级同步** | `/release-deploy` 中的文档同步阶段与 `../../release-deploy/protocols/documentation-sync.md` (严格执行 Diataxis 覆盖率审计) | 已完全吸收 |
| **安全审计与威胁建模** | `/security-privacy-audit` 工作流及 `threat-model`/`privacy-review` 技能 (覆盖 STRIDE 威胁建模与 OWASP 漏洞审计) | 已完全吸收 |
| **范围守卫与编辑锁** | `scope-guard` skill (显式声明 Allowed Paths, Forbidden Paths, Boundary Gates 边界) | 已完全吸收 |
| **提问问题模板化** | 开发者协议中定义的统一 `AskUserQuestion` 推荐格式与 `ask_user_question` 专属工具调用 | 已完全吸收 |
| **代码健康度仪表盘** | `/code-health-dashboard` 工作流 (聚合 linter, typecheck, tests, coverage 趋势) | 已完全吸收 |
| **设计系统与视觉 QA 深化** | `/design-system-audit` 工作流及 `frontend-design` 技能 (强调视觉层次、UX 原则与反模板 AI 审美) | 已完全吸收 |
| **发布后冒烟与性能基线监测** | `/release-deploy` 阶段 7 冒烟监测与 `../../release-deploy/protocols/deploy-protocol.md` (记录并比对 LCP, CLS, INP 性能漂移) | 已完全吸收 |
| **多模型交叉审查与分诊** | `review` 技能 (外部审查信号排重与分层过滤) | 已完全吸收 |
| **浏览器操作流固化** | `browser-flow-codifier` skill (将手工/自动交互步骤逆向固化为可复用 Playwright 脚本) | 已完全吸收 |
| **带所有权防线的提问控制** | `rules.instructions.md` §1 决策所有权矩阵 (DOM) 与 Pause-and-Ask 豁免名单 (减少无谓追问) | 已完全吸收 |
| **工程周期复盘** | `engineering-retro` 技能 (分析 commit、PR、测试趋势与代码重灾区) | 已完全吸收 |

## 3. 功能覆盖矩阵

| 外部 Skill / 命令行 | 覆盖情况 | 本地承载 / 决策形态 | 合理性说明 |
| --------------------- | ---------- | --------------------- | ------------ |
| `/office-hours` | 已覆盖 | `/project-inception` (L1 SSOT 确立) + `/specs-write` (Charter 阶段) | 本地立项和 spec 需求阶段已内化了 6 个强推问题的 reframing 与产品追问机制。 |
| `/plan-ceo-review` | 已覆盖 | `/specs-write` 阶段 1-3 (需求 delta 判定) | 在 spec 规划阶段强制定义 Expansion/Selective/Hold/Reduction 范围。 |
| `/plan-eng-review` | 已覆盖 | `/specs-write` 阶段 4 (设计) + `/specs-execute` | 技术设计中强制包含架构图、数据模型、异常分支和测试用例设计。 |
| `/plan-design-review` | 已覆盖 | `/design-system-audit` + `frontend-design` | 覆盖设计维度评分、视觉规范、反 AI 模板及交互友好度。 |
| `/plan-devex-review` | 已覆盖 | `/developer-experience-audit` | 涉及 TTHW 衡量、开箱体验、开发者痛点和 magical moment 体验设计。 |
| `/plan-tune` | 已覆盖 | `rules.instructions.md` §1 决策所有权矩阵 (DOM) | 制定了清晰 of L-STRAT/L-DESIGN/L-IMPL 分层，实现提问敏感度的自我约束。 |
| `/autoplan` | 已覆盖 | `/specs-write` 连续控制链 | 本地 spec 撰写小助手会自动流水线式执行 Charter -> Requirements -> Design -> Tasks，无需多命令拼接。 |
| `/design-consultation` | 已覆盖 | `frontend-design` + `/design-system-audit` | 承载设计系统构建、设计 tokens 定义及高保真原型输出。 |
| `/review` | 已覆盖 | `review` 技能 (覆盖 Standards, Spec, Verification) | 在发版/PR 前，基于代码规范、需求 delta 和测试验证三轴进行极细审查。 |
| `/codex` | 已覆盖 | `review` 技能 + `/ci-quality-gates` | 多模型交叉验证及外部信号排重机制吸收了独立 Codex cli 的审计理念。 |
| `/investigate` | 已覆盖 | `diagnose` 技能 | 严格执行“先复现调查再应用修复”铁律，并在 diagnose 阶段形成插桩、二分和回归验证。 |
| `/design-review` | 已覆盖 | `/design-system-audit` + `frontend-design` | 结合真实无头/ headed 浏览器完成视觉还原度审查和前端代码微调。 |
| `/design-shotgun` | 部分覆盖 | `frontend-design` + `prototype` 技能 UI 分支 | 提供多套交互原型及布局变体探索，本仓库通过 prototype 平行方案及 frontend-design 实现。 |
| `/design-html` | 已覆盖 | `frontend-design` | 生成高质量、零大型依赖、完美响应式的 production-ready 页面。 |
| `/devex-review` | 已覆盖 | `/developer-experience-audit` | 对开发者 onboarding 及 getting started 进行实测，秒表计时 TTHW。 |
| `/qa` | 已覆盖 | `webapp-testing` | 真实启动 Playwright 查找 bug、自动应用补丁并补充回归测试（regression test）。 |
| `/qa-only` | 已覆盖 | `webapp-testing` with `REPORT_AND_STOP` | 执行相同的端到端浏览器测试，但只输出 bug 报告，不直接改写代码或物理文件。 |
| `/scrape` | 已覆盖 | `webapp-testing` / 普通编码任务 | 数据抓取逻辑作为标准业务任务直接在 `tdd` 或单 Task 阶段实现，不增加冗余 skill。 |
| `/skillify` | 已覆盖 | `browser-flow-codifier` | 将成功的探索流、CAPTHCA 绕过等步骤逆向沉淀为可复用 Playwright 脚本。 |
| `/ship` | 已覆盖 | `/release-deploy` 阶段 1-4 | 核验任务、拉取最新分支、运行全量单测、覆盖率审计并同步 project 文档。 |
| `/land-and-deploy` | 已覆盖 | `/release-deploy` 阶段 5-6 | 自动合并 PR、执行 dry-run 部署、应用 DDL 变更并验证生产 health 端口。 |
| `/canary` | 已覆盖 | `/release-deploy` 阶段 7 (Canary 监控) | 部署后实时监控 console 错误、路由异常，保障核心用户流无阻。 |
| `/landing-report` | 已覆盖 | `/release-deploy` 的 release-report.md | 产生包含部署事实、测试通过率及监控证据的最终 release report。 |
| `/document-release` | 已覆盖 | `/release-deploy` (Doc Sync 阶段) | 分析 diff、对照 Diataxis 模型更新 README、CHANGELOG、运行手册等。 |
| `/document-generate` | 已覆盖 | `/release-deploy` with Diataxis rules | 自动扫描并为漂移/新增的公共接口或函数补充 reference / how-to 级文档。 |
| `/setup-deploy` | 已覆盖 | `/release-deploy` 阶段 5 (配置探测) | 本地探测并记录宿主环境 deploy/status 对应命令与 URL。 |
| `/gstack-upgrade` | **排除不导入** | N/A (自更新机制) | 排除。Windsurf 资产作为工程代码本身的一部分，应通过 Git 统一版本控制，阻断外部静默自更新。 |
| `/context-save` | 已覆盖 | `session-context` (保存状态) | 将临时会话的决策、Allowed Paths、剩余待办一键保存到本地 artifacts。 |
| `/context-restore` | 已覆盖 | `session-context` (恢复状态) | 一键在 Cascade 会话间无缝重置并 grounding 上下文，无 WIP 垃圾提交污染。 |
| `/learn` | 已覆盖 | `operational-learnings` | 将日常开发踩坑、Windows 特殊约定沉淀为 Project Local 并支持 Promotion。 |
| `/retro` | 已覆盖 | `engineering-retro` | 产出带 shipping 趋势、测试覆盖趋势、代码耦合热点的工程复盘材料。 |
| `/health` | 已覆盖 | `/code-health-dashboard` | 统一呈现 tsc, eslint, ruff, pytest, coverage 等本地/CI 门禁信号趋势。 |
| `/benchmark` | 已覆盖 | `/performance-reliability-audit` | 监测并对比 Web LCP, CLS, INP 性能，后端 SQL 慢查询、队列积压等。 |
| `/benchmark-models` | 已覆盖 | `/ci-quality-gates` + 模型交叉审计 | 在审查阶段收集多个模型对同一缺陷修复或设计的 findings 并三角对照。 |
| `/cso` | 已覆盖 | `/security-privacy-audit` | 执行严密的 OWASP Top 10 + STRIDE 威胁建模，阻断越权和 secrets 泄露。 |
| `/setup-gbrain` | **排除不导入** | N/A (外部知识库集成) | 排除。Windsurf 拥有强大的本地符号和内容索引 (`code_search`)，不需要在本地维护一个冗余的向量数据库守护进程。 |
| `/sync-gbrain` | **排除不导入** | N/A (向量库同步) | 排除。理由同上。 |
| `/browse` | 已覆盖 | `webapp-testing` (Playwright) | 在测试和验证阶段原生调用 Playwright API 驱动浏览器执行各种交互。 |
| `/open-gstack-browser` | 部分覆盖 | `webapp-testing` (Headed 模式) | 支持启动 visible headed 浏览器来处理 CAPTCHA / MFA；不导入 sidebar 侧边栏，因为 Cascade 是直接常驻编辑器的。 |
| `/setup-browser-cookies` | **排除不导入** | N/A (Cookie 提取) | 排除。解密并提取主机浏览器 SQLite cookie db 存在隐私和安全合规红线，且在 Win11 新 Chrome 下具有物理不可靠性。 |
| `/pair-agent` | **排除不导入** | N/A (远程浏览器隧道) | 排除。由于安全性（Origin 劫持风险）及开发模式差异，不考虑通过 ngrok 隧道共享浏览器控制句柄。 |
| `/careful` | 已覆盖 | `/repo-safety-setup` | 通过 pre-commit 钩子、安全防护拦截误删、裸 push 或不合规 DDL 变更。 |
| `/freeze` | 已覆盖 | `scope-guard` | 物理锁定当前 Cascade 编辑会话，只允许修改 Allowed Paths 下的特定目录。 |
| `/guard` | 已覆盖 | `scope-guard` + `/repo-safety-setup` | 同时激活安全命令 pre-check 检查与物理编辑文件路径限制。 |
| `/unfreeze` | 已覆盖 | `scope-guard` | 验证通过或用户指示后，一键重置当前编辑锁定路径边界。 |
| `/make-pdf` | **排除不导入** | N/A (PDF 生成) | 排除。通用办公格式（PDF/DOCX/XLSX）读写不属于代理治理资产，开发中直接以标准三方库编码任务在单 Task TDD 落地。 |

## 4. 排除/不吸收机制及理由

| 排除类别 | 具体项 / 机制 | 排除理由与设计考量 |
| ---------- | --------------- | ------------------- |
| **远程穿透与控制隧道** | `pair-agent`、ngrok 隧道暴露、远程 HTTP tunnel 侦听 | 在本地开启 TCP 并通过 ngrok 映射到公网，不仅极易遭受 Origin 劫持，也违背了编辑器本地代理的高安全红线。Windsurf 原生运行在沙盒或本地宿主，无需跨代理穿透。 |
| **外部向量数据库/GBrain** | `gbrain`、`/setup-gbrain`、`/sync-gbrain` | Windsurf 拥有极其敏捷的本地全文与符号索引工具集 (`code_search`)。单独启动外部 PostgreSQL/PGLite 数据库做向量同步属于机制重叠和不必要的过度设计，引入了额外的状态和同步债务。 |
| **持续 Git WIP 垃圾日志** | 连续 checkpoint 提交、WIP 自动 Commit 机制 | 频繁产生 `WIP:` 标记的小微 Commit 会使 Git 历史变得极度破碎混乱。本地通过 `session-context` skill 将现场保存在内存/本地临时 MD 文档，既实现了相同的恢复效果，又保持了 Git commit 树的洁净高质。 |
| **Cookie 解密隐私读取** | 自动提取并解密 Chrome/Edge 的 SQLite cookie 数据库 | 越权读取宿主系统的 Keychain/DPAPI 密钥进行数据解密在生产安全规范中属于高危动作；且在 Windows 11 Chrome 采用 App-Bound Encryption 后，第三方未认证进程已无法正常解密数据，具有底层不可靠性。 |
| **外部自升级机制** | `gstack-upgrade` / 自动拉取外部 git 节点 | 所有的 workflow、skill 和支撑文件都作为仓库核心资产的一部分进行版本化控制，任何升级必须同 spec、同 commit 进行 PR 交付，严禁静默自更新造成状态失控。 |

## 5. 引入规则与指南

1.**[治理重于自动化]**：坚信人机协同的治理流程（如 `/release-deploy` 门禁、`/security-privacy-audit`）优于冰冷的单行 shell 工具自动化。所有破坏性、生产发版、DDL 变更必须遵守 L-STRAT / L-DESIGN 决策划分并获得用户原话批准。

1. **[无直接源码复制]**：禁止将任何外部的 sh、bash、二进制文件或 compiled daemons 直接搬迁至启用路径。所有能力必须用本地的 Python/TypeScript/Powershell 脚本或 Playwright API 重构适配。
2. **[证据胜过主观假设]**：所有约束和引进的逻辑，最终必须在本地运行 `tdd` 编写回归测试，并通过 `webapp-testing` 跑出客观未截断的命令行 stdout 报告（DoD）作为通过证据。

## 6. 验证

| 检查项 | 预期标准 | 实际结果 |
| ------- | ---------- | ---------- |
| 功能矩阵审计 | 深度剖析并完整覆盖了 gstack 全部的 43 个 slash 指令 | 通过 |
| 周期闭环对齐 | 本地 `.claude` 原生工作流无缝覆盖了整个敏捷开发周期 | 通过 |
| 排除理由合宪 | 明确定义了对网络隧道、本地向量 db、cookie 解密的排除理由，安全红线清晰 | 通过 |
| 路径纯净验证 | 启用路径完全没有出现任何 Claude-Code 专属的 `.github/skills` 或混位配置 | 通过 |
