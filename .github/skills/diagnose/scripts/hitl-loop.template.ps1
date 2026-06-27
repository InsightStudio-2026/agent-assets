# Human-in-the-loop reproduction loop.
# Copy this file, edit the steps below, and run it with PowerShell:
#   pwsh -File .\hitl-loop.template.ps1
#
# Two helpers:
#   Step "instruction"              shows an instruction and waits for Enter
#   Capture -Name VAR -Question Q   asks a question and stores the answer
#
# At the end, captured values are printed as KEY=VALUE for the agent to parse.

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$Captured = [ordered]@{}

function Step {
  param(
    [Parameter(Mandatory = $true)]
    [string]$Instruction
  )

  Write-Host ""
  Write-Host ">>> $Instruction"
  Read-Host "    Press Enter when done" | Out-Null
}

function Capture {
  param(
    [Parameter(Mandatory = $true)]
    [string]$Name,

    [Parameter(Mandatory = $true)]
    [string]$Question
  )

  Write-Host ""
  Write-Host ">>> $Question"
  $answer = Read-Host "    >"
  $script:Captured[$Name] = $answer
}

# --- edit below ---------------------------------------------------------

Step "Open the app at http://localhost:3000 and sign in."

Capture -Name "ERRORED" -Question "Click the 'Export' button. Did it throw an error? (y/n)"

Capture -Name "ERROR_MSG" -Question "Paste the error message (or 'none'):"

# --- edit above ---------------------------------------------------------

Write-Host ""
Write-Host "--- Captured ---"
foreach ($entry in $Captured.GetEnumerator()) {
  Write-Host "$($entry.Key)=$($entry.Value)"
}
