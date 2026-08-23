$ErrorActionPreference = "Stop"

try {
    $inputJson = [Console]::In.ReadToEnd() | ConvertFrom-Json
    $toolName = $inputJson.tool_name
    $command = [string]$inputJson.tool_input.command

    if ($toolName -notin @("Bash", "PowerShell")) {
        exit 0
    }

    $dangerousPatterns = @(
        'rm\s+-rf',
        'Remove-Item\b.*-Recurse',
        'Remove-Item\b.*-Force',
        'git\s+push\s+--force',
        'git\s+push\s+-f(?:\s|$)',
        'DROP\s+TABLE',
        'TRUNCATE\s+TABLE',
        'del\s+/s\s+/q',
        'rmdir\s+/s\s+/q'
    )

    foreach ($pattern in $dangerousPatterns) {
        if ($command -match $pattern) {
            @{
                hookSpecificOutput = @{
                    hookEventName = "PreToolUse"
                    permissionDecision = "deny"
                    permissionDecisionReason = "Dangerous command blocked by project hook."
                }
            } | ConvertTo-Json -Compress
            exit 0
        }
    }

    exit 0
}
catch {
    Write-Error "Hook validation failed: $($_.Exception.Message)"
    exit 1
}
