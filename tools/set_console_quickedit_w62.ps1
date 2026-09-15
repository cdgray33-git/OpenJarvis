param([int]$TargetPid, [string]$Out, [ValidateSet('read','off','on')][string]$Action = 'read')
try {
Add-Type -Namespace W62B -Name Con -MemberDefinition @"
[DllImport("kernel32.dll")] public static extern bool FreeConsole();
[DllImport("kernel32.dll", SetLastError=true)] public static extern bool AttachConsole(uint pid);
[DllImport("kernel32.dll", SetLastError=true, CharSet=CharSet.Unicode)] public static extern System.IntPtr CreateFileW(string n, uint a, uint s, System.IntPtr sa, uint d, uint f, System.IntPtr t);
[DllImport("kernel32.dll", SetLastError=true)] public static extern bool GetConsoleMode(System.IntPtr h, out uint m);
[DllImport("kernel32.dll", SetLastError=true)] public static extern bool SetConsoleMode(System.IntPtr h, uint m);
[DllImport("kernel32.dll")] public static extern bool CloseHandle(System.IntPtr h);
"@
[void][W62B.Con]::FreeConsole()
if (-not [W62B.Con]::AttachConsole([uint32]$TargetPid)) { [IO.File]::WriteAllText($Out, "ATTACH FAILED pid=$TargetPid err=$([Runtime.InteropServices.Marshal]::GetLastWin32Error())"); exit }
$hd = [W62B.Con]::CreateFileW('CONIN$', [uint32]3221225472, [uint32]3, [IntPtr]::Zero, [uint32]3, [uint32]0, [IntPtr]::Zero)
if ($hd -eq [IntPtr](-1)) { [IO.File]::WriteAllText($Out, "CONIN OPEN FAILED err=$([Runtime.InteropServices.Marshal]::GetLastWin32Error())"); exit }
$m = [uint32]0
[void][W62B.Con]::GetConsoleMode($hd, [ref]$m)
$before = $m; $setok = 'n/a'
if ($Action -ne 'read') {
  $new = [uint32]($m -bor 0x80)
  if ($Action -eq 'off') { if ($new -band 0x40) { $new = [uint32]($new - 0x40) } } else { $new = [uint32]($new -bor 0x40) }
  $setok = [W62B.Con]::SetConsoleMode($hd, $new)
}
$a = [uint32]0
[void][W62B.Con]::GetConsoleMode($hd, [ref]$a)
[void][W62B.Con]::CloseHandle($hd)
[IO.File]::WriteAllText($Out, ('pid={0} action={1} before=0x{2:X} set={3} after=0x{4:X} QUICKEDIT_LIVE={5}' -f $TargetPid, $Action, $before, $setok, $a, [bool]($a -band 0x40)))
} catch { [IO.File]::WriteAllText($Out, "EXCEPTION: $($_.Exception.Message)") }
