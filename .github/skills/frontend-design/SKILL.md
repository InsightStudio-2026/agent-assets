---
name: frontend-design
description: 创建高质量、非模板化的前端界面、页面、组件和 Web artifacts，强调信息架构、视觉层次、状态诚实、响应式与实现可运行。Use when user asks to build or beautify UI, landing pages, dashboards, React components, HTML/CSS artifacts, or says 前端设计 / UI 美化 / landing page / dashboard / artifact builder。
---

# Frontend Design

## 1. 定位

Frontend Design 用于原创前端界面与 Web artifact 设计实现。它不替代 `prototype` 的可丢弃多方案探索，不替代 `/design-system-audit` 的审计门，也不复制外部 `frontend-design` / `web-artifacts-builder` 实现。

## 2. 触发与分流

| Rule ID | 条件 | 动作 | 分流 |
| --------- | ------ | ------ | ------ |
| FD-R1 | 用户要求创建页面、组件、dashboard、landing page、HTML artifact | 启动 UI 设计实现 | 本 skill |
| FD-R1b | 用户要求设计 UI 但方向不明（未确定风格、布局、信息架构） | 先问：确定方向了？还是想先看几个不同方案？ | 确定 → 本 skill；探索 → `prototype` |
| FD-R2 | 用户要试多个 UI 方向、可丢弃原型 | 分流 | `prototype` |
| FD-R3 | 用户要审计现有设计系统、tokens、A11y、视觉 QA | 分流 | `/design-system-audit` |
| FD-R4 | 用户要求发布真实 Web app | 分流 | `/release-deploy` |
| FD-R5 | 用户只要求修 bug 或测试 | 分流 | `diagnose` / `tdd` |

## 3. 设计输入

| 字段 (Field) | 是否必需 (Required) | 说明 |
| ------- | ---------- | ------ |
| 用户目标 (User goal) | Yes | 页面要帮助用户完成什么 |
| 受众 (Audience) | Yes | 目标用户与使用场景 |
| 内容层级 (Content hierarchy) | Yes | 信息优先级 |
| 约束条件 (Constraints) | Yes | 技术栈、品牌、响应式、A11y、浏览器 |
| 主题与风格 (Theme & Style) | Yes | 视觉与配色主题，优先套用 [THEMES.md](references/THEMES.md) 预设规范，杜绝 AI 味色彩 |
| 数据状态 (Data states) | Yes | loading / empty / error / success / permission |
| 交付形式 (Delivery form) | Yes | React component / static HTML / app route / design brief |

## 4. 设计原则

| 原则 (Principle) | 合格标准 (PASS 标准) | 失败信号 (FAIL 信号) |
| ----------- | ----------- | ----------- |
| 信息架构 (Information architecture) | 主行动、次行动、状态、辅助信息层级清楚 | 只有装饰，无任务路径 |
| 视觉层次 (Visual hierarchy) | 间距、排版与对比度 (spacing、typography、contrast) 支撑阅读；优先使用 [THEMES.md](references/THEMES.md) 配色与排版 | 随机渐变、卡片堆叠、AI 味模板 |
| 匠心细节 (Craftsmanship) | 细节显现极致斟酌（meticulously crafted），如微秒级对齐、无重叠、完美边缘呼吸 | 粗糙的默认边距、多重圆角嵌套、伪手作痕迹 |
| 微弱关联标线 (Subtle Reference) | 巧妙在构图中融入与概念呼应的系统化科学标线、微型标识符 (markers) 或抽象几何，使页面具有科学圣经般的庄严审视感 | 铺天盖地的说明文本，把网页当成报纸 |
| 诚实处理各种状态 (State honesty) | loading / empty / error / disabled 等状态明确 | 只做正常理想路径 (happy path) |
| 响应式设计 (Responsiveness) | mobile / tablet / desktop 有合理布局 | 固定宽度或溢出 |
| 无障碍设计 (Accessibility) | 语义标签、键盘路径、对比度、alt 文案 | 纯 div、低对比、无焦点态 |
| 实现完整性 (Implementation integrity) | 代码可运行，依赖和 import 完整 | 伪组件、缺 import、不可运行 |

## 5. Artifact Builder 规则

| Rule ID | 条件 | 动作 |
| --------- | ------ | ------ |
| FD-A1 | 需要复杂状态 / routing / shadcn-style UI | 优先 React + Tailwind 风格实现 |
| FD-A2 | 只需单页静态展示 | 可用 HTML / CSS / minimal JS |
| FD-A3 | 需要数据展示 | 定义 mock data schema 与空状态 |
| FD-A4 | 需要交互 | 定义事件、状态迁移和可验证结果 |
| FD-A5 | 用户提供现有项目 | 遵守项目已有组件和样式，不引入平行设计系统 |

## 6. 输出模板 (Output Template)

```markdown
## 前端设计信息包 (Frontend Design Packet)

## 设计目标 (Goal)

- <用户的设计目的与目标>

## UI 交互契约 (UI Contract)
|  | 区域/维度 (Area) | 交互设计要求 (Requirement) |  |
|  | ------ | ------------- |  |
|  | 主要操作 (Primary action) | <主行动路径及行为> |  |
|  | 关键状态 (Key states) | 加载中 / 空白 / 错误 / 成功 (loading / empty / error / success) |  |
|  | 响应式适配 (Responsive targets) | 移动端 / 平板 / 桌面端 (mobile / tablet / desktop) |  |
|  | 无障碍说明 (A11y notes) | <无障碍阅读及键盘焦点设计备注> |  |

## 技术实现说明 (Implementation Notes)

- 技术栈 (Stack):
- 拆分组件 (Components):
- 数据结构 (Data shape):
- 验证手段 (Verification):

```

## 7. 禁止项

| 禁止项 | 原因 |
| -------- | ------ |
| 不制造伪人工瑕疵 | 质量应来自领域设计，不是伪装 |
| 不引入项目未使用的大型依赖，除非用户批准 | 控制 scope 与依赖风险 |
| 不把 UI 原型当生产验收 | 发布和真实 QA 归 `/release-deploy` |

## 支撑资源

- [THEMES.md](./references/THEMES.md)
