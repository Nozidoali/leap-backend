#!/usr/bin/env python
# -*- encoding=utf8 -*-

"""
Author: Hanyu Wang
Created time: 2024-05-22 14:47:44
Last Modified by: Hanyu Wang
Last Modified time: 2024-05-22 14:55:36
"""
from typing import List, Dict


class BLIFGraphBase:
    def __init__(self):
        self.top_module = ""
        self.inputs: List[str] = []
        self.outputs: List[str] = []
        self.nodes: List[str] = []
        self.register_inputs: List[str] = []
        self.register_outputs: List[str] = []
        self.ro_to_ri: Dict[str, str] = {}

        self.ro_types: Dict[str, str] = {}

        # __signals is a list of all the nodes in the network in the topological order
        # this is private and should not be modified directly
        self.__signals: List[str] = []

        self.const0: List[str] = []
        self.const1: List[str] = []

        # node fanins return the set of fanins of a node
        #  - note that only nodes can be looked up in this dictionary
        #  - __signals are not safe when directly looked up
        self.__node_fanins: Dict[str, List[str]] = {}

        # node_funcs return the function of a node
        #  - each func is a list of strings
        #  - each string is a minterm and the last character is the output
        self.node_funcs: Dict[str, List[str]] = {}

        self.node_fanouts: Dict[str, List[str]] = {}

        self.submodules = {}

    def is_po(self, signal: str) -> bool:
        return signal in self.outputs

    def is_pi(self, signal: str) -> bool:
        return signal in self.inputs

    def is_ro(self, signal: str) -> bool:
        return signal in self.register_outputs

    def is_ri(self, signal: str) -> bool:
        return signal in self.register_inputs

    def is_const0(self, signal: str) -> bool:
        return signal in self.const0

    def is_const1(self, signal: str) -> bool:
        return signal in self.const1

    def num_nodes(self) -> int:
        return len(self.nodes)

    def num_latch(self) -> int:
        return len(self.register_outputs)

    def num_pis(self) -> int:
        return len(self.inputs)

    def num_pos(self) -> int:
        return len(self.outputs)

    # the CO (combinational outputs are the primary outputs and the register inupts)
    def is_co(self, signal: str) -> bool:
        return signal in self.outputs or signal in self.register_inputs

    # the CI (combinational inptus are the primary inputs and the register outputs)
    def is_ci(self, signal: str) -> bool:
        return (
            signal in self.inputs
            or signal in self.register_outputs
            or signal in self.const0
            or signal in self.const1
        )

    def topological_traversal(self) -> list:
        return self.__signals

    def constants(self):
        return self.const0 + self.const1

    def cos(self):
        return self.outputs + self.register_inputs

    def cis(self):
        return self.inputs + self.register_outputs + self.const0 + self.const1

    def constant0s(self):
        return self.const0

    def constant1s(self):
        return self.const1

    def pis(self):
        return self.inputs

    def pos(self):
        return self.outputs

    def ris(self):
        return self.register_inputs

    def ros(self):
        return self.register_outputs

    def fanins(self, signal: str) -> List[str]:
        return self.__node_fanins[signal][:]

    def has_fanin(self, signal: str) -> bool:
        return signal in self.__node_fanins

    def set_fanins(self, signal: str, fanins: List[str]):
        self.__node_fanins[signal] = fanins

    def get_nodes(self) -> List[str]:
        return self.nodes

    def get_signals(self) -> List[str]:
        return self.__signals

    # sort __signals in a topological order
    # TODO: support runtime modification and maintain the topogical order
    def traverse(self):
        self.__signals = []
        for signal in self.cis():
            assert signal not in self.__signals
            self.__signals.append(signal)

        visited_signals = set()
        for signal in self.cos():
            self.trav_rec(signal, set(), visited_signals)

        for signal in self.__signals:
            self.node_fanouts[signal] = []

        # prepare fanouts: this should be recomputed after each network modification
        for signal in self.__signals:
            if signal in self.__node_fanins:
                for f in self.fanins(signal):
                    self.node_fanouts[f].append(signal)

    # topological traversal, used to sort the __signals in a topological order
    def trav_rec(
        self, signal: str, pending_signals: set = set(), visited_signals: set = set()
    ):
        if signal in self.__signals:
            return

        if signal in visited_signals:
            return

        # print(f"number of visited signals: {len(visited_signals)}", end="\r")
        visited_signals.add(signal)

        if signal not in self.__node_fanins:
            raise ValueError(f"node {signal} not in __node_fanins")

        pending_signals.add(signal)

        for f in self.fanins(signal):
            assert f != signal, f"node {signal} is its own fanin"
            if f not in self.__signals:
                if f in pending_signals:
                    # we have a loop
                    # print(f"recursion stoped at node {signal}")
                    # print(f"pending signals: {pending_signals}")
                    return
                self.trav_rec(f, pending_signals, visited_signals)

        pending_signals.remove(signal)
        self.__signals.append(signal)

    def num_fanouts(self, signal: str):
        return len(self.node_fanouts[signal])

    #
    # graph modifications
    #
    def create_pi(self, name: str):
        assert name not in self.inputs, f"the input {name} already exists"
        self.inputs.append(name)

    def create_po(self, name: str):
        assert name not in self.outputs, f"the output {name} already exists"
        self.outputs.append(name)

    def create_ri(self, name: str):
        assert (
            name not in self.register_inputs
            and "the register input to create already exists"
        )
        self.register_inputs.append(name)

    def create_ro(self, name: str):
        assert (
            name not in self.register_outputs
            and "the register output to create already exists"
        )
        self.register_outputs.append(name)

    def create_const0(self, name: str):
        assert name not in self.const0 and "the constant 0 to create already exists"
        self.const0.append(name)

    def create_const1(self, name: str):
        assert name not in self.const1 and "the constant 1 to create already exists"
        self.const1.append(name)

    def create_node(self, name: str, fanins: List[str], func: List[str]):
        assert name not in self.nodes and "the node to create already exists"
        self.nodes.append(name)
        self.__node_fanins[name] = fanins[:]  # deep copy
        self.node_funcs[name] = func[:]  # deep copy
        self.node_fanouts[name] = []

    def create_and(self, f1: str, f2: str, name: str):
        self.create_node(name=name, fanins=[f1, f2], func=["11 1"])

    def create_or(self, f1: str, f2: str, name: str):
        self.create_node(name=name, fanins=[f1, f2], func=["1- 1", "-1 1"])
        
    def create_not(self, f1: str, name: str):
        self.create_node(name=name, fanins=[f1], func=["0 1"])

    def create_buf(self, fin: str, fout: str):
        self.create_node(name=fout, fanins=[fin], func=["1 1"])

    def create_latch(self, ri: str, ro: str, type: int = 0):
        self.register_inputs.append(ri)
        self.register_outputs.append(ro)
        self.ro_to_ri[ro] = ri
        self.ro_types[ro] = type

    def substitute_fanin(self, signal: str, old_fanin: str, new_fanin: str):
        self.__node_fanins[signal] = [
            new_fanin if x == old_fanin else x for x in self.__node_fanins[signal]
        ]

    def __repr__(self) -> str:
        return f"BLIFGraphBase({self.top_module})"

    def copy(self):
        new_graph = BLIFGraphBase()
        new_graph.top_module = self.top_module
        new_graph.inputs = self.inputs.copy()
        new_graph.outputs = self.outputs.copy()
        new_graph.nodes = self.nodes.copy()
        new_graph.register_inputs = self.register_inputs.copy()
        new_graph.register_outputs = self.register_outputs.copy()
        new_graph.ro_to_ri = self.ro_to_ri.copy()
        new_graph.ro_types = self.ro_types.copy()
        new_graph.__signals = self.__signals.copy()
        new_graph.const0 = self.const0.copy()
        new_graph.const1 = self.const1.copy()
        new_graph.__node_fanins = self.__node_fanins.copy()
        new_graph.node_funcs = self.node_funcs.copy()
        new_graph.node_fanouts = self.node_fanouts.copy()
        new_graph.submodules = self.submodules.copy()
        new_graph.traverse()
        return new_graph

    def funcOf(self, signal: str):
        return self.node_funcs[signal]
