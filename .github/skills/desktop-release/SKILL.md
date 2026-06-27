---
name: desktop-release
description: 桌面发布闭环：治理 Windows / macOS / Linux installer、code signing、notarization、自动更新、本地数据迁移、崩溃上报、release channel 与回滚；用户可见发布和签名 / 更新通道切换必须用户批准。
argument-hint: "要发布哪个桌面应用到哪些平台？"
disable-model-invocation: true
---


# /desktop-release · 桌面发布闭环

**定位**：把桌面应用从构建产物到用户设备可安装、可升级、可回滚、可诊断的发布链路变成可审计 gate；覆盖 installer、code signing、notarization、auto-update、release channel、本地数据迁移、崩溃上报与平台兼容矩阵。

**边界**：不替代 `/specs-write` 定义平台约束，不替代 `/specs-execute` 实现桌面功能，不替代 `/release-deploy` 做通用发布编排；本 workflow 产出 desktop release gate packet，供 `/release-deploy` 或人工发布前消费。签名、notarization、更新通道切换、应用商店发布、用户可见自动更新必须用户批准。

**斜杠命令**：`/desktop-release`

**上游 / 下游**：上游消费 `NFR-PLAT-*`、`NFR-REL-*`、打包工具配置、证书状态、release candidate；下游输出 desktop release gate packet 给 `/release-deploy`，崩溃 / 更新事故分流 `/observability-incident`，本地数据迁移分流 `/data-migration-safety`。

---

## 懒加载契约

- **MUST read**: `./decision-matrix.md`
- 开始判定或执行 Phase 流程前，必须完整懒加载上述细节。

---

## 1. 伴随文档

| 文档 | 角色 | 何时读 |
| ------ | ------ | -------- |
| `templates/desktop-gate-packet-template.md` | 桌面发布门禁包与范围定义模板 | Phase 1, Phase 5 |
| `protocols/installer-gate-protocol.md` | 安装器/卸载器/升级冒烟验证协议 | Phase 2 |
| `protocols/signing-update-protocol.md` | 代码签名/公证/自动更新/灰度发布验证协议 | Phase 3 |
| `protocols/local-data-protocol.md` | 本地数据迁移/符号表/隐私政策审计协议 | Phase 4 |

---

## 2. 阶段骨架

每个 Phase 入口的 **MUST read** 指令是硬规则——不读 = 视为违反该 Phase 的发布与平台安全防御。

| Phase | 目标 | MUST read | 输出 |
| ------- | ------ | ----------- | ------ |
| Phase 1 — Scope Intake | 确认平台、candidate、channel、NFR-PLAT 锚点 | `templates/desktop-gate-packet-template.md §1` | `/desktop-release:DESKTOP_SCOPE_DEFINED` |
| Phase 2 — Installer Gate | 验证 build / install / uninstall / upgrade smoke | `protocols/installer-gate-protocol.md` | installer verdict |
| Phase 3 — Signing & Update Gate | 验证 signing / notarization / auto-update / staged rollout | `protocols/signing-update-protocol.md` | signing/update verdict |
| Phase 4 — Local Data & Crash Gate | 验证本地数据迁移、崩溃上报、symbols、privacy | `protocols/local-data-protocol.md` | local-data verdict |
| Phase 5 — Gate Packet | 装配 desktop release gate packet | `templates/desktop-gate-packet-template.md` | `/desktop-release:DESKTOP_RELEASE_GATE_READY` 或 `/desktop-release:DESKTOP_RELEASE_BLOCKED` |

## 3. 输出格式

```markdown
## 桌面应用发布审计报告 (Desktop Release Report)

## 工作流状态 (Workflow State)

- State: /desktop-release:<STATE>

## 审计范围 (Scope)

- 应用名称 (App): <name>
- 产品版本 (Version): `<version>`
- 目标平台 (Platforms): windows | macos | linux
- 发布渠道 (Channel): dev | beta | stable | app-store

## 审计结论 (Verdict)

- 桌面应用发布门禁结论 (Desktop Release Gate): PASS / FAIL
- 阻碍性缺陷 (Blocking gaps): <None or list>

## 推荐接续路由 (Required Route)

- /release-deploy | /data-migration-safety | /observability-incident | /specs-write | /specs-execute

```

## 4. 禁止动作

| 禁止项 | 原因 |
| -------- | ------ |
| 不自动签名 / notarize / 发布 installer | 用户可见或证书副作用必须批准 |
| 不把 build succeeded 当 release ready | 必须 install / uninstall / upgrade smoke |
| 不忽略本地数据回滚 | 桌面用户数据不可由代码 rollback 自动恢复 |
| 不把 crash reporting 当可选装饰 | 用户设备故障必须可诊断 |
| 不在未授权时切换 update channel | 会影响真实用户设备 |

## 5. 快速自检清单

报告前自检：

- [ ] 是否已确认应用名称、版本、构建平台以及发布通道？
- [ ] 构建产物是否通过了安装、卸载及升级的冒烟验证（不只看 Build Succeeded）？
- [ ] 代码签名和公证是否成功，自动更新灰度机制是否就绪？
- [ ] 本地数据迁移（若有）是否具备回滚方案，符号表及崩溃上报通道是否打通？
- [ ] 真实发布前，是否已将装配的桌面门禁包提报给 `/release-deploy`？

## 支撑资源

- [decision-matrix.md](./references/decision-matrix.md)
- [desktop-gate-packet-template.md](./templates/desktop-gate-packet-template.md)
- [installer-gate-protocol.md](./protocols/installer-gate-protocol.md)
- [local-data-protocol.md](./protocols/local-data-protocol.md)
- [signing-update-protocol.md](./protocols/signing-update-protocol.md)
