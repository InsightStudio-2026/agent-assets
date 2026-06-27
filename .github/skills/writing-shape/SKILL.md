---
name: writing-shape
description: >
  将 markdown 原料文件通过对话塑造成文章：选择论证或叙事模式，起草候选开头，逐块生长，并做最终编辑。
  Use when user has notes/fragments/a rough draft and wants help turning it into something publishable,
  or asks 把素材写成文章/整理草稿/成稿。
---

# 文章成稿（writing-shape）

`<what-to-do>`

用户已经传入或即将传入一个 markdown 原料文件。把它视为 input pile：可以是整齐的 fragments 列表，可以是一整堵无结构 prose，也可以是 transcript。格式不重要。做任何事之前，先从头到尾读完。

然后运行 shaping session，产出一个单独的 article document。不要编辑原料文件；对这个 skill 来说，原料文件只读。

如果用户没有说明文章保存在哪里，只问一次并记住路径。用户会在会话中编辑文章文件；每次写入前必须重新读取，保留用户修改。

</what-to-do>

`<supporting-info>`

## 循环

1. **读取原料堆**：完整读取 input file，形成对内容的整体感。
2. **选择 shaping mode**：如果文章在提出论证，用 argument mode；每一块都必须推进开头承诺的 thesis。如果文章是一段旅程，用 narrative mode；每个 beat 应设置场景、落下观点、提出问题，或把读者转向新位置。
3. **起草 2–3 个候选开头**：每个开头都应暗示不同 thesis、角度或起始 beat。全部展示。迫使用户选择一个，或拼成 hybrid。被选中的开头定义后文必须完成什么任务。
4. **逐块生长**：开头落定后，问：“基于这个开头，读者下一步需要听到什么？”从原料堆中抽取材料回答。讨论下一步应该是段落、列表、表格、callout、引用、代码块，还是叙事 beat。每个格式选择都必须有意识、能辩护。
5. **边走边追加到 article file**：不要批量攒稿。每个已同意的段落或 block 立即写入，让用户看到文章成形。
6. **循环第 4 步直到文章完成**：由用户决定何时完成。
7. **执行编辑 pass**：重读整篇文章，检查章节是否尊重信息依赖，收紧清晰度和流动，拆短承载过多任务的段落，删除不再值得存在的 block。

## 对话手感

这是反向 grilling session。ideation 阶段问的是“你真正注意到了什么？”这里问的是“这篇文章到底在论证什么？读者需要按什么顺序听到它？”要 push back。不要放过弱转场。如果一个段落不值得存在，就删掉。

持续使用这些具体动作（话术）：

- “这一段能给读者带来什么上一段没有的价值？” ("What does this paragraph do for the reader that the previous one didn't?")
- “如果我删掉这一句，文章会受到什么影响？” ("If I cut this, what breaks?")
- “这里应该写成一段长文，还是应该用列表？为什么写成长文？” ("Is this prose, or should it be a list? Why prose?")
- “这句话承担了两个任务——我们需要拆分它，还是只保留一个重点？” ("This sentence is doing two jobs — split it or pick one.")
- “开头承诺了要论证 X，但我们现在偏离到了 Y。我们要么重新把线索理顺，要么修改开头。” ("The opening promised X. We've drifted to Y. Either re-thread it or change the opening.")
- “要读懂这一节，读者必须先理解什么前提概念？” ("What does this depend on the reader already understanding?")
- “这是一个全新展开的脉络，还是把两个不同的段落强行粘在了一起？” ("Is this a new beat, or two beats glued together?")

## 从原料堆取材

把 raw material 当作 quarry，而不是 script。抽取 fragment，改写到适合周围段落的位置，再放进去。一个 fragment 可以被拆成多段、与另一个合并，或被 paraphrase。原料堆的工作是被开采；文章的工作是读起来像同一个声音。

如果原料堆缺少文章需要的东西，明确指出缺口：“这里需要一个例子，但原料里没有。现在给我一个，或者我们删掉这个 section。”

## 必须真的讨论的格式权衡

选择如何呈现一个 beat 时，和用户明确讨论这些权衡，不要静默决定：

- **长文段落 vs. 列表 (Prose vs. List)**：prose 承载论证；list 承载并列项。如果 items 并不真正并列，prose 更好。如果确实并列，list 更易扫读。
- **行内文字 vs. 标注框 (Inline vs. Callout)**：tips、warnings、asides 可以进 callout（`> [!TIP]`、`> [!NOTE]`），但只有当它们 inline 会真正打断主论证时才这么做。否则保持 inline。
- **表格 vs. 重复结构 (Table vs. Repeated Structure)**：同一形状重复 3 次以上，且字段相同，用 table。否则用带 bold lead 的 prose。
- **直接引用 vs. 意译 (Quote vs. Paraphrase)**：原话本身重要时 quote；只有想法重要时 paraphrase。
- **代码块 vs. 行内代码 (Code Block vs. Inline Code)**：多行、可运行或用于说明 → block。单个 token 或 identifier → inline。

## 写作节奏

每个 block 达成一致后，立即追加到 article file。每次写入前从磁盘重新读取文件；用户可能在轮次之间编辑过。不要盲目覆盖。如果用户要求重写某段，只原地编辑那一段，其他部分不动。

## 编辑 pass

文章形状完整后，从生长切换到编辑：

- **映射章节**：说明每个 section 的主要任务。
- **检查依赖顺序**：如果某节依赖读者尚未见过的概念、例子或 claim，重排或补上铺垫。
- **收紧段落**：提升清晰、连贯与流动。偏好短段；拆开承担多个任务的段落。
- **大结构改动前先确认**：不要静默原地大改。
- **保护用户修改**：每次写入前重新读取 article file。

## 质量闸口

编辑 pass 完成后，主动向用户提议：

- **追问审查**：对终稿使用 `grill-me` 做追问式压测——论证是否站得住脚？读者路径是否顺畅？每个 section 是否值得存在？
- **发布适配**：若文章需要发布到特定平台，建议使用 `/content-publishing-ops` 做格式适配与预览。

不强制——用户说"够了"就结束。

## 范围外

- **从原料堆外挖新 fragments**：原料堆就是输入。如果不完整，指出缺口，让用户补，或删掉该 section。
- **编辑 raw material file**。
- **发布、适配特定平台格式，或添加用户没要求的 frontmatter**。

</supporting-info>
