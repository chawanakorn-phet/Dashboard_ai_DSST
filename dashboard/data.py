"""Load the processed real datasets produced by etl/build_real_data.py."""
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"
DATA_DIR = PROCESSED
IS_SAMPLE = False  # kept so the UI can show a synthetic-data banner if sample data is ever reintroduced


@dataclass
class Data:
    programs: pd.DataFrame
    graduates: pd.DataFrame
    courses: pd.DataFrame      # program_id, course, credits, skill
    outcomes: pd.DataFrame
    postings: pd.DataFrame
    posting_skills: pd.DataFrame  # posting_id, skill


@lru_cache(maxsize=1)
def load() -> Data:
    if not (DATA_DIR / "postings.csv").exists():
        raise SystemExit("data/processed is missing - run: python etl/download_raw.py && python etl/build_real_data.py")
    rd = lambda n: pd.read_csv(DATA_DIR / f"{n}.csv")  # noqa: E731
    postings = rd("postings")
    postings = postings[postings.skills.notna() & (postings.skills != "")]  # demand is measured on postings with skills
    # integer ids + categorical skills keep the per-click isin/groupby work fast (~200k postings, ~650k posting-skill rows)
    postings = postings.assign(posting_id=postings.posting_id.str.lstrip("J").astype("int32"))
    ps = postings[["posting_id", "skills"]].assign(skill=lambda d: d.skills.str.split("|")).explode("skill")
    ps = ps.drop_duplicates(["posting_id", "skill"]).assign(skill=lambda d: d.skill.astype("category"))
    programs, courses = rd("programs"), rd("courses")
    if "tuition_total" not in programs:
        programs["tuition_total"] = float("nan")
    return Data(programs, rd("graduates"), courses, rd("outcomes"),
                postings.drop(columns="skills"), ps[["posting_id", "skill"]])
