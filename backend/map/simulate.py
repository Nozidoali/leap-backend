from dataclasses import dataclass, field
from typing import List

from .dt import *
from .tt import *
from ..blif import *


@dataclass
class BasicFunc:
    n_inputs: int
    terms: List[str] = field(default_factory=list)
    value: int = None

    @property
    def sop(self):
        return [f"{x} {self.value}" for x in self.terms]

    @property
    def tt(self):
        return ttStr(getTT(sopToTree(self.terms, self.value, self.n_inputs)))


@dataclass
class Constant0(BasicFunc):
    def __post_init__(self):
        self.terms = ["-" * self.n_inputs]
        self.value = 0


@dataclass
class Constant1(BasicFunc):
    def __post_init__(self):
        self.terms = ["-" * self.n_inputs]
        self.value = 1


@dataclass
class Wire(BasicFunc):
    index: int = None

    def __post_init__(self):
        self.terms = [f"{'-' * self.index}1{'-' * (self.n_inputs - self.index - 1)}"]
        self.value = 1


@dataclass
class LUTFunc(BasicFunc):
    terms: List[str]
    value: int

    def __post_init__(self):
        self.terms = self.terms[:]


def readFunc(sop: List[str]) -> BasicFunc:
    n_inputs = len(sop[0].split()[0])
    func = BasicFunc(n_inputs)
    func.terms = [x.split()[0] for x in sop]
    func.value = int(sop[0].split()[1])
    return func


def mergeFunc(func: BasicFunc, fanins: list, verbose: bool = False) -> LUTFunc:
    assert len(fanins) == func.n_inputs, "the number of inputs must match"
    # extract the terms
    value = func.value
    numInputs = fanins[0].n_inputs
    tts = [getTT(sopToTree(x.terms, x.value, numInputs)) for x in fanins]

    ttSop = ttFalse(numInputs)
    for term in func.terms:
        # get the product of the term
        ttProd = ttTrue(numInputs)
        for i, c in enumerate(term):
            if verbose:
                print(f"{ttProd} & {tts[i]}", end=" ")

            if c == "1":
                ttProd = ttAnd(ttProd, tts[i])
            elif c == "0":
                ttProd = ttAnd(ttProd, ttNot(tts[i]))
            else:
                assert c == "-"

            if verbose:
                print(f"= {ttProd}")

        if verbose:
            print(f"{ttSop} | {ttProd}", end=" ")
        ttSop = ttOr(ttSop, ttProd)
        if verbose:
            print(f"= {ttSop}")

    terms = fromTT(ttSop).toTerms(True, numInputs)
    # print(f"terms: {terms}, sop: {ttSop}")
    return LUTFunc(numInputs, terms, value)


def simulate(graph: BLIFGraph, signal: str, cut: List[str]) -> LUTFunc:
    if signal in cut:
        # get the position of the signal in the cut
        idx = cut.index(signal)
        newFunc = Wire(len(cut), index=idx)
    elif graph.is_const0(signal):
        newFunc = Constant0(len(cut))
    elif graph.is_const1(signal):
        newFunc = Constant1(len(cut))
    else:
        assert signal in graph.get_nodes()
        func: BasicFunc = readFunc(graph.funcOf(signal))
        faninFuncs = [simulate(graph, fanin, cut) for fanin in graph.fanins(signal)]
        newFunc: LUTFunc = mergeFunc(func, faninFuncs)
        # print(f"signal: {signal}, cut: {cut}, func: {func.tt}, fanins: {[x.tt for x in faninFuncs]}, newFunc: {newFunc.tt}")
    # print(f"signal: {signal}, cut: {cut}, func: {newFunc.sop}")
    return newFunc
