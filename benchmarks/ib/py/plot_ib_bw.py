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
OUT_FILE     = Path.home() / "beegfs-thesis/benchmarks/ib/img/ib_bw.pdf"
CSV_DATA     = Path.home() / "beegfs-thesis/benchmarks/ib/out/ib_write_bw.csv"
JSON_DATA    = Path.home() / "beegfs-thesis/benchmarks/dolphin/out/dma_bench/ex3/run0.json"

X_AXIS_LABEL = "Message size [bytes] ($\\log_{2}$)"
Y_AXIS_LABEL = "Bandwidth [GB/s]"

def main() -> None:

    # Standarized plotting style
    apply_palatino_style(font_size=14, tick_size=12)
    fig, ax = standard_ax()

    # Load data
    msg_size = powers_of_two(6, 23)
    ib_lat = load_csv_column(CSV_DATA, "BW average[MB/sec]")
    pcie_lat = load_dolphin_column(JSON_DATA, "Bandwidth")

    # Divide data by 1000 to convert MB/s to GB/s
    ib_lat = [x / 1000 for x in ib_lat]
    pcie_lat = [x / 1000 for x in pcie_lat]


    # Plot data
    plot_line(ax, msg_size, ib_lat, color=palette["ib"],label="InfiniBand")
    plot_line(ax, msg_size, pcie_lat, color=palette["dis"],label="PCIe")

    # Axis styling
    set_axis_labels(ax, X_AXIS_LABEL, Y_AXIS_LABEL)
    set_log_byte_ticks(ax, 6, 23, rotation=45)

    # Other settings
    ax.grid(True, which="both", linestyle="--", linewidth=0.5, alpha=0.7)

    # Save
    save_fig(fig, ax, OUT_FILE)

if __name__ == "__main__":
    main()


