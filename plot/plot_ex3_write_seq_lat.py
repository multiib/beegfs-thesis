#!/usr/bin/env python3

from utils import *

# File paths
OUT_FILE     = Path.home() / "beegfs-thesis/img/fio_ex3_write_seq_lat.pdf"
IB_DATA = Path.home() / "beegfs-thesis/benchmarks/fio/ex3/buffered/results/write_seq_ib.json"
DIS_DATA = Path.home() / "beegfs-thesis/benchmarks/fio/ex3/buffered/results/write_seq_dis.json"
ETH_DATA = Path.home() / "beegfs-thesis/benchmarks/fio/ex3/buffered/results/write_seq_eth.json"

# Configurations
X_AXIS_LABEL = "Latency [ms] ($\\log_{2}$)"
Y_AXIS_LABEL = "Bandwidth [GB/s]"

EXP_START = 10
EXP_END = 16

def main() -> None:

    # Standarized plotting style
    apply_palatino_style(font_size=14, tick_size=12)
    fig, ax = standard_ax(ax_h=2.5)

    # Load data
    msg_size = powers_of_two(EXP_START, EXP_END)
    ib_data = load_fio(IB_DATA, rw_type="write", metric_keys=["lat_ns.mean", "lat_ns.stddev"])
    dis_data = load_fio(DIS_DATA, rw_type="write", metric_keys=["lat_ns.mean", "lat_ns.stddev"])
    eth_data = load_fio(ETH_DATA, rw_type="write", metric_keys=["lat_ns.mean", "lat_ns.stddev"])


    # remove last 8 entries from each data set
    ib_data = ib_data[:-8]
    dis_data = dis_data[:-8]
    eth_data = eth_data[:-8]


    # Convert ns to us
    NS_TO_US = 1 / 1000
    ib_data = ib_data * NS_TO_US
    dis_data = dis_data * NS_TO_US
    eth_data = eth_data * NS_TO_US





    # Slice columns
    ib_mean, ib_std = ib_data[:, 0], ib_data[:, 1]
    dis_mean, dis_std = dis_data[:, 0], dis_data[:, 1]
    eth_mean, eth_std = eth_data[:, 0], eth_data[:, 1]

    # Plot data
    plot_line(ax, msg_size, ib_mean, color=palette["ib"], label="InfiniBand (4x HDR)", marker="o")
    plot_line(ax, msg_size, dis_mean, color=palette["dis"], label="IPoPCIe (PCIe Gen4 x16)", marker="o")
    plot_line(ax, msg_size, eth_mean, color=palette["eth"], label="Ethernet (25 Gbps)", marker="o")


    # # Plot std dev shaded area
    # plot_std_fill(ax, msg_size, ib_mean, ib_std, palette["ib"])
    # plot_std_fill(ax, msg_size, dis_mean, dis_std, palette["dis"])
    # plot_std_fill(ax, msg_size, eth_mean, eth_std, palette["eth"])
    # Axis styling
    set_axis_labels(ax, X_AXIS_LABEL, Y_AXIS_LABEL)
    set_log_byte_ticks(ax, EXP_START, EXP_END, rotation=45)

    # Other settings
    ax.grid(True, which="both", linestyle="--", linewidth=0.5, alpha=0.7)

    # Save
    save_fig(fig, ax, OUT_FILE)

if __name__ == "__main__":
    main()


