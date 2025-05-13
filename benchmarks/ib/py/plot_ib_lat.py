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
OUT_FILE     = Path.home() / "beegfs-thesis/benchmarks/ib/img/ib_lat.pdf"
CSV_DATA     = Path.home() / "beegfs-thesis/benchmarks/ib/out/ib_write_lat.csv"
JSON_DATA    = Path.home() / "beegfs-thesis/benchmarks/dolphin/out/scipp/ex3/run0.json"

X_AXIS_LABEL = "Message size [bytes] ($\\log_{2}$)"
Y_AXIS_LABEL = "Latency [\\textmu s]"

def main() -> None:

    # Standarized plotting style
    apply_palatino_style(font_size=14, tick_size=12)
    fig, ax = standard_ax()

    # Load data
    msg_size = powers_of_two(2, 13)
    ib_lat = load_csv_column(CSV_DATA, "t_avg[usec]")
    pcie_lat = load_dolphin_column(JSON_DATA, "latency (usec)")
    pcie_lat = pcie_lat[1:] # Hack: remove first element (0 msg size)

    # Plot data
    plot_line(ax, msg_size, ib_lat, color=palette["ib"],label="InfiniBand")
    plot_line(ax, msg_size, pcie_lat, color=palette["dis"],label="PCIe")

    # Axis styling
    set_axis_labels(ax, X_AXIS_LABEL, Y_AXIS_LABEL)
    set_log_byte_ticks(ax, 2, 13)

    # Save
    save_fig(fig, ax, OUT_FILE)

if __name__ == "__main__":
    main()
