$ws  = New-Object System.Net.WebSockets.ClientWebSocket
$ct  = [System.Threading.CancellationToken]::None
$uri = [Uri]"ws://127.0.0.1:8010/v1/agents/events"
$ws.ConnectAsync($uri, $ct).Wait()
"STATE: " + $ws.State
"listening - Ctrl+C to stop"
$buf = New-Object byte[] 65536
$seg = New-Object System.ArraySegment[byte] -ArgumentList @(,$buf)
while ($ws.State -eq 'Open') {
  $sb = New-Object System.Text.StringBuilder
  do {
    $r = $ws.ReceiveAsync($seg, $ct); $r.Wait()
    [void]$sb.Append([System.Text.Encoding]::UTF8.GetString($buf, 0, $r.Result.Count))
  } while (-not $r.Result.EndOfMessage)
  (Get-Date -Format "HH:mm:ss.fff") + "  " + $sb.ToString()
}
