#!/usr/bin/env bash
#
# Run every .fio job file in ./job/ and write each result as JSON.
# Output file name pattern:
#   latency_vs_bs + <job-file-basename> + <user-tag>
# Example:
#   ./run_all.sh mytag
#   -> latency_vs_bs_randread_mytag.json, latency_vs_bs_seqwrite_mytag.json …

set -euo pipefail

# ---------- CONFIG -----------------------------------------------------------
JOB_DIR="$HOME/beegfs-thesis/benchmarks/fio/ex3/buffered/job" # where the *.fio job files live
OUTPUT_DIR="$HOME/beegfs-thesis/benchmarks/fio/ex3/buffered/results"
# ---------------------------------------------------------------------------

# --- basic arg / sanity checks ----------------------------------------------
if [[ $# -ne 1 ]]; then
  echo "Usage: $(basename "$0") <user-tag>"
  exit 1
fi
TAG="$1"

if [[ ! -d "$JOB_DIR" ]]; then
  echo "Error: job directory '$JOB_DIR' not found."
  exit 1
fi

# --- main loop ---------------------------------------------------------------
for jobfile in "$JOB_DIR"/*.fio; do
  [[ -e "$jobfile" ]] || { echo "No .fio files in $JOB_DIR"; exit 1; }

  job_base="$(basename "$jobfile" .fio)"
  outfile="${OUTPUT_DIR}/${job_base}_${TAG}.json"

  echo "Running: $jobfile  →  $outfile"
  fio --output="$outfile" --output-format=json "$jobfile"
done