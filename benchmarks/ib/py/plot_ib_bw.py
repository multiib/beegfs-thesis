#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Dict, List
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# Matplotlib style (Palatino via LaTeX)
mpl.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.serif": ["Palatino"],
    "text.latex.preamble": r"\usepackage{mathpazo}",
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
    "font.size":      14,
    "axes.titlesize": 14,
    "axes.labelsize": 14,
    "xtick.labelsize": 12,
    "ytick.labelsize": 12,
    "legend.fontsize": 14,
})

# Fig size constants (inches)
AX_W, AX_H = 8, 2.5
MARG       = dict(L=2, B=2, R=2, T=2)
FIG_W      = AX_W + MARG['L'] + MARG['R']
FIG_H      = AX_H + MARG['B'] + MARG['T']


def standard_ax():
    fig = plt.figure(figsize=(FIG_W, FIG_H))
    left   = MARG['L'] / FIG_W
    bottom = MARG['B'] / FIG_H
    width  = AX_W      / FIG_W
    height = AX_H      / FIG_H
    ax = fig.add_axes([left, bottom, width, height])
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda y, _: f"{y:.0e}"))
    return fig, ax

# Paths
IMG_DIR   = Path.home() / "beegfs-thesis/benchmarks/ib/img"
CSV_PATH1 = Path.home() / "beegfs-thesis/benchmarks/ib/out/ib_write_bw.csv"
DATA_DIR2 = Path.home() / "beegfs-thesis/benchmarks/dolphin/out/dma_bench/ex3"

palette = dict(
    ib="#76B900",    ib2="#97EC00",    
    sisci="#CF24AA", sisci2="#DF47BE", 
    dis="#389E9B",   dis2="#4ABFBB",

)

# Data parsing
_num = re.compile(r"[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?")

def _to_float(s: str) -> float:
    m = _num.search(s)
    if not m:
        raise ValueError(f"no numeric value in {s!r}")
    return float(m.group())


def _to_int(s: str) -> int:
    return int(_to_float(s))

# Data loading
def load_dataset(data_dir: Path, metric_key: str) -> Dict[int, List[float]]:
    files = list(data_dir.glob("*.json"))

    metrics: Dict[int, List[float]] = defaultdict(list)
    for path in files:
        with path.open() as f:
            doc = json.load(f)

        for loop_name, loop_data in doc.get("results", {}).items():
            if not loop_name.startswith("loop"):
                continue
            for entry in loop_data.values():
                size  = _to_int(entry["Message size"])
                value = _to_float(entry[metric_key])
                metrics[size].append(value)

    return metrics

def load_ib_csv(csv_path: Path, value_col: str = "t_avg[usec]") -> Dict[int, List[float]]:

    metrics: Dict[int, List[float]] = defaultdict(list)
    with csv_path.open(newline="") as fh:
        reader = csv.DictReader(fh)

        for row in reader:
            size  = int(row["#bytes"])
            value = float(row[value_col])
            metrics[size].append(value)

    return metrics

# Plot routine
def plot_metric(sizes1: np.ndarray, mean1: np.ndarray, sizes2: np.ndarray,
                mean2: np.ndarray, ylabel: str, outfile: Path) -> None:
    fig, ax = standard_ax()

    ax.plot(sizes1, mean1, "o-", lw=1.6, ms=5, color=palette["ib"],    label="InfiniBand")
    ax.plot(sizes2, mean2, "o-", lw=1.6, ms=5, color=palette["dis"], label="PCIe")

    ax.set_xscale("log", base=2)
    ax.set_xlabel(r"\textbf{Message size [bytes] ($\log_{2}$)}")
    ax.set_ylabel(ylabel)

    ticks = [2 ** i for i in range(6, 20)]
    ax.set_xticks(ticks)
    ax.set_xticklabels([f"{t:,}" for t in ticks], rotation=45)

    ax.legend(frameon=False)

    IMG_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(outfile, dpi=300, bbox_inches="tight", pad_inches=0)
    print(f"Saved {outfile}")

def main() -> None:

    # Load data
    lat1 = load_ib_csv(CSV_PATH1, value_col="BW average[MB/sec]")
    lat2 = load_dataset(DATA_DIR2, "Bandwidth")

    sizes1 = np.array(sorted(lat1))
    sizes2 = np.array(sorted(lat2))
    bw_mean1 = np.array([np.mean(lat1[s]) for s in sizes1])
    bw_mean2 = np.array([np.mean(lat2[s]) for s in sizes2])

    plot_metric(
        sizes1, bw_mean1/1000, sizes2, bw_mean2/1000,
        ylabel=r"\textbf{Bandwidth [GB/s]}",
        outfile=IMG_DIR / "ib_bw.pdf",
    )

if __name__ == "__main__":
    main()
