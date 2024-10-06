import gurobipy as gp
from typing import List, Dict

from ..blif import *
from ..cute import *
from ..map import *
from .timingModel import TimingModel


class MapBufModel(TimingModel):
    def __init__(
        self,
        blifGraph: BLIFGraph,
        schedConstraints: dict,
        clockPeriod: float,
        params: dict = {},
    ) -> None:
        super().__init__(clockPeriod)

        self.lutDelay = params.get("lutDelay", 0.7)
        self.wireDelay = params.get("wireDelay", 0)
        self.inputDelay = params.get("inputDelay", 0)
        self.maxLeaves = params.get("maxLeaves", 6)
        self.loadSubjectGraph(blifGraph)
        self.loadScheduabilityConstraints(schedConstraints)

    def loadScheduabilityConstraints(self, schedConstraints: dict):
        assert "dip" in schedConstraints, "dip is not provided"
        assert "cip" in schedConstraints, "cip is not provided"
        self.ext2idx: Dict[str, int] = {}
        for signal, label in schedConstraints["dip"].items():
            assert signal in self.signals, f"{signal} is not in the graph"
            idx = self.signal2idx[signal]

            if label not in self.ext2idx:
                self.ext2idx[label] = len(self.ext2idx)
                var = self.model.addVar(
                    vtype=gp.GRB.INTEGER, name=f"ext_l_{self.ext2idx[label]}", lb=0
                )
                self.model.update()

            # Data integrity constraints
            # we make sure signal with the same label have the same l variable
            self.model.addConstr(self.model.getVarByName(f"l_{idx}") == var)

        for lhs, rhs, delta in schedConstraints["cip"]:
            assert lhs in self.ext2idx, f"{lhs} is not in the external labels"
            assert rhs in self.ext2idx, f"{rhs} is not in the external labels"
            lhs_idx = self.ext2idx[lhs]
            rhs_idx = self.ext2idx[rhs]

            # Control integrity constraints
            # we make sure the difference between two signals is larger than delta
            self.model.addConstr(
                self.model.getVarByName(f"ext_l_{lhs_idx}")
                - self.model.getVarByName(f"ext_l_{rhs_idx}")
                >= delta
            )

    def loadSubjectGraph(self, graph: BLIFGraph):
        self.graph = graph

        # assign index to signals
        self._assignSignalIndex(graph)
        self._assignCutIndex(graph)
        self.model.update()

        # creating constraints
        for signal in self.signals:
            self._addTimingConstraintsAt(signal)
            self._addCutSelectionConstraintsAt(signal)

        # clock period constraint
        self.model.addConstr(self.tVar <= self.clockPeriod)

        self._addObjective()

    def _createTimingLabel(self, idx: str):
        self.model.addVar(vtype=gp.GRB.INTEGER, name=f"l_{idx}", lb=0)
        self.model.addVar(vtype=gp.GRB.CONTINUOUS, name=f"t_{idx}", lb=0)

    def _addTimingConstraintsAt(self, signal: str):
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
        cp = self.clockPeriod + dLUT  # sufficient slack

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
                self.model.addConstr(
                    tOut + cp * lOut + cp >= tIn + cp * lIn + cp * cutVar + dLUT
                )

    def _addCutSelectionConstraintsAt(self, signal: str):
        idx = self.signal2idx[signal]
        cuts = self.signal2cuts[signal]
        self.model.addConstr(
            gp.quicksum(
                self.model.getVarByName(f"c_{idx}_{i}") for i in range(len(cuts))
            )
            == 1
        )

    def _addObjective(self):
        # ASAP scheduling
        self.model.setObjective(
            gp.quicksum(
                self.model.getVarByName(f"l_{idx}") for idx in range(len(self.signals))
            ),
            gp.GRB.MINIMIZE,
        )

        # Latency minimization
        # self.model.setObjective(self.__latency_variable, gp.GRB.MINIMIZE)

    def _assignSignalIndex(self, graph: BLIFGraph):
        self.signals = []
        self.signal2idx = {}
        for idx, signal in enumerate(graph.topological_traversal()):
            self.signals.append(signal)
            self.signal2idx[signal] = idx
            self._createTimingLabel(idx)

    def _assignCutIndex(self, graph: BLIFGraph):
        # TODO: handle the parameter of the cut enumeration
        self.signal2cuts: dict = cutlessEnum(graph, {"maxLeaves": self.maxLeaves})
        for signal, cuts in self.signal2cuts.items():
            idx = self.signal2idx[signal]
            assert len(cuts) > 0
            for i, _ in enumerate(cuts):
                self.model.addVar(vtype=gp.GRB.BINARY, name=f"c_{idx}_{i}")

    def _insertBuffers(self):
        for signal in self.signals:
            if self.graph.is_ci(signal):
                continue
            label = self.solution[signal]
            new_fanins = []
            for fanin in self.graph.fanins(signal):
                if self.solution[fanin] < label:
                    ri = fanin
                    # name the register usign the stage (scheduling variable)
                    for i in range(self.solution[fanin], label):
                        ro = f"{fanin}_stage_{i+1}"
                        if ro not in self.graph.register_outputs:
                            self.graph.create_latch(ri, ro)
                        ri = ro
                    new_fanins.append(ri)
                else:
                    new_fanins.append(fanin)
            self.graph.set_fanins(signal, new_fanins)

        # update the graph
        self.graph.traverse()

    def getSubjectGraph(self):
        return self.graph

    def dumpGraph(self, fileName: str):
        signal2cut = self.dumpCuts()
        self.graph = techmap(self.graph, signal2cut)
        self.signals = self.graph.topological_traversal()
        self._insertBuffers()
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
                self.solution[f"c_{idx}_{i}"] = self.model.getVarByName(
                    f"c_{idx}_{i}"
                ).X
