# Read-only sample collection for the exact TOC supplied by the user.
[CmdletBinding()]
param(
    [string]$IsoPath = 'D:\Games PS2\God of War II [NTSC]\God of War II.iso',
    [string]$LogRoot = 'D:\logs'
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.IO.Compression.FileSystem

function Read-HeroBytes([System.IO.Stream]$Stream, [long]$Offset, [int]$Count) {
    if ($Offset -lt 0 -or $Count -lt 0 -or $Count -gt 16777216 -or $Offset + $Count -gt $Stream.Length) {
        throw 'Invalid extent, truncated ISO, or metadata/sample larger than 16 MiB.'
    }
    [void]$Stream.Seek($Offset, [System.IO.SeekOrigin]::Begin)
    $buffer = New-Object byte[] $Count
    $done = 0
    while ($done -lt $Count) {
        $read = $Stream.Read($buffer, $done, $Count - $done)
        if ($read -eq 0) { throw 'Unexpected end of ISO.' }
        $done += $read
    }
    return ,$buffer
}

function Read-HeroBoth32([byte[]]$Data, [int]$Offset) {
    $little = [BitConverter]::ToUInt32($Data, $Offset)
    [byte[]]$reverse = $Data[($Offset + 7)..($Offset + 4)]
    if ($little -ne [BitConverter]::ToUInt32($reverse, 0)) { throw 'Inconsistent ISO9660 endian fields.' }
    return $little
}

function Read-HeroRecord([byte[]]$Data, [int]$Position, [long]$ImageSize) {
    $length = [int]$Data[$Position]
    if ($length -lt 34 -or $Position + $length -gt $Data.Length -or $Position % 2048 + $length -gt 2048) {
        throw 'Invalid ISO9660 directory record.'
    }
    $nameLength = [int]$Data[$Position + 32]
    if (33 + $nameLength -gt $length) { throw 'Invalid ISO9660 filename length.' }
    if ($Data[$Position + 1] -ne 0 -or $Data[$Position + 26] -ne 0 -or
        $Data[$Position + 27] -ne 0 -or ($Data[$Position + 25] -band 128)) {
        throw 'Extended, interleaved, or multi-extent ISO records are unsupported.'
    }
    $sector = [long](Read-HeroBoth32 $Data ($Position + 2))
    $bytes = [long](Read-HeroBoth32 $Data ($Position + 10))
    if ($sector * 2048 + $bytes -gt $ImageSize) { throw 'Directory extent exceeds ISO size.' }
    return [PSCustomObject]@{
        Name = [Text.Encoding]::ASCII.GetString($Data, $Position + 33, $nameLength) -replace ';[0-9]+$', ''
        Sector = $sector
        Bytes = $bytes
        Directory = [bool]($Data[$Position + 25] -band 2)
    }
}

function Get-HeroHash([byte[]]$Data) {
    $hasher = [Security.Cryptography.SHA256]::Create()
    try { return [BitConverter]::ToString($hasher.ComputeHash($Data)).Replace('-', '').ToLowerInvariant() }
    finally { $hasher.Dispose() }
}

$runName = 'gow2-muestras-' + (Get-Date -Format 'yyyyMMdd-HHmmss-fff') + '-' + [Guid]::NewGuid().ToString('N')
$run = Join-Path $LogRoot $runName
[System.IO.Directory]::CreateDirectory($run) | Out-Null
$bundle = Join-Path $LogRoot ($runName + '.zip')
$discStream = $null
try {
    $discStream = [System.IO.File]::OpenRead($IsoPath)
    $primary = $null
    for ($sector = 16; $sector -lt 128; $sector++) {
        $descriptor = Read-HeroBytes $discStream ($sector * 2048) 2048
        if ([Text.Encoding]::ASCII.GetString($descriptor, 1, 5) -ne 'CD001' -or $descriptor[6] -ne 1) {
            throw 'Expected an uncompressed ISO9660 image with 2048-byte sectors.'
        }
        if ($descriptor[0] -eq 1) { $primary = $descriptor; break }
        if ($descriptor[0] -eq 255) { break }
    }
    if ($null -eq $primary -or [BitConverter]::ToUInt16($primary, 128) -ne 2048) {
        throw 'Compatible primary ISO9660 descriptor not found.'
    }
    $root = Read-HeroRecord $primary 156 $discStream.Length
    if (-not $root.Directory -or $root.Bytes -gt 8388608) { throw 'Invalid root directory.' }
    $directory = Read-HeroBytes $discStream ($root.Sector * 2048) ([int]$root.Bytes)
    $rows = @()
    $position = 0
    while ($position -lt $directory.Length) {
        $length = [int]$directory[$position]
        if ($length -eq 0) {
            $position = [int]([Math]::Floor($position / 2048) + 1) * 2048
            continue
        }
        $entry = Read-HeroRecord $directory $position $discStream.Length
        if ($entry.Name -ne [string][char]0 -and $entry.Name -ne [string][char]1) { $rows += $entry }
        $position += $length
    }
    $configs = @($rows | Where-Object { -not $_.Directory -and $_.Name -ieq 'SYSTEM.CNF' })
    $indices = @($rows | Where-Object { -not $_.Directory -and $_.Name -ieq 'GODOFWAR.TOC' })
    $paks = @($rows | Where-Object { -not $_.Directory -and $_.Name -ieq 'PART1.PAK' })
    if ($configs.Count -ne 1 -or $indices.Count -ne 1 -or $paks.Count -ne 1 -or $configs[0].Bytes -gt 8192) {
        throw 'Missing or ambiguous SYSTEM.CNF, GODOFWAR.TOC or PART1.PAK.'
    }
    $cnf = [Text.Encoding]::ASCII.GetString((Read-HeroBytes $discStream ($configs[0].Sector * 2048) ([int]$configs[0].Bytes)))
    if ($cnf -notmatch '(?im)^\s*BOOT2\s*=\s*cdrom0?:[\\/]*SCUS_974\.81(?:;1)?\s*$') {
        throw 'BOOT2 does not identify SCUS-97481.'
    }
    $toc = Read-HeroBytes $discStream ($indices[0].Sector * 2048) ([int]$indices[0].Bytes)
    $tocHash = Get-HeroHash $toc
    if ($tocHash -ne '9b339a2dfda12827d221e173a2fb806d7be5d6c436bcffcc650e1486604d77b0') {
        throw 'TOC differs from the supplied index. No game samples were copied.'
    }
    $count = [BitConverter]::ToUInt32($toc, 0)
    $tableEnd = 4 + [long]$count * 36
    if ($count -eq 0 -or $count -gt 100000 -or $tableEnd -gt $toc.Length -or ($toc.Length - $tableEnd) % 4 -ne 0) {
        throw 'Invalid GOW2 TOC tables.'
    }
    $offsetCount = ($toc.Length - $tableEnd) / 4
    $records = @()
    $indexed = $false
    for ($index = 0; $index -lt $count; $index++) {
        $record = 4 + $index * 36
        $name = [Text.Encoding]::ASCII.GetString($toc, $record, 24).Split([char]0)[0]
        $size = [long][BitConverter]::ToUInt32($toc, $record + 24)
        $encounters = [long][BitConverter]::ToUInt32($toc, $record + 28)
        $start = [long][BitConverter]::ToUInt32($toc, $record + 32)
        if ($size -eq 0 -or $encounters -eq 0 -or $start + $encounters -gt $offsetCount) {
            throw 'Invalid GOW2 file or encounter range.'
        }
        $locations = @()
        for ($encounter = 0; $encounter -lt $encounters; $encounter++) {
            $raw = [long][BitConverter]::ToUInt32($toc, [int]($tableEnd + ($start + $encounter) * 4))
            $locations += $raw
            if ($raw -ge 10000000) { $indexed = $true }
        }
        $records += [PSCustomObject]@{ Name = $name; Bytes = $size; Locations = $locations }
    }
    if (-not $indexed) { throw 'Expected the indexed DVD9 TOC layout; this variant is unsupported.' }
    $sampleRows = @()
    $totalBytes = [long]0
    foreach ($wanted in @('R_HERO00.WAD', 'R_HERO01.WAD', 'R_PERMA.WAD')) {
        $selected = @($records | Where-Object { $_.Name -ceq $wanted })
        if ($selected.Count -ne 1) { throw "Missing or ambiguous TOC entry: $wanted" }
        $file = $selected[0]
        $firstPakLocations = @($file.Locations | Where-Object { $_ -lt 10000000 })
        if ($firstPakLocations.Count -eq 0) { throw "No first-layer occurrence: $wanted" }
        $pakOffset = [long]$firstPakLocations[0] * 2048
        if ($file.Bytes -gt 16777216 -or $pakOffset + $file.Bytes -gt $paks[0].Bytes) {
            throw "Sample exceeds supported limits or PART1.PAK: $wanted"
        }
        $totalBytes += $file.Bytes
        if ($totalBytes -gt 33554432) { throw 'Samples exceed the 32 MiB collection limit.' }
        $isoOffset = $paks[0].Sector * 2048 + $pakOffset
        $payload = Read-HeroBytes $discStream $isoOffset ([int]$file.Bytes)
        [IO.File]::WriteAllBytes((Join-Path $run $wanted), $payload)
        $sampleRows += [PSCustomObject]@{
            Name = $wanted
            Bytes = $file.Bytes
            SHA256 = Get-HeroHash $payload
            SourcePak = 'PART1.PAK'
            PakOffset = $pakOffset
            IsoOffset = $isoOffset
        }
    }
    [PSCustomObject]@{
        SerialFromBoot2 = 'SCUS-97481'
        TOCSHA256 = $tocHash
        Samples = $sampleRows
        Scope = 'First PART1.PAK occurrences only; packages not interpreted or changed. No PCSX2 runtime verification.'
    } | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath (Join-Path $run 'informe-muestras.json') -Encoding UTF8
    [IO.Compression.ZipFile]::CreateFromDirectory($run, $bundle)
    Write-Host "Muestras e informe: $run"
    Write-Host "Adjunta este ZIP: $bundle"
    Write-Host 'La ISO original no se ha modificado. Si hubo un error, envia error.txt en lugar del ZIP.'
} catch {
    $failure = $_
    if (Test-Path -LiteralPath $bundle) { Remove-Item -LiteralPath $bundle -Force }
    $failure.Exception.Message | Set-Content -LiteralPath (Join-Path $run 'error.txt') -Encoding UTF8
    throw $failure
} finally {
    if ($null -ne $discStream) { $discStream.Dispose() }
}
