# 安装器门禁协议 (Installer Gate Protocol)

## 1. Installer 范围

| 规则 ID (Rule ID) | Installer Type | 适用平台 | 必需证据 | 默认严重性 |
| --------- | ---------------- | ---------- | ---------- | ------------ |
| IGP-1 | MSI / MSIX / EXE | Windows | build log + install smoke + uninstall smoke + artifact hash | High |
| IGP-2 | DMG / PKG / APP | macOS | build log + quarantine / notarization readiness + install smoke | High |
| IGP-3 | DEB / RPM / AppImage | Linux | build log + install smoke + package metadata | High |
| IGP-4 | Portable build | Windows / macOS / Linux | launch smoke + update behavior + data path proof | Medium |
| IGP-5 | Store package | Microsoft Store / Mac App Store / other | store metadata + entitlement + review risk | Critical |

## 2. Installer Gate 规则

| 规则 ID (Rule ID) | 检查项 | PASS 标准 | FAIL 信号 | 路由 |
| --------- | -------- | ----------- | ----------- | ------ |
| IGP-R1 | Artifact identity | 文件名、version、platform、arch、hash 可追溯 | artifact 未固定或 hash 缺失 | `/desktop-release` Phase 2 |
| IGP-R2 | Clean install | 干净机器 / VM / profile 可安装并启动 | 只在开发机跑过 | `/desktop-release` Phase 2 |
| IGP-R3 | Upgrade install | 从上一稳定版升级后配置和数据可用 | 只测全新安装 | `/data-migration-safety` if local data changed |
| IGP-R4 | Uninstall | 卸载不破坏用户数据，或清理策略明示 | 卸载删除用户数据未告知 | `DESKTOP_RELEASE_BLOCKED` |
| IGP-R5 | Permission model | 安装权限、UAC、keychain、sandbox、entitlement 明确 | 要管理员权限但未说明 | `/security-privacy-audit` if permission risk |
| IGP-R6 | Offline / first launch | 首次启动、无网络、更新服务不可用时有可接受行为 | 离线即崩溃 | `/specs-execute` |
| IGP-R7 | Crash on launch | launch smoke 期间 crash dump / log 可定位 | 崩溃无日志 | `/observability-incident` |

## 3. Smoke Matrix

| 平台 (Platform) | 架构 (Arch) | 运行场景 (Scenario) | 预期结果 (Expected Result) | 证据路径 (Evidence Path) | 判定结论 (Verdict) |
| ---------- | ------ | ---------- | ----------------- | --------------- | --------- |
| windows | x64 / arm64 | clean install + launch | app opens / no crash | `<feature>/artifacts/desktop/install-windows.md` | PASS / FAIL |
| windows | x64 / arm64 | upgrade from previous stable | user config preserved | `<feature>/artifacts/desktop/upgrade-windows.md` | PASS / FAIL |
| macos | x64 / arm64 | clean install + launch | app opens / gatekeeper state known | `<feature>/artifacts/desktop/install-macos.md` | PASS / FAIL |
| linux | x64 / arm64 | package install + launch | app opens / desktop entry works | `<feature>/artifacts/desktop/install-linux.md` | PASS / FAIL |

## 4. Artifact Hash 表

| 交付产物 (Artifact) | 平台 (Platform) | 版本 (Version) | 哈希算法 (Hash Algorithm) | 哈希值 (Hash) | 原始构建命令 (Source Build Command) |
| ---------- | ---------- | --------- | ---------------- | ------ | ---------------------- |
| `<file>` | windows / macos / linux | `<version>` | SHA-256 | `<hash>` | `<command>` |

## 5. 判定

| 条件 | 状态 (State) |
| ------ | ------- |
| build + install + uninstall + upgrade smoke 全 PASS | `/desktop-release:DESKTOP_SCOPE_DEFINED` 可进入 signing/update gate |
| installer 缺 smoke 或 hash | `/desktop-release:INSTALLER_GATE_BLOCKED` |
| local data upgrade 风险未闭环 | `/desktop-release:LOCAL_DATA_GATE_BLOCKED` |
| crash / launch telemetry 缺失 | `/desktop-release:CRASH_REPORTING_REQUIRED` |
