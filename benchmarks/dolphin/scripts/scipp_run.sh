#!/bin/bash

# On remote server, first run:
# scipp -rn 4 -server

# Check minimum argument count
if [ $# -lt 3 ]; then
  echo "Usage: $0 -rn <number> <filename> [additional scipp parameters]"
  exit 1
fi

# Parse and validate -rn
if [ "$1" != "-rn" ]; then
  echo "Error: First argument must be -rn"
  echo "Usage: $0 -rn <number> <filename> [additional scipp parameters]"
  exit 1
fi

RN="$2"
FILENAME="$3"
shift 3

# Construct path to JSON file
JSON_PATH="$HOME/beegfs-thesis/benchmarks/dolphin/out/scipp/${FILENAME}.json"

# Run scipp with required and optional parameters
scipp -rn "$RN" -server -parameter -json "$JSON_PATH" "$@"
