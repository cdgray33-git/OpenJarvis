# OpenJarvis Nuclear Cache Clear  (canonical, C:\Users\Admin\OpenJarvis)
# Run before EVERY tauri build. Clears Vite, dist, static, WebView2, and SW artifacts.
$root     = 'C:\Users\Admin\OpenJarvis'
$frontend = Join-Path $root 'frontend'
$static   = Join-Path $root 'src\openjarvis\server\static'
$builtExe = Join-Path $frontend 'src-tauri\target\release\openjarvis-desktop.exe'

Write-Host '=== 1. Kill all openjarvis processes (releases file locks + SW) ===' -ForegroundColor Cyan
Get-Process | Where-Object { $_.ProcessName -like '*openjarvis*' } | Stop-Process -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 2

Write-Host '=== 2. Vite / build caches ===' -ForegroundColor Cyan
Remove-Item -Recurse -Force "$frontend\node_modules\.vite" -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force "$frontend\dist" -ErrorAction SilentlyContinue

Write-Host '=== 3. Server static (full wipe - build regenerates) ===' -ForegroundColor Cyan
Remove-Item -Recurse -Force "$static" -ErrorAction SilentlyContinue

Write-Host '=== 4. Service worker artifacts (the 3-day-bug source) ===' -ForegroundColor Cyan
Remove-Item -Force "$static\sw.js","$static\registerSW.js","$static\workbox-*.js","$static\manifest.webmanifest" -ErrorAction SilentlyContinue

Write-Host '=== 5. WebView2 cache (EBWebView - holds Cache Storage the SW writes to) ===' -ForegroundColor Cyan
Remove-Item -Recurse -Force "$env:LOCALAPPDATA\OpenJarvis\EBWebView" -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force "$env:LOCALAPPDATA\com.openjarvis.desktop\EBWebView" -ErrorAction SilentlyContinue

Write-Host '=== 6. Stale release exe (avoid launching old binary) ===' -ForegroundColor Cyan
Remove-Item -Force "$builtExe" -ErrorAction SilentlyContinue

Write-Host 'Nuclear clear complete. Safe to run: cd $frontend ; npx tauri build' -ForegroundColor Green