
# Scripts Directory

This directory contains a set of utility scripts used to manage BeeGFS services, interface configuration, benchmarking, and file operations. To make sure these scripts are automatically sourced when you open a terminal, add the following to your `~/.bashrc`:

```bash
for script in ~/scripts/*.sh; do
  [ -r "$script" ] && source "$script"
done
````

This ensures that any shell functions or environment variables defined in these scripts are available in your terminal sessions.

---

## Script Overview

Below is a list of scripts and their intended purpose:

### `beegfs-service.sh`

*Description:*

### `beegfs-swap.sh`

*Description:*

### `cp-binaries.sh`

*Description:*

### `enable-if.sh`

*Description:*

### `fio-run.sh`

*Description:*

---
