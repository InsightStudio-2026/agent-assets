# 更新日志 · Changelog

<!-- markdownlint-disable-file MD024 -->
<!-- 注：Keep a Changelog 格式必然产生重复的 "Added/Changed/Fixed" 子标题（每版本一段），故在此文件局部豁免 MD024。 -->

本项目所有重要变更均会记录在本文件中。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)，版本号遵循 [Semantic Versioning](https://semver.org/lang/zh-CN/)。

## [Unreleased]

### Added

- 仓库根 `README.md`：双语项目说明（中文主体 + 顶部英文摘要），含完整目录、核心方法论、工作流路由表、鸣谢与设计谱系、已知局限、共建指引。
- 仓库根 `README.en.md`：完整英文版，作为国际化入口与中文版翻译参考。
- 仓库根 `CONTRIBUTING.md`：共建规范与提交流程，含 DOM 决策归属、PR 模板、内容质量底线、国际化贡献特别说明。
- 仓库根 `CODE_OF_CONDUCT.md`：基于 Contributor Covenant 2.1 的行为准则（中文版 + 英文版链接）。
- 仓库根 `SECURITY.md`：安全策略，含漏洞报告流程、响应时间承诺、安全设计原则、使用者注意事项。
- 仓库根 `CHANGELOG.md`：本文件。
- 仓库根 `RELEASE-PUBLISH-CHECKLIST.md`：发布到 GitHub 公库的一键操作清单。
- 仓库根 `NOTICE`：正式声明著作权主体、第三方资产来源（greensock/gsap-skills 直接迁移、garrytan/gstack 机制吸收）、商标、AI 辅助开发事实。
- `.vscode/settings.json` 进入版本控制（从 `.gitignore` 中移出），让访客 clone 后即可体验完整 Copilot 接入效果。
- 新 skill `database-drift-defense/SKILL.md`：将 14 层数据库漂移防线从空壳口号转化为通用哲学框架——含 14 层完整定义、最少启动集合、CI 编排建议、baseline 刷新准则、可复制实现模式（伪代码骨架）、GitHub Actions CI 集成示例、baseline JSON 格式规范、逐层失败处置指南。在 AGENTS.md 索引登记。

### Changed

- `LICENSE`：填真实著作权主体「海口秀英区洞悉人工智能应用软件工作室 (92460000MAK66KH20N)」。
- `README.md` / `README.en.md` / `SECURITY.md` / `database.instructions.md`：全局剔除「纯资产仓库 / 无运行时代码」自限语言——本仓库将被 clone 到真实生产代码仓库驱动代理工作，配置资产应在任何项目中直接生效。
- `README.md` §🎁 鸣谢与设计谱系：从笼统的「净室设计」改为**诚实四分类**——直接迁移整合（greensock/gsap-skills 8 个 skill + 用户批准记录）、机制吸收与功能覆盖（garrytan/gstack 详细机制清单）、净室吸收设计哲学（Claude Code / Claude Design）、方法论引用。所有外部来源引用项目自带的来源审计凭证文件。
- `README.md` 新增 §🪞「诚实声明 · 已知局限」：坦白承认设计哲学、流程闭环、可用性、维护四个层面的局限。
- `README.en.md` 同步上述鸣谢诚实化 + Known Limitations + 自限语言剔除。
- `database.instructions.md`：**完全重写**——移除所有空壳脚本引用，改为项目无关的 14 层防线哲学框架 + MCP 驱动防线实现指南 + 速查表补 D2.4 落项 + Schema 变更 SOP。引用 `database-drift-defense` skill 作为哲学完整版。
- `database-drift-defense/SKILL.md`：**二次补强**——新增 §5 可复制实现模式（D2.1 / D2+++ 伪代码骨架）、§6 CI 集成示例（GitHub Actions workflow）、§7 Baseline 文件格式规范（JSON 字段契约）、§8 逐层失败处置指南表。
- `.gitignore`：`.vscode/` 改为只忽略个人级临时文件。
- `AGENTS.md`：Skills 索引增加 `database-drift-defense`。
- `CHANGELOG.md`：compare/release 链接从 `CHANGE_ME_OWNER` 改为 `InsightStudio-2026`。

### Fixed

- **订正「补强清单.md」死引用**（75+ 处，23 个文件）：该文件为过时的噪音垃圾，已从仓库中消失。所有引用按当前 SSOT 文档替换——`checks-catalog.md` / `intake-protocol.md` / `readiness-dashboard.md` / `deploy-protocol.md` / `documentation-sync.md` / `methodology-kernel.md` / `conformance-fixtures/README.md` / `gate-dag-protocol.md` 等。`gate-dag-protocol.md` 自身定位为横切协议 SSOT。
- **订正 `rules-edit.md` 死引用**：`external-provenance-gstack-main.md` 中 1 处改为 `rules.instructions.md`。
- `README.md` / `SECURITY.md` 的 markdownlint MD042 空链接错误。
- `CHANGELOG.md` 的 markdownlint MD024（局部豁免）。

## [0.1.0] - 2026-01-01

### Added

- 项目初始化提交（`initialization`）。
- 完整的 `.github/` 资产体系：`copilot-instructions.md` / `instructions/`（9 个领域规范）/ `skills/`（60+ 个工作流）/ `prompts/`（5 个斜杠命令）/ `agents/`（3 个持久角色）/ `hooks/`（安全拦截 + 审计日志）。
- 跨代理桥接入口：`AGENTS.md`（VS Code 中央注册表）+ `CLAUDE.md`（Claude Code / Cursor / Windsurf）。
- 核心方法论体系：DRI（Directly Responsible Individual）/ 三 Gate / 决策所有权矩阵 DOM / Pause-and-Ask 白名单 / 14 面全景审计 / SSOT 三层文档体系 / 开工四问 / 三 TDD 闭环 / 14 层 drift 防线。
- Markdown 工程基线：`.markdownlint.json` 规则配置 + `.vscode/tasks.json` 全量检查任务。

[Unreleased]: https://github.com/InsightStudio-2026/agent-assets/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/InsightStudio-2026/agent-assets/releases/tag/v0.1.0

---

> **维护者注意**：上方 compare/release 链接已指向 `InsightStudio-2026`。
