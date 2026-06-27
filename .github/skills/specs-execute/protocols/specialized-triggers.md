# 规格执行专项触发器 (Specs Execute Specialized Triggers)

## 1. 目标

本文件补齐 `/specs-execute` 的专项触发器与“先看失败测试”纪律。它不改变单 Task 执行边界，只决定 Phase 1 如何识别入口、是否先读已有失败、以及 Red-Green-Refactor 如何避免跳过 Red。

## 2. 触发器规则表

| 规则 ID (Rule ID) | 前置条件 | 动作 | 下一步 | 禁止项 |
| --------- | ---------- | ------ | -------- | -------- |
| SET-1 | 用户显式 `/specs-execute TASK-###` | 按常规 Task 定位 | Phase 1 Locate | 不跳过 Context Required 复述 |
| SET-2 | 用户说“继续当前 approved task / 下一个 Pending task” | 定位唯一 Pending / In Progress Task | Phase 1 Locate | 多个候选时不得猜 |
| SET-3 | 用户提供失败测试、报错日志、CI 红灯、回归输出 | 先读失败输出并归档为 Failure Readback | Phase 1 Failure Readback | 不先改代码 |
| SET-4 | `/bug-audit` 输出修复路线且已有 approved spec Task | 读取 bug-audit handoff + Task 上游锚点 | Phase 2 Hydrate | 不绕过 spec 直接 patch |
| SET-5 | Task 类型为 constraint-verification / drift / grep / lint / fixture | 使用反向 Red 语义 | Phase 4 Red | 不以“脚手架任务”跳过 Red |
| SET-6 | 安全 / 发布 / 性能专项 workflow 输出 mitigation task | 读取对应 packet 引用 + Task Context | Phase 2 Hydrate | 不继承下游 workflow 的真实副作用授权 |
| SET-7 | 无 approved Task，仅有 bug / failing test | 分流 | `/bug-audit` 或 `/specs-write` | 不进入 `/specs-execute` |

## 3. Failure Readback（先看失败测试）

| 规则 ID (Rule ID) | 检查项 | PASS 标准 | FAIL 信号 |
| --------- | -------- | ----------- | ----------- |
| FR-1 | 失败原文读取 | 已读取用户提供日志、CI 输出、测试输出或本地失败命令输出 | 只看摘要或凭记忆判断 |
| FR-2 | 失败类型分类 | 分类为 assertion / import / env / flaky / timeout / contract drift / unknown | 未分类就改实现 |
| FR-3 | Spec 对照 | 失败断言可映射到 REQ / AC / DSN / EXIST / INV | 失败表达的是未批准需求 |
| FR-4 | Red 确认 | 若失败测试已存在且代表目标行为，可作为 Red；否则补写最小 Red | 把 unrelated failure 当 Red |
| FR-5 | 环境阻塞 | env / permission / dependency 类失败不当作业务 Red | 为环境问题改业务代码 |
| FR-6 | 记录 | Failure Readback 写入 Execution Notes | Done 后没有失败来源证据 |

## 4. Failure Readback 输出格式

```markdown
## 失败日志回读与审计 (Failure Readback)

|  | 审计字段 (Field) | 审计值 (Value) |  |  |  |  |
|  | ------- | ------- |  |  |  |  |
|  | 错误日志来源 (Source) | <user log / CI URL / command output / file path> |  |  |  |  |
|  | 运行命令 (Command) | <command or N/A> |  |  |  |  |
|  | 故障分类 (Failure Type) | 断言失败 (assertion) / 导入错误 (import) / 环境异常 (env) / 随机不稳定性 (flaky) / 超时 (timeout) / 契约漂移 (contract drift) / 未知 (unknown) |  |  |  |  |
|  | 关联规格锚点 (Related Anchor) | <REQ / AC / DSN / EXIST / INV or N/A> |  |  |  |  |
|  | 红灯就绪状态 (Red Status) | existing-red-valid / needs-new-red / env-blocked / spec-repair-required |  |  |  |  |
|  | 下一步行动建议 (Next Action) | <Phase 4 Red | /bug-audit | /specs-write | ENVIRONMENT_BLOCKED> |  |
```

## 5. Red-Green-Refactor 强化规则

| 规则 ID (Rule ID) | 场景 | Red 规则 | Green 规则 | Refactor 规则 |
| --------- | ------ | ---------- | ------------ | --------------- |
| RGR-1 | 新行为 Task | 先写或确认失败测试 | 最小实现使测试通过 | 不改外部行为 |
| RGR-2 | 既有失败测试修复 | 先读失败输出并确认与目标锚点一致 | 只修目标失败 | 相邻测试必须仍 Green |
| RGR-3 | 回归 bug | 先复现或固定 regression test | 修到 regression test 通过 | 不扩大 catch / 不吞错 |
| RGR-4 | constraint-verification | violation fixture 必须报警 | 合规 fixture 静默 | 保留 expected-fail fixture |
| RGR-5 | 无测试基础设施 | 记录 N/A 原因 + 补最小可验证命令 | 用可复检命令替代 | 不把“没测试”当 PASS |

## 6. 路由判定

| 条件 | 状态与路由 (State / Route) |
| ------ | --------------- |
| Failure Readback 映射到 approved Task | `/specs-execute:TASK_LOCATED` |
| Failure Readback 暴露 spec 缺陷 | `/specs-execute:SPEC_REPAIR_REQUIRED` → `/specs-write` |
| Failure Readback 影响面未知 | `/bug-audit` |
| Failure Readback 是环境问题 | `/specs-execute:ENVIRONMENT_BLOCKED` |
| Red / Green / Verify 全 PASS | `/specs-execute:TASK_DONE` |
