#!/bin/bash

# Server-side cmd:
# numactl --cpunodebind=1 qperf -lp 18515

IP="192.168.4.8"
PORT="18515"
TESTS="tcp_bw tcp_lat"
OUTDIR="$HOME/beegfs-thesis/benchmarks/qperf/dis"
OUTFILE="${OUTDIR}/$1"

# CSV header
echo "message_size,${TESTS// /,}" > "$OUTFILE"

# Sweep 2^2 to 2^24
for ((exp=2; exp<=24; exp++)); do
    size=$((2**exp))
    echo "Testing message size $size..."

    OUTPUT=$(qperf -m "$size" $IP -lp $PORT $TESTS)

    LINE="$size"
    for TEST in $TESTS; do
        RAW=$(echo "$OUTPUT" | awk -v t="$TEST" '
            $0 ~ t":" {getline; print $3, $4}')

        VALUE=$(echo "$RAW" | awk '{
            unit = $2
            val = $1
            if (unit == "GB/sec") {
                printf "%.2f", val * 1000
            } else if (unit == "MB/sec") {
                printf "%.2f", val
            } else if (unit == "ms") {
                printf "%.2f", val * 1000
            } else if (unit == "us") {
                printf "%.2f", val
            } else {
                printf "%.2f", val
            }
        }')

        LINE+=",${VALUE:-N/A}"
    done

    echo "$LINE" >> "$OUTFILE"
done
