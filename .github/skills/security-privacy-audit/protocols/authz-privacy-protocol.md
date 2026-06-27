# 权限、隐私与密钥协议 (Authz / Privacy / Secrets Protocol) · /security-privacy-audit

> **本文是 `/security-privacy-audit` workflow 的 authz matrix / PII flow / secrets handling 规范字典**。所有 R-AZP-* 规则在此定义；入口 workflow 与 `security-checks-catalog.md` 按 ID 引用，不重复事实。
> 本文档自身遵循结构化规则表 + ID 体系格式规范（入口骨架 + 支撑文档分离 + 零 ASCII 流程图）。

---

## 0. 定位与索引

### 0.1 文档定位

- authz / PII / secrets 三类核心证据的字段规范；与 `security-privacy-audit` SKILL.md DoD 项零漂移。
- 不是工具教程；不绑定特定权限引擎（OPA / Casbin / 自研）；只规定矩阵字段、PII 字段、secrets 处置必须满足的语义。
- 三大命名空间：R-AZP-AUTHZ-*权限矩阵；R-AZP-PRIVACY-* PII 流向；R-AZP-SECRETS-* 密钥处置。

### 0.2 ID 命名空间

- `R-AZP-AUTHZ-1~6`：authz matrix 字段规范。
- `R-AZP-PRIVACY-1~7`：PII flow 字段规范。
- `R-AZP-SECRETS-1~8`：secrets handling 规范。

---

## 1. Authz Matrix（R-AZP-AUTHZ-*）

`authz-matrix.md` 必填字段；缺任一字段 = R-CHK 失败。

| 规则 ID (Rule ID) | 字段 | 必填 | 范例 | 缺失后果 |
| --------- | ------ | ------ | ------ | --------- |
| `R-AZP-AUTHZ-1` | Resource | 必填 | `User.Profile`、`Order`、`Admin.Console`、`File.Upload` | 矩阵不可读 → `MITIGATION_REQUIRED` |
| `R-AZP-AUTHZ-2` | Operation | 必填 | `Create`、`Read`、`Update`、`Delete`、`Approve`、`Export`、`Impersonate` | 同上 |
| `R-AZP-AUTHZ-3` | Role / Subject | 必填 | `Anonymous`、`User`、`PaidUser`、`Admin`、`SystemService`、`Auditor` | 同上 |
| `R-AZP-AUTHZ-4` | Tenant Boundary | 必填（多租户系统） | `OwnTenantOnly` / `CrossTenantWithAudit` / `Global` | 跨租户越权风险 → `SECURITY_BLOCKED` |
| `R-AZP-AUTHZ-5` | Default Decision | 必填 | `deny-by-default`（任何 cell 未填默认 deny） | 不允许 default-allow → 直接 `SECURITY_BLOCKED` |
| `R-AZP-AUTHZ-6` | Audit Trail Required | 必填（敏感 op） | `Yes / No`；Approve / Delete / Export / Impersonate 必 Yes | 缺审计 → `MITIGATION_REQUIRED` |

### 1.1 Authz Matrix 模板

```markdown
|  | 资源 (Resource) | 操作行为 (Operation) | 匿名用户 (Anonymous) | 普通用户 (User) | 付费会员 (PaidUser) | 管理员 (Admin) | 多租户隔离边界 (Tenant Boundary) | 审计留痕 (Audit) |  |
|  | ---------- | ----------- | ----------- | ------ | ---------- | ------- | ----------------- | ------- |  |
|  | User.Profile | Read | Deny | Self | Self | Any | OwnTenantOnly | No |  |
|  | User.Profile | Update | Deny | Self | Self | Any | OwnTenantOnly | Yes |  |
|  | Order | Create | Deny | Allow | Allow | Allow | OwnTenantOnly | Yes |  |
|  | Order | Refund | Deny | Deny | Deny | Allow | CrossTenantWithAudit | Yes |  |
|  | ... |  |  |  |  |  |  |  |  |
```

### 1.2 Authz 反模式

- ❌ 单一 `is_admin` 布尔代替矩阵
- ❌ 前端隐藏菜单代替服务端 deny
- ❌ "我们没有租户问题"（多用户系统都有隔离边界）
- ❌ 操作粒度不够细（如把 `Order.Refund` 与 `Order.Update` 合并）

---

## 2. PII Flow（R-AZP-PRIVACY-*）

`privacy-flow.md` 必填字段；每个 PII 字段必须有完整生命周期记录。

| 规则 ID (Rule ID) | 字段 | 必填 | 范例 | 缺失后果 |
| --------- | ------ | ------ | ------ | --------- |
| `R-AZP-PRIVACY-1` | PII Field Name | 必填 | `email`、`phone`、`id_card`、`address`、`payment_card`、`health_record`、`location` | 字段未识别 → `MITIGATION_REQUIRED` |
| `R-AZP-PRIVACY-2` | Sensitivity Level | 必填 | `Public` / `Internal` / `Sensitive` / `Highly Sensitive`（按当地法规分级） | 同上 |
| `R-AZP-PRIVACY-3` | Source | 必填 | `用户注册输入` / `第三方 OAuth` / `导入` / `推断` | PII 不可追溯 → `SECURITY_BLOCKED` |
| `R-AZP-PRIVACY-4` | Storage | 必填 | `主库 users 表` / `日志` / `cache` / `bundle` / `第三方 SaaS`；列存储位置 | 存储面不清 → `SECURITY_BLOCKED` |
| `R-AZP-PRIVACY-5` | Sink / Egress | 必填 | `展示给本人` / `导出 CSV` / `第三方分析 SDK` / `webhook` / `monitoring`；列流出路径 | 漏掉 sink → 隐私泄露风险 → `MITIGATION_REQUIRED` |
| `R-AZP-PRIVACY-6` | Retention Period | 必填 | `主动注销 + 30 天` / `订单完结 + 5 年（法定）` / `不保留` | 无保留期 → `MITIGATION_REQUIRED` |
| `R-AZP-PRIVACY-7` | Deletion Path | 必填 | `用户主动删除路径` / `自动清理 job` / `第三方删除 API` / `合规 erasure 接口` | 无删除路径 → `SECURITY_BLOCKED`（违反多数法规） |

### 2.1 Privacy Flow 反模式

- ❌ 把日志 / monitoring / error tracking 当"非 PII 存储"
- ❌ 第三方 SaaS（Sentry / Datadog / Mixpanel）默认采集用户 ID + email 不入 sink
- ❌ "我们不卖数据"代替明确 sink 列表
- ❌ 保留期口语化（"很短时间"、"必要时间"）

### 2.2 法规对齐

本文不替代法规细则；仅要求 PII flow 完整可审。具体合规归专项审计 + 法务确认：

- GDPR / CCPA / PIPL / 网安法 / 等保 / HIPAA / PCI-DSS 等按业务地域 + 行业适用。
- 跨境数据传输（特别是 PIPL 规则）必须在 R-AZP-PRIVACY-5 sink 字段明示。

---

## 3. Secrets Handling（R-AZP-SECRETS-*）

| 规则 ID (Rule ID) | 规则 | 触发范围 | 严重性 |
| --------- | ------ | --------- | -------- |
| `R-AZP-SECRETS-1` | 不硬编码 | 源码 / config 文件 / docker image / 前端 bundle / 文档 / 测试 fixture | Critical |
| `R-AZP-SECRETS-2` | 不进日志 | application log / error tracking / monitoring / debug print；生产环境强制脱敏 | Critical |
| `R-AZP-SECRETS-3` | 不进前端 bundle | service-side only；前端只持 short-lived OAuth token；不允许 API key 暴露给浏览器 | Critical |
| `R-AZP-SECRETS-4` | 不进 git 历史 | 含撤销分支 / amend / rebase 后的历史；secrets archaeology 全量扫 | Critical |
| `R-AZP-SECRETS-5` | 轮换策略 | 静态 secrets ≤ 90 天；token / refresh token / OAuth client secret 按风险定期；变更必走 `HG-IRREV-004` | High |
| `R-AZP-SECRETS-6` | 跨环境隔离 | dev / staging / prod 不共享 secrets；不允许 prod secrets 落地开发者机器 | Critical |
| `R-AZP-SECRETS-7` | CI/CD 隔离 | secrets 注入仅限明确 job；不跨 job / 跨 PR 共享；不读取不可信 PR 上下文 | Critical |
| `R-AZP-SECRETS-8` | 暴露后处置 | 发现暴露 → 立即轮换 + 撤销 + audit log review + 影响面评估；不接受"风险接受"替代 | Critical |

### 3.1 Secrets 反模式

- ❌ `.env.example` 写真实测试 token
- ❌ Dockerfile `ENV API_KEY=...` 默认值
- ❌ 前端 `process.env.STRIPE_SECRET_KEY`（应该是 publishable key）
- ❌ commit 后 force-push 删除（git 历史仍能恢复；必须先轮换）
- ❌ Slack / 飞书 / 微信传 secrets

---

## 4. 检查执行顺序

| Phase | 顺序 | 备注 |
| ------- | ------ | ------ |
| Phase 3 Authz Matrix | 先做完 R-AZP-AUTHZ-* 矩阵填表，再分析越权风险 | 矩阵不全不进入下一 Phase |
| Phase 4 Privacy Flow | 先按 R-AZP-PRIVACY-1~7 字段填表，再分析 sink / retention / deletion 缺口 | 缺字段 → 直接 `MITIGATION_REQUIRED` |
| Phase 5 Secrets Handling | 先 R-AZP-SECRETS-2~4 静态扫描，再 R-AZP-SECRETS-1 / 5-7 配置审查；R-AZP-SECRETS-8 仅当发现暴露才执行 | secrets archaeology 必跑 |

---

## 5. 边界与不替代

| 类别 | 是否在本文 | 委托对象 |
| ------ | ----------- | --------- |
| 法规细则（GDPR / PIPL / HIPAA 等） | 不替代 | 专项审计 + 法务 |
| 业务规则正确性 | 不检查 | `review` skill / 业务测试 |
| 加密算法选择 | 部分（R-SEC-AUTH-13 密码哈希） | 主归专项 cryptographic review |
| KMS / HSM / vault 选型 | 不规定 | 架构决定 |

---

## 6. 修订规则

- 本文修订必须同 PR 修订 `security-privacy-audit.md` Phase 3-5 骨架。
- R-AZP-* ID 一旦分配不得复用；废弃改 deprecated。
- §3 Secrets Handling 任何放宽必须先在 `security-privacy-audit` SKILL.md §0.1 同步并经用户裁决；R-AZP-SECRETS-8 暴露后处置不允许放宽。
- §2 法规对齐章节随业务地域扩展更新；不另起术语，引用专项审计 SSOT。
