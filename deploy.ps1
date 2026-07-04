<#
.SYNOPSIS
    OpenJarvis Automated Build, Patch & Deploy Script
.DESCRIPTION
    1. Patches frontend/src/components/Chat/InputArea.tsx for file uploads.
    2. Clears caches (Vite, Tauri, WSL).
    3. Builds Tauri Release binary (npm install + cargo build --release).
    4. Deploys EXE to C:\Program Files\OpenJarvis (TEST + LIVE backup).
    5. Starts Backend (Python/UV) on Port 8010 as background Job.
    6. Launches TEST.exe for verification.
.NOTES
    - MUST be run as Administrator (writes to Program Files).
    - MUST be saved as a .ps1 file and executed via file path (not pasted).
    - Requires: Node.js, Rust (cargo), Tauri CLI, Python/UV, WebView2 Runtime.
#>
[CmdletBinding()]
param(
    [switch]$LaunchTest,          # Auto-launch TEST.exe after deploy
    [switch]$SkipBuild,           # Skip Tauri build (deploy existing artifact)
    [switch]$SkipBackend,         # Don't start backend job
    [string]$ProjectRoot = $PSScriptRoot # Auto-detects script location
)

# ─────────────────────────────────────────────────────────────────────────────
# CONFIGURATION & PATH RESOLUTION
# ─────────────────────────────────────────────────────────────────────────────
$ErrorActionPreference = "Stop"
$ProgressPreference = "SilentlyContinue"

# Resolve absolute paths safely
$root        = Resolve-Path $ProjectRoot
$frontend    = Join-Path $root.Path "frontend"
$srcTauri    = Join-Path $frontend "src-tauri"
$installDir  = "C:\Program Files\OpenJarvis"

# Artifacts
$builtExe    = Join-Path $srcTauri "target\release\openjarvis-desktop.exe"
$testExe     = Join-Path $installDir "openjarvis-desktop-TEST.exe"
$liveExe     = Join-Path $installDir "openjarvis-desktop.exe"
$goodExe     = Join-Path $installDir "openjarvis-desktop-GOOD.exe"

# Source Files to Patch
$inputArea   = Join-Path $frontend "src\components\Chat\InputArea.tsx"

# Backend
$backendLog  = Join-Path $env:LOCALAPPDATA "OpenJarvis\logs\backend.log"
$startScript = (Get-ChildItem $root.Path -Filter "start-openjarvis.*" -File | Select-Object -First 1).FullName

# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────
function Write-Step { param($msg) Write-Host "`n=== $msg ===" -ForegroundColor Cyan }
function Write-Ok   { param($msg) Write-Host "[OK]  $msg" -ForegroundColor Green }
function Write-Warn { param($msg) Write-Host "[WARN] $msg" -ForegroundColor Yellow }
function Write-Err  { param($msg) Write-Host "[ERROR] $msg" -ForegroundColor Red; throw $msg }

function Ensure-Dir { param($path) if (-not (Test-Path $path)) { New-Item -ItemType Directory -Path $path -Force | Out-Null; Write-Ok "Created dir: $path" } }

# ─────────────────────────────────────────────────────────────────────────────
# PRE-FLIGHT CHECKS
# ─────────────────────────────────────────────────────────────────────────────
Write-Step "Pre-Flight Checks"

# 1. Admin Check
$principal = New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())
if (-not $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    Write-Err "Must run as Administrator. Right-click PowerShell -> 'Run as Administrator'."
}

# 2. Critical Path Validation
$requiredDirs = @($frontend, $srcTauri)
$requiredFiles = @($inputArea)
foreach ($d in $requiredDirs) { if (-not (Test-Path $d)) { Write-Err "Missing Directory: $d" } }
foreach ($f in $requiredFiles) { if (-not (Test-Path $f)) { Write-Err "Missing File: $f" } }
if (-not $startScript) { Write-Warn "Backend launcher 'start-openjarvis.*' not found in $($root.Path). Backend start will be skipped." }

# 3. WebView2 Check
$webview2 = Get-ItemProperty "HKLM:\SOFTWARE\WOW6432Node\Microsoft\EdgeUpdate\Clients\{F3017226-FE2A-4295-8BDF-00C3A9A7E4C5}" -EA SilentlyContinue
if (-not $webview2) { Write-Warn "WebView2 Runtime NOT detected. App will crash. Install: https://go.microsoft.com/fwlink/p/?LinkId=2124703" }
else { Write-Ok "WebView2 Runtime: $($webview2.pv)" }

Write-Ok "Paths Validated. Root: $($root.Path)"

# ─────────────────────────────────────────────────────────────────────────────
# 1. KILL EXISTING PROCESSES
# ─────────────────────────────────────────────────────────────────────────────
Write-Step "1. Killing OpenJarvis Processes"
Get-Process -Name "*openjarvis*" -EA SilentlyContinue | ForEach-Object {
    try { Stop-Process -Id $_.Id -Force; Write-Ok "Stopped $($_.ProcessName) (PID $($_.Id))" }
    catch { Write-Warn "Could not stop $($_.ProcessName): $_" }
}
Start-Sleep 1

# ─────────────────────────────────────────────────────────────────────────────
# 2. PATCH InputArea.tsx (Idempotent & Safe)
# ─────────────────────────────────────────────────────────────────────────────
Write-Step "2. Patching InputArea.tsx (Attachment Feature)"

$content = Get-Content $inputArea -Raw -Encoding UTF8
$backupPath = "$inputArea.bak.$(Get-Date -Format 'yyyyMMdd-HHmmss')"
Copy-Item $inputArea $backupPath -Force
Write-Ok "Backup: $backupPath"

# Check if already patched (look for the unique upload logic)
if ($content -match 'fetch\("http://localhost:8010/v1/connectors/upload/ingest/files"') {
    Write-Warn "InputArea.tsx already appears patched. Skipping."
}
else {
    # Define the EXACT new block (Paperclip button + Hidden File Input + Upload Logic)
    # We replace the <button title="Attach file">...</button> block entirely.
    $newBlock = @'
        <input
          type="file"
          ref={fileInputRef}
          className="hidden"
          accept=".pdf,.txt,.md,.csv,.docx,image/*"
          onChange={async (e) => {
            const file = e.target.files?.[0];
            e.target.value = "";
            if (!file) return;
            const formData = new FormData();
            formData.append("files", file);
            try {
              setInput((prev) => prev + (prev ? " " : "") + `[Uploading: ${file.name}...]`);
              const res = await fetch("http://localhost:8010/v1/connectors/upload/ingest/files", {
                method: "POST",
                body: formData,
              });
              if (!res.ok) {
                const errText = await res.text();
                throw new Error(errText || `Upload failed (${res.status})`);
              }
              const result = await res.json();
              setInput((prev) =>
                prev.replace(`[Uploading: ${file.name}...]`, `[Attached: ${file.name} - ${result.chunks_added} chunks ingested]`)
              );
            } catch (err) {
              console.error("File upload failed:", err);
              setInput((prev) =>
                prev.replace(`[Uploading: ${file.name}...]`, `[Attach failed: ${file.name} - ${err instanceof Error ? err.message : "unknown error"}]`)
              );
            }
          }}
        />
        <button
          onClick={() => fileInputRef.current?.click()}
          disabled={streamState.isStreaming}
          className="p-2 rounded-xl transition-colors shrink-0 cursor-pointer disabled:opacity-30"
          style={{ color: "var(--color-text-tertiary)" }}
          title="Attach file"
        >
          <Paperclip size={16} />
        </button>
'@

    # Regex: Find the button with title="Attach file" and replace it.
    $pattern = '(?s)<button[^>]*title="Attach file"[^>]*>.*?</button>'

    if ($content -match $pattern) {
        $newContent = $content -replace $pattern, $newBlock
        $utf8NoBom = New-Object System.Text.UTF8Encoding $false
        [System.IO.File]::WriteAllText($inputArea, $newContent, $utf8NoBom)
        Write-Ok "InputArea.tsx patched successfully."
    }
    else {
        Write-Err "Could not find '<button title=`"Attach file`">' in InputArea.tsx. File structure may have changed. Check $backupPath"
    }
}

# ─────────────────────────────────────────────────────────────────────────────
# 3. NUCLEAR CACHE CLEAR
# ─────────────────────────────────────────────────────────────────────────────
Write-Step "3. Clearing Caches"
$cachePaths = @(
    (Join-Path $frontend "node_modules\.vite"),
    (Join-Path $frontend "dist"),
    (Join-Path $root.Path "src\openjarvis\server\static"),
    (Join-Path $env:LOCALAPPDATA "OpenJarvis\EBWebView")
)
foreach ($p in $cachePaths) { if (Test-Path $p) { Remove-Item -Recurse -Force $p -EA SilentlyContinue; Write-Ok "Cleared: $p" } }

# WSL Cache (Best effort)
if (Get-Command wsl -EA SilentlyContinue) {
    wsl rm -rf ~/.cache/yarn ~/.npm/_cacache 2>$null
    Write-Ok "WSL caches cleared."
}

# ─────────────────────────────────────────────────────────────────────────────
# 4. BUILD TAURI APP
# ─────────────────────────────────────────────────────────────────────────────
if (-not $SkipBuild) {
    Write-Step "4. Building Tauri App (Release Mode)..."
    Set-Location $frontend

    # Ensure Node Modules
    if (-not (Test-Path "node_modules")) { Write-Host "Installing npm deps..."; npm install | Out-Null }

    # Run Build
    # NOTE: Tauri/npm write informational lines to stderr. With $ErrorActionPreference
    # set to "Stop" globally, PowerShell would treat that stderr noise as a terminating
    # error. Temporarily relax it for this native command and rely on $LASTEXITCODE instead.
    Write-Host "Running: npx tauri build (this takes 3-10 mins)..."
    $prevEAP = $ErrorActionPreference
    $ErrorActionPreference = "Continue"
    $buildOutput = & npx tauri build 2>&1 | ForEach-Object { "$_" }
    $exitCode = $LASTEXITCODE
    $ErrorActionPreference = $prevEAP

    # Show Tail (guard against short output)
    $tailCount = [Math]::Min(30, $buildOutput.Count)
    if ($tailCount -gt 0) {
        $buildOutput[-$tailCount..-1] | ForEach-Object { Write-Host $_ }
    }

    # Verify EXE exists (Tauri often exits non-zero due to MSI WiX failure, but EXE is fine)
    if (-not (Test-Path $builtExe)) {
        Write-Err "Build FAILED. EXE not found at: $builtExe. Exit Code: $exitCode"
    }
    Write-Ok "Build Successful. Artifact: $builtExe"
}
else { Write-Step "4. Skipping Build (Flag: -SkipBuild)" }

# ─────────────────────────────────────────────────────────────────────────────
# 5. DEPLOY TO PROGRAM FILES
# ─────────────────────────────────────────────────────────────────────────────
Write-Step "5. Deploying to $installDir"
Ensure-Dir $installDir

if (-not (Test-Path $builtExe)) { Write-Err "Source EXE missing: $builtExe. Did build run?" }

# Backup Live -> Good
if ((Test-Path $liveExe) -and -not (Test-Path $goodExe)) {
    Copy-Item $liveExe $goodExe -Force
    Write-Ok "Backed up LIVE -> GOOD.exe"
}
elseif (Test-Path $goodExe) {
    Write-Ok "GOOD.exe backup exists."
}

# Deploy New -> TEST
Copy-Item $builtExe $testExe -Force
$deployed = Get-Item $testExe
$ageMin = [math]::Round(((Get-Date) - $deployed.LastWriteTime).TotalMinutes, 1)
Write-Ok "Deployed TEST.exe (Age: $ageMin min, Size: $([math]::Round($deployed.Length/1MB,1)) MB)"

# ─────────────────────────────────────────────────────────────────────────────
# 6. START BACKEND (Background Job)
# ─────────────────────────────────────────────────────────────────────────────
$backendJob = $null
if (-not $SkipBackend -and $startScript) {
    Write-Step "6. Starting Backend on Port 8010"
    Set-Location $root.Path

    $backendJob = Start-Job -Name "OpenJarvisBackend" -ScriptBlock {
        param($rootPath, $launcher)
        Set-Location $rootPath
        if ($launcher -match '\.ps1$') { & powershell -NoExit -File $launcher }
        elseif ($launcher -match '\.bat$') { & cmd /c $launcher }
        else { & $launcher }
    } -ArgumentList $root.Path, $startScript

    Write-Host "Backend Job Started (ID: $($backendJob.Id)). Waiting for Port 8010..."
    $timeout = 120; $start = Get-Date
    $portOpen = $false
    while (((Get-Date) - $start).TotalSeconds -lt $timeout) {
        $testConn = Test-NetConnection -ComputerName localhost -Port 8010 -WarningAction SilentlyContinue
        if ($testConn.TcpTestSucceeded) {
            Write-Ok "Backend Port 8010 is LISTENING."
            $portOpen = $true
            break
        }
        Start-Sleep 2
        if ($backendJob.State -eq 'Failed') {
            $err = Receive-Job -Id $backendJob.Id -EA SilentlyContinue
            Write-Err "Backend Job DIED. Errors: $err"
        }
    }

    if (-not $portOpen) {
        Write-Warn "Port 8010 not open after ${timeout}s. Check Job: Receive-Job -Id $($backendJob.Id)"
    }
}
elseif (-not $startScript) { Write-Warn "Skipping Backend Start (Launcher script not found)." }
else { Write-Step "6. Skipping Backend Start (Flag: -SkipBackend)" }

# ─────────────────────────────────────────────────────────────────────────────
# 7. LAUNCH TEST.EXE
# ─────────────────────────────────────────────────────────────────────────────
Write-Step "7. Ready to Test"

if ($LaunchTest) {
    Write-Host "Auto-launching TEST.exe..." -ForegroundColor Magenta
    try {
        Start-Process -FilePath $testExe -WorkingDirectory $installDir -ErrorAction Stop
        Write-Ok "TEST.exe Launched."
    } catch { Write-Err "Failed to launch TEST.exe: $_" }
}
else {
    Write-Host "`nMANUAL STEPS:" -ForegroundColor Magenta
    Write-Host "1. Launch Test App:  & '$testExe'" -ForegroundColor White
    Write-Host "2. Click Paperclip -> Select File -> Watch Input Box for '[Uploading: filename...]'" -ForegroundColor White
    Write-Host "3. Check Backend Log:  Get-Content '$backendLog' -Tail 20 -Wait" -ForegroundColor Yellow
    Write-Host "`nTO PROMOTE TO LIVE (after verified):" -ForegroundColor Cyan
    Write-Host "   Stop-Process -Name 'openjarvis-desktop-TEST' -Force -ErrorAction SilentlyContinue" -ForegroundColor White
    Write-Host "   Copy-Item '$testExe' '$liveExe' -Force" -ForegroundColor White
}

# ─────────────────────────────────────────────────────────────────────────────
# 8. KEEP ALIVE / CLEANUP HELP
# ─────────────────────────────────────────────────────────────────────────────
Write-Step "8. Session Info & Cleanup Commands"

Write-Host "`n=== BACKEND JOB INFO ===" -ForegroundColor Cyan
if ($backendJob) {
    Write-Host "Job ID: $($backendJob.Id) | Name: $($backendJob.Name) | State: $($backendJob.State)"
    Write-Host "View Logs:      Receive-Job -Id $($backendJob.Id) -Keep"
    Write-Host "Stop Backend:   Stop-Job -Id $($backendJob.Id); Remove-Job -Id $($backendJob.Id)"
}
else {
    Write-Host "No backend job started (skipped or no launcher found)."
}

Write-Host "`n=== QUICK ROLLBACK ===" -ForegroundColor Cyan
Write-Host "If TEST.exe is broken, restore GOOD backup:" -ForegroundColor White
Write-Host "   Stop-Process -Name 'openjarvis-desktop-TEST' -Force -EA 0" -ForegroundColor Gray
Write-Host "   Copy-Item '$goodExe' '$testExe' -Force" -ForegroundColor Gray

Write-Host "`n=== VERIFICATION CHECKLIST ===" -ForegroundColor Cyan
Write-Host "1. Paperclip icon clicks -> File Dialog opens" -ForegroundColor White
Write-Host "2. Select file -> Input box shows '[Uploading: file.pdf...]'" -ForegroundColor White
Write-Host "3. Success -> Input box shows '[Attached: file.pdf - X chunks ingested]'" -ForegroundColor Green
Write-Host "4. Failure -> Input box shows '[Attach failed: file.pdf - Error details]'" -ForegroundColor Red
Write-Host "5. Backend Log ($backendLog) shows 'POST /v1/connectors/upload/ingest/files 200'" -ForegroundColor White

Write-Host "`nDeploy Script Finished." -ForegroundColor Green