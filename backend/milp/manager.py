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

class LPManager:
    def __init__(self) -> None:
        with gp.Env(empty=True) as env:
            env.setParam("OutputFlag", 0)
            env.start()
            self.__model = gp.Model(env=env)

        self.__clock_period = None
        self.__instructions = []

    def setClockPeriod(self, clock_period: float):
        self.__clock_period = clock_period

    def loadModel(self, fileName: str):
        self.__model = gp.read(fileName)

    def loadInstructions(self, fileName: str):
        with open(fileName, "r") as f:
            for line in f:
                self.__instructions.append(line.strip())

    def linkVariables(self, variables: dict):
        self.__variables = variables

    def linkSubjectGraph(self, graph: BLIFGraph):
        self.graph = graph

        # creating variables
        self.signals = []
        self.signal2idx = {}
        for idx, signal in enumerate(graph.topological_traversal()):
            self.signals.append(signal)
            self.signal2idx[signal] = idx
            self.createTlabel(idx)
        # global variables
        self.__depth_variable = self.__model.addVar(
            vtype=gp.GRB.CONTINUOUS, name="cp", lb=0
        )
        self.__latency_variable = self.__model.addVar(
            vtype=gp.GRB.CONTINUOUS, name="latency", lb=0
        )

        self.__model.update()

        # creating constraints
        for idx, signal in enumerate(self.signals):
            self.addConstraints(signal)
            self.__model.addConstr(
                self.__model.getVarByName(f"t_{idx}") <= self.__depth_variable
            )
            self.__model.addConstr(
                self.__model.getVarByName(f"l_{idx}") <= self.__latency_variable
            )
            
        # PO must have the same l variables
        for po in graph.pos():
            self.__model.addConstr(self.__model.getVarByName(f"l_{self.signal2idx[po]}") == self.__latency_variable)

        # clock period constraint
        self.__model.addConstr(self.__depth_variable <= self.__clock_period)

    def dumpModel(self, fileName: str):
        self.__model.write(filename=fileName)

    def createTlabel(self, idx: str):
        self.__model.addVar(vtype=gp.GRB.INTEGER, name=f"l_{idx}", lb=0)
        self.__model.addVar(vtype=gp.GRB.CONTINUOUS, name=f"t_{idx}", lb=0)

    def addConstraints(self, signal: str):
        if self.graph.is_pi(signal):
            t = self.__model.getVarByName(f"t_{self.signal2idx[signal]}")
            # self.__model.addConstr(t >= 1.8)  # usually the PIs need a long wire delay

        if self.graph.is_ci(signal):
            return

        idx = self.signal2idx[signal]
        for fanin in self.graph.node_fanins[signal]:
            assert fanin in self.signal2idx
            fanin_idx = self.signal2idx[fanin]

            tOut = self.__model.getVarByName(f"t_{idx}")
            tIn = self.__model.getVarByName(f"t_{fanin_idx}")
            lOut = self.__model.getVarByName(f"l_{idx}")
            lIn = self.__model.getVarByName(f"l_{fanin_idx}")
            cp = self.__clock_period

            self.__model.addConstr(tOut + cp * lOut >= tIn + cp * lIn + 0.7)

    def addObjective(self):
        # ASAP scheduling
        self.__model.setObjective(self.__latency_variable, gp.GRB.MINIMIZE)

    def solve(self):
        self.__model.optimize()
        if self.__model.status == gp.GRB.INFEASIBLE:
            assert False, "Model is infeasible"
        assert self.__model.status == gp.GRB.OPTIMAL, "Model is not optimal"

        # get the solution
        self.solution = {}
        for idx in range(len(self.signals)):
            signal = self.signals[idx]
            self.solution[signal] = self.__model.getVarByName(f"l_{idx}").X

        # get the depth
        self.depth = self.__depth_variable.X
        
        # get the latency
        self.latency = self.__latency_variable.X
        
        
    def getL(self, signal: str):
        return self.solution[signal]
    
    def getDepth(self):
        return self.depth
    
    def getLatency(self):
        return self.latency

    def insertBuffers(self):
        for signal in self.signals:
            if self.graph.is_ci(signal):
                continue

            label = self.solution[signal]
            new_fanins = []
            for fanin in self.graph.node_fanins[signal]:
                if self.solution[fanin] < label:
                    ri = fanin
                    # self.graph.insert_buffer(fanin, signal)
                    numCycles = int(label - self.solution[fanin])
                    for i in range(numCycles):
                        ro = f"{fanin}_buffer_{i+1}"

                        if ro not in self.graph.register_outputs:
                            self.graph.create_latch(ri, ro)

                        ri = ro

                    new_fanins.append(ri)
                else:
                    new_fanins.append(fanin)
            self.graph.node_fanins[signal] = set(new_fanins)

        # update the graph
        self.graph.traverse()

    def dumpGraph(self, fileName: str):
        write_blif(self.graph, fileName)


    def getSubjectGraph(self):
        return self.graph