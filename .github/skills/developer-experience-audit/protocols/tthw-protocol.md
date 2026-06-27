# TTHW 首次上手协议 (TTHW Protocol)

## 1. 定义

TTHW = Time To Hello World。这里不是人类教程时间承诺，而是可复检的首次跑通摩擦指标。

| 标识 ID (ID) | 术语 | 定义 |
| ---- | ------ | ------ |
| TTHW-1 | Entry Located | 新 agent / 新开发者能定位 README、AGENTS 或等价入口 |
| TTHW-2 | Dependencies Installed | 依赖安装命令真实且可在目标 OS 表达 |
| TTHW-3 | Config Prepared | 示例 env / secrets 边界清楚，不要求真实密钥误入仓库 |
| TTHW-4 | First Run | 第一个页面、API、CLI 或测试可运行 |
| TTHW-5 | First Failure Recovery | 常见失败有定位路径或下一步 workflow |

## 2. 审计规则

| 规则 ID (Rule ID) | 检查项 | PASS 标准 | FAIL 信号 | 路由 |
| --------- | -------- | ----------- | ----------- | ------ |
| TTHW-R1 | 入口真实性 | README / AGENTS / package scripts 指向一致 | 命令散落且无权威入口 | direct docs fix |
| TTHW-R2 | 命令真实性 | 命令可复制；Windows / PowerShell 无 `&&`；写文件命令显式 UTF-8 | shell 方言混用、编码风险 | `/repo-safety-setup` |
| TTHW-R3 | 依赖边界 | 依赖管理文件与命令一致 | README 写 pnpm 但无 lock / package 管理依据 | direct docs fix |
| TTHW-R4 | 环境变量 | `.env.example` 或文档说明 secret 来源与不可提交边界 | 要求真实密钥但无安全说明 | `/security-privacy-audit` |
| TTHW-R5 | 首次成功 | 有明确 first run / first test / health check | “启动项目”无成功判据 | `/repo-safety-setup` |
| TTHW-R6 | 失败自救 | 常见错误指向 troubleshooting、cross-cutting §6 或 workflow | 报错后无下一步 | direct docs fix |

## 3. 测量表

| 阶段 (Step) | 命令/操作 (Command / Action) | 预期结果 (Expected Result) | 事实依据 (Evidence) | 时间预算 (Time Budget) | 判定结论 (Verdict) |
| ------ | ------------------ | ----------------- | ---------- | ------------- | --------- |
| Entry | `<path>` | 找到入口 | `<file>` | N/A | PASS / FAIL |
| Install | `<command>` | 依赖安装完成 | <output or N/A> | `<minutes>` | PASS / FAIL |
| Config | `<action>` | 示例配置可准备 | `<file>` | `<minutes>` | PASS / FAIL |
| First Run | `<command>` | 页面 / API / 测试通过 | `<output>` | `<minutes>` | PASS / FAIL |
| Recovery | `<failure>` | 能找到自救路径 | `<path>` | N/A | PASS / FAIL |

## 4. 判定

| 条件 | 状态 (State) |
| ------ | ------- |
| 所有 TTHW-R* PASS | `/developer-experience-audit:TTHW_MEASURED` |
| 任一命令失真但可文档修复 | `/developer-experience-audit:DX_BLOCKED` |
| 涉本地安全链缺失 | 路由 `/repo-safety-setup` |
| 涉密钥 / PII / 外部凭据 | 路由 `/security-privacy-audit` |
