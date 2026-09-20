# After building openjarvis-python wheel

# Build traces if it exists (optional)
if (Test-Path rust\crates\openjarvis-traces) {
    Write-Host "Building traces..." -ForegroundColor Yellow
    cd rust
    cargo build --release -p openjarvis-traces
    cd ..
}

# Create config to disable traces (it's optional)
$configPath = "$env:USERPROFILE\.openjarvis\config.yaml"
New-Item -Path (Split-Path $configPath) -ItemType Directory -Force
@"
traces:
  enabled: false

skills:
  strict_parsing: false
"@ | Out-File $configPath -Encoding UTF8