# restart-and-verify.ps1
$ErrorActionPreference = "Stop"
$root = "C:\Users\Admin\OpenJarvis"
$venvPy = Join-Path $root ".venv\Scripts\python.exe"

Write-Host "=== Restarting OpenJarvis Server ===" -ForegroundColor Cyan

Write-Host "Killing process on port 8010..." -ForegroundColor Yellow
$pids = Get-NetTCPConnection -LocalPort 8010 -State Listen -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess -Unique
foreach ($pid in $pids) {
    Stop-Process -Id $pid -Force -ErrorAction SilentlyContinue
    Write-Host "  Killed PID $pid"
}
if (-not $pids) { Write-Host "  No process found on port 8010" }

Write-Host "`nStarting server via start-openjarvis.ps1..." -ForegroundColor Yellow
& (Join-Path $root "start-openjarvis.ps1")

Write-Host "`nWaiting for server to start..." -ForegroundColor Yellow
$maxWait = 30
$waited = 0
while ($waited -lt $maxWait) {
    try {
        $resp = Invoke-WebRequest -Uri "http://127.0.0.1:8010/v1/speech/health" -Method Get -UseBasicParsing -TimeoutSec 2 -ErrorAction Stop
        if ($resp.StatusCode -eq 200) { break }
    } catch { }
    Start-Sleep -Seconds 1
    $waited++
}
if ($waited -ge $maxWait) {
    Write-Error "Server did not start within $maxWait seconds"
    exit 1
}

Write-Host "`n=== Health Endpoint Response ===" -ForegroundColor Cyan
$health = Invoke-WebRequest -Uri "http://127.0.0.1:8010/v1/speech/health" -Method Get -UseBasicParsing
Write-Host $health.Content
$healthJson = $health.Content | ConvertFrom-Json

Write-Host "`n=== Validation ===" -ForegroundColor Cyan
$checks = @(
    @{ Name = "available=true";        Test = { $healthJson.available -eq $true } },
    @{ Name = "stt=ok";                Test = { $healthJson.stt -eq "ok" } },
    @{ Name = "tts=ok";                Test = { $healthJson.tts -eq "ok" } },
    @{ Name = "stt_backend=faster-whisper"; Test = { $healthJson.stt_backend -eq "faster-whisper" } },
    @{ Name = "tts_backend=kokoro";    Test = { $healthJson.tts_backend -eq "kokoro" } },
    @{ Name = "voice=am_adam";         Test = { $healthJson.voice -eq "am_adam" } }
)

$allPassed = $true
foreach ($c in $checks) {
    $result = & $c.Test
    $color = if ($result) { "Green" } else { "Red"; $allPassed = $false }
    Write-Host "  $($c.Name): $result" -ForegroundColor $color
}

if ($allPassed) {
    Write-Host "`n[OK] All health checks passed - Backend is LIVE" -ForegroundColor Green
    Write-Host "`n=== WebSocket Endpoint Probe ===" -ForegroundColor Cyan
    try {
        $wsTest = Invoke-WebRequest -Uri "http://127.0.0.1:8010/v1/speech/stream" -Method Get -UseBasicParsing -TimeoutSec 2
        Write-Host "  WS endpoint responds (HTTP $($wsTest.StatusCode)) - Upgrade required" -ForegroundColor Yellow
    } catch {
        Write-Host "  WS endpoint check: $($_.Exception.Message)" -ForegroundColor Yellow
    }
    exit 0
} else {
    Write-Error "`n[FAIL] Some health checks failed"
    exit 1
}
