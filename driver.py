###driver.py
import argparse
import subprocess
from pathlib import Path

def args_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--cfgdir",
        type=str,
        default=".",
        help="Directory to search for .cfg files (default: current folder)"
    )
    parser.add_argument(
        "--csvdir",
        type=str,
        default="csv_data",
        help="Directory to save generated CSV files"
    )
    parser.add_argument(
        "--plotdir",
        type=str,
        default="pdf_graph",
        help="Directory to save generated plot PDFs"
    )
    return parser.parse_args()

def find_cfg_files(cfg_dir: str):
    return sorted(Path(cfg_dir).glob("*.cfg"))


def main():
    args = args_parse()

    # Ensure cfgdir exists
    cfg_path = Path(args.cfgdir)
    if not cfg_path.exists():
        cfg_path.mkdir(parents=True)
        print(f"Created missing directory: {args.cfgdir}")
        print("Please add .cfg files to this folder and rerun the command.")
        return

    # Ensure output directories exist
    Path(args.csvdir).mkdir(parents=True, exist_ok=True)
    Path(args.plotdir).mkdir(parents=True, exist_ok=True)

    cfg_files = find_cfg_files(args.cfgdir)
    if not cfg_files:
        print(f"⚠️ No .cfg files found in {args.cfgdir}. Please add some and try again.")
        return

    for cfg_file in cfg_files:
        stem = cfg_file.stem
        csv_path = f"{args.csvdir}/{stem}-data.csv"

        # Step 1: run generator
        subprocess.run([
            "python", "generator.py",
            str(cfg_file),
            "--output", csv_path
        ], check=True)

        # Step 2: run plotter
        subprocess.run([
            "python", "plotter.py",
            csv_path,
            "--outdir", args.plotdir
        ], check=True)

        print(f"Done: {cfg_file.name}")



if __name__ == "__main__":
    main()

