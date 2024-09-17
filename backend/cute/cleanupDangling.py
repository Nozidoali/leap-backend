#!/usr/bin/env python
# -*- encoding=utf8 -*-

"""
Author: Hanyu Wang
Created time: 2024-06-24 18:02:11
Last Modified by: Hanyu Wang
Last Modified time: 2024-06-24 18:05:00
"""


def cleanupDanglingCuts(old_cuts: dict) -> dict:
    new_cuts: dict = {}
    for signal in old_cuts:
        if len(old_cuts[signal]) == 0:
            continue
        if len(old_cuts[signal]) == 1 and old_cuts[signal][0] == signal:
            continue
        new_cuts[signal] = old_cuts[signal][:]
    return new_cuts
