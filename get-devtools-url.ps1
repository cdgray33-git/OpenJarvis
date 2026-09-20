$ErrorActionPreference = 'Stop'
try {
    $r = Invoke-WebRequest -Uri 'http://127.0.0.1:9222/json' -TimeoutSec 5 -UseBasicParsing
    $targets = $r.Content | ConvertFrom-Json
} catch {
    Write-Host ("[FAIL] could not fetch 9222/json: " + $_.Exception.Message) -ForegroundColor Red
    Write-Host "       Is the OpenJarvis exe still running? Relaunch it and retry." -ForegroundColor Yellow
    exit 1
}

Write-Host "=== all targets on 9222 ===" -ForegroundColor Cyan
foreach ($t in $targets) {
    Write-Host ("  type=" + $t.type + "  title=" + $t.title + "  url=" + $t.url)
}

Write-Host ""
$page = $targets | Where-Object { $_.type -eq 'page' -and $_.url -like '*tauri.localhost*' } | Select-Object -First 1
if (-not $page) { $page = $targets | Where-Object { $_.type -eq 'page' } | Select-Object -First 1 }

if ($page) {
    Write-Host "=== OpenJarvis page target ===" -ForegroundColor Green
    Write-Host ("  title: " + $page.title)
    Write-Host ("  url:   " + $page.url)
    Write-Host ""
    Write-Host "  >>> OPEN THIS IN A NEW CHROME TAB: <<<" -ForegroundColor Yellow
    $fe = $page.devtoolsFrontendUrl
    if ($fe -notlike 'http*') { $fe = "http://localhost:9222" + $fe }
    Write-Host ("  " + $fe) -ForegroundColor White
} else {
    Write-Host "[FAIL] no 'page' target found - exe may not be running" -ForegroundColor Red
}