---
name: gsap-plugins
description: Official GSAP skill for GSAP plugins — registration, ScrollToPlugin, ScrollSmoother, Flip, Draggable, Inertia, Observer, SplitText, ScrambleText, SVG and physics plugins, CustomEase, EasePack, CustomWiggle, CustomBounce, GSDevTools. Use when the user asks about a GSAP plugin, scroll-to, flip animations, draggable, SVG drawing, or plugin registration.
license: MIT
user-invocable: false
---

# GSAP 插件集开发指南

## 何时使用此 Skill

在项目中使用或审查涉及 GSAP 官方扩展插件的代码时，应用此 Skill：注册插件、滚动跳转（scrollTo）、Flip卡片布局过渡、DOM拖拽（draggable）、SVG动效（DrawSVG、MorphSVG、MotionPath 轨迹动画）、文本特效（SplitText、ScrambleText）、物理碰撞、自定义缓动插件（CustomEase、EasePack、CustomWiggle、CustomBounce）或 GSDevTools 调试面板。注意，ScrollTrigger 拥有独立的技能指南 (gsap-scrolltrigger)。

**相关技能：**补间与时间轴核心基础请参考**gsap-core**；ScrollTrigger 滚动触发请参考 **gsap-scrolltrigger**；React 下的生命周期与自动销毁请参考 **gsap-react**。

## 许可说明与依赖安装（重要）

**所有的 GSAP 官方插件现在完全免费，包括商业用途！** 自 Webflow 收购 GSAP 之后，Club GSAP 的收费专有机制已彻底成为历史，**没有任何插件再需要专门购买会员、获取许可证 Key 或配置 private Auth token** —— 这包括原先仅属于 Club 专有的高级插件（**SplitText**、**MorphSVG**等）。

- ✅**直接一键安装**：直接从 NPM 官方公开源安装 gsap 包：`npm install gsap`。所有的插件现在均默认内置其中 —— 开发者直接通过模块导入：`gsap/SplitText`、`gsap/MorphSVGPlugin` 即可，零成本无缝调用。
- ❌ **严禁生成私有 npmrc**：禁止在工作区中编写带 GreenSock token 的 `.npmrc` 配置文件，禁止推荐私有的 `npm.greensock.com` 仓库源。这些做法已彻底过时。

## 注册插件

在项目中，必须在使用前**全局显式注册一次**各插件，以便 GSAP 核心和打包器（Bundlers，如 Webpack/Vite/Rollup）能顺利识别并进行 Tree-shaking 优化：

```javascript
import gsap from "gsap";
import { ScrollToPlugin } from "gsap/ScrollToPlugin";
import { Flip } from "gsap/Flip";
import { Draggable } from "gsap/Draggable";

gsap.registerPlugin(ScrollToPlugin, Flip, Draggable);
```

- ✅ 必须在使用任何插件相关的动画或 API 之前进行全局注册。
- ✅ 在 React 项目中，应在全局顶级（App.js 头部或 useGSAP 执行前）仅注册一次；严禁在频繁重渲染的组件体内注册。注意：`useGSAP` 钩子本身也是一个需要在使用前先注册的插件。

## 滚动

### ScrollToPlugin

用于平滑滚动当前窗口（Window）或某个带 scroll 的局部 DOM 容器。非常适合实现“滚动到元素”或“滚动到绝对位置”，而无需 ScrollTrigger。

```javascript
gsap.registerPlugin(ScrollToPlugin);

gsap.to(window, { duration: 1, scrollTo: { y: 500 } });
gsap.to(window, { duration: 1, scrollTo: { y: "#section", offsetY: 50 } });
gsap.to(scrollContainer, { duration: 1, scrollTo: { x: "max" } });
```

### ScrollToPlugin — 核心 vars 配置项（scrollTo 对象内）

| 配置项 | 详细作用说明 |
| -------- | ------------- |
| `x`, `y` | 目标滚动的绝对像素坐标（数值），或传入 `"max"` 代表滚动到最大可滚动边界。 |
| `element` | 选择器或 DOM 节点引用，直接平滑定位该元素（等同于 scrollIntoView）。 |
| `offsetX`, `offsetY` | 滚动的目标偏置像素（可实现顶部导航栏遮挡保护）。 |

### ScrollSmoother

官方原装的高性能页面级惯性平滑滚动包裹器（实现顺滑物理惯性阻尼效果）。需要 ScrollTrigger 作为前置底层依赖，且需要固定的三层 DOM 结构支撑（内容 Wrapper + 平滑滚动 Wrapper）。在需要平滑、惯性流畅滚动时选用。参考 GSAP 官方文档进行设置，注册时必须排在 ScrollTrigger 的注册之后。其标准的 DOM 结构如下：

```html
<body>
 <div id="smooth-wrapper">
  <div id="smooth-content">
   <!--- 所有的页面内容放这里 --->
  </div>
 </div>
 <!-- 注意：任何带有 position: fixed 的浮动元素可以放在 wrapper 外部 --->
</body>
```

## DOM / UI

### Flip

FLIP 动画规范（First, Last, Invert, Play）。
步骤：通过 `Flip.getState()` 记录一批元素当前的布局位置状态 → 执行任何会改变 DOM 的逻辑（如改变 flex 排序、改 class、改变父容器） → 调用 `Flip.from(state)` 让元素极其丝滑地从旧物理状态过渡到新状态。非常适合在两个布局状态之间进行过渡动画（如列表与网格切换、卡片折叠与展开）。

```javascript
gsap.registerPlugin(Flip);

const state = Flip.getState(".item");
// 执行任何改变 DOM 结构的逻辑 (如重新排序、添加/移除节点、改变样式类)
Flip.from(state, { duration: 0.5, ease: "power2.inOut" });
```

### Flip — 核心 vars 配置项

| 配置项 | 详细作用说明 |
| -------- | ------------- |
| `absolute` | 在过渡时自动将被动画元素设为 `position: absolute`，防止挤压相邻元素造成布局闪烁（默认：`false`）。 |
| `nested` | 当为 `true` 时，测绘过程会向内深入测量一级子节点（非常适合父子嵌套位移）。 |
| `scale` | 设为 `true` 代表通过 scale 替代 width/height 进行过渡（性能极佳，能防止字体拉伸变形）。默认：`true`。 |
| `simple` | 设为 `true` 代表仅执行位置和缩放变换，不重新测量更复杂的样式。 |
| `duration`, `ease` | 传统 Tween 的缓动与时长参数。 |

#### 更多信息 (More information)

`<https://gsap.com/docs/v3/Plugins/Flip>`

### Draggable

使任意 DOM 元素瞬间支持极其流畅的手势拖拽、3D 旋钮旋转、或者是带有物理甩出抛物线的交互。非常适合制作滑块、卡片划过、拼图重排和手势交互。

```javascript
gsap.registerPlugin(Draggable, InertiaPlugin);

Draggable.create(".box", { type: "x,y", bounds: "#container", inertia: true });
Draggable.create(".knob", { type: "rotation" });
```

### Draggable — 核心 vars 配置项

| 配置项 | 详细作用说明 |
| -------- | ------------- |
| `type` | 拖拽方向：`"x"`, `"y"`, `"x,y"` (任意方向), `"rotation"` (3D旋转控制), `"scroll"` (拖拽内容物进行 scroll)。 |
| `bounds` | 拖拽的硬性物理边界限制，可传入选择器、DOM 节点、或边界坐标：`{ minX, maxX, minY, maxY }`。 |
| `inertia` | 物理甩动惯性。设为 `true` 后，松开鼠标元素会因惯性滑行衰减停止（需要 `InertiaPlugin` 支持）。 |
| `edgeResistance` | 0–1 之间；当超出拖拽边界时的物理阻力（1 代表无法拉出，0.5 代表能稍微拉出体验橡皮筋感）。 |
| `cursor` | 拖拽时 CSS 的 cursor 鼠标指针样式。 |
| `onDragStart`, `onDrag`, `onDragEnd` | 核心手势拖拽回调生命周期。 |
| `onThrowUpdate`, `onThrowComplete` | 开启惯性甩动后，惯性滑动中的高频更新与完毕回调。 |

### Inertia (InertiaPlugin)

与 Draggable 结合用于松手后的高级物理惯性模拟，或者用于在自定义业务中追踪任意 JS 对象的某个变量的当前运动速度（Velocity），并一键生成阻尼刹车式的优雅减速过渡。与 Draggable 结合使用并开启 `inertia: true` 时必须将其进行注册：

```javascript
gsap.registerPlugin(Draggable, InertiaPlugin);
Draggable.create(".box", { type: "x,y", inertia: true });
```

或者主动对某属性进行速度追踪：

```javascript
InertiaPlugin.track(".box", "x");
```

随后通过 `"auto"` 配置项，使其基于当前物理速度顺滑减速到刹车：

```javascript
gsap.to(obj, { inertia: { x: "auto" } });
```

### Observer

统一且抽象化多端的 pointer/scroll 事件监听（PC 滚轮、PC 拖拽、移动端划过 Touch 等手势）。非常适合用来制作全屏滑块，在不把动画直接绑定到滚轮距离的情况下（如 ScrollTrigger），直接监听用户的 swipe（划过）方向并执行逻辑：

```javascript
gsap.registerPlugin(Observer);

Observer.create({
  target: "#area",
  onUp: () => {},
  onDown: () => {},
  onLeft: () => {},
  onRight: () => {},
  tolerance: 10
});
```

### Observer — 核心 vars 配置项

| 配置项 | 详细作用说明 |
| -------- | ------------- |
| `target` | 手势事件监听的目标容器选择器或节点。 |
| `onUp`, `onDown`, `onLeft`, `onRight` | 用户在对应方向完成超过 `tolerance` 距离的手势操作时的回调。 |
| `tolerance` | 触发阈值像素，默认 10px。 |
| `type` | 监听的事件类型：`"touch"`, `"pointer"`, 或 `"wheel"`，默认为全部包含 (`"touch,pointer"`)。 |

## Text

### SplitText

将目标 DOM 中的文本，自动拆分为一个一个独立的单字（characters）、单词（words）和单行（lines），并将每个单字包裹在独立的 `<div>` 或 `<span>` 元素中。
这是实现打字机效果、单字依次渐显的终极核心插件。返回包含 `chars`, `words`, `lines` 的实例对象（当配置了 `mask` 时还包含 `masks` ）。离开页面或组件卸载时，可调用 **revert()** 彻底抹除生成的 div 并恢复原始文本标签，或者让 `gsap.context()` 自动托管 revert。支持与 `gsap.context()`、`matchMedia()` 以及 `useGSAP()` 无缝结合。API 格式：**SplitText.create(target, vars)**（target 支持选择器、节点或数组）。

```javascript
gsap.registerPlugin(SplitText);

const split = SplitText.create(".heading", { type: "words, chars" });
gsap.from(split.chars, { opacity: 0, y: 20, stagger: 0.03, duration: 0.4 });
// 在完成或卸载时：手动调用 split.revert()，或者交由 gsap.context() 自动执行 cleanup 销毁
```

支持配置 **onSplit()**(v3.13.0+ 引入) 与**autoSplit: true**，当触发浏览器窗口 resize、窗口宽度拉伸或自定义字体加载完毕导致文字高度改变时，**自动重新测绘并重新拆分文字**，完美杜绝因页面换行产生难看的文字排版 Bug：

```javascript
SplitText.create(".split", {
  type: "lines",
  autoSplit: true,
  onSplit(self) {
    return gsap.from(self.lines, { y: 100, opacity: 0, stagger: 0.05, duration: 0.5 });
  }
});
```

### SplitText — 核心 vars 配置项（SplitText.create vars）

| 配置项 | 描述 |
| -------- | ------------- |
| **type** | 拆分颗粒度：逗号隔开 `"chars"`, `"words"`, `"lines"`。默认值为 `"chars,words,lines"`。出于性能考虑，建议**仅拆分需要动画的级别**（例如只需按行渐显时，只拆 `"words, chars"` 即可）。避免不拆 words/lines 直接单拆 chars，或者通过配置 **smartWrap: true**来防止中文产生异常断句折行 Bug。 |
| **charsClass**`<br>`**wordsClass**`<br>`**linesClass** | 拆分后生成的每个 DOM 节点包裹器的 CSS 类名。支持在后缀追加 `"++"` 自动注册自增 Class（如 `linesClass: "line++"` 会自动生成 `line1`, `line2`, `line3`）。 |
| **aria** | 无障碍（A11y）支持。默认为 `"auto"`：它会在原始 DOM 上添加 `aria-label` 声明，并在生成的单字/行/词节点上添加 `aria-hidden`，这样屏幕阅读器依然能够流利阅读整句大意，而不会生硬地一个字一个字断句；设为 `"none"` 代表跳过不修改 A11y 树。若需要暴露链接等嵌套语义，可配置 `"none"` 并手动通过 Screen-reader-only 创建副本。 |
| **autoSplit** | 自适应自动重拆分。当视口尺寸改变、DOM 容器拉伸、或网络自定义字体加载完成后，自动安全回滚并重新拆分。**必须在 onSplit 回调中生成补间动画**，确保重新拆分时它们能定位到新的 DOM 元素；在 **onSplit()**中**return**动画句柄即可实现自动 revert 和进度自适应同步。 |
| **onSplit(self)** | 拆分完毕以及每次由于自适应导致重拆分时的生命周期回调。接收当前 SplitText 实例。在其内部返回一个 GSAP 补间或时间轴，即可在重拆分时自动进行动画进度和状态的重置同步。 |
| **mask** | 蒙版/遮罩裁剪。可设为 `"lines"`, `"words"`, 或 `"chars"`。它会自动在被动画字体的外层再包裹一个带有 `overflow: clip` 的裁剪 DOM（暴露在 `split.masks` 数组上），非常适合制作文字凭空「擦除渐显」出的效果。只支持单种类型，可通过 `.classname-mask` 选中。 |
| **tag** | 包裹器的 HTML 标签名。默认为 `"div"`。若需行内元素，传入 `"span"`（注意：部分浏览器不支持对 inline 行内元素应用位移或旋转 transform 变换）。 |
| **deepSlice** | 深层切片测量。默认为 `true`（默认值）。它会确保即使文本中存在 `<strong>` 等嵌套标签，换行时也能精准切碎，防止容器产生不合常规的垂直拉伸。 |
| **ignore** | 声明需要忽略、不进行任何拆分操作的特定子元素选择器（例如 `ignore: "sup"`，防止公式上标等被切碎）。 |
| **smartWrap** | 仅拆 chars 时自动开启，可确保中西文混合排版时不会在单词中央产生不合规范的暴裂折行。如果 words 或 lines 已经被拆分，则忽略此配置。默认 `false`。 |
| **wordDelimiter** | 词边界切分符。默认为 `" "` 英文空格，可传入自定义字符、正则、或 `{ delimiter: RegExp, replaceWith: string }` 执行特殊切分。 |
| **prepareText(text, parent)** | 文本预处理。在拆分之前接收原始文本和父级 DOM，返回被修改的文本（例如在无空格的特殊语系中注入断句符）。 |
| **propIndex** | 设为 `true` 后，会自动在每个拆分节点上注入带 Index 编号的 CSS 自定义变量（如 `--word: 1`, `--char: 2`）。 |
| **reduceWhiteSpace** | 自动合并并坍塌连续的空格，默认 `true`。从 v3.13.0 起，也会遵循物理换行并在 `<pre>` 换行处自动注入 `<br>`。 |
| **onRevert** | 当该实例执行 revert() 彻底回滚还原时的回调函数。 |

**SplitText 最佳实践 tips**：

- 为防止文字在拆分为 DOM 的瞬间因为字距微调变化（Kerning Shift）产生轻微的左右文字抖动，强烈建议在被拆分文字的 CSS 上加入以下属性：`font-kerning: none; text-rendering: optimizeSpeed;`。
- 避免对使用了 `text-wrap: balance` 的排版应用 SplitText，两者会产生冲突。
- 注意：SplitText **不支持 SVG 内部的 `<text>` 标签**。

**Learn more:**[SplitText](https://gsap.com/docs/v3/Plugins/SplitText/)

### ScrambleText

实现无序随机乱码闪烁、并逐渐重组还原呈现出真实文案的科技感打字机动效。

```javascript
gsap.registerPlugin(ScrambleTextPlugin);

gsap.to(".text", {
  duration: 1,
  scrambleText: { text: "New message", chars: "01", revealDelay: 0.5 }
});
```

## SVG

### DrawSVG (DrawSVGPlugin)

通过高精度操控 SVG 样式的 `stroke-dashoffset` / `stroke-dasharray` 笔画间距，实现像“手绘勾勒路线”的描边绘制动画。支持 `<path>`、`<line>`、`<polyline>`、`<polygon>`、`<rect>`、`<ellipse>` 等所有 SVG 基础描边图元。**drawSVG 核心机制值**：描述的是**当前可见描边部分的起止比例段**（start 和 end），而非动画时间的百分比。格式为 `"起始比例 终止比例"`。例如：`"0% 100%"` 代表整个描边完整满额显示；`"20% 80%"` 代表仅在 20% 到 80% 范围内绘制线条（两端留空）。补间动画会自动将该元素从**当前段**平滑过渡到配置的**目标段**。如果传入单个值（例如 `0`、`"100%"`）代表起始比例锁定为 0，其中 `"100%"` 等价于 `"0% 100%"`。

### 前置条件：被动画元素必须拥有合法的描边色和宽度（在 SVG 属性或 CSS 中配置 `stroke` 与 `stroke-width`），否则将没有任何线条被绘制渲染

```javascript
gsap.registerPlugin(DrawSVGPlugin);

// 从无到有绘制出整根线条
gsap.from("#path", { duration: 1, drawSVG: 0 });
// 显式声明：从 0% 绘制到 100%
gsap.fromTo("#path", { drawSVG: "0% 0%" }, { drawSVG: "0% 100%", duration: 1 });
// 绘制一条在正中央段滑行的线条
gsap.to("#path", { duration: 1, drawSVG: "20% 80%" });
```

**注意事项：**仅影响 `stroke` 描边，不影响 `fill` 填充。优先使用单 Section 的 `<path>` 元素，多 Section 的路径在部分浏览器中可能会产生异常渲染。`<use>` 标签内部的内容物无法直接进行描边绘制。可以使用**DrawSVGPlugin.getLength(element)**与**DrawSVGPlugin.getPosition(element)**获取总长度和当前比例。**Learn more:**[DrawSVG](https://gsap.com/docs/v3/Plugins/DrawSVGPlugin)

### MorphSVG (MorphSVGPlugin)

将一个 SVG `<path>` 路径，极其丝滑地扭曲、形变演变为另一个完全不同的 SVG `<path>`。起止的两个图形控制点数可以不一致，MorphSVG 会在底层自动将图形转为三次贝塞尔并动态细分增补控制点，实现任意图形的丝滑流变过渡（例如复杂的 ICON 切换、形状过渡）。适用于 `<path>`、`<polyline>` 和 `<polygon>`；对于圆形 `<circle>`、矩形 `<rect>`、椭圆 `<ellipse>` 必须在使用前调用**MorphSVGPlugin.convertToPath(selector | element)**将其一键转为 `<path>` 节点。**morphSVG 值**：可以是一个选择器（如 `"#lightning"`）、DOM 节点、原始 path 的 `d` 属性字符串、或 polygon/polyline 的点坐标字符串。需要进行高级对齐等配置时，传入 vars 配置对象形式，其中 **shape**属性为唯一必选项。

```javascript
gsap.registerPlugin(MorphSVGPlugin);

// 在使用形变前，必须将所有基础几何图元一键安全重构为 Path 路径节点：
MorphSVGPlugin.convertToPath("circle, rect, ellipse, line");

gsap.to("#diamond", { duration: 1, morphSVG: "#lightning", ease: "power2.inOut" });
// 高级对象形式配置：
gsap.to("#diamond", {
  duration: 1,
  morphSVG: { shape: "#lightning", type: "rotational", shapeIndex: 2 }
});
```

### MorphSVG — 核心 vars 配置项（morphSVG 对象内）

| 属性 | 描述 |  |  |  |
| -------- | ------------- |  |  |  |
| **shape** | _(唯一必填项.)_ 目标终点 SVG 元素的选择器、DOM 节点、或 raw 原始 path 数据。 |  |  |  |
| **type** | `"linear"` (默认线性插值) 或 `"rotational"`。旋转流变插值在面对圆弧或复杂旋转图形时，能完美避免线性过渡时产生的中间瞬间折拧、穿透 Bug。 |  |  |  |
| **map** | 段配对机制：`"size"` (默认值), `"position"`, 或 `"complexity"`。当起止段无法正常对齐导致扭动异常时微调此项。如果依然异常，需要将路径进行拆解为多个子 Path 独立执行形变。 |  |  |  |
| **shapeIndex** | 锚点配对纠偏参数，决定了起始 Path 哪个锚点去配对终点 Path 的第一个控制点，防范过渡时的「图形自扭转或自穿透」现象。单 Section 传数字，多 Section 传对应数组（如 `[5, 1, -8]`，负数代表反转该 Section 的过渡方向）。传入**shapeIndex: "log"** 会自动在控制台打印最优测算值。**findShapeIndex(start, end)**提供了一个可视化的 HTML 调试界面来寻找该最佳数值。仅适用于闭合路径（closed paths）。 |  |  |  |
| **smooth** | (v3.14+)。增补点平滑控制。数字（如 `80`）、`"auto"` 或配置对象：`{ points: 40 \ | "auto", redraw: true \ | false, persist: true \ | false }`。配置 `redraw: false` 可以维持原始锚点，得到极佳的物理保真度。`persist: false` 在补间结束后自动移除增补出的控制点。 |
| **curveMode** | 布尔 (v3.14+)。插值时将插值控制柄的「角度和长度」而非「X/Y 绝对物理坐标」，这能极其完美地消除形变至中途时，圆滑曲线上产生的难看折弯尖角。 |  |  |  |
| **origin** | 针对**type: "rotational"**声明的形变旋转中心原点。字符串：默认 `"50% 50%"` 或分别为起点/终点声明 `{ origin: "20% 60%, 35% 90%" }`。 |  |  |  |
| **precision** | 导出变形 Path 数据时的保留小数点精度；默认值 `2`。 |  |  |  |
| **precompile** | 预编译 Path 字符串数组。在面对超大、极复杂的 Path 进行首帧过渡渲染时，声明此项（或调用**precompile: "log"**将计算好的数组打印出来并复制粘回代码中）可以跳过昂贵的 CPU 首帧开销，优化启动性能。仅适用于 `<path>`。 |  |  |  |
| **render** | 回调函数 `Function(rawPath, target)`，在每次补间渲染刷新时调用 —— 例如可用于直接重绘 Canvas 画布。 |  |  |  |
|  |**updateTarget**| 开启 render 自定义重绘时（例如 Canvas），设置 `updateTarget: false` 以避免让原始 DOM 上的 `<path>` 被执行重绘。可以通过 `MorphSVGPlugin.defaultUpdateTarget` 更改默认设置。 |  |  |  |  |**实用工具：** **MorphSVGPlugin.convertToPath(selector | element)** 将 circle/rect/ellipse/line/polygon/polyline 一键转换重构为 Path。**MorphSVGPlugin.rawPathToString(rawPath)**以及**stringToRawPath(d)**可以在 Path 数据字符串和底层坐标二维数组之间进行快速相互转换。插件会将原始 `d` 数据存储在 target 元素上，便于随时回滚。**Tips:**针对出现自扭转的形变，配置**shapeIndex**（使用 `"log"` 或 findShapeIndex() 辅助工具）。多 Section 必须传入数组（每个 Segment 对应一个数值）。预编译仅用于解决启动首帧顿卡，无法优化形变中途的 FPS 卡顿（若中途卡顿，需要简化 SVG 的控制点数或减小尺寸）。**Learn more:** [MorphSVG](https://gsap.com/docs/v3/Plugins/MorphSVGPlugin)

### MotionPath (MotionPathPlugin)

让任意 DOM 节点（或者 SVG 元素），沿着一个任意指定的 SVG 路径轨迹（Path）进行滑行运动：

```javascript
gsap.registerPlugin(MotionPathPlugin);

gsap.to(".dot", {
  duration: 2,
  motionPath: { path: "#path", align: "#path", alignOrigin: [0.5, 0.5] }
});
```

### MotionPath — 核心 vars 配置项（motionPath 对象内）

| 属性 | 描述 |
| -------- | ------------- |
| `path` | 目标 SVG 路径选择器、元素节点或 raw 数据字符串。 |
| `align` | 用于对齐目标位置基准坐标的选择器或元素节点。 |
| `alignOrigin` | 元素的中心基准点比例 `[x, y]`（0-1 之间）；默认值 `[0.5, 0.5]`（保持元素自身正中央粘在轨道上）。 |
| `autoRotate` | 开启车头方向旋转，使其自动根据滑行轨道的切线角度自我旋转。 |
| `curviness` | 0–2；控制路径的平滑度。 |

### MotionPathHelper

MotionPath 轨迹滑行可视化编辑器，在页面上直接生成辅助线和控制柄，供开发者手动拖拽微调滑行路线，开发利器。

```javascript
gsap.registerPlugin(MotionPathPlugin, MotionPathHelperPlugin);

const helper = MotionPathHelper.create(".dot", "#path", { end: 0.5 });
// 在 UI 界面上拖拽微调完毕后，直接复制输出的最新 Path 轨迹代码到补间中使用
```

## Easing

### CustomEase

自定义贝塞尔曲线/SVG 路径缓动插件。在 core API 的缓动不满足物理要求时，可以用来设计精细的自定义缓动（最核心用法已在 gsap-core 中收录，使用时进行注册即可）：

```javascript
gsap.registerPlugin(CustomEase);
const ease = CustomEase.create("name", ".17,.67,.83,.67");
gsap.to(".el", { x: 100, ease: ease, duration: 1 });
```

### EasePack

追加一系列更多好玩的缓动命名别名（例如：`SlowMo` 用于慢镜头、`RoughEase` 用于心电图等高频粗糙抖动、`ExpoScaleEase` 用于解决 2D 缩放时的视觉透视等比例缩放）。在 Tween 前执行注册，并像标准 ease 别名一样在配置中使用。

### CustomWiggle

往复抖动/弹性摆动配置插件（适用于铃铛晃动、弹性回弹）。

### CustomBounce

物理弹跳落地球曲线插件，支持自定义弹跳次数、地表硬度和弹起衰减比。

## Physics

### Physics2D (Physics2DPlugin)

2D 简单粒子物理模拟（初速度、发射角、阻力摩擦、重力）。不需要手动编写 Tick 运算，一键生成重力抛物线落体和喷射效果：

```javascript
gsap.registerPlugin(Physics2DPlugin);

gsap.to(".ball", {
  duration: 2,
  physics2D: {
    velocity: 250,
    angle: 80,
    gravity: 500
  }
});
```

### PhysicsProps (PhysicsPropsPlugin)

将物理运动属性（初速度、加速度）注入并应用到**任意自定义变量**上。

```javascript
gsap.registerPlugin(PhysicsPropsPlugin);

gsap.to(".obj", {
  duration: 2,
  physicsProps: {
    x: { velocity: 100, end: 300 },
    y: { velocity: -50, acceleration: 200 }
  }
});
```

## Development

### GSDevTools

专门在开发期注入的，用于在页面下方渲染控制播放、暂停、快进、倒带、框选 Timeline 段落进行循环（Loop）排错的可视化时间轴调试工具。**仅用于开发，发布前删除。**

```javascript
gsap.registerPlugin(GSDevTools);
GSDevTools.create({ animation: tl });
```

## Other

### Pixi (PixiPlugin)

专门将 GSAP 补间机制接入并驱动 PixiJS 快速 WebGL 渲染管线的插件。

```javascript
gsap.registerPlugin(PixiPlugin);

const sprite = new PIXI.Sprite(texture);
gsap.to(sprite, { pixi: { x: 200, y: 100, scale: 1.5 }, duration: 1 });
```

## Best practices

- ✅ 任何插件使用前，**必须且仅全局注册一次** `gsap.registerPlugin(PluginName)`。
- ✅ 在 Vue 3 或 Svelte 5 组件卸载销毁时，**必须执行销毁清理**（如文字拆分实例 `splitTextInstance.revert()`），或让外层 `ctx.revert()` 一体化自动销毁。
- ✅ 拖拽交互一律使用 `Draggable` + `InertiaPlugin` 的甩手和惯性抛物线组合，以保障极其流畅高大上的交互触感。

## Do Not

- ❌ **严禁使用未注册的插件**：不要绕过 `gsap.registerPlugin` 直接调用 API 或在 Tween 中写扩展名，否则打包器在 Tree-shaking 优化时会将其剔除，引发上线崩溃。
- ❌ **严禁在生产中残留调试工具**：开发期的 `markers: true` 和 `GSDevTools` 绝对不能发布，防止造成额外的性能负担并暴露调试 UI。

### Learn More

`<https://gsap.com/docs/v3/Plugins/>`
