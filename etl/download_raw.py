"""Download the raw open datasets into data/raw/ (skips files that already exist). ~290 MB in total."""
import sys
import urllib.request
from pathlib import Path

RAW = Path(__file__).resolve().parents[1] / "data" / "raw"
IPEDS = "https://nces.ed.gov/ipeds/datacenter/data/"
FILES = {
    **{f"C{y}_A.zip": f"{IPEDS}C{y}_A.zip" for y in range(2019, 2025)},   # IPEDS completions by CIP x award level
    "HD2024.zip": f"{IPEDS}HD2024.zip",                                    # IPEDS institution directory
    "IC2023_AY.zip": f"{IPEDS}IC2023_AY.zip",                              # IPEDS tuition & fees (academic year)
    "Most-Recent-Cohorts-Field-of-Study_06102026.zip":                     # College Scorecard field of study
        "https://ed-public-download.scorecard.network/downloads/Most-Recent-Cohorts-Field-of-Study_06102026.zip",
    "data_jobs.csv": "https://huggingface.co/datasets/lukebarousse/data_jobs/resolve/main/data_jobs.csv",  # Apache-2.0
}


def main():
    RAW.mkdir(parents=True, exist_ok=True)
    for name, url in FILES.items():
        dest = RAW / name
        if dest.exists():
            print("have", name)
            continue
        print("get ", name, flush=True)
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=120) as r, open(dest, "wb") as f:
            while chunk := r.read(1 << 20):
                f.write(chunk)
    print("done", file=sys.stderr)


if __name__ == "__main__":
    main()
