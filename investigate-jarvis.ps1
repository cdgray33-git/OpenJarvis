# MARKER: openjarvis-investigate-v1
# Read-only diagnostic. Writes nothing except a transcript you can attach
# to the next chat. Never echoes the contents of any secrets file.
#
#   cd C:\Users\Admin\Openjarvis
#   .\investigate-jarvis.ps1
#
# Output goes to the console AND to .\jarvis-investigation.txt

$ErrorActionPreference = 'Continue'
$root = (Resolve-Path '.').Path
$out  = Join-Path $root 'jarvis-investigation.txt'
Start-Transcript -Path $out -Force | Out-Null

function Section($n) {
  ""
  "=" * 72
  "  $n"
  "=" * 72
}
function Try-Show($label, $block) {
  try { & $block } catch { "  [error] ${label}: $($_.Exception.Message)" }
}

"OpenJarvis investigation  --  $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
"repo root : $root"

# =====================================================================
Section "1. BACKEND LIVENESS"
Try-Show 'netstat' {
  $l = netstat -ano | Select-String ':8010.*LISTENING'
  if ($l) { "  LISTENING on 8010:"; $l | ForEach-Object { "    " + $_.Line.Trim() } }
  else { "  NOTHING listening on 8010 -- backend is down" }
}
Try-Show 'info' {
  $i = (Invoke-WebRequest 'http://127.0.0.1:8010/v1/info' -UseBasicParsing -TimeoutSec 5).Content
  "  /v1/info : $i"
}
Try-Show 'headers' {
  $h = (Invoke-WebRequest 'http://127.0.0.1:8010/' -UseBasicParsing -TimeoutSec 5).Headers
  "  CSP      : " + $h['content-security-policy']
  "  PERM     : " + $h['permissions-policy']
  "  LastMod  : " + $h['Last-Modified']
}

# =====================================================================
Section "2. FRONTEND BUILD STATE  (why does the exe not load?)"
$static = Join-Path $root 'src\openjarvis\server\static'
"  static dir: $static"
Try-Show 'static' {
  if (Test-Path $static) {
    Get-ChildItem $static -File | Select-Object Name,Length,LastWriteTime | Format-Table -AutoSize | Out-String -Width 200
    $assets = Join-Path $static 'assets'
    if (Test-Path $assets) {
      "  assets/:"
      Get-ChildItem $assets -File | Select-Object Name,Length,LastWriteTime | Format-Table -AutoSize | Out-String -Width 200
    } else { "  !! assets/ MISSING -- this alone would break both surfaces" }
  } else { "  !! static dir MISSING" }
}
"  -- index.html asset references (must match files above) --"
Try-Show 'index refs' {
  $idx = Join-Path $static 'index.html'
  if (Test-Path $idx) {
    Select-String -Path $idx -Pattern 'src=|href=' | ForEach-Object { "    " + $_.Line.Trim() }
  } else { "  !! index.html MISSING" }
}
"  -- vite config (outDir / emptyOutDir) --"
Try-Show 'vite' {
  Get-ChildItem (Join-Path $root 'frontend') -Filter 'vite.config.*' -File |
    ForEach-Object { Select-String -Path $_.FullName -Pattern 'outDir|emptyOutDir|base|root' } |
    ForEach-Object { "    {0}:{1}: {2}" -f $_.Filename, $_.LineNumber, $_.Line.Trim() }
}
"  -- package.json build scripts --"
Try-Show 'pkg' {
  $pkg = Join-Path $root 'frontend\package.json'
  if (Test-Path $pkg) {
    (Get-Content $pkg -Raw | ConvertFrom-Json).scripts.PSObject.Properties |
      ForEach-Object { "    {0,-18} = {1}" -f $_.Name, $_.Value }
  }
}

# =====================================================================
Section "3. TAURI / DESKTOP EXECUTABLE"
Try-Show 'tauri conf' {
  $tc = Join-Path $root 'frontend\src-tauri\tauri.conf.json'
  if (Test-Path $tc) {
    $j = Get-Content $tc -Raw | ConvertFrom-Json
    "  productName    : $($j.productName)"
    "  version        : $($j.version)"
    "  identifier     : $($j.identifier)"
    "  frontendDist   : $($j.build.frontendDist)"
    "  devUrl         : $($j.build.devUrl)"
    "  beforeBuildCmd : $($j.build.beforeBuildCommand)"
    "  beforeDevCmd   : $($j.build.beforeDevCommand)"
    "  windows[0].url : $($j.app.windows[0].url)"
  } else { "  !! tauri.conf.json not found" }
}
"  -- does frontendDist resolve to a directory that actually has files? --"
Try-Show 'dist resolve' {
  $tc = Join-Path $root 'frontend\src-tauri\tauri.conf.json'
  $j  = Get-Content $tc -Raw | ConvertFrom-Json
  $fd = $j.build.frontendDist
  if ($fd) {
    $resolved = Join-Path (Join-Path $root 'frontend\src-tauri') $fd
    "  declared : $fd"
    "  resolves : $resolved"
    if (Test-Path $resolved) {
      $n = (Get-ChildItem $resolved -Recurse -File).Count
      "  EXISTS, $n files"
      if ($n -eq 0) { "  !! EMPTY -- a tauri build against this produces a blank window" }
    } else { "  !! DOES NOT EXIST -- tauri build would fail or embed nothing" }
  }
}
"  -- built executables on disk --"
Try-Show 'exe' {
  $rel = Join-Path $root 'frontend\src-tauri\target\release'
  if (Test-Path $rel) {
    Get-ChildItem $rel -Filter '*.exe' -File -ErrorAction SilentlyContinue |
      Select-Object Name,Length,LastWriteTime | Format-Table -AutoSize | Out-String -Width 200
    $bundle = Join-Path $rel 'bundle'
    if (Test-Path $bundle) {
      "  bundle/:"
      Get-ChildItem $bundle -Recurse -Include '*.exe','*.msi' -File |
        Select-Object FullName,Length,LastWriteTime | Format-Table -AutoSize | Out-String -Width 200
    }
  } else { "  no target\release -- the exe has never been built from this tree" }
}
Try-Show 'installed' {
  $c = Get-ChildItem 'C:\Users\Admin\AppData\Local' -Filter '*OpenJarvis*' -Directory -ErrorAction SilentlyContinue
  if ($c) { "  AppData dirs:"; $c | ForEach-Object { "    " + $_.FullName } }
}
"  -- WebView2 runtime (Tauri needs it; a missing/broken runtime = blank window) --"
Try-Show 'webview2' {
  $k = 'HKLM:\SOFTWARE\WOW6432Node\Microsoft\EdgeUpdate\Clients\{F3017226-FE2A-4295-8BDF-00C3A9A7E4C5}'
  if (Test-Path $k) { "  WebView2 version: " + (Get-ItemProperty $k).pv }
  else { "  !! WebView2 runtime key not found" }
}

# =====================================================================
Section "4. AGENTS  (where did the email agent migration stop?)"
"  -- agent-related source files --"
Try-Show 'agent files' {
  Get-ChildItem $root -Recurse -Include '*.py','*.ts','*.tsx','*.toml','*.json' -File `
    -ErrorAction SilentlyContinue |
    Where-Object { $_.FullName -notmatch 'node_modules|\\target\\|\.git\\|__pycache__' -and
                   $_.Name -match 'agent' } |
    Select-Object FullName,Length,LastWriteTime |
    Sort-Object LastWriteTime -Descending | Format-Table -AutoSize | Out-String -Width 250
}
"  -- email / mail references (file:line only) --"
Try-Show 'email refs' {
  Get-ChildItem $root -Recurse -Include '*.py','*.ts','*.tsx' -File -ErrorAction SilentlyContinue |
    Where-Object { $_.FullName -notmatch 'node_modules|\\target\\|\.git\\|__pycache__' } |
    Select-String -Pattern 'imap|smtp|yahoo|gmail|mailbox|EmailAgent|email_agent' -List |
    ForEach-Object { "    {0}:{1}" -f $_.Path.Replace($root,'.'), $_.LineNumber } |
    Select-Object -First 60
}
"  -- live agent endpoints --"
Try-Show 'agent api' {
  $spec = (Invoke-WebRequest 'http://127.0.0.1:8010/openapi.json' -UseBasicParsing -TimeoutSec 8).Content | ConvertFrom-Json
  $spec.paths.PSObject.Properties.Name | Where-Object { $_ -match 'agent|mail|task|schedul' } |
    Sort-Object | ForEach-Object { "    $_" }
}
Try-Show 'managed-agents' {
  $r = Invoke-WebRequest 'http://127.0.0.1:8010/v1/managed-agents' -UseBasicParsing -TimeoutSec 8
  "  /v1/managed-agents -> $($r.StatusCode), $($r.RawContentLength) bytes"
  $j = $r.Content | ConvertFrom-Json
  if ($j -is [array]) { "  count: $($j.Count)"; $j | ForEach-Object { "    - " + $(if ($_.name) { $_.name } elseif ($_.id) { $_.id } else { '<unnamed>' }) } }
  else { $j.PSObject.Properties.Name | ForEach-Object { "    key: $_" } }
}

# =====================================================================
Section "5. MODEL OVERRIDE  (config.toml says one thing, /v1/info another)"
Try-Show 'config model' {
  $cfg = Join-Path $root 'config.toml'
  if (Test-Path $cfg) {
    Select-String -Path $cfg -Pattern 'model|engine|ollama|host' |
      ForEach-Object { "    {0}: {1}" -f $_.LineNumber, $_.Line.Trim() }
  }
}
"  -- environment variables SET in this shell (names only, values suppressed) --"
Try-Show 'env names' {
  Get-ChildItem Env: | Where-Object { $_.Name -match 'OLLAMA|MODEL|LITELLM|OPENJARVIS|JARVIS' } |
    ForEach-Object { "    {0} = <set, {1} chars>" -f $_.Name, $_.Value.Length }
}
"  -- other places a model name is hardcoded (file:line only) --"
Try-Show 'model refs' {
  Get-ChildItem $root -Recurse -Include '*.py','*.toml','*.ps1','*.json' -File -ErrorAction SilentlyContinue |
    Where-Object { $_.FullName -notmatch 'node_modules|\\target\\|\.git\\|__pycache__' } |
    Select-String -Pattern 'qwen3-coder|qwen2\.5-coder' |
    ForEach-Object { "    {0}:{1}" -f $_.Path.Replace($root,'.'), $_.LineNumber } |
    Select-Object -First 40
}

# =====================================================================
Section "6. SECRETS FILE  (shape only -- no values, ever)"
Try-Show 'dotenv' {
  $envf = Join-Path $root '.env'
  if (Test-Path $envf) {
    $lines = Get-Content $envf
    $valid = ($lines | Where-Object { $_ -match '^\s*[A-Za-z_][A-Za-z0-9_]*\s*=' }).Count
    "    .env total lines : $($lines.Count)"
    "    valid KEY=value  : $valid"
    "    parses cleanly   : $($valid -eq ($lines | Where-Object { $_.Trim() -ne '' -and $_ -notmatch '^\s*#' }).Count)"
  } else { "    no .env at repo root" }
}

# =====================================================================
Section "7. ROLLBACK INVENTORY"
Try-Show 'baks' {
  Get-ChildItem $root -Recurse -Filter '*.bak_*' -File -ErrorAction SilentlyContinue |
    Where-Object { $_.FullName -notmatch 'node_modules|\\target\\' } |
    Select-Object @{n='Path';e={$_.FullName.Replace($root,'.')}},Length,LastWriteTime |
    Sort-Object LastWriteTime -Descending | Format-Table -AutoSize | Out-String -Width 250
}
Try-Show 'memorydb' {
  Get-ChildItem $root -Recurse -Filter 'memory.db*' -File -ErrorAction SilentlyContinue |
    Select-Object @{n='Path';e={$_.FullName.Replace($root,'.')}},Length,LastWriteTime |
    Format-Table -AutoSize | Out-String -Width 250
}

Section "DONE"
"  Transcript written to: $out"
Stop-Transcript | Out-Null
