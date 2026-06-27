---
name: review
description: >
  从固定点（commit、branch、tag 或 merge-base）审查变更，分离 Standards、Spec、Verification 三条轴线；
  命中高风险 diff 时按 multi-axis-protocol 扩展 Risk Gates、Architecture、Operability、Authorship / Provenance。
  Use when user wants to review a branch/PR/work-in-progress changes,
  asks to "review since X", or says 审查/评审这批改动。
context: fork
argument-hint: "审查哪个分支/commit？"
---

# 变更审查（review）

审查用户给出的固定点与 `HEAD` 之间的 diff，并把结论分成三个独立区块：

- **Standards**：代码是否符合仓库中已文档化的工程规范。
- **Spec**：变更是否忠实实现来源 issue / PRD / spec。
- **Verification**：有哪些可运行检查增强或削弱对 diff 的信心。
- **Risk Gates / Architecture / Operability / Authorship-Provenance**：仅在 diff 命中 `.github/skills/review/multi-axis-protocol.md` 触发规则时追加，不替代前三轴。

Standards 与 Spec 是两条不同判断轴。若当前环境支持子代理，二者应并行运行，避免互相污染上下文；然后由本 skill 汇总。Verification 只是机器检查状态，不是第三份主观审查。

issue tracker 应由仓库初始化提供；若 `docs/agents/issue-tracker.md` 缺失，先考虑运行 `/repo-agent-setup`。

## 流程

### 1. 固定比较基准

用户说的就是固定点：commit SHA、branch、tag、`main`、`HEAD~5` 等。不要自作主张替换。如果用户没有指定，问：“要对哪个基准审查？branch、commit，还是 `main`？”拿到基准前不要继续。

记录一次 diff 命令：`git diff<fixed-point>...HEAD`。三点语法表示从 merge-base 比较。同时记录提交列表：`git log<fixed-point>..HEAD --oneline`。

### 2. 找来源 spec

按顺序查找上游依据：

1. commit message 中的 issue 引用，例如 `#123`、`Closes #45`、GitLab `!67`；按 issue tracker 工作流读取。
2. 用户参数里传入的路径。
3. `docs/`、`specs/`、`.scratch/` 下与 branch 或 feature 名匹配的 PRD / spec。
4. 若找不到，问用户 spec 在哪里。若用户确认没有 spec，则跳过 **Spec** 轴，并报告 `no spec available`。

### 3. 找 Standards 来源

任何描述代码应如何书写的仓库文件都算规范来源。常见位置：

- `AGENTS.md`、`AGENTS.md`
- `CONTRIBUTING.md`
- `CONTEXT.md`、`CONTEXT-MAP.md`、各上下文目录中的 `CONTEXT.md`
- `docs/adr/`；架构决策也是规范
- `.editorconfig`、`eslint.config.*`、`biome.json`、`prettier.config.*`、`tsconfig.json`；机器执行的规范只记录，不重复人工检查
- 根目录或 `docs/` 下的 `STYLE.md`、`STANDARDS.md`、`STYLEGUIDE.md` 等

收集文件清单。Standards 审查必须引用具体规范来源。

### 4. 找 Verification 信号

收集本仓库正常应运行的检查。常见来源：

- `package.json`、`pyproject.toml`、`Cargo.toml`、`Makefile`、任务运行器配置
- CI workflow 文件
- README / CONTRIBUTING / AGENTS / CLAUDE 指令
- 当前会话已经运行过的命令

每个检查报告为：

- **Passed**：已运行且通过。
- **Failed**：已运行但失败。
- **Not run**：存在相关命令但未运行。
- **Unknown**：找不到权威命令。

不要手动复查工具已经负责的细节。如果存在 formatter、linter、typechecker，要么在合适时运行，要么标为 Not run。

### 5. 分轴审查

如环境支持子代理，同时启动 Standards 与 Spec 两个审查者；否则顺序执行，但必须保持结论分离。

**Standards 审查输入**：

- 完整 diff 命令与 commit 列表。
- 第 3 步找到的规范来源文件。
- 下方严重性词表。
- 任务：阅读规范文档，再阅读 diff。逐文件 / hunk 报告违反已文档化规范的地方，引用规范来源（文件 + 规则）。区分硬性违反与判断题。跳过工具已自动覆盖的格式问题。每条标严重性。

**Spec 审查输入**：

- 完整 diff 命令与 commit 列表。
- spec 路径或内容。
- 下方严重性词表。
- 任务：阅读 spec，再阅读 diff。报告：(a) spec 要求但缺失或部分实现的内容；(b) diff 中未被要求的行为，即 scope creep；(c) 看似实现但实现方式错误的需求。每条引用 spec 原文行并标严重性。

若没有 spec，跳过 Spec 审查并在最终报告说明。

严重性词表：

- **Blocker**：不得合并；违反 spec、打破文档约束或制造严重风险。
- **Must fix**：合并前应修复，但不是立即阻断。
- **Should fix**：值得修复，能实质降低风险或维护成本。
- **Question**：需要维护者判断或上下文缺失。
- **Nit**：小问题，不应阻塞合并。

### 6. 汇总

最终报告使用 `## Standards`、`## Spec`、`## Verification` 三个标题。若命中 `.github/skills/review/multi-axis-protocol.md`，在三轴后追加 `## Risk Gates`、`## Architecture`、`## Operability`、`## Authorship / Provenance` 中适用的区块。不要合并或重排 Standards 与 Spec 的发现；它们刻意分离，方便用户独立判断。

结尾用一句话总结：每个区块发现数量、最高严重性、验证信号是 strong、weak 还是 missing。

## 为什么必须分区

一次变更可能在一条轴线上通过、另一条轴线上失败：

- 完全遵守规范但实现了错误需求 → **Standards pass, Spec fail**。
- 完全实现 issue 但破坏项目约定 → **Spec pass, Standards fail**。

分开报告能防止一条轴掩盖另一条轴。单独报告 Verification，则能显示机器信心，同时不假装它能取代审查判断。

## 发现问题后的路由

review 只审查、不修复。发现问题后按以下规则分流：

| 发现类型 | 推荐路由 | 说明 |
| ---------- | ---------- | ------ |
| 实现偏离 spec 但修复简单 | `tdd` / direct fix | 明确一句话描述偏离点 |
| spec 本身有缺陷或遗漏 | `/specs-write` | 带上 spec 路径与具体缺陷描述 |
| 架构边界、模块职责、接口设计问题 | `/architecture-audit` | 引用 diff 中暴露问题的具体 hunk |
| 安全、隐私、权限、数据风险 | `/security-privacy-audit` | 标明风险级别与影响面 |
| 影响面未知的 bug | `/bug-audit` | 先审计再修 |
| 母本 / SSOT 与实现冲突 | `/grill-with-docs` | 术语或领域关系冲突 |
| 测试缺口但代码行为正确 | `tdd` 补测试 | 标注哪些路径缺覆盖 |

review 报告结尾应明确列出所有 Blocker / Must fix 发现的推荐路由，不留"需要修复"的模糊结论。

## 支撑资源

- [multi-axis-protocol.md](./protocols/multi-axis-protocol.md)
