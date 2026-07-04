<#
.SYNOPSIS
    Extracts ground-truth context needed to safely build the retrieval-injection fix:
    - Top-level imports (first ~40 lines) of both target files
    - Surrounding context around the two CONFIRMED real anchors
    - Function signature lines containing those anchors, to confirm indentation level
.NOTES
    Read-only. Does not modify any files.
#>
[CmdletBinding()]
param(
    [string]$ProjectRoot = "C:\WINDOWS\system32\OpenJarvis"
)

$ErrorActionPreference = "Stop"

$apiRoutes   = Join-Path $ProjectRoot "src\openjarvis\server\api_routes.py"
$agentMgr    = Join-Path $ProjectRoot "src\openjarvis\server\agent_manager_routes.py"

function Write-Section { param($title) Write-Host "`n========== $title ==========" -ForegroundColor Cyan }

# ── 1. Top-level imports: api_routes.py ─────────────────────────────────
Write-Section "api_routes.py - first 40 lines (top-level imports)"
Get-Content $apiRoutes -TotalCount 40 | ForEach-Object -Begin { $i = 0 } -Process {
    $i++
    Write-Host ("{0,4}: {1}" -f $i, $_)
}

# ── 2. Context around confirmed anchor: engine = getattr(...) ──────────
Write-Section "api_routes.py - context around line 598 (engine = getattr anchor)"
$start = [Math]::Max(1, 580)
$end   = 650
Get-Content $apiRoutes | Select-Object -Skip ($start - 1) -First ($end - $start + 1) | ForEach-Object -Begin { $i = $start } -Process {
    Write-Host ("{0,4}: {1}" -f $i, $_)
    $i++
}

# ── 3. Top-level imports: agent_manager_routes.py ───────────────────────
Write-Section "agent_manager_routes.py - first 40 lines (top-level imports)"
Get-Content $agentMgr -TotalCount 40 | ForEach-Object -Begin { $i = 0 } -Process {
    $i++
    Write-Host ("{0,4}: {1}" -f $i, $_)
}

# ── 4. Context around confirmed anchor: while turns < max_turns: ───────
Write-Section "agent_manager_routes.py - context around line 1043 (while turns anchor)"
$start = 1015
$end   = 1060
Get-Content $agentMgr | Select-Object -Skip ($start - 1) -First ($end - $start + 1) | ForEach-Object -Begin { $i = $start } -Process {
    Write-Host ("{0,4}: {1}" -f $i, $_)
    $i++
}

# ── 5. Function definition containing the while-turns anchor ───────────
Write-Section "agent_manager_routes.py - nearest function def(s) before line 1043"
Get-Content $agentMgr | Select-Object -First 1043 |
    Select-String -Pattern "^\s*(async )?def " |
    Select-Object -Last 5

# ── 6. Function definition containing the engine=getattr anchor ────────
Write-Section "api_routes.py - nearest function def(s) before line 598"
Get-Content $apiRoutes | Select-Object -First 598 |
    Select-String -Pattern "^\s*(async )?def " |
    Select-Object -Last 5

Write-Host "`n========== DONE - copy/paste all of the above ==========" -ForegroundColor Green