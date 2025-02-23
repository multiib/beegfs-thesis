#!/usr/bin/env bash





# --- Configuration ---
# Local path and directories
FIO_PATH="/Users/benjaminborge/thesis/fio"

DATA_DIR="${FIO_PATH}/data/throughput_vs_bs"
IMG_DIR="${FIO_PATH}/img/throughput_vs_bs"
PLOT_DIR="${FIO_PATH}/plot"




# --- Process options ---
transfer=false
while getopts ":t" opt; do
  case $opt in
    t)
        transfer=true
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      exit 1
      ;;
  esac
done
shift $((OPTIND-1))



# --- Transfer files only if requested---

if $transfer; then
  rsync -avz --progress \
  benjabor@mpg-2014-18:/home/benjabor/fio/out/throughput_vs_bs \
  /Users/benjaminborge/thesis/fio/data

    exit 0
fi




# --- All plots ---
# read - seq
python3 ${FIO_PATH}/plot/plot_throughput_vs_bs.py \
    --out_file "${IMG_DIR}/throughput_vs_bs_read_seq.png" \
    --title "Throughput vs. Block Size (Sequential Read)" \
    --rw "read" \
    --jobs "${DATA_DIR}/throughput_vs_bs_read_seq_eth.json" \
           "${DATA_DIR}/throughput_vs_bs_read_seq_dis.json" \
    --colors "eth" "dis" \
    --labels "Ethernet" "IPoPCIe" \
    --x_scale "log" \

# read - rand
python3 ${FIO_PATH}/plot/plot_throughput_vs_bs.py \
    --out_file "${IMG_DIR}/throughput_vs_bs_read_rand.png" \
    --title "Throughput vs. Block Size (Random Read)" \
    --rw "read" \
    --jobs "${DATA_DIR}/throughput_vs_bs_read_rand_eth.json" \
           "${DATA_DIR}/throughput_vs_bs_read_rand_dis.json" \
    --colors "eth" "dis" \
    --labels "Ethernet" "IPoPCIe" \
    --x_scale "log" \

# read - seq rand
python3 ${FIO_PATH}/plot/plot_throughput_vs_bs.py \
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
python3 ${FIO_PATH}/plot/plot_throughput_vs_bs.py \
    --out_file "${IMG_DIR}/throughput_vs_bs_write_seq.png" \
    --title "Throughput vs. Block Size (Sequential Write)" \
    --rw "write" \
    --jobs "${DATA_DIR}/throughput_vs_bs_write_seq_eth.json" \
           "${DATA_DIR}/throughput_vs_bs_write_seq_dis.json" \
    --colors "eth" "dis" \
    --labels "Ethernet" "IPoPCIe" \
    --x_scale "log" \

# write - rand
python3 ${FIO_PATH}/plot/plot_throughput_vs_bs.py \
    --out_file "${IMG_DIR}/throughput_vs_bs_write_rand.png" \
    --title "Throughput vs. Block Size (Random Write)" \
    --rw "write" \
    --jobs "${DATA_DIR}/throughput_vs_bs_write_rand_eth.json" \
           "${DATA_DIR}/throughput_vs_bs_write_rand_dis.json" \
    --colors "eth" "dis" \
    --labels "Ethernet" "IPoPCIe" \
    --x_scale "log" \

# write - seq rand
python3 ${FIO_PATH}/plot/plot_throughput_vs_bs.py \
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
