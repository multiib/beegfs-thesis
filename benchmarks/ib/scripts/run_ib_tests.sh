#!/bin/bash

SERVER_IP=10.128.3.16      # Provide the server IP as first argument
DEVICE=mlx5_2

# Sizes for latency: 4 to 8192
LAT_SIZES=(4 8 16 32 64 128 256 512 1024 2048 4096 8192)

# Sizes for bandwidth: 64 to 524288
BW_SIZES=(64 128 256 512 1024 2048 4096 8192 16384 32768 65536 131072 262144 524288)

LAT_FILE="$HOME/beegfs-thesis/benchmarks/ib/out/ib_latency_results.csv"
BW_FILE="$HOME/beegfs-thesis/benchmarks/ib/out/ib_bw_results.csv"

echo "size,avg_latency_usec" > $LAT_FILE
echo "size,avg_bw_MBps" > $BW_FILE

# Run latency tests
for SIZE in "${LAT_SIZES[@]}"; do
    echo "Testing latency, size = $SIZE"
    LAT_OUT=$(ib_write_lat -s $SIZE -d $DEVICE $SERVER_IP -n 10000 2>/dev/null | grep -v '^#' | tail -1)
    LAT_AVG=$(echo $LAT_OUT | awk '{print $5}')
    echo "$SIZE,$LAT_AVG" >> $LAT_FILE
done

# Run bandwidth tests
for SIZE in "${BW_SIZES[@]}"; do
    echo "Testing bandwidth, size = $SIZE"
    BW_OUT=$(ib_write_bw -s $SIZE -d $DEVICE $SERVER_IP -F -t 5 2>/dev/null | grep -v '^#' | tail -1)
    BW_AVG=$(echo $BW_OUT | awk '{print $5}')
    echo "$SIZE,$BW_AVG" >> $BW_FILE
done
