# External Asset Intake Protocol · /asset-quality-gates 外部资产 intake 协议

> **本文是 `/asset-quality-gates` workflow 的外部资产 intake 流程事实源**。所有"外部 skill / workflow / agent 资产引入"动作必须按本文 6 步走，绝不绕过 quarantine 直接落入启用路径。
> 本文档自身遵循结构化规则表 + ID 体系格式规范（入口骨架 + 支撑文档分离 + 零 ASCII 流程图）。

---

## 0. 定位与硬规则

### 0.1 文档定位

- 外部资产 intake 流程字典，与 `asset-quality-gates.md` Phase 2.5 + Phase 4 字面零漂移。
- 本文承接 `asset-quality-gates.md` Phase 2.5（quarantine）+ Phase 4（intake 检查 R-CHK-10~15）。
- 启用路径禁入硬规则锚点在 `asset-quality-gates.md §0.4`；本文是 §0.4 的展开实现。

### 0.2 范围与适用对象

| 资产来源 | 适用本协议 |
| --------- | ----------- |
| 外部公开仓库（Anthropic skills、社区 workflow、其他代理资产仓库） | ✅ |
| AI 生成的初稿（用户原话"参考某外部仓库的某 skill"） | ✅（视为外部） |
| 本仓库内重命名 / 移动现有资产 | ❌（归 `SCOPE_DEFINED_INTERNAL`） |
| 本仓库内新建从零设计的 workflow / skill | ❌（归 `SCOPE_DEFINED_INTERNAL`） |
| 用户直接粘贴的"完整 SKILL.md / workflow.md 草案"且来源未明 | ✅（视为外部） |

### 0.3 启用路径禁入硬规则

**绝对禁止**：未通过本协议 6 步 + R-CHK-10~15 + 用户批准前，任何外部资产以任何形式出现在以下路径：

- `.github/workflows/*.md`
- `.github/skills/<name>/SKILL.md`
- `.github/skills/<name>/*.md`（支撑文件）
- `.github/workflow-docs/<name>/*.md`（支撑文档）

唯一合法落点：`.github/.quarantine/<source-slug>/`（Cascade / Windsurf 不自动发现）。

违规检测时：立刻进入 `/asset-quality-gates:ACTIVATION_BLOCKED_BY_PATH_VIOLATION` + `FA-HG-4` + 强制 `git restore` 或 quarantine 重置。

---

## 1. 6 步 intake 流程

每步绑定 R-CHK-* 检查项；所有步骤必过才能进入 `ACTIVATION_APPROVED_PENDING_WRITE`。

| 步骤 (Step) | 名称 | 动作 | 产出物 (Deliverable) | 验证规则 (Verify R-CHK) | 状态 (State) |
| ------ | ------ | ------ | ------ | ------------ | ------- |
| `I-1` | Source Identification | 记录来源 URL / commit SHA / 抓取时间 / 抓取者；如无 commit SHA → 必须记录抓取日期 + 仓库 HEAD（不可验证则拒绝） | `<source-slug>/provenance.md` | R-CHK-10 | `DETECTING` → `SCOPE_DEFINED_EXTERNAL_INTAKE` |
| `I-2` | Quarantine Drop | 资产文件原样落入 `.github/.quarantine/<source-slug>/`；目录命名 kebab-case；保留原始结构与命名以便溯源 | `.github/.quarantine/<source-slug>/*` | R-CHK-11 | `QUARANTINED` |
| `I-3` | License Inspection | 抓取原仓库 LICENSE / COPYING / package.json license 字段；副本写入 quarantine；判定与本仓库兼容性 | `<source-slug>/license-original.txt` + `<source-slug>/license-compatibility.md` | R-CHK-12 | `QUARANTINED`（待裁决） |
| `I-4` | Frontmatter & Structure Adaptation | 按本仓库 §0.2 + AGENTS.md 规则改造 frontmatter（一句话 description / kebab-case）；草案放 quarantine，不写入启用路径 | `<source-slug>/<asset>.adapted.md`（草案） | R-CHK-13 | `CHECKS_RUNNING` |
| `I-5` | Skill Eval Seeding（仅 skill） | 定义无 skill 时会失败的 ≥ 1 个 expected behavior 场景 + ≥ 1 个 anti-trigger 场景；写入 `<source-slug>/eval-seed.md` | `<source-slug>/eval-seed.md` | R-CHK-14 | `CHECKS_RUNNING` |
| `I-6` | AGENTS Index Patch Draft | 生成 AGENTS.md 启用 Skill / Workflow 索引补登记 patch 开案（中文名 / 名称 / 角色 / 描述）；不直接写入 | `<source-slug>/agents-patch.md` | R-CHK-15 | `CHECKS_PASSED_PENDING_USER_APPROVAL` |

全部 6 步过 + 用户批准 → 进入 `ACTIVATION_APPROVED_PENDING_WRITE` → Phase 6 写入（quarantine → 启用路径 + AGENTS.md 索引 + 支撑文档目录）。

---

## 2. Provenance 必填字段（R-CHK-10）

`<source-slug>/provenance.md` 必填：

| 字段 | 必填 | 范例 | 缺失后果 |
| ------ | ------ | ------ | --------- |
| `source_url` | 必填 | `https://github.com/anthropics/skills` | R-CHK-10 失败 → FA-HG-2 |
| `commit_sha` | 必填（如适用） | `a1b2c3d` | 缺则需 `fetched_at` + `repo_head_label` |
| `fetched_at` | 必填 | `2026-05-23T22:00:00+08:00` | R-CHK-10 失败 |
| `fetched_by` | 必填 | `Cascade on behalf of 用户` 或具体协作者 | R-CHK-10 失败 |
| `original_license` | 必填 | `MIT` / `Apache-2.0` / `Unknown` | R-CHK-12 起跳条件 |
| `original_path_in_source` | 必填 | `skills/diagnose/SKILL.md` | 用于回溯 |
| `original_frontmatter` | 必填（如有） | 原始 YAML 块 | 用于 R-CHK-13 改造对照 |
| `intent_for_intake` | 必填 | 用户原话或本仓库定位声明 | 用于后续 review |

---

## 3. License 兼容性判定（R-CHK-12）

| License 类别 | 默认动作 | 用户裁决必须 |
| ------------- | --------- | ------------ |
| MIT / Apache-2.0 / BSD-2 / BSD-3 / CC0 / Unlicense | 兼容，可继续 I-4 | 仅在本仓库 license 不兼容时才需裁决 |
| ISC / Zlib / BSL-1.0 | 兼容，可继续 | 同上 |
| MPL-2.0 | 条件兼容；改造文件需保留 license 头 | 必须 |
| LGPL-2.1 / LGPL-3.0 | 一般不直接 vendor 进资产仓库；考虑仅参考机制 | 必须 |
| GPL-2.0 / GPL-3.0 / AGPL-3.0 | **不兼容**；不得 vendor，仅可"先审计后改造"（机制参考重写） | 必须 + 不得直接复制原文 |
| "All Rights Reserved" / 无 license / Custom 限制条款 | **拒绝默认 intake**；只能机制参考重写 | 必须明确放弃直接复制 |
| Unknown / 文件无 license / 仓库无 LICENSE | 拒绝默认 intake | 必须先溯源，溯不到则放弃 |

判定结果写入 `<source-slug>/license-compatibility.md`：

```markdown
## 开源许可证兼容性评估报告 (License Compatibility Report)

- 源许可证协议 (Source License): <类别>
- 兼容性结论 (Compatibility): <兼容 / 条件兼容 / 不兼容 / 未知>
- 默认处置动作 (Default Action): <继续 / 必须用户裁决>
- 用户裁决结论 (User Decision): <未裁决 / 同意直接引入 (vendor) / 同意进行机制参考与重写 / 拒绝>
- 用户原话授权引用 (User quote): "<原话>" (如适用)
- 评估人 (Recorded by): <Cascade 或具体协作者>
- 评估时间戳 (Recorded at): <时间戳>

```

---

## 4. 改造规则（R-CHK-13 适配清单）

外部资产进入本仓库前必须改造的最小项：

| 改造项 | 适用 | 改造动作 |
| -------- | ------ | --------- |
| frontmatter `description` 字段 | workflow / skill | 改为一句话；与本仓库定位 + AGENTS.md `description` 列对齐 |
| `description` 中的触发词 | skill | 补中文触发词（本仓库面向中文工作） |
| 私人路径 / 配置 | 任意 | 删除或抽象为占位符；明确"复用前必须改造" |
| 第三方工具假设 | 任意 | 标注本仓库未启用的工具（如 Claude Desktop 路径），改为通用表达或文档化前置条件 |
| skill 目录契约 | skill | 必须 `.github/skills/<kebab-name>/SKILL.md`；不得分类桶（`engineering/` / `productivity/` 等） |
| workflow 入口契约 | workflow | 必须 `.github/workflows/<kebab-name>.md`；不得子目录 |
| 跨工具兼容路径 | 任意 | 删除 `.github/skills/`、`.github/skills/` 等路径（本仓库主目标是 Windsurf） |
| AGENTS.md 编辑安全 | 任意 | 改造后必须经精确 patch；不得全文件重写邻近内容 |
| 启用 / 停用状态声明 | 任意 | 明确 Role：Active / Personal / Experimental |

改造后版本写入 `<source-slug>/<asset>.adapted.md`（草案），不写入启用路径。

---

## 5. 启用动作（Phase 6 写入）

`ACTIVATION_APPROVED_PENDING_WRITE` 后执行的写入序列：

| Step | 动作 | 路径 | 回滚 |
| ------ | ------ | ------ | ------ |
| `A-1` | 移动 / 复制 quarantine 草案到启用路径 | `.github/.quarantine/<slug>/<asset>.adapted.md` → `.github/workflows/<name>.md` 或 `.github/skills/<name>/SKILL.md` | `git restore` + 重新放回 quarantine |
| `A-2` | 创建支撑文档目录（如需要） | `.github/workflow-docs/<name>/` | `git rm -r` 该目录 |
| `A-3` | 应用 AGENTS.md 索引补登记 patch | `AGENTS.md`（精确 patch，不重写邻近） | 反向 patch |
| `A-4` | 保留 quarantine 中 provenance / license / eval-seed 副本作为审计证据 | `.github/.quarantine/<slug>/`（不删除 provenance.md / license-compatibility.md / eval-seed.md） | 无需回滚（只读证据） |
| `A-5` | 重跑 R-CHK-1~9 验证启用后健康 | 启用路径已就位 | 任一失败 → `VERIFY_FAILED_ROLLBACK_REQUIRED` → 按 A-1~A-3 反向回滚 |

---

## 6. 边界与反模式

| 反模式 | 检测点 | 修复动作 |
| -------- | -------- | --------- |
| 直接 `cp` 外部资产到 `.github/workflows/` 或 `.github/skills/` | R-CHK-11 / `git status` | 强制 `ACTIVATION_BLOCKED_BY_PATH_VIOLATION` + `FA-HG-4` + `git restore` |
| quarantine 缺 provenance.md | R-CHK-10 | 强制返回 I-1；不得继续 |
| license Unknown / 不兼容但跳过用户裁决 | R-CHK-12 | 强制 `EXTERNAL_INTAKE_DECLINED` 或重走 I-3 含用户裁决 |
| 改造时顺手"重写邻近内容" | 编辑 patch | 退回；按 `AGENTS.md` 编辑安全条款只做外科手术 |
| skill 缺 eval seed 直接启用 | R-CHK-14 | 强制返回 I-5 |
| AGENTS.md 索引补登记跳过 / 与启用路径漂移 | R-CHK-15 / R-CHK-5 | 启用前必须补 patch；不得"先启用、后补索引" |
| quarantine 内 provenance / license / eval-seed 被启用过程删除 | A-4 | 保留所有审计证据；删除 = `FA-HG-2` 复发 |

---

## 7. 修订规则

- 本文修订必须同 PR 修订 `asset-quality-gates.md` 入口（State 表 / Phase 骨架 / 报告模板）+ `checks-catalog.md`（R-CHK-* 顺序）。
- I-1~I-6 / A-1~A-5 顺序一旦发布不得变更；新增步骤后缀递增（I-7 / A-6）。
- License 兼容性表与本仓库 LICENSE 改动同步审视；未确认 LICENSE 前默认采用"机制参考重写"路径。
- 不变更"启用路径禁入"硬规则；任何加速 intake 的提议必须先修本文，不得绕过。
