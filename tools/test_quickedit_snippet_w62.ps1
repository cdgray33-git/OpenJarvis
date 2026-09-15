param([string]$Out)
try {
# W62-QUICKEDIT BEGIN - QuickEdit off in this console; a click in it can pause the backend (F-W62-2a)
$ojQeBefore = $null; $ojQeAfter = $null
try {
    Add-Type -Namespace OJStart -Name Con -ErrorAction Stop -MemberDefinition @"
[DllImport("kernel32.dll", SetLastError=true, CharSet=CharSet.Unicode)] public static extern System.IntPtr CreateFileW(string n, uint a, uint s, System.IntPtr sa, uint d, uint f, System.IntPtr t);
[DllImport("kernel32.dll", SetLastError=true)] public static extern bool GetConsoleMode(System.IntPtr h, out uint m);
[DllImport("kernel32.dll", SetLastError=true)] public static extern bool SetConsoleMode(System.IntPtr h, uint m);
[DllImport("kernel32.dll")] public static extern bool CloseHandle(System.IntPtr h);
"@
    $ojQeH = [OJStart.Con]::CreateFileW('CONIN$', [uint32]3221225472, [uint32]3, [IntPtr]::Zero, [uint32]3, [uint32]0, [IntPtr]::Zero)
    if ($ojQeH -ne [IntPtr](-1)) {
        $ojQeM = [uint32]0
        [void][OJStart.Con]::GetConsoleMode($ojQeH, [ref]$ojQeM)
        $ojQeBefore = $ojQeM
        $ojQeNew = [uint32]($ojQeM -bor 0x80)
        if ($ojQeNew -band 0x40) { $ojQeNew = [uint32]($ojQeNew - 0x40) }
        [void][OJStart.Con]::SetConsoleMode($ojQeH, $ojQeNew)
        [void][OJStart.Con]::GetConsoleMode($ojQeH, [ref]$ojQeM)
        $ojQeAfter = $ojQeM
        [void][OJStart.Con]::CloseHandle($ojQeH)
        Write-Host ("QuickEdit off: mode 0x{0:X} -> 0x{1:X}" -f $ojQeBefore, $ojQeAfter) -ForegroundColor Green
    } else { Write-Host "W62-QUICKEDIT: CONIN open failed, QuickEdit unchanged" -ForegroundColor Yellow }
} catch { Write-Host "W62-QUICKEDIT: not applied ($($_.Exception.Message))" -ForegroundColor Yellow }
# W62-QUICKEDIT END
[IO.File]::WriteAllText($Out, ('before=0x{0:X} after=0x{1:X} QUICKEDIT_LIVE={2} PASS={3}' -f $ojQeBefore, $ojQeAfter, [bool]($ojQeAfter -band 0x40), ($null -ne $ojQeAfter -and -not ($ojQeAfter -band 0x40))))
} catch { [IO.File]::WriteAllText($Out, "EXCEPTION: $($_.Exception.Message)") }

