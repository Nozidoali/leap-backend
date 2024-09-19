import pandas as pd
import subprocess
import numpy as np

precharacterization = {
    "multiplier": 8.67,
    "square": 11.025,
    "cube": 16.157,
    "modulo": 105.6,
}

if __name__ == "__main__":

    datas = []
    unit = "cube"

    for clock_period in range(3, 10):
        for method in ["abc", "leap"]:
            for repeat in range(3):
                print(f"Clock period: {clock_period}, Method: {method}")

                n_stages = int(np.ceil(precharacterization[unit] / clock_period))

                subprocess.run(
                    f"./run.sh {n_stages} {clock_period} {method} {unit}> tmp.log",
                    shell=True,
                )

                with open("tmp.log", "r") as f:
                    lines = f.readlines()
                    if len(lines) == 8:
                        latency = int(lines[3].strip())
                        lines = lines[0:3] + lines[4:]
                    else:
                        latency = n_stages - 1

                    lev_before = int(lines[0].strip())
                    node_before = int(lines[1].strip())
                    lat_before = int(lines[2].strip())
                    lev_after = int(lines[3].strip())
                    node_after = int(lines[4].strip())
                    lat_after = int(lines[5].strip())
                    vpr_delay = float(lines[6].strip())

                datas.append(
                    {
                        "clock_period": clock_period,
                        "method": method,
                        "lev_before": lev_before,
                        "node_before": node_before,
                        "lat_before": lat_before,
                        "lev_after": lev_after,
                        "node_after": node_after,
                        "lat_after": lat_after,
                        "vpr_delay": vpr_delay,
                        "latency": latency,
                    }
                )

                df = pd.DataFrame(datas)
                df.to_csv("result.csv", index=False)
