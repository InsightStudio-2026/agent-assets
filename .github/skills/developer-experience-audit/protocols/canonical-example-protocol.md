# 典型样例协议 (Canonical Example Protocol)

## 1. 目标

验证 canonical examples 是否能作为契约测试和上手样本，而不是不可复检的教程文本。

## 2. Example 覆盖矩阵

| Example ID | 路径 | 期望覆盖 | 关联 fixture / check |
| ------------ | ------ | ---------- | ---------------------- |
| EX-G-1 | `../../specs-write/examples/EX-G-1/` | Greenfield happy path + NFR 六类槽位 | R-CHK-EX-1.*+ F-FIX-8 A |
| EX-B-1 | `../../specs-write/examples/EX-B-1/` | Brownfield delta + NFR Delta Operation | R-CHK-EX-1.* + F-FIX-8 B |
| EX-M-1 | `../../specs-write/examples/EX-M-1/` | Medium / single-file 裁剪 | R-CHK-EX-1.* |
| EX-R-1 | `../../specs-write/examples/EX-R-1/` | Spec repair / 回切 | R-CHK-EX-1.* |
| EX-A-1 | `../../specs-write/examples/EX-A-1/` | archive / merge 归档回并 | R-CHK-EX-1.* |

## 3. 审计规则

| 规则 ID (Rule ID) | 检查项 | PASS 标准 | FAIL 信号 |
| --------- | -------- | ----------- | ----------- |
| CE-R1 | 可定位 | examples README 能指向 5 个 example | 新 agent 不知道从哪个样例开始 |
| CE-R2 | 用例不重叠 | 每个 example 覆盖不同 learning target | 多个 example 只是同一 happy path 复写 |
| CE-R3 | 可对照 fixture | 至少关键失败模式有 F-FIX-* 对照 | 只有正例，无失败样本 |
| CE-R4 | NFR 覆盖 | EX-G-1 / EX-B-1 覆盖 NFR 六类与 Brownfield Delta Operation | NFR 只是标题或空表 |
| CE-R5 | 路由锚点有效 | Routed-to 指向真实 workflow 或明确 N/A | 指向不存在 workflow / 锚点 |
| CE-R6 | 不当教程化 | 示例服务契约验证，不引入人类学习路径或耗时承诺 | 写成散文式或课程式教程，脱离 conformance |

## 4. 复检表

| 样例 (Example) | CE-R1 | CE-R2 | CE-R3 | CE-R4 | CE-R5 | CE-R6 | 判定结论 (Verdict) |
| --------- | ------- | ------- | ------- | ------- | ------- | ------- | --------- |
| EX-G-1 | PASS / FAIL | PASS / FAIL | PASS / FAIL | PASS / FAIL | PASS / FAIL | PASS / FAIL | PASS / FAIL |
| EX-B-1 | PASS / FAIL | PASS / FAIL | PASS / FAIL | PASS / FAIL | PASS / FAIL | PASS / FAIL | PASS / FAIL |
| EX-M-1 | PASS / FAIL | PASS / FAIL | PASS / FAIL | N/A | PASS / FAIL | PASS / FAIL | PASS / FAIL |
| EX-R-1 | PASS / FAIL | PASS / FAIL | PASS / FAIL | N/A | PASS / FAIL | PASS / FAIL | PASS / FAIL |
| EX-A-1 | PASS / FAIL | PASS / FAIL | PASS / FAIL | N/A | PASS / FAIL | PASS / FAIL | PASS / FAIL |

## 5. 判定与路由

| 条件 | 状态与路由 (State / Route) |
| ------ | --------------- |
| 全部 example 可定位且 learning target 不重叠 | `/developer-experience-audit:CANONICAL_EXAMPLES_VERIFIED` |
| 缺 fixture 对照或 R-CHK 失败 | `/asset-quality-gates` Phase 3.6 |
| 示例内容与 specs-write 方法论漂移 | `/specs-write` 修订对应支撑文档 |
| Routed-to 指向不存在资产 | direct asset maintenance + AGENTS 索引核验 |
