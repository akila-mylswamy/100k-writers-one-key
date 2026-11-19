from pathlib import Path
from statistics import median
import math
import re

root = Path(__file__).resolve().parent

workloads = {
    "hot": "1 hot row",
    "5": "5 random shards",
    "50": "50 random shards",
}

results = {}

for name, label in workloads.items():
    tps_values = []
    p99_values = []

    for round_num in (1, 2, 3):
        prefix = f"controlled_r{round_num}_{name}"

        summary = (
            root / "summaries" / f"{prefix}_summary.txt"
        ).read_text()

        match = re.search(r"^tps = ([\d.]+)", summary, re.M)
        if not match:
            raise ValueError(f"TPS missing: {prefix}")

        tps = float(match.group(1))

        latencies = []
        log_files = list(
            (root / "logs").glob(prefix + ".[0-9]*")
        )

        if len(log_files) != 5:
            raise ValueError(
                f"{prefix}: expected 5 logs, found {len(log_files)}"
            )

        for filename in log_files:
            with filename.open() as f:
                for line in f:
                    fields = line.split()
                    latencies.append(int(fields[2]) / 1000)

        latencies.sort()

        if len(latencies) != 100000:
            raise ValueError(
                f"{prefix}: expected 100000 transactions, "
                f"found {len(latencies)}"
            )

        p99 = latencies[math.ceil(0.99 * len(latencies)) - 1]

        tps_values.append(tps)
        p99_values.append(p99)

        print(
            f"{prefix:20s} "
            f"TPS={tps:10.2f} "
            f"p99={p99:7.3f} ms"
        )

    results[name] = {
        "tps": median(tps_values),
        "p99": median(p99_values),
    }

print("\nMEDIAN ACROSS THREE ROUNDS")

baseline = results["hot"]

for name, label in workloads.items():
    value = results[name]
    speedup = value["tps"] / baseline["tps"]

    print(
        f"{label:18s} "
        f"TPS={value['tps']:10.2f} "
        f"p99={value['p99']:7.3f} ms "
        f"speedup={speedup:.2f}x"
    )
