def rewriteBlif(inputFile: str, outputFile: str):
    """
    Carmine's code (31.05.2024)
    """
    import re

    with open(inputFile, "r") as f:
        lines = f.readlines()

    with open(outputFile, "w") as f:
        for line in lines:
            line = line.strip()
            if "DFF" in line:
                if "DFFSR" in line:
                    module_name = "DFFSR"
                    continuation = " R=(.+) S=(.+)"
                else:
                    module_name = "DFF"
                    continuation = ""

                reg_pattern = "\.subckt {0} C=(.+) D=(.+) Q=(.+){1}".format(
                    module_name, continuation
                )
                matches = re.findall(reg_pattern, line)
                clock = matches[0][0]
                input = matches[0][1]
                output = matches[0][2]
                line = ".latch {0} {1} re {2} 3".format(input, output, clock)
            if line.startswith(".latch") and "re" not in line:
                # for example: .latch      n1132 cur_state[0]  2
                reg_pattern = "\.latch\s+(.+)\s+(.+)\s+(.+)"
                matches = re.findall(reg_pattern, line)
                input = matches[0][0]
                output = matches[0][1]
                type = matches[0][2]
                if type != "3":
                    clock = "clk"
                    line = ".latch {0} {1} re {2} 3".format(input, output, clock)

            f.write(line + "\n")
    # graph = read_blif(inputFile)
    # write_blif(graph, outputFile)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Rewrite the BLIF file to use the .latch command instead of .subckt"
    )
    parser.add_argument("-i", "--input", help="Input BLIF file")
    parser.add_argument("-o", "--output", help="Output BLIF file")
    args = parser.parse_args()
    rewriteBlif(args.input, args.output)
