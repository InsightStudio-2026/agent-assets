# Expected Failure · F-FIX-4

> 期望 `/asset-quality-gates` Phase 3.6 对本 fixture 的识别结果。

---

## 1. 期望失败信号

| 字段 | 期望值 |
| ------ | -------- |
| Final state | `CHECKS_FAILED_NEEDS_REVISION` |
| 命中规则 | `R-CHK-EX-1.4 active/done 状态漂移` |
| 严重性 | High |
| 失败位置 | `spec.md` §4 + §5.3 + §6 |

---

## 2. 期望报告内容

```markdown
## R-CHK-EX-1.4 active/done 状态漂移 · F-FIX-4

- **严重程度 (Severity)**: High
- **审计发现 (Findings)**:
  - **Mode A**: §4 TASK-3 `Status: Done` 与 §5.3 e2e `FAIL` 矛盾（Done task 不可能 verification FAIL）
  - **Mode B**: §4 TASK-4 `Status: Pending` 与 §6 spec Status `Done` 矛盾（spec Done 不可能存在 Pending task）
- **预期要求 (Expected)**: tasks Status / verification 结果 / spec close-out Status 三者一致；任一不一致即命中
- **处置动作 (Action)**: BLOCK spec close-out until status drift resolved

```

---

## 3. 误识别（不应命中）

| 规则 | 不应误命中原因 |
| ------ | --------------- |
| `R-CHK-EX-1.1` | 本 fixture 是 Greenfield；delta operation 不适用 |
| `R-CHK-EX-1.2` | `Derived From` 字段保留 |
| `R-CHK-EX-1.3` | 本 fixture 不复制 archive.md |
| `R-CHK-EX-1.7` | TASK-1~4 都有 Verification 字段（即使 e2e FAIL，字段本身存在） |

---

## 4. checker 实现提示

| 检测点 | 检测方式 |
| -------- | --------- |
| Mode A | 解析 §4 Tasks 表 + §5.3 Verification 结果表；对每个 TASK，匹配 verification 命令 → verification 结果行；如 Status=Done 且对应行 PASS≠所有，命中 |
| Mode B | 解析 §4 Tasks Status 列 + §6 Spec Status；如 spec Status=Done 但任一 TASK Status≠Done（Pending / Blocked / In Progress）即命中 |
| 报告精度 | 必须列出每个矛盾 TASK ID + 矛盾位置 |
