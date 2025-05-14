#!/bin/bash

# Usage:
# ./qperf_sweep.sh <IP> <PORT> "<TESTS>" <OUTPUT_FILE> [--cm1]

IP="$1"
PORT="$2"
TESTS="$3"
OUTFILE="$4"
USE_CM1="$5"

# Determine whether to include -cm1
CM1_FLAG=""
if [[ "$USE_CM1" == "--cm1" ]]; then
    CM1_FLAG="-cm1"
fi

# Write CSV header
echo "message_size,${TESTS// /,}" > "$OUTFILE"

# Sweep from 2^6 to 2^24
for ((exp=6; exp<=24; exp++)); do
    size=$((2**exp))
    echo "Testing message size $size..."

    # Run qperf with optional -cm1
    OUTPUT=$(numactl --cpunodebind=1 qperf $CM1_FLAG -m "$size" "$IP" -lp "$PORT" $TESTS)

    # Parse output
    LINE="$size"
    for TEST in $TESTS; do
        VALUE=$(echo "$OUTPUT" | awk -v t="$TEST" '
            $0 ~ t":" {getline; print $3}')
        LINE+=",${VALUE:-N/A}"
    done

    echo "$LINE" >> "$OUTFILE"
done
