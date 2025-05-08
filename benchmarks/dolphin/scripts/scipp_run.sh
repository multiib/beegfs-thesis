#!/bin/bash

# On remote server, first run:
# scipp -rn N -server

# Check minimum argument count
if [ $# -lt 2 ]; then
  echo "Usage: $0 <rn_number> <filename> [additional scipp parameters]"
  exit 1
fi

# Parse inputs
RN="$1"
FILENAME="$2"
shift 2

# Construct path to JSON file
JSON_PATH="$HOME/beegfs-thesis/benchmarks/dolphin/out/scipp/${FILENAME}.json"

# Run scipp with required and optional parameters
scipp -rn "$RN" -server -json "$JSON_PATH" "$@"
