#!/usr/bin/env python3

from utils import *

# File paths
OUT_FILE  = Path.home() / "beegfs-thesis/img/qperf_bw.pdf"
ETH_DATA  = Path.home() / "beegfs-thesis/benchmarks/qperf/eth"
IB_DATA   = Path.home() / "beegfs-thesis/benchmarks/qperf/ib"
DIS_DATA  = Path.home() / "beegfs-thesis/benchmarks/qperf/dis"
SSOCKS_DATA = Path.home() / "beegfs-thesis/benchmarks/qperf/ssocks"

# Configurations
X_AXIS_LABEL = "Message size [bytes] ($\\log_{2}$)"
Y_AXIS_LABEL = "Bandwidth [GB/s]"

EXP_START = 2
EXP_END = 24

def main() -> None:

    # Standarized plotting style
    apply_palatino_style(font_size=14, tick_size=12)
    fig, ax = standard_ax()

    # Load data
    msg_size = powers_of_two(EXP_START, EXP_END)
    eth_data = load_csv(ETH_DATA, key="tcp_bw")
    ib_data = load_csv(IB_DATA, key="rc_bw")
    dis_data = load_csv(DIS_DATA, key="tcp_bw")
    ssocks_data = load_csv(SSOCKS_DATA, key="tcp_bw")



    # Convert KB to MB (vectorized)
    ib_data = ib_data * MB_TO_GB
    eth_data = eth_data * MB_TO_GB
    dis_data = dis_data * MB_TO_GB
    ssocks_data = ssocks_data * MB_TO_GB




    # Slice columns
    ib_mean, ib_std, ib_var = stats_2d(ib_data)
    eth_mean, eth_std, eth_var = stats_2d(eth_data)
    dis_mean, dis_std, dis_var = stats_2d(dis_data)
    ssocks_mean, ssocks_std, ssocks_var = stats_2d(ssocks_data)


    # Plot data
    plot_line(ax, msg_size, ib_mean, color=palette["ib"], label="InfiniBand", marker="o")
    plot_line(ax, msg_size, dis_mean, color=palette["dis"], label="IPoPCIe", marker="o")
    plot_line(ax, msg_size, eth_mean, color=palette["eth"], label="Ethernet", marker="o")
    plot_line(ax, msg_size, ssocks_mean, color=palette["ssocks"], label="SuperSockets", marker="o")



    # Plot std dev shaded area
    plot_std_fill(ax, msg_size, ib_mean, ib_std, palette["ib"])
    plot_std_fill(ax, msg_size, dis_mean, dis_std, palette["dis"])
    plot_std_fill(ax, msg_size, eth_mean, eth_std, palette["eth"])
    plot_std_fill(ax, msg_size, ssocks_mean, ssocks_std, palette["ssocks"])
    


    # Axis styling
    set_axis_labels(ax, X_AXIS_LABEL, Y_AXIS_LABEL)
    set_log_byte_ticks(ax, EXP_START, EXP_END, rotation=45)

    # Other settings
    ax.grid(True, which="both", linestyle="--", linewidth=0.5, alpha=0.7)

    # Save
    save_fig(fig, ax, OUT_FILE)

if __name__ == "__main__":
    main()


