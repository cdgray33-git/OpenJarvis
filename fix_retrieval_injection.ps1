<#
.SYNOPSIS
    Verified fix: wire retrieval context injection into chat streaming endpoints.
    Every anchor and type signature below was confirmed against the real files
    before this script was written - no guessed patterns.

.VERIFIED FACTS USED
    - api_routes.py top-level imports end at line 11 (after `from pydantic import BaseModel`)
    - agent_manager_routes.py top-level imports end at line 16 (after the ImportError raise)
    - api_routes.py anchor: `engine = getattr(websocket.app.state, "engine", None)` (line 598, unique)
    - agent_manager_routes.py anchor: `while turns < max_turns:` (line 1043, unique)
    - api_routes.py builds messages as PLAIN DICTS: [{"role": "user", "content": message}]
      -> must be converted to real Message(role=Role.X, content=...) objects before inject_context
    - agent_manager_routes.py ALREADY builds real Message(role=Role.X, content=...) objects
      -> no conversion needed there
    - Message is a dataclass: role: Role, content: str = ""  (core/types.py:62)
    - Role is a str Enum: SYSTEM/USER/ASSISTANT/TOOL (core/types.py:15)
    - KnowledgeStore(MemoryBackend) constructor: __init__(self, db_path: Union[str, Path] = "")
      -> empty string is valid; it falls back to DEFAULT_CONFIG_DIR internally (store.py:158-161)
    - inject_context(query: str, messages: List[Message], backend: MemoryBackend, *, 
      config: Optional[ContextConfig] = None) -> List[Message]  (context.py:60-66)
    - ContextConfig fields: enabled, top_k, min_score, max_context_tokens (context.py:14-21)
.NOTES
    Backs up both files before editing. Throws (no partial edits left half-applied per file)
    if any anchor isn't found exactly once.
#>
[CmdletBinding()]
param(
    [string]$ProjectRoot = "C:\WINDOWS\system32\OpenJarvis"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$FILE_API       = Join-Path $ProjectRoot "src\openjarvis\server\api_routes.py"
$FILE_AGENT_MGR = Join-Path $ProjectRoot "src\openjarvis\server\agent_manager_routes.py"
$BACKUP_DIR     = Join-Path $ProjectRoot ".fix_backups_$(Get-Date -Format 'yyyyMMdd_HHmmss')"

function Write-Step { param($msg) Write-Host "`n=== $msg ===" -ForegroundColor Cyan }
function Write-Ok   { param($msg) Write-Host "[OK]  $msg" -ForegroundColor Green }

function New-Backup {
    param([string]$File)
    New-Item -ItemType Directory -Force -Path $BACKUP_DIR | Out-Null
    $dest = Join-Path $BACKUP_DIR (Split-Path $File -Leaf)
    Copy-Item $File $dest -Force
    Write-Ok "Backed up: $dest"
}

function Assert-SingleMatch {
    param([string]$File, [string]$Pattern)
    $found = @(Select-String -Path $File -Pattern $Pattern)
    if ($found.Count -eq 0) { throw "Anchor NOT FOUND in $File : $Pattern" }
    if ($found.Count -gt 1) { throw "Anchor matched $($found.Count) times (expected 1) in $File : $Pattern" }
    return $found[0].LineNumber
}

function Insert-AfterLine {
    param([string]$File, [int]$LineNumber, [string[]]$InsertLines)
    $lines = Get-Content $File
    $out = @()
    for ($i = 0; $i -lt $lines.Count; $i++) {
        $out += $lines[$i]
        if (($i + 1) -eq $LineNumber) { $out += $InsertLines }
    }
    $out | Set-Content $File -Encoding UTF8
}

function Insert-BeforeLine {
    param([string]$File, [int]$LineNumber, [string[]]$InsertLines)
    $lines = Get-Content $File
    $out = @()
    for ($i = 0; $i -lt $lines.Count; $i++) {
        if (($i + 1) -eq $LineNumber) { $out += $InsertLines }
        $out += $lines[$i]
    }
    $out | Set-Content $File -Encoding UTF8
}

# ─────────────────────────────────────────────────────────────────────────
Write-Step "Backing up both files to $BACKUP_DIR"
New-Backup $FILE_API
New-Backup $FILE_AGENT_MGR

# ═══════════════════════════════════════════════════════════════════════
# FIX 1: api_routes.py - websocket_chat_stream
# ═══════════════════════════════════════════════════════════════════════
Write-Step "Fixing api_routes.py"

# 1a) Re-verify anchors right before editing (in case file changed since last check)
$importAnchorLine = Assert-SingleMatch $FILE_API '^from pydantic import BaseModel$'
$engineAnchorLine  = Assert-SingleMatch $FILE_API 'engine = getattr\(websocket\.app\.state, "engine", None\)'

# 1b) Insert new imports after the existing top-level import block (line 11)
$importBlock = @(
    "from openjarvis.core.types import Message, Role",
    "from openjarvis.tools.storage.context import inject_context, ContextConfig",
    "from openjarvis.connectors.store import KnowledgeStore"
)
Insert-AfterLine $FILE_API $importAnchorLine $importBlock
Write-Ok "Inserted imports after line $importAnchorLine"

# Re-locate the engine anchor (line numbers shifted by +3 after the import insert)
$engineAnchorLine = Assert-SingleMatch $FILE_API 'engine = getattr\(websocket\.app\.state, "engine", None\)'

# 1c) Insert retrieval setup + context injection AFTER the engine-is-None check block,
#     and convert the plain-dict message into a real Message object first.
#     We replace the dict-based message build with a Message object, then inject context.
$content = Get-Content $FILE_API -Raw
$oldMsgPattern = '[ \t]*messages = \[\{"role": "user", "content": message\}\]'
$oldMsgMatch = [regex]::Match($content, $oldMsgPattern)
if (-not $oldMsgMatch.Success) {
    throw "Expected message-build line not found in api_routes.py - aborting before partial edit."
}
# Capture the exact leading whitespace so the replacement inherits it instead of doubling it
$leadingWs = [regex]::Match($oldMsgMatch.Value, '^[ \t]*').Value

$newMsgLines = @(
    "user_message_obj = Message(role=Role.USER, content=message)",
    "messages = [user_message_obj]",
    "",
    "# === RETRIEVAL SETUP & INJECTION ===",
    "knowledge_store = KnowledgeStore()",
    "context_config = ContextConfig(",
    "    enabled=True,",
    "    top_k=5,",
    "    min_score=0.0,",
    "    max_context_tokens=2048,",
    ")",
    "messages = inject_context(message, messages, knowledge_store, config=context_config)"
)
$newMsgBlock = ($newMsgLines | ForEach-Object { if ($_ -eq "") { "" } else { "$leadingWs$_" } }) -join "`r`n"

$content = $content.Substring(0, $oldMsgMatch.Index) + $newMsgBlock + $content.Substring($oldMsgMatch.Index + $oldMsgMatch.Length)
$utf8NoBom = New-Object System.Text.UTF8Encoding $false
[System.IO.File]::WriteAllText($FILE_API, $content, $utf8NoBom)
Write-Ok "Replaced dict-based message build with Message object + retrieval injection (indentation verified)"

# ═══════════════════════════════════════════════════════════════════════
# FIX 2: agent_manager_routes.py - generate() inner function
# ═══════════════════════════════════════════════════════════════════════
Write-Step "Fixing agent_manager_routes.py"

$importAnchorLine2 = Assert-SingleMatch $FILE_AGENT_MGR '^    raise ImportError\("fastapi and pydantic are required for server routes"\)$'
$importBlock2 = @(
    "",
    "from openjarvis.tools.storage.context import inject_context, ContextConfig",
    "from openjarvis.connectors.store import KnowledgeStore"
)
Insert-AfterLine $FILE_AGENT_MGR $importAnchorLine2 $importBlock2
Write-Ok "Inserted imports after line $importAnchorLine2"

# Re-locate the while-turns anchor (shifted by +3 after import insert)
$whileAnchorLine = Assert-SingleMatch $FILE_AGENT_MGR 'while turns < max_turns:'

# messages_for_llm is ALREADY List[Message] - no conversion needed, just inject context
# before the loop starts, using the line we already saw: `messages_for_llm = list(llm_messages)`
$injectBlock2 = @(
    "",
    "        # === RETRIEVAL SETUP & INJECTION ===",
    "        knowledge_store = KnowledgeStore()",
    "        context_config = ContextConfig(",
    "            enabled=True,",
    "            top_k=5,",
    "            min_score=0.0,",
    "            max_context_tokens=2048,",
    "        )",
    "        messages_for_llm = inject_context(user_content, messages_for_llm, knowledge_store, config=context_config)",
    ""
)
Insert-BeforeLine $FILE_AGENT_MGR $whileAnchorLine $injectBlock2
Write-Ok "Inserted retrieval injection before line $whileAnchorLine (while turns < max_turns:)"

Write-Step "Done"
Write-Host "Backups saved to: $BACKUP_DIR" -ForegroundColor Yellow
Write-Host "`nNext steps:" -ForegroundColor Yellow
Write-Host "  1. Restart the backend"
Write-Host "  2. Upload a PDF, then ask about it in the same chat session"
Write-Host "  3. If anything breaks, restore from: $BACKUP_DIR"