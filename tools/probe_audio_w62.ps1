param([string]$Out)
$lines = New-Object System.Collections.Generic.List[string]
$cs = @"
using System; using System.Collections.Generic; using System.Runtime.InteropServices;
namespace W62C {
[ComImport, Guid("BCDE0395-E52F-467C-8E3D-C4579291692E")] class MMDeviceEnumeratorCo {}
[ComImport, Guid("A95664D2-9614-4F35-A746-DE8DB63617E6"), InterfaceType(ComInterfaceType.InterfaceIsIUnknown)]
interface IMMDeviceEnumerator { [PreserveSig] int EnumAudioEndpoints(int flow, int mask, out IMMDeviceCollection col); [PreserveSig] int GetDefaultAudioEndpoint(int flow, int role, out IMMDevice dev); }
[ComImport, Guid("0BD7A1BE-7A1A-44DB-8397-CC5392387B5E"), InterfaceType(ComInterfaceType.InterfaceIsIUnknown)]
interface IMMDeviceCollection { [PreserveSig] int GetCount(out int n); [PreserveSig] int Item(int i, out IMMDevice dev); }
[ComImport, Guid("D666063F-1587-4E43-81F1-B948E807363F"), InterfaceType(ComInterfaceType.InterfaceIsIUnknown)]
interface IMMDevice { [PreserveSig] int Activate(ref Guid iid, int ctx, IntPtr p, [MarshalAs(UnmanagedType.IUnknown)] out object o); [PreserveSig] int OpenPropertyStore(int a, out IntPtr s); [PreserveSig] int GetId([MarshalAs(UnmanagedType.LPWStr)] out string id); [PreserveSig] int GetState(out int st); }
[ComImport, Guid("1BE09788-6894-4089-8586-9A2A6C265AC5"), InterfaceType(ComInterfaceType.InterfaceIsIUnknown)]
interface IMMEndpoint { [PreserveSig] int GetDataFlow(out int f); }
[ComImport, Guid("5CDF2C82-841E-4546-9722-0CF74078229A"), InterfaceType(ComInterfaceType.InterfaceIsIUnknown)]
interface IAudioEndpointVolume { int f1(); int f2(); int f3(); int f4(); int f5(); int f6(); [PreserveSig] int GetMasterVolumeLevelScalar(out float v); int f8(); int f9(); int f10(); int f11(); int f12(); [PreserveSig] int GetMute([MarshalAs(UnmanagedType.Bool)] out bool m); }
[ComImport, Guid("77AA99A0-1BD6-484F-8BC7-2C654C9A9B6F"), InterfaceType(ComInterfaceType.InterfaceIsIUnknown)]
interface IAudioSessionManager2 { int f1(); int f2(); [PreserveSig] int GetSessionEnumerator(out IAudioSessionEnumerator e); }
[ComImport, Guid("E2F5BB11-0570-40CA-ACDD-3AA01277DEE8"), InterfaceType(ComInterfaceType.InterfaceIsIUnknown)]
interface IAudioSessionEnumerator { [PreserveSig] int GetCount(out int n); [PreserveSig] int GetSession(int i, [MarshalAs(UnmanagedType.IUnknown)] out object s); }
[ComImport, Guid("bfb7ff88-7239-4fc9-8fa2-07c950be9c6d"), InterfaceType(ComInterfaceType.InterfaceIsIUnknown)]
interface IAudioSessionControl2 { [PreserveSig] int GetState(out int st); int f2(); int f3(); int f4(); int f5(); int f6(); int f7(); int f8(); int f9(); int f10(); int f11(); [PreserveSig] int GetProcessId(out int pid); }
[ComImport, Guid("87CE5498-68D6-44E5-9215-6DA47EF883D8"), InterfaceType(ComInterfaceType.InterfaceIsIUnknown)]
interface ISimpleAudioVolume { int f1(); [PreserveSig] int GetMasterVolume(out float v); int f3(); [PreserveSig] int GetMute([MarshalAs(UnmanagedType.Bool)] out bool m); }
public static class Audio {
  static string Def(IMMDeviceEnumerator en, int f, int role) { IMMDevice d; if (en.GetDefaultAudioEndpoint(f, role, out d) != 0) return "NONE"; string id; d.GetId(out id); return id; }
  public static List<string> Report() {
    var r = new List<string>();
    var en = (IMMDeviceEnumerator)(new MMDeviceEnumeratorCo());
    r.Add("DEFAULT RENDER console=" + Def(en,0,0) + " comms=" + Def(en,0,2));
    r.Add("DEFAULT CAPTURE console=" + Def(en,1,0) + " comms=" + Def(en,1,2));
    IMMDeviceCollection col; en.EnumAudioEndpoints(2, 1, out col);
    int n; col.GetCount(out n);
    for (int i = 0; i < n; i++) {
      IMMDevice dev; col.Item(i, out dev);
      string id; dev.GetId(out id);
      int flow; ((IMMEndpoint)dev).GetDataFlow(out flow);
      string vol = "vol=?";
      Guid g = typeof(IAudioEndpointVolume).GUID; object o;
      if (dev.Activate(ref g, 23, IntPtr.Zero, out o) == 0) { var ev = (IAudioEndpointVolume)o; float v; bool m; ev.GetMasterVolumeLevelScalar(out v); ev.GetMute(out m); vol = "vol=" + v.ToString("0.00") + " mute=" + m; }
      r.Add("ENDPOINT " + (flow == 0 ? "RENDER " : "CAPTURE") + " " + id + " " + vol);
      Guid g2 = typeof(IAudioSessionManager2).GUID; object o2;
      if (dev.Activate(ref g2, 23, IntPtr.Zero, out o2) == 0) {
        IAudioSessionEnumerator se; ((IAudioSessionManager2)o2).GetSessionEnumerator(out se);
        int sc; se.GetCount(out sc);
        for (int j = 0; j < sc; j++) {
          object so; se.GetSession(j, out so);
          var c2 = (IAudioSessionControl2)so; int st; c2.GetState(out st); int pid; c2.GetProcessId(out pid);
          var sv = (ISimpleAudioVolume)so; float sl; bool sm; sv.GetMasterVolume(out sl); sv.GetMute(out sm);
          r.Add("  SESSION pid=" + pid + " state=" + st + " vol=" + sl.ToString("0.00") + " mute=" + sm);
        }
      }
    }
    return r;
  }
}}
"@
try {
  if (-not ('W62C.Audio' -as [type])) { Add-Type -TypeDefinition $cs -ErrorAction Stop }
  $procs = @{}; Get-CimInstance Win32_Process | ForEach-Object { $procs[[int]$_.ProcessId] = $_ }
  $eps = @(Get-PnpDevice -Class AudioEndpoint -ErrorAction SilentlyContinue)
  foreach ($x in [W62C.Audio]::Report()) {
    $o = $x
    foreach ($e in $eps) { $sfx = ($e.InstanceId -split '\\')[-1]; if ($sfx -and $o.IndexOf($sfx, [StringComparison]::OrdinalIgnoreCase) -ge 0) { $o += "  [$($e.FriendlyName) status=$($e.Status)]" } }
    if ($o -match 'pid=(\d+)') { $p = [int]$Matches[1]; $ch = @(); for ($k = 0; $k -lt 4 -and $procs.ContainsKey($p); $k++) { $ch += $procs[$p].Name; $p = [int]$procs[$p].ParentProcessId }; $o += "  proc=" + ($ch -join '<-') }
    $lines.Add($o)
  }
} catch { $lines.Add("AUDIO EXCEPTION: $($_.Exception.Message)") }
$ms = 'Software\Microsoft\Windows\CurrentVersion\CapabilityAccessManager\ConsentStore\microphone'
foreach ($hv in 'HKCU','HKLM') { $lines.Add("MIC CONSENT $hv = [$((Get-ItemProperty "$($hv):\$ms" -ErrorAction SilentlyContinue).Value)]") }
$np = "HKCU:\$ms\NonPackaged"
$lines.Add("MIC DESKTOP-APPS = [$((Get-ItemProperty $np -ErrorAction SilentlyContinue).Value)]")
Get-ChildItem $np -ErrorAction SilentlyContinue | Where-Object { $_.PSChildName -match 'jarvis|webview' } | ForEach-Object {
  $pp = Get-ItemProperty $_.PSPath
  $a = if ($pp.LastUsedTimeStart) { [DateTime]::FromFileTime($pp.LastUsedTimeStart) } else { '-' }
  $z = if ($pp.LastUsedTimeStop) { [DateTime]::FromFileTime($pp.LastUsedTimeStop) } else { '-' }
  $lines.Add("MIC APP $($_.PSChildName) value=[$($pp.Value)] lastStart=$a lastStop=$z")
}
[IO.File]::WriteAllLines($Out, $lines, [Text.Encoding]::ASCII)
