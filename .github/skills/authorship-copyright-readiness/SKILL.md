---
name: authorship-copyright-readiness
description: 作者性与版权就绪审计：上线、交付、软著或对外审查前核验作者 / 权利人 / 版本 / 依赖来源 / 原创性证据 / AI 残留清理 / 材料一致性；不做 AI 隐身，不替代法律意见。
argument-hint: "要审计哪个交付物？"
disable-model-invocation: true
---


# /authorship-copyright-readiness · 作者性与版权就绪审计

**定位**：在公开发布、客户交付、软著登记、应用商店提交、关于页 / LICENSE / NOTICE / README 整理前，核验作者 / 权利人 / 版本 / 依赖来源 / 原创性证据 / 交付物洁净与申请材料一致性。

**边界**：不做“AI 隐身”，不伪造人工痕迹，不删除合规要求保留的 AI 辅助披露、license、来源或版权信息；不承诺软著或法务结果；不替代律师、登记代理、安全审计或开源合规审计。发现权利链不清、license 风险或材料冲突时，只输出阻塞项和路由。

**斜杠命令**：`/authorship-copyright-readiness`

**默认主体口径**：若项目级 SSOT 无覆盖，作者及著作权人等主体口径严格参考 [compliance.instructions.md](../../instructions/compliance.instructions.md)。源码文件头只放必要版权主体，不扩散统一社会信用代码。

---

## 懒加载契约

- **MUST read**: `./decision-matrix.md`
- 开始判定或执行 Phase 流程前，必须完整懒加载上述细节。

---

## 1. 伴随文档

| 文档 | 角色 | 何时读 |
| ------ | ------ | -------- |
| `protocols/authorship-chain-protocol.md` | 权利链和作者真实性核验协议 | Phase 1, Phase 2 |
| `protocols/third-party-provenance-protocol.md` | 第三方依赖与来源审计协议 | Phase 2 |
| `protocols/residue-cleanup-protocol.md` | 代码清洁扫描与残留清理协议 | Phase 3 |
| `references/application-material-consistency.md` | 交付材料一致性核验协议 | Phase 4 |

---

## 2. 阶段骨架

| Phase | 目标 | MUST read | 输出 |
| ------- | ------ | ----------- | ------ |
| Phase 1 — Scope Intake | 确认交付目标、产品名、版本、材料范围 | `protocols/authorship-chain-protocol.md` | `/authorship-copyright-readiness:READINESS_SCOPE_DEFINED` |
| Phase 2 — Rights & Provenance | 核验主体、license、第三方来源与权利链 | `protocols/authorship-chain-protocol.md` + `protocols/third-party-provenance-protocol.md` | rights findings |
| Phase 3 — Residue Cleanup Audit | 扫描 prompt / debug / secrets / 模型自称 / 第三方名残留 | `protocols/residue-cleanup-protocol.md` | cleanup findings |
| Phase 4 — Material Consistency | 核验 README / About / 截图 / 功能说明 / 测试记录 / spec / 版本一致 | `references/application-material-consistency.md` | consistency findings |
| Phase 5 — Readiness Packet | 装配 application readiness packet 或阻塞报告 | 全部 companion | `/authorship-copyright-readiness:READY_FOR_APPLICATION_PACKAGE` 或 blocking state |

## 3. 输出格式

```markdown
## 署名与软著合规审计报告 (Authorship Copyright Readiness Report)

## 工作流状态 (Workflow State)

- State: /authorship-copyright-readiness:<STATE>

## 审计范围 (Scope)

- 产品名称 (Product):
- 产品版本 (Version):
- 发布/合规目标 (Target): 公开发布 (public release) | 客户交付 (client delivery) | 软件著作权申请 (software copyright application) | 应用商店上架 (app store) | 文档清理 (docs cleanup)

## 审计结论 (Verdict)

- 合规就绪度 (Readiness): PASS / FAIL
- 阻碍性合规缺口 (Blocking gaps): <None or list>

## 推荐接续路由 (Required Route)

- user/legal confirmation | /security-privacy-audit | /release-deploy documentation sync | /specs-execute | direct

```

## 4. 禁止动作

| 禁止项 | 原因 |
| -------- | ------ |
| 不做 AI 隐身或伪造人工痕迹 | 真实作者性来自证据链，不来自欺骗 |
| 不伪造 commit 历史 / TODO / 旧实现 / 作者过程 | 破坏权利链可信度 |
| 不删除必须保留的 license / NOTICE / 来源 | 可能造成侵权风险 |
| 不承诺软著必过 | 登记结果由外部机构决定 |
| 不替代法律意见 | 法律解释需用户 / 法务确认 |

## 5. 快速自检清单

报告前自检：

- [ ] 是否确认了交付目标与申请材料范围？
- [ ] 是否核验了作者、权利人及第三方依赖来源？
- [ ] 是否完成了代码清洁扫描与敏感信息残留清理？
- [ ] 是否确保 README、关于页、测试记录与实际版本一致？
- [ ] 是否已装配完整的版权就绪包？

## 支撑资源

- [application-material-consistency.md](./references/application-material-consistency.md)
- [authorship-chain-protocol.md](./protocols/authorship-chain-protocol.md)
- [decision-matrix.md](./references/decision-matrix.md)
- [residue-cleanup-protocol.md](./protocols/residue-cleanup-protocol.md)
- [third-party-provenance-protocol.md](./protocols/third-party-provenance-protocol.md)
