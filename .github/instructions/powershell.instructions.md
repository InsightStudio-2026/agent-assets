---
name: PowerShell 脚本规范
description: PowerShell 脚本代码风格与安全约束。编辑 .ps1/.psm1 文件时自动加载。
applyTo: '**/*.{ps1,psm1}'
---

# PowerShell 脚本开发规范

> 编辑 PowerShell 脚本时自动生效。本文档是 PS 代码风格的权威 SSOT。

## 1. 自动化检查与修复

**验证检查**：

```powershell
Invoke-ScriptAnalyzer -Path . -Recurse
```

**创建/编辑 .ps1 后的自检纪律**：

```powershell
## 编辑 .ps1 后必须运行，创建 .ps1 后必须运行：
Invoke-ScriptAnalyzer -Path <文件路径>
```

**PSScriptAnalyzer 关键规则速查**：

| 规则 | 说明 | 修复方式 |
| ------ | ------ | ---------- |
| PSAvoidAssignmentToAutomaticVariable | 禁止赋值给自动变量（`$args`、`$event` 等） | 改用自定义变量名 |
| PSUseDeclaredVarsMoreThanAssignments | 声明的变量必须被使用 | 删除未使用变量或补全使用 |
| PSAvoidUsingCmdletAliases | 禁止使用别名（`dir`→`Get-ChildItem`） | 使用完整 Cmdlet 名称 |
| PSUseApprovedVerbs | Cmdlet 动词必须来自批准列表 | 使用 `Get-Verb` 查批准动词 |
| PSAvoidUsingWriteHost | 禁止 `Write-Host`（数据流污染） | 改用 `Write-Output` |
| PSProvideCommentHelp | 脚本/函数需注释帮助 | 添加 `<# .SYNOPSIS #>` 块 |

## 2. 命名与风格

- **变量命名**：`$camelCase` 私有变量，`$PascalCase` 参数和全局变量。
- **禁止别名**：禁止使用 `dir`、`ls`、`echo`、`%`、`?` 等别名，始终使用完整 Cmdlet 名称。
- **函数动词**：自定义函数使用批准的 PowerShell 动词（`Get-`、`Set-`、`New-`、`Remove-`、`Invoke-` 等）。
- **参数块**：每个脚本和函数必须有 `param()` 块声明参数，带类型约束。
- **字符串安全**：需要变量插值时使用双引号 `"..."`，纯字面量使用单引号 `'...'`。
- **输出纪律**：使用 `Write-Output` 写数据，`Write-Error` 写错误，`Write-Information` 写信息。禁止用 `Write-Host` 传递数据。
- **错误处理**：顶部设置 `$ErrorActionPreference = 'Stop'`，关键操作使用 `try/catch`。

### 2.1 安全编码

- **路径拼接**：始终使用 `Join-Path`，禁止字符串拼接路径。
- **Shell 执行**：避免 `Invoke-Expression`；优先使用 `Start-Process` 或直接调用可执行文件。
- **输入验证**：外部输入使用 `[ValidateSet()]`、`[ValidatePattern()]` 等特性约束。
- **清理**：删除临时文件、注释掉的代码、调试用 `Write-Host` 语句。

## 3. 项目约定

- **中文化**：脚本注释、错误消息使用中文。变量名使用英文。
- **编码**：所有 `.ps1` 文件保存为 UTF-8 with BOM（VS Code 默认）。
- **退出码**：明确设置 `exit 0`（成功）、`exit 1`（失败）、`exit 2`（安全拦截）。
- **幂等性**：脚本应支持重复运行而不产生副作用。
- **依赖声明**：顶部 `#Requires` 注释声明最低 PowerShell 版本和所需模块。
