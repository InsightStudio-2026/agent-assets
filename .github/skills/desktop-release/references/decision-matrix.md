---
description: "桌面发布闭环工作流（/desktop-release）专属的触发判定、状态转换路由、状态权威与动作决策矩阵"
---

# 桌面发布闭环决策矩阵（/desktop-release）

## 0. 触发判定

| ID | 前置条件 | 动作 | 下一步 | 源 |
| ---- | ---------- | ------ | -------- | ------ |
| R-DR-ENTRY-1 | 用户显式 `/desktop-release` | 启动桌面发布审计 | Phase 1 | 本文件 §0 |
| R-DR-ENTRY-2 | `NFR-PLAT-* Platform: desktop-*` Active | 启动 platform matrix 审计 | Phase 1 | `../../specs-write/templates/requirements.md §10.6` |
| R-DR-ENTRY-3 | 用户准备发布 installer / dmg / appx / msi / deb / rpm | 启动 installer gate | Phase 2 | 本文件 §2 |
| R-DR-ENTRY-4 | 涉 code signing / notarization / certificate / update channel | 启动 signing/update gate | Phase 3 | 本文件 §0.3 |
| R-DR-ENTRY-5 | 涉本地数据路径、配置迁移、离线缓存、用户文件 | 启动 local data gate；必要时分流 `/data-migration-safety` | Phase 4 | `../protocols/local-data-protocol.md` |
| R-DR-ENTRY-6 | 仅普通 Web 部署 / 无桌面运行时 | 不启用 | `/release-deploy` 或 direct | 本文件 §4 |
| R-DR-ENTRY-7 | 系统状态不清、下一步推进方向不明 | 停止并重定向 | 路由至 `/project-steward` | 临界状态 1 |
| R-DR-ENTRY-8 | 缺失母本或 L1 SSOT | 停止并重定向 | 路由至 `/project-inception` | 临界状态 2 |
| R-DR-ENTRY-9 | 属于纯缺陷根因诊断（局部、具体 bug） | 停止并重定向 | 路由至 `diagnose` 技能 | 临界状态 3 |
| R-DR-ENTRY-10 | 属于新功能、新需求开发、大重构落地 | 停止并重定向 | 路由至 `/specs-write` 与 `/specs-execute` | 临界状态 4 |
| R-DR-ENTRY-11 | 逻辑简单明确且适合 TDD 验证 | 停止并重定向 | 路由至 `tdd` 技能或直接执行 | 临界状态 5 |

## 0.1 状态与路由汇总 (State / Route Summary)

| 状态 (State) | 判定 | 下一步 | Gate / DAG ID 映射 |
| ------- | ------ | -------- | --------------------- |
| `/desktop-release:NO_DESKTOP_SCOPE` | 无桌面平台、安装器、签名、更新、本地数据风险 | 报告 N/A | `REPORT_AND_STOP` |
| `/desktop-release:DESKTOP_SCOPE_DEFINED` | 平台、打包工具、release candidate、目标 channel 已明确 | Phase 2 | `DAG-N-RELEASE-DESKTOP-{slug}` |
| `/desktop-release:INSTALLER_GATE_BLOCKED` | installer 构建、安装、卸载、权限、升级 smoke 缺证据 | 修复后重审 | `S-HG-3 GATE_PACKET_INCOMPLETE` |
| `/desktop-release:SIGNING_GATE_PENDING` | code signing / notarization / certificate 需批准或证据缺 | Phase 3 或等用户 | `HG-RELEASE-*` / `HG-IRREV-002` |
| `/desktop-release:UPDATE_CHANNEL_PENDING` | auto-update feed / staged rollout / channel 切换待确认 | 等用户批准 | `HG-RELEASE-*` |
| `/desktop-release:LOCAL_DATA_GATE_BLOCKED` | 本地数据迁移 / 缓存 / rollback 风险未闭环 | 分流 `/data-migration-safety` 或修 plan | `HG-MIGR-*` 候选 |
| `/desktop-release:CRASH_REPORTING_REQUIRED` | 崩溃上报、symbols、privacy、runbook 缺失 | 分流 `/observability-incident` 或补证据 | `HG-INCIDENT-*` 候选 |
| `/desktop-release:WAITING_DESKTOP_RELEASE_APPROVAL` | 用户可见发布 / 签名 / 更新通道 / app store 动作待批准 | 等用户批准 | `S-HG-4 WAITING_GATE_APPROVAL` |
| `/desktop-release:DESKTOP_RELEASE_GATE_READY` | installer、signing、update、local-data、crash reporting 全 PASS | 输出 gate packet | `S-HG-8 GATE_PASSED` |
| `/desktop-release:DESKTOP_RELEASE_BLOCKED` | 任一 critical 证据缺失或风险不可接受 | 阻塞 release | `REPORT_AND_STOP` |

## 0.2 状态权威与路由动作 (State Authority / Route Action)

| 事项 | 权威事实源 | 路由动作 (Route Action) |
| ------ | ------------ | -------------- |
| 平台约束 | `NFR-PLAT-*` + platform matrix | `CONTINUE_IN_WORKFLOW` |
| installer 验证 | installer build log + install / uninstall smoke | `CONTINUE_IN_WORKFLOW` |
| 签名 / notarization | signing log + certificate metadata + notarization result | `WAIT_FOR_USER` if real signing / publish |
| 自动更新 | update feed / channel / staged rollout plan | `WAIT_FOR_USER` if user-visible |
| 发布放行 | desktop release gate packet | `REPORT_AND_STOP` |

## 0.3 Hard-gate 命中条件

| 条件 | Gate | 必需证据 | 未满足动作 |
| ------ | ------ | ---------- | ------------ |
| code signing / certificate 使用 | `HG-RELEASE-*` + `HG-IRREV-002` | cert scope + command + artifact hash | `/desktop-release:WAITING_DESKTOP_RELEASE_APPROVAL` |
| notarization / app store submit | `HG-RELEASE-*` + `HG-IRREV-003` | target app id + version + rollback / delist plan | `/desktop-release:WAITING_DESKTOP_RELEASE_APPROVAL` |
| auto-update channel 切换 / staged rollout | `HG-RELEASE-*` | channel + cohort + rollback feed | `/desktop-release:WAITING_DESKTOP_RELEASE_APPROVAL` |
| 本地数据 destructive migration | `HG-MIGR-*` / `HG-IRREV-001` | backup / restore / compatibility evidence | `/data-migration-safety` |
