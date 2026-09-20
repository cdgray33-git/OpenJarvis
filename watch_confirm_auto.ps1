# watch_confirm_auto.ps1 - 6e approve-half listener, AUTO-APPROVES
# PowerShell 5.1, Windows box. Run from C:\Users\Admin\OpenJarvis in a SECOND window.
# Difference from watch_confirm.ps1: on a tool_confirm_request it immediately POSTs
# {confirm_id, decision:"approve"} to /v1/tools/confirm and prints the HTTP status,
# the body, and the elapsed ms from frame-arrival to response. Human latency removed.
#
# Reads:
#   200 + tool runs  -> approve half PROVEN.
#   200 + still times out at 120 s -> registry resolved but the gate did NOT wake. Defect.
#   404 -> the id was already gone. Registry/TTL problem, not a race.
#   400 -> decision wording rejected at the route.

param(
    [int]$MaxSeconds = 600,
    [string]$Url = 'ws://127.0.0.1:8010/v1/agents/events',
    [string]$ConfirmUrl = 'http://127.0.0.1:8010/v1/tools/confirm',
    [switch]$NoApprove
)

$ErrorActionPreference = 'Stop'

function Stamp { (Get-Date).ToString('HH:mm:ss.fff') }

function Send-Approve {
    param([string]$Cid)
    $body = @{ confirm_id = $Cid; decision = 'approve' } | ConvertTo-Json -Compress
    $t0 = Get-Date
    try {
        $resp = Invoke-WebRequest -Uri $ConfirmUrl -Method Post -ContentType 'application/json' -Body $body -UseBasicParsing
        $ms = '{0:N0}' -f ((Get-Date) - $t0).TotalMilliseconds
        Write-Host " APPROVE -> HTTP $($resp.StatusCode) in $ms ms" -ForegroundColor Green
        Write-Host " BODY: $($resp.Content)" -ForegroundColor Green
    } catch {
        $ms = '{0:N0}' -f ((Get-Date) - $t0).TotalMilliseconds
        $code = ''
        $bodyTxt = ''
        if ($_.Exception.Response) {
            try { $code = [int]$_.Exception.Response.StatusCode } catch { }
            try {
                $sr = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
                $bodyTxt = $sr.ReadToEnd()
                $sr.Close()
            } catch { }
        }
        Write-Host " APPROVE -> HTTP $code in $ms ms" -ForegroundColor Red
        Write-Host " BODY: $bodyTxt" -ForegroundColor Red
        Write-Host " EXC : $($_.Exception.GetBaseException().Message)" -ForegroundColor Red
    }
}

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
if ($NoApprove) {
    Write-Host "$(Stamp)  NoApprove set - will print confirm_id only." -ForegroundColor Yellow
} else {
    Write-Host "$(Stamp)  AUTO-APPROVE ARMED. Every confirm_id will be approved on arrival." -ForegroundColor Yellow
}
Write-Host "$(Stamp)  listening for $MaxSeconds s. Send the chat message now. Ctrl+C to stop."
Write-Host ""

$buf   = New-Object byte[] 65536
$seg   = New-Object System.ArraySegment[byte] -ArgumentList @(,$buf)
$start = Get-Date
$seen  = @{}

while ($ws.State -eq 'Open' -and ((Get-Date) - $start).TotalSeconds -lt $MaxSeconds) {

    $sb     = New-Object System.Text.StringBuilder
    $done   = $false
    $closed = $false

    while (-not $done) {
        $task = $ws.ReceiveAsync($seg, $cts.Token)
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

    $kind = 'frame'
    $m = [regex]::Match($txt, '"(?:type|event_type|event)"\s*:\s*"([^"]+)"')
    if ($m.Success) { $kind = $m.Groups[1].Value }

    $short = $txt
    if ($short.Length -gt 300) { $short = $short.Substring(0, 300) + ' ...[truncated]' }
    Write-Host "$(Stamp)  +$elapsed s  $kind  $short"

    $cm = [regex]::Match($txt, '"confirm_id"\s*:\s*"([^"]+)"')
    if ($cm.Success) {
        $cid = $cm.Groups[1].Value
        if (-not $seen.ContainsKey($cid)) {
            $seen[$cid] = $true
            $tool = ''
            $tm = [regex]::Match($txt, '"tool"\s*:\s*"([^"]+)"')
            if ($tm.Success) { $tool = $tm.Groups[1].Value }
            Write-Host "=================================================================" -ForegroundColor Yellow
            Write-Host " CONFIRM_ID: $cid   tool: $tool" -ForegroundColor Yellow
            if (-not $NoApprove) { Send-Approve -Cid $cid }
            else { Write-Host " Approve-OJ '$cid'" -ForegroundColor Yellow }
            Write-Host "=================================================================" -ForegroundColor Yellow
            Write-Host ""
        }
    }
}

Write-Host ""
Write-Host "$(Stamp)  stopped. final STATE: $($ws.State)"
try { $ws.Dispose() } catch { }
