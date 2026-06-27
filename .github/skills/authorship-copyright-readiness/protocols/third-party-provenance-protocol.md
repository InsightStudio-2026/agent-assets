# 第三方来源合规协议 (Third-Party Provenance Protocol)

## 1. 来源类别

| 规则 ID (Rule ID) | 来源类型 (Source Type) | 例 (Example) | 必需证据 (Required Evidence) | 风险路由 (Risk Route) |
| --------- | ------------- | ---- | ---------- | ---------- |
| TPP-1 | dependency | npm / PyPI / cargo / system package | lockfile 与 license 摘要 (lockfile + license summary) | `/security-privacy-audit` 若高风险 (if risky) |
| TPP-2 | code snippet | 拷贝的代码片段 / 适配的算法 (copied snippet / adapted algorithm) | 源 URL / license / 修改说明 (source URL / license / adaptation note) | 用户/法务确认 (user/legal confirmation) |
| TPP-3 | asset | 图标 / 图片 / 字体 / 音频 / 模型 (icon / image / font / audio / model) | 源 URL / license / 使用条款 (source URL / license / usage terms) | 用户/法务确认 (user/legal confirmation) |
| TPP-4 | template | 起始模板 / 脚手架 / UI 套件 (starter / boilerplate / UI kit) | 源仓库 / license / 保留的声明 (source repo / license / retained notice) | `/security-privacy-audit` 若不明确 (if unclear) |
| TPP-5 | agent asset | 外部工作流 / 技能 / 提示词 (external workflow / skill / prompt) | 出处 / license / 隔离记录 (provenance / license / quarantine record) | `/asset-quality-gates` |
| TPP-6 | AI-generated material | 生成的文案 / 图片 / 代码 (generated copy / image / code) | 若要求提供提示词出处 + 人工筛选证据 (prompt provenance if required + human selection evidence) | 披露边界核查 (disclosure boundary review) |

## 2. Provenance 规则

| 规则 ID (Rule ID) | 检查项 | PASS 标准 | FAIL 信号 |
| --------- | -------- | ----------- | ----------- |
| TPP-R1 | Source URL | 每个非原创素材 / 代码来源可追溯 | “网上找的” |
| TPP-R2 | License | license 类型、版本、保留义务明确 | license unknown |
| TPP-R3 | Notice preservation | 必须保留的 NOTICE / copyright 未删除 | 第三方声明被清空 |
| TPP-R4 | Compatibility | license 与发布 / 登记目标不明显冲突 | copyleft / no-commercial 未评估 |
| TPP-R5 | Asset rights | 字体、图标、图片、音频有商用 / 分发许可 | 素材来源不明 |
| TPP-R6 | External agent intake | 外部 agent 资产先 quarantine + asset-quality-gates | 直接启用外部资产 |

## 3. Third-Party Provenance 表

| 引入项 (Item) | 引入类型 (Type) | 来源 (Source) | 许可证 (License) | 必需声明 (Required Notice) | 包含于产品中 (Included In Product) | 判定结论 (Verdict) |
| ------ | ------ | -------- | --------- | ----------------- | --------------------- | --------- |
| `<name>` | dependency / snippet / asset / template / agent | `<url/path>` | `<license>` | Yes / No | Yes / No | PASS / FAIL |

## 4. 判定

| 条件 | 状态与路由 (State / Route) |
| ------ | --------------- |
| 所有来源、license、notice 齐 | `/authorship-copyright-readiness:READINESS_SCOPE_DEFINED` 可继续 |
| license unknown / incompatible | `/authorship-copyright-readiness:THIRD_PARTY_PROVENANCE_INCOMPLETE` |
| 安全 / 供应链风险 | `/security-privacy-audit` |
| 外部 agent 资产风险 | `/asset-quality-gates` |
| 法律解释不确定 | `WAITING_RIGHTS_CONFIRMATION` |
