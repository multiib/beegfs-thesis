#!/usr/bin/env python3

from utils import *

# Data
OUT_FILE          = Path.home() / "beegfs-thesis/benchmarks/dolphin/img/dma_bench_numa.pdf"
NUMA_BOUND_DIR   = Path.home() / "beegfs-thesis/benchmarks/dolphin/out/dma_bench/ex3/numa_bound.json"
NUMA_DEFAULT_DIR = Path.home() / "beegfs-thesis/benchmarks/dolphin/out/dma_bench/ex3/numa_default.json"

X_AXIS_LABEL = "Message size [bytes] ($\\log_{2}$)"
Y_AXIS_LABEL = "Bandwidth [GB/s]"

def main() -> None:

    # Standarized plotting style
    apply_palatino_style(font_size=14, tick_size=12)
    fig, ax = standard_ax()

    # Load data
    msg_size = powers_of_two(6, 24)
    numa_bound = load_dolphin_column(NUMA_BOUND_DATA, "Bandwidth")
    numa_default = load_dolphin_column(NUMA_DEFAULT_DATA, "Bandwidth")

    # Divide data by 1000 to convert MB/s to GB/s
    numa_bound = [x / 1000 for x in numa_bound]
    numa_default = [x / 1000 for x in numa_default]

    # Plot data
    plot_line(ax, msg_size, numa_bound, color=palette["dis"],label=r"Bound to NUMA node 1", marker="o")
    plot_line(ax, msg_size, numa_default, color=palette["dis2"],label="Default CPU affinity", marker="s")

    # Axis styling
    set_axis_labels(ax, X_AXIS_LABEL, Y_AXIS_LABEL)
    set_log_byte_ticks(ax, 6, 24, rotation=45)

    # Other settings
    ax.grid(True, which="both", linestyle="--", linewidth=0.5, alpha=0.7)

    # Save
    save_fig(fig, ax, OUT_FILE)

if __name__ == "__main__":
    main()


