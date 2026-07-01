---
name: 文档编写
description: 当用户编写文档、README、技术方案、设计文档、ADR 或项目说明时自动加载。编辑 .md 文件时也自动加载。
applyTo: '**/*.md'
---

# 文档编写规范

> 编辑 Markdown 文档或涉及文档编写任务时自动加载。本文档是文档体系与命名纪律的权威 SSOT。

## 1. 目录体系

### 1.1 三层布局

文档体系按 **L1 战略 SSOT / L2 执行合同 / L3 交付归档** 三层组织。

| 层级 | 路径 | 职责 |
| ---- | ---- | ---- |
| L1 | `docs/blueprints/` | 母本、路线图、主文档 |
| L2 | `docs/specs/active/<feature-slug>/` | Feature spec 合同（进行中） |
| L3 | `docs/specs/done/<feature-slug>/` | Feature 合同归档（完结后 `git mv` 至此） |
| — | `docs/specs/project archives/delivery-log.md` | 工程交付台账（每完成一个 feature 追加一行） |
| — | `docs/todo.md` | 个人待办 |
| — | `docs/notes/` | 零散开发笔记 |
| — | `docs/idea/` | 想法孵化草稿 |
| — | `docs/archives/` | 旧版历史快照（只读） |
| — | `docs/assets/` | 元协议、产品知识库、法律文件 |
| — | `.github/instructions/` | 工程规范 |
| — | `.github/experience/` | 项目运行教训（由 `operational-learnings` skill 管理） |

### 1.2 命名与维护纪律

- **子目录名**：小写英文（`blueprints/`、`specs/`、`archives/`、`assets/`、`notes/`、`idea/`）
- **内容文档名**：优先中文；feature-slug 用 kebab-case、不含日期；文件名不含空格，用 `-` 分隔
- **同源不复制**：一个事实只在一个 SSOT 里定义，其他文档用相对路径 + 锚点引用
- **归档不反流**：`docs/specs/done/` 与 `docs/archives/` 的内容不得被"返工"；需迭代走 `docs/specs/active/<feature-slug>/` 阶段迭代 + 新增交付记录一条
- **顶层不滥增**：`docs/` 顶层 `.md` 仅限 `todo.md`；新需求进 `docs/specs/active/<feature-slug>/`；L1 主文档进 `docs/blueprints/`；工程规范进 `.github/instructions/`；元协议/产品知识库进 `docs/assets/`
- **active → done 单向流转**：feature 完结后 `git mv` 到 `done/`，同步刷新跨文档引用；同时在 `docs/specs/project archives/delivery-log.md` 追加一条交付记录

### 1.3 新增文档决策流

1. **L1 SSOT？** → `docs/blueprints/`
2. **Feature 合同？** → `/specs-write` → `docs/specs/active/<slug>/`
3. **Feature 完结归档？** → `git mv` 到 `docs/specs/done/<slug>/` + 在 `docs/specs/project archives/delivery-log.md` 追加交付记录
4. **工程规范？** → `.github/instructions/`
5. **运行教训/踩坑经验？** → `.github/experience/`（由 `operational-learnings` skill 管理生命周期）
6. **元规则/法律政策？** → `docs/assets/`
7. **历史快照？** → `docs/archives/`（只读）
8. **笔记/草稿？** → `docs/notes/` 或 `docs/idea/`

不属于任何类别 → **不建**。

## 2. 文件与标题结构

### 2.1 MD041 — 每文件必须以 H1 开头

文件第一行必须是一个 `#` 一级标题（YAML front matter 除外）。

```markdown
<!-- ✅ 正确：无 front matter -->
# 文档标题

正文内容。

<!-- ✅ 正确：有 front matter -->
---
description: 文档说明
---

# 文档标题

## 第一节

<!-- ❌ 错误：以正文开头 -->
正文内容没有标题。

<!-- ❌ 错误：以 H2 开头 -->
## 二级标题开头
```

### 2.2 MD025 — 每文档仅一个一级标题

`#` 只在文件最顶部用一次，后续全部用 `##` 及更深层级。

### 2.3 MD001 — 标题层级不允许跳级

从 `#` 往下只能 h1 → h2 → h3 → ...，不允许 h1 → h3 跳过 h2。

### 2.4 MD024 — 全文禁止重复标题

同一文档内任意位置的标题文字不得重复（严格模式，`siblings_only: false`）。

### 2.5 MD036 — 禁止用粗体模拟标题

用 `##` 而非 `**文字**` 做标题。

```markdown
<!-- ❌ 错误：粗体代标题 -->
**注意事项**

<!-- ✅ 正确：使用标准标题 -->
## 注意事项
```

### 2.6 MD026 — 标题不得以标点结尾

```markdown
<!-- ❌ 错误 -->
## 步骤：
### 注意事项。

<!-- ✅ 正确 -->
## 步骤
### 注意事项
```

## 3. 空行与间距

### 3.1 MD022 — 标题前后必须有空行

```markdown
<!-- ✅ 正确 -->
上文段落。

## 标题

下文段落。

<!-- ❌ 错误 -->
上文段落。
## 标题
下文段落。
```

### 3.2 MD031 — 围栏代码块前后必须有空行

````markdown
上文段落。

```python
print("hello")
```

下文段落。
````

### 3.3 MD032 — 列表前后必须有空行

```markdown
<!-- ✅ 正确 -->
这是上文。

- 列表项 1
- 列表项 2

这是下文。

<!-- ❌ 错误 -->
这是上文。
- 列表项 1
- 列表项 2
这是下文。
```

### 3.4 MD012 — 不得连续多个空行

最多允许 1 个连续空行。

### 3.5 MD028 — 块引用内不得有空行

### 3.6 MD009 — 行末不得有空格

## 4. 代码块

### 4.1 MD040 — 围栏代码块必须标注语言

````markdown
❌ ```           （缺语言标识）
✅ ```python
✅ ```markdown
✅ ```json
✅ ```text        （纯文本用 text）
````

无法推断语言的统一标注 `text`。专用修复工具：`fix_md040.py`（见 §9.1）。

### 4.2 MD046 — 代码块必须围栏式

项目配置强制所有代码块使用 ```` ``` ```` 围栏，禁止 4 空格缩进风格。

### 4.3 闭合围栏不得带语言标识

> **严重性：高。** 这是经项目实测确认的破坏性缺陷。

代码块的结束围栏只能是 ```` ``` ````（纯反引号），绝对不能写成 ```` ```text ````、```` ```python ```` 等形式。渲染器会将带语言标识的闭合围栏误判为新代码块的开头，导致后续标题和段落全部被吞入代码块而失效。

````markdown
<!-- ✅ 正确：开围栏标注语言，闭合围栏纯反引号 -->
```python
print("hello")
```

<!-- ❌ 错误：闭合围栏带语言标识（后续内容会消失） -->
```python
print("hello")
```

## 这个标题会消失
````

## 5. 行内格式

### 5.1 MD037 — 强调标记内不得有空格

```markdown
✅ **粗体**    ✅ *斜体*    ✅ ***粗斜体***
❌ ** 粗体 **  ❌ *斜体*    ❌ **粗斜体**
```

### 5.2 MD038 — 行内代码标记内不得有空格

```markdown
✅ `code`
❌ ` code `
```

### 5.3 MD034 — 裸 URL 用尖括号包裹

```markdown
❌ https://example.com
✅ <https://example.com>
```

## 6. 列表

### 6.1 MD007 — 无序列表缩进 2 空格

嵌套列表逐级 +2 空格。

```markdown
<!-- ✅ 正确 -->
- 一级
  - 二级
    - 三级

<!-- ❌ 错误：缩进不一致 -->
- 一级
   - 二级（3 空格，不是 2）
```

列表前后空行见 §3.3（MD032）。

## 7. 表格

### 7.1 MD055 — 表格行首尾必须有管道 `|`

### 7.2 MD058 — 表格后必须有空行

### 7.3 MD060 — 表格管道两侧空格

管道 `|` 两侧必须有一个空格。对齐线也必须管道两侧有空格。

````markdown
<!-- ✅ 正确 -->
| 列A | 列B | 列C |
| --- | --- | --- |
| a   | b   | c   |

<!-- ❌ 错误：管道两侧缺空格 -->
|列A|列B|列C|
|---|---|---|
|a|b|c|
````

专用修复工具：`fix_md060.py`（见 §9.1）。当前项目统一采用两端空格风格。

## 8. 特殊场景

### 8.1 HTML 与模板占位符（MD033）

**绝对禁止在 Markdown 中内嵌 HTML 标签。** 所有样式、结构必须走标准 MD 语法。

模板占位符（如 `<feature-slug>`、`<name>`、`<YYYY-MM-DD>`）必须包裹为行内代码：

```markdown
<!-- ❌ 错误：裸占位符被识别为 HTML -->
路径：docs/specs/active/<feature-slug>/

<!-- ✅ 正确：包裹为行内代码 -->
路径：`docs/specs/active/<feature-slug>/`
```

路径型占位符应合并进同一个代码块，不要拆分：

```markdown
<!-- ✅ 正确：完整路径合并 -->
`docs/specs/active/<feature-slug>/`

<!-- ❌ 错误：拆成多个代码块 -->
`docs/specs/active/`<feature-slug>`/`
```

> **反引号相邻占位符反模式**（项目高频缺陷——曾出现 40+ 处）：当占位符 `<tag>` 夹在两个行内代码之间时，简单正则无法匹配。如 `` `prefix/<slug>/suffix` `` → 应合并为 `` `prefix/<slug>/suffix` ``。专用修复工具 `fix_md033.py` 采用三遍策略（合并→包裹→后处理）自动处理此模式。

### 8.2 含空格占位符

`fix_md033.py` 正则不匹配含空格的标签（如 `<Feature Name>`、`<ISO timestamp>`），必须手动包裹：

```markdown
<!-- ❌ 错误：含空格的裸占位符 -->
## Charter — <Feature Name>

<!-- ✅ 正确：整个标签包裹为行内代码 -->
## Charter — `<Feature Name>`
```

### 8.3 模板文件标题约定

模板文件（如 `templates/*.md`）存在两个标题需求：模板说明 + 占位标题。必须严格遵守 MD041 + MD025：

```markdown
<!-- ✅ 正确：模板说明为 H1，占位标题为 H2 -->
# audit.md 模板

> 模板使用说明...

## Spec Derivation Audit — `<Feature Name>`

<!-- ❌ 错误：两个 H1（违反 MD025） -->
# audit.md 模板
# Spec Derivation Audit — <Feature Name>

<!-- ❌ 错误：模板说明为 H2（违反 MD041） -->
## audit.md 模板
## Spec Derivation Audit — <Feature Name>
```

### 8.4 表格内 `<br>` 换行

`<br>` / `<br/>` 是 Markdown 表格内换行的唯一标准手段。项目在 `.markdownlint.json` 中配置了白名单豁免：

```json
"MD033": { "allowed_elements": ["br"] }
```

因此表格内可直接使用 `<br>` 或 `<br/>`，无需包裹为行内代码。其他 HTML 标签仍然禁止。

```markdown
<!-- ✅ 正确：<br/> 在白名单内 -->
| 列 | 内容 |
| -- | ---- |
| A  | 行1<br/>行2 |

<!-- ❌ 错误：其他 HTML 标签仍被拦截 -->
| A  | <div>内容</div> |
```

### 8.5 嵌套反引号处理

当行内代码内容本身含反引号时，用双反引号作为定界符，并清除内层反引号：

```markdown
<!-- ❌ 错误：单反引号内嵌反引号产生嵌套 -->
`curl -H 'Authorization: `<REDACTED>`'`

<!-- ✅ 正确：双反引号定界，内层去掉反引号 -->
``curl -H 'Authorization: <REDACTED>'``
```

双反引号代码块首尾不得有空格，否则触发 MD038。

## 9. 验证与自动修复

### 9.1 工具矩阵

项目提供统一 Lint 入口 `.github/tools/lint/lint.ps1`：

```powershell
.github\tools\lint\lint.ps1 check          # 运行 markdownlint 检查
.github\tools\lint\lint.ps1 fix-all        # 全自动修复管线（推荐）
.github\tools\lint\lint.ps1 fix-md033      # 仅修复 MD033（模板占位符）
.github\tools\lint\lint.ps1 fix-md040      # 仅修复 MD040（代码块语言）
.github\tools\lint\lint.ps1 fix-md060      # 仅修复 MD060（表格管道间距）
```

### 9.2 `fix-all` 管线

按正确顺序执行六步：

1. `markdownlint --fix` — 自动修复空格/空行/缩进（MD009/MD012/MD022/MD031/MD032/MD037/MD038/MD058）
2. `fix_md033.py` — 三遍策略修复模板占位符
3. `fix_md040.py` — 推断并标注代码块语言
4. `fix_md060.py` — 统一表格管道间距
5. `markdownlint --fix` — 二次清理脚本副作用
6. 最终验证 — 输出剩余需手动处理的条目

### 9.3 IDE 保存时自动修复

`.vscode/settings.json` 已配置：

```json
{
  "editor.codeActionsOnSave": {
    "source.fixAll.markdownlint": "explicit"
  }
}
```

按 `Ctrl+S` 即可自动修复所有可自动修复的格式问题。

### 9.4 自动修复与需人工判断对照表

| 自动修复（`--fix`） | 需人工判断或专用工具 |
| ------------------- | -------------------- |
| MD009 行末空格 | MD001 标题跳级 |
| MD012 连续多空行 | MD007 列表缩进不一致 |
| MD022 标题前后空行 | MD024 全文重复标题 |
| MD031 围栏代码块前后空行 | MD025 多个一级标题 |
| MD032 列表前后空行 | MD026 标题尾随标点 |
| MD034 裸 URL 包裹 | MD033 内嵌 HTML（专用 `fix_md033.py`） |
| MD037 强调标记内空格 | MD036 粗体/斜体代标题 |
| MD038 行内代码空格 | MD040 代码块缺语言（专用 `fix_md040.py`） |
| MD058 表格后空行 | MD041 文件必须以 H1 开头 |
| MD060 表格管道空格（专用 `fix_md060.py`） | MD046 缩进代码块→围栏 |

### 9.5 命令行直接使用

```powershell
# 全量检查
npx markdownlint-cli2 "**/*.md"

# 自动修复
npx markdownlint-cli2 --fix "**/*.md"
```
