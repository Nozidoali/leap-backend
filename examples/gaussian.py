from backend import *
import json


def main():
    input_file = "examples/gaussian/gaussian.blif"
    input_sched_constr = "examples/gaussian/gaussian.json"
    output_file = "examples/gaussian/gaussian_opt.blif"

    graph = read_blif(input_file)
    model = MapBufModel(graph, json.load(open(input_sched_constr)), 4.2, {"maxLeaves": 6})
    model.solve()

    # print some stats
    print(f"Latency: {model.getLatency()}")
    model.dumpGraph(output_file)


if __name__ == "__main__":
    main()
