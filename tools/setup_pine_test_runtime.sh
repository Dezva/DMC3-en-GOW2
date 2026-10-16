#!/usr/bin/env bash
set -euo pipefail

# Cloud tests only. Windows already has PowerShell; no game/loader is installed.
[[ "$(uname -m)" == x86_64 ]] || { echo 'Portable runtime requires Linux x86_64.' >&2; exit 1; }
pine_tools=/workspace/.dmc-tools
pine_archive="$pine_tools/downloads/powershell-7.4.21-linux-x64.tar.gz"
pine_runtime="$pine_tools/powershell-7.4.21"
# SHA-256 checked against Microsoft's v7.4.21 release hashes.sha256.
pine_archive_sha=3fc5e1567c450bd7bd5ae69ebb0a9a4a4e0418bbc36b0232cf6dd547f0bfc0eb
pine_binary_sha=2bc45dd82dd4f80bdd9336e8579dfde92ed2f871331160ff5a79dcc0def1a876
mkdir -p "$pine_tools/downloads"
if [[ ! -e "$pine_archive" ]]; then
    pine_download=$(mktemp "$pine_tools/downloads/powershell.XXXXXXXX")
    trap 'rm -f "$pine_download"' EXIT
    curl --fail --location --retry 2 \
        https://github.com/PowerShell/PowerShell/releases/download/v7.4.21/powershell-7.4.21-linux-x64.tar.gz \
        --output "$pine_download"
    printf '%s  %s\n' "$pine_archive_sha" "$pine_download" | sha256sum --check --status
    mv "$pine_download" "$pine_archive"
    trap - EXIT
fi
printf '%s  %s\n' "$pine_archive_sha" "$pine_archive" | sha256sum --check --status
if [[ ! -e "$pine_runtime" ]]; then
    pine_extract=$(mktemp -d "$pine_tools/powershell-extract.XXXXXXXX")
    trap 'rm -rf "$pine_extract"' EXIT
    tar -xzf "$pine_archive" -C "$pine_extract"
    chmod u+x "$pine_extract/pwsh"
    mv "$pine_extract" "$pine_runtime"
    trap - EXIT
fi
printf '%s  %s\n' "$pine_binary_sha" "$pine_runtime/pwsh" | sha256sum --check --status
mkdir -p "$pine_tools/pwsh-cache" "$pine_tools/pwsh-config" "$pine_tools/pwsh-data"
XDG_CACHE_HOME="$pine_tools/pwsh-cache" XDG_CONFIG_HOME="$pine_tools/pwsh-config" \
    XDG_DATA_HOME="$pine_tools/pwsh-data" "$pine_runtime/pwsh" -NoLogo -NoProfile -NonInteractive \
    -Command '$PSVersionTable.PSVersion.ToString()'
echo 'PINE client test runtime prepared. Use PWSH_BIN=/workspace/.dmc-tools/powershell-7.4.21/pwsh.'
