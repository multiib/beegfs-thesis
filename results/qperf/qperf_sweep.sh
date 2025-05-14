#!/bin/bash

# Usage:
# ./qperf_sweep.sh <IP> <PORT> "<TESTS>" <OUTPUT_FILE>
# Example:
# ./qperf_sweep.sh 10.128.3.16 18515 "rc_bw rc_lat" results.csv

IP="$1"
PORT="$2"
TESTS="$3"
OUTFILE="$4"

# Header for CSV file
echo "message_size,${TESTS// /,}" > "$OUTFILE"

# Sweep message sizes from 2^6 to 2^24
for ((exp=6; exp<=24; exp++)); do
    size=$((2**exp))
    echo "Testing message size $size bytes..."

    # Run qperf
    OUTPUT=$(numactl --cpunodebind=1 qperf -cm1 -m "$size" "$IP" -lp "$PORT" $TESTS)

    # Parse results
    LINE="$size"
    for TEST in $TESTS; do
        VALUE=$(echo "$OUTPUT" | awk -v t="$TEST" '
            $0 ~ t":" {getline; print $3}')
        LINE+=",${VALUE:-N/A}"
    done

    echo "$LINE" >> "$OUTFILE"
done
