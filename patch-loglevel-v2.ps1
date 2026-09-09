# patch-loglevel-v2.ps1
# W42 - single patch: INFO level route, 40 MB total backend.log budget, credential redaction.
# Dry run by default. Use -Apply to write.
#
# Run from: PS C:\Users\Admin\OpenJarvis>
#   powershell -ExecutionPolicy Bypass -File .\patch-loglevel-v2.ps1
#   powershell -ExecutionPolicy Bypass -File .\patch-loglevel-v2.ps1 -Apply

[CmdletBinding()]
param([switch]$Apply)

$ErrorActionPreference = 'Stop'
$stamp = Get-Date -Format 'yyyyMMdd-HHmmss'

$LOGCFG = 'C:\Users\Admin\OpenJarvis\src\openjarvis\cli\log_config.py'
$SERVE  = 'C:\Users\Admin\OpenJarvis\src\openjarvis\cli\serve.py'
$START  = 'C:\Users\Admin\OpenJarvis\start-openjarvis.ps1'

function Read-FileParts {
    param([string]$Path)
    $bytes = [System.IO.File]::ReadAllBytes($Path)
    $hasBom = ($bytes.Length -ge 3 -and $bytes[0] -eq 0xEF -and $bytes[1] -eq 0xBB -and $bytes[2] -eq 0xBF)
    $start = 0; if ($hasBom) { $start = 3 }
    $text = [System.Text.Encoding]::UTF8.GetString($bytes, $start, $bytes.Length - $start)
    $nl = "`n"; if ($text -match "`r`n") { $nl = "`r`n" }
    $trailing = $false
    if ($text.EndsWith($nl)) { $trailing = $true; $text = $text.Substring(0, $text.Length - $nl.Length) }
    $lines = [System.Collections.ArrayList]::new()
    foreach ($l in ($text -split [regex]::Escape($nl))) { [void]$lines.Add($l) }
    [pscustomobject]@{ Path=$Path; Lines=$lines; Nl=$nl; Bom=$hasBom; Trailing=$trailing }
}

function Write-FileParts {
    param($Parts)
    $text = ($Parts.Lines -join $Parts.Nl)
    if ($Parts.Trailing) { $text += $Parts.Nl }
    $enc = New-Object System.Text.UTF8Encoding($Parts.Bom)
    [System.IO.File]::WriteAllText($Parts.Path, $text, $enc)
}

function Get-LineHash {
    param([string]$Line)
    $sha = [System.Security.Cryptography.SHA256]::Create()
    $h = $sha.ComputeHash([System.Text.Encoding]::UTF8.GetBytes($Line))
    ($h | ForEach-Object { $_.ToString('x2') }) -join ''
}

function Assert-Line {
    param($Parts, [int]$Num, [string]$Expected)
    $actual = $Parts.Lines[$Num - 1]
    if ($actual -ne $Expected) {
        Write-Host ("ANCHOR FAILED: {0} line {1}" -f $Parts.Path, $Num) -ForegroundColor Red
        Write-Host ("  expected: [{0}]" -f $Expected) -ForegroundColor Red
        Write-Host ("  actual:   [{0}]" -f $actual) -ForegroundColor Red
        throw 'Anchor mismatch. No file was modified.'
    }
}

Write-Host ''
Write-Host '=== ANCHOR VERIFICATION ===' -ForegroundColor Cyan

$cfg = Read-FileParts $LOGCFG
Assert-Line $cfg 5  'import logging'
Assert-Line $cfg 50 '    if quiet:'
Assert-Line $cfg 51 '        level = logging.ERROR'
Assert-Line $cfg 52 '    elif verbose:'
Assert-Line $cfg 53 '        level = logging.DEBUG'
Assert-Line $cfg 54 '    else:'
Assert-Line $cfg 55 '        level = logging.WARNING'
Write-Host ("log_config.py  OK  (BOM={0}, lines={1})" -f $cfg.Bom, $cfg.Lines.Count) -ForegroundColor Green

$srv = Read-FileParts $SERVE
Assert-Line $srv 61 '        log_path, maxBytes=4 * 1024 * 1024, backupCount=3, encoding="utf-8"'
Assert-Line $srv 63 '    file_handler.setFormatter('
Assert-Line $srv 64 '        logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s")'
Assert-Line $srv 65 '    )'
if ($srv.Lines.Count -lt 552) { throw 'serve.py has fewer than 552 lines. Aborting.' }
$canaryBefore = Get-LineHash $srv.Lines[551]
$canaryLen = $srv.Lines[551].Length
Write-Host ("serve.py       OK  (BOM={0}, lines={1})" -f $srv.Bom, $srv.Lines.Count) -ForegroundColor Green
Write-Host ("  :552 canary  len={0}  sha256={1}" -f $canaryLen, $canaryBefore) -ForegroundColor Yellow

$st = Read-FileParts $START
Assert-Line $st 29 '# Start server'
Assert-Line $st 30 'Write-Host "Starting server on port 8010..." -ForegroundColor Cyan'
Assert-Line $st 31 '& "C:\Users\Admin\OpenJarvis\.venv\Scripts\python.exe" -m openjarvis.cli serve --port 8010'
Write-Host ("start-openjarvis.ps1 OK  (BOM={0}, lines={1})" -f $st.Bom, $st.Lines.Count) -ForegroundColor Green

# ---- edits ----

$cfgL5 = @('import logging', 'import os')

$cfgLadder = @(
'    _env_level = logging.getLevelName(',
'        os.environ.get("OPENJARVIS_LOG_LEVEL", "WARNING").strip().upper()',
'    )',
'    if not isinstance(_env_level, int):',
'        _env_level = logging.WARNING',
'',
'    if quiet:',
'        level = logging.ERROR',
'    elif verbose:',
'        level = logging.DEBUG',
'    else:',
'        level = _env_level'
)

$srvL61 = '        log_path, maxBytes=10 * 1024 * 1024, backupCount=3, encoding="utf-8"'

$srvFormatter = @(
'    from openjarvis.cli.log_config import SanitizingFormatter',
'',
'    file_handler.setFormatter(',
'        SanitizingFormatter("%(asctime)s %(levelname)s %(name)s: %(message)s")',
'    )'
)

$startEnv = @(
'# Route the openjarvis logger tree at INFO (see log_config.setup_logging)',
'$env:OPENJARVIS_LOG_LEVEL = "INFO"'
)

Write-Host ''
Write-Host '=== PLANNED CHANGES ===' -ForegroundColor Cyan
Write-Host 'log_config.py L5     : add "import os"'
Write-Host 'log_config.py L50-55 : env-driven default level, WARNING when unset; flags still win'
Write-Host 'serve.py     L61     : maxBytes 4 MB -> 10 MB (40 MB total with backupCount=3)'
Write-Host 'serve.py     L63-65  : logging.Formatter -> SanitizingFormatter (credential redaction)'
Write-Host 'start-*.ps1  L31     : set OPENJARVIS_LOG_LEVEL=INFO before launch'

if (-not $Apply) {
    Write-Host ''
    Write-Host 'DRY RUN. Nothing written. Re-run with -Apply to commit these changes.' -ForegroundColor Yellow
    exit 0
}

Write-Host ''
Write-Host '=== APPLYING ===' -ForegroundColor Cyan

Copy-Item $LOGCFG "$LOGCFG.bak_loglevel_$stamp" -Force
Copy-Item $SERVE  "$SERVE.bak_loglevel_$stamp"  -Force
Copy-Item $START  "$START.bak_loglevel_$stamp"  -Force
Write-Host 'Backups created.' -ForegroundColor Green

# log_config.py : do the later edit first so indices stay valid
$cfg.Lines.RemoveRange(49, 6)
$cfg.Lines.InsertRange(49, [string[]]$cfgLadder)
$cfg.Lines.RemoveAt(4)
$cfg.Lines.InsertRange(4, [string[]]$cfgL5)
Write-FileParts $cfg

# serve.py
$srv.Lines.RemoveRange(62, 3)
$srv.Lines.InsertRange(62, [string[]]$srvFormatter)
$srv.Lines[60] = $srvL61
Write-FileParts $srv

# start-openjarvis.ps1
$st.Lines.InsertRange(29, [string[]]$startEnv)
Write-FileParts $st

Write-Host 'Files written.' -ForegroundColor Green

Write-Host ''
Write-Host '=== POST-WRITE VERIFICATION ===' -ForegroundColor Cyan

$srv2 = Read-FileParts $SERVE
$expectedCanary = 552 + ($srvFormatter.Count - 3)
$canaryAfter = Get-LineHash $srv2.Lines[$expectedCanary - 1]
if ($canaryAfter -ne $canaryBefore) {
    Write-Host ':552 CANARY HASH CHANGED. ENCODING DAMAGE. ROLL BACK NOW.' -ForegroundColor Red
    Write-Host ("  before={0}" -f $canaryBefore) -ForegroundColor Red
    Write-Host ("  after ={0}" -f $canaryAfter) -ForegroundColor Red
} else {
    Write-Host (":552 canary INTACT (now line {0}), sha256 unchanged." -f $expectedCanary) -ForegroundColor Green
}
if ($srv2.Bom -ne $srv.Bom) { Write-Host 'BOM STATE CHANGED ON serve.py.' -ForegroundColor Red }
else { Write-Host ("serve.py BOM preserved (BOM={0})." -f $srv2.Bom) -ForegroundColor Green }

Write-Host ''
& 'C:\Users\Admin\OpenJarvis\.venv\Scripts\python.exe' -m py_compile $LOGCFG $SERVE
if ($LASTEXITCODE -eq 0) { Write-Host 'py_compile OK for both modules.' -ForegroundColor Green }
else { Write-Host 'py_compile FAILED. Roll back.' -ForegroundColor Red }

Write-Host ''
Write-Host '=== ROLLBACK COMMANDS ===' -ForegroundColor Cyan
Write-Host ("Copy-Item '{0}.bak_loglevel_{1}' '{0}' -Force" -f $LOGCFG, $stamp)
Write-Host ("Copy-Item '{0}.bak_loglevel_{1}' '{0}' -Force" -f $SERVE, $stamp)
Write-Host ("Copy-Item '{0}.bak_loglevel_{1}' '{0}' -Force" -f $START, $stamp)
Write-Host ''
