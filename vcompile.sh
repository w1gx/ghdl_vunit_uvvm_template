#!/usr/bin/env bash
# ------------------------------------------------------------
# compile_tb.sh – Compile each *_tb.v testbench with its
#                 sibling .v files, placing *_tb.v LAST.
# ------------------------------------------------------------

set -euo pipefail

HDL_DIR="${1:-./hdl}"       # Root HDL directory (default: ./hdl)
OUT_DIR="./verilog_build"           # Output directory for compiled files

mkdir -p "$OUT_DIR"

echo "HDL root : $HDL_DIR"
echo "Build dir: $OUT_DIR"
echo

# Find and compile each testbench
find "$HDL_DIR" -type f -name '*_tb.v' | while IFS= read -r TB_FILE; do
    MODULE_DIR=$(dirname "$TB_FILE")
    TB_NAME=$(basename "$TB_FILE")
    TB_BASE="${TB_NAME%.v}"
    OUTPUT="$OUT_DIR/${TB_BASE}.out"

    echo "------------------------------------------------------------"
    echo "• Compiling testbench: $TB_NAME"
    echo "• Directory          : $MODULE_DIR"
    echo "• Output binary      : $OUTPUT"

    # List all .v files EXCEPT *_tb.v
    SRC_FILES=()
    for f in "$MODULE_DIR"/*.v; do
        [[ "$f" == *"_tb.v" ]] && continue
        SRC_FILES+=("$f")
    done

    # Add the testbench LAST
    SRC_FILES+=("$TB_FILE")

    echo "• Compile command:"
    echo "  iverilog -o \"$OUTPUT\" ${SRC_FILES[*]}"

    # Compile using iverilog
    if iverilog -o "$OUTPUT" "${SRC_FILES[@]}"; then
        echo "✓ SUCCESS – created $OUTPUT"
    else
        echo "✗ ERROR – failed to compile $TB_NAME"
    fi
    echo
done

