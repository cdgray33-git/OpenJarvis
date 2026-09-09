<#
  openjarvis-debug-readable-v1   (script build v1b)
  W39 next-action 1.

  Converts the four unreadable [DEBUG] print() calls in cli\serve.py to
  logger.info() so they land in backend.log.

  Targets: serve.py :268 :280 :281 :513
  Leaves :552 (mojibake, 49790 chars) untouched and asserts its bytes.

  v1b fix: target line hashes are held in an ARRAY OF OBJECTS. v1 used an
  [ordered] hashtable with integer keys; OrderedDictionary indexed by an
  integer does POSITIONAL lookup, not key lookup, so every expected hash
  came back $null and all four line checks failed against an intact file.

  DRY RUN by default. Pass -Apply to write.

  Run from: PS C:\Users\Admin\OpenJarvis>
#>

param([switch]$Apply)

$ErrorActionPreference = 'Stop'

# ---------------------------------------------------------------- constants

$Target = 'C:\Users\Admin\OpenJarvis\src\openjarvis\cli\serve.py'

# Baseline measured live 09/07 immediately before this script was written.
$BASE_SHA    = '1B06ACCB2183B54E421E68F11F1C8F74F88265AA4E66BD60304271522C4FCC12'
$BASE_BYTES  = 253764
$BASE_CRLF   = 653
$BASE_BARELF = 0
$BASE_LINES  = 654
$SHA_552     = '88cfa21542a48f4075586a3884bec248a8f555940b31648f948dd1d7ac9b279f'

# Per-line SHA256 of the UTF8 bytes of each target line INCLUDING its trailing CR.
$TARGETS = @(
  [pscustomobject]@{ Line = 268; Sha = 'ff5dc8a26a69961120a57f4a1b364bea941fd1f827b568716bbd3de8b7bf2d98' }
  [pscustomobject]@{ Line = 280; Sha = '0e162968ec2fa34e093a59a995fdd5fc911a26476ca2b366def1d20423162d39' }
  [pscustomobject]@{ Line = 281; Sha = '752b8d022a85fdd8b7fadfbe65cf513da41683e29504a6a2d973f7c1c49e5ba0' }
  [pscustomobject]@{ Line = 513; Sha = 'd3cb2a54f4eda661f75e37b96d226f53ba6c5daba212c59aef5a73b0ec7ca4af' }
)
$TARGET_NUMS = @($TARGETS | ForEach-Object { $_.Line })

$MARKER = '  # openjarvis-debug-readable-v1'

$encR = New-Object System.Text.UTF8Encoding($false)   # read
$encW = New-Object System.Text.UTF8Encoding($true)    # write, RE-EMITS THE BOM

$sha = [System.Security.Cryptography.SHA256]::Create()
function Get-StrHash([string]$s) {
  (($sha.ComputeHash([System.Text.Encoding]::UTF8.GetBytes($s)) |
    ForEach-Object { $_.ToString('x2') }) -join '')
}
function Count-Endings([byte[]]$bytes) {
  $c = 0; $l = 0
  for ($i = 0; $i -lt $bytes.Length; $i++) {
    if ($bytes[$i] -eq 10) {
      if ($i -gt 0 -and $bytes[$i-1] -eq 13) { $c++ } else { $l++ }
    }
  }
  [pscustomobject]@{ CRLF = $c; BARELF = $l }
}

$fail = $false
function Check([string]$name, [bool]$ok, [string]$detail) {
  $tag = if ($ok) { 'PASS' } else { 'FAIL' }
  Write-Host ("  [{0}] {1}{2}" -f $tag, $name, $(if ($detail) { " - $detail" } else { '' }))
  if (-not $ok) { $script:fail = $true }
}

Write-Host ''
Write-Host '=== openjarvis-debug-readable-v1 (build v1b) ==='
Write-Host ("MODE: {0}" -f $(if ($Apply) { 'APPLY' } else { 'DRY RUN - nothing will be written' }))
Write-Host ("FILE: {0}" -f $Target)
Write-Host ''

# ---------------------------------------------------------------- preflight

Write-Host 'PREFLIGHT'

Check 'file exists' (Test-Path $Target) ''
if ($fail) { Write-Host ''; Write-Host 'ABORTED.'; exit 1 }

$origBytes = [System.IO.File]::ReadAllBytes($Target)
$origSha   = (Get-FileHash $Target -Algorithm SHA256).Hash
$e         = Count-Endings $origBytes

Check 'file sha matches baseline' ($origSha -eq $BASE_SHA) "got $origSha"
Check 'byte count matches baseline' ($origBytes.Length -eq $BASE_BYTES) "got $($origBytes.Length)"
Check 'BOM present' ($origBytes[0] -eq 0xEF -and $origBytes[1] -eq 0xBB -and $origBytes[2] -eq 0xBF) ''
Check 'CRLF count matches baseline' ($e.CRLF -eq $BASE_CRLF) "got $($e.CRLF)"
Check 'bare LF count matches baseline' ($e.BARELF -eq $BASE_BARELF) "got $($e.BARELF)"

try {
  $strict = New-Object System.Text.UTF8Encoding($false, $true)
  [void]$strict.GetString($origBytes)
  Check 'strict UTF-8 decode' $true ''
} catch {
  Check 'strict UTF-8 decode' $false 'file contains invalid UTF-8'
}

$text  = [System.IO.File]::ReadAllText($Target, $encR)
$lines = $text -split "`n"

Check 'line count matches baseline' ($lines.Count -eq $BASE_LINES) "got $($lines.Count)"
Check ':552 hash matches baseline (mojibake line untouched)' `
      ((Get-StrHash $lines[551]) -eq $SHA_552) ''

foreach ($t in $TARGETS) {
  $n   = $t.Line
  $got = Get-StrHash $lines[$n-1]
  Check (":$n hash matches baseline") ($got -eq $t.Sha) "got $got"
}

if ($fail) {
  Write-Host ''
  Write-Host 'PREFLIGHT FAILED. Nothing was written. The file is not in the state this'
  Write-Host 'patch was built against. Re-measure before proceeding.'
  exit 1
}

Write-Host ''
Write-Host 'TRANSFORM'

# ---------------------------------------------------------------- transform

$newLines = $lines.Clone()

foreach ($t in $TARGETS) {
  $n        = $t.Line
  $raw      = $lines[$n-1]
  $hadCR    = $raw.EndsWith("`r")
  $stripped = $raw.TrimEnd("`r")

  if ($stripped -notmatch '^\s*print\(') {
    Check (":$n starts with bare print(") $false 'unexpected shape'
    continue
  }

  # Preserve indentation and the f-string exactly. Only the call and the
  # flush kwarg change.
  $new = $stripped -replace '^(\s*)print\(', '$1logger.info('
  $new = $new -replace ',\s*flush\s*=\s*True\s*\)\s*$', ')'

  $ok = ($new -notmatch 'flush\s*=') -and `
        ($new -notmatch '(?<!\.)\bprint\(') -and `
        ($new -match 'logger\.info\(')
  Check (":$n transform well-formed") $ok ''

  $new = $new + $MARKER
  if ($hadCR) { $new = $new + "`r" }
  $newLines[$n-1] = $new

  Write-Host ''
  Write-Host ("  --- :$n")
  Write-Host ("  OLD: " + $stripped)
  Write-Host ("  NEW: " + $new.TrimEnd("`r"))
}

if ($fail) {
  Write-Host ''
  Write-Host 'TRANSFORM FAILED. Nothing was written.'
  exit 1
}

$newText = ($newLines -join "`n")

$newBytesPreview = $encW.GetPreamble() + $encW.GetBytes($newText)
$eNew            = Count-Endings $newBytesPreview
$newLinesSplit   = $newText -split "`n"

Write-Host ''
Write-Host 'POST-TRANSFORM CHECKS (in memory)'
Check 'line count unchanged' ($newLinesSplit.Count -eq $BASE_LINES) "got $($newLinesSplit.Count)"
Check 'CRLF count unchanged' ($eNew.CRLF -eq $BASE_CRLF) "got $($eNew.CRLF)"
Check 'bare LF count unchanged' ($eNew.BARELF -eq $BASE_BARELF) "got $($eNew.BARELF)"
Check ':552 hash unchanged' ((Get-StrHash $newLinesSplit[551]) -eq $SHA_552) ''
Check 'BOM will be re-emitted' ($newBytesPreview[0] -eq 0xEF -and $newBytesPreview[1] -eq 0xBB -and $newBytesPreview[2] -eq 0xBF) ''

$delta = $newBytesPreview.Length - $BASE_BYTES
Write-Host ("  [INFO] byte delta: {0} ({1} -> {2})" -f $delta, $BASE_BYTES, $newBytesPreview.Length)

# Every line other than the four targets must be byte-identical.
$drift = @()
for ($i = 0; $i -lt $BASE_LINES; $i++) {
  $ln = $i + 1
  if ($TARGET_NUMS -contains $ln) { continue }
  if ($lines[$i] -cne $newLinesSplit[$i]) { $drift += $ln }
}
Check 'no drift outside the four target lines' ($drift.Count -eq 0) "drifted: $($drift -join ',')"

if ($fail) {
  Write-Host ''
  Write-Host 'CHECKS FAILED. Nothing was written.'
  exit 1
}

if (-not $Apply) {
  Write-Host ''
  Write-Host 'DRY RUN COMPLETE. All checks passed. Nothing was written.'
  Write-Host 'Re-run with -Apply to make the change.'
  exit 0
}

# ---------------------------------------------------------------- apply

Write-Host ''
Write-Host 'APPLY'

$ts  = Get-Date -Format 'yyyyMMdd-HHmmss'
$bak = "$Target.bak_debugreadable_$ts"
Copy-Item $Target $bak -Force
$bakSha = (Get-FileHash $bak -Algorithm SHA256).Hash
Check 'backup taken and byte-identical' ($bakSha -eq $BASE_SHA) $bak

if ($fail) { Write-Host ''; Write-Host 'BACKUP FAILED. File not modified.'; exit 1 }

[System.IO.File]::WriteAllText($Target, $newText, $encW)

# ---------------------------------------------------------------- verify

Write-Host ''
Write-Host 'VERIFY ON DISK'

$vBytes = [System.IO.File]::ReadAllBytes($Target)
$vE     = Count-Endings $vBytes
$vText  = [System.IO.File]::ReadAllText($Target, $encR)
$vLines = $vText -split "`n"

Check 'BOM present on disk' ($vBytes[0] -eq 0xEF -and $vBytes[1] -eq 0xBB -and $vBytes[2] -eq 0xBF) ''
Check 'byte count as predicted' ($vBytes.Length -eq $newBytesPreview.Length) "got $($vBytes.Length)"
Check 'line count unchanged' ($vLines.Count -eq $BASE_LINES) "got $($vLines.Count)"
Check 'CRLF unchanged' ($vE.CRLF -eq $BASE_CRLF) "got $($vE.CRLF)"
Check 'bare LF unchanged' ($vE.BARELF -eq $BASE_BARELF) "got $($vE.BARELF)"
Check ':552 bytes identical to baseline' ((Get-StrHash $vLines[551]) -eq $SHA_552) ''

$stillPrint = 0
foreach ($t in $TARGETS) {
  $s = $vLines[$t.Line - 1].TrimEnd("`r")
  if ($s -match '(?<!\.)\bprint\(') { $stillPrint++ }
  Write-Host ("  :" + $t.Line + " -> " + $s)
}
Check 'no bare print() remains on the four lines' ($stillPrint -eq 0) ''

# console.print sites must be untouched: 18 expected.
$consoleCount = ([regex]::Matches($vText, 'console\.print\(')).Count
Check 'console.print sites intact (18 expected)' ($consoleCount -eq 18) "got $consoleCount"

# ---------------------------------------------------------------- compile

Write-Host ''
Write-Host 'COMPILE'

$py = $null
foreach ($cand in @('.\.venv\Scripts\python.exe', '.\venv\Scripts\python.exe')) {
  if (Test-Path $cand) { $py = $cand; break }
}
if (-not $py) { $py = 'python' }
Write-Host ("  interpreter: {0}" -f $py)

& $py -m py_compile $Target
Check 'py_compile clean' ($LASTEXITCODE -eq 0) "exit $LASTEXITCODE"

# ---------------------------------------------------------------- report

Write-Host ''
Write-Host '=== RESULT ==='
if ($fail) {
  Write-Host 'ONE OR MORE POST-APPLY CHECKS FAILED. ROLL BACK NOW:'
} else {
  Write-Host 'PATCH APPLIED AND VERIFIED ON DISK.'
  Write-Host ''
  Write-Host 'NOT YET PROVEN: that the lines actually appear in backend.log.'
  Write-Host 'That requires a backend restart. Do not claim the instrument is'
  Write-Host 'readable until a restart has produced these lines in backend.log.'
}
Write-Host ''
Write-Host 'ROLLBACK COMMAND (add to the rollback register):'
Write-Host ("  Copy-Item '{0}' '{1}' -Force" -f $bak, $Target)
Write-Host ''
Write-Host ("NEW FILE SHA: {0}" -f (Get-FileHash $Target -Algorithm SHA256).Hash)
Write-Host ''
if ($fail) { exit 1 } else { exit 0 }
