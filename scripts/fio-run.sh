#!/bin/bash

###############################################################################
#  Run Fio jobs on the specified interface. Save output in JSON format.
#  Function:
#    fio_run <job> <interface>
###############################################################################

fio_run() {
  # --- Usage Check ---
  if [ "$#" -ne 2 ]; then
    echo "Usage: fio_run <job> <interface>"
    return 1
  fi

  # --- Local Variables ---
  local FIO_PATH="$HOME/thesis/benchmarks/fio"
  local JOB_DIR="$FIO_PATH/job"
  local OUTPUT_DIR="$FIO_PATH/out"

  local SUBDIR="$1"
  local SUFFIX="$2"
  local JOB_SUBDIR="$JOB_DIR/$SUBDIR"
  local OUTPUT_SUBDIR="$OUTPUT_DIR/$SUBDIR"

  # --- Ensure output directory exists ---
  mkdir -p "$OUTPUT_SUBDIR"

  # --- Run Fio jobs ---
  local jobfile jobname output_file
  while IFS= read -r jobfile; do
    jobname=$(basename "$jobfile" .fio)
    output_file="${SUBDIR}_${jobname}_${SUFFIX}.json"
    echo "Running fio job: $jobfile"
    echo "Output will be saved as: $OUTPUT_SUBDIR/$output_file"
    fio --output="$OUTPUT_SUBDIR/$output_file" --output-format=json "$jobfile"
  done < <(find "$JOB_SUBDIR" -type f -name "*.fio")
}
