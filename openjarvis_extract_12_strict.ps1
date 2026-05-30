$root = "C:\Windows\System32\OpenJarvis"
$chunkDir = Join-Path $root "qwen_chunks_12"
$outDir = Join-Path $root "qwen_notes_api_strict"
New-Item -ItemType Directory -Force -Path $outDir | Out-Null

$master = Get-Content (Join-Path $chunkDir "000_QWEN_MASTER_PROMPT.txt") -Raw

for ($i = 1; $i -le 12; $i++) {
    $chunkPath = Join-Path $chunkDir ("{0:D3}_QWEN_CORE_BUNDLE_part_{1:D3}.txt" -f $i, $i)
    $outPath = Join-Path $outDir ("QWEN_NOTES_{0:D3}.txt" -f $i)
    $chunkText = Get-Content $chunkPath -Raw

    $prompt = @"
You are extracting grounded evidence from a source chunk for a software architecture audit.

You are NOT writing documentation.
You are NOT continuing an earlier explanation.
You are NOT writing a tutorial.
You are NOT writing recommendations.
You are NOT writing a final audit.
You are NOT allowed to infer missing implementation details.

Use only the exact content provided below.
If a point is not directly supported by the chunk, do not state it as fact.
If the chunk appears incomplete, do not continue it. Only extract what is explicitly present.

Output rules:
- Output only the 10 required sections below.
- Use the exact section titles below, exactly as written.
- Under each section, use bullet points only.
- Each bullet must be one of:
  - a directly supported fact from the chunk, or
  - "None confirmed in this chunk."
- No introduction.
- No conclusion.
- No summary.
- No recommendations.
- No code blocks.
- No markdown emphasis.
- Use plain ASCII only.
- Keep bullets short and concrete.
- Prefer file names, class names, function names, config keys, endpoints, event names, and exact component names when present.

Required sections exactly:

1. Confirmed architecture components
2. Confirmed startup / boot / entrypoint evidence
3. Confirmed dependencies and integrations
4. Confirmed configuration, environment variables, and runtime assumptions
5. Confirmed model / inference / MCP / Ollama wiring
6. Confirmed UI <-> backend/service interactions
7. Confirmed security-relevant findings
8. Confirmed performance-relevant findings
9. Confirmed architecture drift / duplication / inconsistency evidence
10. Open questions caused by missing evidence in this chunk

First, here is the instruction file content:

===== BEGIN QWEN_MASTER_PROMPT.txt =====
$master
===== END QWEN_MASTER_PROMPT.txt =====

Now extract evidence from this source chunk only:

===== BEGIN QWEN_CORE_BUNDLE.md CHUNK $i OF 12 =====
$chunkText
===== END QWEN_CORE_BUNDLE.md CHUNK $i OF 12 =====
"@

    $escaped = $prompt.Replace('\', '\\').Replace('"', '\"').Replace("`r", '\r').Replace("`n", '\n')
    $json = '{"model":"qwen2.5-coder:32b-instruct-q4_K_M","prompt":"' + $escaped + '","stream":false,"keep_alive":-1}'

    try {
        $response = Invoke-RestMethod `
            -Method Post `
            -Uri "http://172.16.33.200:11434/api/generate" `
            -ContentType "application/json; charset=utf-8" `
            -Body $json

        $response.response | Set-Content -Path $outPath -Encoding UTF8
        Write-Host "Completed strict chunk $i -> $outPath"
    }
    catch {
        $_ | Out-String | Set-Content -Path $outPath -Encoding UTF8
        Write-Host "FAILED strict chunk $i -> $outPath"
    }
}
