# 界面去 AI 味门禁 (Design Anti-AI Taste Gate)

## 1. 定位

Design Anti-AI Taste Gate 不是“隐藏 AI 痕迹”，也不是伪造人工瑕疵。它检查 UI 是否缺少领域判断、信息层级、真实用户语境与产品调性，防止模板化、空洞、同质化和假精致。

## 2. Gate 规则

| 规则 ID (Rule ID) | 检查项 | PASS 标准 | FAIL 信号 | 修复路由 |
| --------- | -------- | ----------- | ----------- | ---------- |
| AAT-R1 | 领域信息密度 | 首屏 / 关键卡片展示领域用户真正决策所需信息 | 泛 dashboard 卡片、无业务判断 | `/specs-write` |
| AAT-R2 | 信息架构 | 导航、分组、主次层级对应用户任务 | 四块卡片 + 大标题模板 | `/specs-write` |
| AAT-R3 | 文案语气 | CTA、错误、空态、提示使用领域语言 | “轻松管理一切”“发生错误” | `/specs-execute` |
| AAT-R4 | 状态诚实 | loading / empty / error / disabled 告知真实原因与下一步 | skeleton / toast 泛用，无恢复路径 | `/specs-execute` |
| AAT-R5 | 视觉克制 | 渐变、阴影、玻璃、emoji、插画服务任务而非装饰 | 过度“现代感”掩盖信息贫乏 | `/specs-execute` |
| AAT-R6 | 组件语义 | 组件选择反映业务结构，不用万能卡片堆砌 | 所有内容都是 Card + Badge | `/specs-write` |
| AAT-R7 | 交互成本 | 关键动作路径短、确认和撤销符合风险 | 为显得丰富增加无效步骤 | `/specs-write` |
| AAT-R8 | 证据链 | 设计选择可追溯到用户路径、NFR-UX、DSN-UI 或截图 | 只说“更好看/更高级” | `/design-system-audit` |

## 3. 反模式查询表

| Anti-pattern ID | 名称 | 典型表现 | 必须追问 |
| ----------------- | ------ | ---------- | ---------- |
| AAT-B1 | SaaS 泛模板 | Hero + metrics cards + generic table | 用户真正每天看哪 3 个风险？ |
| AAT-B2 | 空态假温柔 | “这里还没有内容，快去创建吧” | 空的原因是什么？下一步最安全动作是什么？ |
| AAT-B3 | 错误泛化 | “Something went wrong” | 用户能做什么？系统是否已保留数据？ |
| AAT-B4 | 假高级视觉 | 大面积渐变 / 毛玻璃 / 重阴影 | 这些视觉是否提高识别与决策速度？ |
| AAT-B5 | 无领域 CTA | “Submit / Continue / Manage” | 业务动作和后果是什么？ |
| AAT-B6 | 单 happy path | 无失败、等待、撤销、权限不足 | 真实边界状态在哪里？ |

## 4. Taste Finding 模板

| 字段 (Field) | 值 (Value) |
| ------- | ------- |
| Finding ID | DSA-AAT-### |
| Rule | AAT-R*/ AAT-B* |
| Surface | `<route/component>` |
| Evidence | <screenshot / copy / component path> |
| Why it feels generic | `<one sentence>` |
| Domain-specific replacement | `<proposed direction>` |
| Route | /specs-write / /specs-execute / direct |

## 5. 判定

| 条件 | 状态 (State) |
| ------ | ------- |
| AAT-R1~R8 PASS 或仅低风险建议 | `/design-system-audit:DESIGN_SYSTEM_READY` 候选 |
| AAT-R1 / R2 / R6 / R7 FAIL | `/design-system-audit:DESIGN_SPEC_REQUIRED` |
| AAT-R3 / R4 / R5 FAIL | `/design-system-audit:ANTI_AI_TASTE_BLOCKED` |
| 证据不足 | `/design-system-audit:VISUAL_QA_PENDING` |

## 6. 禁止项

| 禁止项 | 原因 |
| -------- | ------ |
| 不伪造人工瑕疵 | 真实作者性来自领域判断和证据链，不来自故意弄糟 |
| 不删除 AI 披露要求 | 合规披露边界不由 UI taste 决定 |
| 不把个人审美当系统规则 | 稳定偏好需用户批准进入 SSOT |
