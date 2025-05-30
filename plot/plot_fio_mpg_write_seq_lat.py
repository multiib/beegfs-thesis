#!/usr/bin/env python3

from utils import *

# File paths
OUT_FILE     = Path.home() / "beegfs-thesis/img/fio_mpg_write_seq_lat.pdf"
ETH_DATA     = Path.home() / "beegfs-thesis/benchmarks/fio/mpg/latency_vs_bs/latency_vs_bs_write_seq_eth.json"
DIS_DATA     = Path.home() / "beegfs-thesis/benchmarks/fio/mpg/latency_vs_bs/latency_vs_bs_write_seq_dis.json"
SSOCKS_DATA  = Path.home() / "beegfs-thesis/benchmarks/fio/mpg/latency_vs_bs/latency_vs_bs_write_seq_ssocks.json"

# Configurations
X_AXIS_LABEL = "Block size [bytes] ($\\log_{2}$)"
Y_AXIS_LABEL = "Latency [\\textmu s]"

EXP_START = 10
EXP_END = 16

def main() -> None:

    # Standarized plotting style
    apply_palatino_style(font_size=14, tick_size=12)
    fig, ax = standard_ax(ax_h=4)

    # Load data
    msg_size = powers_of_two(EXP_START, EXP_END)
    eth_data = load_fio(ETH_DATA, rw_type="write", metric_keys=["lat_ns.mean", "lat_ns.stddev"])
    dis_data = load_fio(DIS_DATA, rw_type="write", metric_keys=["lat_ns.mean", "lat_ns.stddev"])
    ssocks_data = load_fio(SSOCKS_DATA, rw_type="write", metric_keys=["lat_ns.mean", "lat_ns.stddev"])

    # Remove last 8 data points
    eth_data = eth_data[:-8, :]
    dis_data = dis_data[:-8, :]
    ssocks_data = ssocks_data[:-8, :]


    # Convert ns to microseconds (vectorized)
    NS_TO_US = 1e-3
    eth_data = eth_data * NS_TO_US
    dis_data = dis_data * NS_TO_US
    ssocks_data = ssocks_data * NS_TO_US


    # Slice columns
    eth_mean, eth_std = eth_data[:, 0], eth_data[:, 1]
    dis_mean, dis_std = dis_data[:, 0], dis_data[:, 1]
    ssocks_mean, ssocks_std = ssocks_data[:, 0], ssocks_data[:, 1]

    # Plot data
    plot_line(ax, msg_size, eth_mean, color=palette["eth"], label="TCP Ethernet (1Gbps)", marker="o")
    plot_line(ax, msg_size, dis_mean, color=palette["dis"], label="IPoPCIe (PCIe Gen3 x8)", marker="o")
    plot_line(ax, msg_size, ssocks_mean, color=palette["ssocks"], label="SuperSockets (PCIe Gen3 x8)", marker="o")

    # # Plot std dev shaded area
    # plot_std_fill(ax, msg_size, eth_mean, eth_std, palette["eth"])
    # plot_std_fill(ax, msg_size, dis_mean, dis_std, palette["dis"])
    # plot_std_fill(ax, msg_size, ssocks_mean, ssocks_std, palette["ssocks"])

    # Axis styling
    set_axis_labels(ax, X_AXIS_LABEL, Y_AXIS_LABEL)
    set_log_byte_ticks(ax, EXP_START, EXP_END, rotation=45)


    # Other settings
    ax.grid(True, which="both", linestyle="--", linewidth=0.5, alpha=0.7)

    # Save
    save_fig(fig, ax, OUT_FILE)

if __name__ == "__main__":
    main()


