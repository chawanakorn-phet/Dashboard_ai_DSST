"""Download the raw open datasets into data/raw/ (skips files that already exist). ~290 MB in total."""
import sys
import urllib.request
from pathlib import Path

RAW = Path(__file__).resolve().parents[1] / "data" / "raw"
IPEDS = "https://nces.ed.gov/ipeds/datacenter/data/"
SCORECARD = "Most-Recent-Cohorts-Field-of-Study_06102026.zip"
FILES = {
    **{f"C{y}_A.zip": f"{IPEDS}C{y}_A.zip" for y in range(2019, 2025)},   # IPEDS completions by CIP x award level
    "HD2024.zip": f"{IPEDS}HD2024.zip",                                    # IPEDS institution directory
    "IC2023_AY.zip": f"{IPEDS}IC2023_AY.zip",                              # IPEDS tuition & fees (academic year)
    SCORECARD: f"https://ed-public-download.scorecard.network/downloads/{SCORECARD}",  # College Scorecard field of study
    "data_jobs.csv": "https://huggingface.co/datasets/lukebarousse/data_jobs/resolve/main/data_jobs.csv",  # Apache-2.0
}


def fetch(url: str, dest: Path):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=120) as r, open(dest, "wb") as f:
        while chunk := r.read(1 << 20):
            f.write(chunk)


def main():
    RAW.mkdir(parents=True, exist_ok=True)
    failed = []
    for name, url in FILES.items():
        dest = RAW / name
        if dest.exists():
            print("have", name)
            continue
        print("get ", name, flush=True)
        try:
            fetch(url, dest)
        except Exception as e:  # keep going: one blocked host should not stop the others
            dest.unlink(missing_ok=True)
            failed.append((name, url))
            print(f"  FAILED: {e}")
    if failed:
        print()
        print("Could not download (open the URL in a browser and save into data/raw/ if needed):")
        for name, url in failed:
            print(f"  {name}")
            print(f"    {url}")
        if all(n == SCORECARD for n, _ in failed):
            print("Only the College Scorecard file failed - OK: the ETL uses data/curated/outcomes_scorecard.csv instead.")
            return
        sys.exit(1)
    print("done")


if __name__ == "__main__":
    main()
