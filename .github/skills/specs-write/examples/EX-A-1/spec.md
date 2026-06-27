# Spec · 头像上传 + CDN 切换（EX-A-1 Archive / merge 复合边界）

> **EX-A-1 canonical example · 单文件 spec**。本文展示一个 Brownfield Medium spec 内**两类性质不同的 REQ**：REQ-1 一次性 feature（→ Archive Only） + REQ-2 长期能力（→ Merge Back）。
> 与 `../../protocols/methodology-kernel.md` archive 复合边界字面零漂移。

---

## 0. Maturity Intake

| 字段 | 值 |
| ------ | --- |
| Project Maturity | Brownfield（已有头像分发基础设施作为 EXIST-REQ） |
| Audit Profile | Scoped Full-Surface Audit（涉对象存储 / CDN / PII 边界） |
| SSOT Health | OK（`.github/instructions/cdn-strategy.md` 已存在为草案占位 long-living；本 spec 借机贡献首个实质内容） |
| Decision | `PROCEED_TO_CHARTER` |

---

## 1. Charter

### 1.1 Sources

| Source ID | 类型 | 内容 | Timestamp |
| ----------- | ------ | ------ | ----------- |
| `SRC-1` | 用户原话 | "加头像上传 + 把头像分发改用 Cloudflare Images" | 2026-09-01 |
| `SRC-2` | 现网 | 现有头像分发走自建 CDN（`cdn.example.com` + 单 region），延迟高、命中率 65% | baseline |
| `SRC-3` | 运维需求 | Cloudflare Images 接入 + 多 region 自动分发 + 命中率目标 ≥ 90% | 2026-09-01 |

### 1.2 Existing Requirements

| EXIST-REQ ID | Source | 摘要 | Delta Operation |
| -------------- | -------- | ------ | ----------------- |
| `EXIST-REQ-1` | 现网 `users.avatar_url` 列 | 用户已有头像 URL 字段 | **Preserve**（schema 不变，URL 来源切换为 Cloudflare） |
| `EXIST-REQ-2` | 现网自建 CDN | `cdn.example.com` 头像分发 | **Replace**（迁移到 Cloudflare Images） |

### 1.3 Scope

- 用户在"个人资料"页面可上传头像（≤ 2MB / jpg|png|webp）。
- 上传成功后头像走 Cloudflare Images 分发（多 region 自动）。
- 现有头像逐步迁移（30 天迁移期）；迁移完成后旧 CDN 下线。

### 1.4 Out of Charter

- 不实现头像裁剪 UI（用户需自己裁剪后上传）。
- 不实现 GIF 动图头像。
- 不修改 `users.avatar_url` 列结构。
- 不在本 spec 实现 CDN 跨地区迁移（CDN 配置由 `cdn-strategy.md` 长期承载）。

### 1.5 Architectural Invariants

| INV ID | 类型 | 内容 |
| -------- | ------ | ------ |
| `INV-BAN-4` | 禁止 | 不在数据库存原文件二进制；只存 Cloudflare Images ID + URL |
| `INV-LIM-4` | 限制 | 文件类型 allowlist + 文件大小 ≤ 2MB + Content-Type 强校验 |
| `INV-SEC-6` | 必须 | Cloudflare API Token 走 secrets manager，不写代码 |

---

## 2. Requirements

### 2.1 REQ-1：头像上传 UI + 后端 endpoint（一次性 feature → Archive Only）

- **Delta Operation**：**Add**-**Derived From**：`SRC-1` → `REQ-1`
- **Relation to Existing**：复用 `users.avatar_url` 列（`EXIST-REQ-1` Preserve）
- **AC-1.1**：**WHEN** 已登录用户在个人资料页选择文件并提交，**THE SYSTEM SHALL**通过 `POST /api/me/avatar`（multipart/form-data）上传到 Cloudflare Images。

-**AC-1.2**：**WHEN** 上传成功，**THE SYSTEM SHALL**UPDATE `users.avatar_url = <Cloudflare Images URL>` + 删除旧 avatar（如有）。
-**AC-1.3**：**IF** 文件 > 2MB 或类型不在 allowlist（jpg/png/webp），**THEN THE SYSTEM SHALL**返回 `400 INVALID_AVATAR`，不上传。
-**Status**：Active

- **Archive 决策候选**：`Archive Only`（一次性 feature；未来"GIF 头像"或"头像裁剪"是新 spec，不回并）

### 2.2 REQ-2：Cloudflare CDN 路由 + 缓存策略（长期能力 → Merge Back）

- **Delta Operation**：**Replace**（自建 CDN → Cloudflare Images）+ **Deprecate**（自建 CDN 30 天迁移期后下线）
- **Derived From**：`SRC-2` + `SRC-3` → `REQ-2`；引用 `EXIST-REQ-2`
- **Relation to Existing**：自建 CDN `cdn.example.com` Day 0 停新写入 + Day 30 下线
- **AC-2.1**：**WHEN** Day 0 部署完成，**THE SYSTEM SHALL**把所有新上传头像写入 Cloudflare Images；旧头像保持在自建 CDN（迁移期）。

-**AC-2.2**：**WHEN** Day 1~Day 30，**THE SYSTEM SHALL**在用户访问旧头像时异步迁移（lazy migration）到 Cloudflare Images，并 UPDATE `avatar_url`。
-**AC-2.3**：**WHEN** Day 30 + 自建 CDN 调用量 = 0 + 用户批准，**THE SYSTEM SHALL**下线自建 CDN（DNS 切换 + 关闭存储 bucket）。
-**AC-2.4**：**WHEN** Cloudflare Images API 不可用，**THE SYSTEM SHALL**fallback 到 24 小时只读模式（不再上传，已上传头像继续可读）。
-**Status**：Active（迁移期）

- **Archive 决策候选**：`Merge Back`（CDN 路由 + 缓存策略 = 长期能力，需合入 `.github/instructions/cdn-strategy.md`；未来扩展多 region 配置 / 边缘缓存调优等需要本 REQ 作为基线）

---

## 3. Plan / Design

### 3.1 DSN-1 数据契约

| 项 | Schema | 备注 |
| ---- | -------- | ------ |
| `users.avatar_url` | unchanged | URL 内容从 `cdn.example.com/<id>` 切换为 `<account>.imagedelivery.net/<id>` |
| Cloudflare Images account | account_id + API token | 写 secrets manager（`SECRETS_CLOUDFLARE_IMAGES`） |

### 3.2 DSN-2 接口契约

| Endpoint | Method | Auth | 描述 |
| ---------- | -------- | ------ | ------ |
| `POST /api/me/avatar` | POST | Required | 接收 multipart 文件 → 转发 Cloudflare Images API → UPDATE avatar_url |
| `DELETE /api/me/avatar` | DELETE | Required | 删除 Cloudflare Images entity + 清空 avatar_url |

### 3.3 DSN-3 失败策略

| 场景 | 错误码 | HTTP |
| ------ | -------- | ------ |
| 文件超大 | `INVALID_AVATAR_SIZE` | 400 |
| 类型不允许 | `INVALID_AVATAR_TYPE` | 400 |
| Cloudflare API 失败 | `CLOUDFLARE_UPSTREAM_ERROR` | 502 |
| Cloudflare 24h 不可用 | `AVATAR_UPLOAD_PAUSED` | 503（fallback 只读） |

---

## 4. Tasks

| Task ID | Description | Status | Verification | Archive 路径 |
| --------- | ------------ | -------- | -------------- | ------------ |
| `TASK-1` | `POST /api/me/avatar` endpoint + Cloudflare Images 集成 | Done | `pnpm test src/api/__tests__/avatar.test.ts` + e2e 上传流程 | REQ-1 → Archive Only |
| `TASK-2` | `<AvatarUpload>` UI 组件 + 客户端文件校验 | Done | `pnpm test:e2e tests/e2e/avatar-upload.spec.ts` | REQ-1 → Archive Only |
| `TASK-3` | Lazy migration 中间件（旧头像访问时异步迁移） | Done | `pnpm test src/middleware/__tests__/avatar-lazy-migrate.test.ts` | REQ-2 → Merge Back |
| `TASK-4` | 自建 CDN 调用量监控 dashboard（Day 0~30 观测） | Done | `dashboards/legacy-cdn-traffic.json` 上线 + 7 天观测 | REQ-2 → Merge Back |
| `TASK-5` | Cloudflare API token 写 secrets manager + dry-run 模式 | Done | `pnpm test src/lib/__tests__/cloudflare-images.test.ts` | REQ-2 → Merge Back |
| `TASK-DEPRECATE-1` | Day 30: 自建 CDN 下线（DNS 切换 + bucket 关闭） | Pending（计划 2026-10-15） | Day 30 调用量 = 0 + 用户批准 RWSE Gate | REQ-2 → Merge Back（延后至 Day 30 由 cdn-strategy.md 接管 deprecation ledger） |

---

## 5. Verification

### 5.1 整体命令

```powershell
pnpm typecheck
pnpm lint
pnpm test
pnpm test:e2e
pnpm bundle:analyze
```

### 5.2 DoD

- TASK-1~5 Done + Verification 字段。
- TASK-DEPRECATE-1 进入 Pending（Day 30 由 release-deploy 单独闸口处理）。
- 所有 INV（INV-BAN-4 / INV-LIM-4 / INV-SEC-6）测试用例 PASS。

---

## 6. Status

- spec 阶段：Done（除 TASK-DEPRECATE-1 Day 30 任务外）
- archive 决策：见 `archive.md`（**复合**：REQ-1 Archive Only + REQ-2 Merge Back）
