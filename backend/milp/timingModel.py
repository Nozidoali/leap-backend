#!/usr/bin/env python
# -*- encoding=utf8 -*-

"""
Author: Hanyu Wang
Created time: 2024-07-11 16:48:46
Last Modified by: Hanyu Wang
Last Modified time: 2024-07-11 22:48:30
"""

from ..blif import *
from .basicModel import BasicModel

import gurobipy as gp


class TimingModel(BasicModel):
    """
    This is the base class of all the timing models
    The model itself does not have any constraints
    """

    def __init__(self, clockPeriod: float) -> None:
        super().__init__(clockPeriod)
        self._createGlobalVariables()

    def _createGlobalVariables(self):
        # global variables
        self.tVar = self.model.addVar(vtype=gp.GRB.CONTINUOUS, name="cp", lb=0)
        self.lVar = self.model.addVar(vtype=gp.GRB.INTEGER, name="latency", lb=0)

    def solve(self):
        super().solve()
        if not self.isInfeasible():
            self._extractSolution()

    def _extractSolution(self):
        self.solution = {
            signal: int(self.model.getVarByName(f"l_{idx}").X)
            for idx, signal in enumerate(self.signals)
        }
        self.depth = self.tVar.X
        self.latency = self.lVar.X

    def getDepth(self):
        return self.depth

    def getLatency(self):
        return self.latency
