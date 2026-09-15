param([int]$Seconds = 20)
$rate = 8000; $n = $rate * $Seconds * 2
$ms = New-Object IO.MemoryStream; $w = New-Object IO.BinaryWriter($ms)
$a = [Text.Encoding]::ASCII
$w.Write($a.GetBytes('RIFF')); $w.Write([int](36 + $n)); $w.Write($a.GetBytes('WAVEfmt '))
$w.Write([int]16); $w.Write([int16]1); $w.Write([int16]1); $w.Write([int]$rate); $w.Write([int]($rate * 2)); $w.Write([int16]2); $w.Write([int16]16)
$w.Write($a.GetBytes('data')); $w.Write([int]$n); $w.Write((New-Object byte[] $n)); $w.Flush()
$ms.Position = 0
(New-Object System.Media.SoundPlayer($ms)).PlaySync()
