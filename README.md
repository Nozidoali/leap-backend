LEAP-Backend
============

This is the backend for the LEAP project. It contains the folloinwg necessary algorithms to process the subject graph.
- **blif** handles the read/write of BLIF files and provides interface to manipulate the logic network.
- **cute** is a packge for cut enumeration.
- **map** is the LUT mapping algorithm with Boolean simulation.
- **milp** is contains several MILP models for timing regulation whose optimization is powered by Gurobi.

Installation
------------

1. (**recommended**) Download backend as a submodule of the main project.

2. Install and use it elsewhere.

```bash
pip install -e .
```