# Save as start-openjarvis.ps1 (updated)
$env:PYTHONUTF8 = "1"
$env:PYTHONIOENCODING = "utf-8"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
chcp 65001 > $null
Write-Host "Starting OpenJarvis..." -ForegroundColor Cyan
cd C:\Users\Admin\OpenJarvis   # <-- CHANGED

# Ensure HOME is set for memory backend
$env:HOME = $env:USERPROFILE

# Sync venv with all required extras
Write-Host "Syncing venv with required extras..." -ForegroundColor Yellow
uv sync --extra speech --extra server --extra inference-cloud --extra inference-google --extra openhands --extra scheduler --extra pdf --extra tools-search --extra security-signing
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: uv sync failed." -ForegroundColor Red
    exit 1
}

# Always rebuild Rust extension (fast, and uv sync drops it every time)
Write-Host "Rebuilding Rust extension..." -ForegroundColor Yellow
uv run maturin develop --release --manifest-path rust\crates\openjarvis-python\Cargo.toml
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Rust build failed." -ForegroundColor Red
    exit 1
}
Write-Host "All dependencies ready" -ForegroundColor Green

# Start server
Write-Host "Starting server on port 8010..." -ForegroundColor Cyan
& "C:\Users\Admin\OpenJarvis\.venv\Scripts\python.exe" -m openjarvis.cli serve --port 8010
