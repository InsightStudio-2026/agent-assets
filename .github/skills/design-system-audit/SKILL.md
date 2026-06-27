---
name: design-system-audit
description: 设计系统与 UX 审计：治理 UI 组件、tokens、A11y、响应式、交互状态、文案术语、视觉 QA 与 Design Anti-AI Taste Gate；输出 design system readiness report。
argument-hint: "要审计哪个设计系统或组件库？"
disable-model-invocation: true
---


# /design-system-audit · 设计系统与 UX 审计

**定位**：把 UI/UX 从即时审美判断变成可追溯的系统审计；覆盖组件清单、design tokens、A11y、响应式矩阵、交互状态、文案术语、视觉 QA、截图证据与 Design Anti-AI Taste Gate。

**边界**：不替代 `/specs-write` 定义 UX / A11y 需求，不替代 `/specs-execute` 实现 UI，不替代人工品牌审美最终裁决；本 workflow 只产出 design system readiness report、finding 与修复路由。稳定审美偏好不得静默写入 SSOT，必须用户批准。

**斜杠命令**：`/design-system-audit`

**上游 / 下游**：上游消费 `NFR-UX-*`、DSN-UI-*、设计源、截图、组件清单、tokens、关键用户路径；下游将修复分流 `/specs-write`、`/specs-execute`、`/developer-experience-audit` 或 `review`。

---

## 懒加载契约

- **MUST read**: `./decision-matrix.md`
- 开始判定或执行 Phase 流程前，必须完整懒加载上述细节。

---

## 1. 伴随文档

| 文档 | 角色 | 何时读 |
| ------ | ------ | -------- |
| `protocols/component-token-a11y-protocol.md` | 组件清单、token drift、交互状态、A11y 基线 | Phase 1 / 2 |
| `protocols/visual-qa-protocol.md` | 多 viewport 截图、视觉 finding、复验证据 | Phase 3 |
| `protocols/anti-ai-taste-gate.md` | Design Anti-AI Taste Gate、领域感、信息密度、文案质量 | Phase 4 |
| `templates/design-system-report-template.md` | readiness report 与 finding 模板 | Phase 5 |

## 2. 阶段骨架

每个 Phase 入口的 **MUST read** 指令是硬规则——不读 = 视为违反该 Phase 的安全与 UX 防御。

| Phase | 目标 | MUST read | 输出 |
| ------- | ------ | ----------- | ------ |
| Phase 1 — Scope & Sources | 确认 UI surface、NFR-UX、设计源与截图证据 | `protocols/component-token-a11y-protocol.md` | `/design-system-audit:COMPONENT_INVENTORY_READY` 或 `/design-system-audit:DESIGN_SOURCE_MISSING` |
| Phase 2 — Component / Token / A11y | 检查组件复用、tokens、状态面、A11y | `protocols/component-token-a11y-protocol.md` | findings |
| Phase 3 — Visual QA | 多 viewport / 状态截图、复验截图、视觉证据链 | `protocols/visual-qa-protocol.md` | `/design-system-audit:VISUAL_QA_PENDING` 或 pass |
| Phase 4 — Anti-AI Taste | 检查模板味、空洞文案、假精致、无领域信息 | `protocols/anti-ai-taste-gate.md` | `/design-system-audit:ANTI_AI_TASTE_BLOCKED` 或 pass |
| Phase 5 — Report & Route | 装配 readiness report 与修复 route | `templates/design-system-report-template.md` | `/design-system-audit:DESIGN_SYSTEM_READY` 或 blocking report |

## 3. 输出格式

```markdown
## 设计系统与视觉审计报告 (Design System Audit Report)

## 工作流状态 (Workflow State)

- State: /design-system-audit:<STATE>

## 审计范围 (Scope)

- 审计页面/组件 (Surfaces): <routes / components / screens>
- 规格设计锚点 (Source anchors): <NFR-UX-* / DSN-UI-*>

## 审计结论 (Verdict)

- 设计系统门禁结论 (Design System Gate): PASS / FAIL
- 阻碍性缺陷 (Blocking findings): <None or list>

## 推荐改善路由 (Required Route)

- /specs-write | /specs-execute | review | direct

```

## 4. 禁用行为

| 禁止项 | 原因 |
| -------- | ------ |
| 不把主观“好看”当 PASS | 必须有 tokens、截图、A11y、状态面证据 |
| 不把用户偏好静默写入 SSOT | 稳定偏好需用户批准 |
| 不用单一 viewport 通过视觉 QA | 响应式与状态面必须覆盖 |
| 不把模板化 UI 当现代感 | Anti-AI Taste Gate 必须检查领域信息密度 |
| 不直接写生产 UI 代码 | 修复归 `/specs-execute` 或 direct 小修 |

## 5. 快速自检清单

报告前自检：

- [ ] 是否已确认设计系统审计的页面（UI Surface）及 NFR-UX-* 锚点？
- [ ] 检查中是否覆盖了 Component 滥用、Token 漂移及基本的 A11y 交互状态？
- [ ] 视觉 QA（Visual QA）是否已完成多 Viewport/响应式截图验证？
- [ ] 交互设计和文案是否通过了 Anti-AI Taste Gate（排查模板化和空洞营销词汇）？
- [ ] 审计所得的 Findings 是否已整理好并提供了清晰的修复/整改路由？

## 支撑资源

- [anti-ai-taste-gate.md](./protocols/anti-ai-taste-gate.md)
- [component-token-a11y-protocol.md](./protocols/component-token-a11y-protocol.md)
- [decision-matrix.md](./references/decision-matrix.md)
- [design-system-report-template.md](./templates/design-system-report-template.md)
- [visual-qa-protocol.md](./protocols/visual-qa-protocol.md)
