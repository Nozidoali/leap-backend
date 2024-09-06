def getVtrDelayFrom(timingFile: str) -> float:
    import re

    with open(timingFile, "r") as f:
        for line in f:
            # data arrival time 6.355
            m = re.match(r"\s*data arrival time\s+(\d+\.\d+)", line)
            if m:
                return float(m.group(1))
    return None


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Get VTR delay from timing report")
    parser.add_argument("timingFile", help="VTR timing report file")
    args = parser.parse_args()

    delay = getVtrDelayFrom(args.timingFile)
    if delay is not None:
        print(delay)
    else:
        print("Error: failed to get VTR delay")
        exit(1)