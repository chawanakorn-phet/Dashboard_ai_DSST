"""Cross-filter logic. Pure functions so they are unit-testable.

`sel` is the click-selection state shared by all tabs: keys program, skill, level, company.
`exclude` lets a chart ignore its own selection so the other options stay visible (and get highlighted).
"""
import pandas as pd

SEL_KEYS = ("program", "skill", "level", "company")


def _on(sel, key, exclude):
    return sel.get(key) if key not in exclude else None


def select_programs(programs: pd.DataFrame, courses: pd.DataFrame, fields, sel, exclude=()) -> pd.DataFrame:
    p = programs[programs.field.isin(fields)] if fields else programs.iloc[0:0]
    skill = _on(sel, "skill", exclude)
    if skill:
        p = p[p.program_id.isin(courses.loc[courses.skill == skill, "program_id"])]
    prog = _on(sel, "program", exclude)
    if prog:
        p = p[p.program_id == prog]
    return p


def select_postings(postings: pd.DataFrame, posting_skills: pd.DataFrame, fields, years, countries, sel,
                    exclude=()) -> pd.DataFrame:
    d = postings[postings.field.isin(fields) & postings.year.between(*years) & postings.country.isin(countries)]
    for key, col in (("level", "level"), ("company", "company")):
        v = _on(sel, key, exclude)
        if v:
            d = d[d[col] == v]
    skill = _on(sel, "skill", exclude)
    if skill:
        d = d[d.posting_id.isin(posting_skills.loc[posting_skills.skill == skill, "posting_id"])]
    return d


def effective_fields(programs: pd.DataFrame, fields, sel) -> list:
    """A selected program narrows the job market to that program's field."""
    prog = sel.get("program")
    if not prog:
        return list(fields)
    pf = programs.loc[programs.program_id == prog, "field"].tolist()
    return [f for f in fields if f in pf]


def describe(sel: dict) -> list[str]:
    labels = {"program": "หลักสูตร", "skill": "ทักษะ", "level": "ระดับ", "company": "บริษัท"}
    return [f"{labels[k]}: {sel[k]}" for k in SEL_KEYS if sel.get(k)]
