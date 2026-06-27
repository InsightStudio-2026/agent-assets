# Deploy Protocol · /release-deploy 部署协议事实源

> **本文是 `/release-deploy` workflow 的 dry-run / deploy / smoke / canary / rollback 命令规范与证据要求字典**。所有 P-DEP-*/ P-SMK-* / P-CAN-*/ P-RBK-* 协议项在此定义；入口 workflow 按 ID 引用，不重复事实。
> 本文档自身遵循结构化规则表 + ID 体系格式规范（入口骨架 + 支撑文档分离 + 零 ASCII 流程图）。

---

## 0. 定位与索引

### 0.1 文档定位

- 部署 / 验证 / 回滚四类操作的命令规范与证据要求；与 `release-deploy.md` deploy / canary / rollback 项零漂移。
- 不是工具教程；不绑定特定平台（Vercel / Netlify / AWS / Cloudflare / 自建），只规定每类操作必须满足的语义。
- 每个 P-* 给：动作 / 证据要求 / 失败条件 / 不可绕过项。

### 0.2 ID 命名空间

- `P-DEP-1~6`：Deploy 阶段协议（含 dry-run）。
- `P-SMK-1~5`：Post-deploy Smoke 协议。
- `P-CAN-1~5`：Canary / Rollout 协议。
- `P-RBK-1~6`：Rollback 协议。

---

## 1. Deploy 阶段（P-DEP-*）

| 规则 ID (Rule ID) | 动作 | 证据要求 | 失败条件 | 不可绕过项 |
| --------- | ------ | --------- | --------- | ----------- |
| `P-DEP-1` | Deploy Config 记录 | 平台名 / 生产 URL / health endpoint / deploy 命令 / status 命令 / 凭证存放位置（不入库）；写入 `release-plan.md` | 缺任一 | 首次真实发布前必填 |
| `P-DEP-2` | Dry-run | dry-run 命令实际执行；输出全文保存到 `artifacts/dry-run-`<version>`.log`；包含 plan diff / resource diff / migration plan | dry-run 报错 / 暴露平台 / URL / 命令 / migration 缺陷 | 首次真实发布、全新目标环境、关键平台变更必须；非首次可跳过但需 `release-report.md` 明示 |
| `P-DEP-3` | Approval Packet 装配 | F-HG-1~8 全齐：F-HG-1 范围、F-HG-2 影响面、F-HG-3 用户原话、F-HG-4 作用范围、F-HG-5 dry-run 等前置证据、F-HG-6 rollback 命令、F-HG-7 严重性、F-HG-8 owner | 任一字段缺 | F-HG-3 必含完整原话引用；F-HG-6 必含完整 rollback 命令或不可回滚明示 |
| `P-DEP-4` | Deploy 执行 | 命令输出全文保存到 `artifacts/deploy-`<version>`.log`；目标环境 health endpoint 检查通过 | 命令非零退出 / health endpoint 红 / 部分 service 未就绪 | 仅在 `APPROVED_TO_DEPLOY` 后执行；命令必须与 packet F-HG-3 展示一致 |
| `P-DEP-5` | 部署后立即验证 | health endpoint 5xx / 4xx 检查；version endpoint 返回新版本号；DB 连接 / 队列 / 缓存连通 | 任一失败 | 不视为 deploy 成功；进入 `DEPLOY_FAILED` |
| `P-DEP-6` | 失败处置 | 进入 `DEPLOY_FAILED`；判定是否 `ROLLBACK_REQUIRED` | 失败后未记录原因 / 未判定 rollback | 不允许"重跑一次试试"；必须先分析后决定 |

---

## 2. Post-deploy Smoke（P-SMK-*）

| 规则 ID (Rule ID) | 动作 | 证据要求 | 失败条件 | 不可绕过项 |
| --------- | ------ | --------- | --------- | ----------- |
| `P-SMK-1` | Health Check | liveness / readiness / dependency check 三类全过；输出保存到 `artifacts/smoke-health-`<version>`.log` | 任一红 | 不允许只跑 liveness 跳过 readiness |
| `P-SMK-2` | 关键路径 Smoke | 注册 / 登录 / 主流程提交 / 支付 / 订阅 / 数据同步等关键路径全过；按 spec 定义的 `acceptance` 列表 | 任一关键路径失败 | 关键路径清单来自 spec；不允许临时缩减 |
| `P-SMK-3` | Console / Network Errors | 浏览器 console error / network 4xx 5xx / unhandled promise rejection 检查 | 任一关键路径产生 console error 或 5xx | UI 类发布必须；纯后端可标 N/A |
| `P-SMK-4` | 截图证据 | 关键页面截图保存到 `artifacts/screenshots-<version>/`；命名 `<route>-`<viewport>`.png` | 截图缺 / 无法识别页面状态 | UI 类发布必须；纯后端可标 N/A |
| `P-SMK-5` | Smoke 总结 | `post-deploy-smoke.md` 列每条关键路径 PASS / FAIL + 证据链接 | 总结缺 / 与原始日志漂移 | 必须；smoke 是 RELEASE_DONE 前置 |

---

## 3. Canary / Rollout（P-CAN-*）

| 规则 ID (Rule ID) | 动作 | 证据要求 | 失败条件 | 不可绕过项 |
| --------- | ------ | --------- | --------- | ----------- |
| `P-CAN-1` | Baseline 采集 | 发布前 baseline 数据：p95 / LCP / CLS / INP / 资源数 / 总传输量 / 错误率 / 关键业务转化率 | baseline 缺 | UI / 用户可见类发布必须；后端可只采 p95 + 错误率 |
| `P-CAN-2` | Canary 阶段配置 | 流量百分比 / 用户群 / 时长 / 自动扩量条件 / 自动回滚条件；写入 `release-plan.md` | 配置缺 / 自动回滚未定义 | 大流量发布必须；小流量可标 N/A 但需明示 |
| `P-CAN-3` | Canary 数据采集 | 与 baseline 同维度数据采集；窗口至少覆盖一个完整业务周期 / 按 spec 定义 | 采集窗口太短 / 维度漂移 | 不允许只看错误率忽略性能 |
| `P-CAN-4` | Regression 判定 | 按 baseline 比较；超阈值（业务定义）即 `CANARY_REGRESSION_DETECTED` | 漏掉某维度 / 用单次截图代替统计 | 必须用统计不是截图 |
| `P-CAN-5` | 扩量到全量 | 每次扩量都是新的 `WAITING_DEPLOY_APPROVAL`；新一轮 packet 装配；F-HG-3 必含本次扩量原话 | 沿用上一轮批准跳过 | 扩量授权不继承；详 `release-deploy.md §0.3` |

---

## 4. Rollback（P-RBK-*）

| 规则 ID (Rule ID) | 动作 | 证据要求 | 失败条件 | 不可绕过项 |
| --------- | ------ | --------- | --------- | ----------- |
| `P-RBK-1` | Rollback Plan 草拟 | rollback 命令 / 数据回滚步骤 / feature flag 关闭顺序 / 通信稿模板；写入 `rollback-plan.md`；纳入 packet F-HG-6 | rollback 步骤缺 / 数据不可回滚未明示 | 全部 release 前必填；不可回滚必须前置告知用户并写入 packet |
| `P-RBK-2` | Rollback 触发条件 | 按 `DEPLOY_FAILED` / `SMOKE_FAILED` / `CANARY_REGRESSION_DETECTED` 自动判定；用户也可手动触发 | 触发后无判定 / 久拖不决 | 必须明确决策点 |
| `P-RBK-3` | Rollback 执行 | 严格按 `rollback-plan.md` 步骤；命令输出保存到 `artifacts/rollback-`<version>`.log` | 偏离 plan / 改步骤 | 不允许临场改 plan；如必改 → 重新展示给用户批准 |
| `P-RBK-4` | 数据回滚 | DB restore / backfill 撤销 / 缓存清理 / 队列处置；命令输出保存 | restore 失败 / 数据漂移 | 数据回滚优先级高于代码回滚 |
| `P-RBK-5` | Rollback 验证 | 按 P-SMK-1~3 重跑 health + 关键路径 smoke | 任一红 | rollback 必须有验证；否则不视为 `ROLLED_BACK` |
| `P-RBK-6` | Incident 路由判定 | rollback 后判断是否需启 `/observability-incident`（如用户已感知 / SLO 违约 / 数据丢失） | 应启未启 | 必须显式判定，不能默认跳过 |

---

## 5. 边界与禁止项

| 反模式 | 检测点 | 修复动作 |
| -------- | -------- | --------- |
| 把 `deploy succeeded` 当 RELEASE_DONE | P-SMK-*/ P-CAN-* | 必须 smoke + canary 全过才进入 RELEASE_DONE |
| Smoke 跳过 console / network 检查 | P-SMK-3 | UI 类不允许跳过 |
| Canary 用单次截图代替统计 | P-CAN-3 / P-CAN-4 | 强制要求多窗口统计 |
| Rollback 临场改 plan | P-RBK-3 | 必须重新展示给用户批准 |
| 不可回滚 migration 静默 deploy | P-RBK-1 | 必须前置告知用户；packet F-HG-6 含明示 |
| 扩量到全量沿用旧批准 | P-CAN-5 | 强制重批 |
| 仅监控错误率忽略性能 | P-CAN-3 | 强制采集 baseline 同维度 |
| dry-run 跳过但是首次发布 | P-DEP-2 | 强制必跑 |

---

## 6. 修订规则

- 本文修订必须同 PR 修订 `release-deploy.md` Phase 5-8 骨架与 §0.3 Hard-gate 表。
- P-DEP-*/ P-SMK-* / P-CAN-*/ P-RBK-* ID 一旦分配不得复用；废弃改 deprecated。
- 新增 P-* 必须先在 `release-deploy.md` 对应项同步事实源。
- 不引入平台特定命令；保持平台无关的语义层规范。
