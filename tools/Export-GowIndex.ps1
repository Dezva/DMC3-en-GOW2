# Read the first ISO9660 root and copy only its small configuration/index files.
[CmdletBinding()]
param(
    [string]$IsoPath = 'D:\Games PS2\God of War II [NTSC]\God of War II.iso',
    [string]$LogRoot = 'D:\logs'
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Read-DiscBytes([System.IO.Stream]$Stream, [long]$Offset, [int]$Count) {
    if ($Count -lt 0 -or $Count -gt 16777216 -or $Offset -lt 0 -or $Offset + $Count -gt $Stream.Length) {
        throw 'Invalid extent, truncated image, or metadata larger than 16 MiB.'
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

function Read-Both32([byte[]]$Data, [int]$Offset) {
    $little = [BitConverter]::ToUInt32($Data, $Offset)
    [byte[]]$reverse = $Data[($Offset + 7)..($Offset + 4)]
    if ($little -ne [BitConverter]::ToUInt32($reverse, 0)) {
        throw 'Inconsistent ISO9660 endian fields.'
    }
    return $little
}

function Read-IsoRecord([byte[]]$Data, [int]$Position, [long]$ImageSize) {
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
    $sector = [long](Read-Both32 $Data ($Position + 2))
    $bytes = [long](Read-Both32 $Data ($Position + 10))
    if ($sector * 2048 + $bytes -gt $ImageSize) { throw 'Directory extent exceeds ISO size.' }
    $name = [Text.Encoding]::ASCII.GetString($Data, $Position + 33, $nameLength)
    return [PSCustomObject]@{
        Name = $name -replace ';[0-9]+$', ''
        Sector = $sector
        Bytes = $bytes
        Directory = [bool]($Data[$Position + 25] -band 2)
    }
}

$runName = 'gow2-indice-' + (Get-Date -Format 'yyyyMMdd-HHmmss-fff') + '-' + [Guid]::NewGuid().ToString('N')
$run = Join-Path $LogRoot $runName
[System.IO.Directory]::CreateDirectory($run) | Out-Null
$discStream = $null
try {
    $discStream = [System.IO.File]::OpenRead($IsoPath)
    $primary = $null
    for ($sector = 16; $sector -lt 128; $sector++) {
        $descriptor = Read-DiscBytes $discStream ($sector * 2048) 2048
        if ([Text.Encoding]::ASCII.GetString($descriptor, 1, 5) -ne 'CD001' -or $descriptor[6] -ne 1) {
            throw 'Expected an uncompressed ISO9660 image with 2048-byte sectors.'
        }
        if ($descriptor[0] -eq 1) { $primary = $descriptor; break }
        if ($descriptor[0] -eq 255) { break }
    }
    if ($null -eq $primary -or [BitConverter]::ToUInt16($primary, 128) -ne 2048) {
        throw 'Compatible primary ISO9660 descriptor not found.'
    }
    $root = Read-IsoRecord $primary 156 $discStream.Length
    if (-not $root.Directory -or $root.Bytes -gt 8388608) { throw 'Invalid root directory.' }
    $directory = Read-DiscBytes $discStream ($root.Sector * 2048) ([int]$root.Bytes)
    $rows = @()
    $position = 0
    while ($position -lt $directory.Length) {
        $length = [int]$directory[$position]
        if ($length -eq 0) {
            $position = [int]([Math]::Floor($position / 2048) + 1) * 2048
            continue
        }
        $entry = Read-IsoRecord $directory $position $discStream.Length
        if ($entry.Name -ne [string][char]0 -and $entry.Name -ne [string][char]1) { $rows += $entry }
        $position += $length
    }
    $rows | Export-Csv -LiteralPath (Join-Path $run 'raiz-iso.csv') -NoTypeInformation -Encoding UTF8 -NoClobber
    $configs = @($rows | Where-Object { -not $_.Directory -and $_.Name -ieq 'SYSTEM.CNF' })
    if ($configs.Count -ne 1 -or $configs[0].Bytes -gt 8192) { throw 'SYSTEM.CNF missing or ambiguous.' }
    $cnfBytes = Read-DiscBytes $discStream ($configs[0].Sector * 2048) ([int]$configs[0].Bytes)
    $cnf = [Text.Encoding]::ASCII.GetString($cnfBytes)
    if ($cnf -notmatch '(?im)^\s*BOOT2\s*=\s*cdrom0?:[\\/]*SCUS_974\.81(?:;1)?\s*$') {
        throw 'BOOT2 does not identify SCUS-97481. Send raiz-iso.csv and error.txt.'
    }
    $indices = @($rows | Where-Object {
        -not $_.Directory -and ($_.Name -ieq 'GODOFWAR.TOC' -or $_.Name -ieq 'GODOFWAR.BIN')
    })
    if ($indices.Count -ne 1 -or $indices[0].Bytes -gt 16777216) {
        throw 'A single supported GODOFWAR.TOC/BIN index was not found. Send raiz-iso.csv and error.txt.'
    }
    $index = $indices[0]
    $indexBytes = Read-DiscBytes $discStream ($index.Sector * 2048) ([int]$index.Bytes)
    $indexPath = Join-Path $run $index.Name
    [System.IO.File]::WriteAllBytes($indexPath, $indexBytes)
    [System.IO.File]::WriteAllBytes((Join-Path $run 'SYSTEM.CNF'), $cnfBytes)
    [PSCustomObject]@{
        SerialFromBoot2 = 'SCUS-97481'
        IndexName = $index.Name
        IndexBytes = $index.Bytes
        IndexSHA256 = (Get-FileHash -LiteralPath $indexPath -Algorithm SHA256).Hash
        Scope = 'First ISO9660 root only. No PAK/WAD extraction. PCSX2 CRC not recalculated.'
    } | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $run 'informe-gow.json') -Encoding UTF8
    Write-Host "Indice y listado creados en: $run"
    Write-Host 'Adjunta el indice GODOFWAR.TOC/BIN, raiz-iso.csv e informe-gow.json.'
} catch {
    $failure = $_
    $failure.Exception.Message | Set-Content -LiteralPath (Join-Path $run 'error.txt') -Encoding UTF8
    throw $failure
} finally {
    if ($null -ne $discStream) { $discStream.Dispose() }
}
