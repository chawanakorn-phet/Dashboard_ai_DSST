"""Build dashboard tables from REAL open data (US-centric; country is not a constraint per project owner).

Inputs (data/raw/, fetched by etl/download_raw.py):
  C2019_A..C2024_A.zip  NCES IPEDS completions by CIP x award level   (public domain, US Dept. of Education)
  HD2024.zip            IPEDS institution directory
  IC2023_AY.zip         IPEDS academic-year tuition & fees
  Most-Recent-Cohorts-Field-of-Study_*.zip  College Scorecard field-of-study earnings/employment
  data_jobs.csv         Luke Barousse 2023 data job postings          (Apache-2.0, Hugging Face)
  data/curated/courses_curated.csv  hand-collected required courses of 9 programs (source URL per row)
Outputs: data/processed/{programs,graduates,courses,outcomes,postings}.csv
"""
import ast
import re
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

from skills import map_course, map_posting_skill

ROOT = Path(__file__).resolve().parents[1]
RAW, CUR, OUT = ROOT / "data" / "raw", ROOT / "data" / "curated", ROOT / "data" / "processed"

CIP = {  # IPEDS 6-digit CIP -> (field, title)
    "11.0102": ("AI", "Artificial Intelligence"),
    "30.7001": ("DS", "Data Science"), "30.7101": ("DS", "Data Analytics"), "30.7102": ("DS", "Business Analytics"),
    "30.7103": ("DS", "Data Visualization"), "30.7104": ("DS", "Financial Analytics"), "30.7199": ("DS", "Data Analytics, Other"),
    "27.0501": ("STAT", "Statistics"), "27.0502": ("STAT", "Mathematical Statistics & Probability"),
    "27.0503": ("STAT", "Mathematics & Statistics"), "27.0599": ("STAT", "Statistics, Other"),
}
CIP4_TO_FIELD = {"3070": "DS", "3071": "DS", "2705": "STAT"}  # Scorecard uses 4-digit CIP; no AI-only code exists
AWARD = {5: "Bachelor", 7: "Master", 17: "PhD", 18: "PhD", 19: "PhD"}
YEARS_OF_STUDY = {"Bachelor": 4, "Master": 2, "PhD": 5}


def read_zip_csv(path, usecols=None, **kw):
    """Read the main CSV of an IPEDS zip; some files carry a UTF-8 BOM that latin1 turns into 'ï»¿' in the first header."""
    z = zipfile.ZipFile(path)
    name = [n for n in z.namelist() if not n.endswith("_rv.csv")][0]
    clean = lambda c: c.replace("ï»¿", "").strip()  # noqa: E731
    want = None if usecols is None else (lambda c: clean(c) in usecols) if not callable(usecols) else (lambda c: usecols(clean(c)))
    df = pd.read_csv(z.open(name), encoding="latin1", usecols=want, **kw)
    return df.rename(columns=clean)


def build_graduates():
    frames = []
    for f in sorted(RAW.glob("C20??_A.zip")):
        year = int(f.name[1:5])
        df = read_zip_csv(f, usecols=lambda c: c in ("UNITID", "CIPCODE", "AWLEVEL", "CTOTALT"), dtype={"CIPCODE": str})
        df = df[df.CIPCODE.isin(CIP) & df.AWLEVEL.isin(AWARD)]
        frames.append(df.assign(year=year))
    g = pd.concat(frames)
    g["level"] = g.AWLEVEL.map(AWARD)
    g = g.groupby(["UNITID", "CIPCODE", "level", "year"], as_index=False).CTOTALT.sum()
    g["program_id"] = g.UNITID.astype(str) + "-" + g.CIPCODE + "-" + g.level
    return g.rename(columns={"CTOTALT": "count"})


def curated_program_keys():
    """(program_id, UNITID, CIPCODE, level) of every curated program, even if IPEDS lists no completers yet."""
    c = pd.read_csv(CUR / "courses_curated.csv", dtype={"cip": str}).drop_duplicates(["institution", "cip", "award_level"])
    hd = read_zip_csv(RAW / "HD2024.zip", usecols=["UNITID", "INSTNM"])
    c = c.merge(hd, left_on="institution", right_on="INSTNM")
    c["level"] = c.award_level.map({5: "Bachelor", 7: "Master"})
    c["program_id"] = c.UNITID.astype(str) + "-" + c.cip + "-" + c.level
    return c.rename(columns={"cip": "CIPCODE"})[["program_id", "UNITID", "CIPCODE", "level"]]


def build_programs(g):
    hd = read_zip_csv(RAW / "HD2024.zip", usecols=["UNITID", "INSTNM", "STABBR"])
    ic = read_zip_csv(RAW / "IC2023_AY.zip", usecols=["UNITID", "TUITION2", "FEE2", "TUITION6", "FEE6"])
    base = pd.concat([g[["program_id", "UNITID", "CIPCODE", "level"]], curated_program_keys()]).drop_duplicates("program_id")
    p = base.merge(hd, on="UNITID", how="left").merge(ic, on="UNITID", how="left")
    for c in ("TUITION2", "FEE2", "TUITION6", "FEE6"):
        p[c] = pd.to_numeric(p[c], errors="coerce")  # IPEDS uses blanks / "." for not applicable
    ug = p.level == "Bachelor"
    p["tuition_per_year"] = np.where(ug, p.TUITION2 + p.FEE2, p.TUITION6 + p.FEE6)
    p["tuition_total"] = p.tuition_per_year * p.level.map(YEARS_OF_STUDY)
    p["field"] = p.CIPCODE.map(lambda c: CIP[c][0])
    p["university"] = p.INSTNM.fillna("Unknown (" + p.UNITID.astype(str) + ")")
    p["program_name"] = p.CIPCODE.map(lambda c: CIP[c][1]) + " (" + p.level + ") – " + p.university
    return p.rename(columns={"CIPCODE": "cip"})[["program_id", "UNITID", "program_name", "university", "STABBR", "level", "field", "cip",
                                                  "tuition_per_year", "tuition_total"]]


def build_outcomes(programs, g):
    """College Scorecard field-of-study earnings. Published horizons in this release: 1, 3, 4, 5 years after completion
    (no 2-year horizon). "Employed" = working and not enrolled (WNE) - the not-working count is mostly suppressed, so
    we report counts + median earnings, NOT an employment rate."""
    cache = CUR / "outcomes_scorecard.csv"
    zips = list(RAW.glob("Most-Recent-Cohorts-Field-of-Study_*.zip"))
    if not zips:  # Scorecard host blocks some cloud IPs (HTTP 403) - fall back to the committed derived table
        print(f"WARNING: Scorecard zip not found in {RAW}; using cached {cache.name}")
        return pd.read_csv(cache)
    f = zips[0]
    years = (1, 3, 4, 5)
    cols = ["UNITID", "CIPCODE", "CREDLEV"] + [f"EARN_COUNT_WNE_{y}YR" for y in years] +            [f"EARN_MDN_{y}YR" for y in (1, 4, 5)] + ["EARN_NE_MDN_3YR"]
    z = zipfile.ZipFile(f)
    name = [n for n in z.namelist() if n.lower().endswith(".csv")][0]
    fs = pd.read_csv(z.open(name), usecols=cols, dtype=str, na_values=["PS", "NULL", "PrivacySuppressed"])
    fs = fs.dropna(subset=["UNITID"])
    fs["field"] = fs.CIPCODE.str[:4].map(CIP4_TO_FIELD)
    fs = fs[fs.field.notna() & fs.CREDLEV.isin(["3", "5", "6"])]
    fs["level"] = fs.CREDLEV.map({"3": "Bachelor", "5": "Master", "6": "PhD"})
    rows = []
    for r in fs.itertuples():
        for y in years:
            n = pd.to_numeric(getattr(r, f"EARN_COUNT_WNE_{y}YR"))
            m = pd.to_numeric(r.EARN_NE_MDN_3YR if y == 3 else getattr(r, f"EARN_MDN_{y}YR"))
            if pd.notna(n):
                rows.append(dict(UNITID=int(r.UNITID), field=r.field, level=r.level, years_after=y, n_employed=n, median_earnings=m))
    o = pd.DataFrame(rows)
    # Scorecard is field-level (4-digit CIP): attach to the single biggest program of each institution x field x level
    tot = g.groupby("program_id")["count"].sum().rename("tot")
    key = programs.merge(tot, left_on="program_id", right_index=True)
    key = key.sort_values("tot", ascending=False).drop_duplicates(["UNITID", "field", "level"])[["program_id", "UNITID", "field", "level"]]
    o = o.merge(key, on=["UNITID", "field", "level"])
    o = o[["program_id", "years_after", "n_employed", "median_earnings"]]
    o.to_csv(cache, index=False)  # small derived cache, committed so cloud environments without access still work
    return o


def build_courses(programs):
    c = pd.read_csv(CUR / "courses_curated.csv", dtype={"cip": str})
    hd = read_zip_csv(RAW / "HD2024.zip", usecols=["UNITID", "INSTNM"])
    c = c.merge(hd, left_on="institution", right_on="INSTNM", how="left")
    miss = c[c.UNITID.isna()].institution.unique()
    if len(miss):
        raise SystemExit(f"institution(s) not found in IPEDS HD: {list(miss)}")
    level = {5: "Bachelor", 7: "Master"}
    c["program_id"] = c.UNITID.astype(int).astype(str) + "-" + c.cip + "-" + c.award_level.map(level)
    rows = [dict(program_id=r.program_id, course=f"{r.code} {r.course}", credits=r.credits, skill=s, source_url=r.source_url)
            for r in c.itertuples() for s in map_course(r.course)]
    out = pd.DataFrame(rows)
    out["has_graduates"] = out.program_id.isin(programs.program_id)
    return out


LEVEL_SENIOR = re.compile(r"\b(senior|sr\.?|lead|principal|staff|head|director|manager|vp|chief|architect)\b", re.I)
LEVEL_JUNIOR = re.compile(r"\b(junior|jr\.?|entry|intern|internship|associate|graduate|trainee|new grad|apprentice)\b", re.I)
AI_TITLE = re.compile(r"\b(ai|a\.i\.|machine learning|deep learning|nlp|computer vision|llm|generative|ml)\b", re.I)
STAT_TITLE = re.compile(r"statistic|biostat|quantitative", re.I)


def build_postings(top_countries=25):
    use = ["job_title_short", "job_title", "job_country", "job_posted_date", "company_name", "salary_year_avg", "job_skills"]
    d = pd.read_csv(RAW / "data_jobs.csv", usecols=use)
    title = d.job_title.fillna("")
    field = np.select(
        [title.str.contains(STAT_TITLE), d.job_title_short.str.contains("Machine Learning") | title.str.contains(AI_TITLE),
         d.job_title_short.str.contains("Data Scientist")],
        ["STAT", "AI", "DS"], default="")
    d = d.assign(field=field)
    d = d[d.field != ""].copy()
    t = d.job_title.fillna("")
    d["level"] = np.where(t.str.contains(LEVEL_SENIOR) | d.job_title_short.str.contains("Senior"), "เชี่ยวชาญ",
                          np.where(t.str.contains(LEVEL_JUNIOR), "เริ่มต้น", "ปานกลาง"))
    d["posted"] = pd.to_datetime(d.job_posted_date, errors="coerce")
    d["year"], d["month"] = d.posted.dt.year, d.posted.dt.month
    keep = d.job_country.value_counts().head(top_countries).index
    d = d[d.job_country.isin(keep)].rename(columns={"job_country": "country", "company_name": "company", "salary_year_avg": "salary_usd"})
    d = d.reset_index(drop=True)
    d["posting_id"] = "J" + d.index.astype(str)

    def conv(s):
        try:
            toks = ast.literal_eval(s) if isinstance(s, str) else []
        except (ValueError, SyntaxError):
            toks = []
        out = []
        for tk in toks:
            for sk in map_posting_skill(tk):
                if sk not in out:
                    out.append(sk)
        return "|".join(out)

    d["skills"] = d.job_skills.map(conv)
    d["raw_skill_count"] = d.job_skills.map(lambda s: len(ast.literal_eval(s)) if isinstance(s, str) and s.startswith("[") else 0)
    d["title"] = d.job_title_short
    cols = ["posting_id", "title", "company", "country", "field", "level", "year", "month", "salary_usd", "skills"]
    return d[cols], d


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    g = build_graduates()
    programs = build_programs(g)
    outcomes = build_outcomes(programs, g)
    courses = build_courses(programs)
    postings, raw = build_postings()
    g[["program_id", "year", "count"]].to_csv(OUT / "graduates.csv", index=False)
    programs.to_csv(OUT / "programs.csv", index=False)
    outcomes.to_csv(OUT / "outcomes.csv", index=False)
    courses.to_csv(OUT / "courses.csv", index=False)
    postings.to_csv(OUT / "postings.csv", index=False)
    # coverage report — how much of the raw data the skill mapping actually captured
    tok = raw.job_skills.dropna().map(ast.literal_eval).explode().str.lower()
    mapped = tok.map(lambda t: bool(map_posting_skill(t)))
    print(f"programs={len(programs)} graduates rows={len(g)} outcomes={len(outcomes)} course-skill rows={len(courses)} postings={len(postings)}")
    print(f"posting skill tokens mapped: {mapped.mean():.1%} (unmapped top: {tok[~mapped].value_counts().head(15).to_dict()})")
    print("postings without any mapped skill:", f"{(postings.skills == '').mean():.1%}")


if __name__ == "__main__":
    main()
