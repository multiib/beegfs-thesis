#!/usr/bin/env bash

# run_plot.sh
# This script:
#  1. Transfers (via scp) JSON output files from a remote host for each given job.
#  2. Lists available python plot scripts (from a specified directory) and prompts the user to choose one.
#  3. Prompts for an image file name.
#  4. Runs the chosen plot script with the JSON files as input.
#  5. Moves the resulting image file to the designated image directory with the provided name.

# --- Configuration ---
# Remote host and directories
REMOTE_HOST="benjabor@mpg-2014-18"
REMOTE_DIR="/home/benjabor/fio/out"

# Local path and directories
FIO_PATH="/Users/benjaminborge/thesis/fio"

DATA_DIR="${FIO_PATH}/data"
IMG_DIR="${FIO_PATH}/img"
PLOT_DIR="${FIO_PATH}/plot"

# Plot configuration
OUT_FILE_EXTENSION=".png"

# --- End Configuration ---

# --- Process options ---
skip_transfer=false
while getopts ":s" opt; do
  case $opt in
    s)
      skip_transfer=true
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      exit 1
      ;;
  esac
done
shift $((OPTIND-1))

# Check if at least one job name is provided
if [ "$#" -eq 0 ]; then
  echo "Usage: $0 job1 [job2 ...]"
  exit 1
fi

# Create local directories if they do not exist
mkdir -p "${DATA_DIR}"
mkdir -p "${IMG_DIR}"
mkdir -p "${PLOT_DIR}"

# --- Step 1: Transfer files for each job (unless skipped) ---
if [ "$skip_transfer" = false ]; then
  for job in "$@"; do
    remote_file="${REMOTE_DIR}/${job}.json"
    local_file="${DATA_DIR}/${job}.json"
    echo "Transferring file for job '${job}':"
    echo "  Remote: ${REMOTE_HOST}:${remote_file}"
    echo "  Local:  ${local_file}"
    
    scp "${REMOTE_HOST}:${remote_file}" "${local_file}"
    if [ $? -ne 0 ]; then
      echo "Error transferring file for job '${job}'. Exiting."
      exit 1
    fi
  done
else
  echo "Skipping file transfer as requested."
fi

# --- Step 2: Choose the plot script ---
echo -e "\nAvailable plot scripts:"
# Enable nullglob so that the glob expands to an empty list if no files match
shopt -s nullglob

# List all .py files in the plot directory (displaying only the filename)
for file in "${PLOT_DIR}"/*.py; do
  echo "$(basename "$file")"
done

# Change directory to PLOT_DIR to allow file autocompletion when reading input
pushd "$PLOT_DIR" > /dev/null
# Use -e to enable Readline autocompletion and -p for the prompt (Bash syntax)
read -e -p "Enter the plot python program name (with .py extension): " plot_script
popd > /dev/null

# Exit if the file does not exist
if [ ! -f "${PLOT_DIR}/${plot_script}" ]; then
  echo "Plot script '${plot_script}' does not exist. Exiting."
  exit 1
fi

# --- Step 3: Get the output image name ---
read -p "Enter the output image name (e.g., result.png): " out_file_name
# Append .png if the user did not include an extension
if [[ $out_file_name != *.* ]]; then
  out_file_name="${out_file_name}${OUT_FILE_EXTENSION}"
fi

# --- Step 4: Get the title for the plot ---
read -p "Enter the title for the plot: " title

# --- Step 5: Run the plot script with the JSON files as arguments ---
# Build an array of JSON files (one for each job)
json_files=()
for job in "$@"; do
  json_files+=("${DATA_DIR}/${job}.json")
done

echo -e "\nRunning plot script: ${PLOT_DIR}/${plot_script}"
# Run the plot script with the JSON files as arguments
python3 "${PLOT_DIR}/${plot_script}" "${out_file_name}" "${title}" "${json_files[@]}"



echo "Image saved to ${IMG_DIR}/${out_file_name}"


echo "Done."