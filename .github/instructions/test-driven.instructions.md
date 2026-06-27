---
name: 测试驱动开发
description: 当用户编写测试、运行测试、讨论测试策略、要求 TDD 或修复测试失败时自动加载。不依赖文件匹配，仅凭任务语义触发。
applyTo: '**/*.{test,spec}.{py,ts,tsx,js,jsx}'
---

# 测试驱动开发 (TDD) 与任务完成门禁

> 当任务涉及测试编写、测试策略或 TDD 流程时自动加载。本文档是任务完成门禁 (DoD) 的权威 SSOT。

## 0. 微闭环自愈协议（Micro-Closed-Loop Self-Healing）

> **铁律**：任何代码变更完成后，必须通过终端运行自动化验证套件并显式检查 `$LASTEXITCODE`。若 `$LASTEXITCODE` 非 0（即测试/构建/静态分析失败），禁止向人类请求帮助——你必须自行分析 stderr 与 traceback，并至少自我重试修正 3 轮。仅当连续 3 轮自我修正仍失败，或遇到需要底层架构决断的阻塞时，才能暂停并请求 Vibe 协同。

### 0.1 执行-捕获-修正循环

在任何 Python 后端逻辑或 C# 端点完成后，AI 必须：

1. **生成对应的测试脚本**（或调用已有的测试套件）。
2. **通过终端运行**测试并显式检查 `$LASTEXITCODE`——若该变量非 0，本次修改未完成。
3. **禁止向人类请求帮助**：测试失败、构建失败、静态分析告警均不属于 Pause-and-Ask 白名单场景（详见 `@.github/instructions/rules.instructions.md#13-pause-and-ask-白名单收窄`）。
4. **自主分析** stderr 与 traceback，定位根因后修正代码——不得以扩大 catch、吞错、重试、降级、兼容别名、特殊 case 叠加等方式治标。
5. **至少自我重试 3 轮**，每轮必须变更策略（非机械重复同一修复）。
6. **升级路径**：连续 3 轮仍失败后，触发 `/diagnose` 深度诊断而非直接求助用户；若诊断后判定需要架构决断（如 schema 契约变更、新依赖引入、跨模块重构），才暂停并请求 Vibe 协同。

### 0.2 跨语言 DoD 命令

- **Python**：`python -m pytest --tb=short` + `ruff check`
- **TypeScript/JS**：`npx jest --no-coverage` + `npx eslint` + `npx tsc --noEmit`
- **PowerShell**：`Invoke-ScriptAnalyzer -Path <file>` + 显式 `exit 0/1`

任何 DoD 命令执行后必须读取输出，确认 0 错误 / 0 失败 / 0 告警，方可宣告完成。

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
