from typing import List

from .dt import *


def getTT(dt: DTree) -> List[bool]:
    # convert the decision tree to a truth table
    n: int = 2**dt.numInputs
    return [dt.getVal(i) for i in range(n)]


def fromTT(tt: List[bool]) -> DTree:
    # convert the truth table to a decision tree
    import math

    terms = []
    numInputs: int = int(math.log2(len(tt)))
    for i, val in enumerate(tt):
        if val:
            term = bin(i)[2:].zfill(numInputs)[::-1]
            terms.append(term)

    dt: DTree = sopToTree(terms, True, numInputs)
    return dt


def ttFalse(n: int) -> List[bool]:
    return [False] * (2**n)


def ttTrue(n: int) -> List[bool]:
    return [True] * (2**n)


def ttAnd(a: List[bool], b: List[bool]) -> List[bool]:
    return [x and y for x, y in zip(a, b)]


def ttOr(a: List[bool], b: List[bool]) -> List[bool]:
    return [x or y for x, y in zip(a, b)]


def ttNot(a: List[bool]) -> List[bool]:
    return [not x for x in a]


def ttStr(tt: List[bool]) -> str:
    return "".join(["1" if x else "0" for x in tt])
