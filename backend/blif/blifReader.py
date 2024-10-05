#!/usr/bin/env python
# -*- encoding=utf8 -*-

"""
Author: Hanyu Wang
Created time: 2023-03-11 18:18:27
Last Modified by: Hanyu Wang
Last Modified time: 2023-03-11 20:05:38
"""

from typing import List, Dict
import os
from .network.blif import *


def read_blif(*args):
    if len(args) == 1:
        g: BLIFGraph = BLIFGraph()
        read_blif_impl(g, args[0])
        return g

    elif len(args) == 2:
        read_blif_impl(args[0], args[1])


def on_input(g: BLIFGraph, line: str):
    for s in line.split()[1:]:
        g.create_pi(s.strip())


def on_output(g: BLIFGraph, line: str):
    for s in line.split()[1:]:
        g.create_po(s.strip())


def on_latch(g: BLIFGraph, line: str):
    ri = line.split()[1].strip()
    ro = line.split()[2].strip()
    ro_type = line.split()[-1].strip()
    g.create_latch(ri, ro, int(ro_type))


def on_gate(g: BLIFGraph, line: str, sop: list):
    fanout = line.split()[-1]

    # constants
    # this should not be directly connected to a input, instead, we should reserve:
    #   - constant 0
    #   - constant 1
    # as two unique inputs, and connect this signals to them
    if len(line.split()) == 2:
        if len(sop) == 0:
            # weird case, we should not have this, but we can handle it
            g.create_const0(fanout)
            return

        assert (
            len(sop) == 1
        ), f"constant 0 or 1 should have only one line, but got {len(sop)}, sop: {sop}, \nline: {line}"
        func = sop[0].strip()
        if func == "0":
            g.create_const0(fanout)
        elif func == "1":
            g.create_const1(fanout)
        return

    # regular nodes
    g.create_node(fanout, line.split()[1:-1], sop[:])


def on_subckt(g: BLIFGraph, line: str):

    module: str = line.split()[1].strip()

    try:
        _g: BLIFGraph = g.submodules[module]
    except:
        _g = None
    for d in line.split()[2:]:
        p: str = d.split("=")[0].strip()
        s: str = d.split("=")[1].strip()
        if _g is None or p in _g.pos():
            # if s not in g.pis():
            if s not in g.get_nodes() and s not in g.pis():
                g.create_pi(s)
        if _g is None or p in _g.pis():
            if s not in g.pis() and s not in g.pos():
                g.create_po(s)


def read_blif_impl(graph: BLIFGraph, filename: str) -> None:
    """Read BLIF file and construct a BLIF graph

    Args:
        graph (BLIFGraph): the graph to be constructed
        filename (str): the BLIF file name

    Raises:
        FileNotFoundError: if the file is not found
    """

    if os.path.exists(filename) == False:
        raise FileNotFoundError(f"File {filename} not found")

    modules: Dict[str, List[str]] = {}
    module: str = ""
    with open(filename, "r") as f:
        for line in f:
            while line.strip().endswith("\\"):
                line = line.strip()[:-1] + next(f)

            if line.startswith("#"):
                # we skip comments
                continue

            if line.strip() == "":
                # we skip empty lines
                continue

            if line.startswith(".model"):
                module = line.split()[1].strip()
                modules[module] = []

                if graph.top_module == "":
                    graph.top_module = module
                continue

            modules[module].append(line)

    # sub modules
    for module in modules:
        if module == graph.top_module:
            continue
        _g: BLIFGraph = BLIFGraph()
        for line in modules[module]:
            if line.startswith(".input"):
                on_input(_g, line)
            if line.startswith(".output"):
                on_output(_g, line)
        graph.submodules[module] = _g

    index: int = 0
    while True:
        assert index < len(modules[graph.top_module]) and "index out of range"
        line = modules[graph.top_module][index]
        if line.startswith(".end"):
            break
        elif line.startswith(".input"):
            on_input(graph, line)
            index += 1
        elif line.startswith(".output"):
            on_output(graph, line)
            index += 1
        elif line.startswith(".latch"):
            on_latch(graph, line)
            index += 1
        elif line.startswith(".names"):
            # also add the logic
            sop: list = []
            while True:
                index += 1
                _nextline: str = modules[graph.top_module][index].strip()
                if len(_nextline) == 0:
                    break
                if _nextline.startswith("."):
                    index -= 1  # we already reached the next useful line
                    break
                sop.append(_nextline)
            on_gate(graph, line, sop)
            index += 1
        elif line.startswith(".subckt"):
            on_subckt(graph, line)
            index += 1
        else:
            # here there are several possible situations:
            #   - comment: not possible because it is filtered out
            #   - empty line: skip
            index += 1
            continue

    graph.traverse()
