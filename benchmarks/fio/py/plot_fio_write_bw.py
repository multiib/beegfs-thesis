#!/usr/bin/env python3

from __future__ import annotations

import sys
from pathlib import Path

# Set up local imports
UTILS_PATH = Path.home() / "beegfs-thesis" / "utils"
sys.path.append(str(UTILS_PATH))

## Local imports
from plot_utils import *

# Confgurations
OUT_FILE     = Path.home() / "beegfs-thesis/benchmarks/fio/img/write_seq_bw.pdf"
ETH_DATA     = Path.home() / "beegfs-thesis/benchmarks/fio/out/throughput_vs_bs/throughput_vs_bs_write_seq_eth.json"
DIS_DATA     = Path.home() / "beegfs-thesis/benchmarks/fio/out/throughput_vs_bs/throughput_vs_bs_write_seq_dis.json"
SSOCKS_DATA  = Path.home() / "beegfs-thesis/benchmarks/fio/out/throughput_vs_bs/throughput_vs_bs_write_seq_ssocks.json"

X_AXIS_LABEL = "Message size [bytes] ($\\log_{2}$)"
Y_AXIS_LABEL = "Bandwidth [MB/s]"

def main() -> None:

    # Standarized plotting style
    apply_palatino_style(font_size=14, tick_size=12)
    fig, ax = standard_ax(ax_h=4)

    # Load data
    msg_size = powers_of_two(10, 24)
    eth_data = load_fio_column(ETH_DATA, rw_type="write", metric_key="bw")
    dis_data = load_fio_column(DIS_DATA, rw_type="write", metric_key="bw")
    ssocks_data = load_fio_column(SSOCKS_DATA, rw_type="write", metric_key="bw")
    
    # Divide data by 1000 to convert MB/s to GB/s
    eth_data = [x / 1000 for x in eth_data]
    dis_data = [x / 1000 for x in dis_data]
    ssocks_data = [x / 1000 for x in ssocks_data]

    # Plot data
    plot_line(ax, msg_size, eth_data, color=palette["eth"], label="Ethernet")
    plot_line(ax, msg_size, dis_data, color=palette["dis"], label="IPoPCIe")
    plot_line(ax, msg_size, ssocks_data, color=palette["ssocks"], label="SuperSockets")
    # Axis styling
    set_axis_labels(ax, X_AXIS_LABEL, Y_AXIS_LABEL)
    set_log_byte_ticks(ax, 10, 24, rotation=45)

    # Other settings
    ax.grid(True, which="both", linestyle="--", linewidth=0.5, alpha=0.7)

    # Save
    save_fig(fig, ax, OUT_FILE)

if __name__ == "__main__":
    main()


