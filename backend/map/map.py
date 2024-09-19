from ..blif import *
from .simulate import *


def mapNode(graph: BLIFGraph, mapped: BLIFGraph, signal2cut: dict):
    for signal in graph.cos():
        mapNodeRec(graph, mapped, signal2cut, signal)


def mapNodeRec(graph: BLIFGraph, mapped: BLIFGraph, signal2cut: dict, signal: str):
    if signal in mapped.get_nodes():
        return
    if graph.is_ci(signal):
        return
    cut = signal2cut[signal]
    for fanin in cut:
        mapNodeRec(graph, mapped, signal2cut, fanin)

    func = simulate(graph, signal, cut)
    mapped.create_node(signal, cut, func.sop)


def techmap(graph: BLIFGraph, signal2cut: dict) -> BLIFGraph:
    newGraph = BLIFGraph()
    newGraph.top_module = graph.top_module

    # CIs
    newGraph.inputs = graph.inputs.copy()
    newGraph.register_outputs = graph.register_outputs.copy()

    # COs
    newGraph.outputs = graph.outputs.copy()
    newGraph.register_inputs = graph.register_inputs.copy()
    newGraph.ro_to_ri = graph.ro_to_ri.copy()
    newGraph.ro_types = graph.ro_types.copy()

    newGraph.const0 = graph.const0.copy()
    newGraph.const1 = graph.const1.copy()
    newGraph.submodules = graph.submodules.copy()

    # start the mapping
    mapNode(graph, newGraph, signal2cut)

    newGraph.traverse()

    return newGraph
