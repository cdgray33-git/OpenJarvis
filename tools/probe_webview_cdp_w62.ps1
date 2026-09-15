param([string]$Out, [int]$Port = 9222)
$L = New-Object System.Collections.Generic.List[string]
$ct = [Threading.CancellationToken]::None
$script:buf = New-Object byte[] 65536
$script:ms = New-Object IO.MemoryStream
$script:pend = $null
$script:nid = 0
function Send-Cdp($ws, [string]$method, $params) {
  $script:nid++
  $j = @{ id = $script:nid; method = $method; params = $params } | ConvertTo-Json -Depth 6 -Compress
  $b = [Text.Encoding]::UTF8.GetBytes($j)
  [void]$ws.SendAsync([ArraySegment[byte]]::new($b), [Net.WebSockets.WebSocketMessageType]::Text, $true, $ct).Wait(5000)
  return $script:nid
}
function Recv-Cdp($ws, [int]$Ms) {
  $got = New-Object System.Collections.Generic.List[object]
  $end = [DateTime]::UtcNow.AddMilliseconds($Ms)
  while ($true) {
    if (-not $script:pend) { $script:pend = $ws.ReceiveAsync([ArraySegment[byte]]::new($script:buf), $ct) }
    $left = [int]($end - [DateTime]::UtcNow).TotalMilliseconds
    if ($left -le 0 -or -not $script:pend.Wait($left)) { break }
    $r = $script:pend.Result; $script:pend = $null
    if ($r.MessageType -eq [Net.WebSockets.WebSocketMessageType]::Close) { break }
    $script:ms.Write($script:buf, 0, $r.Count)
    if ($r.EndOfMessage) {
      $txt = [Text.Encoding]::UTF8.GetString($script:ms.ToArray()); $script:ms.SetLength(0)
      try { $got.Add(($txt | ConvertFrom-Json)) } catch { }
    }
  }
  return ,$got
}
$ws = $null
try {
  $targets = @(Invoke-RestMethod -Uri "http://127.0.0.1:$Port/json/list" -TimeoutSec 5)
  foreach ($x in $targets) { $L.Add("TARGET type=$($x.type) url=$($x.url)") }
  $pg = $targets | Where-Object { $_.type -eq 'page' } | Select-Object -First 1
  if (-not $pg) { throw 'NO PAGE TARGET' }
  $ws = New-Object Net.WebSockets.ClientWebSocket
  if (-not $ws.ConnectAsync([Uri]$pg.webSocketDebuggerUrl, $ct).Wait(5000)) { throw 'WS CONNECT TIMEOUT' }
  [void](Send-Cdp $ws 'Runtime.enable' @{})
  [void](Send-Cdp $ws 'Log.enable' @{})
  $ev = Recv-Cdp $ws 3000
  $n = 0; $kept = 0
  $pat = 'PUMPDBG|\[tts\]|AudioContext|autoplay|getUserMedia|MediaRecorder|speech|synthesi|transcri|microphone|NotAllowed|NotFound'
  foreach ($m in $ev) {
    $line = $null; $lvl = ''
    if ($m.method -eq 'Runtime.consoleAPICalled') {
      $n++; $lvl = [string]$m.params.type
      $parts = @($m.params.args | ForEach-Object { if ($null -ne $_.value) { [string]$_.value } elseif ($_.description) { [string]$_.description } else { [string]$_.type } })
      $line = "CONSOLE ${lvl}: " + ($parts -join ' ')
    } elseif ($m.method -eq 'Log.entryAdded') {
      $n++; $e = $m.params.entry; $lvl = [string]$e.level
      $line = "LOG $lvl/$($e.source): $($e.text) $($e.url)"
    }
    if ($line -and ($line -match $pat -or $lvl -match '^(error|warning)$') -and $kept -lt 120) {
      $s = $line -replace '[^\x20-\x7E]', '?'
      if ($s.Length -gt 300) { $s = $s.Substring(0, 300) }
      $L.Add($s); $kept++
    }
  }
  $L.Add("CONSOLE+LOG ENTRIES REPLAYED: $n  KEPT: $kept")
  $expr = @"
(async () => {
  const r = {};
  r.url = location.href;
  r.visibility = document.visibilityState;
  r.focus = document.hasFocus();
  r.activation = navigator.userActivation ? (navigator.userActivation.hasBeenActive + '/' + navigator.userActivation.isActive) : 'n/a';
  try { const C = window.AudioContext || window.webkitAudioContext; const c = new C(); r.testCtx = c.state + ' sr=' + c.sampleRate + ' sink=' + (c.sinkId === undefined ? 'n/a' : (c.sinkId === '' ? 'default' : 'custom')); await c.close(); } catch (e) { r.testCtx = 'ERR ' + e; }
  try { r.micPerm = (await navigator.permissions.query({ name: 'microphone' })).state; } catch (e) { r.micPerm = 'ERR ' + e; }
  try { const d = await navigator.mediaDevices.enumerateDevices(); r.devices = d.map(x => x.kind + (x.label ? '+label' : '-label')).join(' '); } catch (e) { r.devices = 'ERR ' + e; }
  r.mediaRecorder = typeof MediaRecorder;
  return JSON.stringify(r);
})()
"@
  $eid = Send-Cdp $ws 'Runtime.evaluate' @{ expression = $expr; awaitPromise = $true; returnByValue = $true }
  $res = Recv-Cdp $ws 8000
  $hit = $res | Where-Object { $_.id -eq $eid } | Select-Object -First 1
  if ($hit) { $L.Add("PAGE STATE: $($hit.result.result.value) $($hit.result.exceptionDetails.text)") } else { $L.Add('PAGE STATE: NO REPLY') }
} catch { $L.Add("EXCEPTION: $($_.Exception.Message)") } finally { if ($ws) { $ws.Abort() } }
[IO.File]::WriteAllLines($Out, $L, [Text.Encoding]::ASCII)
