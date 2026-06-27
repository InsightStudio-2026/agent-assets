---
name: prototype
description: >
  构建可丢弃原型，在正式实现前回答设计问题。Routes between two branches: a runnable terminal app for
  state/business-logic questions, or several radically different UI variations toggleable from one route.
  Use when user wants to prototype, sanity-check a data model/state machine, mock up UI, explore design options,
  says "prototype this"/"let me play with it"/"try a few designs", or asks 做原型/试几个方案。
---

# 原型验证（prototype）

原型是**用来回答一个问题的可丢弃代码**。问题决定形状。

## 选择分支

从用户提示、周围代码或必要时向用户确认，先识别要回答的问题：

- **“这套逻辑 / 状态模型感觉对吗？”**→ [LOGIC.md](references/LOGIC.md)。构建一个很小的交互式终端 app，让状态机跑过纸面上难以推理的案例。

-**“这个界面应该长什么样？”**→ [UI.md](references/UI.md)。在单一路由生成几个结构上截然不同的 UI 变体，通过 URL search param 和底部浮动栏切换。

两个分支会产出完全不同的 artifact；选错分支会浪费整个原型。若问题确实模糊且用户不在线，按周围代码默认：后端模块 → logic；页面或组件 → UI。并在原型顶部写明假设。

## 两个分支都适用的规则

1.**从第一天起就是可丢弃代码，并明确标记。**原型代码放在接近真实使用位置的地方，方便理解上下文；但命名必须让读者一眼看出这是 prototype，不是 production。一次性 UI route 要遵守项目已有路由约定，不发明新的顶层结构。
2.**一个命令即可运行。**使用项目既有任务运行器支持的命令，例如 `pnpm <name>`、`python <path>`、`bun <path>`。用户不应需要记路径。
3.**默认不持久化。**状态存在内存里。持久化通常是原型要检查的对象，而不是依赖。如果问题明确涉及数据库，使用 scratch DB 或带有清晰 `PROTOTYPE — wipe me` 标记的本地文件。
4.**跳过打磨。**不写测试；除了让原型可运行所需的错误处理，不做额外抽象。目标是快速学习，然后删除。
5.**暴露状态。**每次 action 后（logic）或每次变体切换时（UI），打印或渲染完整相关状态，让用户看到变化。
6.**完成后删除或吸收。** 原型回答问题后，要么删除，要么把已验证的决定折入真实代码。不要让它在仓库里腐烂。

## 完成时

原型里唯一值得保留的是**答案**。把答案与它回答的问题一起记录到耐久位置：commit message、ADR、issue，或原型旁边的 `NOTES.md`。若用户在线，用快速对话确认；若不在线，留下占位，让用户或下一轮代理在删除原型前补上结论。

### 产出回流表

原型答案应根据触发场景沉淀到对应的耐久位置：

| 触发场景 | 答案去向 | 说明 |
| ---------- | ---------- | ------ |
| `/project-inception` Phase 7 Spike | 母本 §11 架构种子 或 §15 假设校验 | 验证结果直接回流到母本草案 |
| `/specs-write` design 阶段技术验证 | `design.md` 的技术决策段 | 原型结论作为设计依据 |
| 独立架构探索 | ADR（满足三条 ADR 条件时） | 不满足时记入 commit message |
| UI 方向探索 | `frontend-design` 的设计输入 | 确认方向后由 frontend-design 接手生产实现 |
| 纯好奇 / 学习 | 原型旁 `NOTES.md` 或直接删除 | 不强制回流 |

回流时只记录**结论与理由**，不复制原型代码。

## 支撑资源

- [LOGIC.md](./references/LOGIC.md)
- [UI.md](./references/UI.md)
