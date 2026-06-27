---
name: browser-flow-codifier
description: 将用户已接受的成功只读浏览器探索流程沉淀为可复用脚本、测试或操作手册，并保留 trigger、host、输入输出 schema、fixture、验证与回滚边界。Use when user asks to codify a browser flow, turn browser QA into a script, save a Playwright flow, or says 浏览器流程固化 / 录制流程 / 沉淀浏览器脚本。
---

# Browser Flow Codifier

## 1. 定位

Browser Flow Codifier 只把最近一次用户接受的成功只读浏览器流程沉淀为可测试资产。它不默认用于登录、下单、发帖、支付、删除、发布等真实副作用流程；mutating flow 必须另设确认门并路由对应 workflow。

## 2. 触发规则

| Rule ID | 前置条件 | 动作 | 下一步 |
| --------- | ---------- | ------ | -------- |
| BFC-R1 | 用户要求把成功浏览器探索固化为脚本 / 测试 | 提取最终成功路径 | 生成草案 |
| BFC-R2 | 最近流程是只读 scrape / QA / navigation | 可 codify | 写临时资产 |
| BFC-R3 | 流程包含登录、下单、发帖、支付、删除、发布、生产写入 | 不自动 codify | 等用户确认并分流专项 workflow |
| BFC-R4 | 流程尚未成功或用户未接受 | 不固化 | 先完成探索 / QA |
| BFC-R5 | selector / host / 输入输出 schema 不清 | 输出缺口 | 等补充事实源 |

## 3. 资产字段

| 字段 (Field) | 是否必需 (Required) | 说明 |
| ------- | ---------- | ------ |
| Trigger | Yes | 何时运行该 flow |
| Host / Origin | Yes | 目标 host、环境、base URL |
| Inputs | Yes | 参数、fixture、账号类型；不得包含真实 secrets |
| Outputs | Yes | 期望提取数据、截图、断言或报告 |
| Steps | Yes | 只保留最终成功路径 |
| Fixtures | Yes | 可重复运行的测试数据或 mock |
| Verification | Yes | 如何证明脚本有效 |
| Rollback / cleanup | Conditional | 若有写入倾向必须说明并确认 |

## 4. 固化信息包 (Codification Packet)

```markdown
## 浏览器流程固化信息包 (Browser Flow Codification Packet)

## 范围 (Scope)

- 流程名称 (Flow name):
- 是否只读 (Read-only): yes / no
- 目标主机 (Host):
- 触发条件 (Trigger):

## 输入与 Fixtures (Inputs / Fixtures)
|  | 输入项 (Input) | 来源 (Source) | 是否属于敏感密钥 (Secret?) |  |
|  | ------- | -------- | --------- |  |
|  | <input> | <fixture/env/user> | yes / no |  |

## 预期输出 (Expected Outputs)
|  | 输出项 (Output) | 格式 (Format) | 断言 (Assertion) |  |
|  | -------- | -------- | ----------- |  |
|  | <output> | <json/screenshot/text> | <assertion> |  |

## 最终成功步骤 (Final Successful Steps)
|  | 步骤 (Step) | 操作 (Action) | 选择器/URL (Selector / URL) | 预期结果 (Expected) |  |
|  | ------ | -------- | ---------------- | ---------- |  |
|  | 1 | <action> | <selector/url> | <expected> |  |

## 验证 (Verification)

- 验证命令 (Command):
- 预期运行结果 (Expected result):

## 边界与约束 (Boundary)

- 写入/副作用操作 (Mutating actions): none / listed
- 是否需要用户批准 (User approval required): yes / no

```

## 5. 生成规则

| Rule ID | 规则 | 禁止 |
| --------- | ------ | ------ |
| BFC-G1 | 只提取最终成功路径 | 保留失败 selector、聊天噪声、早期尝试 |
| BFC-G2 | 先写临时目录或草案 | 未验证直接进入生产测试目录 |
| BFC-G3 | 通过验证且用户批准后再进入最终位置 | 自动修改测试套件 |
| BFC-G4 | secrets 只引用环境变量名 | 写入真实 token / cookie |
| BFC-G5 | mutation 单独 gate | 把只读 scrape 与真实副作用混用 |

## 6. 路由规则

| 条件 | Route |
| ------ | ------- |
| release browser smoke | `/release-deploy` Browser QA |
| design / visual QA flow | `/design-system-audit` |
| security-sensitive browser flow | `/security-privacy-audit` |
| content publishing flow | `/content-publishing-ops` |
| flaky browser test | `/ci-quality-gates` / `diagnose` |

## 7. 禁止项

| 禁止项 | 原因 |
| -------- | ------ |
| 不从失败探索生成脚本 | 会固化错误路径 |
| 不默认处理真实副作用流程 | 需要用户批准和专项 workflow |
| 不保存 secrets / session cookies | 安全边界 |
| 不把脚本生成等同测试通过 | 必须运行验证或标 not run |
