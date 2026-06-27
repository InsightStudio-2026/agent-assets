---
name: asset-quality-gates
description: 代理资产质量门：让 workflow / skill 自身像代码一样可 lint、可 review、可验证；外部资产先 quarantine、后审计、再启用，绝不直接落入启用路径。
argument-hint: "要检查哪个代理资产？"
disable-model-invocation: true
---


# /asset-quality-gates · 代理资产质量门

**定位**：把 `.github/skills/`、`AGENTS.md` 当代码资产管理；新增、删除、重命名、移动、拆分资产，以及外部资产引入时，统一走本 skill 的结构 / 索引 / 边界 / eval / 命名 / 启用路径检查。

**边界**：只检查结构 / 索引 / 目录 / 状态动作 / 引用 / 入口骨架化 / 方法论一致性 / eval 证据 / 启用路径禁入；不替代人工设计审查、不自动重写长文档、不判断业务 spec 正确性、不替代 `/repo-safety-setup` 的本地安全基线（hooks / pre-commit / typecheck）。

**斜杠命令**：`/asset-quality-gates`

**配对实现 workflow**：`/repo-safety-setup`（本地 CI 类质量基线）、`/repo-agent-setup`（代理上下文初始化）。

---

## 懒加载契约

- **MUST read**: `./decision-matrix.md`
- 开始判定或执行 Phase 流程前，必须完整懒加载上述细节。

---

## 1. 伴随文档

| 文档 | 角色 | 何时读 |
| ------ | ------ | -------- |
| `references/checks-catalog.md` | R-CHK-1~15 检查项规则表（9 内部 + 6 intake）+ §3 R-CHK-EX-1.1~1.8 spec conformance 子规则（含 NFR 完整性） | Phase 3 / Phase 3.5 / Phase 3.6 / Phase 6 验证 |
| `protocols/intake-protocol.md` | 外部资产 6 步 intake 流程（provenance / license / quarantine / 适配 / AGENTS 索引 / 启用路径禁入） | Phase 2.5 / Phase 4 |
| `../specs-write/examples/` 5 个 canonical examples（EX-G-1 / EX-B-1 / EX-M-1 / EX-R-1 / EX-A-1，含 NFR 6 类示范） | spec conformance 应通过验证参考集 | Phase 3.6 |
| `../specs-write/conformance-fixtures/` 8 个 fixtures（F-FIX-1~8，含 NFR 留空 + Brownfield NFR 缺 Delta Op） | spec conformance 应失败验证参考集；must-hit 错误详 `expected-failure.md` | Phase 3.6 |
| `../specs-write/protocols/gate-dag-protocol.md` | Gate / DAG ID 横切协议（HG-OPS-*/ HG-SEC-* / S-HG-*/ F-HG-* / FA-HG-*/ DAG-* 命名空间事实源） | State 表 / Phase 4 装配 packet |
| `AGENTS.md` | 仓库级维护契约 + 启用 Workflow / Skill 索引 | Phase 3.5 / Phase 5 写入 |

---

## 2. 阶段骨架（具体规则细节见伴随文档）

每个 Phase 入口的 **MUST read**指令是硬规则——不读 = 视为违反该 Phase 的安全与质量防御。

### 阶段 1 — 范围探测**MUST read**`references/checks-catalog.md`

- 识别变更资产范围；分流 `/asset-quality-gates:SCOPE_DEFINED_INTERNAL` / `/asset-quality-gates:SCOPE_DEFINED_EXTERNAL_INTAKE` / `/asset-quality-gates:SCOPE_DEFINED_INDEX_SYNC`。
- 外部 intake 强制 Phase 2.5；内部修订直接 Phase 3。

### 阶段 2 — 内部资产盘点（仅 SCOPE_DEFINED_INTERNAL）**MUST read**`references/checks-catalog.md`

- 列出受影响的 workflow / skill / 支撑文档清单。
- 标记是新增 / 修订 / 重命名 / 移动 / 拆分 / 删除。

### 阶段 2.5 — 外部资产隔离（仅 SCOPE_DEFINED_EXTERNAL_INTAKE）**MUST read**`protocols/intake-protocol.md`

- 按 `intake-protocol.md` 落入 `.github/.quarantine/<source-slug>/`。
- 记录 provenance（来源 URL / commit SHA / 抓取时间 / 抓取者）+ license 文本副本 + 原始 frontmatter。
- 不得直接 `cp` 到 `.github/skills/`。

### 阶段 3 — 运行内部检查（R-CHK-1~9）**MUST read** `references/checks-catalog.md`

- 按 `checks-catalog.md` R-CHK-1~9 顺序执行。
- 失败 → 累积到 DAG-N-AUDIT-* F-N-5；不中断后续检查。
- 全部跑完 → 汇总报告。

### 阶段 3.5 — 运行索引同步检查（仅 SCOPE_DEFINED_INDEX_SYNC 或所有 scope 末尾）

**MUST read**`references/checks-catalog.md`。

- 按 `checks-catalog.md` R-CHK-9 子项检查 AGENTS.md 启用索引 vs 真实目录。
- 漂移 → `/asset-quality-gates:INDEX_SYNC_GAP_REPORTED`。

### 阶段 3.6 — 运行规范符合性检查（仅 SCOPE_DEFINED_SPEC_CONFORMANCE 或 SCOPE_DEFINED_INTERNAL 伴随 `../specs-write/examples/` / `../specs-write/conformance-fixtures/` 变更时）**MUST read**`references/checks-catalog.md §3`

- 按 `checks-catalog.md §3 R-CHK-EX-1.1~1.8` 子规则顺序检查（8 子规则：delta op / traceability / archive·merge / active·done / INV / out-of-charter / verification·artifacts /**NFR 完整性**）。
- **examples must-PASS**：对 `../specs-write/examples/EX-G-1/` / `EX-B-1` / `EX-M-1` / `EX-R-1` / `EX-A-1` 5 个 canonical examples 跑全 R-CHK-EX-1.1~1.8；任一子规则 FAIL 即 `/asset-quality-gates:CHECKS_FAILED_NEEDS_REVISION`。
- **fixtures must-HIT**：对 `../specs-write/conformance-fixtures/F-FIX-1~8/` 8 个 fixture 跑对应子规则；必须命中各自 `expected-failure.md` 声明的错误。漏识别 → `/asset-quality-gates:CHECKS_FAILED_NEEDS_REVISION`（checker 本身缺陷，修 checker 而不是修 fixture）。
- **启用状态**：子规则定义已启用（`checks-catalog.md §3.1`）；自动 checker 实现 pending — 在 checker 未落地前，本 phase 以人工对照模式运行（reviewer 按 fixture `expected-failure.md §2 期望报告内容` 逐项核对）。
- **全部 PASS** → 进入主流程下一阶段；DAG-N-AUDIT-*F-N-5 记录每条 R-CHK-EX-1.* 状态。

### 阶段 4 — 运行引入检查（仅 SCOPE_DEFINED_EXTERNAL_INTAKE）

**MUST read** `protocols/intake-protocol.md`。

- 按 `checks-catalog.md` R-CHK-10~15 顺序执行（provenance / license / 启用路径污染 / frontmatter / AGENTS 索引补登记 / skill eval 起点）。
- 失败 → `/asset-quality-gates:CHECKS_FAILED_NEEDS_REVISION`；可能整体回退到 `/asset-quality-gates:EXTERNAL_INTAKE_DECLINED`。

### 阶段 5 — 补丁起草与用户批准

- 生成 patch 草案（启用路径写入 + AGENTS.md 索引 + 支撑文档目录）。
- 装配 `HG-OPS-*` packet（F-HG-1~8 齐 + F-HG-6 回滚明确）。
- 等用户批准。

### 阶段 6 — 应用写入与验证

- 仅按批准 patch 写入；不扩范围。
- 写入后立即重跑 R-CHK-1~9（启用路径已就位）。
- 任一失败 → `/asset-quality-gates:VERIFY_FAILED_ROLLBACK_REQUIRED` → 按 F-HG-6 回滚 → `/asset-quality-gates:ROLLED_BACK`。
- 全部通过 → `/asset-quality-gates:DONE`。

---

## 3. 输出格式

每轮结束输出：

```markdown
## 代理资产与质量门禁审计报告 (Asset Quality Gates Report)

## 工作流状态 (Workflow State)

- State: /asset-quality-gates:`<state>`

## 审计范围 (Scope)

- 审计类型 (Internal / External Intake / Index Sync): <哪一种>
- 受影响资产 (Affected assets): <文件清单>

## 门禁/节点状态 (Gate / DAG Status)

- HG-OPS-{repo}-asset: <S-HG-* 状态>
- HG-SEC-{repo}-license: <S-HG-* 状态 或 N/A>
- DAG-N-AUDIT-{repo}-asset-quality: <node 状态>

## 细则检查结果 (Check Results)

- R-CHK-1 frontmatter 描述 (frontmatter description): <PASS / FAIL + 文件 + 行号>
- R-CHK-2 入口骨架化: <...>
- R-CHK-3 workflows 无子目录: <...>
- R-CHK-4 支撑文档位置: <...>
- R-CHK-5 AGENTS.md 启用索引登记: <...>
- R-CHK-6 状态权威与路由动作、恢复源说明 (State Authority / Route Action / Resume Source): <...>
- R-CHK-7 路由动作 (route action) 统一语义与无越界: <...>
- R-CHK-8 workflow 不误用 skill 术语: <...>
- R-CHK-9 别名 <sw> / <se> 指向真实路径: <...>
- R-CHK-10 来源溯源 (provenance) 完整（外部 intake 才填）: <...>
- R-CHK-11 启用路径未污染: <...>
- R-CHK-12 许可证协议 (license) 兼容（外部 intake 才填）: <...>
- R-CHK-13 frontmatter 已适配（外部 intake 才填）: <...>
- R-CHK-14 skill eval 评测起点已定义（外部 skill 才填）: <...>
- R-CHK-15 AGENTS 索引补登记 patch 已生成（外部 intake 才填）: <...>
- R-CHK-EX-1.1 增量差异动作显式化 (delta operation 1.1) (仅在 spec conformance 范围填): <PASS examples + HIT F-FIX-1 / FAIL>
- R-CHK-EX-1.2 溯源链追踪 (traceability) (同上): <PASS + HIT F-FIX-2 / FAIL>
- R-CHK-EX-1.3 归档/合并边界 (archive / merge) (同上): <PASS + HIT F-FIX-3 / FAIL>
- R-CHK-EX-1.4 活跃与完工状态一致 (active/done) (同上): <PASS + HIT F-FIX-4 / FAIL>
- R-CHK-EX-1.5 恒定规则守护 (INV) (同上): <PASS + HIT F-FIX-5 / FAIL>
- R-CHK-EX-1.6 规章外边界 (out-of-charter) (同上): <PASS + HIT F-FIX-6 / FAIL>
- R-CHK-EX-1.7 校验与产出交付物 (verification + artifacts) (同上): <PASS + HIT F-FIX-7 / FAIL>
- R-CHK-EX-1.8 非功能性需求完整性 (NFR) (同上): <PASS examples + HIT F-FIX-8 (Greenfield NFR 留空 + Brownfield NFR 缺 Delta Op) / FAIL>

## 失败检查项 (Failures)

- <按 R-CHK-* 列出失败项 + 修复建议 + FA-HG-* 失败动作>

## 修补补丁草案 (Patch Drafts)

- 待启用资产清单 + frontmatter / 入口骨架 / AGENTS.md 索引补登记 / 回滚方式

## 受约束的安全写入范围 (Safe-write Scope - 如涉受限写入)

- 写入标的 (Exact target): <N/A or 路径>
- 已有锚点 (Existing slot): <N/A or 锚点>
- 未越权说明 (No authority escalation because): <N/A or 理由>

## 授权边界 (Authorization Boundary)

- 路由动作 (Route Action): <CONTINUE_IN_WORKFLOW | WAIT_FOR_USER | CONFIRMED_ACTION | REPORT_AND_STOP>
- 授权来源 (Confirmation source): <N/A or 用户原话>
- 授权范围 (Authorized scope): <已展示的启用路径写入 + AGENTS 索引同步 + quarantine 删除>
- 未授权范围 (Not authorized): <业务代码 / feature spec / tracker / 下游 workflow / 真实世界副作用>

## 推荐下一步路由 (Recommended Next Route)

- <continue checking | /repo-safety-setup | /repo-agent-setup | /project-steward | EXTERNAL_INTAKE_DECLINED>

## 恢复/返航契约 (Return Contract)

- 目标路由 (Target route):
- 准入输入 (Entry input):
- 未决失败项/未填满信息包字段 (Outstanding failures / open patch drafts):

```

---

## 4. 禁用行为

- 不在未通过本 skill 的情况下直接 `cp` / `mv` 外部资产到 `.github/skills/`。
- 不自动重写超长 skill 入口；只生成"应抽到 skill 资源文件"的建议清单 。
- 不替代人工设计审查；R-CHK-* 失败时只报告 + 提建议，不绕过用户裁决。
- 不修改业务代码、feature spec、tracker、L1 SSOT 或 standards；只改资产层 + AGENTS.md 索引。
- 不把"AGENTS.md 未登记"自动当成漂移直接修；先报告 `/asset-quality-gates:INDEX_SYNC_GAP_REPORTED`，由用户决定是补登还是删资产。
- 不绕过 §0.4 启用路径禁入硬规则；不为加速跳过 quarantine。
- 不替代 skill eval 实测；R-CHK-14 只检查 eval 起点是否定义，不直接判定 skill 行为质量。

## 5. 快速自检清单

报告前自检：

- [ ] 是否已正确识别受影响资产并将其归入对应的变更 Scope？
- [ ] 外部资产引入前，是否已将其放入 quarantine 目录并记录了来源及 License？
- [ ] 资产修订后，是否严格运行了 R-CHK-1~9 内部规则检查？
- [ ] 是否确认了 AGENTS.md 索引与物理文件的映射完全同步？
- [ ] 启用路径写入前，是否已装配 `HG-OPS-*` 并获得了用户明确批准？
- [ ] 写入后是否重跑了校验，并验证了验证结果？

## 支撑资源

- [checks-catalog.md](./references/checks-catalog.md)
- [decision-matrix.md](./references/decision-matrix.md)
- [external-provenance-gsap-skills.md](./references/external-provenance-gsap-skills.md)
- [external-provenance-gstack-main.md](./references/external-provenance-gstack-main.md)
- [intake-protocol.md](./protocols/intake-protocol.md)
