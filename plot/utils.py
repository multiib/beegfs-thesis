from __future__ import annotations

import matplotlib.ticker as ticker
import matplotlib as mpl
import matplotlib.pyplot as plt
import csv
import numpy as np
from pathlib import Path
from typing import List, Tuple, Sequence, Union
import json
import matplotlib.figure
from pathlib import Path




# Constants
MIB_TO_GB = 0.001048576  # 1 MiB in decimal gigabytes
MB_TO_GB = 0.001  # 1 MB in decimal gigabytes
KB_TO_MB = 0.001  # 1 KB in decimal megabytes

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
def load_csv_column(csv_path: Path, key: str) -> np.ndarray:
    """
    Load a single column from a CSV file as a 1D NumPy array of floats.
    """
    vals = []
    with csv_path.open(newline="") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            try:
                vals.append(float(row[key]))
            except (KeyError, ValueError):
                continue
    return np.array(vals)

def load_csv(directory: Path, key: str) -> np.ndarray:
    """
    Load a specified column from all CSV files in the directory.
    Returns a 2D NumPy array of shape (num_files, num_elements_per_file).
    """
    data = []

    for file in sorted(directory.glob("*.csv")):
        if file.is_file():
            values = load_csv_column(file, key)
            data.append(values)

    return np.array(data)

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

def load_dolphin(directory: Path, key: str) -> np.ndarray:
    """
    Load the specified column from all files in the directory using load_dolphin_column.
    Returns a 2D NumPy array with shape (num_files, num_elements_per_file).
    """
    directory = Path(directory)
    data = []

    for file in sorted(directory.glob("*.json")):
        if file.is_file():
            arr = load_dolphin_column(file, key)
            data.append(arr)

    return np.array(data)



# def load_fio(json_path: Path, rw_type: str, metric_keys: List[str]) -> np.ndarray:
#     """
#     Load multiple performance metric columns from FIO JSON output.

#     Parameters:
#         json_path   -- path to the FIO JSON file
#         rw_type     -- 'read' or 'write'
#         metric_keys -- list of keys inside 'read' or 'write' to extract (e.g., ['iops', 'bw'])

#     Returns:
#         2D NumPy array of shape (num_jobs, num_metrics)
#     """
#     with json_path.open() as f:
#         doc = json.load(f)

#     rows = []
#     for job in doc["jobs"]:
#         try:
#             row = [float(job[rw_type][key]) for key in metric_keys]
#             rows.append(row)
#         except (KeyError, ValueError, TypeError):
#             continue

#     return np.array(rows)


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
    linestyle: str = "-",
    marker: str = "o",
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
    ax.plot(x, y, color=color, label=label, lw=lw, ms=ms,
            linestyle=linestyle, marker=marker)


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

def stats_2d(array: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Compute column-wise mean, standard deviation, and variance of a 2D NumPy array.
    
    Returns:
        mean:     1D array of column-wise means
        std_dev:  1D array of column-wise standard deviations
        variance: 1D array of column-wise variances
    """
    mean = np.mean(array, axis=0)
    std_dev = np.std(array, axis=0)
    variance = np.var(array, axis=0)
    return mean, std_dev, variance

def plot_std_fill(ax, x, mean, std, color, alpha=0.2, label=None):
    """
    Plot shaded area representing standard deviation around the mean.

    Parameters:
        ax    : matplotlib Axes object
        x     : x-axis values (e.g., message sizes)
        mean  : mean values (same length as x)
        std   : standard deviation values (same length as x)
        color : color of the shaded region
        alpha : transparency (default 0.2)
        label : optional label for the shaded area
    """
    ax.fill_between(
        x,
        mean - std,
        mean + std,
        color=color,
        alpha=alpha,
        label=label,
    )







KeyPath = Union[str, Sequence[str]]



def _dig(d: dict, path: KeyPath):
    """
    Walk `d` following the components in `path` and return the leaf value.

    Parameters
    ----------
    d      : dict
        The dictionary to traverse.
    path   : KeyPath
        A dot-separated string (``"clat_ns.mean"``) **or** a tuple/list
        (``("clat_ns", "mean")``).

    Returns
    -------
    Any
        The value at the end of the path.

    Raises
    ------
    KeyError
        If any component is missing.
    """
    if isinstance(path, str):
        path = path.split(".")
    for p in path:
        d = d[p]
    return d


def load_fio(
    json_path: Path,
    rw_type: str,
    metric_paths: List[KeyPath] = None,
    *,
    # backward-compatibility alias
    metric_keys: List[KeyPath] = None
) -> np.ndarray:
    """
    Load multiple performance-metric columns from an FIO JSON result.

    Parameters
    ----------
    json_path   : pathlib.Path
        Path to the FIO JSON file.
    rw_type     : str
        Either ``"read"`` or ``"write"`` – selects the per-job block to parse.
    metric_paths : list[KeyPath], optional
        Metrics to extract.  Each entry may be:

        * A simple key (``"iops"``, ``"bw"``)
        * A *dot* path (``"clat_ns.mean"``)
        * A tuple/list of path components (``("clat_ns", "mean")``)

        Order defines the column order in the returned array.

    Keyword-only Parameters
    -----------------------
    metric_keys : list[KeyPath], optional
        **Deprecated but kept for backward compatibility** – synonym for
        *metric_paths*.  If both are provided, *metric_paths* wins.

    Returns
    -------
    numpy.ndarray
        Shape ``(n_jobs, len(metric_paths))`` of ``float`` values.

    Notes
    -----
    * Jobs missing *any* requested key (or holding non-numeric data) are
      **skipped**, mirroring the behaviour of the original function.
    * Change the error-handling block if you prefer ``NaN`` filling instead of
      skipping.
    """
    # Resolve parameter alias
    if metric_paths is None:
        metric_paths = metric_keys
    if metric_paths is None:
        raise TypeError("`metric_paths` (or `metric_keys`) must be specified.")

    # --------------------------------------------------------------------- #
    # Parse file
    # --------------------------------------------------------------------- #
    with json_path.open() as f:
        doc = json.load(f)

    rows = []
    for job in doc["jobs"]:
        try:
            row = [float(_dig(job[rw_type], path)) for path in metric_paths]
            rows.append(row)
        except (KeyError, ValueError, TypeError):
            # Skip jobs that lack any requested metric or hold non-numeric data
            continue

    return np.asarray(rows)