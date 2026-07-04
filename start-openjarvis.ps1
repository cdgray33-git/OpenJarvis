# start-openjarvis.ps1
$env:PYTHONUTF8 = "1"
$env:PYTHONIOENCODING = "utf-8"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
chcp 65001 > $null
Write-Host "Starting OpenJarvis..." -ForegroundColor Cyan
cd C:\Windows\System32\OpenJarvis

# Ensure HOME is set for memory backend
$env:HOME = $env:USERPROFILE

# Sync venv with all required extras
Write-Host "Syncing venv with required extras..." -ForegroundColor Yellow
uv sync --extra speech --extra server
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
uv run jarvis serve --port 8010
