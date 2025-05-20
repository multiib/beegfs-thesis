# #!/usr/bin/env python3

from utils import *

# File paths
OUT_FILE = Path.home() / "beegfs-thesis/img/scibench2_ex3_v_mpg.pdf"
EX3_DATA = Path.home() / "beegfs-thesis/benchmarks/scibench2/ex3"
MPG_DATA = Path.home() / "beegfs-thesis/benchmarks/scibench2/mpg"

# Configurations
X_AXIS_LABEL = "Segment size [bytes] ($\\log_{2}$)"
Y_AXIS_LABEL = "Avg. send latency [\\textmu s]"

EXP_START = 2
EXP_END = 16

def main() -> None:

    # Standarized plotting style
    apply_palatino_style(font_size=14, tick_size=12)
    fig, ax = standard_ax()

    # Load data (2D array)
    msg_size = powers_of_two(EXP_START, EXP_END)
    ex3_data = load_dolphin(EX3_DATA, "Average Send Latency")
    mpg_data = load_dolphin(MPG_DATA, "Average Send Latency")

    ex3_mean, ex3_std, ex3_var = stats_2d(ex3_data)
    mpg_mean, mpg_std, mpg_var = stats_2d(mpg_data)

    # Plot data
    plot_line(ax, msg_size, ex3_mean, color=palette["dis"], label="eX3", marker="o")
    plot_line(ax, msg_size, mpg_mean, color=palette["dis2"], label="MPG", marker="o")

    # Plot std dev shaded area
    plot_std_fill(ax, msg_size, ex3_mean, ex3_std, palette["dis"])
    plot_std_fill(ax, msg_size, mpg_mean, mpg_std, palette["dis2"])



    # Axis styling
    set_axis_labels(ax, X_AXIS_LABEL, Y_AXIS_LABEL)
    set_log_byte_ticks(ax, EXP_START, EXP_END, rotation=45)

    # Other settings
    ax.grid(True, which="both", linestyle="--", linewidth=0.5, alpha=0.7)

    # Save
    save_fig(fig, ax, OUT_FILE)

if __name__ == "__main__":
    main()


