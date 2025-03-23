# plotter.py
import argparse
import pandas as pd
import matplotlib.pyplot as plt

def args_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("csv", help="Path to generated data .csv")
    parser.add_argument("--outdir", type=str, help="Directory to save output PDFs", default=".")
    return parser.parse_args()

def _plot_cdf(df):
    fig, ax = plt.subplots()

    for label, col in df.items():
        sorted_col = col.sort_values()
        y = [v / len(col) for v in range(1, len(col)+1)]
        ax.plot(sorted_col, y, label=label)

    ax.set_title("CDF of Generated Distributions")
    ax.set_xlabel("Value")
    ax.set_ylabel("Cumulative Probability")
    ax.legend(title="Distributions", loc="lower right")
    ax.grid(True)
    fig.tight_layout()

    return fig



def _plot_box(df):
    fig, ax = plt.subplots()
    df.boxplot(ax=ax)

    ax.set_title("Boxplot of Generated Distributions")
    ax.set_ylabel("Value")
    ax.grid(True)

    fig.tight_layout()
    return fig



def main():
    args = args_parse()

    import os
    os.makedirs(args.outdir, exist_ok=True)

    df = pd.read_csv(args.csv)
    
    def extract_dist_name(label: str) -> str:
        return label.split("(")[0]

    prefix = "_".join(extract_dist_name(c) for c in df.columns[:3])  
    base = os.path.join(args.outdir, prefix)

    
    _plot_cdf(df).savefig(base + "-CDF.pdf")
    _plot_box(df).savefig(base + "-Box.pdf")
    print("Saved:", base + "-CDF.pdf and -Box.pdf")

if __name__ == "__main__":
    main()


