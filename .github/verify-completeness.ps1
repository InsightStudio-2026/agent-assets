# PowerShell Asset Index Verification Script
# Target: Verify Skills are correctly indexed in AGENTS.md
# OS: Windows 11

$ErrorActionPreference = "Stop"

Write-Host "=== Asset Index Verification ===" -ForegroundColor Cyan

$root = Get-Item .
$agentsPath = Join-Path $root.FullName "AGENTS.md"
$skillsDir = Join-Path $root.FullName ".github\skills"
$hasError = $false

if (-not (Test-Path $agentsPath)) { Write-Error "AGENTS.md is missing!"; exit 1 }

$physicalSkills = @()
if (Test-Path $skillsDir) {
    $physicalSkills = Get-ChildItem -Path $skillsDir -Recurse -Filter "SKILL.md" | ForEach-Object { $_.Directory.Name }
}
Write-Host "Found $($physicalSkills.Count) physical Skill(s)" -ForegroundColor Green

$agentsContent = Get-Content -Path $agentsPath -Raw
$registeredSkills = @()
$skillMatches = [regex]::Matches($agentsContent, "\[([a-zA-Z0-9\-]+?)\]\(\.github/skills/([a-zA-Z0-9\-]+?)/SKILL\.md\)")
foreach ($match in $skillMatches) { $registeredSkills += $match.Groups[2].Value }

$unindexed = @(); $stale = @()
foreach ($ps in $physicalSkills) { if ($registeredSkills -notcontains $ps) { $unindexed += $ps } }
foreach ($rs in $registeredSkills) { if ($physicalSkills -notcontains $rs) { $stale += $rs } }

if ($unindexed.Count -gt 0) { Write-Host "ERROR: Unindexed: $($unindexed -join ', ')" -ForegroundColor Red; $hasError = $true }
else { Write-Host "SUCCESS: All Skills correctly indexed" -ForegroundColor Green }
if ($stale.Count -gt 0) { Write-Host "ERROR: Stale entries: $($stale -join ', ')" -ForegroundColor Red; $hasError = $true }

Write-Host "`n=== Result ===" -ForegroundColor Cyan
if ($hasError) { Write-Host "FAILED" -ForegroundColor Red; exit 1 }
else { Write-Host "PASSED" -ForegroundColor Green; exit 0 }