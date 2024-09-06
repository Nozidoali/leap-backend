#!/usr/bin/env python
# -*- encoding=utf8 -*-

"""
Author: Hanyu Wang, Carmine Rizzi
Created time: 2024-05-22 14:51:11
Last Modified by: Hanyu Wang
Last Modified time: 2024-05-31 08:04:13
"""

from .network.blif import *
from .blifReader import *
from .blifWriter import *


def rewriteBlif(inputFile: str, outputFile: str):
    """
    Carmine's code (31.05.2024)
    """
    import re

    with open(inputFile, "r") as f:
        lines = f.readlines()

    with open(outputFile, "w") as f:
        for line in lines:
            if "DFF" in line:
                if "DFFSR" in line:
                    module_name = "DFFSR"
                    continuation = " R=(.+) S=(.+)"
                else:
                    module_name = "DFF"
                    continuation = ""

                reg_pattern = "\.subckt {0} C=(.+) D=(.+) Q=(.+){1}".format(
                    module_name, continuation
                )
                matches = re.findall(reg_pattern, line)
                clock = matches[0][0]
                input = matches[0][1]
                output = matches[0][2]
                line = ".latch {0} {1} re {2} 3\n".format(input, output, clock)
            f.write(line)
    # graph = read_blif(inputFile)
    # write_blif(graph, outputFile)


def rewriteBlifLatch(inputFile: str, outputFile: str):
    import re

    graph = read_blif(inputFile)
    # we need to add clk if it is not present
    if "clk" not in graph.inputs:
        graph.inputs.add("clk")
    write_blif(graph, outputFile)

    with open(outputFile, "r") as f:
        lines = f.readlines()

    with open(outputFile, "w") as f:
        for line in lines:
            if "latch" in line:
                # for example: .latch      n1132 cur_state[0]  2
                reg_pattern = "\.latch\s+(.+)\s+(.+)\s+(.+)"
                matches = re.findall(reg_pattern, line)
                input = matches[0][0]
                output = matches[0][1]
                type = matches[0][2]
                if type != "3":
                    clock = "clk"
                    line = ".latch {0} {1} re {2} 3\n".format(input, output, clock)

            f.write(line)
