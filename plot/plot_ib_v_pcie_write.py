#!/usr/bin/env python3

from utils import *

# Confgurations
OUT_FILE     = Path.home() / "beegfs-thesis/img/ib_v_pcie_bw.pdf"
IB_DATA     = Path.home() / "beegfs-thesis/results/ib/ib_write_bw"
PCIE_DATA    = Path.home() / "beegfs-thesis/results/dma_bench/ex3/numa_bound"

X_AXIS_LABEL = "Message size [bytes] ($\\log_{2}$)"
Y_AXIS_LABEL = "Bandwidth [GB/s]"

def main() -> None:

    # Standarized plotting style
    apply_palatino_style(font_size=14, tick_size=12)
    fig, ax = standard_ax()

    # Load data
    msg_size = powers_of_two(6, 24)
    ib_data = load_csv(IB_DATA, key="BWaverage[MiB/sec]")
    pcie_data = load_dolphin(PCIE_DATA, "Bandwidth")


    # Convert KB to MB (vectorized)
    ib_data = ib_data * MIB_TO_GB
    pcie_data = pcie_data * MIB_TO_GB



    # Slice columns
    ib_mean, ib_std, ib_var = stats_2d(ib_data)
    pcie_mean, pcie_std, pcie_var = stats_2d(pcie_data)

    # Plot data
    plot_line(ax, msg_size, ib_mean, color=palette["ib"], label="InfiniBand (4x HDR)", marker="o")
    plot_line(ax, msg_size, pcie_mean, color=palette["dis"], label="PCIe (Gen4 x16)", marker="o")


    # Plot std dev shaded area
    plot_std_fill(ax, msg_size, ib_mean, ib_std, palette["ib"])
    plot_std_fill(ax, msg_size, pcie_mean, pcie_std, palette["dis"])

    # Axis styling
    set_axis_labels(ax, X_AXIS_LABEL, Y_AXIS_LABEL)
    set_log_byte_ticks(ax, 6, 24, rotation=45)

    # Other settings
    ax.grid(True, which="both", linestyle="--", linewidth=0.5, alpha=0.7)

    # Save
    save_fig(fig, ax, OUT_FILE)

if __name__ == "__main__":
    main()


