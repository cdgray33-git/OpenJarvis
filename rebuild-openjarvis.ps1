# Fix pynvml warning
Write-Host "Patching GPU monitor..." -ForegroundColor Yellow
$gpuFile = "src\openjarvis\telemetry\gpu_monitor.py"
$content = Get-Content $gpuFile -Raw

if (!($content -match "warnings.filterwarnings.*pynvml")) {
    $content = $content -replace 
        'try:\s+import pynvml',
        "try:`n    import warnings`n    warnings.filterwarnings('ignore', category=FutureWarning, message='.*pynvml.*')`n    import pynvml"
    $content | Out-File $gpuFile -Encoding UTF8 -NoNewline
    Write-Host "✅ GPU monitor patched" -ForegroundColor Green
}