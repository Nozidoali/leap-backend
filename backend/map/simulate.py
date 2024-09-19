from .dt import *
from .tt import *
from ..blif import *


class BasicFunc:
    def __init__(self, n_inputs: int) -> None:
        self.n_inputs = n_inputs
        self.terms = []
        self.value = None

    @property
    def sop(self):
        return [f"{x} {self.value}" for x in self.terms]


class Constant0(BasicFunc):
    def __init__(self, n_inputs: int) -> None:
        super().__init__(n_inputs)
        self.terms = ["-" * n_inputs]
        self.value = 0


class Constant1(BasicFunc):
    def __init__(self, n_inputs: int) -> None:
        super().__init__(n_inputs)
        self.terms = ["-" * n_inputs]
        self.value = 1


class Wire(BasicFunc):
    def __init__(self, n_inputs: int, index: int) -> None:
        super().__init__(n_inputs)
        self.index = index
        self.terms = [f"{'-'*index}1{'-'*(n_inputs-index-1)}"]
        self.value = 1


class LUTFunc(BasicFunc):
    def __init__(self, n_inputs: int, terms: list, value: int) -> None:
        super().__init__(n_inputs)
        self.terms = terms[:]
        self.value = value


def readFunc(sop: list) -> BasicFunc:
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


def simulate(graph: BLIFGraph, signal: str, cut: list) -> LUTFunc:
    if signal in cut:
        # get the position of the signal in the cut
        idx = cut.index(signal)
        newFunc = Wire(len(cut), idx)
    elif graph.is_const0(signal):
        newFunc = Constant0(len(cut))
    elif graph.is_const1(signal):
        newFunc = Constant1(len(cut))
    else:
        assert signal in graph.get_nodes()
        func: BasicFunc = readFunc(graph.funcOf(signal))
        faninFuncs = [simulate(graph, fanin, cut) for fanin in graph.fanins(signal)]
        newFunc: LUTFunc = mergeFunc(func, faninFuncs)
    # print(f"signal: {signal}, cut: {cut}, func: {newFunc.sop}")
    return newFunc
