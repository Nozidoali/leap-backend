import pygraphviz as pgv

class DNode:
    def __init__(self) -> None:
        self.trueBranch = None
        self.falseBranch = None
        self.idx = None
        self.value = None

class TNode(DNode):
    def __init__(self) -> None:
        super().__init__()
        self.value = 1
        
class FNode(DNode):
    def __init__(self) -> None:
        super().__init__()
        self.value = 0

class DTree:
    def __init__(self) -> None:
        self.root = FNode()
        self.numInputs = 0
        
    def toTerms(self, val: bool, num_inputs: int) -> list:
        return self.toTermsRec(self.root, val, num_inputs)

    def toTermsRec(self, node: DNode, val: bool, num_inputs: int) -> list:
        if isinstance(node, TNode):
            return ["-"*num_inputs] if val else []
        if isinstance(node, FNode):
            return [] if val else ["-"*num_inputs]
        trueTerms = self.toTermsRec(node.trueBranch, val, num_inputs)
        falseTerms = self.toTermsRec(node.falseBranch, val, num_inputs)
        pos = node.idx
        terms = []
        for t in trueTerms:
            terms.append(t[:pos] + "1" + t[pos+1:])
        for f in falseTerms:
            terms.append(f[:pos] + "0" + f[pos+1:])
        return terms

    def toGraph(self, dotFile: str) -> None:
        graph = pgv.AGraph(strict=False, directed=True)
        self.toGraphRec(graph, self.root)
        graph.write(dotFile)
    
    def toGraphRec(self, graph: pgv.AGraph, node: DNode) -> None:
        if isinstance(node, TNode):
            graph.add_node(str(id(node)), label="1")
        elif isinstance(node, FNode):
            graph.add_node(str(id(node)), label="0")
        else:
            graph.add_node(str(id(node)), label=f"{node.idx}?")
            self.toGraphRec(graph, node.trueBranch)
            self.toGraphRec(graph, node.falseBranch)
            graph.add_edge(str(id(node)), str(id(node.trueBranch)), label="1")
            graph.add_edge(str(id(node)), str(id(node.falseBranch)), label="0")

    def getVal(self, index: int) -> bool:
        return self.getValRec(self.root, index)
    
    def getValRec(self, node: DNode, index: int) -> bool:
        if isinstance(node, TNode):
            return True
        if isinstance(node, FNode):
            return False
        tf = (index >> node.idx) & 1
        if tf:
            return self.getValRec(node.trueBranch, index)
        else:
            return self.getValRec(node.falseBranch, index)

def sopToTree(terms: list, val: bool, numInputs) -> DTree:
    dt = DTree()
    dt.root = sopToTreeRec(terms, val)
    dt.numInputs = numInputs
    return dt

def sopToTreeRec(terms: list, val: bool) -> DNode:
    if len(terms) == 0:
        return FNode() if val else TNode()
    # TODO: entropy calculation
    pivot: int = mostInformativeIdx(terms)
    
    if pivot == -1:
        return TNode() if val else FNode()
    
    # print(f"terms: {terms}, pivot: {pivot}")
    node = DNode()
    node.idx = pivot
    
    trueTerms = list(set([x[:pivot] + '-' + x[pivot+1:] for x in terms if x[pivot] != "0"]))
    falseTerms = list(set([x[:pivot] + '-' + x[pivot+1:] for x in terms if x[pivot] != "1"]))
    
    node.trueBranch = sopToTreeRec(trueTerms, val)
    node.falseBranch = sopToTreeRec(falseTerms, val)
    
    return node

def invert(terms: list) -> list:
    # convert terms to a bdd
    dt = DTree()
    
def mostInformativeIdx(terms: list) -> int:
    # calculate the entropy of each variable
    # return the variable with the highest entropy
    import math
    bestEntropy, bestIdx = 0, -1
    for i in range(len(terms[0])):
        ones = sum([1 for x in terms if x[i] == "1"])
        zeros = sum([1 for x in terms if x[i] == "0"])
        dontcares = sum([1 for x in terms if x[i] == "-"])
        total = ones + zeros + dontcares
        if total == 0:
            continue
        if ones == 0 and zeros == 0:
            continue
        prob1 = ones / total + 1e-6
        prob0 = zeros / total + 1e-6
        entropy = -prob1 * math.log2(prob1) - prob0 * math.log2(prob0)
        if entropy > bestEntropy:
            bestEntropy = entropy
            bestIdx = i
    
    return bestIdx