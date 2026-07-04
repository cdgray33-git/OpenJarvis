<#
.SYNOPSIS
    Fixes OpenJarvis TTS endpoint to use Kokoro's existing streaming endpoint (/synthesize-stream)
.DESCRIPTION
    Surgically updates speech_route.py to point to the correct Kokoro endpoint.
    Includes backup, verification, and optional formatting check.
.NOTES
    Run from OpenJarvis root: C:\Windows\System32\OpenJarvis
#>

# ======================
# CONFIGURATION
# ======================
$FilePath = "openjarvis\server\speech_route.py"
$BackupDir = "openjarvis\server\backups"
$PrettierPath = "node_modules\.bin\prettier.cmd" # Adjust if using npx/yarn

# ======================
# STEP 1: VALIDATE FILE EXISTS
# ======================
if (-Not (Test-Path $FilePath)) {
    Write-Error "❌ CRITICAL: File not found at $FilePath"
    Write-Error "   Run this script from OpenJarvis root directory"
    exit 1
}

# ======================
# STEP 2: CREATE TIMESTAMPED BACKUP
# ======================
$Timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
$BackupFile = Join-Path $BackupDir "speech_route.py.$Timestamp.bak"
if (-Not (Test-Path $BackupDir)) { New-Item -ItemType Directory -Path $BackupDir | Out-Null }
Copy-Item -Path $FilePath -Destination $BackupFile -Force
Write-Host "✅ BACKUP CREATED: $BackupFile"

# ======================
# STEP 3: READ ORIGINAL CONTENT
# ======================
$OriginalContent = Get-Content -Path $FilePath -Raw

# ======================
# STEP 4: DEFINE PRECISE TARGET FOR REPLACEMENT
# ======================
# We're replacing ONLY the endpoint in the synthesize function
$OldEndpoint = [regex]::Escape("$KOKORO_SERVER + " + "/synthesize"")
$NewEndpoint = "$KOKORO_SERVER + " + "/synthesize-stream""

# ======================
# STEP 5: VERIFY TARGET EXISTS
# ======================
if ($OriginalContent -notmatch $OldEndpoint) {
    Write-Error "❌ CRITICAL: Expected endpoint pattern not found in $FilePath"
    Write-Error "   Searched for: $OldEndpoint"
    Write-Error "   ABORTING - file may be already modified"
    exit 1
}

# ======================
# STEP 6: PERFORM REPLACEMENT
# ======================
$NewContent = $OriginalContent -replace $OldEndpoint, $NewEndpoint

# ======================
# STEP 7: VERIFY MODIFICATION
# ======================
if ($OriginalContent -eq $NewContent) {
    Write-Error "❌ CRITICAL: No changes made - replacement failed"
    exit 1
}

# ======================
# STEP 8: WRITE MODIFIED FILE
# ======================
Set-Content -Path $FilePath -Value $NewContent -Encoding UTF8
Write-Host "✅ FILE UPDATED: $FilePath"
Write-Host "   Changed: /synthesize → /synthesize-stream"

# ========================
# STEP 9: OPTIONAL FORMATTING CHECK
#======
if (Test-Path $PrettierPath) {
    Write-Host "🔍 RUNNING PRETTIER FORMATTING CHECK..."
    & $PrettierPath --check $FilePath
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ FORMATTING VALID PASSED"
    } else {
        Write-Warning "⚠️ FORMATTING ISSUES DETECTED (run prettier to fix)"
    }
} else {
    Write-Host "ℹ️ Prettier not found - skipping formatting check"
}

# ======================
# STEP 10: SHOW SUMMARY
# ======================
Write-Host "`n=== CHANGE SUMMARY ==="
Write-Host "File: $FilePath"
Write-Host "Backup: $BackupFile"
Write-Host "Modification: Updated TTS endpoint to Kokoro's streaming endpoint"
Write-Host ""
Write-Host "✅ NEXT STEPS:"
Write-Host "   1. Restart Kokoro server (see instructions below)"
Write-Host "   2. Restart OpenJarvis: .\start-openjarvis.ps1"
Write-Host "   3. Test voice response - should now speak DURING LLM output"
Write-Host ""
exit 0