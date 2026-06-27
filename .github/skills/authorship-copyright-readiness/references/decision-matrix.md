---
description: "作者性与版权就绪审计工作流（/authorship-copyright-readiness）专属的触发判定、状态转换路由、状态权威与动作决策矩阵"
---

# 作者性与版权就绪审计决策矩阵（/authorship-copyright-readiness）

## 0. 触发判定

| ID | 前置条件 | 动作 | 下一步 | 源 |
| ---- | ---------- | ------ | -------- | ------ |
| R-ACR-ENTRY-1 | 用户显式 `/authorship-copyright-readiness` | 启动审计 | Phase 1 | 本文件 §0 |
| R-ACR-ENTRY-2 | 准备公开发布 / 客户交付 / 应用商店提交 | 启动权利与材料一致性审计 | Phase 1 | 本文件 §0 |
| R-ACR-ENTRY-3 | 准备软著登记 / 版权材料整理 | 启动申请材料一致性审计 | Phase 1 | 本文件 §0 |
| R-ACR-ENTRY-4 | 整理 LICENSE / NOTICE / README / 关于页 | 启动主体与 license 审计 | Phase 2 | 本文件 §1 |
| R-ACR-ENTRY-5 | 内部实验 / 一次性原型 / 不对外交付草稿 | 不启用 | direct | 本文件 §4 |
| R-ACR-ENTRY-6 | 系统状态不清、下一步推进方向不明 | 停止并重定向 | 路由至 `/project-steward` | 临界状态 1 |
| R-ACR-ENTRY-7 | 缺失母本或 L1 SSOT | 停止并重定向 | 路由至 `/project-inception` | 临界状态 2 |
| R-ACR-ENTRY-8 | 属于纯缺陷根因诊断（局部、具体 bug） | 停止并重定向 | 路由至 `diagnose` 技能 | 临界状态 3 |
| R-ACR-ENTRY-9 | 属于新功能、新需求开发、大重构落地 | 停止并重定向 | 路由至 `/specs-write` 与 `/specs-execute` | 临界状态 4 |
| R-ACR-ENTRY-10 | 逻辑简单明确且适合 TDD 验证 | 停止并重定向 | 路由至 `tdd` 技能或直接执行 | 临界状态 5 |

## 0.1 状态与路由汇总 (State / Route Summary)

| 状态 (State) | 判定 | 下一步 | 路由动作 (Route Action) |
| ------- | ------ | -------- | -------------- |
| `/authorship-copyright-readiness:NOT_REQUIRED` | 内部实验或无对外交付目标 | 报告 N/A | `REPORT_AND_STOP` |
| `/authorship-copyright-readiness:READINESS_SCOPE_DEFINED` | 产品名、版本、交付目标、材料范围已明确 | Phase 2 | `CONTINUE_IN_WORKFLOW` |
| `/authorship-copyright-readiness:AUTHORSHIP_CHAIN_INCOMPLETE` | 作者 / 权利人 / LICENSE / NOTICE / 关于页主体不一致或缺事实源 | 等用户 / 法务确认 | `WAIT_FOR_USER` |
| `/authorship-copyright-readiness:THIRD_PARTY_PROVENANCE_INCOMPLETE` | 依赖、素材、代码片段、外部资产来源不清 | 补 provenance 或分流 `/security-privacy-audit` | `REPORT_AND_STOP` |
| `/authorship-copyright-readiness:RESIDUE_FOUND` | prompt 残留、模型自称、debug、secrets、第三方项目名残留 | 输出 cleanup route | `/specs-execute` 或 direct |
| `/authorship-copyright-readiness:EVIDENCE_PACKET_INCOMPLETE` | spec、截图、测试、commit、版本、权利链证据缺 | 补证据 | `REPORT_AND_STOP` |
| `/authorship-copyright-readiness:WAITING_RIGHTS_CONFIRMATION` | 权利主体、授权、license 解释或披露边界需用户确认 | 等用户确认 | `WAIT_FOR_USER` |
| `/authorship-copyright-readiness:READY_FOR_APPLICATION_PACKAGE` | 主体、来源、残留、材料一致性均 PASS | 输出 readiness packet | `REPORT_AND_STOP` |

## 0.2 状态权威与路由动作 (State Authority / Route Action)

| 事项 | 权威事实源 | 路由动作 (Route Action) |
| ------ | ------------ | -------------- |
| 作者 / 权利人 | 项目级 SSOT / 用户确认 / legal docs | `WAIT_FOR_USER` if conflict |
| license / provenance | dependency lockfile / LICENSE / NOTICE / source URL | `REPORT_AND_STOP` if risk |
| release 文档一致性 | README / About / release notes / application materials | `CONTINUE_IN_WORKFLOW` |
| residue cleanup | grep / scan report / diff | `/specs-execute` or direct |
| 法律解释 | 用户 / 法务 | `WAIT_FOR_USER` |

## 1. 伴生文档 (Companion Documents)

| 文档 | 角色 | 何时读 |
| ------ | ------ | -------- |
| `../protocols/authorship-chain-protocol.md` | 作者、权利人、版本、关于页、README、LICENSE / NOTICE 主体一致性 | Phase 1 / 2 |
| `../protocols/third-party-provenance-protocol.md` | 依赖、素材、外部代码、agent 资产 provenance 与 license 风险 | Phase 2 |
| `../protocols/residue-cleanup-protocol.md` | AI 残留、prompt 残留、debug、secrets、第三方项目名残留清理 | Phase 3 |
| `application-material-consistency.md` | 软著 / 交付材料 / 截图 / 功能说明 / 测试记录一致性 | Phase 4 / 5 |
