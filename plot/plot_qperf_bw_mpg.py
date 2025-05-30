#!/usr/bin/env python3

from utils import *

# File paths
OUT_FILE  = Path.home() / "beegfs-thesis/img/qperf_bw_mpg.pdf"
ETH_DATA  = Path.home() / "beegfs-thesis/benchmarks/qperf/eth"
DIS_DATA  = Path.home() / "beegfs-thesis/benchmarks/qperf/dis"
SSOCKS_DATA = Path.home() / "beegfs-thesis/benchmarks/qperf/ssocks"

# Configurations
X_AXIS_LABEL = "Message size [bytes] ($\\log_{2}$)"
Y_AXIS_LABEL = "Throughput [GB/s]"

EXP_START = 2
EXP_END = 24

def main() -> None:

    # Standarized plotting style
    apply_palatino_style(font_size=14, tick_size=12)
    fig, ax = standard_ax(ax_h=2.5)

    # Load data
    msg_size = powers_of_two(EXP_START, EXP_END)
    eth_data = load_csv(ETH_DATA, key="tcp_bw")
    dis_data = load_csv(DIS_DATA, key="tcp_bw")
    ssocks_data = load_csv(SSOCKS_DATA, key="tcp_bw")



    # Convert KB to MB (vectorized)
    eth_data = eth_data * MB_TO_GB
    dis_data = dis_data * MB_TO_GB
    ssocks_data = ssocks_data * MB_TO_GB




    # Slice columns
    eth_mean, eth_std, eth_var = stats_2d(eth_data)
    dis_mean, dis_std, dis_var = stats_2d(dis_data)
    ssocks_mean, ssocks_std, ssocks_var = stats_2d(ssocks_data)


    # Plot data
    plot_line(ax, msg_size, dis_mean, color=palette["dis"], label="IPoPCIe (PCIe Gen3 x8)", marker="o")
    # plot_line(ax, msg_size, eth_mean, color=palette["eth"], label="Ethernet", marker="o")

    # plot_line(ax, msg_size, eth_mean, color=palette["eth"], label="Ethernet (1 Gbps)", marker="o")
    plot_line(ax, msg_size, ssocks_mean, color=palette["ssocks"], label="SuperSockets (PCIe Gen3 x8)", marker="o")


    # Plot std dev shaded area
    plot_std_fill(ax, msg_size, dis_mean, dis_std, palette["dis"])
    # plot_std_fill(ax, msg_size, eth_mean, eth_std, palette["eth"])
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


