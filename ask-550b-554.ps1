# ask-550b-554.ps1
# Builds the serve.py bundle with the five-part :554 question embedded at the top,
# sends it directly to the 550B on OpenRouter, and writes the answer to the repo root.
# READ-ONLY against serve.py. Does not modify any source file.
# Run from PS C:\Users\Admin\OpenJarvis> as:
#   powershell -ExecutionPolicy Bypass -File 'C:\Users\Admin\OpenJarvis\ask-550b-554.ps1'

$ErrorActionPreference = 'Stop'
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

$src    = 'C:\Users\Admin\OpenJarvis\src\openjarvis\cli\serve.py'
$root   = 'C:\Users\Admin\OpenJarvis'
$keyf   = 'C:\Users\Admin\.openjarvis\cloud-keys.env'
$model  = 'nvidia/nemotron-3-ultra-550b-a55b:free'
$stamp  = Get-Date -Format 'yyyyMMdd-HHmmss'
$bundle = Join-Path $root ("bundle-serve-554-$stamp.md")
$answer = Join-Path $root ("ANSWER-554-$stamp.md")

# ---------- 1. canary check (read-only, hash only, never print the literal) ----------
$expected = '272cc73cafba1e8324e2398524d0bd0303deb4f52a6a5d3a01a446be1e9314a4'
$lines = Get-Content $src
if ($lines.Count -lt 554) { throw "serve.py has only $($lines.Count) lines - expected 655." }
$canary = $lines[553]
$sha = [Security.Cryptography.SHA256]::Create()
$hash = ([BitConverter]::ToString($sha.ComputeHash([Text.Encoding]::UTF8.GetBytes($canary)))).Replace('-','').ToLower()
Write-Host ("CANARY: len={0} match={1}" -f $canary.Length, ($hash -eq $expected))
Write-Host ("FILE:   lines={0}" -f $lines.Count)

# ---------- 2. the embedded question ----------
$question = @'
# TASK BRIEF FOR THE MODEL

You are analysing one Python file from a self-hosted assistant platform called OpenJarvis.
The whole file is provided below with 1-based line numbers. Answer the five numbered
questions at the end. Cite a line number for every claim you make.

## ESTABLISHED FACTS - DO NOT RE-DERIVE OR CONTRADICT THESE

1. The file is `src/openjarvis/cli/serve.py`. It is 655 lines. `uvicorn.Config` is at line 653.
2. **Line 554 is a single damaged string literal of 49,789 characters.** It is the result of
   repeated UTF-8-read-as-cp1252 re-encode cycles across many read-modify-write passes. It is
   TRUNCATED to 300 characters in the listing below. **Do not analyse, quote, repair, or
   comment on its contents. It is a known separate issue and is not what is being asked.**
   Treat it only as an opaque token that occupies line 554.
3. Line 554 is a plain `logger.info(...)` call on a credentials-related code path.
4. The logging problem has already been solved and is NOT the question. Specifically: the
   `openjarvis` parent logger used to sit at WARNING, which silently rejected every INFO
   record in the subtree. On 2026-09-09 an `OPENJARVIS_LOG_LEVEL` environment override was
   added and the tree was raised to INFO. This is runtime-verified: four other `logger.info`
   calls in this same module now arrive in `backend.log`.
5. **Despite the logger tree being open, line 554 did not emit on that restart.**
   Therefore the log level, the handler, the formatter, and the module import are all ruled
   out. The remaining explanation is that the code at line 554 is never reached.

## THE QUESTION: WHY DOES LINE 554 NEVER EXECUTE ON STARTUP?

Answer these five, in order, numbered, with line-number citations:

**1. ENCLOSING SCOPE.** What function, method, or block contains line 554? Give its exact
starting line, its full signature, and its ending line. Name any class it belongs to.

**2. GUARD CHAIN.** Trace every condition between that enclosing function's entry point and
line 554. List each `if`, `elif`, `else`, `try`/`except`/`finally`, `for`, `while`, `with`,
early `return`, `continue`, `break`, and `raise` that stands between them. For each one, give
its line number and state what must be true for control to continue toward line 554. Then
state, in one sentence, the complete condition under which line 554 executes.

**3. REACHABILITY FROM STARTUP.** Is the enclosing function actually called during the normal
`jarvis serve` startup sequence? Find every call site of it inside this file and give the line
numbers. If it is called from a FastAPI route handler, a lifespan/startup event, a background
task, a CLI subcommand other than `serve`, a lazily imported path, or is not called at all
within this file, say exactly which and cite the line. If it is called at startup, identify
which specific guard from question 2 is the most likely one to be failing, and say why.

**4. WHAT IT LOGS.** What does line 554 actually log? Name each variable in the call, state
where each is assigned (line number), and say whether the logged value would contain
credentials, tokens, or secrets in the normal case. Do not reproduce the damaged literal.

**5. MINIMUM PROOF.** Give the smallest non-invasive test that would prove whether the guard
chain is the reason line 554 does not fire. Requirements for the test: it must be
NON-INTERACTIVE and run to completion on its own without a human reacting to screen output
inside a time window; it must NOT modify `serve.py`; and it should be runnable as a single
PowerShell command from `C:\Users\Admin\OpenJarvis`. If the only possible proof requires
touching the file, say so plainly and give the smallest such change instead.

## OUTPUT RULES

- Number your answers 1 through 5. No preamble, no summary section at the end.
- Cite `line N` for every structural claim.
- If the file does not contain the information needed for a question, say so explicitly
  rather than guessing.
- Never reproduce any part of the line 554 literal.

---

# FILE: src/openjarvis/cli/serve.py

Lines longer than 300 characters are truncated and marked.

'@

# ---------- 3. build the bundle ----------
$b = New-Object System.Text.StringBuilder
[void]$b.AppendLine($question)
[void]$b.AppendLine('```python')
for ($i = 1; $i -le $lines.Count; $i++) {
    $t = $lines[$i-1]
    if ($t.Length -gt 300) { $t = $t.Substring(0,300) + " ...[TRUNCATED, original length " + $lines[$i-1].Length + "]" }
    [void]$b.AppendLine(("{0}: {1}" -f $i, $t))
}
[void]$b.AppendLine('```')
$content = $b.ToString()
[IO.File]::WriteAllText($bundle, $content, (New-Object System.Text.UTF8Encoding($false)))
Write-Host ("BUNDLE: {0} ({1} KB)" -f $bundle, [math]::Round((Get-Item $bundle).Length/1KB,1))

# ---------- 4. key, read silently ----------
if (-not (Test-Path $keyf)) { throw "Key file not found: $keyf" }
$kl = Get-Content $keyf | Where-Object { $_ -match '^\s*OPENROUTER_API_KEY\s*=' } | Select-Object -First 1
if (-not $kl) { throw "No OPENROUTER_API_KEY line in cloud-keys.env" }
$key = ($kl -split '=',2)[1].Trim().Trim('"').Trim("'")
Write-Host ("KEY:    found=True len={0} prefix_ok={1}" -f $key.Length, $key.StartsWith('sk-or-'))

# ---------- 5. send ----------
$payload = @{
    model       = $model
    max_tokens  = 6000
    temperature = 0.2
    messages    = @(@{ role = 'user'; content = $content })
} | ConvertTo-Json -Depth 6 -Compress

$bytes = [Text.Encoding]::UTF8.GetBytes($payload)
$hdr = @{ 'Authorization' = "Bearer $key"; 'Content-Type' = 'application/json' }

Write-Host ("SEND:   model={0} payload={1} KB" -f $model, [math]::Round($bytes.Length/1KB,1))
$sw = [Diagnostics.Stopwatch]::StartNew()
try {
    $r = Invoke-RestMethod -Uri 'https://openrouter.ai/api/v1/chat/completions' -Method Post -Headers $hdr -Body $bytes -TimeoutSec 900
} catch {
    $sw.Stop()
    Write-Host ("FAILED after {0}s" -f [math]::Round($sw.Elapsed.TotalSeconds,1)) -ForegroundColor Red
    Write-Host ("ERROR:  {0}" -f $_.Exception.Message) -ForegroundColor Red
    if ($_.Exception.Response) {
        $rd = New-Object IO.StreamReader($_.Exception.Response.GetResponseStream())
        Write-Host ("BODY:   {0}" -f $rd.ReadToEnd()) -ForegroundColor Red
    }
    exit 1
}
$sw.Stop()

$msg = $r.choices[0].message
$out = $msg.content
if ([string]::IsNullOrWhiteSpace($out) -and $msg.reasoning) { $out = "[REASONING FIELD ONLY]`r`n" + $msg.reasoning }

Write-Host ("ELAPSED: {0}s" -f [math]::Round($sw.Elapsed.TotalSeconds,1))
Write-Host ("FINISH:  {0}" -f $r.choices[0].finish_reason)
Write-Host ("CHARS:   {0}" -f $out.Length)

$hdrTxt = "# ANSWER: serve.py:554 guard question`r`nmodel: $model`r`nasked: $stamp`r`nelapsed: $([math]::Round($sw.Elapsed.TotalSeconds,1))s`r`nfinish: $($r.choices[0].finish_reason)`r`nbundle: $bundle`r`n`r`n---`r`n`r`n"
[IO.File]::WriteAllText($answer, $hdrTxt + $out, (New-Object System.Text.UTF8Encoding($false)))
Write-Host ("ANSWER:  {0}" -f $answer)
Write-Host ""
Write-Host "----- BEGIN ANSWER -----"
Write-Host $out
Write-Host "----- END ANSWER -----"
