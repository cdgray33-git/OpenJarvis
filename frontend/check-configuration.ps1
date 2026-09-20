# Check Tauri configuration and paths - CORRECTED FOR YOUR ACTUAL SETUP
$projectRoot = "C:\Users\Admin\OpenJarvis"
$tauriConfigPath = "C:\Users\Admin\OpenJarvis\frontend\src-tauri\tauri.conf.json"

# 1. Verify Tauri configuration file exists
if (-not (Test-Path $tauriConfigPath)) {
    Write-Warning "Tauri config file missing! Expected at: $tauriConfigPath"
    exit 1
}

$tauriConfigContent = Get-Content $tauriConfigPath -Raw | ConvertFrom-Json

# Check if paths are relative (good practice)
if ($tauriConfigContent.bundle.includeFiles) {
    $includeFiles = $tauriConfigContent.bundle.includeFiles | Where-Object { $_.from -match "\." }
    if ($includeFiles) {
        Write-Host "âœ… Tauri paths are relative (good practice)"
    } else {
        Write-Warning "âš ï¸ Tauri paths are absolute - should be relative to project root"
    }
} else {
    Write-Warning "âš ï¸ Tauri bundle configuration missing"
}

# 2. Check backend paths
$backendDir = Join-Path $projectRoot "src\openjarvis"
if (-not (Test-Path $backendDir)) {
    Write-Warning "âš ï¸ Backend directory missing: $backendDir"
} else {
    Write-Host "âœ… Backend directory exists: $backendDir"
}

# 3. Verify environment variables
$envVars = @{
    "TAURI_APP_PATH" = $projectRoot
    "TAURI_PLATFORM" = "windows"
}

foreach ($var in $envVars.Keys) {
    $value = $envVars[$var]
    $actualValue = [Environment]::GetEnvironmentVariable($var)
    
    if ($actualValue -ne $value) {
        Write-Warning "âš ï¸ Environment variable $var is set to '$actualValue' instead of '$value'"
    } else {
        Write-Host "âœ… Environment variable $var set correctly"
    }
}

# 4. Check if backend is running on correct port
$backendPort = 8010
$testUrl = "http://localhost:$backendPort/v1/agents"

try {
    $response = Invoke-RestMethod -Uri $testUrl -Method Get -ErrorAction Stop
    Write-Host "âœ… Backend is running and accessible at $testUrl"
    
    # Check if agents are registered
    if ($response.registered -and $response.registered.Count -gt 0) {
        Write-Host "âœ… Agents registered: $($response.registered -join ',')"
    } else {
        Write-Warning "âš ï¸ No agents registered in backend"
    }
} catch {
    Write-Warning "âš ï¸ Backend not accessible at $testUrl"
}

# 5. Check Tauri build configuration
$buildDir = Join-Path $projectRoot "frontend\src-tauri\target\release\bundle"
if (-not (Test-Path $buildDir)) {
    Write-Host "âš ï¸ Build directory not found (expected at $buildDir)"
} else {
    Write-Host "âœ… Build directory exists: $buildDir"
}

# 6. Check for stale build artifacts
$staleArtifacts = @(
    "frontend\src-tauri\target\debug"
    "frontend\src-tauri\target\release\bundle\nsis\OpenJarvis_0.1.0_x64-setup.exe"
)

foreach ($artifact in $staleArtifacts) {
    $path = Join-Path $projectRoot $artifact
    if (Test-Path $path) {
        Write-Host "âš ï¸ Found stale build artifact: $path"
    }
}
