---
name: developer-experience-audit
description: 开发体验审计：验证新 agent / 新开发者从仓库入口到首个可运行结果、首个合格 Medium spec、canonical examples 复现、协作恢复、CI / code health awareness 与 Windows / PowerShell 兼容。
argument-hint: "要审计哪个仓库的开发体验？"
disable-model-invocation: true
---


# /developer-experience-audit · 开发体验审计

**定位**：把“新 agent / 新开发者能否低摩擦跑通仓库并安全协作”变成可测事实；审计 README / setup / command / TTHW / spec 上手路径 / canonical examples / CI gate awareness / code health awareness / session recovery / 失败自救，不替代 `/repo-safety-setup` 的本地保护链，也不替代 `/asset-quality-gates` 的资产结构检查。

**边界**：只产出 DevEx audit packet、缺口列表和修订建议；不直接改业务代码，不静默改 L1 SSOT，不替代 `/specs-write` 写 feature spec，不替代 `/release-deploy` 做发布验证。若发现命令、文档或资产缺陷，按 Route Action 回切到对应 workflow 或 direct asset maintenance。

**斜杠命令**：`/developer-experience-audit`

---

## 懒加载契约

- **MUST read**: `./decision-matrix.md`
- 开始判定或执行 Phase 流程前，必须完整懒加载上述细节。

---

## 1. 伴随文档

| 文档 | 角色 | 何时读 |
| ------ | ------ | -------- |
| `protocols/tthw-protocol.md` | TTHW(首次成功运行时间)度量协议 | Phase 2 |
| `protocols/onboarding-path-protocol.md` | spec 编写与规格上手审计协议 | Phase 3 |
| `protocols/canonical-example-protocol.md` | 典范用例与 fixture 对照协议 | Phase 4 |
| `protocols/collaboration-readiness-protocol.md` | 协作就绪与 session 恢复验证协议 | Phase 5, Phase 6 |

---

## 2. 阶段骨架

每个 Phase 入口的 **MUST read** 指令 is a hard rule——不读 = 视为违反该 Phase 的开发体验质量防御。

| Phase | 目标 | MUST read | 输出 | 失败路由 |
| ------- | ------ | ----------- | ------ | ---------- |
| Phase 1 — Scope & Persona | 确定 persona、入口、首个成功定义 | N/A | `/developer-experience-audit:DX_SCOPE_DEFINED` | `/developer-experience-audit:DX_SCOPE_MISSING` |
| Phase 2 — TTHW Measurement | 验证 clone / install / setup / first run / first test | `protocols/tthw-protocol.md` | `/developer-experience-audit:TTHW_MEASURED` | `/repo-safety-setup` 或 direct docs fix |
| Phase 3 — Spec Onboarding | 用 `methodology-kernel + entry-decision-tree + cross-cutting §6` 完成首个 Medium spec 路径审计 | `protocols/onboarding-path-protocol.md` | `/developer-experience-audit:SPEC_ONBOARDING_VERIFIED` | `/specs-write` 或 direct asset maintenance |
| Phase 4 — Canonical Examples | 验证 EX-G-1 / EX-B-1 / EX-M-1 / EX-R-1 / EX-A-1 可定位、可解释、可被 fixture 对照 | `protocols/canonical-example-protocol.md` | `/developer-experience-audit:CANONICAL_EXAMPLES_VERIFIED` | `/asset-quality-gates` |
| Phase 5 — Collaboration Readiness | 验证 CI gate、code health、risk labels、session recovery、operational learnings、scope guard 可定位且有路由 | `protocols/collaboration-readiness-protocol.md` | `/developer-experience-audit:COLLABORATION_READINESS_VERIFIED` | `/ci-quality-gates` / `/code-health-dashboard` / `/tasks-to-issues` / `/issue-triage` / relevant skill |
| Phase 6 — Packet & Route | 装配 DevEx audit packet，列出缺口和下一步 | `protocols/collaboration-readiness-protocol.md` | `/developer-experience-audit:DX_APPROVED` 或 `/developer-experience-audit:DX_BLOCKED` | 对应 workflow |

## 3. 输出格式

```markdown
## 开发者体验与上手审计报告 (Developer Experience Audit Packet)

## 工作流状态 (Workflow State)

- State: /developer-experience-audit:`<state>`

## 审计范围 (Scope)

- 受试用户角色 (Persona): <new agent | new developer | maintainer>
- 目标成功事件 (Target success): <first run | first test | first Medium spec | examples verification>

## 首次运行耗时与体验测绘 (TTHW)
|  | 步骤 (Step) | 运行命令/动作 (Command / Action) | 预期结果 (Expected Result) | 实际结果 (Actual Result) | 耗时 (Time) | 结论 (Verdict) |  |
|  | ------ | ------------------ | ----------------- | --------------- | ------ | --------- |  |

## 规格上手路径审计 (Spec Onboarding)
|  | 检查项 (Check) | 信息源 (Source) | 结论 (Verdict) | 体验缺口 (Gap) |  |
|  | ------- | -------- | --------- | ----- |  |

## 规范标准示例审计 (Canonical Examples)
|  | 示例名称 (Example) | 预期学习收获 (Expected Learning) | Fixture 链接 (Fixture Link) | 结论 (Verdict) |  |
|  | --------- | ------------------- | -------------- | --------- |  |

## 协作就绪度审计 (Collaboration Readiness)
|  | 检查项 (Check) | 运行状态 (Status) | 事实依据 (Evidence) | 体验缺口 (Gap) | 跟踪路由 (Route) |  |
|  | ------- | -------- | ---------- | ----- | ------- |  |

## 阻碍性合规缺口 (Blocking Gaps)

- <None or list>

## 推荐改善路由 (Recommended Route)

- <direct docs fix | /repo-safety-setup | /specs-write | /asset-quality-gates | /ci-quality-gates | /code-health-dashboard | /tasks-to-issues | /issue-triage | session-context | operational-learnings | scope-guard>

```

## 4. 禁用行为

| 禁止项 | 原因 |
| -------- | ------ |
| 不把 README 命令“看起来合理”当 PASS | 必须有命令、预期、失败点或明确 N/A |
| 不把 canonical examples 当教程散文 | examples 必须能与 fixtures / checks 对照 |
| 不把 collaboration readiness 当 CI / code health 通过证据 | 它只验证协作入口可发现，实际 gate 归对应 workflow |
| 不替代 `/asset-quality-gates` | 资产结构、frontmatter、索引、conformance 仍归 AQG |
| 不替代 `/repo-safety-setup` | hooks / pre-commit / 本地命令保护链归 repo safety |

## 5. 快速自检清单

报告前自检：

- [ ] 是否已明确开发体验审计的 Persona 及目标 Success 定义？
- [ ] README 安装与运行命令是否被真实度量并记录了 TTHW？
- [ ] Onboarding 路径是否成功跑通了首个 Medium Spec 校验？
- [ ] 所有的 Canonical Examples 是否均能与对应的 Fixtures 对照通过？
- [ ] 协作就绪性（CI、Code Health、标签分流等）是否可在本仓成功被定位并具有明确路由？

## 支撑资源

- [canonical-example-protocol.md](./protocols/canonical-example-protocol.md)
- [collaboration-readiness-protocol.md](./protocols/collaboration-readiness-protocol.md)
- [decision-matrix.md](./references/decision-matrix.md)
- [onboarding-path-protocol.md](./protocols/onboarding-path-protocol.md)
- [tthw-protocol.md](./protocols/tthw-protocol.md)
