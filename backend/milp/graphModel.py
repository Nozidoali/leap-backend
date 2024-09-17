from ..blif import *
from .timingModel import TimingModel

import gurobipy as gp

class GraphModel(TimingModel):
    def __init__(self, blifGraph: BLIFGraph, dfg: dict, clockPeriod: float, params: dict = {}) -> None:
        super().__init__(clockPeriod)
        
        self.lutDelay = params.get("lutDelay", 0.7)
        self.wireDelay = params.get("wireDelay", 0)
        self.inputDelay = params.get("inputDelay", 0)
        self.loadDataflowGraph(dfg)
        self.loadSubjectGraph(blifGraph)
        
    def loadDataflowGraph(self, dfg):
        self.dfg = dfg
    
    def loadSubjectGraph(self, graph: BLIFGraph):
        self.graph = graph
        # creating variables
        self.signals = []
        self.signal2idx = {}
        for idx, signal in enumerate(graph.topological_traversal()):
            self.signals.append(signal)
            self.signal2idx[signal] = idx
            self.createTimingLabel(idx)
        # global variables
        self.__depth_variable = self.model.addVar(
            vtype=gp.GRB.CONTINUOUS, name="cp", lb=0
        )
        self.__latency_variable = self.model.addVar(
            vtype=gp.GRB.CONTINUOUS, name="latency", lb=0
        )
        self.model.update()

        # creating constraints
        for idx, signal in enumerate(self.signals):
            self.addTimingConstraintsAt(signal)
            self.model.addConstr(
                self.model.getVarByName(f"t_{idx}") <= self.__depth_variable
            )
            self.model.addConstr(
                self.model.getVarByName(f"l_{idx}") <= self.__latency_variable
            )
            
        # PO must have the same l variables
        for po in graph.pos():
            self.model.addConstr(self.model.getVarByName(f"l_{self.signal2idx[po]}") == self.__latency_variable)

        # clock period constraint
        self.model.addConstr(self.__depth_variable <= self.clockPeriod)

    def createTimingLabel(self, idx: str):
        self.model.addVar(vtype=gp.GRB.INTEGER, name=f"l_{idx}", lb=0)
        self.model.addVar(vtype=gp.GRB.CONTINUOUS, name=f"t_{idx}", lb=0)

    def addTimingConstraintsAt(self, signal: str):
        if self.graph.is_pi(signal):
            tIn = self.model.getVarByName(f"t_{self.signal2idx[signal]}")
            dIn = self.inputDelay
            
            self.model.addConstr(tIn >= dIn)  # usually the PIs need a long wire delay

        if self.graph.is_ci(signal):
            return

        idx = self.signal2idx[signal]
        for fanin in self.graph.node_fanins[signal]:
            assert fanin in self.signal2idx
            fanin_idx = self.signal2idx[fanin]

            tOut = self.model.getVarByName(f"t_{idx}")
            tIn = self.model.getVarByName(f"t_{fanin_idx}")
            lOut = self.model.getVarByName(f"l_{idx}")
            lIn = self.model.getVarByName(f"l_{fanin_idx}")
            cp = self.clockPeriod
            dLUT = self.lutDelay

            self.model.addConstr(tOut + cp * lOut >= tIn + cp * lIn + dLUT)

    def addObjective(self):
        # ASAP scheduling
        self.model.setObjective(gp.quicksum(self.model.getVarByName(f"l_{idx}") for idx in range(len(self.signals))), gp.GRB.MINIMIZE)
        
        # Latency minimization
        # self.model.setObjective(self.__latency_variable, gp.GRB.MINIMIZE)

    def solve(self):
        super().solve()
        self.solution = {
            signal: self.model.getVarByName(f"l_{idx}").X
            for idx, signal in enumerate(self.signals)
        }
        
        self.depth = self.__depth_variable.X
        self.latency = self.__latency_variable.X
    
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

    def getSubjectGraph(self):
        return self.graph

    def dumpGraph(self, fileName: str):
        self.insertBuffers()
        write_blif(self.graph, fileName)