from ..blif import *
from ..cute import *
from ..map import *
from .timingModel import TimingModel

import gurobipy as gp

class MapBufModel(TimingModel):
    def __init__(self, blifGraph: BLIFGraph, dfg: dict, clockPeriod: float, params: dict = {}) -> None:
        super().__init__(clockPeriod)
        
        self.lutDelay = params.get("lutDelay", 0.7)
        self.wireDelay = params.get("wireDelay", 0)
        self.inputDelay = params.get("inputDelay", 0)
        self.maxLeaves = params.get("maxLeaves", 6)
        self.loadDataflowGraph(dfg)
        self.loadSubjectGraph(blifGraph)
        
    def loadDataflowGraph(self, dfg):
        self.dfg = dfg
    
    def loadSubjectGraph(self, graph: BLIFGraph):
        self.graph = graph
        
        # assign index to signals
        self._assignSignalIndex(graph)
        self._assignCutIndex(graph)
        self.model.update()

        # creating constraints
        for signal in self.signals:
            self.addTimingConstraintsAt(signal)
            self.addCutSelectionConstraintsAt(signal)

        # PO must have the same l variables
        # TODO: this is conservative, we can relax this constraint
        for po in graph.pos():
            self.model.addConstr(self.model.getVarByName(f"l_{self.signal2idx[po]}") == self.lVar)

        # clock period constraint
        self.model.addConstr(self.tVar <= self.clockPeriod)

    def createTimingLabel(self, idx: str):
        self.model.addVar(vtype=gp.GRB.INTEGER, name=f"l_{idx}", lb=0)
        self.model.addVar(vtype=gp.GRB.CONTINUOUS, name=f"t_{idx}", lb=0)

    def addTimingConstraintsAt(self, signal: str):
        if self.graph.is_pi(signal):
            tIn = self.model.getVarByName(f"t_{self.signal2idx[signal]}")
            dIn = self.inputDelay
            
            # usually the PIs need a long wire delay
            self.model.addConstr(tIn >= dIn)  

        if self.graph.is_ci(signal):
            # register's output are fine
            return

        idx = self.signal2idx[signal]

        tOut = self.model.getVarByName(f"t_{idx}")
        lOut = self.model.getVarByName(f"l_{idx}")
        dLUT = self.lutDelay
        cp = self.clockPeriod + dLUT # sufficient slack
        
        self.model.addConstr(tOut <= self.tVar)
        self.model.addConstr(lOut <= self.lVar)
        
        cuts = self.signal2cuts[signal]
        for i, cut in enumerate(cuts):
            cutVar = self.model.getVarByName(f"c_{idx}_{i}")
            
            for fanin in cut:
                assert fanin in self.signal2idx
                fanin_idx = self.signal2idx[fanin]

                tIn = self.model.getVarByName(f"t_{fanin_idx}")
                lIn = self.model.getVarByName(f"l_{fanin_idx}")

                # NOTE: delay propagation constraints
                # tOut + cp * ( (lOut - lIn) or (1 - cutVar) ) >= tIn + dLUT
                self.model.addConstr(tOut + cp * lOut + cp >= tIn + cp * lIn + cp * cutVar + dLUT)

    def addCutSelectionConstraintsAt(self, signal: str):
        idx = self.signal2idx[signal]
        cuts = self.signal2cuts[signal]
        self.model.addConstr(gp.quicksum(self.model.getVarByName(f"c_{idx}_{i}") for i in range(len(cuts))) == 1)

    def addObjective(self):
        # ASAP scheduling
        self.model.setObjective(gp.quicksum(self.model.getVarByName(f"l_{idx}") for idx in range(len(self.signals))), gp.GRB.MINIMIZE)
        
        # Latency minimization
        # self.model.setObjective(self.__latency_variable, gp.GRB.MINIMIZE)
        
    def _assignSignalIndex(self, graph: BLIFGraph):
        self.signals = []
        self.signal2idx = {}
        for idx, signal in enumerate(graph.topological_traversal()):
            self.signals.append(signal)
            self.signal2idx[signal] = idx
            self.createTimingLabel(idx)

    def _assignCutIndex(self, graph: BLIFGraph):
        # TODO: handle the parameter of the cut enumeration
        self.signal2cuts: dict = cutlessEnum(graph, {"maxLeaves": self.maxLeaves})
        for signal, cuts in self.signal2cuts.items():
            idx = self.signal2idx[signal]
            assert len(cuts) > 0
            for i, _ in enumerate(cuts):
                self.model.addVar(vtype=gp.GRB.BINARY, name=f"c_{idx}_{i}")

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
        signal2cut = self.dumpCuts()
        self.graph = techmap(self.graph, signal2cut)
        self.signals = self.graph.topological_traversal()
        self.insertBuffers()
        write_blif(self.graph, fileName)
    
    def dumpCuts(self):
        signal2cut = {}
        
        # check the solution, and assign the cuts
        for signal, cuts in self.signal2cuts.items():
            if self.graph.is_ci(signal):
                continue
            idx = self.signal2idx[signal]
            for i, cut in enumerate(cuts):
                if self.solution[f"c_{idx}_{i}"] > 0.5:
                    signal2cut[signal] = cut
                    break
    
        return signal2cut
    
    def solve(self):
        super().solve()
        
        # we need to store the cut selection
        for signal, cuts in self.signal2cuts.items():
            if self.graph.is_ci(signal):
                continue
            idx = self.signal2idx[signal]
            for i, _ in enumerate(cuts):
                self.solution[f"c_{idx}_{i}"] = self.model.getVarByName(f"c_{idx}_{i}").X