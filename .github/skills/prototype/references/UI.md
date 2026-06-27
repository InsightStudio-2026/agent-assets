# UI Prototype / UI 原型

在单一路由生成**几个结构上截然不同的 UI 变体**，并用底部浮动栏切换。用户在浏览器里来回比较，选一个，或从多个方案里偷取局部，然后丢弃其余部分。

如果问题是逻辑 / 状态，而不是“看起来怎样”，分支选错了；使用 [LOGIC.md](LOGIC.md)。

## 何时使用这种形状

- “这个页面应该长什么样？”
- “正式提交前，我想看几个 dashboard 方案。”
- “给 settings screen 试一个不同布局。”
- 任何用户原本会在脑子里花一天比较三个模糊 mockup 的场景。

## 两种子形状：强烈优先 A

UI 原型贴着真实 app 更容易判断：真实 header、真实 sidebar、真实数据、真实密度。单独的 throwaway route 是真空；每个变体在孤立状态都可能看起来不错。只要存在合理的既有页面可承载变体，默认使用子形状 A。只有原型确实没有附近归宿时，才使用子形状 B。

### 子形状 A：调整既有页面（优先）

route 已经存在。变体渲染在**同一路由**，由 `?variant=` URL search param 控制。既有 data fetching、params、auth 全部保留；只切换渲染子树。除非有明确理由，否则默认选择它。

如果原型对象还没有独立页面，但**自然会生活在某个既有页面内部**，例如 dashboard 新区块、settings 新卡片、既有 flow 新步骤，也仍然是子形状 A。把变体挂载到宿主页面内部。

### 子形状 B：新页面（最后手段）

只有当被原型化的对象确实没有既有页面可容纳时使用，例如全新的顶层 surface，或无法合理嵌入任何页面的 flow。

按项目已有路由约定创建**一次性 route**；不要发明新的顶层结构。命名必须明显表示 prototype，例如 path 或文件名包含 `prototype`。同样使用 `?variant=` 模式。

采用子形状 B 前，先自检：真的没有页面可以嵌入吗？空 route 会掩盖设计问题；填充过的真实页面才会暴露问题。

两种子形状的底部浮动栏相同。

## 流程

### 1. 写明问题并选择 N

默认生成 **3 个变体**。超过 5 个后通常不再是“截然不同”，而是噪音；上限为 5。

在原型位置或文件顶部注释写一行计划：

> "Three variants of the settings page, switchable via `?variant=`, on the existing `/settings` route."

无论用户是否在线，这都能留下可检查假设。

### 2. 生成结构上不同的变体

起草每个变体。每个变体都必须服从：

- **页面目的与可访问数据**-**项目组件库 / 样式系统**：TailwindCSS、shadcn、MUI、plain CSS 等
- **清晰导出的组件名**：例如 `VariantA`、`VariantB`、`VariantC`

变体必须**结构上不同**：布局不同、信息层级不同、主 affordance 不同，而不只是颜色不同。三个稍微调过的 card grid 不是 UI 原型，只是壁纸。如果两个草稿太相似，明确要求其中一个“不要使用 card grid”并重做。

### 3. 串联变体

在 route 上创建单个 switcher 组件：

```tsx
// 伪代码：按项目框架调整
const variant = searchParams.get('variant') ?? 'A';
return (
  <>
    {variant === 'A' && <VariantA {...data} />}
    {variant === 'B' && <VariantB {...data} />}
    {variant === 'C' && <VariantC {...data} />}
    <PrototypeSwitcher variants={['A','B','C']} current={variant} />
  </>
);
```

对子形状 A（既有页面）：所有既有 data fetching 保持在 switcher 上方；只有渲染子树随 variant 改变。

对子形状 B（新页面）：在 `/prototype/<name>` 下的一次性 route 挂载同一个 switcher。

### 4. 构建底部浮动切换器

屏幕底部居中的小型 fixed bar，包含三部分：

- **Left arrow**：切到上一个变体，循环。
- **Variant label**：显示当前变体 key；如果变体导出名称，也显示名称，例如 `B — Sidebar layout`。
- **Right arrow**：切到下一个变体，循环。

行为：

- 点击箭头更新 URL search param；使用框架 router，例如 Next 的 `router.replace` 或 React Router 的 `navigate`，让变体可分享、刷新后稳定。
- 键盘 `←` / `→` 也可切换。焦点在 `<input>`、`<textarea>` 或 `[contenteditable]` 内时，不要拦截方向键。
- 视觉上与页面区分明显，例如高对比 pill、轻 shadow，让它显然不是被评估设计的一部分。
- 生产构建隐藏：用 `process.env.NODE_ENV !== 'production'` 或等价检查 gate，避免原型误合并后把切换栏发给用户。

把 switcher 放到一个共享组件中，便于两种子形状复用。位置遵守项目 shared UI 约定。

### 5. 交给用户

给出 URL 和 `?variant=` key。用户之后可以自己切换。最有价值的反馈通常是：**“我要 B 的 header，但要 C 的 sidebar。”**这才是真正想要的设计。

### 6. 捕获答案并清理

一旦某个变体胜出，写下是哪一个以及为什么：commit message、ADR、issue，或用户不在线时原型旁的 `NOTES.md`。然后：

-**子形状 A**：删除失败变体和 switcher，把胜出方案折回既有页面。

- **子形状 B**：把胜出方案提升为真实 route，删除一次性 route 和 switcher。

不要把 variant 组件或 switcher 留在仓库里。它们很快腐烂，并误导下一个读者。

## 反模式

- **只在颜色或文案上不同的变体。**那是微调，不是原型。真正的变体会在结构上分歧。

-**变体之间共享过多代码。**共享 `<Header>` 可以；共享 `<Layout>` 会破坏目的。每个变体都应能丢弃布局。
-**把变体接到真实 mutation。**只读原型可以。若变体必须 mutate，指向 stub；问题是“它应该长什么样”，不是“后端能不能工作”。
-**把原型直接推成生产代码。** 变体是在原型约束下写的：无测试、最小错误处理。折回真实代码时应按生产标准重写。
