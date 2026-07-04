<#
.SYNOPSIS
    Bundles all relevant OpenJarvis RAG/ingest pipeline files into one text file
    for upload to a cloud LLM for analysis.
.DESCRIPTION
    Reads a fixed list of real, confirmed-existing files relative to the project
    root, and writes them all into a single output file, each clearly separated
    with a header showing its original relative path. Missing files are reported
    as warnings but do not stop the script.
.NOTES
    Run from anywhere; it resolves paths relative to -ProjectRoot.
    Output file is written with UTF8 (no BOM).
#>
[CmdletBinding()]
param(
    [string]$ProjectRoot = "C:\WINDOWS\system32\OpenJarvis",
    [string]$OutputFile  = "C:\WINDOWS\system32\OpenJarvis\bundle_for_cloud_model.txt",
    [switch]$PriorityOnly   # Only bundle the 6 priority files instead of the full list
)

$ErrorActionPreference = "Stop"

function Write-Ok   { param($msg) Write-Host "[OK]  $msg" -ForegroundColor Green }
function Write-Warn { param($msg) Write-Host "[WARN] $msg" -ForegroundColor Yellow }
function Write-Step { param($msg) Write-Host "`n=== $msg ===" -ForegroundColor Cyan }

# ─────────────────────────────────────────────────────────────────────────────
# FILE LIST (relative to ProjectRoot)
# ─────────────────────────────────────────────────────────────────────────────

$priorityFiles = @(
    "src\openjarvis\server\upload_router.py",
    "src\openjarvis\connectors\store.py",
    "src\openjarvis\tools\storage\__init__.py",
    "src\openjarvis\tools\storage\context.py",
    "src\openjarvis\tools\retrieval.py",
    "src\openjarvis\server\api_routes.py"
)

$fullFiles = @(
    # Frontend
    "frontend\src\components\Chat\InputArea.tsx",
    "frontend\src\components\setup\IngestDashboard.tsx",
    "frontend\src\components\setup\SetupWizard.tsx",
    "frontend\src\pages\DataSourcesPage.tsx",
    "frontend\src\types\connectors.ts",

    # Backend - Upload & Connector Routing
    "src\openjarvis\server\upload_router.py",
    "src\openjarvis\server\connectors_router.py",
    "src\openjarvis\connectors\__init__.py",
    "src\openjarvis\connectors\_stubs.py",
    "src\openjarvis\connectors\pipeline.py",
    "src\openjarvis\connectors\chunker.py",

    # Backend - Storage/Embedding
    "src\openjarvis\connectors\store.py",
    "src\openjarvis\connectors\embedding_store.py",
    "src\openjarvis\connectors\embeddings.py",
    "src\openjarvis\connectors\retriever.py",
    "src\openjarvis\connectors\hybrid_search.py",

    # Backend - Retrieval/Tools
    "src\openjarvis\tools\storage\__init__.py",
    "src\openjarvis\tools\storage\_stubs.py",
    "src\openjarvis\tools\storage\ingest.py",
    "src\openjarvis\tools\storage\hybrid.py",
    "src\openjarvis\tools\storage\dense.py",
    "src\openjarvis\tools\storage\sqlite.py",
    "src\openjarvis\tools\storage\faiss_backend.py",
    "src\openjarvis\tools\storage\bm25.py",
    "src\openjarvis\tools\storage\colbert_backend.py",
    "src\openjarvis\tools\storage\context.py",
    "src\openjarvis\tools\storage_tools.py",
    "src\openjarvis\tools\knowledge_search.py",
    "src\openjarvis\tools\knowledge_sql.py",
    "src\openjarvis\tools\retrieval.py",
    "src\openjarvis\tools\scan_chunks.py",

    # Backend - Chat turn / orchestration
    "src\openjarvis\server\api_routes.py",
    "src\openjarvis\server\agent_manager_routes.py",
    "src\openjarvis\agents\executor.py",
    "src\openjarvis\agents\operative.py",
    "src\openjarvis\core\registry.py"
)

$fileList = if ($PriorityOnly) { $priorityFiles } else { $fullFiles }
$fileList = $fileList | Select-Object -Unique

# ─────────────────────────────────────────────────────────────────────────────
# BUNDLE
# ─────────────────────────────────────────────────────────────────────────────
Write-Step "Bundling $($fileList.Count) files from $ProjectRoot"

$sb = New-Object System.Text.StringBuilder
$found = 0
$missing = 0

foreach ($relPath in $fileList) {
    $fullPath = Join-Path $ProjectRoot $relPath

    if (Test-Path $fullPath) {
        $content = Get-Content $fullPath -Raw -Encoding UTF8
        [void]$sb.AppendLine("=" * 100)
        [void]$sb.AppendLine("FILE: $relPath")
        [void]$sb.AppendLine("=" * 100)
        [void]$sb.AppendLine($content)
        [void]$sb.AppendLine("")
        Write-Ok "Added: $relPath"
        $found++
    }
    else {
        [void]$sb.AppendLine("=" * 100)
        [void]$sb.AppendLine("FILE: $relPath  <<< NOT FOUND - SKIPPED >>>")
        [void]$sb.AppendLine("=" * 100)
        [void]$sb.AppendLine("")
        Write-Warn "Missing (skipped): $relPath"
        $missing++
    }
}

$utf8NoBom = New-Object System.Text.UTF8Encoding $false
[System.IO.File]::WriteAllText($OutputFile, $sb.ToString(), $utf8NoBom)

Write-Step "Done"
Write-Ok "Bundle written to: $OutputFile"
Write-Host "Files included: $found" -ForegroundColor White
if ($missing -gt 0) {
    Write-Warn "Files missing/skipped: $missing (see warnings above for which ones)"
}

$sizeKB = [math]::Round((Get-Item $OutputFile).Length / 1KB, 1)
Write-Host "Bundle size: $sizeKB KB" -ForegroundColor White