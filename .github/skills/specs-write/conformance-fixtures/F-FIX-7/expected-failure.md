# Expected Failure · F-FIX-7

> 期望 `/asset-quality-gates` Phase 3.6 对本 fixture 的识别结果。

---

## 1. 期望失败信号

| 字段 | 期望值 |
| ------ | -------- |
| Final state | `CHECKS_FAILED_NEEDS_REVISION` |
| 命中规则 | `R-CHK-EX-1.7 verification missing` |
| 严重性 | **Critical** |
| 失败位置 | `tasks.md` TASK-3 / TASK-4 / TASK-5 |

---

## 2. 期望报告内容

```markdown
## R-CHK-EX-1.7 verification missing · F-FIX-7

-**严重程度 (Severity)**: Critical

- **审计发现 (Findings)**:
  - **Mode A**: TASK-3 `Status: Done` 但 `Verification:` 列空白 → 无法验证 callback handler 是否真实测试通过
  - **Mode B**: TASK-5 `Status: Done` 但 `Artifacts:` 列空白 → 无 e2e screenshot / 测试日志，UI 交付证据缺失
  - **Mode C**: TASK-4 `Artifacts:` 引用 `artifacts/account-resolver-NONEXISTENT.log` 不存在 → 引用失效
- **预期要求 (Expected)**: 每个 `Status: Done` Task 必有：(1) 非空 `Verification:` 命令字段；(2) 非空 `Artifacts:` 字段；(3) Artifacts 引用文件实际存在（fixture 目录或 spec 目录可访问）
- **处置动作 (Action)**: BLOCK spec close-out + REQUIRE Done Task verification evidence

```

---

## 3. 误识别（不应命中）

| 规则 | 不应误命中原因 |
| ------ | --------------- |
| `R-CHK-EX-1.4 active/done 状态漂移` | 本 fixture Status 与 verification 结果未矛盾（仅缺字段，不存在 PASS/FAIL 矛盾） |
| `R-CHK-EX-1.5 INV violation` | 本 fixture 不引入违反 INV 的字段或依赖 |
| `R-CHK-EX-1.6 out-of-charter` | 所有 task 仍在 Google OAuth scope 内，未越界 |

---

## 4. checker 实现提示

| 检测点 | 检测方式 |
| -------- | --------- |
| Mode A 缺 Verification 字段 | 解析 tasks 表，对每个 `Status: Done` 的行，检查 `Verification:` 列是否非空且包含可执行命令（如 `pnpm`、`pytest`、`npm test` 等关键字） |
| Mode B 缺 Artifacts 字段 | 同上检查 `Artifacts:` 列非空 |
| Mode C Artifacts 文件不存在 | 解析 Artifacts 列引用的相对路径，相对 fixture 目录或 spec 目录做 stat 检查；不存在即命中 |
| 严重性 = Critical | Verification 是 Done 的硬证据，缺失 = 伪 Done = 项目交付权利链断裂 |
| 误命中防御 | `Status: Pending / In Progress / Blocked` 的 Task 不要求 Verification / Artifacts 字段；只检查 Done |
