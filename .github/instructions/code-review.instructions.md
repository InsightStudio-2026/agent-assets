---
name: 代码审查
description: 当用户要求审查代码、review PR、检查变更、审计 diff 或进行代码质量检查时自动加载。不依赖文件匹配，仅凭任务语义触发。
applyTo: '**/*.{review,audit}.{md,json,yaml}'
---

# 代码审查规范

> 当任务涉及代码审查、diff 审计或质量检查时自动加载。

## 审查三维度

### 1. Standards（规范合规）

- 是否符合 DOM 决策归属？
- 是否触发了不必要的 Pause-and-Ask？
- 每一行 diff 是否能追溯到请求？
- 是否有"顺手改进"邻近代码？

### 2. Spec（规格一致）

- 是否覆盖了需求中的所有 REQ？
- 验收标准是否可验证？
- 是否有 Spec Breach？

### 3. Verification（验证完整）

- 测试是否通过？
- DoD 门禁是否全部绿灯？
- 是否有残留调试代码？

## 高风险扩展审查

命中以下条件时追加四轴审查：

- **Risk Gates**：触及 Gate C 边界（生产写入、删除数据等）
- **Architecture**：新依赖、新模块、跨层调用
- **Operability**：迁移脚本、环境配置、CI/CD 变更
- **Authorship**：版权声明、AI 残留、占位符

## 审查流程

1. 读取 `.github/skills/review/SKILL.md`
2. 获取待审查 diff
3. 逐文件逐变更过三条轴线
4. 输出结构化报告

详见 `@.github/prompts/code-review.prompt.md`
