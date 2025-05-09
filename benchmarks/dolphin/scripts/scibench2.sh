#!/bin/bash

# On remote server, first run:
# /opt/DIS/bin/scibench2 -rn N -server

# Check minimum argument count
if [ $# -lt 2 ]; then
  echo "Usage: $0 <rn_number> <filename> [additional scibench2 parameters]"
  exit 1
fi

# Parse inputs
RN="$1"
FILENAME="$2"
shift 2

# Construct path to JSON file
JSON_PATH="$HOME/beegfs-thesis/benchmarks/dolphin/out/scibench2/${FILENAME}.json"

# Run scibench2 with required and optional parameters
/opt/DIS/bin/scibench2 -rn "$RN" -client -json "$JSON_PATH" "$@"
