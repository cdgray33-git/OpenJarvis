$path = "C:\Windows\System32\openjarvis\frontend\src\lib\store.ts"
$old = @"
  updateLastAssistant: (
    conversationId: string,
    content: string,
    toolCalls?: ToolCallInfo[],
    usage?: TokenUsage,
    telemetry?: MessageTelemetry,
    audio?: { url: string },
  ) => void;
"@
$new = @"
  updateLastAssistant: (
    conversationId: string,
    content: string,
    toolCalls?: ToolCallInfo[],
    usage?: TokenUsage,
    telemetry?: MessageTelemetry,
    audio?: { url: string },
    persist?: boolean,
  ) => void;
"@

$content = Get-Content $path -Raw
if ($content -notmatch [regex]::Escape($old)) {
    Write-Host "PATTERN NOT FOUND - no changes made. Manual edit needed." -ForegroundColor Red
    exit 1
}
$content.Replace($old, $new) | Set-Content -Path $path -NoNewline
Write-Host "Interface updated successfully." -ForegroundColor Green
Write-Host "=== Verification ===" -ForegroundColor Cyan
Get-Content $path | Select-Object -Skip 154 -First 13