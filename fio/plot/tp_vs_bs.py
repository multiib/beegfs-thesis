import sys
import os
import json
import time
import matplotlib.pyplot as plt
from cycler import cycler

# Dirs
IMG_DIR = "/Users/benjaminborge/thesis/fio/img"
DATA_DIR = "/Users/benjaminborge/thesis/fio/data"

# Plot title and axis labels
TITLE = 'Throughput vs. Block Size'
X_LABEL = 'Block Size (KB)'
Y_LABEL = 'Throughput (MB/s)'

# Plot dimensions
HEIGHT = 6
WIDTH = 8

# Plot settings
X_SCALE = 'log'
Y_SCALE = 'linear'

# Labels (legend)
LABELS = [
    # 'Ethernet',
    # 'IPoPCIe',
    'Ethernet (Sequential)',
    'IPoPCIe (Sequential)',
    'Ethernet (Random)',
    'IPoPCIe (Random)',

]
# Define a list of colors (hex codes, named colors, etc.)
custom_colors = [
    "#fab900",  # BeeGFS
    "#389e9b",  # Dolphin
    "#dd0001",  # UiO
    "#00a087",  # Ceph
    "#B900FA",  # Lighter yellow variant (mix of #fab900 with white)
    "#9B389E",  # Lighter teal variant (softer, pastel teal)
    "#BEFA00",  # Lighter red variant (softer red)
    "#e5a900",  # Darker yellow variant (richer, more saturated yellow)
    "#317c7a",  # Darker teal variant (deeper teal)
    "#b50000"   # Darker red variant (more intense red)
]

# Set the custom color cycle globally
plt.rcParams['axes.prop_cycle'] = cycler(color=custom_colors)
# Command line arguments
if len(sys.argv) < 3:
    exit('Usage: python tp_vs_bs.py <out_file_name> <job1> [<job2> ...]')

out_file_name = sys.argv[1]
jobs = sys.argv[2:]
num_jobs = len(jobs)

# Create the plot.
plt.figure(figsize=(WIDTH, HEIGHT))

# Loop over each job name.
for i, job in enumerate(jobs):
    input_path = os.path.join(DATA_DIR, job)
    
    # Load the JSON data.
    with open(input_path, 'r') as f:
        data = json.load(f)
    
    block_sizes = []
    throughputs = []
    
    # Process each job entry in the JSON.
    for sub_job in data.get('jobs', []):
        sub_job_str = sub_job.get('jobname', '')
        try:
            # Assume the block size is the second token in the job name (e.g., "job_4k").
            bs_str = sub_job_str.split('_')[1]
        except IndexError:
            continue

        # Convert the block size string to a numeric value in KB.
        bs_str_lower = bs_str.lower()

        if bs_str_lower.endswith('k'):
            bs_kb = float(bs_str_lower.rstrip('k'))
        elif bs_str_lower.endswith('m'):
            bs_kb = float(bs_str_lower.rstrip('m')) * 1024
        else:
            bs_kb = float(bs_str) / 1024.0
        block_sizes.append(bs_kb)



        # Retrieve the write bandwidth in KB/s, then convert to MB/s.
        bw_kb = sub_job.get('write', {}).get('bw', 0)
        bw_mb = bw_kb / 1024.0
        throughputs.append(bw_mb)

    # If valid data was found, sort it by block size and plot.
    if block_sizes and throughputs:
        sorted_data = sorted(zip(block_sizes, throughputs))
        block_sizes, throughputs = zip(*sorted_data)
        plt.plot(block_sizes, throughputs, marker='o', linestyle='-', label=LABELS[i])
    else:
        print(f'No valid data found in {input_path}')

plt.style.use('seaborn-v0_8-paper')
ax = plt.gca()  # Get current axes
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)



plt.xlabel(X_LABEL)
plt.ylabel(Y_LABEL)
plt.title(TITLE)
plt.grid(True)
plt.xscale(X_SCALE)
plt.yscale(Y_SCALE)

if num_jobs > 1: (plt.legend())

# Save the plot to the designated output path.
output_path = os.path.join(IMG_DIR, out_file_name)
plt.savefig(output_path, dpi=300)

