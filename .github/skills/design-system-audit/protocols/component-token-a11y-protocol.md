# 组件、Tokens与无障碍协议 (Component / Token / A11y Protocol)

## 1. 组件盘点 (Component Inventory)

| 规则 ID (Rule ID) | 检查项 | PASS 标准 | FAIL 信号 |
| --------- | -------- | ----------- | ----------- |
| CTA-R1 | 组件来源 | Button / Input / Modal / Toast / Table / Navigation / Empty State 有权威来源 | 新 UI 临时手写重复组件 |
| CTA-R2 | 状态覆盖 | loading / error / empty / success / disabled / undo / confirm 均有定义或 N/A 理由 | 只做 happy path |
| CTA-R3 | 复用边界 | 新组件有复用理由，不污染公共组件 API | 为单页面抽泛化组件 |
| CTA-R4 | 术语一致 | CTA、错误信息、字段名与领域术语一致 | 泛化文案“操作成功/发生错误” |

## 2. Token Drift

| 规则 ID (Rule ID) | 检查项 | PASS 标准 | FAIL 信号 |
| --------- | -------- | ----------- | ----------- |
| TOK-R1 | Color | 使用 design token 或明确例外 | 任意 hex / rgb 散落 |
| TOK-R2 | Typography | 字号、行高、字重来自 token scale | 单次视觉微调 hardcode |
| TOK-R3 | Spacing | 间距来自 spacing scale | magic number 散落 |
| TOK-R4 | Radius / Shadow | 圆角、阴影、边框层级一致 | 卡片风格碎裂 |
| TOK-R5 | Motion | 动效时长、easing、可关闭策略一致 | 动效抢注意力或不可关闭 |

## 3. 无障碍基线 (A11y Baseline)

| 规则 ID (Rule ID) | 检查项 | PASS 标准 | FAIL 信号 |
| --------- | -------- | ----------- | ----------- |
| A11Y-R1 | Keyboard | 关键路径键盘可达，Tab 顺序合理 | 鼠标专用交互 |
| A11Y-R2 | Focus | focus visible，不被弹窗 / drawer 吞掉 | focus 丢失或不可见 |
| A11Y-R3 | Contrast | 文本 / 控件满足目标 WCAG 标准 | 低对比灰字 |
| A11Y-R4 | ARIA | aria-label / role / live region 合理 | 无语义 div button |
| A11Y-R5 | Screen reader | 表单、错误、状态变化可读 | 错误只靠颜色 |
| A11Y-R6 | Responsive | desktop / tablet / mobile 或窗口缩放矩阵通过 | 单尺寸截图通过 |

## 4. Finding 模板

| 字段 (Field) | 值 (Value) |
| ------- | ------- |
| Finding ID | DSA-FIND-### |
| Type | component / token / a11y / interaction / copy |
| Source | NFR-UX-*/ DSN-UI-* / screenshot |
| Evidence | `<path>` |
| Severity | low / medium / high |
| Recommended Route | /specs-write / /specs-execute / direct |

## 5. 判定

| 条件 | 状态 (State) |
| ------ | ------- |
| component + token + a11y 全 PASS | `/design-system-audit:COMPONENT_INVENTORY_READY` |
| token drift 存在 | `/design-system-audit:TOKEN_DRIFT_FOUND` |
| a11y high/medium finding 存在 | `/design-system-audit:A11Y_RISK_FOUND` |
| 状态面冲突 | `/design-system-audit:INTERACTION_CONFLICT_FOUND` |
