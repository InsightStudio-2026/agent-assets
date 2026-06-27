# Phase Stop Conditions Matrix（唯一停止与前置条件矩阵）

> **When to read**: 在 `/specs-write` 任一 Phase 进入下阶段前，或判断是否必须停止时读取本文。

| 当前阶段 | 产出 | 必停时机 | 进入下阶段条件 | 否决态 |
| ---------- | ------ | ---------- | ---------------- | -------- |
| 0 Maturity Intake | `maturity-intake.md` | Decision = `BLOCKED_SSOT_REPAIR` / `BLOCKED_UNFIT_SOURCE` / Gate A 命中 | maturity-intake.Status = Approved（Gate N/A 时 AI-DRI 自动批准） + Decision = PROCEED_TO_CHARTER（SSOT Health ∈ {Healthy, Needs Clarification, SSOT Absent}；`SSOT Absent` 需附 `templates/maturity-intake.md §Phase 0 判定硬规则` 规定的 charter 标注 + Open Questions SSOT 重建计划 + Stewardship Suggestions 草案） | 无 |
| 1 Charter | `charter.md` | Spec Breach / Open Questions 含 L-STRAT 必停项 / **Out-of-Charter 含上游 SSOT 明确要求的功能且未附 Exclusion Justification** | charter.Status = Acknowledged + 模式合规 + Out-of-Charter 降级项均附 Justification（见 §3 反降级规则） | charter 不走完整 Decision Gate |
| 1.5 Audit | `audit.md` | Conflict-with-SSOT 类硬阻塞 / Audit Depth Gate = BLOCKED_AUDIT_DEBT | audit.Status = Approved + Audit Depth Gate = PASS_TO_REQUIREMENTS | 仅 Hybrid / Brownfield 模式 |
| 2 Requirements | `requirements.md` | Gate A/B / 缺 EARS+BDD 配对 / 失败分支缺失 / **SSOT 覆盖率门禁未通过（charter Sources 表有 SRC 节未被任何 REQ 的 Derived From 覆盖且未在 Out of Charter 排除）** | requirements.Status = Approved（用户 Gate 批准或 AI-DRI 自动批准）+ SSOT Coverage Gate PASS（见 §2 覆盖率门禁） | 无 |
| 3 Design | `design.md` | Gate B/C / Spec Breach / 跨边界 DSN 漏 Failure Strategy / DSN-LLM 三件防御不全 | design.Status = Approved（用户 Gate 批准或 AI-DRI 自动批准） | Medium 路径①跳过 |
| 4 Tasks | `tasks.md` | Gate B/C / Spec Breach / 硬阻塞命中 | tasks.Status = Approved（用户 Gate 批准或 AI-DRI 自动批准） | 无 |
| 5 Handoff | `handoff-payload.yaml` + 人读简报 | handoff 发现 Gate 漏判或 payload 结构不合法 | AI-DRI 自动切换 `/specs-execute` 建议；无需用户再次批准 | 无 |

每阶段交付时必须输出三段（详主 workflow §0.4）：**段 1 总结 → 段 2 Critical Assumptions Summary → 段 3 Gate 判定**。

---

## §2 SSOT 覆盖率门禁（Coverage Gate）

- **触发时机**：Phase 2（Requirements）出口
- **规则**：charter §1 Sources 表登记的每个 `SRC-###` 节，必须在 requirements.md §8 Derivation Map 中有 ≥1 条 REQ 声明 `Derived From: SRC-###`
- **未覆盖处置**：
  - 未覆盖的 SRC 节 → 补 REQ 覆盖
  - 若该 SRC 节确属本 Phase 范围外 → 必须在 charter §6 Out of Charter 中显式排除并附 `Exclusion Justification`
- **验证命令**：提取 charter Sources 的 SRC ID 集合与 requirements Derivation Map 的 SRC ID 集合求差集 → 差集必须为空或全部在 Out of Charter 中有 Justification
- **与现有 Derivation Map 的关系**：Derivation Map（REQ→SRC 正向）是必要但不充分条件——本门禁补足了反向（SRC→REQ）的覆盖验证

---

## §3 Out-of-Charter 反降级约束

- **触发时机**：Phase 1（Charter）出口
- **规则**：Out of Charter 中的每一项若满足以下任一条件 → 自动升级为 **Gate B**（需用户拍板）：
  1. 出现在上游 SSOT 本 Phase 范围内（即上游 SSOT 明确将其列为当前阶段交付物）
  2. 未被上游 SSOT 的 Out-of-Scope 声明覆盖
  3. 涉及数据持久化 / 安全 / 合规
- **格式要求**：升级项必须附加：
  - `Exclusion Justification: <≥1 句理由>`
  - `Gate: B — 请确认排除`
- **处置**：用户确认排除 → 保留在 Out of Charter 并引用用户原话作为批准留痕；用户拒绝排除 → 移回 In-Scope，补对应 REQ/DSN/TASK
