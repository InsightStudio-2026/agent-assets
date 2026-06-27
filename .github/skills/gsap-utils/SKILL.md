---
name: gsap-utils
description: GSAP 实用工具集官方开发指南 —— 涵盖 clamp 数值夹逼, mapRange 映射, normalize 归一化, interpolate 差值, random 随机, snap 步进对齐, toArray, wrap 循环。当用户咨询关于 GSAP 的数学转换、网格对齐、随机波动、数组转换、函数式管道（Pipe）等实用工具时使用。
license: MIT
user-invocable: false
---

# gsap.utils

## 何时使用此 Skill

当在编写或审查包含 **gsap.utils**调用的代码时，应用此 Skill。这些工具函数广泛用于数学计算、数组/集合操作、单位解析、或者在动画中实现值重映射（例如将滚动位置映射到一个变量值、随机化数据、将坐标吸附对齐到网格中、或对输入值执行归一化计算）。**相关技能：**在构建动画时，配合**gsap-core**、**gsap-timeline**和**gsap-scrolltrigger**使用；CustomEase 与其他缓动实用工具包含在**gsap-plugins**中。

## 工具库总览**gsap.utils** 提供了一系列纯函数 Helper 辅助工具，**不需要**专门进行 registerPlugin 注册。它们可以直接在补间 vars 配置（例如函数式动态计算值）、ScrollTrigger 或 Observer 的回调中、或驱动 GSAP 的任何 JavaScript 脚本中使用。所有方法均直接挂载在 **gsap.utils**作用域下（例如 `gsap.utils.clamp()`）。**柯里化偏函数形式（省略值参数）**：许多实用工具将“即将接受转换的值”作为**最后一个**参数传入。如果调用时省略最后一个参数，该工具函数会自动返回一个**柯里化偏函数**，用以在后续接受并转换数值。当需要使用相同的边界或区间参数高频对大量不同数据进行 clamp（限定）、map（映射）、normalize（归一化）或 snap（对齐吸附）时（例如在 mousemove 移动监听、或者 requestAnimationFrame 补间回调中），推荐使用这种函数形式。*特例：`random()` 方法除外* —— 必须显式在最后一个参数传入 **true**来获取可重用函数（不能通过省略参数获取）；详情请参阅 [random()](https://gsap.com/docs/v3/GSAP/UtilityMethods/random/)

```javascript
// 带有具体数值的调用：直接返回计算结果
gsap.utils.clamp(0, 100, 150); // 返回 100

// 不带数值的柯里化调用：返回一个供后续调用的偏函数
let c = gsap.utils.clamp(0, 100);
c(150);  // 返回 100
c(-10);  // 返回 0
```

## 夹逼与数值区间

### clamp(min, max, value?)

将输入数值严格限制在给定最小值 min 与最大值 max 之间。故意省略最后一个参数**value**可以返回一偏函数：`clamp(min, max)(value)`。

```javascript
gsap.utils.clamp(0, 100, 150); // 返回 100
gsap.utils.clamp(0, 100, -10); // 返回 0

let clampFn = gsap.utils.clamp(0, 100);
clampFn(150); // 返回 100
```

### mapRange(inMin, inMax, outMin, outMax, value?)

将一个数值从旧的输入范围比例重映射到全新的输出范围中。在将滚动位置、进度百分比（0-1）、或滑块 input 范围转换为特定的动画过渡区间时极其好用。故意省略最后一个参数**value**可以返回一偏函数：`mapRange(inMin, inMax, outMin, outMax)(value)`。

```javascript
gsap.utils.mapRange(0, 100, 0, 500, 50);  // 返回 250
gsap.utils.mapRange(0, 1, 0, 360, 0.5);   // 将进度百分比转换为旋转角度，返回 180

let mapFn = gsap.utils.mapRange(0, 100, 0, 500);
mapFn(50);  // 返回 250
```

### normalize(min, max, value?)

根据给定的区间范围，计算出输入数值在其中所处的等比例百分比位置（返回 0 到 1 之间的数值）。这是输出区间锁定在 0-1 时的比例映射的逆运算。故意省略最后一个参数**value**可以返回一偏函数：`normalize(min, max)(value)`。

```javascript
gsap.utils.normalize(0, 100, 50);   // 返回 0.5
gsap.utils.normalize(100, 300, 200); // 返回 0.5

let normFn = gsap.utils.normalize(0, 100);
normFn(50); // 返回 0.5
```

### interpolate(start, end, progress?)

根据传入的百分比进度 `progress`（0 到 1 之间），在起点值 `start` 和终点值 `end` 之间执行比例插值计算。支持对数值、十六进制/RGB/RGBA 颜色、以及拥有相同 key 的复杂 Object 嵌套数据结构进行完美的插值混合计算。故意省略最后一个参数**progress**可以返回一偏函数：`interpolate(start, end)(progress)`。

```javascript
gsap.utils.interpolate(0, 100, 0.5);       // 返回 50
gsap.utils.interpolate("#ff0000", "#0000ff", 0.5); // 返回红蓝过渡的正中央过渡色
gsap.utils.interpolate({ x: 0, y: 0 }, { x: 100, y: 50 }, 0.5); // 返回 { x: 50, y: 25 }

let lerp = gsap.utils.interpolate(0, 100);
lerp(0.5); // 返回 50
```

## 随机波动与步进对齐

### random(minimum, maximum[, snapIncrement, returnFunction]) / random(array[, returnFunction])

在给定的**minimum**（最小值）到 **maximum**（最大值）范围内产生一个随机数，或从指定的**数组成员**中随机抽取一项。

- 可选参数 **snapIncrement**支持将随机结果吸附对齐到指定的整数倍数上（例如 `5` 代表结果必须能被 5 整除）。

-**生成偏函数**：必须在最后一个参数（**returnFunction**）显式传入 **true**。返回一个无参、可重复调用、每次运行都会吐出全新随机值的函数。这是唯一必须显式传 `true` 生成偏函数（柯里化）而不能省略参数的实用工具。

```javascript
// 直接计算：吐出随机数值
gsap.utils.random(-100, 100);        // 例如：42.7
gsap.utils.random(0, 500, 5);        // 0到500之间，且吸附对齐到最邻近 5 的倍数上

// 生成偏函数：最后一个参数传 true
let randomFn = gsap.utils.random(-200, 500, 10, true);
randomFn();  // 返回在区间内且整除 10 的随机值
randomFn();  // 再次运行返回另一全新随机值

// 从数组成员中进行随机抽取
gsap.utils.random(["red", "blue", "green"]);  // 返回一随机抽取色
let randomFromArray = gsap.utils.random([0, 100, 200], true);
randomFromArray();  // 随机吐出 0, 100, 或 200
```

**Vars 配置内的高能极简字符串别名**：GSAP 支持在 Tween vars 属性值中直接写入 `"random(-100, 100)"` 格式的字符串，GSAP 会在底层自动展开并为每个动画 Target 元素独立运行和注入不同的随机值：

```javascript
gsap.to(".box", { x: "random(-100, 100, 5)", duration: 1 });
gsap.to(".item", { backgroundColor: "random([red, blue, green])" });
```

### snap(snapTo, value?)

将输入数值吸附对齐到最邻近的 **snapTo**的倍数上，或者对齐到传入的「唯一点位数组列表」中离其物理位置最近的一个成员上。故意省略最后一个参数**value**可以返回一偏函数：`snap(snapTo)(value)`（或 `snap(snapArray)(value)`）。

```javascript
gsap.utils.snap(10, 23);     // 离 20 最近，返回 20
gsap.utils.snap(0.25, 0.7);  // 离 0.75 最近，返回 0.75
gsap.utils.snap([0, 100, 200], 150); // 距离 100 和 200 相同，返回 100 或 200

let snapFn = gsap.utils.snap(10);
snapFn(23); // 返回 20
```

可以直接在 Tween 属性中作为简写配置（实现磁吸/网格效果）：

```javascript
gsap.to(".x", { x: 200, snap: { x: 20 } });
```

### shuffle(array)

安全洗牌打乱算法。返回一个被完全乱序的全新数组副本（不改变原始输入数组）。

```javascript
gsap.utils.shuffle([1, 2, 3, 4]); // 例如：[3, 1, 4, 2]
```

### distribute(config)**专门返回一个高级偏函数**。其会自动根据元素在一维数组或二维 Grid 布局中的相对物理排列位置，计算并分配非线性阶梯数值（多用于手动设计极其复杂的瀑布流交错 stagger 延迟、自适应 scale、自适应 opacity 透明度分布等）

该返回函数接口符合 `(index, target, targets)` 签名。你可以直接在 Tween vars 中直接将其作为值注入，GSAP 会在底层为每个元素自动执行计算：

### Config 配置参数（全部可选）

| 属性项 | 类型 | 描述 |  |  |
| ---------- | ------ | ------------- |  |  |
| `base` | 数字 | 起步基础值。默认值为 `0`。 |  |  |
| `amount` | 数字 | 即将被全员瓜分的总数值额。例如：`amount: 1` 且有 100 个元素时，每两个元素之间的步进差自动计算为 0.01。与 `each` 互斥。 |  |  |
| `each` | 数字 | 显式锁定两个元素之间的绝对步进阶梯差值。例如：`each: 1` 且有 4 个元素时，分配值为 0, 1, 2, 3。与 `amount` 互斥。 |  |  |
| `from` | 数字 \ | 字符串 \ | 数组 | 数值波动的源头发射起点位置。可传入：数组索引下标、或者 `"start"`, `"center"`, `"edges"`, `"random"`, `"end"`，也支持传入二维比率如 `[0.25, 0.75]`。 默认为 `0`。 |
| `grid` | 字符串 \ | 数组 | 声明元素的二维排版布局，以便计算二维空间距离：`[行, 列]`（如 `[5, 10]`），或设为 `"auto"` 由 GSAP 自动测绘，默认不开启（视为一维扁平数组）。 |  |
| `axis` | 字符串 | 开启 grid 后，可锁定仅在单轴（`"x"` 或 `"y"`）上执行间距扩散计算。 |  |  |
| `ease` | 缓动别名 | 声明瓜分间距阶梯的数学分布曲线（如 `"power1.inOut"`）。默认为 `"none"` 匀速分配。 |  |  |

**在补间中直接调用**：作为属性的目标值传入，GSAP 会在计算每个目标时传入 `(index, target, targets)` 自动执行该偏函数：

```javascript
// 缩放：中心部分的元素缩放最少（0.5），四周边缘的元素缩放最大（0.5 + 2.5 = 3.0），从中心向两端自适应扩散分布
gsap.to(".class", {
  scale: gsap.utils.distribute({
    base: 0.5,
    amount: 2.5,
    from: "center"
  })
});
```

**在 JS 中手动单独调用**：

```javascript
const distributor = gsap.utils.distribute({
  base: 50,
  amount: 100,
  from: "center",
  ease: "power1.inOut"
});
const targets = gsap.utils.toArray(".box");
const valueForIndex2 = distributor(2, targets[2], targets); // 精确计算出 index 为 2 的元素的最终分配数值
```

详细官方指南：[distribute()](https://gsap.com/docs/v3/GSAP/UtilityMethods/distribute/)。

## 单位获取与格式解析

### getUnit(value)

获取数值中的 CSS 样式单位：

```javascript
gsap.utils.getUnit("100px");   // 返回 "px"
gsap.utils.getUnit("50%");     // 返回 "%"
gsap.utils.getUnit(42);        // 返回 "" (无单位)
```

### unitize(value, unit)

为数值追加单位。若输入已带单位，则保持不变直接返回（常用于拼写 CSS 终点样式值）：

```javascript
gsap.utils.unitize(100, "px");  // 返回 "100px"
gsap.utils.unitize("2rem", "px"); // 已带单位，直接返回原样 "2rem"
```

### splitColor(color, returnHSL?)

颜色值反解析器。它能将 hex 十六进制、`"rgb()"`、`"rgba()"`、`"hsl()"`、甚至 HTML 英文颜色别名（如 `"red"`），一键反解析为标准数值数组： **`[Red, Green, Blue]`**(0-255) 或**`[Red, Green, Blue, Alpha]`**(若存在透明度通道)。
若第二个参数 `returnHSL` 传为**true**，会返回对应的 **`[Hue, Saturation, Lightness]`** HSL 色彩空间成分。常用于自定义 Canvas 像素级绘图和渐变渲染，详细请参阅 [splitColor()](https://gsap.com/docs/v3/GSAP/UtilityMethods/splitColor/)：

```javascript
gsap.utils.splitColor("red");                    // 返回 [255, 0, 0]
gsap.utils.splitColor("#6fb936");                // 返回 [111, 185, 54]
gsap.utils.splitColor("rgba(204, 153, 51, 0.5)"); // 自动保留 alpha，返回 [204, 153, 51, 0.5]
gsap.utils.splitColor("#6fb936", true);          // 转换为 HSL，返回 [94, 55, 47]
```

## DOM 集合与复合管道

### selector(scope)

专门针对组件化环境（如 React Ref、Vue Ref）设计的作用域选择器。
其接收一个根容器（Ref 对象、React 的 `.current` 对象、或 DOM 节点）作为 Scope 作用域，并返回一个专属的 Selector 函数。在该函数内部执行的任何选择器查找，**都将被严格局限在该根容器子树内部**，彻底断绝全局冲突：

```javascript
const q = gsap.utils.selector(containerRef);
q(".box");        // 仅匹配并获取 containerRef 内部的 .box 元素节点，不影响外面
gsap.to(q(".circle"), { x: 100 });
```

### toArray(value, scope?)

一维数组格式化转换器。它能将任何传入的：CSS 选择器字符串（支持传入第二个 scope 参数进行范围查询）、`NodeList` 集合、`HTMLCollection`、单个 DOM 节点、或已经存在的数组，一键安全、平扁地转换为**原生 JS 数组**，保证可以直接调用诸如 `.map` / `.forEach` 等原生数组方法：

```javascript
gsap.utils.toArray(".item");           // 将所有匹配项，转换重构为一维原生 Array 数组
gsap.utils.toArray(".item", container); // 仅在 container 内部进行查找并数组化转换
gsap.utils.toArray(nodeList);          // 将 NodeList 安全扁平化为原生数组
```

### pipe(...functions)

高能函数合成器（FP 编程流）。
`pipe(f1, f2, f3)(value)` 等价于执行 `f3(f2(f1(value)))`。数据会像流水线一样依次被后面的函数加工转换，非常适合用于在高频交互或 ScrollTrigger 事件中执行坐标级联运算（例如：坐标值 → 归一化 → mapRange 区间映射 → snap 网格磁吸对齐）：

```javascript
const fn = gsap.utils.pipe(
  (v) => gsap.utils.normalize(0, 100, v),
  (v) => gsap.utils.snap(0.1, v)
);
fn(50); // 先执行 normalize 归一化，结果再由 snap 磁吸对齐，最后返回
```

### wrap(min, max, value?)

边界溢出环绕。当数值超过 max（不含 max 本身）时，自动环绕回 min 重新累加；低于 min 时，自动环绕到 max。常用于无限循环跑马灯位置计算、无限滑动条等。故意省略最后一个参数 **value**可以返回一偏函数：`wrap(min, max)(value)`。

```javascript
gsap.utils.wrap(0, 360, 370);  // 溢出 10，自动回弹环绕返回 10
gsap.utils.wrap(0, 360, -10);   // 低于 min，自动折叠环绕返回 350

let wrapFn = gsap.utils.wrap(0, 360);
wrapFn(370); // 返回 10
```

### wrapYoyo(min, max, value?)

边界双向折返环绕（当超出边界时，自动在 min 和 max 的界限处像 Yoyo 一样钟摆折返）。故意省略最后一个参数**value** 可以返回一偏函数：`wrapYoyo(min, max)(value)`。

```javascript
gsap.utils.wrapYoyo(0, 100, 150); // 150 超出 100，折返 50 像素，返回 50

let wrapY = gsap.utils.wrapYoyo(0, 100);
wrapY(150); // 返回 50
```

## 官方工具箱最佳实践

- ✅ 面对高频事件刷新或需要在动画高频 callback 中执行相同转换时，**必须省略 value 参数，柯里化生成一个 reusable function 重复调用**，这能免去重复实例化边界参数的性能消耗。
- ✅ 步进磁吸和网格对齐一律优先选用 `snap`；面对混杂的 DOM、选择器或 NodeList 输入，统一使用 `toArray` 规范化为原生 Array 数组类型。
- ✅ 组件化开发中，**务必使用 `gsap.utils.selector(scope)` 建立组件内部专属选择器**，彻底杜绝同名组件同时加载的选择器冲突 Bug。

## 开发避坑红线 (Do Not)

- ❌ **理清 mapRange / normalize 等数学工具边界**：这些工具只能计算**纯数值**，严禁传入任何带单位的字符串参数（如传入 `"100px"` 将直接导致 NaN 破坏性崩溃）。处理单位时必须配合 `getUnit`、`unitize` 组合拳执行。
- ❌ **严禁使用 undocumented 的非公开 API。**

### Learn More

`<https://gsap.com/docs/v3/HelperFunctions>`
