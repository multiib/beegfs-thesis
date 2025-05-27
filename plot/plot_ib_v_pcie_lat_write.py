#!/usr/bin/env python3

from utils import *

# File paths
OUT_FILE  = Path.home() / "beegfs-thesis/img/ib_v_pcie_lat_write.pdf"
IB_DATA   = Path.home() / "beegfs-thesis/benchmarks/ib/ib_write_lat/run.csv"
PCIE_DATA = Path.home() / "beegfs-thesis/benchmarks/scipp/ex3"

# Configurations
X_AXIS_LABEL = "Message size [bytes] ($\\log_{2}$)"
Y_AXIS_LABEL = "Latency [\\textmu s]"

EXP_START = 5
EXP_END = 13

def main() -> None:

    # Standarized plotting style
    apply_palatino_style(font_size=14, tick_size=12)
    fig, ax = standard_ax()

    # Load data
    msg_size = powers_of_two(EXP_START, EXP_END)
    ib_mean = load_csv_column(IB_DATA, "t_avg[usec]")
    ib_std = load_csv_column(IB_DATA, "t_stdev[usec]")
    pcie_data = load_dolphin(PCIE_DATA, "latency (usec)")


    ib_mean = ib_mean
    ib_std = ib_std

    pcie_mean, pcie_std, pcie_var = stats_2d(pcie_data)

    # remove first 4 values from pcie_mean and pcie_std np.array
    pcie_mean = pcie_mean[4:]
    pcie_std = pcie_std[4:]

    # remove last 10 values from ib_mean and ib_std np.array
    ib_mean = ib_mean[:-10]
    ib_std = ib_std[:-10]







    # Plot data
    plot_line(ax, msg_size, ib_mean, color=palette["ib"], label="InfiniBand (4x HDR)", marker="o")
    plot_line(ax, msg_size, pcie_mean, color=palette["dis"], label="PCIe (Gen4 x16)", marker="o")

    # Plot std dev shaded area
    plot_std_fill(ax, msg_size, ib_mean, ib_std, palette["ib"])
    plot_std_fill(ax, msg_size, pcie_mean, pcie_std, palette["dis"])


    # Axis styling
    set_axis_labels(ax, X_AXIS_LABEL, Y_AXIS_LABEL)
    set_log_byte_ticks(ax, EXP_START, EXP_END, rotation=45)

    # Other settings
    ax.grid(True, which="both", linestyle="--", linewidth=0.5, alpha=0.7)

    # Save
    save_fig(fig, ax, OUT_FILE)

if __name__ == "__main__":
    main()
