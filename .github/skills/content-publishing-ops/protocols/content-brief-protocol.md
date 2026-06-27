# 内容简案协议 (Content Brief Protocol)

## 1. Brief 字段

| 字段 (Field) | 是否必需 (Required) | 说明 |
| ------- | ---------- | ------ |
| Source | Yes | 原始 Markdown / 文章 / 教程 / 宣发稿路径或用户输入 |
| Audience | Yes | 目标读者 / 用户群 |
| Goal | Yes | 认知、转化、公告、教程、召回、品牌建设 |
| Target platforms | Yes | 公众号 / 小红书 / 微博 / 博客 / 其他 |
| Voice boundary | Yes | 语气、禁用词、品牌口径 |
| Rights boundary | Conditional | 图片、字体、第三方素材、引用来源 |
| Publish status | Yes | draft / preview / approval pending / published |

## 2. 简案规则

| 规则 ID (Rule ID) | 检查项 | PASS 标准 | FAIL 信号 | 目标路由 (Route) |
| --------- | -------- | ----------- | ----------- | ------- |
| CB-R1 | 内容源清晰度 (Source clarity) | 内容源可定位或用户原文完整 | 只有模糊主题 | writing-fragments / writing-shape |
| CB-R2 | 目标受众 (Audience) | 受众明确 | 面向“所有人”且无平台差异 | 询问用户或草拟假设 (ask user or draft assumption) |
| CB-R3 | 发布平台目标 (Platform target) | 每个平台目标明确 | 未说明发布到哪里 | `CONTENT_SOURCE_MISSING` |
| CB-R4 | 宣传口径边界 (Claims boundary) | 宣称可由事实源支持 | 夸大产品能力 | `/release-deploy` / 文档同步 (docs sync) |
| CB-R5 | 版权权利边界 (Rights boundary) | 第三方素材 / 引用来源清楚 | 素材来源不明 | `/authorship-copyright-readiness` |

## 3. Brief 模板

```markdown
## 宣发媒体内容策划简案 (Content Brief)

## 宣发事实源 (Source)

- <源文件路径或粘贴的内容源>

## 目标受众 (Audience)

- <具体受众>

## 发布目的 (Goal)

- <为什么发布>

## 目标发布平台矩阵 (Target Platforms)
|  | 发布平台 (Platform) | 该平台发布目的 (Goal) | 平台硬性合规约束 (Constraints) |  |
|  | ---------- | ------ | ------------- |  |
|  | <platform> | <goal> | <constraints> |  |

## 品牌调性与负面免责边界 (Voice Boundary)

- 语气调性 (Tone):
- 禁止宣称的空话口径 (Forbidden claims):
- 必需附加的免责声明 (Required disclaimers):

## 权利链保护边界 (Rights Boundary)

- 第三方素材/引用来源 (Third-party assets):
- 引用出处声明需求 (Citation needs):
- 需要审批项 (Approval required):

```

## 4. 判定

| 条件 | 状态 (State) |
| ------ | ------- |
| Brief 字段齐 | `/content-publishing-ops:CONTENT_SCOPE_DEFINED` |
| 内容源或平台缺失 | `/content-publishing-ops:CONTENT_SOURCE_MISSING` |
| 权利链不清 | `/authorship-copyright-readiness` |
