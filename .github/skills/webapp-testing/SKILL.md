---
name: webapp-testing
description: 使用真实浏览器检查本地 Web 应用的功能、UI 行为、console 日志、截图和 Playwright 风格测试证据。Use when user asks to test a local web app, debug UI behavior in browser, capture screenshots/logs, verify frontend flows, or says Web 应用测试 / 浏览器测试 / Playwright / UI 验证。
argument-hint: "要测试哪个 URL 或功能？"
---

# Webapp Testing

## 1. 定位

Webapp Testing 用于对本地或预览环境 Web 应用做真实浏览器验证、UI 行为调试和测试证据收集。它不替代 `/release-deploy` 的发布闸口，不替代 `browser-flow-codifier` 的流程固化，也不默认执行登录、支付、发帖、删除、发布等真实副作用流程。

## 2. 触发与分流

| Rule ID | 条件 | 动作 | 分流 |
| --------- | ------ | ------ | ------ |
| WAT-R1 | 用户要求测试本地 Web app / 页面 / 组件 | 启动浏览器测试 | 本 skill |
| WAT-R2 | 用户要求把已成功流程固化为脚本 | 分流 | `browser-flow-codifier` |
| WAT-R3 | 用户要求发布前 smoke / Browser QA | 分流 | `/release-deploy` |
| WAT-R4 | 用户要求设计系统视觉 QA | 分流 | `/design-system-audit` |
| WAT-R5 | 流程包含真实副作用 | 暂停并要求确认 | 专项 workflow |

## 3. 测试输入

| Field | Required | 说明 |
| ------- | ---------- | ------ |
| Target URL | Yes | 本地或预览 URL |
| Test goal | Yes | 要验证的行为 |
| Browser / viewport | Yes | 浏览器和视口矩阵 |
| Fixtures | Conditional | 测试账号、mock 数据、seed data；不得包含 secrets |
| Expected result | Yes | 可观察断言 |
| Side effect boundary | Yes | 是否只读，是否需要 cleanup |

## 3.5 服务生命周期托管

| Rule ID | 场景 | 托管动作 | 验收与残留控制 |
| --------- | ------ | ---------- | ---------------- |
| WAT-S1 | 本地服务（如 Vue/React、Python API）尚未启动 | 必须使用自带的 [scripts/with_server.py](scripts/with_server.py) 脚本托管拉起，禁止使用 `&` 等后台挂起命令 | 进程运行完成后，必须在 `finally` 块或脚本终结时，确保端口与子进程全部安全回收 |
| WAT-S2 | Windows 11 宿主下 npm/node 产生进程树 | [scripts/with_server.py](scripts/with_server.py) 必须在 Windows 下支持 `taskkill /F /T` 树级物理毁灭 | 验证 5173、3000 等测试端口在退出后未被任何孤儿 node 进程死锁残留 |
| WAT-S3 | 需多端并发测试（如前端 + 后端双端口运行） | 使用 `--server` 重复参数，为各端指定不同端口，等待所有端口就绪后执行 Playwright 自动化 | 主测试进程完成退出后，各端服务一并级联停止 |

## 4. 测试矩阵

| Check | PASS 标准 | Evidence |
| ------- | ----------- | ---------- |
| Navigation | 页面可加载，无错误路由 | URL + screenshot |
| Console | 无阻塞性 console error | console log excerpt |
| UI behavior | 关键交互符合预期 | step result |
| Network / API | 关键请求成功或失败状态被处理 | status / error evidence |
| Responsive | 目标 viewport 布局可用 | screenshots |
| Accessibility smoke | 可聚焦、基础语义、明显对比问题 | notes |
| State coverage | loading / empty / error / success 至少关键路径覆盖 | screenshots / assertions |

## 5. 报告模板 (Report Template)

```markdown
## Webapp 测试报告 (Webapp Testing Report)

## 测试范围 (Scope)

- 目标 URL (Target URL):
- 浏览器与视口 (Browser / viewport):
- 是否只读 (Read-only): yes / no

## 测试步骤 (Steps)
|  | 步骤 (Step) | 操作 (Action) | 预期结果 (Expected) | 实际结果 (Actual) | 结论 (Verdict) |  |
|  | ------ | -------- | ---------- | -------- | --------- |  |

## 测试证据 (Evidence)
|  | 证据类型 (Type) | 路径/摘录 (Path / Excerpt) | 备注 (Notes) |  |
|  | ------ | ---------------- | ------- |  |
|  | 屏幕截图 (screenshot) | <path> | <notes> |  |
|  | 控制台日志 (console) | <excerpt> | <notes> |  |
|  | 网络请求 (network) | <excerpt> | <notes> |  |

## 最终结论 (Verdict)

- 通过/失败/受阻/未运行 (PASS / FAIL / BLOCKED / NOT RUN)

## 下一步路由 (Next Route)

- <diagnose | browser-flow-codifier | /release-deploy | /design-system-audit>

```

## 6. 禁止项

| 禁止项 | 原因 |
| -------- | ------ |
| 不把手工浏览器验证冒充自动测试通过 | 必须区分 manual evidence 与 automated test |
| 不保存 cookies / tokens / secrets | 安全边界 |
| 不执行未授权真实副作用 | 外部副作用需要用户确认 |
| 不从失败探索直接生成稳定脚本 | 固化归 `browser-flow-codifier` 且需成功路径 |
| 不使用深层脆弱的 CSS/XPath 选择器 | 必须优先使用 Playwright `getByRole()` / `getByText()` / `getByLabel()` 等 A11y 语义选择器定位元素，提升测试稳定性 |
