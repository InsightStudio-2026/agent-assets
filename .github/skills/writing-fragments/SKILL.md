---
name: writing-fragments
description: >
  通过追问从用户那里采集写作碎片：观点、场景、锐句、半成形想法，并追加到同一个文档，作为未来文章原料。
  Use when user wants to develop ideas before imposing structure, mentions "fragments"/"ideate"/"raw material",
  or asks 采集碎片/写作素材/先别定结构。
---

# 写作碎片采集（writing-fragments）

`<what-to-do>`

运行一个产出 fragments 的追问会话。围绕用户想写的东西持续追问。不要强加阶段、提纲或结构；这明确不在范围内。

当对话任一方产生 fragment 时，将其追加到同一个 markdown 文件。用户会在会话中编辑这个文件；每次写入前都必须重新读取，保留用户修改。

如果用户没有传入路径，只问一次文档保存在哪里，然后在本次会话剩余时间记住它。

从用户说的第一句话开始捕获 fragments，包括初始 prompt。

第一次写入时，只在顶部放一个带工作标题的 H1；标题之后可以改。不要加 metadata、TOC 或日期。

</what-to-do>

`<supporting-info>`

## 什么是 fragment

fragment 是任何可能进入最终文章的文本片段。它必须能被作者自己读懂，但不需要定义所有术语，也不需要让冷读者完全理解。判断标准是“这是不是一块好写作素材”，而不是“这是不是自洽论证”。

Fragments 刻意保持异质。以下都可以是 fragment：

- **一句锐句**：你想放进文章，但暂时不知道放在哪里。
- **一个观点**：附一行理由。
- **一个小场景**：发生过的事、代码片段、情境、类比。
- **一个半成形想法**：“X 感觉像 Y，之后展开。”
- **一句引用 / 对话 / 偶然听到的话**。
- **一组凭感觉相关的观察**。
- **抱怨、坦白、包袱**。

模型是小说家的日记：多年无结构的 noticing，之后被开采成原料。Fragments 就是 noticings。

## 文件格式

```markdown
## 工作标题 (Working title)

第一条写作碎片放在这里 (A first fragment lives here)。

它可以是多个段落，也可以包含列表、代码、引用——可以是任何碎片呈现出的自然形态
(It can be multiple paragraphs. It can include lists, code, quotes — whatever shape the fragment naturally takes)。

---

第二条写作碎片 (A second fragment)。

---

> 用户想要记录的引用文字 (A quoted line that the user wants to keep around)。

针对该引用的想法与反应 (A reaction to it)。

---

- 一组在感觉上相互关联的观察 (A cluster of related observations)
- 它们适合靠在一起展示 (That hang together by feel)
- 并且希望在空间上靠近 (And want to be near each other)

```

Fragments 之间用水平线分隔：`\n---\n`。正文内部不加 headings。不加 tags。除了追加顺序，不施加额外排序。

## 写作节奏

静默追加。不要为每个 fragment 单独请求许可。可以顺带说“这句我加进去”，但不要用保存确认打断对话。

每次写入前：从磁盘重新读取文件。用户可能已经编辑、重排或删除 fragments；必须保留这些修改。不要覆盖整个文件；只追加，除非用户要求编辑某个特定 fragment。

用户随时可以说“删掉上一条”“把那条改锋利点”“合并那两条”。这些都是一等指令。

</supporting-info>
