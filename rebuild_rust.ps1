# FRONTEND REBUILD NOTE:
# To rebuild the Tauri frontend (UI changes only):
#   cd frontend && npm run build:tauri
# To rebuild the Rust exe (required after ANY Rust/Tauri changes):
#   cd frontend && npx tauri build
# After exe rebuild: kill msedgewebview2, delete %LOCALAPPDATA%\com.openjarvis.desktop, relaunch
#
﻿# Rebuild openjarvis_rust extension after any venv wipe, then start server
Write-Host "Rebuilding openjarvis_rust..." -ForegroundColor Cyan
cd "C:\Windows\System32\OpenJarvis"

# Ensure HOME is set for memory backend
$env:HOME = $env:USERPROFILE

# Sync venv with all required extras
Write-Host "Syncing venv with required extras..." -ForegroundColor Yellow
uv sync --extra speech --extra server
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: uv sync failed." -ForegroundColor Red
    exit 1
}

# Rebuild Rust extension
uv run maturin develop --release --manifest-path rust\crates\openjarvis-python\Cargo.toml
if ($LASTEXITCODE -eq 0) {
    Write-Host "openjarvis_rust rebuilt successfully." -ForegroundColor Green
} else {
    Write-Host "ERROR: Rust build failed." -ForegroundColor Red
    exit 1
}

uv run jarvis serve --port 8010
