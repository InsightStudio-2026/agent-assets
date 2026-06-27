# PreToolUse Safety Guard Hook
# 仅拦截真正不可逆的灾难性操作
# 退出码 2 = 阻止执行，0 = 允许

param(
    [Parameter(ValueFromPipeline=$true)]
    [string]$InputJson
)

$hookData = $InputJson | ConvertFrom-Json
$toolName = $hookData.tool_name
$toolInput = $hookData.tool_input | ConvertTo-Json -Depth 3 -Compress

# 危险模式列表（仅保留不可逆数据破坏操作）
$dangerousPatterns = @(
    'rm\s+-rf',
    'DROP\s+TABLE',
    'DROP\s+DATABASE',
    'TRUNCATE\s+TABLE',
    'git\s+push\s+--force'
)

foreach ($pattern in $dangerousPatterns) {
    if ($toolInput -match $pattern) {
        $result = @{
            continue      = $false
            stopReason    = "检测到危险命令模式: $pattern"
            toolName      = $toolName
            systemMessage = '操作被安全钩子拦截。如需执行，请手动确认。'
        }
        Write-Output ($result | ConvertTo-Json -Compress)
        exit 2
    }
}

# 允许执行
exit 0