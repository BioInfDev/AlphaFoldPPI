#!/usr/bin/env bash
set -euo pipefail

FOLD="$(cd -- "$1" && pwd)"
CHAIN_A="$2"
CHAIN_B="$3"

PROJECT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
SCRIPTS_DIR="$PROJECT_DIR/src"

for ((i = 0; i <= 4; i++)); do
    mkdir "model_$i" && cd "model_$i"
    CIF="$FOLD/$FOLD_model_$i.cif"
    FULL_DATA="$FOLD/$FOLD_full_data_$i.json"
    python3 "$SCRIPTS_DIR/render.py" "$CIF" -c1 "$CHAIN_A" -c2 "$CHAIN_B"

done
 