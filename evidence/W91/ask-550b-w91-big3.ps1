# ask-550b-w91-big3.ps1  (W91)
# Pattern reused from ask-550b-554.ps1 (tooling register s8). READ-ONLY against the worktree.
# Reads the three conflicted frontend files (diff3 markers) from the upgrade worktree, embeds the
# question at the top, posts to the 550B on OpenRouter (paid, then :free fallback), and writes the
# bundle and the answer to evidence\W91\ (one home per data type).
# Run from PS C:\Users\Admin\OpenJarvis> as:
#   powershell -ExecutionPolicy Bypass -File 'C:\Users\Admin\OpenJarvis\evidence\W91\ask-550b-w91-big3.ps1'

$ErrorActionPreference = 'Stop'
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

$root   = 'C:\Users\Admin\OpenJarvis'
$wt     = 'C:\Users\Admin\OpenJarvis-upgrade'
$outdir = Join-Path $root 'evidence\W91'
$keyf   = 'C:\Users\Admin\.openjarvis\cloud-keys.env'
$models = @('nvidia/nemotron-3-ultra-550b-a55b', 'nvidia/nemotron-3-ultra-550b-a55b:free')
$stamp  = Get-Date -Format 'yyyyMMdd-HHmmss'
$bundle = Join-Path $outdir ("bundle-550b-big3-$stamp.md")
$answer = Join-Path $outdir ("ANSWER-550b-big3-$stamp.md")
$utf8   = New-Object System.Text.UTF8Encoding($false)
New-Item -ItemType Directory -Force -Path $outdir | Out-Null

# path, expected diff3 hunk count, fence language
$files = @(
  @('frontend/src-tauri/src/lib.rs', 15, 'rust'),
  @('frontend/src/components/Chat/ChatArea.tsx', 3, 'tsx'),
  @('frontend/src/components/Chat/InputArea.tsx', 8, 'tsx')
)

$question = @'
# TASK BRIEF FOR THE MODEL

You are resolving git merge conflicts in three files of a Tauri 2 + React desktop app called
OpenJarvis. Each file below is the REAL conflicted working copy with 1-based line numbers.
Answer the four numbered questions at the end. Cite a line number for every claim.

## HOW TO READ THE MARKERS (diff3 style) - DO NOT MISREAD

    <<<<<<< ours      -> start of OURS  (Graystone fork, commit 3df27c53)
    ||||||| base      -> start of BASE  (common ancestor, author commit af21bc18)
    =======           -> start of THEIRS (author upstream, commit a6dcf846)
    >>>>>>> theirs    -> end of hunk

The section between `||||||| base` and `=======` is BASE. It is NOT ours. Text outside markers
has already merged cleanly and is present in the result regardless of your decisions.

## ESTABLISHED FACTS - DO NOT RE-DERIVE OR CONTRADICT

1. Directive: adopt the AUTHOR's structure and keep ONLY the Graystone layer the author lacks.
2. Graft artifact: our real history starts from a 2026-05-30 author snapshot that was grafted
   onto af21bc18. Author code added between that snapshot and af21bc18 therefore appears as
   "deleted by ours". Such hunks are NOT Graystone intent. Each file lists our real commits.
3. Already decided in other files (treat as fixed):
   - api.ts: author `export const apiFetch(path, init)` prepends getBase() and adds auth.
     Our full-URL apiFetch and getAuthHeaders are REMOVED. Author `authHeaders`, `getApiKey`,
     `getInferenceSource`, `setInferenceSource`, approvals API are present. Our `confirmTool`
     (Defect 6 confirmation gate, POST /v1/tools/confirm) is kept.
   - sse.ts: `streamChat(request, signal)` keeps OUR single POST inside try with a 30 s
     timeout (taking the author's hunk would have sent every chat request TWICE).
     `streamResearch(query, model?, signal?)` uses the AUTHOR signature.
     `ResearchEvent` is exported from sse.ts as an alias of SSEEvent, NOT from ../types.
   - store.ts: author `apiKey: string` (required) in settings; conversation save keeps our
     `persist` flag plus the author `activeId === conversationId` guard.
   - tauri.conf.json: OUR CSP allowlist is kept (connect-src localhost, 127.0.0.1,
     172.16.33.200, ipc.localhost; media-src blob: data:). No arbitrary external hosts.
   - App.tsx: no analytics `track` calls (Graystone removed PostHog analytics deliberately).
   - Toolchain after merge: TypeScript ~7.0, Vite 8, React 19.3, lucide-react 1.46, motion 13.
4. Graystone layer that MUST survive:
   - ChatArea.tsx: OURS owns the send flow: the TTS driver (AudioContext playback engine in
     ../audio/ttsPlayer, chunked synthesis while streaming), the stop control, the backend
     liveness probe, and file attachments. Port the author's `isCurrentChatStreaming` /
     `conversationId` handling into our flow.
   - InputArea.tsx: OURS is a full rewrite: useSpeechStream WebSocket STT, attachments, agent
     selector, stop. Planned approach: take OURS whole and port author deltas only where the
     store/types or the kept APIs above require it. Confirm or refute this plan per hunk.
   - lib.rs: take the AUTHOR boot rewrite (inference-source consent, boot_plan, owned child
     processes, keyring). Re-apply on top of it: backend port 8010 (JARVIS_PORT; author uses
     8000), remote Ollama at http://172.16.33.200:11434 (ours: configured_ollama_host with an
     http:// prefix fix; the author path may be SourceKind::Custom or config), the DISABLED
     automatic repo clone, the find_project_root fallback path, and the removal of `uv sync`
     and startup model checks from the boot sequence (our commit 383ccd5e).

## THE QUESTIONS

**1. PER-HUNK DECISION.** For every conflict hunk in each file, numbered in order of appearance
(h01, h02, ...) with the line number of its `<<<<<<< ours` marker, give exactly one of:
OURS / THEIRS / COMBINE / DROP-BOTH, and a one-line reason. For COMBINE, give the exact
resolved text in a fenced block. Say explicitly when a hunk is a graft artifact.

**2. CLEAN-REGION BREAKAGE.** Under your resolution, list every identifier in the clean
(unmarked) text that becomes undefined, duplicated, or unused in a way that fails the build
(TypeScript strict with noUnusedLocals, or a Rust compile error). Give line numbers.

**3. LIB.RS PLACEMENT.** For each Graystone behavior listed for lib.rs, state where it must
live in the author's new boot structure (function name and line), and whether the author
already provides an equivalent mechanism that makes our change unnecessary.

**4. SILENT-FAILURE RISKS.** List anything where the merged result would compile but
misbehave at runtime (duplicate requests, handlers never wired, lost cleanup, races, port or
host mismatches), in the style of the double-POST found in sse.ts.

## OUTPUT RULES

- Four numbered sections. No preamble, no closing summary.
- Cite `file:line` for every structural claim.
- If the files do not contain the information needed, say "insufficient information" rather
  than guessing.

---

'@

# ---------- build the bundle (real bytes, read-only) ----------
$sb = New-Object System.Text.StringBuilder
[void]$sb.AppendLine($question)
foreach ($f in $files) {
  $p = Join-Path $wt ($f[0] -replace '/','\')
  $txt = [IO.File]::ReadAllText($p, $utf8)
  $ls = $txt -split "`n"
  $n = @($ls | Where-Object { $_ -like '<<<<<<< *' }).Count
  Write-Host ("FILE:   {0} lines={1} hunks={2} expected={3}" -f $f[0], $ls.Count, $n, $f[1])
  if ($n -ne $f[1]) { throw "Hunk count mismatch in $($f[0]) - aborting before send." }
  if ($txt -match 'sk-or-v1-[0-9a-fA-F]{20,}|sk-ant-[A-Za-z0-9_-]{20,}|AKIA[0-9A-Z]{16}|ghp_[A-Za-z0-9]{30,}') {
    throw "Secret-like pattern found in $($f[0]) - aborting before send."
  }
  $commits = & git -C $wt --no-replace-objects --no-pager log --format='%h %ad %s' --date=short HEAD -- $f[0]
  [void]$sb.AppendLine("# FILE: $($f[0])  ($n conflict hunks, diff3)")
  [void]$sb.AppendLine('')
  [void]$sb.AppendLine('## Our real commits touching this file (graft off, newest first)')
  foreach ($c in $commits) { [void]$sb.AppendLine("- $c") }
  [void]$sb.AppendLine('')
  [void]$sb.AppendLine('```' + $f[2])
  for ($i = 1; $i -le $ls.Count; $i++) {
    $t = $ls[$i-1].TrimEnd("`r")
    if ($t.Length -gt 400) { $t = $t.Substring(0,400) + " ...[TRUNCATED, original length $($ls[$i-1].Length)]" }
    [void]$sb.AppendLine(("{0}: {1}" -f $i, $t))
  }
  [void]$sb.AppendLine('```')
  [void]$sb.AppendLine('')
}
$content = $sb.ToString()
[IO.File]::WriteAllText($bundle, $content, $utf8)
Write-Host ("BUNDLE: {0} ({1} KB) SHA256={2}" -f $bundle, [math]::Round((Get-Item -LiteralPath $bundle).Length/1KB,1), (Get-FileHash -LiteralPath $bundle -Algorithm SHA256).Hash)

# ---------- key, read silently ----------
if (-not (Test-Path -LiteralPath $keyf)) { throw "Key file not found: $keyf" }
$kl = Get-Content -LiteralPath $keyf | Where-Object { $_ -match '^\s*OPENROUTER_API_KEY\s*=' } | Select-Object -First 1
if (-not $kl) { throw "No OPENROUTER_API_KEY line in cloud-keys.env" }
$key = ($kl -split '=',2)[1].Trim().Trim('"').Trim("'")
Write-Host ("KEY:    found=True len={0} prefix_ok={1}" -f $key.Length, $key.StartsWith('sk-or-'))
$hdr = @{ 'Authorization' = "Bearer $key"; 'Content-Type' = 'application/json' }

# ---------- send: paid first, then :free ----------
$r = $null; $used = $null; $sw = [Diagnostics.Stopwatch]::StartNew()
foreach ($m in $models) {
  $payload = @{
    model       = $m
    max_tokens  = 16000
    temperature = 0.1
    messages    = @(@{ role = 'user'; content = $content })
  } | ConvertTo-Json -Depth 6 -Compress
  $bytes = [Text.Encoding]::UTF8.GetBytes($payload)
  Write-Host ("SEND:   model={0} payload={1} KB" -f $m, [math]::Round($bytes.Length/1KB,1))
  try {
    $r = Invoke-RestMethod -Uri 'https://openrouter.ai/api/v1/chat/completions' -Method Post -Headers $hdr -Body $bytes -TimeoutSec 1800
    $used = $m; break
  } catch {
    Write-Host ("FAILED: {0} after {1}s: {2}" -f $m, [math]::Round($sw.Elapsed.TotalSeconds,1), $_.Exception.Message) -ForegroundColor Red
    if ($_.Exception.Response) {
      try { $rd = New-Object IO.StreamReader($_.Exception.Response.GetResponseStream()); Write-Host ("BODY:   {0}" -f $rd.ReadToEnd()) -ForegroundColor Red } catch {}
    }
  }
}
$sw.Stop()
if (-not $r) { Write-Host 'ALL MODELS FAILED - no answer written.' -ForegroundColor Red; exit 1 }

$msg = $r.choices[0].message
$out = $msg.content
if ([string]::IsNullOrWhiteSpace($out) -and $msg.reasoning) { $out = "[REASONING FIELD ONLY]`r`n" + $msg.reasoning }

$hdrTxt = "# ANSWER: W91 big-three merge (lib.rs, ChatArea.tsx, InputArea.tsx)`r`nmodel: $used`r`nasked: $stamp`r`nelapsed: $([math]::Round($sw.Elapsed.TotalSeconds,1))s`r`nfinish: $($r.choices[0].finish_reason)`r`nusage: $($r.usage | ConvertTo-Json -Compress)`r`nbundle: $bundle`r`n`r`n---`r`n`r`n"
[IO.File]::WriteAllText($answer, $hdrTxt + $out, $utf8)
Write-Host ("MODEL:   {0}" -f $used)
Write-Host ("ELAPSED: {0}s" -f [math]::Round($sw.Elapsed.TotalSeconds,1))
Write-Host ("FINISH:  {0}" -f $r.choices[0].finish_reason)
Write-Host ("CHARS:   {0}" -f $out.Length)
Write-Host ("ANSWER:  {0}  SHA256={1}" -f $answer, (Get-FileHash -LiteralPath $answer -Algorithm SHA256).Hash)
