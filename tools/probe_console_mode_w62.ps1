param([int]$TargetPid, [string]$Out)
try {
Add-Type -Namespace W62 -Name Con -MemberDefinition @"
[DllImport("kernel32.dll")] public static extern bool FreeConsole();
[DllImport("kernel32.dll", SetLastError=true)] public static extern bool AttachConsole(uint pid);
[DllImport("kernel32.dll", SetLastError=true, CharSet=CharSet.Unicode)] public static extern System.IntPtr CreateFileW(string n, uint a, uint s, System.IntPtr sa, uint d, uint f, System.IntPtr t);
[DllImport("kernel32.dll", SetLastError=true)] public static extern bool GetConsoleMode(System.IntPtr h, out uint m);
[DllImport("kernel32.dll")] public static extern bool CloseHandle(System.IntPtr h);
"@
[void][W62.Con]::FreeConsole()
if (-not [W62.Con]::AttachConsole([uint32]$TargetPid)) {
  [IO.File]::WriteAllText($Out, "ATTACH FAILED pid=$TargetPid err=$([Runtime.InteropServices.Marshal]::GetLastWin32Error())"); exit
}
$hd = [W62.Con]::CreateFileW('CONIN$', [uint32]3221225472, [uint32]3, [IntPtr]::Zero, [uint32]3, [uint32]0, [IntPtr]::Zero)
if ($hd -eq [IntPtr](-1)) { [IO.File]::WriteAllText($Out, "CONIN OPEN FAILED err=$([Runtime.InteropServices.Marshal]::GetLastWin32Error())"); exit }
$m = [uint32]0
$ok = [W62.Con]::GetConsoleMode($hd, [ref]$m)
[void][W62.Con]::CloseHandle($hd)
$line = ('pid={0} getmode={1} mode=0x{2:X} QUICKEDIT_LIVE={3} EXTENDED={4}' -f $TargetPid, $ok, $m, [bool]($m -band 0x40), [bool]($m -band 0x80))
[IO.File]::WriteAllText($Out, $line)
} catch { [IO.File]::WriteAllText($Out, "EXCEPTION: $($_.Exception.Message)") }
