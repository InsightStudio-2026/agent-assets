# 签名、公证与更新协议 (Signing / Notarization / Update Protocol)

## 1. 签名与更新范围

| 规则 ID (Rule ID) | 范围 | 命中条件 | 强控门禁 (Gate) |
| --------- | ------ | ---------- | ------ |
| SUP-1 | code signing | 使用 Windows / macOS / Linux package signing certificate | `HG-RELEASE-*` + `HG-IRREV-002` |
| SUP-2 | notarization | macOS notarization / stapling / Gatekeeper 相关 | `HG-RELEASE-*` + `HG-IRREV-003` |
| SUP-3 | app store submit | Microsoft Store / Mac App Store / third-party store | `HG-RELEASE-*` + `HG-IRREV-003` |
| SUP-4 | auto-update feed | update manifest / feed URL / delta update | `HG-RELEASE-*` |
| SUP-5 | channel switch | dev / beta / stable / staged rollout cohort | `HG-RELEASE-*` |

## 2. Signing 规则

| 规则 ID (Rule ID) | 检查项 | PASS 标准 | FAIL 信号 |
| --------- | -------- | ----------- | ----------- |
| SUP-R1 | Certificate scope | certificate owner、expiry、platform、用途明确 | 证书来源 / 过期未知 |
| SUP-R2 | Secret handling | signing key 不落源码 / 日志 / artifacts | key path / password 泄露 |
| SUP-R3 | Signed artifact hash | 签名前后 artifact hash 与签名结果记录 | 无法追踪实际签名文件 |
| SUP-R4 | Verification command | `signtool verify` / `codesign --verify` / 等价命令有输出 | 只相信 build tool success |
| SUP-R5 | Revocation / rollback | 误签或恶意 artifact 有撤回 / 下架路径 | 无撤回策略 |

## 3. Notarization / Store 规则

| 规则 ID (Rule ID) | 检查项 | PASS 标准 | FAIL 信号 |
| --------- | -------- | ----------- | ----------- |
| SUP-R6 | Notarization result | request id、result、staple 状态记录 | 只上传无结果 |
| SUP-R7 | Entitlements | sandbox / permission / file access 与 spec 对齐 | entitlement 扩大但无安全审计 |
| SUP-R8 | Store metadata | version、release notes、privacy、permissions 一致 | store 文案与实际权限不一致 |
| SUP-R9 | Review rollback | 被拒 / 紧急下架 / 回滚路径清楚 | 被拒后无 plan |

## 4. Auto-update 规则

| 规则 ID (Rule ID) | 检查项 | PASS 标准 | FAIL 信号 |
| --------- | -------- | ----------- | ----------- |
| SUP-R10 | Feed identity | feed URL、channel、version、artifact hash 明确 | update feed 指向浮动 latest |
| SUP-R11 | Staged rollout | cohort、比例、扩量条件、停止条件明确 | 直接全量推送无监控 |
| SUP-R12 | Rollback feed | 能阻止继续升级或回指安全版本 | 更新事故无法停止 |
| SUP-R13 | Compatibility | 新旧版本 data / config / protocol 兼容 | 升级后旧版本不可读数据且无恢复 |
| SUP-R14 | User-visible consent | 用户可见推送、强制更新、channel 切换有授权 | 未授权影响真实用户设备 |

## 5. Approval Packet 字段

| 字段 (Field) | 是否必需 (Required) |
| ------- | ---------- |
| Target platform / channel | Yes |
| Artifact path + hash | Yes |
| Signing command / notarization request | Yes if applicable |
| Update feed URL / rollout cohort | Yes if applicable |
| Rollback / delist / stop-update plan | Yes |
| User approval quote | Yes before real action |

## 6. 判定

| 条件 | 状态 (State) |
| ------ | ------- |
| signing / notarization / update evidence 全齐，真实动作未执行 | `/desktop-release:WAITING_DESKTOP_RELEASE_APPROVAL` |
| 用户批准后证据齐且动作完成 | `/desktop-release:DESKTOP_RELEASE_GATE_READY` |
| 证书、secret、权限风险未闭环 | `/security-privacy-audit` 或 `/desktop-release:SIGNING_GATE_PENDING` |
| update channel 无 rollback feed | `/desktop-release:UPDATE_CHANNEL_PENDING` |
