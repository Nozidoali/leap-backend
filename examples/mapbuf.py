from backend import *
import json


def main():
    # input_file = "examples/add2/add2.blif"
    # input_sched_constr = "examples/add2/add2.json"
    # output_file = "examples/add2/add2_opt.blif"

    input_file = "examples/mem/mem.blif"
    input_sched_constr = "examples/mem/mem.json"
    output_file = "examples/mem/mem_opt.blif"

    graph = read_blif(input_file)
    model = MapBufModel(graph, json.load(open(input_sched_constr)), 1, {"maxLeaves": 3})
    model.solve()

    # print some stats
    print(f"Latency: {model.getLatency()}")
    model.dumpGraph(output_file)

    import subprocess

    # CEC check works if no buffer is inserted
    # subprocess.run(f"abc -c 'cec {input_file} {output_file}'", shell=True)

    # Verify the LUT level
    # subprocess.run(f"abc -c 'read {output_file}; print_stats'", shell=True)


if __name__ == "__main__":
    main()
