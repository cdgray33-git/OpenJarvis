# Delete the broken one first
Remove-Item "C:\Users\Admin\OpenJarvis\frontend\apply-api-auth.ps1" -Force -ErrorAction SilentlyContinue

# Save this SIMPLE, CLEAN version
$scriptPath = "C:\Users\Admin\OpenJarvis\frontend\apply-api-auth.ps1"

$script = @'
param([switch]$DryRun)

$frontendPath = "C:\Users\Admin\OpenJarvis\frontend"
$backupDir = "$frontendPath\.backups\$(Get-Date -Format 'yyyy-MM-dd_HHmmss')"
$logFile = "$frontendPath\patch-log.txt"

function Log { param([string]$msg); $stamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"; "$stamp : $msg" | Tee-Object -FilePath $logFile -Append | Write-Host }
function LogOk { Log "OK - $args" }
function LogErr { Log "ERROR - $args"; exit 1 }

Clear-Host
Write-Host "=============================================="
Write-Host "OpenJarvis API Auth Setup"
Write-Host "=============================================="

Log "Starting..."

if (!(Test-Path $frontendPath)) { LogErr "Frontend path not found" }

Write-Host "`nStep 1: Creating Backups..."
$filesToBackup = @(
    "$frontendPath\src\lib\store.ts",
    "$frontendPath\src\components\Desktop\SettingsPanel.tsx",
    "$frontendPath\src\lib\api.ts"
)

if (!(Test-Path $backupDir)) { New-Item -ItemType Directory -Path $backupDir -Force | Out-Null }

foreach ($file in $filesToBackup) {
    if (Test-Path $file) {
        $name = Split-Path $file -Leaf
        Copy-Item $file "$backupDir\$name" -Force
        LogOk "Backed up $name"
    }
}

Write-Host "`nStep 2: Verifying Backups..."
foreach ($file in $filesToBackup) {
    $name = Split-Path $file -Leaf
    $backupFile = "$backupDir\$name"
    if ((Get-Item $file).Length -ne (Get-Item $backupFile).Length) {
        LogErr "Backup verification failed for $name"
    }
    LogOk "Verified $name"
}

if ($DryRun) {
    Write-Host "`nDRY RUN MODE - No changes applied"
    Write-Host "Backups ready at: $backupDir"
    exit 0
}

Write-Host "`nStep 3: Applying Changes..."

$storePath = "$frontendPath\src\lib\store.ts"
$panelPath = "$frontendPath\src\components\Desktop\SettingsPanel.tsx"
$apiPath = "$frontendPath\src\lib\api.ts"

try {
    $content = Get-Content $storePath -Raw
    $old = "interface Settings {`n  theme: ThemeMode;`n  apiUrl: string;`n  fontSize:"
    $new = "interface Settings {`n  theme: ThemeMode;`n  apiUrl: string;`n  apiKey?: string;`n  fontSize:"
    if ($content -match [regex]::Escape($old)) {
        $content = $content -replace [regex]::Escape($old), $new
        Set-Content $storePath $content -Encoding UTF8
        LogOk "Updated store.ts"
    }
} catch {
    LogErr "Failed to update store.ts: $_"
}

try {
    $newPanel = @'
import { useState, useEffect } from 'react';
import type React from 'react';
import { useAppStore } from '../../lib/store';

const styles: Record<string, React.CSSProperties> = {
  container: { backgroundColor: '#1e1e2e', color: '#cdd6f4', padding: 24, maxWidth: 600 },
  heading: { fontSize: 20, fontWeight: 600, marginBottom: 24, color: '#89b4fa' },
  fieldGroup: { marginBottom: 20 },
  label: { display: 'block', fontSize: 13, fontWeight: 500, color: '#a6adc8', marginBottom: 6 },
  input: { width: '100%', padding: '8px 12px', borderRadius: 6, border: '1px solid #313244', backgroundColor: '#181825', color: '#cdd6f4', fontSize: 14, outline: 'none', boxSizing: 'border-box' as const },
  toggleRow: { display: 'flex', gap: 8 },
  toggleButton: { padding: '8px 16px', borderRadius: 6, border: '1px solid #313244', backgroundColor: 'transparent', color: '#a6adc8', cursor: 'pointer', fontSize: 14, fontWeight: 500, transition: 'all 0.15s ease' },
  toggleActive: { backgroundColor: '#313244', color: '#cdd6f4', borderColor: '#89b4fa' },
  savedNotice: { marginTop: 16, padding: '8px 12px', borderRadius: 6, backgroundColor: '#1e3a2f', color: '#a6e3a1', fontSize: 13 },
  description: { fontSize: 12, color: '#6c7086', marginTop: 4 },
};

export function SettingsPanel({ onSettingsChange }: any) {
  const { settings, updateSettings } = useAppStore();
  const [saved, setSaved] = useState(false);

  useEffect(() => {
    onSettingsChange?.(settings);
    setSaved(true);
    const timer = setTimeout(() => setSaved(false), 2000);
    return () => clearTimeout(timer);
  }, [settings, onSettingsChange]);

  return (
    <div style={styles.container}>
      <h2 style={styles.heading}>Settings</h2>

      <div style={styles.fieldGroup}>
        <label style={styles.label}>API URL</label>
        <input style={styles.input} type="text" value={settings.apiUrl} onChange={(e) => updateSettings({ apiUrl: e.target.value })} placeholder="http://localhost:8000" />
      </div>

      <div style={styles.fieldGroup}>
        <label style={styles.label}>Backend API Key</label>
        <input style={styles.input} type="password" value={settings.apiKey || ''} onChange={(e) => updateSettings({ apiKey: e.target.value })} placeholder="Enter API key (optional)" />
        <div style={styles.description}>Required if your backend has authentication enabled</div>
      </div>

      <div style={styles.fieldGroup}>
        <label style={styles.label}>Theme</label>
        <div style={styles.toggleRow}>
          <button style={{ ...styles.toggleButton, ...(settings.theme === 'dark' ? styles.toggleActive : {}) }} onClick={() => updateSettings({ theme: 'dark' })}>Dark</button>
          <button style={{ ...styles.toggleButton, ...(settings.theme === 'light' ? styles.toggleActive : {}) }} onClick={() => updateSettings({ theme: 'light' })}>Light</button>
        </div>
      </div>

      {saved && <div style={styles.savedNotice}>Settings saved</div>}
    </div>
  );
}
'@
    Set-Content $panelPath $newPanel -Encoding UTF8
    LogOk "Updated SettingsPanel.tsx"
} catch {
    LogErr "Failed to update SettingsPanel.tsx: $_"
}

try {
    $apiContent = Get-Content $apiPath -Raw
    $apiContent = $apiContent -replace "headers: \{ 'Content-Type': 'application/json' \},", "headers: { 'Content-Type': 'application/json', ...getAuthHeaders() },"
    Set-Content $apiPath $apiContent -Encoding UTF8
    LogOk "Updated api.ts"
} catch {
    LogErr "Failed to update api.ts: $_"
}

Write-Host "`nStep 4: Verifying Changes..."
if ((Get-Content $storePath -Raw) -match "apiKey") { LogOk "Verified store.ts" } else { LogErr "store.ts missing apiKey" }
if ((Get-Content $panelPath -Raw) -match "useAppStore") { LogOk "Verified SettingsPanel.tsx" } else { LogErr "SettingsPanel.tsx missing useAppStore" }

Write-Host "`n=============================================="
Write-Host "SUCCESS - All changes applied!"
Write-Host "=============================================="
Write-Host "Backups: $backupDir"
Write-Host "`nNext steps:"
Write-Host "  npm run build"
Write-Host "  npm run dev"
Write-Host ""
Log "Setup complete"
'@

$script | Set-Content $scriptPath -Encoding ASCII

Write-Host "SUCCESS! Script ready!" -ForegroundColor Green
Write-Host "Location: $scriptPath" -ForegroundColor Cyan
Write-Host ""
Write-Host "Run dry-run first:"
Write-Host "  cd C:\Users\Admin\OpenJarvis\frontend" -ForegroundColor Yellow
Write-Host "  .\apply-api-auth.ps1 -DryRun" -ForegroundColor Yellow
