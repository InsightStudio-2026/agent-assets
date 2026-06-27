# 作者权属链协议 (Authorship Chain Protocol)

## 1. 主体一致性检查

| 规则 ID (Rule ID) | 检查项 | PASS 标准 | FAIL 信号 | 处理 |
| --------- | -------- | ----------- | ----------- | ------ |
| ACP-R1 | Product name | README / About / release notes / 申请材料产品名一致 | 同一产品多名并存 | `WAITING_RIGHTS_CONFIRMATION` |
| ACP-R2 | Version | README / About / installer / package / 申请材料版本一致 | version 漂移 | Phase 4 修正 |
| ACP-R3 | Author | 作者字段与项目 SSOT 或用户确认一致 | 作者名混用或缺失 | `WAITING_RIGHTS_CONFIRMATION` |
| ACP-R4 | Copyright holder | 著作权人 / 登记主体一致 | LICENSE / About / 材料主体冲突 | `WAITING_RIGHTS_CONFIRMATION` |
| ACP-R5 | LICENSE / NOTICE | license 文本、copyright notice 与主体一致 | 复制第三方 notice 未改或误删 | `/security-privacy-audit` if legal risk |
| ACP-R6 | About page | 关于页主体、版本、license、第三方声明与材料一致 | 关于页遗漏权利信息 | Phase 4 修正 |
| ACP-R7 | Source headers | 源码文件头只放必要版权主体，不扩散敏感登记信息 | 大量无必要头或主体冲突 | direct cleanup |

## 2. 默认主体口径

| 字段 (Field) | 默认值 (无项目 SSOT 覆盖时) (Default if no project SSOT override) |
| ------- | ------------------------------------- |
| Author | 详见 [compliance.instructions.md](../../instructions/compliance.instructions.md) 的"自然人作者" |
| Copyright holder | 同上，见“著作权人 / 登记主体” |
| Unified social credit code | 仅在 LICENSE / NOTICE / LEGAL / 软著材料等需要处使用；源码文件头不扩散 |

## 3. Authorship Chain 表

| 交付产物 (Artifact) | 产品名称 (Product) | 版本 (Version) | 作者 (Author) | 著作权人 (Rights Holder) | 事实依据 (Evidence) | 判定结论 (Verdict) |
| ---------- | --------- | --------- | -------- | --------------- | ---------- | --------- |
| README | `<name>` | `<version>` | `<author>` | `<holder>` | `<path>` | PASS / FAIL |
| LICENSE | `<name>` | `<version>` | `<author>` | `<holder>` | `<path>` | PASS / FAIL |
| About page | `<name>` | `<version>` | `<author>` | `<holder>` | `<path>` | PASS / FAIL |
| Application materials | `<name>` | `<version>` | `<author>` | `<holder>` | `<path>` | PASS / FAIL |

## 4. 判定

| 条件 | 状态 (State) |
| ------ | ------- |
| 主体、版本、材料一致 | `/authorship-copyright-readiness:READINESS_SCOPE_DEFINED` 可继续 |
| 任一主体冲突 | `/authorship-copyright-readiness:AUTHORSHIP_CHAIN_INCOMPLETE` |
| 需用户确认权利主体 | `/authorship-copyright-readiness:WAITING_RIGHTS_CONFIRMATION` |
