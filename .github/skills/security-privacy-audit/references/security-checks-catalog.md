# Security Checks Catalog · /security-privacy-audit 安全检查项规则字典

> **本文是 `/security-privacy-audit` workflow 的安全 / 隐私 / 攻击面 / 滥用场景检查项事实源**。所有 R-SEC-* 规则在此定义；入口 workflow 按 ID 引用，不重复事实。
> 本文档自身遵循结构化规则表 + ID 体系格式规范（入口骨架 + 支撑文档分离 + 零 ASCII 流程图）。

---

## 0. 定位与索引

### 0.1 文档定位

- 安全检查项规则字典；与 `security-privacy-audit` SKILL.md 最低检查面 + 基础设施安全面 + 滥用场景项零漂移。
- 不是工具教程；不绑定特定扫描器（Snyk / Dependabot / OSV / TruffleHog）；只规定每类检查必须满足的语义。
- 三大命名空间：R-SEC-AUTH-*应用层；R-SEC-INFRA-* 基础设施层；R-SEC-ABUSE-* 滥用场景。

### 0.2 ID 命名空间

- `R-SEC-AUTH-1~13`：最低检查面（应用层 13 项）。
- `R-SEC-INFRA-1~13`：基础设施安全面（13 项）。
- `R-SEC-ABUSE-1~5`：滥用场景（5 项）。
- 严重性分级：Critical / High / Medium / Low；Critical / High 默认 `MITIGATION_REQUIRED`，不允许 `WAITING_RISK_ACCEPTANCE`。

---

## 1. 最低检查面 — 应用层（R-SEC-AUTH-*）

| 规则 ID (Rule ID) | 检查项 | 检查动作 | 默认严重性 | 失败动作 |
| --------- | -------- | --------- | ----------- | --------- |
| `R-SEC-AUTH-1` | 登录 | 密码强度 / 失败计数 / 锁定 / 重放 / brute-force 防护 | High | `MITIGATION_REQUIRED` |
| `R-SEC-AUTH-2` | 会话 | session token 熵 / HttpOnly / Secure / SameSite / 失效 / 同步登出 | High | `MITIGATION_REQUIRED` |
| `R-SEC-AUTH-3` | refresh token | 轮换 / 撤销 / 跨设备隔离 / 滥用检测 | High | `MITIGATION_REQUIRED` |
| `R-SEC-AUTH-4` | OAuth | redirect_uri 白名单 / state 防 CSRF / scope 最小化 / token 存储 | High | `MITIGATION_REQUIRED` |
| `R-SEC-AUTH-5` | MFA | 强制条件 / 备用代码 / 设备信任 / 跳过路径审计 | High | `MITIGATION_REQUIRED` |
| `R-SEC-AUTH-6` | 账号恢复 | 邮箱 / 手机验证强度 / 知识题 / 客服路径 / 滥用 | High | `MITIGATION_REQUIRED` |
| `R-SEC-AUTH-7` | 角色 / 资源 / 操作 / 租户隔离 | authz matrix 完整；deny-by-default；越权检测 | Critical | `SECURITY_BLOCKED` 起步 |
| `R-SEC-AUTH-8` | PII 生命周期 | 采集 / 存储 / 展示 / 导出 / 删除 / 保留期；详 `authz-privacy-protocol.md` | Critical | `SECURITY_BLOCKED` 起步 |
| `R-SEC-AUTH-9` | 密钥与日志脱敏 | secrets / token / PII / 信用卡 / 健康信息不进日志 / error message / 监控数据 | Critical | `SECRET_HANDLING_BLOCKED` |
| `R-SEC-AUTH-10` | 输入验证（多向量） | 文件上传 / 富文本 / URL / SQL / 命令执行 / 模板注入 / SSRF / XXE / Deserialization | Critical | `MITIGATION_REQUIRED` |
| `R-SEC-AUTH-11` | 审计日志 | 谁 / 何时 / 何资源 / 何操作 / 结果 / 来源 IP / user-agent；不可篡改 / 保留期 | High | `MITIGATION_REQUIRED` |
| `R-SEC-AUTH-12` | 错误信息泄露 | 不暴露 stack trace / 数据库结构 / 内部路径 / 版本号 / 用户存在性 | Medium | `MITIGATION_REQUIRED` |
| `R-SEC-AUTH-13` | 密码 / 凭证存储 | bcrypt / argon2 / scrypt + per-user salt；不允许 MD5 / SHA1 / 明文 | Critical | `SECRET_HANDLING_BLOCKED` |

---

## 2. 基础设施安全面（R-SEC-INFRA-*）

| 规则 ID (Rule ID) | 检查项 | 检查动作 | 默认严重性 | 失败动作 |
| --------- | -------- | --------- | ----------- | --------- |
| `R-SEC-INFRA-1` | Attack Surface Census | 公开 endpoint / auth boundary / admin route / webhook / background job / queue worker / WebSocket / file upload 完整盘点 | High | `MITIGATION_REQUIRED` |
| `R-SEC-INFRA-2` | Secrets Archaeology | 全量 git 历史 / 已删除分支 / commit message / issue / artifact 中 secrets 残留 | Critical | `SECRET_HANDLING_BLOCKED` + 立即轮换 |
| `R-SEC-INFRA-3` | 依赖供应链 | 直接 + 传递依赖 CVE / 已知恶意包 / typosquatting / abandoned package | High | `MITIGATION_REQUIRED` |
| `R-SEC-INFRA-4` | Install Scripts | postinstall / preinstall / pinstall script 审查；未审脚本不得执行 | High | `MITIGATION_REQUIRED` |
| `R-SEC-INFRA-5` | Abandoned Packages | 维护停止 / 单一维护者 / 关键路径 vendoring 评估 | Medium | `MITIGATION_REQUIRED` |
| `R-SEC-INFRA-6` | CI/CD Security | GitHub Actions / 自托管 runner secrets 暴露 / 跨 job 共享 | Critical | `SECRET_HANDLING_BLOCKED` |
| `R-SEC-INFRA-7` | Unpinned Actions | actions 必须 SHA pin（不允许 @v1 / @main）；third-party action 必须 SHA pin | High | `MITIGATION_REQUIRED` |
| `R-SEC-INFRA-8` | pull_request_target | 谨慎使用；不得在不可信 PR 上下文执行写入；不得读 secrets | Critical | `SECURITY_BLOCKED` 起步 |
| `R-SEC-INFRA-9` | Script Injection | workflow 中 `${{ github.event.* }}` 直接拼入 shell；issue title / branch name 注入 | Critical | `SECURITY_BLOCKED` 起步 |
| `R-SEC-INFRA-10` | CODEOWNERS | 关键路径有 owner；review required；不允许绕过 | High | `MITIGATION_REQUIRED` |
| `R-SEC-INFRA-11` | Agent Supply Chain | 引入 MCP / external skill / external workflow / external tool 时审查 provenance + license + 行为；走 `/asset-quality-gates` external intake | High | `MITIGATION_REQUIRED` |
| `R-SEC-INFRA-12` | Tool Allowlist | agent 可调用工具白名单；不允许任意 shell / network 调用 | High | `MITIGATION_REQUIRED` |
| `R-SEC-INFRA-13` | Prompt Injection Surface | 网页 / PR 评论 / 抓取内容 / 用户输入 / 第三方 API 响应进入 agent context 必须标记信任边界 | High | `MITIGATION_REQUIRED` |

---

## 3. 滥用场景（R-SEC-ABUSE-*）

| 规则 ID (Rule ID) | 场景 | 检查动作 | 默认严重性 |
| --------- | ------ | --------- | ----------- |
| `R-SEC-ABUSE-1` | 撞库 | rate limit / IP 信誉 / 失败计数 / CAPTCHA / honeypot | High |
| `R-SEC-ABUSE-2` | 刷接口 | 频次限制 / token bucket / IP + user 双维度 / cost-based throttle | Medium |
| `R-SEC-ABUSE-3` | 越权爬取 | resource enumeration 防护 / opaque ID / 带签名链接 | High |
| `R-SEC-ABUSE-4` | 付费绕过 | 价格 / 库存 / 优惠码服务端校验 / 防重放 / 防订单篡改 | Critical |
| `R-SEC-ABUSE-5` | 邀请 / 邀请码 / 推荐滥用 | 多账号检测 / 设备指纹 / 邀请码生命周期 / 反作弊 | Medium |

---

## 4. 严重性 → 失败动作映射

| 严重性 | 默认 State | 是否允许 risk acceptance | 是否允许 release 放行 |
| -------- | ----------- | -------------------------- | ---------------------- |
| Critical | `SECURITY_BLOCKED` 起步 | ❌ 不允许；必须 mitigation | ❌ |
| High | `MITIGATION_REQUIRED` | ❌ 不允许；必须 mitigation 或显式安全降级 + 用户批准 | ❌ 直接放行 |
| Medium | `MITIGATION_REQUIRED` 默认；可申请 `WAITING_RISK_ACCEPTANCE` | ✅ 用户原话裁决 + 时限 | ✅ 限期内可放行 |
| Low | `WAITING_RISK_ACCEPTANCE` 默认 | ✅ 用户原话裁决 | ✅ |

权限 / 认证 / 密钥 / PII / 生产权限五类**强制 Hard-gate**（`HG-IRREV-004`），不论严重性都不允许仅以 risk acceptance 替代用户批准。

---

## 5. 边界与不检查项

| 类别 | 是否检查 | 委托对象 |
| ------ | --------- | --------- |
| 业务逻辑漏洞 | 部分（如 R-SEC-ABUSE-4 付费绕过） | 主要归 `review` skill / 业务测试 |
| 性能 / 容量 / 可靠性 | 不检查 | `/performance-reliability-audit` |
| 数据迁移安全 | 不检查 | `/data-migration-safety` |
| 法律合规（GDPR / CCPA / 等保 / 软著） | 不替代 | 法务 + 专项审计 |
| 物理安全 / 社会工程 / 内部威胁 | 不检查 | 组织级安全 |

---

## 6. 修订规则

- 本文修订必须同 PR 修订 `security-privacy-audit.md` Phase 骨架与 §0.3 Hard-gate 表。
- R-SEC-* ID 一旦分配不得复用；废弃改 deprecated。
- 严重性 → 失败动作映射（§4）任何放宽必须先在 `security-privacy-audit` SKILL.md 同步并经用户裁决。
- 新增检查项必须先在 `security-privacy-audit` SKILL.md 最低检查面 / 基础设施安全面 / 滥用场景同步事实源。
