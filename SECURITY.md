# 安全策略 · Security Policy

## 🛡️ 支持版本

本项目为 Markdown + JSON 配置仓库（无编译二进制产物），因此不存在传统意义上的"安全漏洞"（如内存破坏、注入、XSS 等）。但仍重视以下类型的安全相关问题：

| 类型 | 严重程度 | 说明 |
| ---- | ---- | ---- |
| **`hooks/` 安全拦截失效** | 高 | `safety-guard.json` 漏拦 `rm -rf` / `DROP TABLE` / `git push --force` 等灾难命令 |
| **硬编码凭据** | 高 | 仓库中混入 API key / token / 密码 |
| **`.vscode/settings.json` 不安全默认** | 中 | 默认配置会让访客机器暴露在风险中（如关闭了必要的隔离） |
| **协议漏洞导致 Copilot 执行危险操作** | 高 | 协议逻辑缺陷让 Copilot 在 Pause-and-Ask 白名单外执行不可回滚动作 |
| **AI 残留伪造** | 低 | 故意伪造人类作者痕迹（详见 `.github/instructions/compliance.instructions.md`） |
| **License 违规** | 中 | 鸣谢的项目实际 License 与本仓库声明不符 |

## 📣 如何报告安全漏洞

**请勿在公开 Issue 中披露任何安全漏洞。**

请通过以下私密渠道报告：

1. **优先**：使用 GitHub 的 [Security Advisories](../../security/advisories/new) 功能私密报告。
2. **备用**：发送邮件到仓库 Insights → Contributors 中公布的维护者邮箱，邮件主题以 `[SECURITY]` 开头。

**报告中请包含**：

- 漏洞类型与影响范围
- 复现步骤（如适用）
- 建议的修复方案（可选）
- 你的联系方式（用于跟进）

## ⏱️ 响应时间

| 阶段 | 时间承诺 |
| ---- | ---- |
| 收到报告后确认 | 3 个工作日内 |
| 初步评估与分类 | 7 个工作日内 |
| 修复发布 | 严重程度而定（高危 ≤ 30 天，中危 ≤ 90 天，低危跟随下个版本） |
| 公开披露 | 修复发布后 7 天内（与报告者协商披露时机） |

## 🎁 致谢

报告者在漏洞修复后会出现在 [SECURITY-ACKNOWLEDGEMENTS.md](./SECURITY-ACKNOWLEDGEMENTS.md)（若报告者同意公开致谢）。

## 🔒 安全设计原则

本仓库的安全设计遵循以下原则（详见 [`rules.instructions.md`](./.github/instructions/rules.instructions.md) §1.1 Gate C）：

- **三层拦截**：仓库 `.github/hooks/safety-guard.json`（硬拦灾难命令）+ VS Code Autopilot（语义识别）+ 用户人工确认（Pause-and-Ask 白名单）
- **不可回滚动作必须用户裁决**：生产 DB 写入、DDL apply、删除数据、上线发布、真实付费 API
- **PreToolUse 钩子永远兜底**：即使关闭了 Autopilot 高级评估器，仓库 hook 仍拦 5 类灾难操作

## ⚠️ 使用者注意事项

本仓库的 `.vscode/settings.json` 包含以下"放行"配置（设计依据记录在项目记忆库中，拦截边界见 `.github/hooks/safety-guard.json`）：

```json
"chat.permissions.default": "autopilot",
"chat.tools.autoApprove": true,
"chat.tools.global.autoApprove": true,
"chat.autopilot.advanced.enabled": false
```

**含义**：在本工作区内放行 Copilot 工具调用，关闭 VS Code 的高级语义评估器（该层曾把 `pip install` 类依赖安装误判为高风险并拦截）。

**风险**：关闭高级评估器意味着 Copilot 可以更自主地执行命令，**灾难性兜底完全依赖仓库 `.github/hooks/safety-guard.json`**。如果你不信任本仓库的 hook 拦截规则，请删除上述四行配置恢复 VS Code 默认行为。

---

**Security is a shared responsibility.** 报告漏洞是你对社区最大的贡献。
