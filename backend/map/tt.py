from .dt import *


def getTT(dt: DTree) -> list:
    # convert the decision tree to a truth table
    n: int = 2**dt.numInputs
    return [dt.getVal(i) for i in range(n)]


def fromTT(tt: list) -> DTree:
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


def ttFalse(n: int) -> list:
    return [False] * (2**n)


def ttTrue(n: int) -> list:
    return [True] * (2**n)


def ttAnd(a: list, b: list) -> list:
    return [x and y for x, y in zip(a, b)]


def ttOr(a: list, b: list) -> list:
    return [x or y for x, y in zip(a, b)]


def ttNot(a: list) -> list:
    return [not x for x in a]
