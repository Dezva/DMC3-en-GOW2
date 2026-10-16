# Phase 1: finite, read-only diagnostics. Compatible with Windows PowerShell 5.1.
[CmdletBinding()]
param(
    [string]$IsoPath = 'D:\Games PS2\God of War II [NTSC]\God of War II.iso',
    [string]$GameRoot = 'D:\HayJueguitosEnLaCompu\Devil May Cry HD Collection',
    [string]$LogRoot = 'D:\logs',
    [ValidateRange(1, 65535)][int]$PinePort = 28011,
    [ValidateRange(100, 10000)][int]$TimeoutMs = 1500
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
if (-not [BitConverter]::IsLittleEndian) { throw 'This diagnostic requires a little-endian machine.' }
$session = [Guid]::NewGuid().ToString('N')
$run = Join-Path $LogRoot ('pine-probe-' + (Get-Date -Format 'yyyyMMdd-HHmmss-fff') + '-' + $session)
[void][IO.Directory]::CreateDirectory($run)
$utf8 = New-Object Text.UTF8Encoding($false, $true)
$clock = [Diagnostics.Stopwatch]::StartNew()
$script:sequence = 0
$script:errors = New-Object 'System.Collections.Generic.List[object]'
$eventsPath = Join-Path $run 'events.jsonl'
$report = [ordered]@{
    protocol = 'dmc3-gow2-diagnostic'; schema_version = 1; session = $session
    started_utc = [DateTime]::UtcNow.ToString('o'); read_only = $true
    platform = [Environment]::OSVersion.Platform.ToString()
    pcsx2_processes = @(); dmc3 = $null; pine = $null; memory_test = $null
    phase1_verified = $false; authentic_attacks_detected = $false
    game_to_game_communication = $false
}

function Add-Event([string]$Stage, [object]$Data) {
    $script:sequence++
    $entry = [ordered]@{
        protocol = 'dmc3-gow2-diagnostic'; schema_version = 1; session = $session
        sequence = $script:sequence; utc = [DateTime]::UtcNow.ToString('o')
        elapsed_ms = $clock.ElapsedMilliseconds; stage = $Stage; data = $Data
    }
    [IO.File]::AppendAllText($eventsPath, (($entry | ConvertTo-Json -Depth 12 -Compress) + "`n"), $utf8)
}

function Add-Failure([string]$Stage, [string]$Message) {
    $failure = [ordered]@{ stage = $Stage; message = $Message }
    $script:errors.Add($failure)
    Add-Event 'error' $failure
}

function Read-FileBytes([IO.Stream]$Stream, [long]$Offset, [int]$Count) {
    if ($Offset -lt 0 -or $Count -lt 0 -or $Count -gt 8388608 -or $Offset + $Count -gt $Stream.Length) {
        throw 'Invalid or truncated file extent (maximum metadata read: 8 MiB).'
    }
    [void]$Stream.Seek($Offset, [IO.SeekOrigin]::Begin)
    $buffer = New-Object byte[] $Count
    $done = 0
    while ($done -lt $Count) {
        $got = $Stream.Read($buffer, $done, $Count - $done)
        if ($got -eq 0) { throw 'Unexpected end of file.' }
        $done += $got
    }
    return ,$buffer
}

function Get-ExecutableFingerprint([string]$Path) {
    $result = [ordered]@{ path = $Path; status = 'unknown' }
    $fileStream = $null
    try {
        # Read sharing only: do not change an executable or install a loader.
        $fileStream = [IO.File]::Open($Path, [IO.FileMode]::Open, [IO.FileAccess]::Read, [IO.FileShare]::ReadWrite)
        $result.bytes = $fileStream.Length
        $hash = [Security.Cryptography.SHA256]::Create()
        try { $result.sha256 = ([BitConverter]::ToString($hash.ComputeHash($fileStream))).Replace('-', '').ToLowerInvariant() }
        finally { $hash.Dispose() }
        $dos = Read-FileBytes $fileStream 0 64
        if ($dos[0] -ne 0x4d -or $dos[1] -ne 0x5a) { throw 'Not a PE executable: missing MZ.' }
        $peOffset = [BitConverter]::ToUInt32($dos, 60)
        $pe = Read-FileBytes $fileStream $peOffset 24
        if ([BitConverter]::ToUInt32($pe, 0) -ne 0x4550) { throw 'Invalid PE signature.' }
        $optionalLength = [BitConverter]::ToUInt16($pe, 20)
        if ($optionalLength -lt 60) { throw 'Truncated PE optional header.' }
        $optional = Read-FileBytes $fileStream ($peOffset + 24) $optionalLength
        $magic = [BitConverter]::ToUInt16($optional, 0)
        if ($magic -ne 0x10b -and $magic -ne 0x20b) { throw 'Unsupported PE optional header.' }
        $result.pe_machine = '0x{0:X4}' -f [BitConverter]::ToUInt16($pe, 4)
        $result.pe_timestamp = [BitConverter]::ToUInt32($pe, 8)
        $result.pe_size_of_image = [BitConverter]::ToUInt32($optional, 56)
        $version = [Diagnostics.FileVersionInfo]::GetVersionInfo($Path)
        $result.file_version = $version.FileVersion
        $result.product_version = $version.ProductVersion
        $result.status = 'fingerprinted'
    } catch [IO.FileNotFoundException] { $result.status = 'missing' }
      catch [IO.DirectoryNotFoundException] { $result.status = 'missing' }
      catch { $result.error = $_.Exception.Message }
    finally { if ($null -ne $fileStream) { $fileStream.Dispose() } }
    return $result
}

function Get-ProcessSnapshot([Diagnostics.Process]$Process, [switch]$Dmc) {
    $row = [ordered]@{
        pid = $Process.Id; name = $Process.ProcessName; path = $null
        executable_identity = 'unknown'; modules_status = 'not_requested'
    }
    try {
        $row.working_set_mib = [Math]::Round($Process.WorkingSet64 / 1MB, 2)
        $row.private_bytes_mib = [Math]::Round($Process.PrivateMemorySize64 / 1MB, 2)
        $row.start_utc = $Process.StartTime.ToUniversalTime().ToString('o')
        $row.path = $Process.MainModule.FileName
        $baseName = [IO.Path]::GetFileName($row.path)
        if ($Dmc) {
            if ($baseName -ieq 'dmc3.exe') { $row.executable_identity = 'dmc3.exe' }
            else { $row.executable_identity = 'other_executable' }
        } else { $row.executable_identity = $baseName }
    } catch { $row.inspection_error = $_.Exception.Message }
    if ($Dmc) {
        try {
            $row.observed_mod_modules = @($Process.Modules | Where-Object {
                $_.ModuleName -ieq 'Mary.dll' -or $_.ModuleName -ieq 'dinput8.dll'
            } | ForEach-Object { [ordered]@{ name = $_.ModuleName; path = $_.FileName } })
            $row.modules_status = 'observed'
        } catch { $row.modules_status = 'unknown'; $row.modules_error = $_.Exception.Message }
    }
    return $row
}

function Get-DmcDiagnostic {
    $candidates = @(Get-Process -Name 'dmc3' -ErrorAction SilentlyContinue)
    $launchers = @(Get-Process -Name 'dmcLauncher' -ErrorAction SilentlyContinue)
    $snapshots = @($candidates | ForEach-Object { Get-ProcessSnapshot $_ -Dmc })
    $confirmed = @($snapshots | Where-Object { $_.executable_identity -eq 'dmc3.exe' })
    $running = 'not_observed'
    if ($confirmed.Count -gt 0) { $running = 'confirmed' }
    elseif ($candidates.Count -gt 0) { $running = 'unknown_candidate_present' }
    $paths = @((Join-Path $GameRoot 'dmc3.exe'), (Join-Path $GameRoot 'Mary.dll'), (Join-Path $GameRoot 'dinput8.dll'))
    foreach ($candidate in $confirmed) { $paths += $candidate.path }
    return [ordered]@{
        running = $running; candidates = $snapshots; launcher_pids = @($launchers | ForEach-Object { $_.Id })
        fingerprints = @($paths | Select-Object -Unique | ForEach-Object { Get-ExecutableFingerprint $_ })
        ddmk_compatibility = 'unverified'; telemetry_profile = $null
        note = 'A launcher or executable name is not an attack detector or proof of DDMK compatibility.'
    }
}

function Read-IsoBoth32([byte[]]$Bytes, [int]$Offset) {
    $value = [BitConverter]::ToUInt32($Bytes, $Offset)
    [byte[]]$reverse = $Bytes[($Offset + 7)..($Offset + 4)]
    if ($value -ne [BitConverter]::ToUInt32($reverse, 0)) { throw 'Inconsistent ISO9660 endian fields.' }
    return $value
}

function Read-IsoEntry([byte[]]$Data, [int]$Position, [long]$ImageLength) {
    $size = [int]$Data[$Position]
    if ($size -lt 34 -or $Position + $size -gt $Data.Length -or $Position % 2048 + $size -gt 2048) {
        throw 'Invalid ISO directory record.'
    }
    $nameLength = [int]$Data[$Position + 32]
    if (33 + $nameLength -gt $size -or $Data[$Position + 1] -ne 0 -or
        $Data[$Position + 26] -ne 0 -or $Data[$Position + 27] -ne 0 -or ($Data[$Position + 25] -band 128)) {
        throw 'Unsupported extended/interleaved/multi-extent ISO record.'
    }
    $sector = [long](Read-IsoBoth32 $Data ($Position + 2))
    $length = [long](Read-IsoBoth32 $Data ($Position + 10))
    if ($sector * 2048 + $length -gt $ImageLength) { throw 'ISO extent exceeds file size.' }
    return [PSCustomObject]@{
        name = [Text.Encoding]::ASCII.GetString($Data, $Position + 33, $nameLength) -replace ';[0-9]+$', ''
        sector = $sector; length = $length; directory = [bool]($Data[$Position + 25] -band 2)
    }
}

function Get-CodeProbe([string]$Path) {
    $disc = [IO.File]::OpenRead($Path)
    try {
        $primary = $null
        for ($sector = 16; $sector -lt 128; $sector++) {
            $descriptor = Read-FileBytes $disc ($sector * 2048) 2048
            if ([Text.Encoding]::ASCII.GetString($descriptor, 1, 5) -ne 'CD001' -or $descriptor[6] -ne 1) {
                throw 'Expected an uncompressed ISO9660 image, 2048-byte sectors.'
            }
            if ($descriptor[0] -eq 1) { $primary = $descriptor; break }
            if ($descriptor[0] -eq 255) { break }
        }
        if ($null -eq $primary -or [BitConverter]::ToUInt16($primary, 128) -ne 2048 -or
            $primary[130] -ne 8 -or $primary[131] -ne 0) { throw 'Unsupported ISO volume descriptor.' }
        $root = Read-IsoEntry $primary 156 $disc.Length
        if (-not $root.directory) { throw 'ISO root is not a directory.' }
        $directory = Read-FileBytes $disc ($root.sector * 2048) ([int]$root.length)
        $rows = New-Object 'System.Collections.Generic.List[object]'
        $position = 0
        while ($position -lt $directory.Length) {
            if ($directory[$position] -eq 0) {
                $position = [int]([Math]::Floor($position / 2048) + 1) * 2048
                continue
            }
            $entry = Read-IsoEntry $directory $position $disc.Length
            $rows.Add($entry)
            $position += $directory[$position]
        }
        $configs = @($rows | Where-Object { -not $_.directory -and $_.name -ieq 'SYSTEM.CNF' })
        if ($configs.Count -ne 1 -or $configs[0].length -gt 8192) { throw 'Missing/ambiguous SYSTEM.CNF.' }
        $cnf = [Text.Encoding]::ASCII.GetString((Read-FileBytes $disc ($configs[0].sector * 2048) ([int]$configs[0].length)))
        if ($cnf -notmatch '(?im)^\s*BOOT2\s*=\s*cdrom0?:[\\/]*SCUS_974\.81(?:;1)?\s*$') {
            throw 'ISO BOOT2 does not identify SCUS-97481.'
        }
        $executables = @($rows | Where-Object { -not $_.directory -and $_.name -ieq 'SCUS_974.81' })
        if ($executables.Count -ne 1) { throw 'SCUS_974.81 missing or ambiguous in ISO root.' }
        $exe = $executables[0]
        $base = $exe.sector * 2048
        $header = Read-FileBytes $disc $base 52
        if ([BitConverter]::ToUInt32($header, 0) -ne 0x464c457f -or $header[4] -ne 1 -or
            $header[5] -ne 1 -or $header[6] -ne 1 -or [BitConverter]::ToUInt16($header, 16) -ne 2 -or
            [BitConverter]::ToUInt16($header, 18) -ne 8) { throw 'Expected little-endian ELF32 MIPS executable.' }
        $entryAddress = [long][BitConverter]::ToUInt32($header, 24)
        $phOffset = [long][BitConverter]::ToUInt32($header, 28)
        $phSize = [BitConverter]::ToUInt16($header, 42)
        $phCount = [BitConverter]::ToUInt16($header, 44)
        if ($exe.length -lt 52 -or $phSize -ne 32 -or $phCount -lt 1 -or $phCount -gt 128 -or
            $phOffset -lt 52 -or $phOffset + $phCount * 32 -gt $exe.length) { throw 'Invalid ELF program headers.' }
        $segments = New-Object 'System.Collections.Generic.List[object]'
        for ($i = 0; $i -lt $phCount; $i++) {
            $ph = Read-FileBytes $disc ($base + $phOffset + $i * 32) 32
            $type = [BitConverter]::ToUInt32($ph, 0)
            $offset = [long][BitConverter]::ToUInt32($ph, 4)
            $vaddr = [long][BitConverter]::ToUInt32($ph, 8)
            $fileSize = [long][BitConverter]::ToUInt32($ph, 16)
            $memorySize = [long][BitConverter]::ToUInt32($ph, 20)
            $flags = [BitConverter]::ToUInt32($ph, 24)
            if ($type -eq 1 -and ($flags -band 1) -and $entryAddress -ge $vaddr -and $entryAddress + 4 -le $vaddr + $fileSize) {
                if ($fileSize -gt $memorySize -or $offset + $fileSize -gt $exe.length) { throw 'Invalid ELF load segment.' }
                $segments.Add([PSCustomObject]@{ offset = $offset; vaddr = $vaddr })
            }
        }
        if ($segments.Count -ne 1) { throw 'ELF entry is not uniquely backed by an executable load segment.' }
        # Accept direct RAM or its MIPS KSEG0/KSEG1 aliases, never arbitrary MMIO.
        $eeAddress = $entryAddress -band 0x1fffffff
        if (($entryAddress -ne $eeAddress -and $entryAddress -ne $eeAddress + 0x80000000L -and
             $entryAddress -ne $eeAddress + 0xa0000000L) -or $eeAddress % 4 -ne 0 -or $eeAddress + 4 -gt 0x02000000) {
            throw 'ELF entry is outside aligned EE RAM.'
        }
        $fileOffset = $segments[0].offset + ($entryAddress - $segments[0].vaddr)
        $instruction = Read-FileBytes $disc ($base + $fileOffset) 4
        return [ordered]@{
            provenance = 'ISO SCUS_974.81 executable PT_LOAD entry instruction, not a gameplay variable'
            iso_path = $Path; elf_entry = ('0x{0:X8}' -f $entryAddress)
            ee_address = [uint32]$eeAddress; ee_address_hex = ('0x{0:X8}' -f $eeAddress)
            elf_file_offset = $fileOffset; expected_u32 = [BitConverter]::ToUInt32($instruction, 0)
            expected_hex = ('0x{0:X8}' -f [BitConverter]::ToUInt32($instruction, 0))
        }
    } finally { $disc.Dispose() }
}

function Read-NetworkExact([IO.Stream]$Stream, [int]$Count, [long]$Deadline) {
    $buffer = New-Object byte[] $Count
    $done = 0
    while ($done -lt $Count) {
        $remaining = $Deadline - $clock.ElapsedMilliseconds
        if ($remaining -le 0) { throw 'PINE reply deadline exceeded.' }
        $Stream.ReadTimeout = [int]$remaining
        $got = $Stream.Read($buffer, $done, $Count - $done)
        if ($got -eq 0) { throw 'PINE connection closed during reply.' }
        $done += $got
    }
    return ,$buffer
}

function Invoke-PineQuery([IO.Stream]$Stream, [byte]$Opcode, [byte[]]$Arguments = @()) {
    if (@(2, 8, 11, 12, 13, 14, 15) -notcontains [int]$Opcode) { throw 'Opcode is outside the read-only allowlist.' }
    if (($Opcode -eq 2 -and $Arguments.Length -ne 4) -or ($Opcode -ne 2 -and $Arguments.Length -ne 0)) {
        throw 'Invalid read-only query arguments.'
    }
    [byte[]]$frame = [BitConverter]::GetBytes([uint32](5 + $Arguments.Length)) + @($Opcode) + $Arguments
    $Stream.WriteTimeout = $TimeoutMs
    $Stream.Write($frame, 0, $frame.Length)
    $deadline = $clock.ElapsedMilliseconds + $TimeoutMs
    $header = Read-NetworkExact $Stream 4 $deadline
    $length = [BitConverter]::ToUInt32($header, 0)
    if ($length -lt 5 -or $length -gt 16384) { throw 'Invalid PINE reply length (limit 16 KiB).' }
    $body = Read-NetworkExact $Stream ([int]$length - 4) $deadline
    if ($body[0] -eq 255) { throw ('PINE IPC_FAIL for opcode {0}.' -f $Opcode) }
    if ($body[0] -ne 0) { throw 'Unknown PINE result code.' }
    if ($Opcode -eq 2 -or $Opcode -eq 15) {
        if ($body.Length -ne 5) { throw 'Invalid PINE uint32 payload.' }
        $value = [BitConverter]::ToUInt32($body, 1)
    } else {
        if ($body.Length -lt 6) { throw 'Truncated PINE string.' }
        $stringLength = [BitConverter]::ToUInt32($body, 1)
        if ($stringLength -lt 1 -or $stringLength -ne $body.Length - 5 -or $body[$body.Length - 1] -ne 0) {
            throw 'Invalid PINE string length or terminator.'
        }
        $value = $utf8.GetString($body, 5, [int]$stringLength - 1)
        if ($value.IndexOf([char]0) -ge 0) { throw 'Embedded NUL in PINE string.' }
    }
    Add-Event 'pine.reply' ([ordered]@{ opcode = [int]$Opcode; value = $value })
    return $value
}

function Get-PineIdentity([IO.Stream]$Stream) {
    return [ordered]@{
        title = (Invoke-PineQuery $Stream 11); serial = (Invoke-PineQuery $Stream 12)
        crc = (Invoke-PineQuery $Stream 13); game_version = (Invoke-PineQuery $Stream 14)
    }
}

function Test-Target([object]$Identity) {
    return $Identity.serial -ieq 'SCUS-97481' -and $Identity.crc -ieq '2F123FD8'
}

$client = $null
try {
    Add-Event 'session.start' ([ordered]@{ read_only = $true; pine_endpoint = "127.0.0.1:$PinePort" })
    try {
        $report.pcsx2_processes = @(Get-Process -Name 'pcsx2*' -ErrorAction SilentlyContinue | ForEach-Object { Get-ProcessSnapshot $_ })
        Add-Event 'pcsx2.processes' $report.pcsx2_processes
    } catch { Add-Failure 'pcsx2.processes' $_.Exception.Message }
    try { $report.dmc3 = Get-DmcDiagnostic; Add-Event 'dmc3.diagnostic' $report.dmc3 }
    catch { Add-Failure 'dmc3.diagnostic' $_.Exception.Message }

    $pine = [ordered]@{
        endpoint = "127.0.0.1:$PinePort"; tcp_connected = $false; responds = $false
        version = $null; version_supported = $false; status = $null; status_name = 'unknown'
        identity = $null; target_matches = $false
        process_association = 'Process list and PINE identity observed independently; listener PID not verified.'
    }
    $report.pine = $pine
    $report.memory_test = [ordered]@{ status = 'not_attempted'; matches_iso = $false }
    try {
        $client = New-Object Net.Sockets.TcpClient
        $pending = $client.BeginConnect('127.0.0.1', $PinePort, $null, $null)
        try {
            if (-not $pending.AsyncWaitHandle.WaitOne($TimeoutMs)) { throw 'PINE connect timed out. Check Enable PINE and Slot.' }
            $client.EndConnect($pending)
        } finally { $pending.AsyncWaitHandle.Close() }
        $client.NoDelay = $true
        $pine.tcp_connected = $true
        $stream = $client.GetStream()
        $pine.version = Invoke-PineQuery $stream 8
        if ($pine.version -notmatch '^PCSX2\s') { throw 'Endpoint does not identify itself as PCSX2.' }
        $pine.status = Invoke-PineQuery $stream 15
        if ($pine.status -gt 2) { throw 'Unknown PINE VM status.' }
        $pine.responds = $true
        $pine.version_supported = $pine.version -match '^PCSX2\s+v?2\.8\.2(?:[.\s\-+]|$)'
        $pine.status_name = @('running', 'paused', 'shutdown')[[int]$pine.status]
        if ($pine.status -ne 2) {
            $pine.identity = Get-PineIdentity $stream
            $pine.target_matches = Test-Target $pine.identity
        }
        if ($pine.status -eq 2) { $report.memory_test.reason = 'VM shutdown: no game loaded.' }
        elseif (-not $pine.target_matches) { $report.memory_test.reason = 'Wrong/unknown game serial or CRC: memory read refused.' }
        elseif (-not $pine.version_supported) { $report.memory_test.reason = 'PCSX2 version differs from researched 2.8.2: memory read refused.' }
        else {
            # Read disk metadata before requesting any EE RAM. No arbitrary address parameter exists.
            $probe = Get-CodeProbe $IsoPath
            $report.memory_test.probe = $probe
            $beforeStatus = Invoke-PineQuery $stream 15
            if ($beforeStatus -gt 1 -or -not (Test-Target (Get-PineIdentity $stream))) {
                throw 'Game changed before memory probe; read refused.'
            }
            $actual = Invoke-PineQuery $stream 2 ([BitConverter]::GetBytes([uint32]$probe.ee_address))
            $report.memory_test.actual_hex = '0x{0:X8}' -f $actual
            $report.memory_test.status = 'read'
            $afterStatus = Invoke-PineQuery $stream 15
            $afterIdentity = Get-PineIdentity $stream
            $report.memory_test.identity_after = $afterIdentity
            $report.memory_test.status_after = $afterStatus
            if ($afterStatus -gt 1 -or -not (Test-Target $afterIdentity)) { throw 'Game changed during probe; result invalidated.' }
            $report.memory_test.matches_iso = ($actual -eq $probe.expected_u32)
            if ($report.memory_test.matches_iso) { $report.memory_test.status = 'verified' }
            else { Add-Failure 'memory_test' 'Instruction differs from ISO; investigate boot state/patches/build. No write attempted.' }
        }
    } catch {
        $report.memory_test.status = 'incomplete'
        $report.memory_test.matches_iso = $false
        Add-Failure 'pine' $_.Exception.Message
    } finally { if ($null -ne $client) { $client.Dispose(); $client = $null } }
    $report.phase1_verified = $report.memory_test.status -eq 'verified'
    Add-Event 'session.result' ([ordered]@{ phase1_verified = $report.phase1_verified })
} catch { Add-Failure 'session' $_.Exception.Message }
finally {
    if ($null -ne $client) { $client.Dispose() }
    $report.errors = @($script:errors.ToArray())
    $report.completed_utc = [DateTime]::UtcNow.ToString('o')
    $report.elapsed_ms = $clock.ElapsedMilliseconds
    [IO.File]::WriteAllText((Join-Path $run 'report.json'), ($report | ConvertTo-Json -Depth 14), $utf8)
}

Write-Host "Diagnostico guardado en: $run"
Write-Host ('PINE + identidad + lectura ELF verificados: ' + $report.phase1_verified)
Write-Host 'No se detectaron ataques ni se enviaron acciones. Adjunta report.json y events.jsonl.'
if (-not $report.phase1_verified) { exit 1 }
