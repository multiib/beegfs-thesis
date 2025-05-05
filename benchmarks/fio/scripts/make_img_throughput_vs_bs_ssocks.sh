#!/usr/bin/env bash

# --- Configuration ---
FIO_PATH="$HOME/beegfs-thesis/benchmarks/fio"
DATA_DIR="${FIO_PATH}/out/throughput_vs_bs"
IMG_DIR="${FIO_PATH}/img/throughput_vs_bs_ssocks"
PLOT_DIR="${FIO_PATH}/plot"

# --- All plots ---
# read - seq
python3 ${FIO_PATH}/py/plot_throughput_vs_bs.py \
    --out_file "${IMG_DIR}/throughput_vs_bs_read_seq_ssocks.pdf" \
    --title "Throughput vs. Block Size (Sequential Read)" \
    --rw "read" \
    --jobs "${DATA_DIR}/throughput_vs_bs_read_seq_eth.json" \
           "${DATA_DIR}/throughput_vs_bs_read_seq_dis.json" \
           "${DATA_DIR}/throughput_vs_bs_read_seq_ssocks.json" \
    --colors "eth" "dis" "ssocks" \
    --labels "Ethernet" "IPoPCIe" "SuperSockets" \
    --x_scale "log" \

# read - rand
python3 ${FIO_PATH}/py/plot_throughput_vs_bs.py \
    --out_file "${IMG_DIR}/throughput_vs_bs_read_rand_ssocks.pdf" \
    --title "Throughput vs. Block Size (Random Read)" \
    --rw "read" \
    --jobs "${DATA_DIR}/throughput_vs_bs_read_rand_eth.json" \
           "${DATA_DIR}/throughput_vs_bs_read_rand_dis.json" \
           "${DATA_DIR}/throughput_vs_bs_read_rand_ssocks.json" \
    --colors "eth" "dis" "ssocks" \
    --labels "Ethernet" "IPoPCIe" "SuperSockets" \
    --x_scale "log" \

# read - seq rand
python3 ${FIO_PATH}/py/plot_throughput_vs_bs.py \
    --out_file "${IMG_DIR}/throughput_vs_bs_read_all_ssocks.pdf" \
    --title "Throughput vs. Block Size (Sequential and Random Read)" \
    --rw "read" \
    --jobs "${DATA_DIR}/throughput_vs_bs_read_seq_eth.json" \
           "${DATA_DIR}/throughput_vs_bs_read_seq_dis.json" \
           "${DATA_DIR}/throughput_vs_bs_read_seq_ssocks.json" \
           "${DATA_DIR}/throughput_vs_bs_read_rand_eth.json" \
           "${DATA_DIR}/throughput_vs_bs_read_rand_dis.json" \
           "${DATA_DIR}/throughput_vs_bs_read_rand_ssocks.json" \
    --colors "eth" "dis" "ssocks" "eth2" "dis2" "ssocks2" \
    --markers "o" "o" "o" "d" "d" "d" \
    --labels "Ethernet (Sequential)" "IPoPCIe (Sequential)" "SuperSockets (Sequential)" "Ethernet (Random)" "IPoPCIe (Random)" "SuperSockets (Random)" \
    --x_scale "log" \

# write - seq
python3 ${FIO_PATH}/py/plot_throughput_vs_bs.py \
    --out_file "${IMG_DIR}/throughput_vs_bs_write_seq_ssocks.pdf" \
    --title "Throughput vs. Block Size (Sequential Write)" \
    --rw "write" \
    --jobs "${DATA_DIR}/throughput_vs_bs_write_seq_eth.json" \
           "${DATA_DIR}/throughput_vs_bs_write_seq_dis.json" \
           "${DATA_DIR}/throughput_vs_bs_write_seq_ssocks.json" \
    --colors "eth" "dis" "ssocks" \
    --labels "Ethernet" "IPoPCIe" "SuperSockets" \
    --x_scale "log" \

# write - rand
python3 ${FIO_PATH}/py/plot_throughput_vs_bs.py \
    --out_file "${IMG_DIR}/throughput_vs_bs_write_rand_ssocks.pdf" \
    --title "Throughput vs. Block Size (Random Write)" \
    --rw "write" \
    --jobs "${DATA_DIR}/throughput_vs_bs_write_rand_eth.json" \
           "${DATA_DIR}/throughput_vs_bs_write_rand_dis.json" \
           "${DATA_DIR}/throughput_vs_bs_write_rand_ssocks.json" \
    --colors "eth" "dis" "ssocks" \
    --labels "Ethernet" "IPoPCIe" "SuperSockets" \
    --x_scale "log" \

# write - seq rand
python3 ${FIO_PATH}/py/plot_throughput_vs_bs.py \
    --out_file "${IMG_DIR}/throughput_vs_bs_write_all_ssocks.pdf" \
    --title "Throughput vs. Block Size (Sequential and Random Write)" \
    --rw "write" \
    --jobs "${DATA_DIR}/throughput_vs_bs_write_seq_eth.json" \
           "${DATA_DIR}/throughput_vs_bs_write_seq_dis.json" \
           "${DATA_DIR}/throughput_vs_bs_write_seq_ssocks.json" \
           "${DATA_DIR}/throughput_vs_bs_write_rand_eth.json" \
           "${DATA_DIR}/throughput_vs_bs_write_rand_dis.json" \
           "${DATA_DIR}/throughput_vs_bs_write_rand_ssocks.json" \
    --colors "eth" "dis" "ssocks" "eth2" "dis2" "ssocks2" \
    --markers "o" "o" "o" "d" "d" "d" \
    --labels "Ethernet (Sequential)" "IPoPCIe (Sequential)" "SuperSockets (Sequential)" "Ethernet (Random)" "IPoPCIe (Random)" "SuperSockets (Random)" \
    --x_scale "log" \
