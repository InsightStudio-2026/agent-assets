<#
.SYNOPSIS
    Markdown Lint 工具集统一入口 —— 检查、修复、分析、压缩。

.DESCRIPTION
    用法：
        lint.ps1 check             运行 markdownlint-cli2 检查
        lint.ps1 fix [目录]         运行全部自动修复脚本（三步）
        lint.ps1 fix-all [目录]      修复管线：markdownlint --fix → 三步脚本 → 验证
        lint.ps1 fix-md033 [目录]   仅修复 MD033（模板占位符）
        lint.ps1 fix-md040 [目录]   仅修复 MD040（围栏代码块语言）
        lint.ps1 fix-md060 [目录]   仅修复 MD060（表格管道间距）
        lint.ps1 compress <json>    压缩 VS Code Problems JSON
        lint.ps1 analyze <json>     分析压缩后的问题 JSON
        lint.ps1 sample <json> <code> 抽样查看指定规则的违规

    示例：
        .\.github\tools\lint\lint.ps1 check
        .\.github\tools\lint\lint.ps1 fix-all              # 推荐：全自动修复管线
        .\.github\tools\lint\lint.ps1 fix docs/specs/
        .\.github\tools\lint\lint.ps1 compress "问题 copy.json"
        .\.github\tools\lint\lint.ps1 analyze "问题_压缩.json"
        .\.github\tools\lint\lint.ps1 sample "问题_压缩.json" MD033
#>

[CmdletBinding()]
param(
    [Parameter(Position = 0, Mandatory = $true)]
    [ValidateSet("check", "fix", "fix-all", "fix-md033", "fix-md040", "fix-md060",
                 "compress", "analyze", "sample")]
    [string]$Action,

    [Parameter(Position = 1)]
    [string]$Arg1,

    [Parameter(Position = 2)]
    [string]$Arg2
)

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Resolve-Path (Join-Path $ScriptDir "../../..")

function Invoke-PythonScript {
    param([string]$ScriptName, [string[]]$Arguments)
    $scriptPath = Join-Path $ScriptDir $ScriptName
    if (-not (Test-Path $scriptPath)) {
        Write-Error "脚本不存在: $scriptPath"
        exit 1
    }
    $argsStr = $Arguments -join " "
    python $scriptPath $argsStr
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
}

switch ($Action) {
    "check" {
        Push-Location $RepoRoot
        try {
            npx markdownlint-cli2 "**/*.md" 2>&1
        } finally {
            Pop-Location
        }
    }
    "fix" {
        $dir = if ($Arg1) { $Arg1 } else { $RepoRoot }
        Write-Host "=== 运行全部自动修复脚本 ===" -ForegroundColor Cyan
        Invoke-PythonScript "fix_md033.py" @($dir)
        Invoke-PythonScript "fix_md040.py" @($dir)
        Invoke-PythonScript "fix_md060.py" @($dir)
        Write-Host "`n完成后请运行 lint.ps1 check 验证" -ForegroundColor Yellow
    }
    "fix-all" {
        $dir = if ($Arg1) { $Arg1 } else { $RepoRoot }
        Write-Host "=== Phase 1/3: markdownlint --fix（自动修复空格/空行/缩进等）===" -ForegroundColor Cyan
        Push-Location $RepoRoot
        try {
            npx markdownlint-cli2 "**/*.md" --fix 2>&1 | Out-Null
        } finally {
            Pop-Location
        }
        Write-Host "=== Phase 2/3: 运行三步修复脚本（MD033/MD040/MD060）===" -ForegroundColor Cyan
        Invoke-PythonScript "fix_md033.py" @($dir)
        Invoke-PythonScript "fix_md040.py" @($dir)
        Invoke-PythonScript "fix_md060.py" @($dir)
        Write-Host "=== Phase 3/3: 最终验证 ===" -ForegroundColor Cyan
        Push-Location $RepoRoot
        try {
            $errors = (npx markdownlint-cli2 "**/*.md" 2>&1 | Select-String "error" | Measure-Object).Count
        } finally {
            Pop-Location
        }
        if ($errors -eq 0) {
            Write-Host "`n✓ 零错误 — 全部 Markdown 格式问题已修复" -ForegroundColor Green
        } else {
            Write-Host "`n✗ 剩余 $errors 条错误 — 可能需要手动处理（如 MD046 缩进代码块、MD001 标题层级等）" -ForegroundColor Yellow
        }
    }
    "fix-md033" {
        $dir = if ($Arg1) { $Arg1 } else { $RepoRoot }
        Invoke-PythonScript "fix_md033.py" @($dir)
    }
    "fix-md040" {
        $dir = if ($Arg1) { $Arg1 } else { $RepoRoot }
        Invoke-PythonScript "fix_md040.py" @($dir)
    }
    "fix-md060" {
        $dir = if ($Arg1) { $Arg1 } else { $RepoRoot }
        Invoke-PythonScript "fix_md060.py" @($dir)
    }
    "compress" {
        if (-not $Arg1) { Write-Error "用法: lint.ps1 compress <输入.json> [输出.json]"; exit 1 }
        $pyParams = @($Arg1)
        if ($Arg2) { $pyParams += $Arg2 }
        Invoke-PythonScript "compress_problems.py" $pyParams
    }
    "analyze" {
        if (-not $Arg1) { Write-Error "用法: lint.ps1 analyze <压缩后的JSON>"; exit 1 }
        Invoke-PythonScript "analyze_problems.py" @($Arg1)
    }
    "sample" {
        if (-not $Arg1 -or -not $Arg2) {
            Write-Error "用法: lint.ps1 sample <压缩后的JSON> <CODE>"
            exit 1
        }
        Invoke-PythonScript "analyze_problems.py" @($Arg1, "--sample", $Arg2)
    }
}
