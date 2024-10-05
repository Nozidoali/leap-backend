from backend import *


def main():
    # input_file = "examples/blif/const.blif"
    input_file = "examples/adder.blif"
    output_file = "tmp.blif"

    graph = read_blif(input_file)
    print(f"number of nodes: {len(graph.nodes)}")
    model = MapBufModel(graph, {}, 10000)
    # model.dumpModel("tmp.lp")
    model.solve()
    model.dumpGraph(output_file)

    import subprocess

    subprocess.run(f"abc -c 'cec {input_file} {output_file}'", shell=True)


if __name__ == "__main__":
    main()
