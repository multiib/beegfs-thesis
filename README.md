# RDMA Integration for BeeGFS over PCIe NTB Interconnects

**Master’s Thesis – Informatics: Programming and Systems Architecture**
**University of Oslo, 2025**

---

## Overview

This repository supports my Master’s thesis, which explores integrating Remote Direct Memory Access (RDMA) into the BeeGFS parallel file system using PCIe Non-Transparent Bridges from Dolphin Interconnect Solutions. The thesis aims to evaluate the performance improvements and design trade-offs of replacing the traditional TCP/IP messaging layer with low-latency NTB-based RDMA communication.

## Abstract

*The final abstract will be added after the formal thesis submission.*

## Repository Structure

* **`beegfs-ssocks/`** – Fork of the BeeGFS source tree with SuperSockets support.
* **`benchmarks/`** – Scripts, configuration files and results.
* **`bin/`** - BeeGFS binaries.
* **`div/`** – Miscellaneous files.
* **`img/`** – Plots and figures to visualize benchmark results.
* **`plot/`** – Python scripts to generate plots and figures.
* **`scripts/`** – Workflow scripts.
* **`tex/`** – LaTeX source files.

## Related Resources

- [Dolphin Interconnect Solutions](https://www.dolphinics.com/) – Provider of PCIe NTB hardware and software used for low-latency interconnects.
- [ThinkParQ – BeeGFS Official Site](https://www.beegfs.io/) – Official website of the BeeGFS parallel file system developed by ThinkParQ.

## License
The original source code in the **`beegfs-ssocks`** directory is © ThinkParQ GmbH and has been modified as a part of this project. The official BeeGFS codebase is available at: [ThinkParQ/beegfs](https://github.com/ThinkParQ/beegfs)

## Citation

If you use this work in academic research, please cite:

```bibtex
@mastersthesis{borge2025thesis,
  title        = {RDMA Integration for BeeGFS over PCIe NTB Interconnects},
  author       = {Benjamin Borge},
  year         = 2025,
  month        = {May},
  address      = {Oslo, Norway},
  school       = {University of Oslo},
  type         = {Master's thesis}
}
```


