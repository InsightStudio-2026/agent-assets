# 视觉 QA 协议 (Visual QA Protocol)

## 1. 证据矩阵

| 规则 ID (Rule ID) | 证据类型 | 最低覆盖 | PASS 标准 |
| --------- | ---------- | ---------- | ----------- |
| VQA-1 | Route screenshot | 关键 route / screen | desktop + mobile 或目标 viewport |
| VQA-2 | Component state screenshot | loading / error / empty / success / disabled | 每类状态至少一个代表样本 |
| VQA-3 | Interaction screenshot | modal / dropdown / toast / navigation / focus | 打开态、关闭态、错误态可见 |
| VQA-4 | Before / after | 修复 visual finding 时 | 同 viewport、同数据态对比 |
| VQA-5 | Regression snapshot | Storybook / Playwright / visual diff | diff 有阈值和人工解释 |

## 2. 视口矩阵 (Viewport Matrix)

| Surface | Desktop | Tablet | Mobile | Notes |
| --------- | --------- | -------- | -------- | ------- |
| `<route/component>` | PASS / FAIL / N/A | PASS / FAIL / N/A | PASS / FAIL / N/A | `<reason>` |

## 3. 视觉 Finding 规则 (Visual Finding Rules)

| 规则 ID (Rule ID) | 检查项 | PASS 标准 | FAIL 信号 |
| --------- | -------- | ----------- | ----------- |
| VF-R1 | 可定位 | finding 指向 screenshot + viewport + state | 只写“看起来怪” |
| VF-R2 | 可修复 | finding 指向 component / token / copy / layout route | 无法落到修复对象 |
| VF-R3 | 可复验 | 修复后有同条件 after screenshot | 修复只凭主观口头通过 |
| VF-R4 | 可回滚 | CSS / component diff 可追溯到 Task | 大范围改主题无回滚边界 |
| VF-R5 | 不单点视角 | 不以单一 viewport / happy path 代表全 UI | 只看 1440px 首页 |

## 4. Finding 表

| 发现项 ID (Finding ID) | 界面路由 (Surface) | 响应式视口 (Viewport) | 状态面 (State) | 验证证据 (Evidence) | 缺陷描述 (Issue) | 修复路由 (Route) | 复验结果证据 (Recheck Evidence) |
| ------------ | --------- | ---------- | ------- | ---------- | ------- | ------- | ------------------ |
| DSA-VQA-### | `<screen>` | desktop / tablet / mobile | loading / error / empty / normal | `<path>` | `<summary>` | /specs-execute | `<path>` |

## 5. 判定

| 条件 | 状态 (State) |
| ------ | ------- |
| 所有关键路径有 viewport + state evidence | `/design-system-audit:DESIGN_SYSTEM_READY` 候选 |
| 截图缺失或复验缺失 | `/design-system-audit:VISUAL_QA_PENDING` |
| visual finding 指向 UX spec 缺口 | `/design-system-audit:DESIGN_SPEC_REQUIRED` |
