# Phase Stop Conditions Matrix（唯一停止与前置条件矩阵）

> **When to read**: 在 `/specs-write` 任一 Phase 进入下阶段前，或判断是否必须停止时读取本文。

| 当前阶段 | 产出 | 必停时机 | 进入下阶段条件 | 否决态 |
| ---------- | ------ | ---------- | ---------------- | -------- |
| 0 Maturity Intake | `maturity-intake.md` | Decision = `BLOCKED_SSOT_REPAIR` / `BLOCKED_UNFIT_SOURCE` / Gate A 命中 | maturity-intake.Status = Approved（Gate N/A 时 AI-DRI 自动批准） + Decision = PROCEED_TO_CHARTER（SSOT Health ∈ {Healthy, Needs Clarification, SSOT Absent}；`SSOT Absent` 需附 `templates/maturity-intake.md §Phase 0 判定硬规则` 规定的 charter 标注 + Open Questions SSOT 重建计划 + Stewardship Suggestions 草案） | 无 |
| 1 Charter | `charter.md` | Spec Breach / Open Questions 含 L-STRAT 必停项 | charter.Status = Acknowledged + 模式合规 | charter 不走完整 Decision Gate |
| 1.5 Audit | `audit.md` | Conflict-with-SSOT 类硬阻塞 / Audit Depth Gate = BLOCKED_AUDIT_DEBT | audit.Status = Approved + Audit Depth Gate = PASS_TO_REQUIREMENTS | 仅 Hybrid / Brownfield 模式 |
| 2 Requirements | `requirements.md` | Gate A/B / 缺 EARS+BDD 配对 / 失败分支缺失 | requirements.Status = Approved（用户 Gate 批准或 AI-DRI 自动批准） | 无 |
| 3 Design | `design.md` | Gate B/C / Spec Breach / 跨边界 DSN 漏 Failure Strategy / DSN-LLM 三件防御不全 | design.Status = Approved（用户 Gate 批准或 AI-DRI 自动批准） | Medium 路径①跳过 |
| 4 Tasks | `tasks.md` | Gate B/C / Spec Breach / 硬阻塞命中 | tasks.Status = Approved（用户 Gate 批准或 AI-DRI 自动批准） | 无 |
| 5 Handoff | `handoff-payload.yaml` + 人读简报 | handoff 发现 Gate 漏判或 payload 结构不合法 | AI-DRI 自动切换 `/specs-execute` 建议；无需用户再次批准 | 无 |

每阶段交付时必须输出三段（详主 workflow §0.4）：**段 1 总结 → 段 2 Critical Assumptions Summary → 段 3 Gate 判定**。
