# 参与共建 · Contributing to Agent Assets

> 感谢你愿意为 `agent-assets` 贡献力量！本文件是协作规范与提交流程的权威指南。先读这份，再开 PR。

**语言策略**：协议正文中文主导；issue / PR / commit message 接受中英双语。本文档提供中英对照要点。

---

## 🌟 我们欢迎什么样的贡献

| 类型 | 说明 | 提交方式 |
| ---- | ---- | ---- |
| 🐛 Bug 报告 | 协议自相矛盾、SKILL 触发错乱、markdownlint 报错、接入点失效 | [Issues](../../issues) |
| 💡 增强建议 | 新 Skill、新 instruction、新工作流、跨代理兼容性改进 | [Issues](../../issues) 先讨论 |
| 🔀 Pull Request | 协议补充、文案优化、英文翻译、文档完善 | PR（流程见下） |
| 🌐 国际化 | 翻译成英文 / 日文 / 韩文等 | PR，建议先开 Issue 对齐术语 |
| 📖 使用案例 | 在你项目里用了本仓库？分享场景与改进点 | [Discussions](../../discussions) |
| ⭐ Star & Fork | 让更多人看到 | 仓库右上角 |

## 🚫 我们不欢迎什么样的贡献

为了保持仓库质量与一致性，以下贡献**会被礼貌拒绝**：

- **提示词堆砌式 PR**：只堆"咒语"而无方法论锚点、无可验证 DoD。
- **直接复制他人源码**：本项目坚持净室设计，吸收外部概念必须改写为中文协议并显式鸣谢。
- **跨代理包装 PR**：把本仓库改造成 `.cursorrules` / `.clinerules` 单文件方案。本仓库是 VS Code 原生方案，跨代理兼容只通过 `CLAUDE.md` 桥接。
- **未经 Issue 讨论的大型重构**：超过 150 行 / 5 文件的变更请先开 Issue 对齐设计。
- **AI 残留伪造**：故意加入"假装人类写的"低级玩笑、虚假 TODO、编造的修改历史。详见 [`.github/instructions/compliance.instructions.md`](./.github/instructions/compliance.instructions.md)。

## 📋 提交流程（PR Workflow）

### 1. 开 Issue 对齐（大型变更必走）

如果你要新增 Skill、修改核心协议、调整目录结构，**先开 Issue** 描述：

- 你想解决什么问题？
- 现有协议 / Skill 为什么不够？
- 你建议的方案是什么？是否有外部灵感来源（必须鸣谢）？

维护者会在 3 个工作日内回复是否接受方向。

### 2. Fork & 分支

```bash
git clone https://github.com/<your-username>/agent-assets.git
cd agent-assets
git checkout -b feat/your-feature-slug
```

**分支命名**（kebab-case，前缀语义化）：

- `feat/`：新功能 / 新 Skill / 新协议
- `fix/`：bug 修复
- `docs/`：纯文档
- `i18n/`：国际化
- `chore/`：构建 / 配置 / 依赖

### 3. 本地验证（DoD）

提交前必须本地通过：

```powershell
# Markdown 全量校验（0 errors）
npx markdownlint-cli2 "**/*.md"

# 资产完整性自检
pwsh -File .github/verify-completeness.ps1

# 若你新增 / 修改了 .ps1，必须用 UTF-8 with BOM 保存
# （Windows PowerShell 5.x 读取无 BOM UTF-8 会中文乱码）
```

### 4. Commit 规范

严格遵守 [`rules.instructions.md` §5.2 Git 规范](./.github/instructions/rules.instructions.md)：

- **中文标题** + 中英双语描述
- **原子粒度**：每个 commit 只做一件事
- **不自动提交**：只在你确信时 `git add`

格式参考：

```text
feat(specs-write): 新增 §3.2 EARS 语句模板

- 在 requirements 模板中加入 EARS 关键词矩阵
- 补充 4 个行业示例（金融 / 电商 / SaaS / 物联网）
- 同步更新 self-check.md 对应自检项

English: Add EARS sentence templates to requirements phase
```

### 5. PR 描述模板

PR 描述必须包含以下五段（参考 `.github/instructions/code-review.instructions.md` 三维度）：

```markdown
## 变更摘要
<!-- 1-2 句话说清楚做了什么 -->

## 动机与背景
<!-- 关联 Issue #N，说明为什么改 -->

## Standars 合规
<!-- 引用了哪些 .github/instructions/ 中的规范 -->

## Spec 一致
<!-- 是否触及核心协议？是否经过 /specs-write？ -->

## Verification
<!-- 本地跑了哪些验证命令，结果如何 -->
- [ ] markdownlint: 0 errors
- [ ] verify-completeness.ps1: PASS
- [ ] 手动触发 Copilot 验证 Skill 命中正确
```

### 6. Code Review

维护者会按 [`code-review.instructions.md`](./.github/instructions/code-review.instructions.md) 三维度审查：

- **Standards**：是否符合仓库已文档化的工程规范？
- **Spec**：是否忠实实现来源 issue / PRD？
- **Verification**：有哪些可运行检查增强或削弱对 diff 的信心？

高风险 diff 会追加 Risk Gates / Architecture / Operability / Authorship-Provenance 四轴审查。

## 🧭 贡献者决策归属（DOM）

为了让贡献者高效协作，本仓库把 [`rules.instructions.md`](./.github/instructions/rules.instructions.md) 的决策所有权矩阵投影到贡献场景：

| 决策级别 | 典型内容 | 归属 |
| ---- | ---- | ---- |
| **L-STRAT 战略级** | 项目方向 / 商业模型 / 仓库 license / 是否接受跨代理改造 | **维护者拍板** |
| **L-DESIGN 设计级** | 新 Skill 架构 / 目录结构调整 / 新增 instruction 分类 | **维护者拍板**（贡献者提供方案 + ≤ 2 备选 + 代价） |
| **L-IMPL 实现级** | 文案措辞 / 示例补充 / Skill 内部章节拆分 / 错别字 | **贡献者自决**，PR 描述说明 |
| **L-ROUTINE 例行级** | 格式化 / 链接修复 / markdownlint 修复 | **贡献者自决**，直接 PR |

## 📐 内容质量底线

所有新增 / 修改的协议文件必须满足：

1. **H1 开头**：MD041 强制。
2. **YAML front matter 完整**：`name` / `description` / `applyTo`（如适用）/ `argument-hint`（如适用）。
3. **同源不复制**：一个事实只在一个 SSOT 里定义，其他用相对路径 + 锚点引用。
4. **懒加载契约**：长文档必须把细节抽到子文档，主文件只保留控制流骨架（详见 [`documentation.instructions.md`](./.github/instructions/documentation.instructions.md)）。
5. **可验证**：新增工作流必须能被 Copilot 触发并产出预期输出；新增 DoD 必须有可运行命令。
6. **中文主导**：协议正文中文；术语首次出现时附英文（如「DRI（Directly Responsible Individual）」）。
7. **无 AI 残留**：不允许 "As an AI..."、虚假 TODO、编造的修改历史。

## 🌐 国际化贡献特别说明

本项目是**中文主导**，英文版（`README.en.md`）为翻译参考。国际化贡献请遵循：

- **术语统一**：核心术语（DRI / 三 Gate / DOM / SSOT / 14 面审计）首次出现必须附英文原文；翻译时建议保留中文术语 + 英文注释。
- **不要破坏中文 SSOT**：`README.md` 是权威源，`README.en.md` 是派生翻译；当两者冲突时以中文版为准。
- **翻译 PR 流程**：先开 Issue 锁定翻译范围（避免多人重复翻译），完成后整段提交。

## 🤝 行为准则

参与本仓库即代表你接受 [Code of Conduct](./CODE_OF_CONDUCT.md)。请保持友善、尊重、建设性。

## 📬 联系维护者

- **公开讨论**：[GitHub Discussions](../../discussions)
- **Bug 与建议**：[GitHub Issues](../../issues)
- **安全漏洞**：详见 [SECURITY.md](./SECURITY.md)，**请勿在公开 Issue 中披露安全漏洞**
- **邮件**：维护者邮箱见仓库 Insights → Contributors

---

**再次感谢你的贡献！** 你的每一份 PR 都让 Copilot 离"项目首席责任人"更近一步。🚀
