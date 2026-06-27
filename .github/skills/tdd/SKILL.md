---
name: tdd
description: >
  使用 Red-Green-Refactor 闭环进行测试驱动开发。Use when user wants to build features or fix bugs using TDD,
  mentions "red-green-refactor", wants integration tests, asks for test-first development, or says 测试先行/TDD。
---

# 测试驱动开发（tdd）

## 0. 触发与临界路由

| ID | 前置条件 | 匹配动作 | 下一步/目标路由 | 源 / 备注 |
| ---- | ---------- | ---------- | ----------------- | ----------- |
| R-ROUTE-TDD-1 | 用户显式提及 `tdd` 技能或通过 `@tdd` 调用 | 启用本技能 | 进入 规划 (Phase 1) | 显式入口 |
| R-ROUTE-TDD-2 | 用户提出要以 TDD / 测试先行方式构建一个局部简单功能或修复已知小 bug | 启用本技能 | 进入 规划 (Phase 1) | 局部 TDD 驱动 |
| R-ROUTE-TDD-3 | 系统状态不清、下一步推进方向不明 | 停止并重定向 | 路由至 `/project-steward` | 临界状态 1 |
| R-ROUTE-TDD-4 | 缺失母本或 L1 SSOT | 停止并重定向 | 路由至 `/project-inception` | 临界状态 2 |
| R-ROUTE-TDD-5 | 需要构建的新功能或变更偏复杂，涉及多模块、Schema、外部 API、权限或计费 | 停止并重定向 | 路由至 `/specs-write` 与 `/specs-execute` | 临界状态 4 |
| R-ROUTE-TDD-6 | 属于纯缺陷根因诊断且尚未定位 Bug 根因 | 停止并重定向 | 路由至 `diagnose` 技能 | 临界状态 3 |
| R-ROUTE-TDD-7 | 缺陷的系统性影响面、严重性或风险分级未知 | 停止并重定向 | 路由至 `/bug-audit` | 缺陷审计引流 |

## 哲学

**核心原则**：测试应该通过公共接口验证行为，而不是验证实现细节。代码可以彻底重构；测试不应该因此破裂。

**好测试**偏集成风格：通过公共 API 走真实代码路径。它描述系统“做什么”，而不是“怎么做”。好测试读起来像规格，例如“用户可以用有效购物车结账”明确说明能力是什么。因为不关心内部结构，这类测试能穿过重构存活。

**坏测试**耦合实现：mock 内部协作者、测试私有方法，或绕过接口从外部验证状态，例如直接查数据库。警告信号是：你重构了内部结构，行为没变，测试却失败。若改名一个内部函数导致测试失败，那测试测的是实现，不是行为。

示例见 [tests.md](references/tests.md)，mock 准则见 [mocking.md](references/mocking.md)。

## 反模式：水平切片

**不要先写完所有测试，再写所有实现。** 这是“水平切片”：把 RED 当成“写所有测试”，把 GREEN 当成“写所有代码”。

这会制造差测试：

- 批量写出的测试验证的是**想象中的行为**，不是实际行为。
- 容易测试数据结构、函数签名等“形状”，而不是用户可见行为。
- 测试对真实变化不敏感：行为坏了也可能过，行为没坏却可能失败。
- 在理解实现前就锁死测试结构。

**正确方式**：通过 tracer bullet 做垂直切片。一个测试 → 一个实现 → 重复。每个测试都响应上一轮学到的东西。因为刚写完代码，你更清楚哪些行为重要、如何验证。

```text
WRONG (horizontal):
  RED:   test1, test2, test3, test4, test5
  GREEN: impl1, impl2, impl3, impl4, impl5

RIGHT (vertical):
  RED→GREEN: test1→impl1
  RED→GREEN: test2→impl2
  RED→GREEN: test3→impl3
  ...
```

## 工作流

### 1. 规划

探索代码库时，使用项目领域词汇，让测试名与接口词汇匹配项目语言，并尊重触达区域的 ADR。

写代码前：

- [ ] 明确要验证的可观察行为，而不是实现步骤。
- [ ] 识别公共接口变化；能从 spec、现有接口和调用点推断时，由代理作为 DRI 决策。
- [ ] 只有公共接口、验收优先级或真实世界副作用无法安全自决时，才向用户确认。
- [ ] 识别 [deep modules](references/deep-modules.md) 机会：小接口，深实现。
- [ ] 按 [testability](references/interface-design.md) 设计接口。
- [ ] 把测试努力集中在关键路径和复杂逻辑，不追求覆盖每个边角。

必要时问：“公共接口应该长什么样？哪些行为最值得优先锁定？”

### 2. Tracer Bullet

先写一个测试，只确认系统的一件事：

```yaml
RED:   为第一个行为写测试 → 测试失败
GREEN: 写最小实现使其通过 → 测试通过
```

这是 tracer bullet：证明路径端到端可走。

### 3. 增量循环

对剩余行为逐个重复：

```yaml
RED:   写下一个测试 → 失败
GREEN: 写最小代码通过当前测试 → 通过
```

规则：

- 一次只写一个测试。
- 只写足够通过当前测试的代码。
- 不预支未来测试。
- 测试始终聚焦可观察行为。

### 4. 重构

全部测试通过后，寻找 [refactor candidates](references/refactoring.md)：

- [ ] 抽取重复。
- [ ] 加深模块：把复杂度移到简单接口后面。
- [ ] 在自然适配处应用 SOLID 原则。
- [ ] 观察新代码暴露出的既有问题。
- [ ] 每一步重构后运行测试。

**RED 状态下永远不要重构。**先回到 GREEN。

## 每轮检查清单

```text
[ ] 测试描述行为，而不是实现
[ ] 测试只使用公共接口
[ ] 测试能穿过内部重构存活
[ ] 代码只是当前测试所需的最小实现
[ ] 没有加入推测性功能
```

## 测试反模式与 Mock 核心卫兵

### 1. 三大铁律（Iron Laws）

-**铁律一：严禁测试 Mock 行为**。Mock 只是隔离外部慢速/不可达环境的手段，绝不是测试的目标。永远不要断言 `*-mock` test ID 的存在，而必须测试组件在有 Mock 时暴露的**真实公共行为**。

- **铁律二：严禁向生产代码注入 test-only 方法**。严禁在生产类（Production Classes）中添加任何仅服务于测试 `afterEach` 清理的生产级接口（例如 `Session.destroy()`）。测试清理逻辑必须独立拆出并外置于 `test-utils` 清理器中，保持生产 API 的 YAGNI 洁净度。
- **铁律三：严禁不完整 Mock**。一旦决定使用 Mock，必须高保真地还原真实 API 响应的 **完整数据结构与 Schema**（即便当前测试只消费一两个字段）。不完整的 Mock 会在下游隐式链路迭代时掩盖集成雪崩，制造危险的虚假绿灯。

### 2. 反作弊阻断门（Anti-Cheat Gate）

```text
[CHECK] 准备在测试中断言 Mock 元素或追加 Mock 时：

  1. 我是在验证 real component 的行为，还是在验证 mock 的存在？
     --> 若是后者，立即停止并重构，不准提交。
  2. 我要为 production class 增加清理方法吗？
     --> 立即停止，该清理逻辑必须写入 test utilities 辅助文件。
  3. 我的 Mock 返回值是否完整镜像了真实的生产 API 结构？
     --> 若非全字段镜像，必须补充完整 Schema，防 silent integration leaks。

```

## 支撑资源

- [deep-modules.md](./references/deep-modules.md)
- [interface-design.md](./references/interface-design.md)
- [mocking.md](./references/mocking.md)
- [refactoring.md](./references/refactoring.md)
- [tests.md](./references/tests.md)
