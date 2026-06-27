---
name: scaffold-exercises
description: >
  创建课程练习目录结构，包括 sections、problems、solutions 与 explainers，并确保通过 lint。
  Use when user wants to scaffold exercises, create exercise stubs, set up a new course section,
  or asks 脚手架练习/创建课程小节/生成练习目录。
---

# 课程练习脚手架（scaffold-exercises）

创建能通过 `pnpm ai-hero-cli internal lint` 的练习目录结构。只有在用户明确要求提交时，才执行 `git commit`。

## 目录命名

- **Sections**：位于 `exercises/` 下，格式为 `XX-section-name/`，例如 `01-retrieval-skill-building`。
- **Exercises**：位于 section 下，格式为 `XX.YY-exercise-name/`，例如 `01.03-retrieval-with-bm25`。
- **Section number** = `XX`，**exercise number**= `XX.YY`。

-**名称使用 dash-case**：小写 + 连字符。

## 练习变体

每个 exercise 至少需要以下子目录之一：

- `problem/`：学生工作区，包含 TODO。
- `solution/`：参考实现。
- `explainer/`：概念材料，不含 TODO。

创建 stub 时，除非计划另有说明，默认使用 `explainer/`。

## 必需文件

每个子目录（`problem/`、`solution/`、`explainer/`）都需要一个 `readme.md`，并满足：

- **非空**：必须有真实内容，只有一个标题行也可以。
- **没有坏链接**。

创建 stub 时，写一个带标题和说明的最小 readme：

```md
## 练习标题 (Exercise Title)

练习说明放在这里 (Description here)
```

如果子目录包含代码，也需要一个超过 1 行的 `main.ts`。但对 stub 来说，只有 readme 的 exercise 可以接受。

## 工作流

1. **解析计划**：提取 section 名、exercise 名和 variant 类型。
2. **创建目录**：使用编辑工具或 PowerShell `New-Item -ItemType Directory -Force -Path <path>` 为每个路径创建目录。
3. **创建 stub readme**：每个 variant 目录一个 `readme.md`，至少包含标题。
4. **运行 lint**：用 `pnpm ai-hero-cli internal lint` 验证。
5. **修复错误**：迭代直到 lint 通过。

## Lint 规则摘要

`pnpm ai-hero-cli internal lint` 会检查：

- 每个 exercise 有子目录：`problem/`、`solution/`、`explainer/`。
- 至少存在 `problem/`、`explainer/` 或 `explainer.1/` 之一。
- 主子目录中存在非空 `readme.md`。
- 没有 `.gitkeep` 文件。
- 没有 `speaker-notes.md` 文件。
- readme 中没有坏链接。
- readme 中没有 `pnpm run exercise` 命令。
- 除非是 readme-only，否则每个子目录需要 `main.ts`。

## 移动 / 重命名 exercises

重新编号或移动 exercises 时：

1. 使用 `git mv` 重命名目录以保留 git history；不要使用裸 `mv`。
2. 更新数字前缀，保持顺序。
3. 移动后重新运行 lint。

Example:

```powershell
git mv exercises/01-retrieval/01.03-embeddings exercises/01-retrieval/01.04-embeddings
```

## 示例：从计划创建 stub

给定计划：

```text

Section 05: Memory Skill Building

- 05.01 Introduction to Memory
- 05.02 Short-term Memory (explainer + problem + solution)
- 05.03 Long-term Memory

```

创建：

```powershell
New-Item -ItemType Directory -Force -Path "exercises/05-memory-skill-building/05.01-introduction-to-memory/explainer" | Out-Null
New-Item -ItemType Directory -Force -Path "exercises/05-memory-skill-building/05.02-short-term-memory/explainer" | Out-Null
New-Item -ItemType Directory -Force -Path "exercises/05-memory-skill-building/05.02-short-term-memory/problem" | Out-Null
New-Item -ItemType Directory -Force -Path "exercises/05-memory-skill-building/05.02-short-term-memory/solution" | Out-Null
New-Item -ItemType Directory -Force -Path "exercises/05-memory-skill-building/05.03-long-term-memory/explainer" | Out-Null
```

然后创建 readme stubs：

```text

exercises/05-memory-skill-building/05.01-introduction-to-memory/explainer/readme.md -> "# Introduction to Memory"
exercises/05-memory-skill-building/05.02-short-term-memory/explainer/readme.md -> "# Short-term Memory"
exercises/05-memory-skill-building/05.02-short-term-memory/problem/readme.md -> "# Short-term Memory"
exercises/05-memory-skill-building/05.02-short-term-memory/solution/readme.md -> "# Short-term Memory"
exercises/05-memory-skill-building/05.03-long-term-memory/explainer/readme.md -> "# Long-term Memory"

```
