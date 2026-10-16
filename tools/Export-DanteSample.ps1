# Copy one known DMC3 entry to a fresh directory; never change the installation.
[CmdletBinding()]
param(
    [string]$GameRoot = 'D:\HayJueguitosEnLaCompu\Devil May Cry HD Collection',
    [string]$LogRoot = 'D:\logs'
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.IO.Compression.FileSystem

$runName = 'dmc3-dante-' + (Get-Date -Format 'yyyyMMdd-HHmmss-fff') + '-' + [Guid]::NewGuid().ToString('N')
$run = Join-Path $LogRoot $runName
[System.IO.Directory]::CreateDirectory($run) | Out-Null
$sample = Join-Path $run 'pl000.pac'
$manifest = Join-Path $run 'informe.json'
$archive = $null

try {
    $nbz = Join-Path $GameRoot 'data/dmc3/dmc3-0.nbz'
    $archive = [System.IO.Compression.ZipFile]::OpenRead($nbz)
    $selectedEntries = @($archive.Entries | Where-Object { $_.FullName -ceq 'GData.afs/pl000.pac' })
    if ($selectedEntries.Count -ne 1) {
        throw 'Expected exactly one GData.afs/pl000.pac entry; no file was selected.'
    }
    $entry = $selectedEntries[0]
    # Size from the user's NBZ inventory. Reject a different revision for inspection.
    if ($entry.Length -ne 1335280) {
        throw 'Entry size differs from the supplied inventory. Send error.txt before continuing.'
    }
    [System.IO.Compression.ZipFileExtensions]::ExtractToFile($entry, $sample, $false)
    if ((Get-Item -LiteralPath $sample).Length -ne $entry.Length) {
        throw 'Extracted length does not match the archive entry.'
    }
    [PSCustomObject]@{
        SourceEntry = $entry.FullName
        Bytes = $entry.Length
        CompressedBytes = $entry.CompressedLength
        SHA256 = (Get-FileHash -LiteralPath $sample -Algorithm SHA256).Hash
        Verification = 'Length checked; SHA256 is a fingerprint, not a comparison with a trusted hash. Source ZIP CRC not checked by this script.'
    } | ConvertTo-Json | Set-Content -LiteralPath $manifest -Encoding UTF8
    Write-Host "Muestra creada: $sample"
    Write-Host "Informe creado: $manifest"
    Write-Host 'Adjunta pl000.pac e informe.json. El juego original no se ha modificado.'
} catch {
    $failure = $_
    if (Test-Path -LiteralPath $sample) {
        Remove-Item -LiteralPath $sample -Force
    }
    $failure.Exception.Message | Set-Content -LiteralPath (Join-Path $run 'error.txt') -Encoding UTF8
    throw $failure
} finally {
    if ($null -ne $archive) { $archive.Dispose() }
}
