---
name: zoom-out
description: >
  要求代理拉高视角，给出更广上下文或更高层抽象。Use when you're unfamiliar with a section of code,
  need to understand how it fits into the bigger picture, or asks 放大视角/讲整体脉络。
disable-model-invocation: true
---

# 拉高视角（zoom-out）

我还不熟悉这片代码。请上升一层抽象，用项目领域词汇画出相关模块、调用者、数据流和责任边界的地图。

## 输出格式

按以下四层从近到远输出：

1. **当前代码**：这段代码做什么、对谁负责（≤ 3 句）。
2. **调用链**：谁调用它、它调用谁。用 `A → B → C` 箭头链表示。
3. **模块边界**：它属于哪个模块/上下文，模块的公共接口是什么，邻居模块有哪些。
4. **系统全景**：这个模块在整个系统中扮演什么角色（一句话）。

每层只写该层需要的信息，不混层。如有 `CONTEXT.md` 或 ADR，引用其中的术语和决策。

## 不做的事

- 不改代码。
- 不给优化建议（除非用户追问）。
- 不展开实现细节——zoom-out 的目的是缩小，不是放大。
