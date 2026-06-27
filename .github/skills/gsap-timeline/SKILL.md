---
name: gsap-timeline
description: GSAP 时间轴官方开发指南 —— 涵盖 `gsap.timeline()`、位置参数（Position Parameter）、时间轴嵌套、播放状态控制。Use when building multi-step animations, sequencing complex keyframes, asking about timeline/playback control, or says 动画序列/时间轴/多步骤动画/播放顺序。
license: MIT
user-invocable: false
---

# GSAP 时间轴

## 何时使用此 Skill

当需要构建复杂的连贯多步骤动画序列、精确协同控制多个补间的同步或异步播放时，或者用户咨询关于 GSAP 的时间轴（Timeline）、动画链排版、关键帧机制时应用此 Skill。

**相关技能：**单个 Tween 和 Ease 请参考**gsap-core**；滚动联动的 Timeline 请参考 **gsap-scrolltrigger**；React 下的销毁清理请参考 **gsap-react**。

## 创建时间轴

```javascript
const tl = gsap.timeline();
tl.to(".a", { x: 100, duration: 1 })
  .to(".b", { y: 50, duration: 0.5 })
  .to(".c", { opacity: 0, duration: 0.3 });
```

默认情况下，时间轴上的补间是按队列顺序**接连追加（Appended）**的。使用 **Position Parameter (位置参数)** 可以精确调节补间的播放起点或实现重叠播放。

## 位置参数 (Position Parameter)

通过补间方法（如 `to()`、`from()` 等）的**第三个参数**来控制该动画在时间轴上的播放时机（vars 配置中也可以通过 `position` 属性定义）：

- **绝对时间点**：`1` — 在时间轴第 1 秒时刻准时启动。
- **相对时间点（默认追加）**：`"+=0.5"` — 在前一个动画结束的 0.5 秒后启动；`"-=0.2"` — 在前一个动画结束的前 0.2 秒启动（实现提前重叠播放）。
- **时间轴标签 (Label)**：`"labelName"` — 在该标签锁定的时刻启动；`"labelName+=0.3"` — 在该标签时刻的 0.3 秒后启动。
- **关联参照点**：
  - `"<"` — 与**上一个刚刚被添加的动画**同时同起点播放。
  - `">"` — 在**上一个刚刚被添加的动画**播放结束后立刻播放（即默认追加机制）。
  - `"<0.2"` — 在上一个被添加动画开始播放的 0.2 秒后启动。

代码演示：

```javascript
tl.to(".a", { x: 100 }, 0);           // 在时间轴 0 秒刻度播放
tl.to(".b", { y: 50 }, "+=0.5");      // 在 a 结束 0.5s 后播放
tl.to(".c", { opacity: 0 }, "<");     // 与 b 同时同步启动播放
tl.to(".d", { scale: 2 }, "<0.2");    // 在 c 启动播放的 0.2 秒后启动
```

## 时间轴默认参数

可以直接在时间轴构造配置中传入默认 Vars 选项，时间轴内的所有子补间都会自动继承：

```javascript
const tl = gsap.timeline({ defaults: { duration: 0.5, ease: "power2.out" } });
tl.to(".a", { x: 100 }).to(".b", { y: 50 }); // a 和 b 都会默认使用 0.5s 时长以及 power2.out 曲线
```

## 时间轴构造配置

- **paused: true**— 初始化后默认处于暂停状态；调用 `.play()` 才会开启播放。

-**repeat, yoyo**— 与 Tween 相同，但其会作用于整条时间轴的所有动画。
-**onComplete, onStart, onUpdate**— 时间轴全局级别的生命周期事件回调。
-**defaults**— 批量注入到子补间的 vars 配置。

## 时间轴标签 (Labels)

合理使用 Labels 标签，可以极大提高动画序列编排的可读性与可维护性：

```javascript
tl.addLabel("intro", 0);
tl.to(".a", { x: 100 }, "intro");
tl.addLabel("outro", "+=0.5");
tl.to(".b", { opacity: 0 }, "outro");

tl.play("outro");  // 直接跳转到 "outro" 标签时刻开始播放
tl.tweenFromTo("intro", "outro"); // 暂停当前时间轴，并自动生成并返回一个过渡补间（Tween），它会在没有 Easing 的情况下匀速将播放指针从 "intro" 推动到 "outro" 时刻。
```

## 嵌套时间轴

时间轴内部支持无限制地 add 其它子时间轴，支持无限深度。

```javascript
const master = gsap.timeline();
const child = gsap.timeline();
child.to(".a", { x: 100 }).to(".b", { y: 50 });

master.add(child, 0); // 将子时间轴精准嵌入到 master 的 0 秒处
master.to(".c", { opacity: 0 }, "+=0.2");
```

## 播放控制

-**tl.play()**/**tl.pause()**— 播放 / 暂停。
-**tl.reverse()**— 一键倒带/反向回放（若动画处于尾页，可配合 `tl.progress(1)` 强制反向）。
-**tl.restart()**— 重头重新播放。
-**tl.time(2)**— 直接将指针跳转到第 2 秒。
-**tl.progress(0.5)**— 直接定位到 50% 进度处。
-**tl.kill()** — 彻底销毁当前时间轴及其下辖的所有子补间动画。

## 官方 GSAP 最佳实践

- ✅ 编写多步骤、连贯步骤的复杂动画序列时，**绝对且唯一推荐使用 Timeline**。
- ✅ 善用**位置参数（Position Parameter，即第三个参数）**控制补间起止，避免在子 Tween vars 中写 delay 拼凑。
- ✅ 建议通过 `addLabel()` 建立标签机制，提高长动画指针控制的可复用性。
- ✅ 务必利用构造函数中的 `defaults` 来重用诸如 duration、ease 等属性。
- ✅ 如果结合了滚动联动插件，**务必将 `scrollTrigger` 直接绑定到 Timeline 构造函数中**，严禁绑定到 Timeline 内部的子 Tween 上。

## 开发避坑红线 (Do Not)

- ❌ **严禁使用 delay 拼凑多步骤动画**：当需要顺序播放多个动画时，严禁通过手动计算并添加 `delay: 1`、`delay: 2.5` 等属性进行拼凑；必须使用 `gsap.timeline()` 加上位置参数实现，否则维护时任何一个时长的变动都会导致后续动画全部错位。
- ❌ **避免遗漏 defaults 继承**：当时间轴中的多数子补间共享相同的时长或缓动参数时，绝不漏掉全局 defaults 声明，防止造成代码臃肿。
- ❌ **理清 timeline 时长概念**：务必分清时间轴构造参数中的 `duration` 并非子补间时长；时间轴实例的最终 duration 是由其内部的所有子节点拓扑排序算出的。
- ❌ **严禁在 Timeline 内部子补间上配置 ScrollTrigger**：滚动触发器只能存在于顶级 Tween 或顶级 Timeline 本身上，嵌套的子动画配置 ScrollTrigger 会导致滚动碰撞检测失效和极其怪异的视觉卡顿。
