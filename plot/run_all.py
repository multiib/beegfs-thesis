#!/usr/bin/env python3

import subprocess
from pathlib import Path

def main():
    current_dir = Path(__file__).parent
    for py_file in sorted(current_dir.glob("plot*.py")):
        result = subprocess.run(["python3", str(py_file)], capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error running {py_file.name}:\n{result.stderr}")
            exit(1)
        else:
            print(f"{result.stdout}")


if __name__ == "__main__":
    main()
