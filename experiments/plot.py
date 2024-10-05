def plot(csvFile: str):
    import matplotlib.pyplot as plt

    df = pd.read_csv(csvFile)

    # we plot the vpr_delay of leap and abc, x-axis is the clock period
    fig, ax = plt.subplots()
    for method in ["abc", "leap"]:
        df_method = df[df["method"] == method]
        # we plot the scatter plot
        ax.scatter(df_method["clock_period"], df_method["vpr_delay"], label=method)

        # we find the average for each clock period
        # we need to drop the method
        df_method = df_method.drop(columns=["method"])
        df_avg = df_method.groupby("clock_period").mean()
        ax.plot(
            df_avg.index, df_avg["vpr_delay"], label=f"{method} (avg)", linestyle="--"
        )

    ax.set_xlabel("Clock period")
    ax.set_ylabel("VPR delay")
    ax.legend()
    plt.savefig("plot.png")


if __name__ == "__main__":
    import pandas as pd
    import sys

    plot(sys.argv[1])
