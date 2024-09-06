#!/usr/bin/env python
# -*- encoding=utf8 -*-

"""
Author: Hanyu Wang
Created time: 2024-06-24 18:26:26
Last Modified by: Hanyu Wang
Last Modified time: 2024-06-24 18:34:42
"""

from ..common import *


def printCutsStats(signal_to_cuts: dict):
    total_cut_count = 0
    cut_count_by_size = {}
    max_cut_count: int = 0

    for signal in signal_to_cuts:
        total_cut_count += len(signal_to_cuts[signal])

        if len(signal_to_cuts[signal]) > max_cut_count:
            max_cut_count = len(signal_to_cuts[signal])

        for cut in signal_to_cuts[signal]:
            cut_size = cut.size()
            if cut_size not in cut_count_by_size:
                cut_count_by_size[cut_size] = 0
            cut_count_by_size[cut_size] += 1

    print(f"Total cut count = {text_orange(total_cut_count)}")
    print(f"Max cut count = {text_orange(max_cut_count)}")
    for cut_size in cut_count_by_size:
        print(f"Cut size {cut_size} count = {cut_count_by_size[cut_size]}")

    stats = {}
    stats["total_cut_count"] = total_cut_count
    stats["max_cut_count"] = max_cut_count
    for cut_size in cut_count_by_size:
        stats[f"cut_size_{cut_size}_count"] = cut_count_by_size[cut_size]

    return stats


def writeCuts(signal_to_cuts: dict, filename: str) -> None:
    with open(filename, "w") as f:
        for signal in signal_to_cuts:
            cuts = signal_to_cuts[signal]
            num_cuts = len(cuts)
            f.write(f"{signal} {num_cuts}\n")

            cut: list
            for index, cut in enumerate(cuts):
                f.write(f"Cut #{index}: {len(cuts)}\n")
                for leaf in cut:
                    f.write(f"\t{leaf}\n")


def readCuts(filename: str) -> dict:
    with open(filename, "r") as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]

        signal_to_cuts = {}

        index = 0
        while index < len(lines):
            line = lines[index]
            index += 1
            signal, num_cuts = line.split()
            num_cuts = int(num_cuts)

            cuts = []
            for i in range(num_cuts):
                line = lines[index]
                index += 1

                assert line.startswith(f"Cut #{i}:")
                num_leaves = int(line.split()[-1])

                # parse leaves
                leaves = []
                for j in range(num_leaves):
                    line = lines[index]
                    index += 1
                    leaves.append(line)

                cuts.append(list(leaves)[:])

            signal_to_cuts[signal] = cuts

        return signal_to_cuts
