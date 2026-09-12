# apply-w51-confirm-ui.ps1
# openjarvis-confirm-ui-v1 - Defect 6 / 6e browser half
#
# Run from the repo root: PS C:\Users\Admin\OpenJarvis>
# Windows box, PowerShell. Makes NO server-side change.
#
# Backs up, then makes two edits:
#   1. frontend\src\lib\api.ts                  - append confirmTool()
#   2. frontend\src\components\Chat\ChatArea.tsx - import + render ConfirmPrompt
#
# Idempotent: re-running detects existing markers and skips.
# Aborts WITHOUT writing anything if any anchor is missing or not unique.

$ErrorActionPreference = 'Stop'

$api  = 'frontend\src\lib\api.ts'
$chat = 'frontend\src\components\Chat\ChatArea.tsx'
$comp = 'frontend\src\components\Chat\ConfirmPrompt.tsx'

function Fail($m) { Write-Host "ABORT: $m" -ForegroundColor Red; exit 1 }

# ---- preflight -------------------------------------------------------------

foreach ($f in @($api, $chat, $comp)) {
    if (-not (Test-Path $f)) { Fail "missing file: $f" }
}
Write-Host "preflight: all three files present" -ForegroundColor Green

$apiText  = Get-Content $api  -Raw
$chatText = Get-Content $chat -Raw

$apiDone  = $apiText  -match 'openjarvis-confirm-ui-v1'
$chatDone = $chatText -match 'ConfirmPrompt'

$importAnchor = "import { streamChat } from '../../lib/sse';"
$renderAnchor = "      <div style={{ paddingBottom: '0.75rem' }}>"

if (-not $apiDone) {
    if (($apiText -split 'export async function apiFetch|async function apiFetch').Count -lt 2) {
        Fail "api.ts: apiFetch helper not found - house-style fetch wrapper changed"
    }
}
if (-not $chatDone) {
    $ic = ([regex]::Matches($chatText, [regex]::Escape($importAnchor))).Count
    $rc = ([regex]::Matches($chatText, [regex]::Escape($renderAnchor))).Count
    if ($ic -ne 1) { Fail "ChatArea.tsx: import anchor found $ic times, need exactly 1" }
    if ($rc -ne 1) { Fail "ChatArea.tsx: render anchor found $rc times, need exactly 1" }
    Write-Host "preflight: both ChatArea anchors unique" -ForegroundColor Green
}

# ---- backup ----------------------------------------------------------------

$stamp = Get-Date -Format 'yyyyMMdd-HHmmss'
if (-not $apiDone)  { Copy-Item $api  "$api.w51.bak"  -Force; Write-Host "backup: $api.w51.bak" }
if (-not $chatDone) { Copy-Item $chat "$chat.w51.bak" -Force; Write-Host "backup: $chat.w51.bak" }

# ---- edit 1: api.ts --------------------------------------------------------

if ($apiDone) {
    Write-Host "edit 1 SKIPPED - api.ts already carries openjarvis-confirm-ui-v1" -ForegroundColor Yellow
} else {
    $addition = @'

// ---------------------------------------------------------------------------
// openjarvis-confirm-ui-v1 - Defect 6 confirmation gate, inbound half
//
// Route read live 2026-09-12 at agent_manager_routes.py:2046-2110.
// Body is confirm_id + decision ONLY. turn_id is NOT sent - it comes back in
// the response from the registry entry (:2100). decision must be the lowercase
// word approve or deny (:2062-2067); anything else is a 400 before the
// registry is touched. Registry is write-once: a second POST reports 409 with
// the decision already held. 404 means the id expired (:2085).
// ---------------------------------------------------------------------------

export interface ConfirmToolResponse {
  ok: boolean;
  status: number;
  body: Record<string, unknown>;
}

export async function confirmTool(
  confirmId: string,
  decision: 'approve' | 'deny',
): Promise<ConfirmToolResponse> {
  const res = await apiFetch(`${getBase()}/v1/tools/confirm`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ confirm_id: confirmId, decision }),
  });
  let body: Record<string, unknown> = {};
  try {
    body = (await res.json()) as Record<string, unknown>;
  } catch {
    body = {};
  }
  return { ok: res.ok, status: res.status, body };
}
'@
    Add-Content -Path $api -Value $addition -Encoding utf8
    $check = Get-Content $api -Raw
    if ($check -match 'export async function confirmTool') {
        Write-Host "edit 1 OK - confirmTool appended to api.ts" -ForegroundColor Green
    } else {
        Fail "edit 1 FAILED - confirmTool not found after append"
    }
}

# ---- edit 2: ChatArea.tsx --------------------------------------------------

if ($chatDone) {
    Write-Host "edit 2 SKIPPED - ChatArea.tsx already references ConfirmPrompt" -ForegroundColor Yellow
} else {
    $newImport = $importAnchor + "`r`nimport { ConfirmPrompt } from './ConfirmPrompt';"
    $newRender = "      {/* openjarvis-confirm-ui-v1 */}`r`n      <ConfirmPrompt />`r`n`r`n" + $renderAnchor

    $chatText = $chatText.Replace($importAnchor, $newImport)
    $chatText = $chatText.Replace($renderAnchor, $newRender)

    Set-Content -Path $chat -Value $chatText -Encoding utf8 -NoNewline

    $check = Get-Content $chat -Raw
    $okImp = $check -match "import \{ ConfirmPrompt \} from './ConfirmPrompt';"
    $okRen = $check -match '<ConfirmPrompt />'
    if ($okImp -and $okRen) {
        Write-Host "edit 2 OK - ChatArea.tsx imports and renders ConfirmPrompt" -ForegroundColor Green
    } else {
        Fail "edit 2 FAILED - import=$okImp render=$okRen"
    }
}

# ---- report ----------------------------------------------------------------

Write-Host ""
Write-Host "stamp: $stamp"
Write-Host "ROLLBACK (PowerShell, repo root):"
Write-Host "  Copy-Item '$api.w51.bak' '$api' -Force"
Write-Host "  Copy-Item '$chat.w51.bak' '$chat' -Force"
Write-Host "  Remove-Item '$comp' -Force"
Write-Host ""
Write-Host "NEXT: npm run build  (from frontend\) - typecheck is the first gate."
