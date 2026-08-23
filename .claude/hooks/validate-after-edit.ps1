$ErrorActionPreference = "Stop"

try {
    $inputJson = [Console]::In.ReadToEnd() | ConvertFrom-Json
    $toolName = [string]$inputJson.tool_name
    $toolInput = $inputJson.tool_input

    if ($toolName -notin @("Edit", "Write")) {
        exit 0
    }

    $candidatePaths = @()

    foreach ($property in @("file_path", "path", "filePath")) {
        if ($null -ne $toolInput.$property) {
            $candidatePaths += [string]$toolInput.$property
        }
    }

    $pythonFiles = $candidatePaths |
        Where-Object { $_ -match "\.py$" } |
        Select-Object -Unique

    if (-not $pythonFiles) {
        exit 0
    }

    foreach ($pythonFile in $pythonFiles) {
        python -m py_compile $pythonFile
        if ($LASTEXITCODE -ne 0) {
            Write-Error "Python syntax validation failed for $pythonFile."
            exit 1
        }
    }

    Write-Output "Python syntax validation passed."
    exit 0
}
catch {
    Write-Error "Post-edit validation failed: $($_.Exception.Message)"
    exit 1
}
