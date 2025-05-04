# Scripts Directory

This folder contains helper scripts used during build, test, and benchmarking workflows.

To automatically source all `.sh` files in this directory, add the following to your `~/.bashrc`:

```bash
for script in ~/scripts/*.sh; do
  [ -r "$script" ] && source "$script"
done
````

This ensures that any shell functions or environment variables defined in these scripts are available in your terminal sessions.

---

## Repository Structure

* **`beegfs-service/`** – Fill in.
* **`cpy-binaries/`** – Miscellaneous files.
* **`fio-run/`** – Workflow scripts.
* **`swap-binaries/`** – Scripts, configuration files and results.

---
