import matplotlib.ticker as ticker
import matplotlib as mpl
import matplotlib.pyplot as plt
import csv
import numpy as np
from pathlib import Path
from typing import Tuple, List
import json
import matplotlib.figure
from pathlib import Path


# Custom colors for plotting
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

from matplotlib.ticker import FuncFormatter

def set_log_byte_ticks(
    ax,
    start_exp: int,
    end_exp: int,
    axis: str = "x",
    rotation: float = 0
) -> None:
    """
    Set log-scale ticks on the specified axis to powers of 2 with human-readable
    byte labels (B, KiB, MiB, GiB), with optional label rotation.

    Parameters:
        ax        -- matplotlib Axes object
        start_exp -- starting exponent (e.g. 6 for 64 B)
        end_exp   -- ending exponent (e.g. 33 for 8 GiB)
        axis      -- 'x' or 'y' (default: 'x')
        rotation  -- tick label rotation angle in degrees (default: 0)
    """
    if axis not in ("x", "y"):
        raise ValueError("axis must be 'x' or 'y'")

    ticks = [2 ** i for i in range(start_exp, end_exp + 1)]

    def format_bytes(x, _):
        if x >= 2**30:
            return f"{int(x / 2**30)} GiB"
        elif x >= 2**20:
            return f"{int(x / 2**20)} MiB"
        elif x >= 2**10:
            return f"{int(x / 2**10)} KiB"
        else:
            return f"{int(x)} B"

    formatter = FuncFormatter(format_bytes)

    if axis == "x":
        ax.set_xscale("log", base=2)
        ax.set_xticks(ticks)
        ax.xaxis.set_major_formatter(formatter)
        for label in ax.get_xticklabels():
            label.set_rotation(rotation)
    else:
        ax.set_yscale("log", base=2)
        ax.set_yticks(ticks)
        ax.yaxis.set_major_formatter(formatter)
        for label in ax.get_yticklabels():
            label.set_rotation(rotation)


# LaTeX-compatible matplotlib style
def apply_palatino_style(font_size: int = 14, tick_size: int = 12) -> None:
    """
    Apply a LaTeX-compatible matplotlib style using Palatino fonts and custom sizes.

    Parameters:
        font_size -- Base font size for axes and labels
        tick_size -- Font size for tick labels
    """
    mpl.rcParams.update({
        "text.usetex": True,
        "font.family": "serif",
        "font.serif": ["Palatino"],
        "text.latex.preamble": r"\usepackage{mathpazo}",
        "pdf.fonttype": 42,
        "ps.fonttype": 42,

        "font.size":       font_size,
        "axes.titlesize":  font_size,
        "axes.labelsize":  font_size,
        "xtick.labelsize": tick_size,
        "ytick.labelsize": tick_size,
        "legend.fontsize": font_size,
    })


# Standardized figure and axis creation
def standard_ax(ax_w: float = 8, ax_h: float = 2.5, margin: float = 2.0):
    """
    Create a matplotlib figure with standardized axis sizing and proportional margins.

    Parameters:
        ax_w  -- width of the plotting area (in inches)
        ax_h  -- height of the plotting area (in inches)
        margin -- size of each margin (left, right, top, bottom) in inches

    Returns:
        (fig, ax) -- Matplotlib figure and axis objects
    """
    fig_w = ax_w + 2 * margin
    fig_h = ax_h + 2 * margin
    fig = plt.figure(figsize=(fig_w, fig_h))

    left   = margin / fig_w
    bottom = margin / fig_h
    width  = ax_w   / fig_w
    height = ax_h   / fig_h

    ax = fig.add_axes([left, bottom, width, height])
    # ax.legend(frameon=False)
    return fig, ax

# CSV loading function
def load_csv_column(csv_path: Path, key: str) -> List[float]:
    """
    Load a single column from a CSV file as a list of floats.
    """
    vals = []
    with csv_path.open(newline="") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            try:
                vals.append(float(row[key]))
            except (KeyError, ValueError):
                continue
    return vals



def _parse_number(s: str) -> float:
    """Extract the numeric part from a string like '123.45 MBytes/s'."""
    return float(s.split()[0])


def load_dolphin_column(json_path: Path, key: str) -> np.ndarray:
    """
    Load one column of values from a Dolphin-style JSON file.

    Parameters:
        json_path -- path to the JSON file
        key       -- key to extract (e.g., 'Throughput', 'Average Send Latency')

    Returns:
        1D NumPy array of values
    """
    with json_path.open() as f:
        doc = json.load(f)

    loop_data = doc["results"].get("loop 0", {})
    values = []

    for entry in loop_data.values():
        try:
            val = _parse_number(entry[key])
            values.append(val)
        except (KeyError, ValueError):
            continue

    return np.array(values)



def _parse_block_size(bs: str) -> int:
    """Convert FIO-style block size (e.g., '4k', '1M') to bytes."""
    units = {"k": 1024, "m": 1024**2, "g": 1024**3}
    bs = bs.strip().lower()
    if bs[-1] in units:
        return int(float(bs[:-1]) * units[bs[-1]])
    return int(bs)

def load_fio_column(json_path: Path, rw_type: str = "write", metric_key: str = "iops") -> np.ndarray:
    """
    Load a single performance metric column from FIO JSON output.

    Parameters:
        json_path  -- path to the FIO JSON file
        rw_type    -- 'read' or 'write'
        metric_key -- key inside 'read' or 'write' to extract (e.g., 'iops', 'bw')

    Returns:
        1D NumPy array of values
    """
    with json_path.open() as f:
        doc = json.load(f)

    values = []
    for job in doc["jobs"]:
        try:
            value = float(job[rw_type][metric_key])
            values.append(value)
        except (KeyError, ValueError, TypeError):
            continue

    return np.array(values)

# Generate numpy array of powers of two
def powers_of_two(n: int, m: int) -> np.ndarray:
    return 2 ** np.arange(n, m + 1)

def plot_line(
    ax,
    x: np.ndarray,
    y: np.ndarray,
    color: str,
    label: str,
    lw: float = 1.8,
    ms: float = 5,
) -> None:
    """
    Plot a styled line with optional line width and marker size.

    Parameters:
        ax    -- matplotlib Axes object
        x     -- x-axis data
        y     -- y-axis data
        color -- line color
        label -- legend label
        lw    -- line width (default: 1.8)
        ms    -- marker size (default: 5)
    """
    ax.plot(x, y, "o-", lw=lw, ms=ms, color=color, label=label)

# Save figure with directory creation

def save_fig(fig: matplotlib.figure.Figure, ax: mpl.axes.Axes, filename: str) -> None:
    """
    Save a matplotlib figure to the given file path, creating directories as needed.

    Parameters:
        fig      -- Matplotlib Figure object
        ax       -- Matplotlib Axes object
        filename -- Full file path as string (e.g., "img/plot.pdf")
    """
    path = Path(filename)
    path.parent.mkdir(parents=True, exist_ok=True)
    ax.legend(frameon=False)
    fig.savefig(path, dpi=300, bbox_inches="tight", pad_inches=0)
    print(f"Saved figure to {path}")

# Set LaTeX-formatted axis labels
def set_axis_labels(ax, xlabel: str, ylabel: str) -> None:
    """
    Set LaTeX-formatted axis labels with bold text.

    Parameters:
        ax      -- matplotlib Axes object
        xlabel  -- x-axis label as LaTeX string
        ylabel  -- y-axis label as LaTeX string
    """
    ax.set_xlabel(rf"\textbf{{{xlabel}}}")
    ax.set_ylabel(rf"\textbf{{{ylabel}}}")
