from backend import *


# Test 00
#
def test_00_sop_to_dt():
    sop = [
        "0-",
        "1-",
    ]
    dt = sopToTree(sop, True, 2)
    dt.toGraph("tmp.dot")


# Test 01
# simulate
def test_01_simulate():
    graph = BLIFGraph()
    graph.create_pi("a")
    graph.create_pi("b")
    graph.create_pi("c")
    graph.create_po("d")

    graph.create_and("a", "b", "n1")
    graph.create_or("n1", "c", "d")

    cut = ["a", "b", "c"]
    root = "d"
    func: LUTFunc = simulate(graph, root, cut)
    assert func.tt == "00011111"


# Test 02
# simulate
def test_02_simulate():
    graph = BLIFGraph()
    graph.create_pi("a")
    graph.create_pi("b")
    graph.create_pi("c")
    graph.create_po("d")

    graph.create_and("a", "b", "n1")
    graph.create_or("n1", "c", "d")

    cut = ["b", "a", "c"]
    root = "d"
    func: LUTFunc = simulate(graph, root, cut)
    assert func.tt == "00011111"


if __name__ == "__main__":
    # test_00_sop_to_dt()
    test_01_simulate()
    test_02_simulate()
