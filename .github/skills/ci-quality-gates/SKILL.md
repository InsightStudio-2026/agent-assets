---
name: ci-quality-gates
description: CI 质量门：把本地 lint、typecheck、test、coverage、安全、依赖、license、bundle、migration 与 flaky 管理升级为持续门禁；branch protection / required checks 变更必须用户批准。
argument-hint: "要配置哪个仓库的 CI 门禁？"
disable-model-invocation: true
---


# /ci-quality-gates · CI 质量门

**定位**：把本地验证升级为持续质量门，确保 PR / release candidate 在 CI 上可重复验证；覆盖 CI provider 探测、required checks、质量命令对齐、artifact 上传、失败分类、flaky 隔离、branch protection 建议。

**边界**：不替代 `/repo-safety-setup` 配置本地 hooks，不替代 `/code-health-dashboard` 汇总健康趋势，不替代 `/security-privacy-audit` 审计 secrets / CI/CD 安全；不自动修改远端 branch protection、repository settings、secrets、runner 或付费 CI 配额，必须用户批准。

**斜杠命令**：`/ci-quality-gates`

---

## 懒加载契约

- **MUST read**: `./decision-matrix.md`
- 开始判定或执行 Phase 流程前，必须完整懒加载上述细节。

---

## 1. 伴随文档

| 文档 | 角色 | 何时读 |
| ------ | ------ | -------- |
| `protocols/ci-provider-protocol.md` | CI provider 探测协议 | Phase 1 |
| `references/quality-gates-catalog.md` | 质量门门禁字典 | Phase 2 |
| `protocols/flaky-artifact-protocol.md` | artifact 和 flaky 治理协议 | Phase 3 |
| `templates/ci-gate-report-template.md` | 门禁报告模板 | Phase 4 |

---

## 2. 阶段骨架

| Phase | 目标 | MUST read | 输出 |
| ------- | ------ | ----------- | ------ |
| Phase 1 — Provider & Scope | 探测 CI provider、目标分支、现有 jobs、required checks | `protocols/ci-provider-protocol.md` | `/ci-quality-gates:CI_SCOPE_DEFINED` 或 `/ci-quality-gates:CI_PROVIDER_MISSING` |
| Phase 2 — Gate Design | 对齐本地命令与 CI jobs，定义 required / optional gates | `references/quality-gates-catalog.md` | `/ci-quality-gates:QUALITY_GATE_DRAFTED` |
| Phase 3 — Failure / Artifact / Flaky | 定义 artifact、失败分类、flaky 隔离与 rerun 边界 | `protocols/flaky-artifact-protocol.md` | gate evidence plan |
| Phase 4 — Report / Approval | 输出 CI gate report；涉及写入或远端保护变更等用户批准 | `templates/ci-gate-report-template.md` | `/ci-quality-gates:CI_GATE_READY` / `/ci-quality-gates:WAITING_CI_CHANGE_APPROVAL` |

## 3. 输出格式

```markdown
## CI 质量门禁报告 (CI Quality Gates Report)

## 工作流状态 (Workflow State)

- State: /ci-quality-gates:<STATE>

## 审计范围 (Scope)

- CI 提供商 (Provider):
- 目标分支 (Target branches):
- 强控校验项 (Required checks):

## 审计结论 (Verdict)

- CI 门禁就绪状态 (CI Gate): READY / BLOCKED / APPROVAL_REQUIRED
- 阻碍性缺陷 (Blocking gaps): <None or list>

## 推荐接续路由 (Required Route)

- /repo-safety-setup | /security-privacy-audit | /code-health-dashboard | user approval

```

## 4. 禁止动作

| 禁止项 | 原因 |
| -------- | ------ |
| 不自动改远端 branch protection | 真实仓库设置副作用必须用户批准 |
| 不降低质量门来通过临时失败 | flaky / env_error 必须分类处理 |
| 不把 CI 绿灯当 release approval | 发布放行归 `/release-deploy` |
| 不在不可信 PR 上读 secrets | CI/CD 安全风险归 `/security-privacy-audit` |
| 不写 CI 配置后不验证 | CI 门禁必须有可运行证据 |

## 5. 快速自检清单

报告前自检：

- [ ] 是否正确探测并锁定了当前 CI Provider 与目标分支？
- [ ] 是否对齐了本地校验命令与 CI Jobs？
- [ ] 是否为 Artifact、失败分类与 Flaky 隔离制定了处理规则？
- [ ] 涉及 branch protection 或 secrets 变更时，是否已取得用户批准？
- [ ] 是否完成了 CI 门禁配置文件写入后的运行验证？

## 支撑资源

- [ci-gate-report-template.md](./templates/ci-gate-report-template.md)
- [ci-provider-protocol.md](./protocols/ci-provider-protocol.md)
- [decision-matrix.md](./references/decision-matrix.md)
- [flaky-artifact-protocol.md](./protocols/flaky-artifact-protocol.md)
- [quality-gates-catalog.md](./references/quality-gates-catalog.md)
