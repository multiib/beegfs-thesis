#!/usr/bin/env python3

from __future__ import annotations

import json
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Dict, List

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# ────────────────────────── Matplotlib style (Palatino via LaTeX) ─────────────
mpl.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.serif": ["Palatino"],
    "text.latex.preamble": r"\usepackage{mathpazo}",
    "pdf.fonttype": 42,
    "ps.fonttype": 42,

    # uniform font sizes
    "font.size":      13,
    "axes.titlesize": 13,
    "axes.labelsize": 13,
    "xtick.labelsize": 11,
    "ytick.labelsize": 11,
    "legend.fontsize": 13,
})

# ─────────────────────────── Axes‑size constants (inches) ─────────────────────
AX_W, AX_H = 8, 3
MARG       = dict(L=2, B=2, R=2, T=2)
FIG_W      = AX_W + MARG['L'] + MARG['R']
FIG_H      = AX_H + MARG['B'] + MARG['T']


def standard_ax():
    """Return (fig, ax) where *ax* is always AX_W x AX_H inches."""
    fig = plt.figure(figsize=(FIG_W, FIG_H))
    # convert inch margins → figure‑fraction
    left   = MARG['L'] / FIG_W
    bottom = MARG['B'] / FIG_H
    width  = AX_W      / FIG_W
    height = AX_H      / FIG_H
    ax = fig.add_axes([left, bottom, width, height])
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda y, _: f"{y:.0e}"))
    return fig, ax

# ─────────────────────────────── Paths & palette ──────────────────────────────
IMG_DIR   = Path.home() / "beegfs-thesis/benchmarks/dolphin/img/scipp"
DATA_DIR1 = Path.home() / "beegfs-thesis/benchmarks/dolphin/out/scipp/mpg"
DATA_DIR2 = Path.home() / "beegfs-thesis/benchmarks/dolphin/out/scipp/ex3"

palette = dict(
    dis="#389E9B",   dis2="#4ABFBB",   # Lab Machines
    sisci="#CF24AA", sisci2="#DF47BE", # eX3
)

# ───────────────────────────── helper regex parsers ───────────────────────────
_num = re.compile(r"[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?")

def _to_float(s: str) -> float:
    m = _num.search(s)
    if not m:
        raise ValueError(f"no numeric value in {s!r}")
    return float(m.group())


def _to_int(s: str) -> int:
    return int(_to_float(s))

# ─────────────────────────────────── I/O ───────────────────────────────────────

def load_dataset(data_dir: Path, metric_key: str) -> Dict[int, List[float]]:
    """Return {segment_size: [metric, …]} for *metric_key* in all JSON files."""
    files = list(data_dir.glob("*.json"))
    if not files:
        sys.exit(f"No JSON files found in {data_dir}!")

    metrics: Dict[int, List[float]] = defaultdict(list)
    for path in files:
        with path.open() as f:
            doc = json.load(f)

        for loop_name, loop_data in doc.get("results", {}).items():
            if not loop_name.startswith("loop"):
                continue
            for entry in loop_data.values():
                try:
                    size  = _to_int(entry["size"])
                    value = _to_float(entry[metric_key])
                    metrics[size].append(value)
                except (KeyError, ValueError):
                    pass
    return metrics

# ───────────────────────── plot routine (fixed‑frame) ─────────────────────────

def plot_metric(sizes1: np.ndarray, mean1: np.ndarray, sizes2: np.ndarray,
                mean2: np.ndarray, ylabel: str, outfile: Path) -> None:
    fig, ax = standard_ax()

    ax.plot(sizes1, mean1, "o-", lw=1.6, ms=5, color=palette["dis"],   label="Lab Machines")
    ax.plot(sizes2, mean2, "o-", lw=1.6, ms=5, color=palette["sisci"], label="eX3")

    ax.set_xscale("log", base=2)
    ax.set_xlabel(r"\textbf{Message size [bytes] ($\log_{2}$)}")
    ax.set_ylabel(ylabel)

    sizes1, mean1 = sizes1[1:], mean1[1:]
    sizes2, mean2 = sizes2[1:], mean2[1:]

    ticks = [2 ** i for i in range(2, 14)]
    ax.set_xticks(ticks)
    ax.set_xticklabels([f"{t:,}" for t in ticks], rotation=45)

    ax.legend(frameon=False)



    IMG_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(outfile, dpi=300, bbox_inches="tight", pad_inches=0)
    print(f"Saved {outfile}")

# ────────────────────────────────── main ──────────────────────────────────────

def main() -> None:

    # ——— Send latency ————————————————————————————————
    lat1 = load_dataset(DATA_DIR1, "latency (usec)")
    lat2 = load_dataset(DATA_DIR2, "latency (usec)")

    sizes1 = np.array(sorted(lat1))
    sizes2 = np.array(sorted(lat2))
    lat_mean1 = np.array([np.mean(lat1[s]) for s in sizes1])
    lat_mean2 = np.array([np.mean(lat2[s]) for s in sizes2])

    plot_metric(
        sizes1, lat_mean1, sizes2, lat_mean2,
        ylabel=r"\textbf{Latency [\textmu s]}",
        outfile=IMG_DIR / "scipp_latency_mpg_vs_ex3.pdf",
    )

# ───────────────────────────────── entry ──────────────────────────────────────
if __name__ == "__main__":
    main()





# #!/usr/bin/env python3

# from __future__ import annotations

# import json
# import re
# import sys
# from collections import defaultdict
# from pathlib import Path
# from typing import Dict, List

# import numpy as np
# import matplotlib as mpl
# import matplotlib.pyplot as plt

# # ────────────────────────── Matplotlib style (Palatino via LaTeX) ─────────────
# mpl.rcParams.update({
#     "text.usetex": True,
#     "font.family": "serif",
#     "font.serif": ["Palatino"],
#     "text.latex.preamble": r"\usepackage{mathpazo}",
#     "pdf.fonttype": 42,
#     "ps.fonttype": 42,

#     # uniform font sizes
#     "font.size":      13,
#     "axes.titlesize": 13,
#     "axes.labelsize": 13,
#     "xtick.labelsize": 11,
#     "ytick.labelsize": 11,
#     "legend.fontsize": 13,
# })

# # ─────────────────────────── Axes‑size constants (inches) ─────────────────────
# AX_W, AX_H = 8, 3
# MARG       = dict(L=2, B=2, R=2, T=2)
# FIG_W      = AX_W + MARG['L'] + MARG['R']
# FIG_H      = AX_H + MARG['B'] + MARG['T']


# def standard_ax():
#     """Return (fig, ax) where *ax* is always AX_W x AX_H inches."""
#     fig = plt.figure(figsize=(FIG_W, FIG_H))
#     # convert inch margins → figure‑fraction
#     left   = MARG['L'] / FIG_W
#     bottom = MARG['B'] / FIG_H
#     width  = AX_W      / FIG_W
#     height = AX_H      / FIG_H
#     ax = fig.add_axes([left, bottom, width, height])
#     return fig, ax

# # ─────────────────────────────── Paths & palette ──────────────────────────────
# IMG_DIR   = Path.home() / "beegfs-thesis/benchmarks/dolphin/img/scipp"
# DATA_DIR1 = Path.home() / "beegfs-thesis/benchmarks/dolphin/out/scipp/mpg"
# DATA_DIR2 = Path.home() / "beegfs-thesis/benchmarks/dolphin/out/scipp/ex3"

# palette = dict(
#     dis="#389E9B",   dis2="#4ABFBB",   # Lab Machines
#     sisci="#CF24AA", sisci2="#DF47BE", # eX3
# )



# def load_dataset(data_dir: str):
#     """Load all JSON files in *data_dir* and return a mapping size -> list[latency]."""
#     files = glob.glob(os.path.join(data_dir, "*.json"))
#     if not files:
#         sys.exit(f"No JSON files found in {data_dir}!")

#     latencies = defaultdict(list)

#     for path in files:
#         with open(path, "r") as f:
#             doc = json.load(f)

#         for loop_name, loop_data in doc.get("results", {}).items():
#             if not loop_name.startswith("loop"):
#                 continue
#             for entry in loop_data.values():
#                 try:
#                     size = int(entry["size"])
#                     lat = float(entry["latency (usec)"])
#                 except (KeyError, ValueError):
#                     continue
#                 latencies[size].append(lat)

#     return latencies


# def main() -> None:
#     # --- Load datasets ----------------------------------------------------
#     latencies1 = load_dataset(DATA_DIR1)
#     latencies2 = load_dataset(DATA_DIR2)

#     # --- Compute means ----------------------------------------------------
#     sizes1 = np.array(sorted(latencies1))
#     lat_means1 = np.array([np.mean(latencies1[s]) for s in sizes1])

#     sizes2 = np.array(sorted(latencies2))
#     lat_means2 = np.array([np.mean(latencies2[s]) for s in sizes2])

#     # Optionally drop the first point (size = 0 byte ping/pong) if present
#     if sizes1[0] == 0:
#         sizes1, lat_means1 = sizes1[1:], lat_means1[1:]
#     if sizes2[0] == 0:
#         sizes2, lat_means2 = sizes2[1:], lat_means2[1:]

#     # --- Plot -------------------------------------------------------------
#     plt.figure(figsize=(8, 3))

#     plt.plot(sizes1, lat_means1, "o-", lw=1.6, markersize=5, color=palette["dis"], label="Lab Machines")
#     plt.plot(sizes2, lat_means2, "o-", lw=1.6, markersize=5, color=palette["sisci"], label="eX3")

#     plt.xscale("log", base=2)
#     plt.xlabel("Message size (bytes, log scale)")
#     plt.ylabel("Latency (µs)")
#     plt.title("Latency vs. Message Size (scipp)")
#     plt.grid(False)
#     plt.xticks(
#         [2**i for i in range(2, 14)],
#         [f"{2**i:,}" for i in range(2, 14)],
#         rotation=45,
#     )
#     plt.legend(frameon=False)
#     plt.tight_layout()

#     # --- Save -------------------------------------------------------------
#     os.makedirs(IMG_DIR, exist_ok=True)
#     outfile = os.path.join(IMG_DIR, "scipp_mpg_vs_ex3.pdf")

#     plt.savefig(outfile, dpi=300)
#     print(f"Saved figure to {outfile}")


# if __name__ == "__main__":
#     main()
