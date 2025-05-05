# Scripts

This folder contains helper scripts used during build, test, and benchmarking workflows.

To automatically source all `.sh` files in this directory, add the following to your `~/.bashrc`:

```bash
for script in ~/beegfs-thesis/scripts/*.sh; do
  [ -r "$script" ] && source "$script"
done
````

This ensures that any shell functions or environment variables defined in these scripts are available in your terminal sessions.

---

## Repository Structure

* **`beegfs-service/`** – Service helpers for BeeGFS.
* **`beegfs-swap/`** – Binary updater for services and module.
* **`conf.sh/`** – Configuration for the other scripts.
* **`cpy-binaries/`** – Distribution of binaries after build.
* **`fio-run/`** – Helper for FIO benchmarking.


---
