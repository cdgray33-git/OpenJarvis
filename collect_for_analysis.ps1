$targets = @(
  "src\openjarvis\agents\native_openhands.py",
  "src\openjarvis\agents\_stubs.py",
  "src\openjarvis\tools\_stubs.py",
  "src\openjarvis\core\registry.py"
)
$Out = "codebase_dump.txt"
$sb = New-Object System.Text.StringBuilder
$found = @()
foreach ($t in $targets) { if (Test-Path $t) { $found += $t } else { "MISSING: $t" } }
[void]$sb.AppendLine("=== MANIFEST: $($found.Count) files ===")
foreach ($t in $found) { [void]$sb.AppendLine("$t  $((Get-Item $t).Length) B") }
[void]$sb.AppendLine("")
foreach ($t in $found) {
  [void]$sb.AppendLine("========== BEGIN FILE: $t ==========")
  [void]$sb.AppendLine([IO.File]::ReadAllText((Join-Path $PWD $t)))
  [void]$sb.AppendLine("========== END FILE: $t ==========")
  [void]$sb.AppendLine("")
}
[IO.File]::WriteAllText((Join-Path $PWD $Out), $sb.ToString())
$len = (Get-Item $Out).Length
"WROTE $Out"
"BYTES $len  (approx tokens: $([math]::Round($len/4)))"
