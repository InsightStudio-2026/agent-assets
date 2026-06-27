---
name: mcp-builder
description: 设计和实现 MCP server，包括工具边界、输入输出 schema、鉴权、错误处理、测试、注册与安全审计。Use when building MCP servers, integrating external APIs as tools, designing Model Context Protocol services, or says MCP server / MCP 工具 / 外部 API 工具化。
---

# MCP Builder

## 1. 定位

MCP Builder 用于把外部服务、数据库、内部脚本或 API 设计成可被 agent 安全调用的 MCP server。它不替代 `/security-privacy-audit` 的权限 / secrets 审计，不替代 `/specs-write` 的复杂功能合同，也不复制外部 `mcp-builder` 实现。

## 2. 触发与分流

| Rule ID | 条件 | 动作 | 分流 |
| --------- | ------ | ------ | ------ |
| MCP-R1 | 用户要创建 MCP server 或 MCP tool | 启动 MCP 设计流程 | 本 skill |
| MCP-R2 | 涉 PII、secrets、生产权限、写操作 | 加安全 gate | `/security-privacy-audit` |
| MCP-R3 | MCP 是较大产品功能一部分 | 先写 spec | `/specs-write` |
| MCP-R4 | 只是普通 API client 代码 | 直接实现或 `tdd` | direct / `tdd` |
| MCP-R5 | 需要部署 / 发布 MCP 服务 | 发布 gate | `/release-deploy` |

## 3. MCP Tool 设计表

| 字段 (Field) | 是否必需 (Required) | 说明 |
| ------- | ---------- | ------ |
| Tool name | Yes | 动词 + 领域对象，稳定、明确 |
| Purpose | Yes | 工具解决什么任务 |
| Inputs schema | Yes | JSON schema / typed object；不得接收任意字符串执行 |
| Outputs schema | Yes | 成功与失败结构 |
| Side effects | Yes | read-only / write / external notification / data mutation |
| Auth boundary | Yes | API key / OAuth / local token；不得硬编码 |
| Rate limits | Conditional | 外部 API 限制 |
| Error model | Yes | 可恢复 / 不可恢复 / 用户需介入 |
| Tests | Yes | schema、happy path、failure path |

## 4. 工具边界规则

| Rule ID | 规则 | 禁止 |
| --------- | ------ | ------ |
| MCP-G1 | 每个 tool 做一个清晰动作 | 万能 `execute` / `run_query` 无约束入口 |
| MCP-G2 | 输入必须结构化 | 接收 shell / SQL / eval 字符串直通 |
| MCP-G3 | 输出必须可机读 | 只返回散文文本 |
| MCP-G4 | secrets 只从环境变量或 secret store 读取 | 写入源码、README、fixture |
| MCP-G5 | 写操作必须显式命名并声明副作用 | 把 mutation 藏在 read tool |
| MCP-G6 | 错误要带可行动信息 | 吞错或返回 vague failure |

## 5. 安全检查

| 检查项 (Check) | 合格标准 (PASS 标准) | 路由 (Route) |
| ------- | ----------- | ------- |
| Secrets | 无硬编码 key / token / cookie | `/security-privacy-audit` |
| Permission | 最小权限、scope 可解释 | `/security-privacy-audit` |
| Data exposure | 输出不泄露 PII / secrets | `/security-privacy-audit` |
| Write actions | 有确认边界、幂等或回滚说明 | `/specs-write` / `/release-deploy` |
| Logging | 不记录敏感输入输出 | `/observability-incident` |

## 6. MCP 设计信息包 (MCP Design Packet)

```markdown
## MCP 设计信息包 (MCP Design Packet)

## 服务目的 (Server Purpose)

- <purpose>

## 工具列表 (Tools)
|  | 工具名称 (Tool) | 副作用 (Side Effect) | 输入 Schema (Inputs) | 输出 Schema (Outputs) | 鉴权 (Auth) |  |
|  | ------ | ------------- | -------- | --------- | ------ |  |
|  | <tool> | 只读/写入 (read-only / write) | <schema> | <schema> | <auth> |  |

## 安全边界 (Security Boundary)

- 凭证/密钥 (Secrets):
- 权限范围 (Permissions):
- 数据泄露防护 (Data exposure):
- 频次限制 (Rate limits):

## 测试用例 (Tests)
|  | 测试项 (Test) | 预期结果 (Expected) |  |
|  | ------ | ---------- |  |
|  | Schema 校验 (schema validation) | <expected> |  |
|  | 正常路径 (happy path) | <expected> |  |
|  | 异常路径 (failure path) | <expected> |  |
```

## 7. 禁止项

| 禁止项 | 原因 |
| -------- | ------ |
| 不硬编码 API key 或用户 token | secrets 安全 |
| 不创建万能执行工具 | agent 工具边界必须可审计 |
| 不把生产写操作伪装成只读查询 | 外部副作用需明确 gate |
