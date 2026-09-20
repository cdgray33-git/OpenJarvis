# patch_threadprobe.ps1
# Defect 6 / 6c prerequisite - thread-name probe on the EXISTING dispatch record.
# Target: src\openjarvis\tools\_stubs.py
# Run from repo root:  PS C:\Users\Admin\OpenJarvis> .\patch_threadprobe.ps1
# Read-only until all three anchor counts are exactly 1. No bare exit anywhere.

$ErrorActionPreference = 'Stop'
$p = 'src\openjarvis\tools\_stubs.py'

if (-not (Test-Path $p)) {
    'ABORT - target not found: ' + $p
} else {
    $full = (Get-Item $p).FullName
    $t = [System.IO.File]::ReadAllText($full)

    $rx1 = [regex]'(?m)^import time'
    $rx2 = [regex]'"ATTEMPT turn=%s tool=%s args=%s",'
    $rx3 = [regex]'(?m)^([ \t]*)_args_digest\(tool_call\.arguments\),'

    $c1 = $rx1.Matches($t).Count
    $c2 = $rx2.Matches($t).Count
    $c3 = $rx3.Matches($t).Count
    'anchor counts -> import time: ' + $c1 + '    fmt: ' + $c2 + '    args: ' + $c3

    if ($t.Contains('current_thread')) {
        'ABORT - probe text already present. File may be partially patched. Nothing written.'
    }
    elseif ($c1 -ne 1 -or $c2 -ne 1 -or $c3 -ne 1) {
        'ABORT - anchor count not exactly 1. Nothing written.'
    }
    else {
        $bak = $full + '.bak_defect6_threadprobe_' + (Get-Date -Format 'yyyyMMdd_HHmmss')
        Copy-Item $full $bak -Force
        'backup: ' + $bak

        # Edit 1 - insert the threading import before "import time"
        $m1 = $rx1.Match($t)
        $t = $t.Insert($m1.Index, "import threading`r`n")

        # Edit 2 - widen the format string
        $t = $t.Replace('"ATTEMPT turn=%s tool=%s args=%s",', '"ATTEMPT turn=%s tool=%s args=%s thread=%s",')

        # Edit 3 - add the arg, matching the indent of the anchor line
        $m3 = $rx3.Match($t)
        $ind = $m3.Groups[1].Value
        $t = $t.Insert($m3.Index + $m3.Length, "`r`n" + $ind + 'threading.current_thread().name,')

        $enc = New-Object System.Text.UTF8Encoding($false)
        [System.IO.File]::WriteAllText($full, $t, $enc)
        'write complete'

        '--- VERIFY MARKERS ---'
        'threading import : ' + (Select-String -Path $p -Pattern '^import threading' -Quiet)
        'fmt patched      : ' + (Select-String -Path $p -Pattern 'args=%s thread=%s' -Quiet)
        'arg patched      : ' + (Select-String -Path $p -Pattern 'current_thread' -Quiet)
        'control ATTEMPT  : ' + (Select-String -Path $p -Pattern 'ATTEMPT turn=' -Quiet)

        '--- ENCODING CONTROL (this line holds a dash glyph, it must render intact) ---'
        (Select-String -Path $p -Pattern 'dispatch engine for tool calls' | Select-Object -First 1).Line

        '--- PATCHED REGION ---'
        Select-String -Path $p -Pattern 'ATTEMPT turn=' -Context 0,4 | Select-Object -First 1

        '--- SYNTAX CHECK ---'
        & '.venv\Scripts\python.exe' -m py_compile $p
        if ($LASTEXITCODE -eq 0) {
            'py_compile OK'
        } else {
            'py_compile FAILED - restore now with:'
            "Copy-Item '$bak' '$full' -Force"
        }

        '--- ROLLBACK COMMAND ---'
        "Copy-Item '$bak' '$full' -Force"
    }
}
