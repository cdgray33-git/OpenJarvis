# ensure-rust.ps1
# Automatically ensures openjarvis_rust is available

$ErrorActionPreference = "Stop"
cd C:\Windows\System32\OpenJarvis

# Quick check if module exists
$moduleCheck = python -c "import openjarvis_rust" 2>&1

if ($moduleCheck -like "*ModuleNotFoundError*") {
    Write-Host "⚠️  openjarvis_rust not found. Building..." -ForegroundColor Yellow
    
    # Build it
    cd rust\crates\openjarvis-python
    maturin develop --release --quiet
    
    Write-Host "✅ openjarvis_rust built and installed" -ForegroundColor Green
    cd C:\Windows\System32\OpenJarvis
} else {
    Write-Host "✅ openjarvis_rust already available" -ForegroundColor Green
}