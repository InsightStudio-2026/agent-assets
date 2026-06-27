# 宣发审批协议 (Publishing Approval Protocol)

## 1. 真实发布确认包字段

| 字段 (Field) | 是否必需 (Required) | 说明 |
| ------- | ---------- | ------ |
| Platform | Yes | 发布平台 |
| Account | Yes | 使用哪个账号 / 主体 |
| Content version | Yes | 预览稿路径、hash 或版本摘要 |
| Publish time | Yes | 立即发布 / 定时发布时间 |
| External side effect | Yes | 用户可见、通知、链接、评论区等影响 |
| Rollback / correction path | Yes | 删除、撤回、更正、补发方式 |
| Rights confirmation | Conditional | 第三方素材 / 引用 / AI 生成素材边界 |

## 2. 审批规则 (Approval Rules)

| 规则 ID (Rule ID) | 条件 | 动作 | 状态 (State) |
| --------- | ------ | ------ | ------- |
| PAP-R1 | 只有 preview，没有用户批准 | 等待批准 | `/content-publishing-ops:WAITING_PUBLISH_APPROVAL` |
| PAP-R2 | 用户批准明确包含平台、账号、内容版本、时间 | 可执行批准范围内发布 | `/content-publishing-ops:APPROVED_TO_PUBLISH` |
| PAP-R3 | 用户只说“发吧”但平台 / 账号 / 版本不明 | 追问缺项 | `/content-publishing-ops:WAITING_PUBLISH_APPROVAL` |
| PAP-R4 | 权利链或素材授权不清 | 阻塞并分流 | `/authorship-copyright-readiness` |
| PAP-R5 | 涉产品真实 release announcement 但 release 状态不清 | 阻塞并分流 | `/release-deploy` |

## 3. Approval Packet 模板

```markdown
## 宣发媒体发布审批授权单 (Publishing Approval Packet)

## 拟发布标的 (Target)

- 目标平台 (Platform):
- 发布账号 (Account):
- 发布内容版本 (Content version):
- 发布时间 (Publish time):

## 用户可见社会效应 (User-visible Effect)

- <发布后公众将能看到什么、有什么影响>

## 纠错/撤回预案 (Rollback / Correction)

- 物理删除预案 (Delete):
- 局部修订预案 (Edit):
- 更正声明预案 (Correction post):

## 需留痕审计证据 (Evidence to Capture)

- 发布 URL (URL):
- 屏幕截图 (Screenshot):
- 执行时间戳 (Timestamp):

## 授权边界说明 (Authorization Boundary)

- 已授权范围 (Authorized): <拟发布的平台 + 账号 + 版本 + 时间>
- 未授权范围 (Not authorized): <其他平台 / 未来发布计划 / 本版本以外的篡改性编辑>

```

## 4. 禁止项

| 禁止项 | 原因 |
| -------- | ------ |
| 不继承 preview 确认为 publish 确认 | 预览与发布是不同副作用 |
| 不把一次授权扩展到未来内容 | 授权只限当前 packet |
| 不用模糊批准执行真实发布 | 平台、账号、版本、时间必须明确 |
