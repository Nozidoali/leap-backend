LEAP-Backend
============

This is the backend for the LEAP project. It contains the folloinwg necessary algorithms to process the subject graph.
- **blif** handles the read/write of BLIF files and provides interface to manipulate the logic network.
- **cute** is a packge for cut enumeration.
- **map** is the LUT mapping algorithm with Boolean simulation.
- **milp** contains several MILP models for timing regulation whose optimization is powered by Gurobi.

Installation
------------

1. (**recommended**) Download backend as a submodule of the main project.

2. Install and use it elsewhere.

```bash
pip install -e .
```

Getting Started
---------------

The example can be executed using `python examples/mapbuf.py`. This example:
1. Takes the BLIF file `examples/add2/add2.blif` as input (synthesized from `examples/add2/add2.v`).
2. Reads the schedulability constraints from `examples/add2/add2.json`.
3. Maps the logic network to a LUT-based FPGA with `maxLeaves=3` and `clockPeriod=1ns` (1 LUT level is `0.7ns`).
4. Writes the optimized BLIF file to `examples/add2/add2_opt.blif`.

```python
if __name__ == "__main__":
    from backend import *
    
    input_file = "examples/add2/add2.blif"
    input_sched_constr = "examples/add2/add2.json"
    output_file = "examples/add2/add2_opt.blif"

    graph = read_blif(input_file)
    model = MapBufModel(graph, json.load(open(input_sched_constr)), 1, {"maxLeaves": 3})
    model.solve()
    model.dumpGraph(output_file)

    import subprocess

    # CEC check works if no buffer is inserted
    # subprocess.run(f"abc -c 'cec {input_file} {output_file}'", shell=True)
    subprocess.run(f"abc -c 'read {output_file}; print_stats'", shell=True)
```
