# 规格设计编排与执行引擎 (Specs Write Orchestration)

## 阶段输出契约 (Phase Output Contract)

每件交付的三段输出不可缺、不可换序：

- **段 1 总结**· 已完成 `<file>.md`（REQ=N · DSN=N · TASK=N · BDD=N）

-**段 2 Critical Assumptions Summary**（详下节）

- **段 3 Gate 判定**（详 `cross-cutting.md §2`）：Gate N/A → AI-DRI 自动进下一 Phase / Gate A/B/C 命中 → 强推荐 + ≤ 2 备选 + 代价，等白名单批准 / 修订 → 修当前文件或回跳上游

## 关键假设摘要规则 (Critical Assumptions Summary)

- **数量**：requirements / design 至少 1 条、最多 3 条；超出 = 收敛不足。maturity-intake / charter / audit / tasks 可填 N/A 但必说明原因
- **格式**：每条 3 段（原文 1 句 / 破坏点 ID / 若不成立 → 需打回重做的具体节点与范围）
- **空话黑名单**（见即未完）：「一切都很好」/「未发现问题」/「设计合理」/「按惯例」/「同项目习惯」

## 阶段输出骨架 (Phase Output Skeleton)

**Step 1 写文件**→ 按 `../templates/<file>.md` 模板落地。**Step 2 三段输出**→ 按本文件 `Phase Output Contract`。**Step 3 Gate 判定后续动作**：Gate N/A → AI-DRI 自动推进（Notes 写 `AI-DRI auto-approved` 留痕，详 `cross-cutting.md §2.3`）/ Gate A/B/C 命中 → 强推荐 + ≤ 2 备选 + 代价 → 等待用户白名单批准 / Spec Breach → 停下请求修订 / 用户主动修订 → 修订当前文件或回跳上游。

## 子文档路由指南 (Child Document Routing Reference)

以下主题触发即读（详细规则都在 `../` 下）：

- **横切契约**·`cross-cutting.md`：§1 标识与追溯 / §2 Decision Gate / §3 EARS·BDD·TDD / §4 Spec Contract Schema / §5 INV-*
- **禁令与停止**：`forbidden-actions.md`（30+ 条 Phase 级严禁 + 处置锚点） + `stop-conditions.md`（Phase Stop Conditions Matrix）
- **Project Adapter**·`project-adapter.md`：项目级槽位（脚本 / 工具 / attention_budget / shell / OS）+ INV-* 示例库
- **出口自检**·`self-check.md`：Phase 0→§1 / 1→§2 / 1.5→§3 / 2→§4 / 3→§5 / 4→§6 / 5→§7
- **高级防线**·`appendix.md`：§A.1 防 1 Traceability 双源 / §A.2 防 2 BDD + Test Anchors / §A.3 防 3 Revert Conflict / §A.4 防 4 Audit Evidence 外置 / §A.5 防 5 Context Required + Anti-Invariants / §A.6 抢占式中断（禁用 git stash）/ §A.7 Implementation Reflections + active→done 迁移

## 运行示例 (Usage Example)

用户：`/specs-write` 或描述新功能。AI 依次走 Phase 0 → 1 → [1.5] → 2 → 3 → 4 → 5；每 Phase 开头按入口文件 `Companion Documents` 表读子文档，结尾勾 `self-check.md` + 走 `cross-cutting.md §2` Gate 判定。完整示例见 `../templates/maturity-intake.md`。
