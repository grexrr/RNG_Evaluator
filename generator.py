# generator.py
import math
import numpy as np
import argparse
import csv, os

def _args_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("config", help="Path to the .cfg file")
    parser.add_argument(
        "--output",
        type=str,
        help="Optional path to save the generated .csv file. Default: <cfg name>-data.csv",
        default=None
    )
    return parser.parse_args()

def _parse_cfg_file(path):
    with open(path, "r") as f:
        lines = f.readlines()

    seed = None
    samples = None
    dist_list = []

    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if line.lower().startswith("seed"):
            seed = int(line.split("=")[1].strip())
        elif line.lower().startswith("samples"):
            samples = int(line.split("=")[1].strip())
        else:
            parts = line.split()
            dist_name = parts[0].lower()
            dist_args = parts[1:]
            dist_list.append((dist_name, dist_args))

    return seed, samples, dist_list


def _generate_data(seed, samples, dist_list):
    np.random.seed(seed)
    rng_factory = RNGFactory(seed, samples)

    headers = []
    data = []

    for dist_name, args in dist_list:
        try:
            values = rng_factory.get(dist_name, args)
            param_str = ", ".join(args)
            headers.append(f"{dist_name}({param_str})")
            data.append(values)
        except Exception as e:
            print(f"Error generating '{dist_name}({', '.join(args)})': {e}")
            continue

    return headers, np.array(data).T



def _save_to_csv(filename, header, data):
    os.makedirs(os.path.dirname(filename), exist_ok=True)  # 自动创建父目录
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(data)



#################### RNG ########################
class RNGFactory:
    def __init__(self, seed: int, count: int):
        self.seed = seed
        self.count = count
        self._dist_map = {
            "dag": lambda args: self.dagum(*map(float, args)),
            "ske": lambda args: self.skellam(*map(float, args)),
            "exp": lambda args: self.exponential(*map(float, args)),
            "gau": lambda args: self.gaussian(*map(float, args)),
        }

    def get(self, dist_name: str, args: list[str]):
        dist_name = dist_name.lower()
        if dist_name not in self._dist_map:
            raise ValueError(f"Unsupported distribution: {dist_name}")
        return self._dist_map[dist_name](args)

    # THIS IS MY TARGET(123120787)
    def dagum(self, a: float, b: float, p: float):
        u = np.random.uniform(0, 1, self.count)
        return b * ((u ** (-1 / p) - 1) ** (-1 / a))
    
    # THIS IS MY TARGET(123120787)
    @staticmethod
    def bessel_I(k: int, x: float, terms: int = 20) -> float:
        res = 0.0
        x_half = x / 2
        for m in range(terms):
            try:
                numerator = x_half ** (2 * m + k)
                denominator = math.factorial(m) * math.factorial(m + k)
                res += numerator / denominator
            except OverflowError:
                break
        return res

    def skellam(self, mu1: float, mu2: float):
        k_range = np.arange(-30, 31)
        x = 2 * np.sqrt(mu1 * mu2)

        with np.errstate(divide='ignore', invalid='ignore'):
            ratio = (mu1 / mu2) ** (k_range / 2)

        pmf = np.array([
            np.exp(-(mu1 + mu2)) * ratio[i] * self.bessel_I(abs(int(k)), x)
            for i, k in enumerate(k_range)
        ])

        if not np.isfinite(pmf).all() or pmf.sum() == 0:
            raise ValueError("Invalid Skellam PMF: check parameters.")

        pmf /= pmf.sum()
        cdf = np.cumsum(pmf)
        u = np.random.uniform(0, 1, self.count)
        samples = np.searchsorted(cdf, u)
        return k_range[samples]

    def exponential(self, lam: float):
        return np.random.exponential(1 / lam, self.count)

    def gaussian(self, mu: float, sigma: float):
        return np.random.normal(mu, sigma, self.count)


def main():
    args = _args_parse()
    seed, samples, dist_list = _parse_cfg_file(args.config)
    headers, data = _generate_data(seed, samples, dist_list)
    csv_path = args.output if args.output else args.config.replace(".cfg", "-data.csv")
    _save_to_csv(csv_path, headers, data)
    print("Saved:", csv_path)


if __name__ == "__main__":
    main()


