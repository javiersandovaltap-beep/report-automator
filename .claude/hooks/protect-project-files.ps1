$ErrorActionPreference = "Stop"

try {
    $inputJson = [Console]::In.ReadToEnd() | ConvertFrom-Json
    $toolName = [string]$inputJson.tool_name
    $toolInput = $inputJson.tool_input

    if ($toolName -notin @("Edit", "Write")) {
        exit 0
    }

    $protectedFiles = @(
        "AGENTS.md",
        "CLAUDE.md",
        ".env",
        ".env.example"
    )

    $candidatePaths = @()

    foreach ($property in @("file_path", "path", "filePath")) {
        if ($null -ne $toolInput.$property) {
            $candidatePaths += [string]$toolInput.$property
        }
    }

    foreach ($candidatePath in $candidatePaths) {
        $normalizedPath = $candidatePath.Replace("\", "/")
        $fileName = Split-Path $normalizedPath -Leaf

        if ($protectedFiles -contains $fileName) {
            @{
                hookSpecificOutput = @{
                    hookEventName = "PreToolUse"
                    permissionDecision = "deny"
                    permissionDecisionReason = "Protected project file blocked by hook."
                }
            } | ConvertTo-Json -Compress
            exit 0
        }
    }

    exit 0
}
catch {
    Write-Error "Protected-file hook failed: $($_.Exception.Message)"
    exit 1
}
