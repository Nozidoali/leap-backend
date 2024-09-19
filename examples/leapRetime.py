from lp import *


def retime(inputFile, outputFile, clockPeriod):

    graph = read_blif(inputFile)
    manager = LPManager()
    manager.setClockPeriod(float(clockPeriod))

    manager.linkSubjectGraph(graph)
    manager.addObjective()
    manager.solve()
    manager.insertBuffers()
    manager.dumpGraph(outputFile)

    latency = manager.getLatency()
    print(int(latency))


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Retime the BLIF file")
    parser.add_argument("-i", "--input", help="Input BLIF file")
    parser.add_argument("-o", "--output", help="Output BLIF file")
    parser.add_argument("-c", "--clock", help="Clock period")
    args = parser.parse_args()
    retime(args.input, args.output, args.clock)
