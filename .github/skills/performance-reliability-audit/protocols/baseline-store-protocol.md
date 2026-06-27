# 基线存储协议 (Baseline Store Protocol)

> 性能 baseline 的双部位存储 / 版本化 / 同步规则；`/performance-reliability-audit` Phase 2 跑这些规则。决策来源：第 5 问"双部位：spec 生成 + 集中跨 spec refresh"。

---

## 1. 双部位存储

### 1.1 部位 A：spec artifact

**路径**：`docs/specs/<slug>/perf-audit/baseline.json`

**生命周期**：与 feature spec 同生同灭：

- spec Draft → 不写
- spec Active → Phase 2 写入 / 刷新
- spec Done → 不动（保留作为 close-out 快照）
- spec Archive → 与 spec 一同归档（保留 90 天）
- spec Merge Back → 升级到部位 B long-living（详 §1.4）

**用途**：

- 单 feature audit 期内快照
- spec close-out R-RDY-10 packet 引用
- review 时与 design 性能假设对照

### 1.2 部位 B：集中存储

**路径**：`perf-baseline/<scope>/baseline-v<N>.json`（仓库根目录下集中目录）

**目录结构**：

- `perf-baseline/<scope>/`：性能 baseline 根目录，其中 `<scope>` 代表子模块（如 `auth` / `api` / `frontend`）。
- `perf-baseline/<scope>/baseline-v<N>.json`：各版本 baseline，最新 `baseline-v<N>.json` 视为活跃（Active）版本。
- `perf-baseline/<scope>/deprecated/`：Brownfield 替换后，旧 baseline 的存储位置（保留 90 天）。
- `perf-baseline/<scope>/closed/`：spec close-out 时期快照的存储位置。
- `perf-baseline/<scope>/long-living/`：spec merge back 之后的长期 baseline。

**用途**：

- 跨 feature 性能演进追溯
- 跨 release regression 比对
- scheduled refresh 周期检查
- canary feedback 反向追溯

### 1.3 双部位职责对比

| 维度 | 部位 A (spec artifact) | 部位 B (集中) |
| ------ | ---------------------- | -------------- |
| 生命周期 | 与 spec 同 | 跨 spec 长期 |
| 版本化 | 无（最新覆盖） | ✅ 多版本保留 |
| 可被 packet 引用 | ✅ 主要引用 | ✅ 次要引用（用于历史比对） |
| 跨 spec 比对 | ❌ | ✅ |
| 归档 | 与 spec | 独立保留 |
| Merge back | → 升级到 B long-living | 保留所有版本 |

### 1.4 部位间同步规则

| ID | 触发事件 | 部位 A (spec artifact) 动作 | 部位 B (集中) 动作 | Changelog 描述 |
| ---- | ---------- | --------------------------- | ------------------- | --------------- |
| R-SYNC-1 | spec Active 且 Phase 2 首次写 baseline | 写入 `<slug>/perf-audit/baseline.json` | 写入 `perf-baseline/<scope>/baseline-v(N+1).json` | "新建 baseline，feature: `<slug>`" |
| R-SYNC-2 | spec Active 且 Phase 2 refresh 偏差 < 5% | 仅更新 `last_refreshed_at` | 仅更新 `last_refreshed_at`（不增加版本） | "Refresh 无显著变化" |
| R-SYNC-3 | spec Active 且 Phase 2 refresh 偏差在 5%~20% | 覆盖 `baseline.json` | 写入 `baseline-v(N+1).json`，保留原 `v(N)` | "Refresh diff `<X>`%，新版本 v(N+1)" |
| R-SYNC-4 | spec Active 且 Phase 2 refresh 偏差 >= 20% | 触发 `HG-AUDIT-PERF-BL-OVERWRITE` 挂起，用户批准后覆盖 `baseline.json` | 写入 `baseline-v(N+1).json`，保留原 `v(N)` | "Refresh diff >= 20%, 用户批准覆盖，原话: `<quote>`" |
| R-SYNC-5 | Brownfield Replace 路径 (旧 NFR-PERF deprecated) | 仅写入新路径 baseline | 旧 baseline 移动至 `deprecated/`（保留 90 天） | "Brownfield Replace, 旧 baseline 移至 deprecated" |
| R-SYNC-6 | spec close-out 或 Done | 保持不动 (保留作为快照) | 同步当前最新 baseline 到 `closed/<feature-slug>-v(N).json` | "Spec close-out, 快照保存" |
| R-SYNC-7 | 仅归档 spec (Archive Only) | 与 spec 一同归档 (保留 90 天) | 保留 `closed/<feature-slug>-v(N).json` | "Spec archived" |
| R-SYNC-8 | spec 合并回 long-living (Merge Back) | 保持不动 | 升级 `closed/` 目录至 `long-living/<scope>-v(N).json` | "Spec merged back to long-living" |

---

## 2. baseline.json 完整 schema

```json
{
  "$schema": "https://example.com/perf-baseline.schema.json",
  "audit_id": "PERF-<slug>-<YYYY-MM-DD>-<seq>",
  "feature_slug": "<slug>",
  "scope": "<scope>",
  "baseline_version": "v<N>",
  "established_at": "<ISO 8601>",
  "last_refreshed_at": "<ISO 8601>",
  "next_refresh_due": "<ISO 8601>",
  "refresh_cycle": "monthly | quarterly | per-release | manual",
  "established_by": "/performance-reliability-audit Phase 2",
  "trigger_mode": "spec-gate | scheduled | user-explicit",
  "user_quote_for_overwrite": "<quote or N/A>",

  "measure_environment": {
    "node_version": "20.10.0",
    "deps_lockfile_hash": "<sha256 of pnpm-lock.yaml or package-lock.json>",
    "deps_lockfile_path": "pnpm-lock.yaml",
    "data_volume": "10k users / 1M sessions / 100MB DB",
    "hardware": "Linode 4GB / 2 vCPU / SSD",
    "network": "<latency to dependent services>",
    "git_sha": "<commit sha>",
    "feature_flags": ["<active flags>"]
  },

  "metrics": {
    "<NFR-PERF-XXX>": {
      "metric": "latency-p95 | latency-p99 | memory | bundle-size | cold-start | API-throughput | DB-query-count | LCP | INP | CLS",
      "measure_command": "<reproducible command>",
      "samples": [<num>, <num>, <num>],
      "median": <num>,
      "p95": <num>,
      "p99": <num>,
      "stddev": <num>,
      "unit": "ms | KB | MB | rps | count",
      "budget": <num>,
      "verdict_at_baseline": "PASS | VIOLATED-MINOR | VIOLATED-MAJOR | VIOLATED-CRITICAL"
    }
  },

  "changelog": [
    {
      "version": "v<N>",
      "timestamp": "<ISO>",
      "trigger": "spec-gate | scheduled | user-explicit",
      "reason": "<change reason>",
      "user_quote": "<quote or N/A>",
      "diff_from_previous": "<diff_pct or N/A>"
    }
  ],

  "deprecated": false,
  "deprecated_at": null,
  "replaced_by": null
}
```

---

## 3. Refresh 周期表

| Scope 类型 | 默认周期 | 触发器 |
| ----------- | --------- | ------- |
| Active feature spec | per-release | spec close-out / release-deploy 调用 |
| Long-living scope（auth / api / frontend） | monthly | scheduled trigger |
| External integration（OAuth / payment / email） | quarterly | scheduled + 依赖变更 |
| Frontend bundle / LCP / INP | per-release | release-deploy canary |
| Cold start / startup time | per-release + 依赖升级 | spec-gate / scheduled |

每个 baseline 写入 `refresh_cycle` 字段；自动检查 `now() > next_refresh_due` 时标 `BASELINE_REQUIRED`。

---

## 4. 历史保留规则

| 部位 | 保留规则 |
| ------ | --------- |
| 部位 A spec artifact | 与 spec：Active 期保留；Archive 后 90 天 |
| 部位 B 当前版本 | 永久保留至下次覆盖 |
| 部位 B 历史版本 | 保留最近 **3 个**版本（baseline-v(N-2) / v(N-1) / v(N)） |
| 部位 B `deprecated/` | Brownfield Replace 后保留**90 天**然后删 |
| 部位 B `closed/` | spec close-out 快照保留**180 天** 然后归档 |
| 部位 B `long-living/` | merge back 后**永久保留**所有版本 |

清理脚本必须批量批准（不自动删除生产数据）。

---

## 5. 双部位一致性 invariants

| Invariant | 描述 |
| ----------- | ------ |
| INV-PERF-BL-1 | 每条 NFR-PERF 必有部位 A baseline.json（Active 期） |
| INV-PERF-BL-2 | 每条 NFR-PERF 必有部位 B baseline-v`<N>`.json（与 A 对应） |
| INV-PERF-BL-3 | 部位 A 与 B 当前版本的 metrics 必须字面一致（diff = 0） |
| INV-PERF-BL-4 | baseline_version 在两部位必须相同 |
| INV-PERF-BL-5 | 部位 B 历史版本不允许修改（只读快照） |
| INV-PERF-BL-6 | deprecated baseline 必须在 deprecated_at + 90 天后才能删 |
| INV-PERF-BL-7 | long-living baseline 不允许覆盖（只能新增版本） |

任一 invariant 违反 → `R-CHK-PERF-BL-*` FAIL。

---

## 6. 跨 release 比对决策表

| ID | 操作步骤 | 输入与对象 | 预期输出与计算公式 |
| ---- | ---------- | ------------ | ------------------- |
| R-COMP-1 | 历史数据拉取 | 部位 B 跨 release 历史：`v(N-3)`、`v(N-2)`、`v(N-1)`、`v(N)` | 对应版本的 baseline 数据 |
| R-COMP-2 | 计算演进趋势 | 对每条 NFR-PERF 计算中位数序列 | 计算各版本的 median：`median(v(N-3))`、`median(v(N-2))`、`median(v(N-1))`、`median(v(N))` |
| R-COMP-3 | 趋势特征识别 | 比对数值特征与跃迁度 | 判定性能趋势：1. 单调改善（性能提升）；2. 单调退化（渐进 regression）；3. 阶跃跳变（突发 regression）；4. 震荡（环境/测试不稳定） |
| R-COMP-4 | 产出审计报告 | 汇总上述趋势特征分析 | 写入 `cross-release-trend-report.md` |

---

## 7. 修订规则

- 本文修订必须同 PR 修订 `audit-protocol.md` Phase 2 + `../references/perf-checks-catalog.md` §1。
- schema 字段变更 → 必须有迁移脚本 + invariants 同步更新。
- 周期表调整 → 不需 RWSE Gate 但需 changelog 记录。
- `deprecated/` `closed/` `long-living/` 子目录命名不允许变更（被 workflow 直接引用）。
