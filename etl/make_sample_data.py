"""Generate SYNTHETIC sample data so the dashboard can be developed before real data lands.

Nothing here is real: university names are placeholders and every number is random (seeded).
Output: data/sample/{programs,graduates,courses,outcomes,postings}.csv
"""
from pathlib import Path

import numpy as np
import pandas as pd

OUT = Path(__file__).resolve().parents[1] / "data" / "sample"
RNG = np.random.default_rng(42)

SKILLS = {
    "AI": ["Python", "Machine Learning", "Deep Learning", "NLP", "Computer Vision", "GenAI/LLM",
           "Docker", "Cloud", "MLOps", "Statistics", "SQL"],
    "DS": ["Python", "SQL", "R", "Statistics", "Machine Learning", "Data Visualization", "Tableau",
           "Power BI", "Regression", "A/B Testing", "Spark", "Cloud"],
    "STAT": ["R", "Statistics", "Regression", "Bayesian", "Time Series", "A/B Testing", "Python", "SQL",
             "Data Visualization"],
}
ALL = sorted({s for v in SKILLS.values() for s in v} | {"Airflow"})

PROGRAM_SPECS = [
    ("AI", "วท.บ. ปัญญาประดิษฐ์", "Bachelor"), ("AI", "วท.ม. ปัญญาประดิษฐ์", "Master"),
    ("AI", "วศ.บ. วิศวกรรมปัญญาประดิษฐ์", "Bachelor"), ("AI", "วท.บ. ปัญญาประดิษฐ์และข้อมูล", "Bachelor"),
    ("DS", "วท.บ. วิทยาการข้อมูล", "Bachelor"), ("DS", "วท.บ. วิทยาการข้อมูลและการวิเคราะห์", "Bachelor"),
    ("DS", "วท.ม. วิทยาการข้อมูล", "Master"), ("DS", "วท.บ. วิทยาการข้อมูลธุรกิจ", "Bachelor"),
    ("DS", "วท.บ. การวิเคราะห์ข้อมูล", "Bachelor"),
    ("STAT", "วท.บ. สถิติ", "Bachelor"), ("STAT", "วท.ม. สถิติประยุกต์", "Master"),
    ("STAT", "วท.บ. สถิติและวิทยาการข้อมูล", "Bachelor"),
]
UNIS = ["A", "B", "C", "D", "E", "F"]


def programs_and_children():
    prog, grad, courses, outcomes = [], [], [], []
    for i, (field, name, level) in enumerate(PROGRAM_SPECS, 1):
        pid = f"P{i:02d}"
        uni = f"มหาวิทยาลัยตัวอย่าง {UNIS[i % len(UNIS)]}"
        term = int(RNG.integers(15, 60) * 1000) if level == "Bachelor" else int(RNG.integers(25, 70) * 1000)
        n_terms = 8 if level == "Bachelor" else 4
        prog.append(dict(program_id=pid, program_name=f"{name} – {uni}", university=uni, level=level,
                         field=field, tuition_per_term=term, tuition_total=term * n_terms))
        base = int(RNG.integers(20, 120))
        for y in range(2019, 2026):
            grad.append(dict(program_id=pid, year=y, count=int(base * (1 + 0.15 * (y - 2019)) * RNG.uniform(0.85, 1.15))))
        # each program covers a random 60-85% of its field's skills (+ a few extras)
        pool = SKILLS[field]
        chosen = list(RNG.choice(pool, size=max(4, int(len(pool) * RNG.uniform(0.6, 0.85))), replace=False))
        extras = list(RNG.choice(ALL, size=2, replace=False))
        for s in dict.fromkeys(chosen + extras):
            courses.append(dict(program_id=pid, course=f"วิชาบังคับ: {s} {RNG.integers(1, 3)}",
                                credits=int(RNG.choice([2, 3, 3, 3, 4])), skill=s))
        for cohort in (2021, 2022, 2023):
            n_total = int(RNG.integers(15, 120))
            r1 = RNG.uniform(0.6, 0.85)
            for k, years_after in enumerate((1, 2, 3)):
                emp = min(0.98, r1 + 0.05 * k)
                inf = emp * RNG.uniform(0.4 + 0.1 * k, 0.7 + 0.1 * k)
                outcomes.append(dict(program_id=pid, cohort_year=cohort, years_after=years_after, n_total=n_total,
                                     n_employed=int(n_total * emp), n_in_field=int(n_total * min(inf, emp))))
    return (pd.DataFrame(prog), pd.DataFrame(grad), pd.DataFrame(courses), pd.DataFrame(outcomes))


def postings(n=4000):
    companies = [f"Company {c}" for c in "ABCDEFGHIJKLMNOPQRST"]
    countries = ["TH", "US", "GB", "SG", "DE", "IN"]
    cw = [0.08, 0.35, 0.12, 0.1, 0.12, 0.23]
    cmult = {"TH": 0.35, "US": 1.0, "GB": 0.75, "SG": 0.7, "DE": 0.8, "IN": 0.3}
    lvl_base = {"เริ่มต้น": 55000, "ปานกลาง": 95000, "เชี่ยวชาญ": 150000}
    rows = []
    for i in range(n):
        field = RNG.choice(["AI", "DS", "STAT"], p=[0.3, 0.5, 0.2])
        level = RNG.choice(list(lvl_base), p=[0.35, 0.4, 0.25])
        country = RNG.choice(countries, p=cw)
        pool = list(SKILLS[field])
        if level != "เริ่มต้น":
            pool += ["Cloud", "Docker", "Spark", "Airflow"]
        if level == "เชี่ยวชาญ":
            pool += ["MLOps", "MLOps", "Cloud"]
        k = int(RNG.integers(4, 9))
        skills = sorted(set(RNG.choice(pool, size=k)))
        sal = lvl_base[level] * cmult[country] * RNG.lognormal(0, 0.2)
        rows.append(dict(posting_id=f"J{i:05d}", title=f"{field} {level}", company=RNG.choice(companies),
                         country=country, field=field, level=level, year=int(RNG.choice([2022, 2023, 2024, 2025], p=[.15, .25, .3, .3])),
                         salary_usd=round(float(sal), 0), skills="|".join(skills)))
    return pd.DataFrame(rows)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    prog, grad, courses, outcomes = programs_and_children()
    for name, df in [("programs", prog), ("graduates", grad), ("courses", courses),
                     ("outcomes", outcomes), ("postings", postings())]:
        df.to_csv(OUT / f"{name}.csv", index=False)
        print(f"{name}: {len(df)} rows")


if __name__ == "__main__":
    main()
