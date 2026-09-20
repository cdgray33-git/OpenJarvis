<#
.SYNOPSIS
    Updates InputArea.tsx with agent field mapping and verifies the change.
.DESCRIPTION
    Replaces the raw `data.registered || []` assignment with a mapped transform
    (key->id, class->name, accepts_tools->acceptsTools), then prints +-15 lines
    around the change for verification.
#>

$file = "C:\Users\Admin\OpenJarvis\frontend\src\components\Chat\InputArea.tsx"
$backup = "$file.$(Get-Date -Format 'yyyyMMdd_HHmmss').bak"

# 1. Safety: ensure file exists
if (-not (Test-Path $file)) {
    Write-Error "File not found: $file"
    exit 1
}

# 2. Backup
Copy-Item $file $backup -Force
Write-Host "Backup created: $backup" -ForegroundColor Cyan

# 3. Read content
$content = Get-Content $file -Raw

# 4. Define the exact old block (from your grep output) and new block
$oldBlock = @"
    // Fetch agents on mount
    useEffect(() => {
      fetch(`${getBase()}/v1/agents`)
        .then(r => r.ok ? r.json() : [])
        .then(data => setManagedAgents(data.registered || []))
        .catch(() => {});
    }, [setManagedAgents]);
"@

$newBlock = @"
    // Fetch agents on mount
    useEffect(() => {
      fetch(`${getBase()}/v1/agents`)
        .then(r => r.ok ? r.json() : [])
        .then(data => setManagedAgents(
          (data.registered || []).map(agent => ({
            id: agent.key,
            name: agent.class.replace('Agent', ''),
            acceptsTools: agent.accepts_tools
          }))
        ))
        .catch(() => {});
    }, [setManagedAgents]);
"@

# 5. Replace (exact match, including indentation)
if ($content -notmatch [regex]::Escape($oldBlock)) {
    Write-Error "Old block not found -- file may have already been modified or formatting differs."
    Write-Host "Searching for similar patterns..." -ForegroundColor Yellow
    Select-String -Pattern "setManagedAgents\(data\.registered" -Path $file -Context 3,3
    exit 1
}

$newContent = $content -replace [regex]::Escape($oldBlock), $newBlock

# 6. Write back
Set-Content -Path $file -Value $newContent -NoNewline
Write-Host "File updated." -ForegroundColor Green

# 7. Verify: show +-15 lines around the change
$lines = $newContent -split "`r?`n"
$matchIndex = $lines | Select-String -Pattern "id: agent\.key" | Select-Object -First 1 -ExpandProperty LineNumber
if ($null -eq $matchIndex) {
    Write-Warning "Could not locate new block after write."
    exit 0
}
$start = [math]::Max(0, $matchIndex - 16)
$end   = [math]::Min($lines.Count - 1, $matchIndex + 14)

Write-Host "`n=== VERIFICATION: Lines $($start+1) to $($end+1) ===" -ForegroundColor Cyan
for ($i = $start; $i -le $end; $i++) {
    $prefix = if ($i -eq $matchIndex - 1) { ">>> " } else { "    " }
    Write-Host "$prefix$($i+1): $($lines[$i])"
}

# 8. Quick syntax sanity-check (TypeScript compile)
Write-Host "`nRunning TypeScript check..." -ForegroundColor Cyan
cd "C:\Users\Admin\OpenJarvis\frontend"
npx tsc --noEmit --skipLibCheck 2>&1 | Select-Object -First 20