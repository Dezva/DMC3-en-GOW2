#!/usr/bin/env bash
set -euo pipefail

# Dependencies only: these checkouts are not additional user projects.
dmc_tool_root=/workspace/.dmc-tools
mkdir -p "$dmc_tool_root"

prepare_dmc_dependency() {
    local dmc_repo_url="$1" dmc_commit="$2" dmc_destination="$3"
    if [[ ! -e "$dmc_destination" ]]; then
        git init -q "$dmc_destination"
        git -C "$dmc_destination" remote add origin "$dmc_repo_url"
        git -C "$dmc_destination" fetch --depth 1 origin "$dmc_commit"
        git -C "$dmc_destination" checkout --detach FETCH_HEAD
    fi
    [[ "$(git -C "$dmc_destination" rev-parse --verify 'HEAD^{commit}')" == "$dmc_commit" ]] || {
        echo 'Unexpected dependency revision; existing files preserved.' >&2
        return 1
    }
    [[ "$(git -C "$dmc_destination" remote get-url origin)" == "$dmc_repo_url" ]] || {
        echo 'Unexpected dependency origin; existing files preserved.' >&2
        return 1
    }
    git -C "$dmc_destination" diff --quiet HEAD -- || {
        echo 'Dependency has tracked modifications; existing files preserved.' >&2
        return 1
    }
}

prepare_dmc_dependency https://github.com/rehan-remade/universal-modder.git \
    23902ef42e8ea9b077bfbbf6911eb8ea0348e55a "$dmc_tool_root/universal-modder"
prepare_dmc_dependency https://github.com/deshayu/DMC3HDC-Import-Tools.git \
    248dec2a0b7984fbd0c74f85c7de94a09dd81e06 "$dmc_tool_root/dmc3-importer"

# The selected cloud image already provides Python and Blender; verify the prerequisites.
python3 -c 'import PIL, numpy, yaml; print("Universal Modder Python dependencies available")'
blender --version
UM_NO_UV=1 "$dmc_tool_root/universal-modder/bin/um" --version

# Exercise the Windows diagnostic client in cloud using the real PS runtime.
bash /workspace/DMC3-en-GOW2/tools/setup_pine_test_runtime.sh
