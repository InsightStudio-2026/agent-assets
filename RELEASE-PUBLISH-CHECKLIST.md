# 发布到 GitHub 公库清单 · Release Publish Checklist

> 本文件是 DRI 把本仓库首次发布到 GitHub 公开仓库的操作清单。**所有项目都可以一键复制执行**。

## 🎯 目标

把 `agent-assets` 仓库从本地状态（无 remote、单 commit）发布为 GitHub 公开仓库，并完成首次公开发布版本 `v0.1.0`。

## ✅ 发布前自检（Pre-Publish Self-Check）

发布前**逐项打勾**，缺一不可。

### A. 法律与署名

- [x] **A1** `LICENSE` 第 3 行已填真实著作权主体「海口秀英区洞悉人工智能应用软件工作室 (Unified Social Credit Code: 92460000MAK66KH20N)」
- [x] **A2** `README.md` 末尾 License 区块的署名与 LICENSE 一致（含统一社会信用代码）
- [x] **A3** `README.en.md` 末尾 License 区块的署名与 LICENSE 一致
- [x] **A4** `CHANGELOG.md` 中 `[Unreleased]` 与 `[0.1.0]` 的 compare/release 链接已指向 `InsightStudio-2026`
- [x] **A5** 仓库内无任何硬编码的真实 API key / token / 密码 / 个人邮箱泄露
- [x] **A6** 检查 `.gitignore` 是否覆盖 `reports/`、`tmp/`、`cleanup_manifest_*.md`、`locales/` 等本地副产物（已覆盖）
- [x] **A7** `NOTICE` 文件已创建，完整声明著作权主体、第三方资产来源、商标、AI 辅助开发事实

### B. 资产完整性

- [ ] **B1** `npx markdownlint-cli2 "**/*.md"` 全量通过（0 errors）
- [ ] **B2** `pwsh -File .github/verify-completeness.ps1` 通过
- [ ] **B3** `.github/skills/` 下每个 SKILL.md 都有合法的 YAML front matter（`name` + `description`）
- [ ] **B4** `.github/instructions/` 下每个 instruction 都有合法的 YAML front matter（`name` + `description` + `applyTo`）
- [ ] **B5** `.github/agents/` 下每个 agent 都有合法的 YAML front matter（`name` + `description` + `tools`）
- [ ] **B6** `.github/prompts/` 下每个 prompt 都有合法的 YAML front matter（`name` + `description`）
- [ ] **B7** `AGENTS.md` 与 `CLAUDE.md` 中引用的 skill / instruction / agent / prompt 名称都能在仓库中找到（无死链）

### C. Copilot 接入验证（手动）

- [ ] **C1** 用 VS Code 打开本仓库，确认 Copilot Chat 自动识别 `AGENTS.md`（右下角出现 Agent 模式提示）
- [ ] **C2** 在 Copilot Chat 中说"项目状态不清"，确认 Copilot 自动命中 `/project-steward`（不命中说明 skill front matter 有问题）
- [ ] **C3** 创建一个 `.py` 文件并触发对话，确认 `backend.instructions.md` 自动加载（`applyTo: '**/*.py'`）
- [ ] **C4** 创建一个 `.tsx` 文件并触发对话，确认 `frontend.instructions.md` 自动加载
- [ ] **C5** 在终端执行 `git push --force`（在测试仓库中），确认 `safety-guard.json` 拦截生效
- [ ] **C6** 触发 commit message 生成，确认 Copilot 输出符合本仓库 Git 规范（中文标题 + 双语描述）

### D. 公库可读性

- [ ] **D1** `README.md` 顶部 badges 链接全部可访问（License / VS Code / Copilot / markdownlint / PRs Welcome）
- [ ] **D2** `README.md` 中所有相对链接（`./CONTRIBUTING.md`、`./CODE_OF_CONDUCT.md` 等）均存在
- [ ] **D3** `README.md` 目录锚点（`#-这是什么` 等）与实际标题匹配
- [ ] **D4** 仓库在 GitHub 上 About 一栏填写了简介 + 网站（如有）+ Topics（推荐：`vscode` / `copilot` / `agent` / `ai-agent` / `spec-driven` / `dri` / `chinese`）

## 🚀 发布操作（执行步骤）

### 步骤 1：本地最终提交

```powershell
# 在仓库根目录
git add .
git status   # 确认所有变更都是预期的
git commit -F commit-msg.txt   # 中文标题 + 双语描述，详见 rules.instructions.md §5.2
```

建议的 commit message（无 BOM UTF-8 写入 `commit-msg.txt`）：

```text
feat: 完成公库发布物料（诚实化外部谱系 + 填真实署名）

核心改动：
- LICENSE / README / README.en / NOTICE 填真实著作权主体：
  海口秀英区洞悉人工智能应用软件工作室（92460000MAK66KH20N）
- README §🎁 鸣谢从「净室设计」改为诚实四分类：
  · 直接迁移整合（greensock/gsap-skills 8 个 skill + 用户批准记录）
  · 机制吸收与功能覆盖（garrytan/gstack 详细机制清单）
  · 净室吸收设计哲学（Claude Code / Claude Design）
  · 方法论引用（EARS / BDD / TDD / GOOS / Debugging / Pragmatic）
- README 新增 §🪞「诚实声明 · 已知局限」章节（设计哲学/流程闭环/可用性/维护）
- README.en 同步上述诚实化
- 新增 NOTICE（著作权主体 + 第三方资产来源 + 商标 + AI 辅助声明）

English: Complete public-release materials with honest external lineage
and real copyright holder attribution.
```

### 步骤 2：创建 GitHub 公库

**方式 A（推荐，通过 MCP）**：

```text
调用 mcp_github-mcp-se_create_repository：
  name: agent-assets
  description: VS Code-native Copilot customization kit — turns Copilot into a project DRI with spec-driven workflows, 14-surface audits, and three-Gate governance. 中文协议主导。
  private: false
  autoInit: false   # 关键：仓库已有内容，不要让 GitHub 初始化 README
```

**方式 B（通过 GitHub 网页）**：

1. 访问 <https://github.com/new>
2. Repository name: `agent-assets`
3. Description: 见上方
4. 选 **Public**
5. **不要勾选** "Add a README file" / "Add .gitignore" / "Choose a license"（仓库已有）
6. 点击 Create repository

### 步骤 3：关联远程并推送

```powershell
# 替换 OWNER 为你的 GitHub 用户名或组织名
git remote add origin https://github.com/OWNER/agent-assets.git
git branch -M main
git push -u origin main
```

### 步骤 4：仓库设置

在 GitHub 网页 → Settings：

- [ ] **General → Features**：勾选 Issues / Discussions（共建必需）；Wiki 可选
- [ ] **General → Pull Requests**：勾选 "Allow merge commits" + "Automatically delete head branches"
- [ ] **General → Rulesets**（推荐）：为 `main` 分支添加 protection rule（require PR / require status checks）
- [ ] **Security → Code security**：启用 Dependabot alerts（即使本项目无依赖，未来扩展时有用）
- [ ] **Secrets and variables → Actions**：若未来加 CI，在此配置

### 步骤 5：完善 About 与 Topics

仓库主页右上角 ⚙️：

- **Description**：`VS Code-native Copilot customization kit — turns Copilot into a project DRI. 中文协议主导。`
- **Website**：（可选，填你的博客 / 项目主页）
- **Topics**：`vscode` `copilot` `github-copilot` `agent` `ai-agent` `spec-driven-development` `dri` `tdd` `chinese` `instructions` `skills`

### 步骤 6：打首版 Tag 并发布 Release

```powershell
git tag -a v0.1.0 -m "v0.1.0: 首个公库版本

- 完整 .github/ 资产体系
- 跨代理桥接入口 (AGENTS.md + CLAUDE.md)
- 核心方法论：DRI / 三 Gate / DOM / 14 面审计 / SSOT 三层文档"
git push origin v0.1.0
```

然后在 GitHub → Releases → Draft a new release：

- **Tag**: `v0.1.0`
- **Title**: `v0.1.0 · 首个公库版本`
- **Description**：引用 `CHANGELOG.md` 中 `[0.1.0]` 区块

### 步骤 7：宣发（可选）

- [ ] 在你的社交平台（Twitter / 微博 / 小红书 / LinkedIn）分享
- [ ] 提交到 [VS Code Awesome](https://github.com/viatsko/awesome-vscode)（若符合收录标准）
- [ ] 提交到 [Awesome GitHub Copilot](https://github.com/topics/awesome-copilot) 类列表
- [ ] 在相关技术社区（V2EX / Hacker News / Reddit r/vscode）发帖介绍

## 🔄 后续维护节奏

| 频率 | 任务 |
| ---- | ---- |
| 跟随 | VS Code Copilot Agent Customization 官方更新（新增接入点 → 同步本仓库） |
| 周度 | 检查 Issues 并分类（参考 `/issue-triage` skill） |
| 月度 | 发布 patch release（bug fix），更新 `CHANGELOG.md` |
| 季度 | 发布 minor release（新 Skill / 新协议），打 tag |
| 年度 | 回顾 + 发布 major release（如有 breaking change） |

## 🚨 回滚预案

若发布后发现严重问题（如协议漏洞、鸣谢错误、license 违规）：

1. **小型问题**：开 hotfix PR → 合入 `main` → patch release
2. **严重问题**：
   - 立即在 GitHub Settings → General → Danger Zone 暂时切回 Private
   - 评估是否需要 `git revert` 历史 commit
   - 在 SECURITY.md 流程下报告
   - 修复后重新发布并发布安全公告（GitHub Security Advisory）

---

**完成本清单后，本仓库即可正式作为开源项目对外服务。** 🎉
