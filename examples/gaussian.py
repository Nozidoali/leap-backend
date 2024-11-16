from backend import *
import json


def main():
    input_dir = "examples/gaussian/"
    # input_dir = "examples/gaussian-vitis/"
    input_file = input_dir + "gaussian_abc.blif" # use the functional-hashed blif to avoid constant signal
    input_sched_constr = input_dir + "gaussian.json"
    output_file = input_dir + "gaussian_opt.blif"
    lp_file = input_dir + "gaussian_opt.lp"
    solution_file = input_dir + "gaussian_opt.sol"
    mapping_file = input_dir + "gaussian_mapping.json"

    graph = read_blif(input_file)
    model = MapBufModel(graph, json.load(open(input_sched_constr)), 4.2, {"maxLeaves": 6})
    
    model.dumpIndexMapping(mapping_file)
    model.dumpModel(lp_file)
    model.solve(iterative=True)

    # print some stats
    print(f"Latency: {model.getLatency()}")
    model.dumpGraph(output_file)
    model.dumpModel(solution_file)
    
    # rename the latches in the network
    

    # print the l labels
    # for signal, idx in model.signal2idx.items():
    #     print(f"{signal}: {model.model.getVarByName(f'l_{idx}').X}")

if __name__ == "__main__":
    main()
