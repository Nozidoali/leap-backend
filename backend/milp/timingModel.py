#!/usr/bin/env python
# -*- encoding=utf8 -*-

"""
Author: Hanyu Wang
Created time: 2024-07-11 16:48:46
Last Modified by: Hanyu Wang
Last Modified time: 2024-07-11 22:48:30
"""

from ..blif import *

import gurobipy as gp

class TimingModelBase:
    def __init__(self, clockPeriod: float) -> None:
        with gp.Env(empty=True) as env:
            env.setParam("OutputFlag", 0)
            env.start()
            self.model = gp.Model(env=env)

        self.clockPeriod = clockPeriod
        self.__instructions = []

    def loadModel(self, fileName: str):
        self.model = gp.read(fileName)

    def dumpModel(self, fileName: str):
        self.model.write(filename=fileName)

    def loadInstructions(self, fileName: str):
        with open(fileName, "r") as f:
            for line in f:
                self.__instructions.append(line.strip())

    def solve(self):
        self.model.optimize()
        if self.model.status == gp.GRB.INFEASIBLE:
            assert False, "Model is infeasible"
        assert self.model.status == gp.GRB.OPTIMAL, "Model is not optimal"

    def getDepth(self):
        raise NotImplementedError
    
    def getLatency(self):
        raise NotImplementedError

class TimingModel(TimingModelBase):
    def __init__(self, clockPeriod: float) -> None:
        super().__init__(clockPeriod)
