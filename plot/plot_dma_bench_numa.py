#!/usr/bin/env python3

from utils import *

# File paths
OUT_FILE         = Path.home() / "beegfs-thesis/img/dma_bench_numa.pdf"
NUMA_BOUND_DIR   = Path.home() / "beegfs-thesis/bench/dma_bench/ex3/numa_bound"
NUMA_DEFAULT_DIR = Path.home() / "beegfs-thesis/bench/dma_bench/ex3/numa_default"

# Configurations
X_AXIS_LABEL = "Message size [bytes] ($\\log_{2}$)"
Y_AXIS_LABEL = "Bandwidth [GB/s]"

def main() -> None:

    # Standarized plotting style
    apply_palatino_style(font_size=14, tick_size=12)
    fig, ax = standard_ax()

    # Load data (2D array)
    msg_size = powers_of_two(6, 24)
    numa_bound = load_dolphin(NUMA_BOUND_DIR, "Bandwidth")
    numa_default = load_dolphin(NUMA_DEFAULT_DIR, "Bandwidth")

    # MiB to GB conversion
    numa_bound = [x * MIB_TO_GB for x in numa_bound]
    numa_default = [x * MIB_TO_GB for x in numa_default]

    numa_bound_mean, numa_bound_std, numa_bound_var = stats_2d(numa_bound)
    numa_default_mean, numa_default_std, numa_default_var = stats_2d(numa_default)

    # Plot data
    plot_line(ax, msg_size, numa_bound_mean, color=palette["dis"],label="Bound to NUMA node", marker="o")
    plot_line(ax, msg_size, numa_default_mean, color=palette["dis2"],label="Default CPU affinity", marker="s")

    # Plot std dev shaded area
    plot_std_fill(ax, msg_size, numa_bound_mean, numa_bound_std, palette["dis"])
    plot_std_fill(ax, msg_size, numa_default_mean, numa_default_std, palette["dis2"])

    # Axis styling
    set_axis_labels(ax, X_AXIS_LABEL, Y_AXIS_LABEL)
    set_log_byte_ticks(ax, 6, 24, rotation=45)

    # Other settings
    ax.grid(True, which="both", linestyle="--", linewidth=0.5, alpha=0.7)

    # Save
    save_fig(fig, ax, OUT_FILE)

if __name__ == "__main__":
    main()


