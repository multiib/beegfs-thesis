#!/bin/bash
###############################################################################
#  Run Fio jobs on the specified interface. Save output in JSON format.
#  Functions:
#    fio-run <job> <interface>
###############################################################################

# --- Configuration ---
FIO_PATH="$HOME/thesis/benchmarks/fio"
JOB_DIR="$FIO_PATH/job"
OUTPUT_DIR="$FIO_PATH/out"

# --- Usage Check ---
if [ "$#" -ne 2 ]; then
  echo "Usage: $0 <job> <interface>"
  exit 1
fi

# --- Setup Variables ---
SUBDIR="$1"          # This will be used as both the job subdirectory and the prefix.
SUFFIX="$2"
JOB_SUBDIR="$JOB_DIR/$SUBDIR"
OUTPUT_SUBDIR="$OUTPUT_DIR/$SUBDIR"

# --- Check if the job subdirectory exists ---
mkdir -p "$OUTPUT_SUBDIR"

# --- Run Fio jobs ---
find "$JOB_SUBDIR" -type f -name "*.fio" | while read -r jobfile; do
  jobname=$(basename "$jobfile" .fio)
  output_file="${SUBDIR}_${jobname}_${SUFFIX}.json"
  echo "Running fio job: $jobfile"
  echo "Output will be saved as: $OUTPUT_SUBDIR/$output_file"
  fio --output="$OUTPUT_SUBDIR/$output_file" --output-format=json "$jobfile"
done
