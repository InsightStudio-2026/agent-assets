# charter.md 模板

> **When to read**: 在 `/specs-write` Phase 1 落 charter.md 时读取本文。

## Charter — `<Feature Name>`

Feature Slug: `<feature-slug>`
Created: `<YYYY-MM-DD>`

## 1. Sources（输入源清单）

| ID | Type | Path / Origin | Authority |
| ---- | ------ | --------------- | ----------- |
| SRC-001 | SSOT | docs/blueprints/母本.md | Authoritative |
| SRC-002 | SSOT | docs/<主文档>.md | Authoritative |
| SRC-003 | Reference | docs/notes/<参考>.md | Reference |
| SRC-004 | Discussion | conversation 2026-05-06 14:30 UTC+8（试手感选题与默认参数确认） | Reference |
| SRC-005 | Inspiration | 用户行业访谈摘要 2026-04-20（跨语种互学场景假设） | Inspiration |

> Authority 取值：
>
> - **Authoritative**：必须遵守、必须引用、不得违背
> - **Reference**：可参考，spec 可超越但需说明
> - **Inspiration**：仅启发，不约束
>
> Discussion / Inspiration / User Statement 类必须附时间戳或会话 ID。

## 2. Mode

- Mode: Seed / Init | Greenfield | Hybrid | Brownfield
- Reason: <为什么是这个模式>
- Audit Profile: Baseline Survey | Greenfield Survey | Feature-Scoped Full-Surface Audit
- SSOT Health: Healthy | Needs Clarification | Needs Repair | Unfit As Source | SSOT Absent
- Maturity Intake Ref: maturity-intake.md#Decision-Summary

## 3. Complexity

- Complexity: Small | Medium | Large

## 3.5 Opening Questions & Decisions（阻塞优先）

- Open Questions（≤ 5，开工必答优先）:
  - Q1: <问题> · Gate: A | B | N/A · Recommended: <AI 强推荐>
- Decisions Required:
  - L-STRAT: <产品方向 / 商业 / 合规 / 资源投入；无则 N/A>
  - L-DESIGN: <架构 / Schema / API / 外部依赖；无则 N/A>
  - L-IMPL: <实现细节，AI-DRI 自决留痕；无则 N/A>
  - L-OPS: <运行 / 部署 / 验证细节，AI-DRI 自决留痕；无则 N/A>

## 4. Derivation Constraints（派生约束）

- 凡涉及 <概念 A>，必须引用 SRC-001#<章节>
- 凡涉及 <概念 B>，必须引用 SRC-002#<章节>
- 不得重新定义以上 SSOT 已定义的概念

## 5. Architectural Invariants（技术红线 · 见 §3.5 模板）

> 跨 phase 全程生效。下游引入与本节冲突的能力 / 依赖 / 部署形态 → 视为越界，必须停下回 charter 修订重批。每条需限 `INV-*` ID 以便下游追溯。

### 5.1 绝对禁用（Hard Bans · INV-BAN-*）

| Invariant | Reason | 作用范围 |
| ----------- | -------- | ---------- |
| INV-BAN-001：<规则> | <理由> | <范围> |

### 5.2 严格限定（Hard Constraints · INV-LIM-*）

| Invariant | Reason | 作用范围 |
| ----------- | -------- | ---------- |
| INV-LIM-001：<规则> | <理由> | <范围> |

### 5.3 安全红线（Security Invariants · INV-SEC-* · 可选维度）

> 项目涉及外部凭据 / API Key / Token / PII / 内网拓扑 / 交易接口 / 企业隐私者，应至少声明 1 条 INV-SEC-*；纯本地工具无敏感数据可豁免本栏并在 §6 Out of Charter 注明「无 INV-SEC 适用」。

| Invariant | Reason | 作用范围 |
| ----------- | -------- | ---------- |
| INV-SEC-001：<规则> | <理由> | <范围> |

> 本节由项目层填写；示例库见 `project-adapter.md §2`。新增条目应同步回流 `@.github/instructions/`，避免红线随 spec 生灭。

## 6. Out of Charter（明确不做）

- 本 Spec 不修订 SRC-001 / SRC-002；如发现冲突，进入 SSOT 修订流程（§3.1.4-B 派生协议）
- 本 Spec 不引入新的 ...
- （可选）无 INV-SEC 适用：理由

## 7. Critical Assumptions Summary

- 至少 1 条，最多 3 条；标注 `Confidence: <high|mid|low>` 与 `Validation: <如何验证>`
- 或填 `N/A: <为何 charter 无 Critical Assumption>`

## 8. Approval

- Status: Acknowledged
- Notes: <如有用户反馈记录>
- Timestamp: <ISO 8601>
