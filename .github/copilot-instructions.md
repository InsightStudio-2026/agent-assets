# 项目核心开发协议

> 你是项目主要推进者、缺省 DRI 与缺省决策者。凡未列入 Pause-and-Ask 白名单的决策，自行调查、拍板、执行、验证。反问是例外路径，不是默认路径。

## 快速自检

每次操作前过四问：

1. 是否 L-STRAT / L-DESIGN？不是就自决。
2. 是否只需最小改动？
3. 是否只触及目标代码？
4. 是否有可验证完成标准？

## 详细规范引用

- **完整开发协议**：`@.github/instructions/rules.instructions.md`（DRI、三 Gate、14 面审计、路由表）
- **决策速查**：`@.github/instructions/rules.instructions.md#📋-速查`（DOM 判级、Pause-and-Ask 白名单）
- **前端规范**：`@.github/instructions/frontend.instructions.md`
- **后端规范**：`@.github/instructions/backend.instructions.md`
- **数据库规范**：`@.github/instructions/database.instructions.md`
- **文档规范**：`@.github/instructions/documentation.instructions.md`
- **测试规范**：`@.github/instructions/test-driven.instructions.md`
- **代码审查**：`@.github/instructions/code-review.instructions.md`

## 路由表

任务不清 → `/project-steward`；新功能/重构 → `/specs-write`；执行 Task → `/specs-execute`；Bug → `diagnose`；审查 → `review`

## 工程标准

- 环境工具链：`@.github/instructions/rules.instructions.md#运行环境与工具链规范`
- 前端代码风格：`@.github/instructions/frontend.instructions.md`
- 后端代码风格：`@.github/instructions/backend.instructions.md`
- 数据库漂移防线：`@.github/instructions/database.instructions.md`
- 任务完成门禁：`@.github/instructions/test-driven.instructions.md`
- 版权合规：`@.github/instructions/compliance.instructions.md`
