#!/usr/bin/env python3

from utils import *

# File paths
OUT_FILE     = Path.home() / "beegfs-thesis/img/fio_mpg_ssock_seq_vs_rand.pdf"
SSOCKS2 = Path.home() / "beegfs-thesis/benchmarks/fio/mpg/throughput_vs_bs/throughput_vs_bs_write_rand_ssocks.json"
SSOCKS1 = Path.home() / "beegfs-thesis/benchmarks/fio/mpg/throughput_vs_bs/throughput_vs_bs_write_seq_ssocks.json"

# Configurations
X_AXIS_LABEL = "Block size [bytes] ($\\log_{2}$)"
Y_AXIS_LABEL = "Throughput [MB/s]"

EXP_START = 10
EXP_END = 24

def main() -> None:

    # Standarized plotting style
    apply_palatino_style(font_size=14, tick_size=12)
    fig, ax = standard_ax(ax_h=3)

    # Load data
    msg_size = powers_of_two(EXP_START, EXP_END)
    ssocks_seq = load_fio(SSOCKS1, rw_type="write", metric_keys=["bw_mean", "bw_dev"])
    ssocks_rand = load_fio(SSOCKS2, rw_type="write", metric_keys=["bw_mean", "bw_dev"])

    # Convert KB to MB (vectorized)
    ssocks_seq = ssocks_seq * KB_TO_MB
    ssocks_rand = ssocks_rand * KB_TO_MB

    # Slice columns
    ssocks_seq_mean, ssocks_seq_std = ssocks_seq[:, 0], ssocks_seq[:, 1]
    ssocks_rand_mean, ssocks_rand_std = ssocks_rand[:, 0], ssocks_rand[:, 1]

    # Plot data
    plot_line(ax, msg_size, ssocks_seq_mean, color=palette["ssocks"], label="SuperSockets (Sequential Write)", marker="o")
    plot_line(ax, msg_size, ssocks_rand_mean, color=palette["sisci"], label="SuperSockets (Random Write)", marker="o")

    # Plot std dev shaded area
    plot_std_fill(ax, msg_size, ssocks_seq_mean, ssocks_seq_std, palette["ssocks"])
    plot_std_fill(ax, msg_size, ssocks_rand_mean, ssocks_rand_std, palette["sisci"])



    # Axis styling
    set_axis_labels(ax, X_AXIS_LABEL, Y_AXIS_LABEL)
    set_log_byte_ticks(ax, EXP_START, EXP_END, rotation=45)


    # Other settings
    ax.grid(True, which="both", linestyle="--", linewidth=0.5, alpha=0.7)

    # Save
    save_fig(fig, ax, OUT_FILE)

if __name__ == "__main__":
    main()


