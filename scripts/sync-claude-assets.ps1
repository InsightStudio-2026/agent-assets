# Sync Claude Code Assets from GitHub Copilot SSOT
# One-way mirror: .github/ (SSOT) -> .claude/ (derived)
# Run this script after any change to .github/skills/ or .github/instructions/
# OS: Windows 11 / PowerShell 7+
param(
    [switch]$WhatIf,
    [switch]$SkillsOnly,
    [switch]$RulesOnly
)

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$root = Split-Path -Parent $root  # Go up from scripts/ to project root

$githubSkills  = Join-Path $root ".github\skills"
$claudeSkills  = Join-Path $root ".claude\skills"
$githubInstructions = Join-Path $root ".github\instructions"
$claudeRules    = Join-Path $root ".claude\rules"

Write-Host "=== Sync Claude Code Assets ===" -ForegroundColor Cyan
Write-Host "SSOT: .github/  -->  Derived: .claude/" -ForegroundColor DarkGray
if ($WhatIf) { Write-Host "[WHAT-IF MODE] No changes will be made" -ForegroundColor Yellow }

# ============================================================
# Phase 1: Skills Mirror
# ============================================================
if (-not $RulesOnly) {
    Write-Host "`n--- Phase 1: Skills Mirror ---" -ForegroundColor Green

    if (-not (Test-Path $githubSkills)) {
        Write-Error ".github/skills/ not found at $githubSkills"
        exit 1
    }

    if (-not (Test-Path $claudeSkills)) {
        if (-not $WhatIf) { New-Item -ItemType Directory -Path $claudeSkills -Force | Out-Null }
    }

    # Get list of skill directories from SSOT
    $srcDirs = Get-ChildItem -Path $githubSkills -Directory | Select-Object -ExpandProperty Name
    $syncCount = 0

    foreach ($dirName in $srcDirs) {
        $srcDir  = Join-Path $githubSkills $dirName
        $destDir = Join-Path $claudeSkills $dirName

        if ($WhatIf) {
            Write-Host "  [WHAT-IF] Would sync: $dirName"
            $syncCount++
            continue
        }

        # Robust mirror: robocopy the entire skill directory
        robocopy $srcDir $destDir /MIR /NJH /NJS /NP /NDL /R:1 /W:1 | Out-Null
        # robocopy exit codes: 0-7 = success (0=no changes, 1=files copied, etc.)
        if ($LASTEXITCODE -ge 8) {
            Write-Warning "  robocopy failed for $dirName (exit code: $LASTEXITCODE)"
        } else {
            $syncCount++
        }
    }

    # Clean up: remove skills in .claude/skills/ that no longer exist in SSOT
    $destDirs = Get-ChildItem -Path $claudeSkills -Directory -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Name
    foreach ($dirName in $destDirs) {
        if ($dirName -notin $srcDirs) {
            $staleDir = Join-Path $claudeSkills $dirName
            if ($WhatIf) {
                Write-Host "  [WHAT-IF] Would remove stale: $dirName"
            } else {
                Write-Host "  Removing stale skill: $dirName" -ForegroundColor DarkYellow
                Remove-Item -Path $staleDir -Recurse -Force
            }
        }
    }

    Write-Host "  Skills synced: $syncCount / $($srcDirs.Count)" -ForegroundColor Green
}

# ============================================================
# Phase 2: Rules Auto-Generation
# ============================================================
if (-not $SkillsOnly) {
    Write-Host "`n--- Phase 2: Rules Auto-Generation ---" -ForegroundColor Green

    if (-not (Test-Path $githubInstructions)) {
        Write-Error ".github/instructions/ not found at $githubInstructions"
        exit 1
    }

    if (-not (Test-Path $claudeRules)) {
        if (-not $WhatIf) { New-Item -ItemType Directory -Path $claudeRules -Force | Out-Null }
    }

    $instructionFiles = Get-ChildItem -Path $githubInstructions -Filter "*.instructions.md"
    $ruleCount = 0

    foreach ($srcFile in $instructionFiles) {
        # Derive .claude/rules/ filename: strip ".instructions" suffix
        $ruleName = $srcFile.Name -replace "\.instructions\.md$", ".md"
        $destPath = Join-Path $claudeRules $ruleName

        # Read source content
        $rawContent = Get-Content -Path $srcFile.FullName -Raw -Encoding UTF8

        # Parse YAML frontmatter (between --- delimiters, multi-line)
        if ($rawContent -match '(?s)^---\s*\r?\n(.*?)\r?\n---\s*\r?\n(.*)$') {
            $frontmatterBlock = $matches[1]
            $body = $matches[2]
        } else {
            Write-Warning "  Skipping $($srcFile.Name): no YAML frontmatter found"
            continue
        }

        # Transform frontmatter for Claude Code compatibility:
        #   applyTo: "**/*.py"  -->  paths: ["**/*.py"]
        #   applyTo: '**/*.py'  -->  paths: ["**/*.py"]
        # Keep name: and description: (harmless for Claude Code, improves logs).
        # Remove applyTo: after conversion to avoid confusing Claude Code.
        $frontmatterBlock = $frontmatterBlock -replace '(?m)^applyTo:\s*"(.*)"\s*$', 'paths: ["$1"]'
        $frontmatterBlock = $frontmatterBlock -replace "(?m)^applyTo:\s*'(.*)'\s*$", 'paths: ["$1"]'

        # Remove other Copilot-specific fields that Claude Code ignores
        $frontmatterBlock = $frontmatterBlock -replace '(?m)^argument-hint:.*\r?\n?', ''
        $frontmatterBlock = $frontmatterBlock -replace '(?m)^disable-model-invocation:.*\r?\n?', ''
        $frontmatterBlock = $frontmatterBlock -replace '(?m)^handoffs:.*\r?\n?', ''

        # Clean up: remove leading/trailing blank lines from frontmatter
        $frontmatterBlock = $frontmatterBlock -replace '(?m)^\s*\r?\n', ''
        $frontmatterBlock = $frontmatterBlock.Trim()

        # Assemble Claude Code rule file with proper YAML frontmatter formatting
        $frontmatterBlock = $frontmatterBlock.Trim()
        $output = "---`n${frontmatterBlock}`n---`n`n${body}"

        if ($WhatIf) {
            Write-Host "  [WHAT-IF] Would generate: $ruleName"
            $ruleCount++
            continue
        }

        # Write as UTF-8 (no BOM needed for Claude Code rules which are plain markdown)
        $utf8NoBom = New-Object System.Text.UTF8Encoding $false
        [System.IO.File]::WriteAllText($destPath, $output, $utf8NoBom)
        $ruleCount++
    }

    Write-Host "  Rules generated: $ruleCount / $($instructionFiles.Count)" -ForegroundColor Green
}

Write-Host "`n=== Sync Complete ===" -ForegroundColor Cyan
