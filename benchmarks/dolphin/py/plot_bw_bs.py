#!/usr/bin/env python3
"""
Plot throughput vs. message size (mean of all JSON runs) for two datasets
(DATA_DIR1 and DATA_DIR2) on the same figure.
"""

import glob
import json
import os
import sys
import re
from collections import defaultdict


import numpy as np
import matplotlib.pyplot as plt

IMG_DIR = os.path.expandvars("$HOME/beegfs-thesis/benchmarks/dolphin/img/dma_bench")
DATA_DIR1 = os.path.expandvars("$HOME/beegfs-thesis/benchmarks/dolphin/out/dma_bench/mpg")
DATA_DIR2 = os.path.expandvars("$HOME/beegfs-thesis/benchmarks/dolphin/out/dma_bench/ex3")

# Custom colors
palette = {
    "eth":    "#FAB900",  # BeeGFS
    "eth2":   "#FFC92E",  # BeeGFS light
    "dis":    "#389E9B",  # Dolphin
    "dis2":   "#4ABFBB",  # Dolphin light
    "ssocks": "#DD0001",  # UiO
    "ssocks2": "#FF1112", # UiO light
    "sisci":  "#CF24AA",  # Pink
    "sisci2": "#DF47BE",  # Pink light
    "ib":     "#76B900",  # Nvidia
    "ib2":    "#97EC00",  # Nvidia light
}




_num = re.compile(r"[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?")   # grabs the first numeric literal

def _to_float(s: str) -> float:
    """Return the first numeric literal found in *s* as a float."""
    m = _num.search(s)
    if not m:
        raise ValueError(f"No numeric value in {s!r}")
    return float(m.group())

def _to_int(s: str) -> int:
    return int(_to_float(s))     # reuse the same regex, then cast to int

def load_dataset(data_dir: str):
    """Load all JSON files in *data_dir* and return {size: [bandwidth,…]}."""
    files = glob.glob(os.path.join(data_dir, "*.json"))
    if not files:
        sys.exit(f"No JSON files found in {data_dir}!")

    latencies: dict[int, list[float]] = defaultdict(list)

    for path in files:
        with open(path) as f:
            doc = json.load(f)

        for loop_name, loop_data in doc.get("results", {}).items():
            if not loop_name.startswith("loop"):
                print(f"Skipping {loop_name} in {path}")
                continue

            for entry in loop_data.values():
                try:
                    size = _to_int(entry["Message size"])
                    bw   = _to_float(entry["Bandwidth"])
                    latencies[size].append(bw)
                except (KeyError, ValueError) as exc:
                    print(f"Skipping {entry} in {path}: {exc}")

    return latencies



def main() -> None:
    # --- Load datasets ----------------------------------------------------
    latencies1 = load_dataset(DATA_DIR1)
    latencies2 = load_dataset(DATA_DIR2)

    # --- Compute means ----------------------------------------------------
    sizes1 = np.array(sorted(latencies1))
    lat_means1 = np.array([np.mean(latencies1[s]) for s in sizes1])

    sizes2 = np.array(sorted(latencies2))
    lat_means2 = np.array([np.mean(latencies2[s]) for s in sizes2])

    # Optionally drop the first point (size = 0 byte ping/pong) if present
    # if sizes1[0] == 0:
    #     sizes1, lat_means1 = sizes1[1:], lat_means1[1:]
    # if sizes2[0] == 0:
    #     sizes2, lat_means2 = sizes2[1:], lat_means2[1:]

    # --- Plot -------------------------------------------------------------
    plt.figure(figsize=(8, 3))

    plt.plot(sizes1, lat_means1, "o-", lw=1.6, markersize=5, color=palette["dis"], label="Lab Machines")
    plt.plot(sizes2, lat_means2, "o-", lw=1.6, markersize=5, color=palette["sisci"], label="eX3")

    plt.xscale("log", base=2)
    plt.xlabel("Message size (bytes, log scale)")
    plt.ylabel("Bandwidth (MB/s)")
    plt.title("Bandwith vs. Message Size (dma_bench)")
    plt.grid(False)
    plt.xticks(
        [2**i for i in range(6, 20)],
        [f"{2**i:,}" for i in range(6, 20)],
        rotation=45,
    )
    plt.legend(frameon=False)
    plt.tight_layout()

    # --- Save -------------------------------------------------------------
    os.makedirs(IMG_DIR, exist_ok=True)
    outfile = os.path.join(IMG_DIR, "dma_bench_mpg_vs_ex3.pdf")

    plt.savefig(outfile, dpi=300)
    print(f"Saved figure to {outfile}")


if __name__ == "__main__":
    main()
