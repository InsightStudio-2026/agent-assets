---
name: 测试驱动开发
description: 当用户编写测试、运行测试、讨论测试策略、要求 TDD 或修复测试失败时自动加载。不依赖文件匹配，仅凭任务语义触发。
applyTo: '**/*.{test,spec}.{py,ts,tsx,js,jsx}'
---

# 测试驱动开发 (TDD) 与任务完成门禁

> 当任务涉及测试编写、测试策略或 TDD 流程时自动加载。本文档是任务完成门禁 (DoD) 的权威 SSOT。

## TDD 循环（不可跳步）

1. **Red**：先写失败测试，确认测试确实失败
2. **Green**：最小实现让测试通过
3. **Refactor**：清理代码，保持测试绿色

## 可验证目标

模糊任务必须转成可验证目标：

- "加校验" → "为非法输入写测试，让测试通过"
- "修 Bug" → "写复现测试，让它通过"

## 测试覆盖要求

- 代码入口面必须有对应测试覆盖
- Bug 修复必须先补齐复现测试
- 新功能必须有验收测试
- Contract / API 变更必须有 OpenAPI spec 冻结验证

---

## DoD 门禁（Definition of Done）

> 在标记任何子任务为完成前，必须逐项通过本门禁检查，禁止跳过。

### 1. 双层 DoD 机制

- **合同层**：feature 级 `tasks.md §5` 规定——REQ 全覆盖 + Acceptance Test 通过 + TDD 闭环。
- **命令层**：以下自动化校验命令。`/specs-execute` Phase 7 必须通过双层 DoD。

### 2. 前端 DoD (TypeScript / React Native)

- **静态检查**：ESLint 0 warnings / 0 errors；Prettier 格式 100% 匹配。
- **类型系统**：TypeScript 0 compilation errors。
- **功能验证**：Jest 单元测试套件全量通过。

```powershell
npx eslint . --max-warnings 0
npx prettier --check .
npx tsc --noEmit
npx jest --no-coverage --verbose
```

### 3. 后端 DoD (Python / FastAPI)

- **静态检查**：Ruff "All checks passed!"，无残留告警。
- **功能验证**：pytest 0 failures / 0 errors。

```powershell
.\venv\Scripts\python.exe -m ruff check .
.\venv\Scripts\python.exe -m pytest tests/ -v --tb=short
```

### 4. Schema 变更 DoD（14 层 Drift 防线）

> **铁律**：任何数据库 Schema/ORM/索引/CHECK/触发器/视图变更，完成前必须跑 14 层 ALL GREEN。

Schema 变更 SOP 详见 `@.github/instructions/database.instructions.md`。

### 5. 占位符禁令

源文件中绝对禁止以下占位符：

- JS/TS: `// ... existing code ...` · `/*...*/` · `// rest unchanged`
- Python: `# ... existing code ...` · `# (省略)` · `pass  # TODO 填充`
- SQL: `-- ... unchanged ...` · `-- (rest)`
- YAML/JSON: `# ... 原有配置保留 ...`
- Markdown: `<填入其他代码>` · `<原有内容保留>`

### 6. 任务结束清理

- 删除 `debug_*.py` · `test_scratch.*` 等一次性调试脚本。
- 删除代码中残留的 `console.log()` / `print()` 调试语句。
- 删除注释掉的大段废弃代码。
- 将所有 `@ts-ignore` 替换为 `@ts-expect-error`。

### 7. 完成声明格式

**通用任务**：

```markdown
✅ DoD 检查通过

- ESLint:       0 warnings
- Prettier:     通过
- TypeScript:   0 errors
- Jest:         XX/XX 通过
- Ruff:         通过
- pytest:       XXX passed
- 清理检查:     已完成

```

**Schema 相关任务**（追加 Drift 防线）：

```markdown
✅ DoD 检查通过（命令同上）
✅ Drift 防线 14 层全绿
  [D1] migration runner verify         ✓
  [D1+] migration timestamp uniqueness  ✓
  [D2.1] schema.sql ↔ ORM (postgres)    ✓
  ...（全部 14 层）
后端测试:   XXX passed / 0 failed
```
