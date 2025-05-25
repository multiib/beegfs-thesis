#!/usr/bin/env python3

from utils import *

# File paths
OUT_FILE     = Path.home() / "beegfs-thesis/img/fio_ex3_write_dis.pdf"
BUFFERED_DATA = Path.home() / "beegfs-thesis/benchmarks/fio/ex3/buffered/results/write_seq_dis.json"
DIRECT_DATA = Path.home() / "beegfs-thesis/benchmarks/fio/ex3/direct/results/write_seq_dis.json"

# Configurations
X_AXIS_LABEL = "Block size [bytes] ($\\log_{2}$)"
Y_AXIS_LABEL = "Bandwidth [MB/s]"

EXP_START = 10
EXP_END = 24

def main() -> None:

    # Standarized plotting style
    apply_palatino_style(font_size=14, tick_size=12)
    fig, ax = standard_ax(ax_h=4)

    # Load data
    msg_size = powers_of_two(EXP_START, EXP_END)
    direct_data = load_fio(DIRECT_DATA, rw_type="write", metric_keys=["bw_mean", "bw_dev"])
    buffered_data = load_fio(BUFFERED_DATA, rw_type="write", metric_keys=["bw_mean", "bw_dev"])

    # Convert KB to MB (vectorized)
    direct_data = direct_data * KB_TO_MB
    buffered_data = buffered_data * KB_TO_MB

    # Slice columns
    direct_mean, direct_std = direct_data[:, 0], direct_data[:, 1]
    buffered_mean, buffered_std = buffered_data[:, 0], buffered_data[:, 1]

    # Plot data
    plot_line(ax, msg_size, direct_mean, color=palette["dis"], label="IPoPCIe (direct)", marker="o")
    plot_line(ax, msg_size, buffered_mean, color=palette["dis2"], label="IPoPCIe (buffered)", marker="s")


    # Plot std dev shaded area
    plot_std_fill(ax, msg_size, direct_mean, direct_std, palette["dis"])

    plot_std_fill(ax, msg_size, buffered_mean, buffered_std, palette["dis2"])
    # Axis styling
    set_axis_labels(ax, X_AXIS_LABEL, Y_AXIS_LABEL)
    set_log_byte_ticks(ax, EXP_START, EXP_END, rotation=45)

    # Other settings
    ax.grid(True, which="both", linestyle="--", linewidth=0.5, alpha=0.7)

    # Save
    save_fig(fig, ax, OUT_FILE)

if __name__ == "__main__":
    main()


