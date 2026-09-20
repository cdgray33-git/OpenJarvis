# watch_confirm.ps1 - 6e approve-half listener
# PowerShell 5.1, Windows box. Run from C:\Users\Admin\OpenJarvis in a SECOND window.
# Mounts ws://127.0.0.1:8010/v1/agents/events with NO agent_id param (a filtered
# client drops the event per ws_bridge.py:48-51).
# Prints every frame, and prints CONFIRM_ID on its own line the moment one appears.

param(
    [int]$MaxSeconds = 300,
    [string]$Url = 'ws://127.0.0.1:8010/v1/agents/events'
)

$ErrorActionPreference = 'Stop'

function Stamp { (Get-Date).ToString('HH:mm:ss.fff') }

$ws  = New-Object System.Net.WebSockets.ClientWebSocket
$cts = New-Object System.Threading.CancellationTokenSource

Write-Host "$(Stamp)  connecting: $Url"
try {
    $ws.ConnectAsync([Uri]$Url, $cts.Token).Wait()
} catch {
    Write-Host "$(Stamp)  CONNECT FAILED: $($_.Exception.GetBaseException().Message)" -ForegroundColor Red
    exit 1
}
Write-Host "$(Stamp)  STATE: $($ws.State)" -ForegroundColor Green
Write-Host "$(Stamp)  listening for $MaxSeconds s. Send the chat message now. Ctrl+C to stop."
Write-Host ""

$buf   = New-Object byte[] 65536
$seg   = New-Object System.ArraySegment[byte] -ArgumentList @(,$buf)
$start = Get-Date
$seen  = @{}

while ($ws.State -eq 'Open' -and ((Get-Date) - $start).TotalSeconds -lt $MaxSeconds) {

    $sb   = New-Object System.Text.StringBuilder
    $done = $false
    $closed = $false

    while (-not $done) {
        $task = $ws.ReceiveAsync($seg, $cts.Token)
        # poll so Ctrl+C stays responsive and MaxSeconds is honored
        while (-not $task.Wait(500)) {
            if (((Get-Date) - $start).TotalSeconds -ge $MaxSeconds) { break }
        }
        if (-not $task.IsCompleted) { $done = $true; $closed = $true; break }
        $res = $task.Result
        if ($res.MessageType -eq [System.Net.WebSockets.WebSocketMessageType]::Close) {
            $closed = $true; $done = $true; break
        }
        [void]$sb.Append([Text.Encoding]::UTF8.GetString($buf, 0, $res.Count))
        if ($res.EndOfMessage) { $done = $true }
    }

    if ($closed) { break }
    $txt = $sb.ToString()
    if ([string]::IsNullOrWhiteSpace($txt)) { continue }

    $elapsed = '{0,7:N3}' -f ((Get-Date) - $start).TotalSeconds

    # frame type, without assuming the key name
    $kind = 'frame'
    $m = [regex]::Match($txt, '"(?:type|event_type|event)"\s*:\s*"([^"]+)"')
    if ($m.Success) { $kind = $m.Groups[1].Value }

    $short = $txt
    if ($short.Length -gt 300) { $short = $short.Substring(0, 300) + ' ...[truncated]' }
    Write-Host "$(Stamp)  +$elapsed s  $kind  $short"

    # the payload we are here for
    $cm = [regex]::Match($txt, '"confirm_id"\s*:\s*"([^"]+)"')
    if ($cm.Success) {
        $cid = $cm.Groups[1].Value
        if (-not $seen.ContainsKey($cid)) {
            $seen[$cid] = $true
            $tool = ''
            $tm = [regex]::Match($txt, '"tool"\s*:\s*"([^"]+)"')
            if ($tm.Success) { $tool = $tm.Groups[1].Value }
            $exp = ''
            $em = [regex]::Match($txt, '"expires_at"\s*:\s*("?[^",}]+"?)')
            if ($em.Success) { $exp = $em.Groups[1].Value.Trim('"') }
            Write-Host ""
            Write-Host "=================================================================" -ForegroundColor Yellow
            Write-Host " CONFIRM_ID: $cid" -ForegroundColor Yellow
            Write-Host " tool: $tool   expires_at: $exp" -ForegroundColor Yellow
            Write-Host " In the OTHER window run:  Approve-OJ '$cid'" -ForegroundColor Yellow
            Write-Host "=================================================================" -ForegroundColor Yellow
            Write-Host ""
        }
    }
}

Write-Host ""
Write-Host "$(Stamp)  stopped. final STATE: $($ws.State)"
try { $ws.Dispose() } catch { }
