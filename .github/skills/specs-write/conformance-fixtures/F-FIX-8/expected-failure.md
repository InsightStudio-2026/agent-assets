# F-FIX-8 期望失败报告

**Fixture ID**: `F-FIX-8`
**对应 Sub-rule**: `R-CHK-EX-1.8`（NFR 完整性校验）
**触发时机**: `/asset-quality-gates` Phase 3.6
**应失败动作**: `FA-HG-2` + 阻塞 spec close-out

---

## 1. 期望失败信号（checker 必报告）

`R-CHK-EX-1.8` 跑 `F-FIX-8/requirements-A.md` 与 `F-FIX-8/requirements-B.md` 时，必须输出以下 4 类失败信号：

### A. Greenfield NFR 留空（requirements-A.md）

```text
FAIL R-CHK-EX-1.8 in F-FIX-8/requirements-A.md:

  - §10.0 标 5 类 High（SEC / PERF / OBS / REL / UX）但 §10.1~§10.5 整段空白：
    NFR-SEC: 0 条 Active, 0 条 N/A
    NFR-PERF: 0 条 Active, 0 条 N/A
    NFR-OBS: 0 条 Active, 0 条 N/A
    NFR-REL: 0 条 Active, 0 条 N/A
    NFR-UX: 0 条 Active, 0 条 N/A
  - §10.6 标 NFR-PLAT = Low 但既不是 Active 也无 'Status: N/A: <理由>' 显式声明
  - §10.7 路由表为空表头，与 §10.1~§10.6 不一致（缺 routing 入口）
  - §10.8 DoD 自检空白

```

### B. Brownfield NFR 缺 Delta Operation（requirements-B.md）

```text
FAIL R-CHK-EX-1.8 in F-FIX-8/requirements-B.md:

  - charter Project Mode = Brownfield，每条 NFR 必填 'Delta Operation' 字段
  - §10.1 NFR-SEC-002: 缺 'Delta Operation' 字段（实际应为 Preserve）
  - §10.2 NFR-PERF-001: 缺 'Delta Operation' 字段（实际应为 Replace）
  - §10.7 路由表 'Delta Op' 列两行标 'MISSING'，与 §10.1/§10.2 一致漂移
  - §10.8 DoD: Brownfield delta 自检项未通过

```

---

## 2. 期望报告内容（checker 必生成）

```markdown
## Asset Quality Gates Report (Phase 3.6 Spec Conformance)

## R-CHK-EX-1.8 NFR 完整性 — FAIL

### F-FIX-8 / requirements-A.md (Greenfield NFR 留空)

|  | 失败项 | 位置 | 期望修复 |  |
|  | ------- | ------ | --------- |  |
|  | NFR-SEC 类 High 但无 Active | §10.1 | 至少加 1 条 NFR-SEC-* `Status: Active` |  |
|  | NFR-PERF 类 High 但无 Active | §10.2 | 至少加 1 条 NFR-PERF-* `Status: Active` |  |
|  | NFR-OBS 类 High 但无 Active | §10.3 | 至少加 1 条 NFR-OBS-* `Status: Active` |  |
|  | NFR-REL 类 High 但无 Active | §10.4 | 至少加 1 条 NFR-REL-* `Status: Active` |  |
|  | NFR-UX 类 High 但无 Active | §10.5 | 至少加 1 条 NFR-UX-* `Status: Active` |  |
|  | NFR-PLAT 类 Low 未显式 N/A | §10.6 | 加 `NFR-PLAT: N/A — <理由>` 声明 |  |
|  | 路由表空 | §10.7 | 与 §10.1~§10.6 各类一致填充 |  |

参考 `../../examples/EX-G-1/requirements.md §6` 修复。

### F-FIX-8 / requirements-B.md (Brownfield NFR 缺 Delta Op)

|  | 失败项 | 位置 | 期望修复 |  |
|  | ------- | ------ | --------- |  |
|  | NFR-SEC-002 缺 Delta Operation | §10.1 | 加 `Delta Operation: Preserve` |  |
|  | NFR-PERF-001 缺 Delta Operation | §10.2 | 加 `Delta Operation: Replace` |  |
|  | 路由表 Delta Op 列 MISSING | §10.7 | 与 §10.1/§10.2 同步填 |  |

参考 `../../examples/EX-B-1/requirements.md §7` 修复。

## 失败动作

- `FA-HG-2`: 报告失败 + 修复建议
- 阻塞 spec close-out（高风险 NFR 不可静默忽略）
- 不阻塞 long-living spec merge back（NFR 漂移在 active 期就该修，不进 archive）

```

---

## 3. checker 必规避的误识别

`R-CHK-EX-1.8` 不应误判以下合法 spec：

- ✅ **Greenfield 全 Low + 全 N/A**：High-Risk 表全标 Low，每类 §10.x 显式 `Status: N/A: <理由>`，§10.7 全 N/A 行 — 应 PASS。
- ✅ **Greenfield 6 类 High + 6 条 Active**：每类各 1 条 Active，无 Delta Operation 字段（Greenfield 不强制）— 应 PASS。
- ✅ **Brownfield + Greenfield 混合 spec**：spec 主体 Greenfield 但引用 EXIST-NFR-* — 检查仍按 charter Project Mode 字段判定。
- ✅ **Active NFR 有 Verification 但 Routed to: N/A**：UX-002 类型场景，本身合规（不强制每类必有 routed to 专项 workflow，但必有 Verification）。

---

## 4. checker 实现提示

```python
## 伪代码 / 实施提示
def check_R_CHK_EX_1_8(requirements_md_path, charter_md_path):
    project_mode = parse_charter_project_mode(charter_md_path)  # 'Greenfield' | 'Brownfield' | 'Hybrid'
    nfr_section = parse_nfr_section(requirements_md_path)  # §10
    
    failures = []
    
    # (1) High-Risk Assessment 表存在
    if not nfr_section.high_risk_table:
        failures.append("§10.0 High-Risk Assessment 表缺失")
        return failures
    
    # (2) 每个 High 类必有 ≥ 1 条 Active NFR
    for nfr_type, risk_level in nfr_section.high_risk_table.items():
        if risk_level == 'High':
            actives = [n for n in nfr_section.nfrs(nfr_type) if n.status == 'Active']
            if len(actives) == 0:
                failures.append(f"{nfr_type} 类 High 但无 Active NFR")
    
    # (3) Low 类必显式 N/A
    for nfr_type, risk_level in nfr_section.high_risk_table.items():
        if risk_level == 'Low':
            actives = [n for n in nfr_section.nfrs(nfr_type) if n.status == 'Active']
            na_decls = [n for n in nfr_section.nfrs(nfr_type) if n.status.startswith('N/A:')]
            if len(actives) == 0 and len(na_decls) == 0:
                failures.append(f"{nfr_type} 类 Low 但未显式 N/A")
    
    # (4) 每条 Active NFR 必有 Verification
    for nfr in nfr_section.all_active_nfrs():
        if not nfr.verification:
            failures.append(f"{nfr.id} Verification 字段空白")
    
    # (5) Brownfield 模式：每条 NFR 必有 Delta Operation
    if project_mode in ('Brownfield', 'Hybrid'):
        for nfr in nfr_section.all_nfrs():
            if not nfr.delta_operation:
                failures.append(f"{nfr.id} 缺 Delta Operation 字段（Brownfield 必填）")
    
    # (6) §10.7 路由表与 §10.1~§10.6 一致
    table_ids = set(nfr_section.routing_table_ids())
    section_ids = set(nfr.id for nfr in nfr_section.all_nfrs())
    if table_ids != section_ids:
        failures.append(f"路由表 ↔ 各类 NFR 不一致：差集 {table_ids ^ section_ids}")
    
    # (7) tasks.md 至少有 1 个 Task 引用每条 Active NFR（需要 cross-file 检查）
    # 略 — 实施时跨文件解析 tasks.md
    
    return failures
```

---

## 5. 修订规则

- 本文件修订必须同 PR 修订 `../../../asset-quality-gates/references/checks-catalog.md §3.1 R-CHK-EX-1.8` + `README.md`。
- 不允许"看似失败但 checker 能 hack 通过"：A 类必须真留空（不是隐藏在 HTML 注释里有声明），B 类必须真缺字段（不是字段顺序问题）。
- 新增 NFR 失败模式（如某类专项 workflow 路由错配 / NFR 与 task 引用断裂）→ 新建 `F-FIX-9` 或本 fixture 加子 fixture C，不在 A/B 上扩展。
