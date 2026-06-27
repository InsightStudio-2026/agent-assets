# 平台适配协议 (Platform Adaptation Protocol)

## 1. 平台适配矩阵

| 发布平台 (Platform) | 重点 | 必查项 | 输出 |
| ---------- | ------ | -------- | ------ |
| WeChat Official Account | 标题、摘要、排版、封面、引用 | 链接、图片、版权、导读 | Markdown / HTML-ready preview |
| Xiaohongshu | 标题钩子、图片卡片、标签、短段落 | 夸大宣传、敏感词、封面 brief | post copy + image brief |
| Weibo | 短文案、话题、链接、图 | 字数、链接可见性、话题边界 | short copy |
| Blog / Website | SEO title、slug、摘要、canonical link | frontmatter、引用、代码块 | publish-ready Markdown |
| Generic | 平台未知 | 保留内容结构，列缺失约束 | neutral preview |

## 2. 适配规则 (Adaptation Rules)

| 规则 ID (Rule ID) | 检查项 | PASS 标准 | FAIL 信号 |
| --------- | -------- | ----------- | ----------- |
| PA-R1 | Content fidelity | 核心事实不因平台改写而变形 | 标题党改变承诺 |
| PA-R2 | Format fit | 段落、标题、列表、代码块适配平台 | 原文硬贴导致不可读 |
| PA-R3 | Link strategy | 外链 / 引用 / CTA 在平台规则内 | 平台不支持的链接形式 |
| PA-R4 | Image brief | 封面 / 信息图 brief 明确且不伪造素材权利 | 图片来源或生成权利不清 |
| PA-R5 | Compliance | 不绕过平台敏感规则 | 暗示规避审核 |
| PA-R6 | Status honesty | preview / published 状态分明 | 预览稿冒充已发布 |

## 3. Preview Diff 表

| 发布平台 (Platform) | 变换类型 (Change Type) | 原内容小节 (Source Section) | 适配后方案 (Adapted Form) | 适配决策理由 (Reason) |
| ---------- | ------------- | ---------------- | -------------- | -------- |
| `<platform>` | title / summary / format / image / tag | `<section>` | `<adapted>` | `<reason>` |

## 4. Preview Packet

```markdown
## 多平台发布预览包 (Platform Preview)

## 发布平台 (Platform)

- <platform>

## 标题候选方案 (Title Options)

1. <候选标题 (title)>
2. <候选标题 (title)>

## 适配后正文内容 (Body)
<已适配的平台内容正文 (adapted content)>

## 多媒体/视觉配图企划 (Media Brief)

- 封面图设计 (Cover):
- 正文配图/插图 (Images):
- 无障碍替换文本 (Alt text):

## 话题与标签 (Tags / Topics)

- <tag>

## 核心行动号召 (CTA)

- <call to action>

## 适配改动说明 (Adaptation Notes)

- <改变了什么以及为什么 (what changed and why)>

```

## 5. 判定

| 条件 | 状态 (State) |
| ------ | ------- |
| 平台稿与 preview diff 齐 | `/content-publishing-ops:PLATFORM_ADAPTATION_READY` |
| 预览稿可展示但需用户确认 | `/content-publishing-ops:PREVIEW_READY` |
| 权利 / 平台规则 / 账号边界不清 | `/content-publishing-ops:PUBLISHING_BLOCKED` |
