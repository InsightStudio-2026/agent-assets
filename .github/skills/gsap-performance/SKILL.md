---
name: gsap-performance
description: GSAP 高性能动画调优指南 —— 涵盖优先使用 CSS3 变换（Transforms）、杜绝布局抖动（Layout Thrashing）、合理使用 `will-change`、读写批处理等调优机制。Use when optimizing GSAP animation performance, eliminating jank/dropped frames, achieving 60fps, doing scroll performance analysis, or says 动画性能优化/GSAP 卡顿/掉帧/FPS。
license: MIT
user-invocable: false
---

# GSAP 性能调优

## 何时使用此 Skill

在需要优化 GSAP 动画以确保丝滑 60fps 稳定帧率、降低浏览器内核重排与重绘消耗（Layout/Paint cost）、或者用户咨询关于动画卡顿、掉帧、异步优化最佳实践时，应用此 Skill。

**相关技能：**编写动画请使用**gsap-core**（优先使用位移、autoAlpha）以及 **gsap-timeline**；滚动联动场景下的性能分析请参考 **gsap-scrolltrigger**。

## 优先使用 Transforms 与 Opacity

在动画中优先且唯一推荐去 animate **transform**属性（即 `x`、`y`、`scaleX`、`scaleY`、`rotation`、`rotationX`、`rotationY`、`skewX`、`skewY` 等别名）以及**opacity**（即 `autoAlpha`）。

这些属性直接在浏览器的**合成器线程（Compositor Thread）**上运行并启用 GPU 硬件加速，能完美避开重排（Layout）并免除大多数重绘（Paint）。绝对避免去直接 animate 高能耗布局属性：

- ✅ **推荐动画项：**`x`, `y`, `scale`, `rotation`, `opacity` / `autoAlpha`。
- ❌**严禁高能耗动画项：**`width`, `height`, `top`, `left`, `margin`, `padding`（这些会疯狂触发浏览器重排，直接导致千元机级设备大面积卡顿）。

GSAP 内部的 `x` 和 `y` 默认全部映射为 CSS3 3D位移变换（translate3d），请务必用它们来代替 `left` / `top` 完成位置移动！

## CSS 优化建议：will-change

在 CSS 中，为即将应用复杂动画的 DOM 元素显式添加**will-change**。这会提前通知浏览器将其提升为独立的 GPU 渲染图层（Layer Promotion）：

```css
/*仅在需要动画的元素上声明，禁止滥用*/
will-change: transform;
```

## 读写操作批处理（避免布局抖动）

GSAP 内部自带有高度优化的读写批处理（Batching）。
当你需要将 GSAP 补间动画与原生 DOM 读取（如 `element.offsetHeight` 等触发重排的 API）或依赖布局的 JS 业务逻辑混合执行时，**严禁交错读写 DOM**（即读一个、写一个、再读一个）。这会强迫浏览器频繁进行同步重布局（Layout Thrashing）；应该**先完成所有的 DOM 读取，再统一交由 GSAP 执行动画写入**。

## 面对海量元素（Stagger 与长列表）的优化

- **聚合交错**：面对相同动画逻辑的大量元素，必须使用 `stagger` 属性将其聚合为一个 Tween 执行，禁止创建数百个各自带 delay 的独立小补间。
- **长虚拟列表**：面对极长列表，应结合**虚拟化（Virtualization）**技术或仅对视口内的可见 DOM 节点运行动画；严禁同一时间在后台运行成百上千个不可见活跃补间。
- **时间轴重用**：在动画需要极高频调用时（如动画循环），尽量复用已创建的时间轴实例；严禁在每一帧（Frame）内频繁 `new` 创建新时间轴。

## 极高频更新属性优化（如鼠标跟随器）

对于像鼠标指针跟随器（Mouse Follower）、高频陀螺仪反馈、或者随着滚动高频计算位移的场景，**绝对推荐使用 `gsap.quickTo()`**。
它会重用单个底层补间，其运行能耗和性能远超每次高频事件触发时频繁调用 `gsap.to()` 创建新补间：

```javascript
// quickTo 极速重绘
let xTo = gsap.quickTo("#id", "x", { duration: 0.4, ease: "power3" }),
    yTo = gsap.quickTo("#id", "y", { duration: 0.4, ease: "power3" });

document.querySelector("#container").addEventListener("mousemove", (e) => {
  // 直接以极低能耗将目标过渡到最新物理坐标
  xTo(e.pageX);
  yTo(e.pageY);
});
```

## ScrollTrigger 专属性能调优

- **Pin 节点控制**：`pin: true` 会将被固定的元素自动提升为独立硬件加速图层；因此请只在必须固定的外层主 Wrapper 元素上配置 pin，避免 pin 多个碎小的子元素。
- **Scrub 阻尼延迟**：配置一个轻微的延迟数值（如 `scrub: 1`）不仅可以带来丝滑流畅感，还能有效归拢页面由于急促划过滚轮时的大量重绘压力。
- **避开频繁 refresh**：只有在页面数据、DOM 真实高度发生重排变化时才主动调用 `ScrollTrigger.refresh()`；严禁在浏览器的 `resize` 监听回调中高频同步 refresh（GSAP 本身自带高稳定性 resize 防抖）。

## 降低并发运行负荷

- **视口外自动拦截**：当页面路由切换（如单页面组件卸载）、或者元素由于滚动滑出视口成为不可见状态时，务必将这些处于视口外或非激活状态的动画立即 **Pause（暂停）**或**Kill（物理销毁）**，防止其在后台继续消耗 CPU 周期。
- **简化属性**：避免同一个 DOM 上同时有数十个不同属性同时独立运行补间；尝试进行属性归拢或顺序编排。

## 性能调优最佳实践

- ✅ 动画执行项必须锁定为 **transforms**（位移缩放等）和 **opacity**，在动画节点上合理配置 CSS `will-change: transform`。
- ✅ 面对同名多节点动画，**必须使用 `stagger`** 代替大批量独立 Tween delay。
- ✅ 面对高频事件刷新（如鼠标跟随器），**必须使用 `gsap.quickTo()`**代替高频触发 `gsap.to()`。
- ✅ SPA 应用中离开页面必须干净注销所有 Tween 与 ScrollTrigger。

## 开发避坑红线 (Do Not)

- ❌**严禁 animate 布局样式**：严禁对 `width`/`height`/`top`/`left`/`margin` 等布局属性直接运行补间；位移必须使用 `x`/`y` 硬件加速别名代替。
- ❌ **严禁万物皆 will-change**：不要盲目在页面所有元素上添加 `will-change` 或 `force3D: true`；这会迅速耗尽浏览器的显存（VRAM），引发不可预知的闪白和 crash 崩溃。
- ❌ **拒绝低端设备裸跑**：不要同一时间并发执行数百个重叠交错动画；必须在低端机型/移动端视口上进行性能回归测试。
- ❌ **禁止遗漏 cleanup 清理**：游离的动画如果继续在后台空转，会像隐形病毒一样持续剥夺 CPU 显卡算力并干扰后续动画运行。
