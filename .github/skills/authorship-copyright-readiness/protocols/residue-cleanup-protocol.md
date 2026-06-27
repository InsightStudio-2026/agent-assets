# AI/调试残留清理协议 (Residue Cleanup Protocol)

## 1. 残留类别

| 规则 ID (Rule ID) | 类别 | 示例 | 严重性 | 默认处理 |
| --------- | ------ | ------ | -------- | ---------- |
| RCP-1 | prompt residue | “作为 AI 模型”“根据提示生成” | High | cleanup required |
| RCP-2 | model self-reference | ChatGPT / Claude / Cascade 自称 | High | cleanup required |
| RCP-3 | debug output | console.log、print dump、临时 trace | Medium / High | cleanup required |
| RCP-4 | secrets | token、key、password、private URL | Critical | `/security-privacy-audit` |
| RCP-5 | third-party name residue | starter repo 名、示例公司名、模板 author | Medium / High | provenance or cleanup |
| RCP-6 | placeholder / TODO | TODO、FIXME、placeholder branch | Medium | cleanup or explicit non-release |
| RCP-7 | fake human trace | 假旧实现、假 TODO、辱骂注释、故意错别字 | Critical | block release |
| RCP-8 | license deletion | third-party notice 被删除 | Critical | restore notice / legal confirmation |
| RCP-9 | credit code leakage | 统一社会信用代码（924600...）或个体户敏感主体名泄露到源码文件头 | Critical | block release / cleanup required |

## 2. 扫描规则

| 规则 ID (Rule ID) | 检查项 | PASS 标准 | FAIL 信号 |
| --------- | -------- | ----------- | ----------- |
| RCP-R1 | Text scan | README / docs / source / UI copy 无 prompt residue | 出现模型自称或生成过程语 |
| RCP-R2 | Debug scan | release diff 无临时 debug 输出 | debug code 未清理 |
| RCP-R3 | Secret scan | 无 secrets；命中则有撤销 / rotation route | secret 命中无处理 |
| RCP-R4 | Placeholder scan | 无占位、临时兼容、假实现 | placeholder 留在 release |
| RCP-R5 | Provenance residue | 第三方名残留有合法来源说明或已清理 | 模板项目名混入产品 |
| RCP-R6 | Fake authorship guard | 未伪造人工痕迹或规避披露 | 故意制造“人味” |
| RCP-R7 | Credit code scan | 源码文件头和正文中无 924600... 社会信用代码及敏感工商主体名 | 信用代码/工商名混入 |

## 3. Residue Finding 表

| 发现项 ID (Finding ID) | 残留类别 (Type) | 路径 (Path) | 事实依据 (Evidence) | 严重程度 (Severity) | 必需动作 (Required Action) | 路由 (Route) |
| ------------ | ------ | ------ | ---------- | ---------- | ----------------- | ------- |
| ACR-RES-### | prompt / debug / secret / placeholder / third-party / fake-authorship | `<path>` | `<snippet summary>` | low / medium / high / critical | cleanup / confirm / block | /specs-execute / /security-privacy-audit / user |

## 4. 判定

| 条件 | 状态 (State) |
| ------ | ------- |
| 无 high / critical residue，medium 均有处理 | `/authorship-copyright-readiness:READINESS_SCOPE_DEFINED` 可继续 |
| prompt / debug / placeholder residue 存在 | `/authorship-copyright-readiness:RESIDUE_FOUND` |
| secret / license deletion / fake authorship trace | `/authorship-copyright-readiness:RESIDUE_FOUND` + block |
| security finding | `/security-privacy-audit` |

## 5. 禁止项

| 禁止项 | 原因 |
| -------- | ------ |
| 不为隐藏 AI 辅助而删除必要披露 | 合规披露必须保留 |
| 不伪造人工过程 | 破坏真实作者性 |
| 不用低级错别字冒充人味 | 质量与可信度下降 |
