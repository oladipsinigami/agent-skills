# Install agent skills into Claude Code and/or OpenCode.
# Usage: .\install.ps1 [-Target all|claude|opencode]

param(
    [ValidateSet("all", "claude", "opencode")]
    [string]$Target = "all"
)

$ErrorActionPreference = "Stop"
$src = Join-Path $PSScriptRoot "skills"

function Install-Collection {
    param([string]$Name, [string]$From, [string]$To)

    if (-not (Test-Path $From)) {
        Write-Host "skip: $From not found"
        return
    }
    New-Item -ItemType Directory -Force $To | Out-Null
    Get-ChildItem -Path $From -Force | ForEach-Object {
        Copy-Item -Path $_.FullName -Destination $To -Recurse -Force
    }
    $count = (Get-ChildItem -Path $To -Directory).Count
    Write-Host "installed $Name -> $To ($count skills)"
}

switch ($Target) {
    "claude"   { Install-Collection "Claude Code" (Join-Path $src "claude")   (Join-Path $HOME ".claude\skills") }
    "opencode" { Install-Collection "OpenCode"    (Join-Path $src "opencode") (Join-Path $HOME ".config\opencode\skills") }
    "all" {
        Install-Collection "Claude Code" (Join-Path $src "claude")   (Join-Path $HOME ".claude\skills")
        Install-Collection "OpenCode"    (Join-Path $src "opencode") (Join-Path $HOME ".config\opencode\skills")
    }
}

Write-Host ""
Write-Host "Done. Restart the agent (or start a new session) to pick up the skills."
