"""Load datasets. Currently reads the synthetic sample; swap DATA_DIR for processed real data later."""
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data" / "sample"
IS_SAMPLE = True


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
    rd = lambda n: pd.read_csv(DATA_DIR / f"{n}.csv")  # noqa: E731
    postings = rd("postings")
    ps = postings[["posting_id", "skills"]].assign(skill=lambda d: d.skills.str.split("|")).explode("skill")
    return Data(rd("programs"), rd("graduates"), rd("courses"), rd("outcomes"),
                postings.drop(columns="skills"), ps[["posting_id", "skill"]])
