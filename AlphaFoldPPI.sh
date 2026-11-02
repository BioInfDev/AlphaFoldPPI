#!/usr/bin/env bash
set -euo pipefail
shopt -s nullglob

FOLD="$(cd -- "$1" && pwd)"
CHAIN_A="$2"
CHAIN_B="$3"

PROJECT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
SCRIPTS_DIR="$PROJECT_DIR/src"

mkdir "$PWD/AlphaFoldPPI_${CHAIN_A}_${CHAIN_B}" && cd "$PWD/AlphaFoldPPI_${CHAIN_A}_${CHAIN_B}"

python3 "$SCRIPTS_DIR/metrics.py" "$FOLD" -c1 "$CHAIN_A" -c2 "$CHAIN_B"

for ((i = 0; i <= 4; i++)); do
    mkdir -p "model_$i" && cd "model_$i"

    CIF="$FOLD/${FOLD##*/}_model_$i.cif"
    FULL_DATA="$FOLD/${FOLD##*/}_full_data_$i.json"
    python3 "$SCRIPTS_DIR/render.py" "$CIF" -c1 "$CHAIN_A" -c2 "$CHAIN_B"
    python3 "$SCRIPTS_DIR/contact-map.py" "$CIF" -c1 "$CHAIN_A" -c2 "$CHAIN_B"
    python3 "$SCRIPTS_DIR/pae.py" "$FULL_DATA" -c1 "$CHAIN_A" -c2 "$CHAIN_B"
    python3 "$SCRIPTS_DIR/contact-probs.py" "$FULL_DATA" -c1 "$CHAIN_A" -c2 "$CHAIN_B"
    python3 "$SCRIPTS_DIR/plddt.py" "$FULL_DATA" -c1 "$CHAIN_A" -c2 "$CHAIN_B"

    cd ..
    
    mv ./*_model_$i*.csv "./model_$i"/
done