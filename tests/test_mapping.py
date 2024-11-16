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


# Test 03
# simulate
def test_03_simulate():
    graph = BLIFGraph()
    graph.create_pi("a")
    graph.create_po("d")

    graph.create_not("a", "n1")
    graph.create_and("a", "n1", "d")
    
    cut = ["a"]
    root = "d"
    func: LUTFunc = simulate(graph, root, cut)
    assert func.sop == [], func.sop
    
    
# Test 04
# simulate
def test_04_simulate():
    graph = BLIFGraph()
    graph.create_pi("a")
    graph.create_po("d")

    graph.create_not("a", "n1")
    graph.create_or("a", "n1", "d")
    
    cut = ["a"]
    root = "d"
    func: LUTFunc = simulate(graph, root, cut)
    assert func.sop != [], func.sop


# Test 05
# simulate
def test_05_simulate():
    graph = BLIFGraph()
    graph.create_pi("a")
    graph.create_po("d")

    graph.create_node("n1", ["a"], ["1 0"]) # different not definition
    graph.create_and("a", "n1", "d")
    
    cut = ["a"]
    root = "d"
    func: LUTFunc = simulate(graph, root, cut)
    assert func.sop == [], func.sop
    
    
# Test 06
# simulate
def test_06_simulate():
    graph = BLIFGraph()
    graph.create_pi("a")
    graph.create_po("d")

    graph.create_node("n1", ["a"], ["1 0"])
    graph.create_or("a", "n1", "d")
    
    cut = ["a"]
    root = "d"
    func: LUTFunc = simulate(graph, root, cut)
    assert func.sop != [], func.sop
    
if __name__ == "__main__":
    # test_00_sop_to_dt()
    # test_01_simulate()
    # test_02_simulate()
    # test_03_simulate()
    # test_04_simulate()
    test_05_simulate()
    # test_06_simulate()