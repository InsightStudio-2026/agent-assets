---
name: skill-eval
description: >
  评估 agent skill 的触发精度、反触发边界、渐进披露、用例覆盖、eval fixture、benchmark 与 provenance 证据。
  Use when auditing or designing a skill evaluation suite, trigger/anti-trigger rules, skill benchmarks, or asks skill 评测 / eval / benchmark / provenance / 触发描述校验。
---

# Skill 评测（skill-eval）

## 定位

评估单个或一组 skill 是否能被代理稳定、准确、低误触发地使用；输出可交给 `/asset-quality-gates` 的 eval packet。只评估 skill 资产质量，不替代 workflow 状态机审计，也不直接改业务代码。

## 输入

| 输入 | 必填 | 说明 |
| ------ | ------ | ------ |
| Target Skill | 是 | `.github/skills/<name>/SKILL.md` |
| Intended Use Cases | 是 | 该 skill 应触发的代表性请求 |
| Anti-Use Cases | 是 | 该 skill 不应触发的相邻请求 |
| Supporting Files | 否 | 同目录支撑文档、示例、脚本 |
| Provenance | 外部来源时必填 | 来源、license、改造说明、启用路径 |

## 评估规则表

| Rule ID | 检查项 | PASS 标准 | FAIL 信号 |
| --------- | -------- | ----------- | ----------- |
| SE-1 | `description` 触发精度 | 第一段说明能力；含 `Use when`；触发词具体 | 泛化如 “helps with code”；缺中文触发词；与现有 skill 重叠 |
| SE-2 | 反触发边界 | 明确哪些相邻任务不应使用本 skill | 与 workflow / 其他 skill 职责混淆 |
| SE-3 | 渐进披露 | `SKILL.md` 是入口；低频细节在支撑文件 | 入口堆满长背景、模板或大段参考材料 |
| SE-4 | 用例覆盖 | 至少 3 个正例、3 个反例、1 个边界例 | 只写 happy path；无误触发样本 |
| SE-5 | 可复检 fixture | 每个 eval case 有输入、期望是否触发、期望输出形态 | 只有主观描述，无法复跑 |
| SE-6 | Benchmark 口径 | 有 precision / recall / false-positive / false-negative 记录口径 | 只写 “好用 / 不好用” |
| SE-7 | Provenance | 外部机制有来源、license、改造点、不吸收清单 | 复制外部资产但无来源或 license |
| SE-8 | 索引与边界 | 启用 skill 已登记 `AGENTS.md`；Role 合理 | 目录存在但未登记，或 Personal 资产误标 Active |

## Eval Case 格式

| 字段 | 内容 |
| ------ | ------ |
| Case ID | `SE-CASE-`<skill>`-<NN>` |
| Input Prompt | 用户原始请求样本 |
| Expected Trigger | `MUST_TRIGGER` / `MUST_NOT_TRIGGER` / `MAY_TRIGGER_WITH_CONTEXT` |
| Expected Behavior | 应读取哪些文件、输出什么形态、不得做什么 |
| Evidence | 关联规则 ID 与文件路径 |

## 输出格式 (Output Format)

```markdown
## Skill 评估包 (Skill Eval Packet)

## 评估目标 (Target)

- 技能名称 (Skill): <name>
- 物理路径 (Path): .github/skills/<name>/SKILL.md

## 评估结论 (Verdict)

- 总体结论 (Overall): PASS / FAIL / NEEDS_REVISION
- 触发阻塞规则 (Blocking Rules): <SE-* or None>

## 触发精准度 (Trigger Quality)
|  | 用例 ID (Case ID) | 预期触发状态 (Expected Trigger) | 实际判定 (Actual Judgment) | 结论 (Verdict) |  |
|  | --------- | ------------------ | ----------------- | --------- |  |

## 细则检查结果 (Rule Results)
|  | 规则 ID (Rule ID) | 结论 (Verdict) | 事实依据 (Evidence) | 改进要求 (Required Fix) |  |
|  | --------- | --------- | ---------- | -------------- |  |

## 来源及沿革说明 (Provenance)

- 来源渠道 (Source): <internal / external URL + commit>
- 许可证协议 (License): <license or N/A>
- 适配改造记录 (Adaptation Notes): <改造点>
- 外部未吸收项 (Not Absorbed): <外部机制未吸收项>

## 交接与执行 (Handoff)

- 分流目标 (Route to): /asset-quality-gates or direct asset maintenance
- 下一步行动 (Required next action): <具体修订或登记动作>

```

## 禁止动作

| 禁止项 | 原因 |
| -------- | ------ |
| 不把 skill eval 当 workflow gate 通过证明 | workflow 入口、状态机、Route Action 仍归 `/asset-quality-gates` |
| 不为追求触发率扩大 `description` 到泛化词 | 会造成误触发和 skill 冲突 |
| 不把外部 skill 原样复制进启用路径 | 必须先 provenance / license / quarantine / 适配 |
| 不把 Personal skill 直接标 Active | 需清理私人路径与复用边界 |
