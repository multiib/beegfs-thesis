#!/usr/bin/env bash

# --- Configuration ---
FIO_PATH="$HOME/beegfs-thesis/benchmarks/fio"
DATA_DIR="${FIO_PATH}/out/throughput_vs_bs"
IMG_DIR="${FIO_PATH}/img/throughput_vs_bs"
PLOT_DIR="${FIO_PATH}/plot"

# --- All plots ---
# read - seq
python3 ${FIO_PATH}/py/plot_throughput_vs_bs.py \
    --out_file "${IMG_DIR}/throughput_vs_bs_read_seq.png" \
    --title "Throughput vs. Block Size (Sequential Read)" \
    --rw "read" \
    --jobs "${DATA_DIR}/throughput_vs_bs_read_seq_eth.json" \
           "${DATA_DIR}/throughput_vs_bs_read_seq_dis.json" \
    --colors "eth" "dis" \
    --labels "Ethernet" "IPoPCIe" \
    --x_scale "log" \

# read - rand
python3 ${FIO_PATH}/py/plot_throughput_vs_bs.py \
    --out_file "${IMG_DIR}/throughput_vs_bs_read_rand.png" \
    --title "Throughput vs. Block Size (Random Read)" \
    --rw "read" \
    --jobs "${DATA_DIR}/throughput_vs_bs_read_rand_eth.json" \
           "${DATA_DIR}/throughput_vs_bs_read_rand_dis.json" \
    --colors "eth" "dis" \
    --labels "Ethernet" "IPoPCIe" \
    --x_scale "log" \

# read - seq rand
python3 ${FIO_PATH}/py/plot_throughput_vs_bs.py \
    --out_file "${IMG_DIR}/throughput_vs_bs_read_all.png" \
    --title "Throughput vs. Block Size (Sequential and Random Read)" \
    --rw "read" \
    --jobs "${DATA_DIR}/throughput_vs_bs_read_seq_eth.json" \
           "${DATA_DIR}/throughput_vs_bs_read_seq_dis.json" \
           "${DATA_DIR}/throughput_vs_bs_read_rand_eth.json" \
           "${DATA_DIR}/throughput_vs_bs_read_rand_dis.json" \
    --colors "eth" "dis" "eth2" "dis2" \
    --markers "o" "o" "d" "d" \
    --labels "Ethernet (Sequential)" "IPoPCIe (Sequential)" "Ethernet (Random)" "IPoPCIe (Random)" \
    --x_scale "log" \

# write - seq
python3 ${FIO_PATH}/py/plot_throughput_vs_bs.py \
    --out_file "${IMG_DIR}/throughput_vs_bs_write_seq.png" \
    --title "Throughput vs. Block Size (Sequential Write)" \
    --rw "write" \
    --jobs "${DATA_DIR}/throughput_vs_bs_write_seq_eth.json" \
           "${DATA_DIR}/throughput_vs_bs_write_seq_dis.json" \
    --colors "eth" "dis" \
    --labels "Ethernet" "IPoPCIe" \
    --x_scale "log" \

# write - rand
python3 ${FIO_PATH}/py/plot_throughput_vs_bs.py \
    --out_file "${IMG_DIR}/throughput_vs_bs_write_rand.png" \
    --title "Throughput vs. Block Size (Random Write)" \
    --rw "write" \
    --jobs "${DATA_DIR}/throughput_vs_bs_write_rand_eth.json" \
           "${DATA_DIR}/throughput_vs_bs_write_rand_dis.json" \
    --colors "eth" "dis" \
    --labels "Ethernet" "IPoPCIe" \
    --x_scale "log" \

# write - seq rand
python3 ${FIO_PATH}/py/plot_throughput_vs_bs.py \
    --out_file "${IMG_DIR}/throughput_vs_bs_write_all.png" \
    --title "Throughput vs. Block Size (Sequential and Random Write)" \
    --rw "write" \
    --jobs "${DATA_DIR}/throughput_vs_bs_write_seq_eth.json" \
           "${DATA_DIR}/throughput_vs_bs_write_seq_dis.json" \
           "${DATA_DIR}/throughput_vs_bs_write_rand_eth.json" \
           "${DATA_DIR}/throughput_vs_bs_write_rand_dis.json" \
    --colors "eth" "dis" "eth2" "dis2" \
    --markers "o" "o" "d" "d" \
    --labels "Ethernet (Sequential)" "IPoPCIe (Sequential)" "Ethernet (Random)" "IPoPCIe (Random)" \
    --x_scale "log" \
