#!/bin/bash

# Usage:
# ./qperf_sweep.sh <IP> <PORT> <OUTPUT_FILE>

IP="$1"
PORT="$2"
TESTS="$3"
OUTFILE="$4"

# CSV header
echo "message_size,${TESTS// /,}" > "$OUTFILE"

# Sweep 2^6 to 2^24
for ((exp=6; exp<=24; exp++)); do
    size=$((2**exp))
    echo "Testing message size $size..."

    OUTPUT=$(numactl --cpunodebind=1 qperf -cm -m "$size" "$IP" -lp "$PORT" rc_bw rc_lat)

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
dis_run_ssocks qperf  -m 32768 10.128.1.16 -lp 18515 tcp_bw tcp_lat