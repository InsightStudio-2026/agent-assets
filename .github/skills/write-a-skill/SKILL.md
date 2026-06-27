---
name: write-a-skill
description: >
  创建符合结构约定、渐进披露和支撑资源组织规则的新 agent skill。
  Use when user wants to create/write/build a new skill, or asks 创建 skill/编写技能/新增代理能力。
---

# 编写 Skill（write-a-skill）

## 流程规则表

| ID | 步骤名称 | 核心动作 | 确认要素与核验重点 |
| ---- | ---------- | ---------- | ------------------- |
| R-SKILL-1 | 收集需求 | 向用户明确任务边界与用例范围 | 覆盖领域、核心用例、是否需执行脚本、参考材料 |
| R-SKILL-2 | 起草 Skill | 创建物理资产文件与辅助脚本 | `SKILL.md`入口、低频细节拆分支撑文件、确定性脚本 |
| R-SKILL-3 | 审查验证 | 与用户对齐细节并进行验证 | 校验用例覆盖度、细节完整度、可读性，通过完整性校验 |

## Skill 目录契约

- `skill-name/`：Skill 根目录
- `skill-name/SKILL.md`：主要入口指令（必需）
- `skill-name/REFERENCE.md`：详细参考文档（可选）
- `skill-name/EXAMPLES.md`：用法示例（可选）
- `skill-name/scripts/`：辅助实用脚本目录（可选）
- `skill-name/scripts/helper.js`：特定实用脚本（可选）

## `SKILL.md` 模板

```md
---
name: skill-name
description: 简短说明能力。Use when [specific triggers]. 可补充中文触发词。
---

## Skill Name

## Quick start

[最小可行工作示例 (Minimal working example)]

## Workflows

[针对复杂任务的、带检查清单的逐步过程说明 (Step-by-step processes with checklists for complex tasks)]

## Advanced features

[链接到独立拆分的文件，例如：请参阅 [REFERENCE.md](REFERENCE.md) (Link to separate files: See [REFERENCE.md](REFERENCE.md))]
```

## 描述信息要求 (Description Requirements)

`description` 是代理决定是否加载 skill 时唯一稳定可见的内容。它会和其他已安装 skill 的描述一起出现在系统提示中。代理读取这些描述，并根据用户请求选择相关 skill。

**目标**：给代理刚好足够的信息，让它知道：

1. 这个 skill 提供什么能力。
2. 何时 / 为什么触发它：具体关键词、上下文、文件类型。

**格式**：

- 最多 1024 字符。
- 使用第三人称描述。
- 第一句说明它做什么。
- 第二句使用 `Use when [specific triggers]`，并可补充中文触发词。

**好例子**：

```text

Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDF files or when user mentions PDFs, forms, or document extraction.

```

**坏例子**：

```text

Helps with documents.

```

坏例子无法让代理区分它和其他文档类 skill。

## 何时添加脚本

以下情况添加 utility scripts：

- **操作是确定性的**：验证、格式化等。
- **同类代码会被重复生成**。
- **错误需要显式处理**。

脚本相比每次生成代码更省 token，也更可靠。

## 何时拆分文件

以下情况拆成单独文件：

- **入口过长**：`SKILL.md` 已明显难以快速阅读。
- **内容属于不同子领域**：例如 finance schema 与 sales schema。
- **高级能力很少使用**。

## 审查清单

起草后确认：

- [ ] `description` 包含触发条件：`Use when...`。
- [ ] `SKILL.md` 保持入口性质；低频细节拆到支撑文件。
- [ ] 没有时间敏感信息。
- [ ] 术语一致。
- [ ] 包含具体例子。
- [ ] 引用层级尽量只深入一层。
