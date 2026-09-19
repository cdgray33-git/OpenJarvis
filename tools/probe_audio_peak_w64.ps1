# probe_audio_peak_w64.ps1
# Measures ACTUAL audio sample levels on render endpoints and per-session.
# Distinguishes "session open but silent" (keepalive only) from "real audio".
# PS 5.1 compatible. -Out must be an ABSOLUTE path (.NET WriteAllLines).
param(
  [Parameter(Mandatory=$true)][string]$Out,
  [int]$Seconds = 60,
  [int]$IntervalMs = 200
)

$cs = @"
using System; using System.Collections.Generic; using System.Runtime.InteropServices;
namespace W64M {
[ComImport, Guid("BCDE0395-E52F-467C-8E3D-C4579291692E")] class MMDeviceEnumeratorCo {}
[ComImport, Guid("A95664D2-9614-4F35-A746-DE8DB63617E6"), InterfaceType(ComInterfaceType.InterfaceIsIUnknown)]
interface IMMDeviceEnumerator { [PreserveSig] int EnumAudioEndpoints(int flow, int mask, out IMMDeviceCollection col); [PreserveSig] int GetDefaultAudioEndpoint(int flow, int role, out IMMDevice dev); }
[ComImport, Guid("0BD7A1BE-7A1A-44DB-8397-CC5392387B5E"), InterfaceType(ComInterfaceType.InterfaceIsIUnknown)]
interface IMMDeviceCollection { [PreserveSig] int GetCount(out int n); [PreserveSig] int Item(int i, out IMMDevice dev); }
[ComImport, Guid("D666063F-1587-4E43-81F1-B948E807363F"), InterfaceType(ComInterfaceType.InterfaceIsIUnknown)]
interface IMMDevice { [PreserveSig] int Activate(ref Guid iid, int ctx, IntPtr p, [MarshalAs(UnmanagedType.IUnknown)] out object o); [PreserveSig] int OpenPropertyStore(int a, out IntPtr s); [PreserveSig] int GetId([MarshalAs(UnmanagedType.LPWStr)] out string id); [PreserveSig] int GetState(out int st); }
[ComImport, Guid("C02216F6-8C67-4B5B-9D00-D008E73E0064"), InterfaceType(ComInterfaceType.InterfaceIsIUnknown)]
interface IAudioMeterInformation { [PreserveSig] int GetPeakValue(out float p); }
[ComImport, Guid("77AA99A0-1BD6-484F-8BC7-2C654C9A9B6F"), InterfaceType(ComInterfaceType.InterfaceIsIUnknown)]
interface IAudioSessionManager2 { int f1(); int f2(); [PreserveSig] int GetSessionEnumerator(out IAudioSessionEnumerator e); }
[ComImport, Guid("E2F5BB11-0570-40CA-ACDD-3AA01277DEE8"), InterfaceType(ComInterfaceType.InterfaceIsIUnknown)]
interface IAudioSessionEnumerator { [PreserveSig] int GetCount(out int n); [PreserveSig] int GetSession(int i, [MarshalAs(UnmanagedType.IUnknown)] out object s); }
[ComImport, Guid("bfb7ff88-7239-4fc9-8fa2-07c950be9c6d"), InterfaceType(ComInterfaceType.InterfaceIsIUnknown)]
interface IAudioSessionControl2 { [PreserveSig] int GetState(out int st); int f2(); int f3(); int f4(); int f5(); int f6(); int f7(); int f8(); int f9(); int f10(); int f11(); [PreserveSig] int GetProcessId(out int pid); }

public static class Meter {
  static IMMDeviceEnumerator en;
  static List<IMMDevice> devs;
  static List<string> ids;

  public static void Init() {
    en = (IMMDeviceEnumerator)(new MMDeviceEnumeratorCo());
    devs = new List<IMMDevice>();
    ids = new List<string>();
    IMMDeviceCollection col;
    en.EnumAudioEndpoints(0, 1, out col);   // eRender, DEVICE_STATE_ACTIVE
    int n; col.GetCount(out n);
    for (int i = 0; i < n; i++) {
      IMMDevice d; col.Item(i, out d);
      string id; d.GetId(out id);
      devs.Add(d); ids.Add(id);
    }
  }

  public static int DeviceCount() { return devs.Count; }
  public static string DeviceId(int i) { return ids[i]; }

  // Returns lines: DEV|<id>|<peak>   and   SES|<id>|<pid>|<state>|<peak>
  public static List<string> Sample() {
    var r = new List<string>();
    for (int i = 0; i < devs.Count; i++) {
      IMMDevice d = devs[i];
      float dp = -1f;
      Guid gm = typeof(IAudioMeterInformation).GUID; object om;
      if (d.Activate(ref gm, 23, IntPtr.Zero, out om) == 0) {
        try { ((IAudioMeterInformation)om).GetPeakValue(out dp); } catch { dp = -2f; }
      }
      r.Add("DEV|" + ids[i] + "|" + dp.ToString("0.000000"));

      Guid gs = typeof(IAudioSessionManager2).GUID; object os;
      if (d.Activate(ref gs, 23, IntPtr.Zero, out os) == 0) {
        IAudioSessionEnumerator se;
        if (((IAudioSessionManager2)os).GetSessionEnumerator(out se) == 0) {
          int sc; se.GetCount(out sc);
          for (int j = 0; j < sc; j++) {
            object so;
            if (se.GetSession(j, out so) != 0) continue;
            int st = -1; int pid = -1; float sp = -1f;
            try { var c2 = (IAudioSessionControl2)so; c2.GetState(out st); c2.GetProcessId(out pid); } catch { }
            try { var mi = (IAudioMeterInformation)so; mi.GetPeakValue(out sp); } catch { sp = -2f; }
            r.Add("SES|" + ids[i] + "|" + pid + "|" + st + "|" + sp.ToString("0.000000"));
          }
        }
      }
    }
    return r;
  }
}}
"@

$lines = New-Object System.Collections.Generic.List[string]
$lines.Add("PEAK PROBE W64  started=" + (Get-Date).ToString("yyyy-MM-dd HH:mm:ss"))
$lines.Add("duration=${Seconds}s interval=${IntervalMs}ms")

try {
  if (-not ('W64M.Meter' -as [type])) { Add-Type -TypeDefinition $cs -ErrorAction Stop }
  [W64M.Meter]::Init()

  # Friendly names for endpoint ids
  $names = @{}
  foreach ($e in @(Get-PnpDevice -Class AudioEndpoint -ErrorAction SilentlyContinue)) {
    $sfx = ($e.InstanceId -split '\\')[-1]
    if ($sfx) { $names[$sfx] = $e.FriendlyName }
  }
  function Get-Friendly([string]$id) {
    foreach ($k in $names.Keys) {
      if ($id.IndexOf($k, [StringComparison]::OrdinalIgnoreCase) -ge 0) { return $names[$k] }
    }
    return '<unknown>'
  }

  $devMax = @{}
  $sesMax = @{}
  $sesState = @{}
  $samples = 0
  $deadline = (Get-Date).AddSeconds($Seconds)

  while ((Get-Date) -lt $deadline) {
    foreach ($row in [W64M.Meter]::Sample()) {
      $p = $row -split '\|'
      if ($p[0] -eq 'DEV') {
        $id = $p[1]; $v = [double]$p[2]
        if (-not $devMax.ContainsKey($id) -or $v -gt $devMax[$id]) { $devMax[$id] = $v }
      } elseif ($p[0] -eq 'SES') {
        $key = $p[1] + '#' + $p[2]
        $v = [double]$p[4]
        if (-not $sesMax.ContainsKey($key) -or $v -gt $sesMax[$key]) { $sesMax[$key] = $v }
        $sesState[$key] = $p[3]
      }
    }
    $samples++
    Start-Sleep -Milliseconds $IntervalMs
  }

  $lines.Add("samples=$samples")
  $lines.Add("")
  $lines.Add("---- PEAK PER RENDER ENDPOINT (max over run) ----")
  foreach ($id in $devMax.Keys) {
    $lines.Add(("DEV peak={0:0.000000}  {1}  {2}" -f $devMax[$id], (Get-Friendly $id), $id))
  }
  $lines.Add("")
  $lines.Add("---- PEAK PER SESSION (max over run) ----")
  foreach ($key in $sesMax.Keys) {
    $parts = $key -split '#'
    $pidv = $parts[1]
    $pname = '<gone>'
    if ($pidv -ne '0' -and $pidv -ne '-1') {
      $pr = Get-Process -Id ([int]$pidv) -ErrorAction SilentlyContinue
      if ($pr) { $pname = $pr.ProcessName }
    } elseif ($pidv -eq '0') { $pname = 'system-sounds' }
    $lines.Add(("SES peak={0:0.000000} pid={1} ({2}) state={3}  {4}" -f $sesMax[$key], $pidv, $pname, $sesState[$key], (Get-Friendly $parts[0])))
  }
  $lines.Add("")
  $lines.Add("VERDICT NOTE: peak=0.000000 on every sample means NO real audio samples")
  $lines.Add("were rendered during the run (digital silence only). peak=-1 means the")
  $lines.Add("meter was not readable; peak=-2 means the interface call threw.")
  $lines.Add("This block reports ONLY measured peak levels. It does not measure")
  $lines.Add("whether audio was audible in headphones.")
}
catch {
  $lines.Add("PEAK PROBE EXCEPTION: " + $_.Exception.Message)
}

[IO.File]::WriteAllLines($Out, $lines, [Text.Encoding]::ASCII)
Write-Host ("WROTE " + $Out)
Get-Content $Out | Select-Object -Last 40
