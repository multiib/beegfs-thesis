#!/bin/bash

# Usage:
# ./qperf_sweep.sh <IP> <PORT> "<TESTS>" <OUTPUT_FILE> [--cm1]

IP="$1"
PORT="$2"
TESTS="$3"
OUTFILE="$4"
USE_CM1="$5"

# Optional cm1 flag
CM1_FLAG=""
if [[ "$USE_CM1" == "--cm1" ]]; then
    CM1_FLAG="-cm1"
fi

# CSV header
echo "message_size,${TESTS// /,}" > "$OUTFILE"

# Sweep 2^6 to 2^24
for ((exp=6; exp<=24; exp++)); do
    size=$((2**exp))
    echo "Testing message size $size..."

    OUTPUT=$(numactl --cpunodebind=1 qperf $CM1_FLAG -m "$size" "$IP" -lp "$PORT" $TESTS)

    LINE="$size"
    for TEST in $TESTS; do
        RAW=$(echo "$OUTPUT" | awk -v t="$TEST" '
            $0 ~ t":" {getline; print $3, $4}')

        VALUE=$(echo "$RAW" | awk '{
            if ($2 == "GB/sec") {
                printf "%.2f", $1 * 1000
            } else {
                printf "%.2f", $1
            }
        }')

        LINE+=",${VALUE:-N/A}"
    done

    echo "$LINE" >> "$OUTFILE"
done
