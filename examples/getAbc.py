def getAbcInfoFrom(logFile: str) -> list:
    datas = []
    with open(logFile, "r") as f:
        for line in f:
            data = {}
            line = line.strip()
            # remove "="
            line = line.replace("=", " ")
            # split by " "
            line = line.split()
            for i in range(len(line)):
                if line[i] == "lev":
                    try:
                        data["lev"] = int(line[i + 1])
                    except:
                        continue
                if line[i] == "lat":
                    try:
                        data["lat"] = int(line[i + 1])
                    except:
                        continue
                if line[i] == "nd" or line[i] == "and":
                    try:
                        data["node"] = int(line[i + 1])
                    except:
                        continue
            if data != {} and "lev" in data and "lat" in data and "node" in data:
                datas.append(data)
    return datas

if __name__ == "__main__":

    import argparse
    parser = argparse.ArgumentParser(description='Get ABC info from log file.')
    parser.add_argument('logFile', type=str, help='log file')
    datas = getAbcInfoFrom(parser.parse_args().logFile)
    print(datas[0]["lev"])
    print(datas[0]["node"])
    print(datas[0]["lat"])