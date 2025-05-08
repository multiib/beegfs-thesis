#!/bin/bash

# On remote server, first run:
# /opt/DIS/bin/dma_bench -rn N -server

# Check minimum argument count
if [ $# -lt 2 ]; then
  echo "Usage: $0 <rn_number> <filename> [additional dma_bench parameters]"
  exit 1
fi

# Parse inputs
RN="$1"
FILENAME="$2"
shift 2

# Construct path to JSON file
JSON_PATH="$HOME/beegfs-thesis/benchmarks/dolphin/out/dma_bench/${FILENAME}.json"

# Run scipp with required and optional parameters
/opt/DIS/bin/dma_bench -rn "$RN" -client -json "$JSON_PATH" "$@"