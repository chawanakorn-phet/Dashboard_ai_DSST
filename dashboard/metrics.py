"""Skill-mismatch metrics (BRD §5.4). posting_skills must hold unique (posting_id, skill) pairs.

D(s)  demand share   = postings requiring s / postings in filter
S(s)  supply coverage= graduates of programs that require a course mapped to s / graduates in filter
Gap   = D - S        (+ shortage, - oversupply)
Mismatch(p) = sum_s D(s)*(1-covered(p,s)) / sum_s D(s)
"""
import pandas as pd


def demand_share(postings: pd.DataFrame, posting_skills: pd.DataFrame, skills) -> pd.Series:
    n = postings.posting_id.nunique()
    if n == 0:
        return pd.Series(0.0, index=list(skills))
    ps = posting_skills[posting_skills.posting_id.isin(postings.posting_id)]  # (posting_id, skill) pairs are unique
    return (ps.groupby("skill", observed=True).posting_id.size() / n).reindex(list(skills), fill_value=0.0)


def supply_coverage(program_ids, graduates: pd.DataFrame, courses: pd.DataFrame, skills) -> pd.Series:
    ids = list(program_ids)
    if not ids:
        return pd.Series(0.0, index=list(skills))
    w = graduates[graduates.program_id.isin(ids)].groupby("program_id")["count"].sum().reindex(ids, fill_value=0)
    if w.sum() == 0:
        w = pd.Series(1.0, index=ids)  # fall back to equal weights when no graduate counts
    cov = courses[courses.program_id.isin(ids)][["program_id", "skill"]].drop_duplicates()
    cov = cov.assign(w=cov.program_id.map(w))
    return (cov.groupby("skill").w.sum() / w.sum()).reindex(list(skills), fill_value=0.0)


def gap_table(demand: pd.Series, supply: pd.Series) -> pd.DataFrame:
    df = pd.DataFrame({"demand": demand, "supply": supply})
    df["gap"] = df.demand - df.supply
    return df.rename_axis("skill").reset_index()


def program_mismatch(demand: pd.Series, courses: pd.DataFrame, program_ids) -> pd.Series:
    total = demand.sum()
    out = {}
    for pid in program_ids:
        covered = set(courses.loc[courses.program_id == pid, "skill"])
        missing = demand[~demand.index.isin(covered)].sum()
        out[pid] = missing / total if total else 0.0
    return pd.Series(out, dtype=float)


def quadrant(row, d_cut: float, s_cut: float) -> str:
    hi_d, hi_s = row.demand >= d_cut, row.supply >= s_cut
    if hi_d and not hi_s:
        return "ขาดแคลน"
    if hi_d and hi_s:
        return "สมดุล"
    if not hi_d and hi_s:
        return "ผลิตเกิน"
    return "ความต้องการต่ำ"
