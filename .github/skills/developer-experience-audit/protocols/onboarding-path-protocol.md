# 上手路径协议 (Onboarding Path Protocol)

## 1. 核心上手事实源三件套

DevEx 审计必须验证以下三件套作为新上手的标准入口事实源：

| 事实源 ID (Source ID) | 事实源 | 角色 |
| ----------- | -------- | ------ |
| OP-SRC-1 | `../../specs-write/protocols/methodology-kernel.md` | 一页说明 spec 生命周期语义层、delta operation、裁剪规则、archive / merge 关系 |
| OP-SRC-2 | `../../specs-write/protocols/entry-decision-tree.md` | 从请求类型路由到正确 workflow / mode |
| OP-SRC-3 | `../../specs-write/references/cross-cutting.md §6` | 反模式与修复查询表，帮助失败自救 |
| OP-SRC-4 | `../../specs-write/examples/` | happy path / Brownfield delta / repair / archive 的可复检例子 |

## 2. Medium spec 上手检查

| 规则 ID (Rule ID) | 检查项 | PASS 标准 | FAIL 信号 |
| --------- | -------- | ----------- | ----------- |
| OP-R1 | 入口可定位 | 新 agent 能从 workflow 入口定位 OP-SRC-1~3 | 入口只指向废弃 quickstart 或散文说明 |
| OP-R2 | 路由可判定 | 常见请求能通过 entry decision tree 得出唯一推荐 workflow | 需要主观猜测或问用户实现细节 |
| OP-R3 | Medium spec 可完成 | 不通读全部支撑文档也能写出 charter / audit / requirements / design / tasks 的合格裁剪 | 必须翻全库才能知道格式 |
| OP-R4 | Brownfield delta 可表达 | 能找到 Add / Modify / Replace / Deprecate / Preserve 示例 | Brownfield 只能重写全量规格 |
| OP-R5 | 失败自救可查 | 常见错误能从 cross-cutting §6 找到修复路径 | 失败后无归因 / 无 route |
| OP-R6 | NFR 上游清楚 | NFR-* 六类槽位能路由到专项 workflow | NFR 只剩泛泛质量要求 |

## 3. Eval prompt 表

| 评估用例 ID (Case ID) | 用户提示词 (Prompt) | 预期路由 (Expected Route) | 预期参考事实源 (Expected Sources) | 判定结论 (Verdict) |
| --------- | -------- | ---------------- | ------------------ | --------- |
| OP-CASE-1 | “我有一个中等复杂新功能，要写 spec” | `/specs-write` | OP-SRC-1 + OP-SRC-2 | PASS / FAIL |
| OP-CASE-2 | “我要把旧通知服务替换成 Mailgun” | `/specs-write` Brownfield delta | OP-SRC-1 + EX-B-1 | PASS / FAIL |
| OP-CASE-3 | “spec 写完但 NFR-PERF 缺 baseline” | `/performance-reliability-audit` 或补 requirements §10 | OP-SRC-2 + examples | PASS / FAIL |
| OP-CASE-4 | “我不知道为什么这个 spec 被 gate 卡住” | cross-cutting §6 | OP-SRC-3 | PASS / FAIL |

## 4. 输出

| 字段 | 内容 |
| ------ | ------ |
| Onboarding Verdict | PASS / FAIL |
| Missing Source | OP-SRC-* 缺口 |
| Friction Point | 新 agent 首次卡住的位置 |
| Route | direct asset maintenance / `/specs-write` / `/asset-quality-gates` |
