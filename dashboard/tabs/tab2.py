"""Tab 2 – jobs demanded and the skills they require (BQ2)."""
import plotly.graph_objects as go
from dash import Input, Output, html

from .. import data, filters
from ..config import LEVELS
from ..ui import card, colors_for, empty, graph, kpis, style

FIG_NAMES = ["t2-postings", "t2-skills", "t2-companies", "t2-salary"]
TOP_N = 15


def layout():
    return html.Div([
        html.Div(id="t2-kpis"),
        html.Div([
            card("ปริมาณตำแหน่งว่าง (ประกาศงาน) รายเดือน ปี 2023", graph("t2-postings"), "snapshot ปี 2023 · นับจากประกาศงาน ไม่ใช่จำนวนที่จ้างจริง · ไม่ผูกกับตัวกรองช่วงปี"),
            card(f"ทักษะที่ต้องการ Top {TOP_N} (% ของประกาศ)", graph("t2-skills"), "คลิกทักษะเพื่อกรอง"),
            card(f"บริษัทที่รับ Top {TOP_N} (จำนวนประกาศ)", graph("t2-companies"), "คลิกบริษัทเพื่อกรอง"),
            card("เงินเดือนตามระดับงาน (USD/ปี)", graph("t2-salary"), "เฉพาะประกาศที่ระบุเงินเดือน (ส่วนใหญ่สหรัฐฯ) · ระดับจัดจากชื่อตำแหน่ง · คลิก box เพื่อเลือกระดับ"),
        ], className="grid2"),
    ])


def build(d: data.Data, fields, years, countries, sel):
    years = (0, 9999)  # postings are a single-year snapshot; the year slider applies to graduates only
    fields = filters.effective_fields(d.programs, fields, sel)

    def posts(exclude=()):
        return filters.select_postings(d.postings, d.posting_skills, fields, years, countries, sel, exclude)

    # C1 volume per year by level (ignores level selection so the split stays visible)
    p = posts(("level",))
    if p.empty:
        f1 = empty()
    else:
        g = p.groupby(["month", "level"]).size().unstack(fill_value=0).reindex(columns=LEVELS, fill_value=0)
        f1 = go.Figure()
        for lv in LEVELS:
            op = 1 if not sel.get("level") or sel["level"] == lv else 0.25
            f1.add_bar(x=g.index, y=g[lv], name=lv, opacity=op)
        f1.update_layout(barmode="stack", xaxis=dict(dtick=1, title="เดือน (2023)"), yaxis_title="จำนวนประกาศ")
        style(f1)

    # C2 top skills (ignores skill selection so other skills stay clickable)
    p = posts(("skill",))
    ps = d.posting_skills[d.posting_skills.posting_id.isin(p.posting_id)]
    if p.empty or ps.empty:
        f2 = empty()
    else:
        s = (ps.groupby("skill", observed=True).size() / len(p) * 100).sort_values().tail(TOP_N)
        f2 = go.Figure(go.Bar(y=s.index, x=s.values, orientation="h", marker_color=colors_for(list(s.index), sel.get("skill")),
                              hovertemplate="%{y}: %{x:.1f}% ของประกาศ<extra></extra>"))
        f2.update_layout(xaxis_title="% ของประกาศ", yaxis=dict(dtick=1))
        style(f2)

    # C3 companies
    p = posts(("company",))
    if p.empty:
        f3 = empty()
    else:
        c = p.company.value_counts().head(TOP_N).sort_values()
        f3 = go.Figure(go.Bar(y=c.index, x=c.values, orientation="h", marker_color=colors_for(list(c.index), sel.get("company"))))
        f3.update_layout(xaxis_title="จำนวนประกาศ", yaxis=dict(dtick=1))
        style(f3)

    # C4 salary by level
    p = posts(("level",))
    if p.empty:
        f4 = empty()
    else:
        f4 = go.Figure()
        for lv in LEVELS:
            s = p[p.level == lv].salary_usd
            if len(s):
                dim = sel.get("level") and sel["level"] != lv
                f4.add_trace(go.Box(y=s, x=[lv] * len(s), name=lv, opacity=0.35 if dim else 1, boxpoints=False))
        f4.update_layout(showlegend=False, yaxis_title="USD / ปี")
        style(f4)

    cur = posts()
    start = cur[cur.level == "เริ่มต้น"].salary_usd
    top_skill = "—"
    ps = d.posting_skills[d.posting_skills.posting_id.isin(cur.posting_id)]
    if len(ps):
        top_skill = ps.skill.value_counts().idxmax()
    k = kpis([("ตำแหน่ง/ประกาศ", f"{len(cur):,}"), ("เงินเดือนมัธยฐานระดับเริ่มต้น (USD)", f"{start.median():,.0f}" if len(start) else "n/a"),
              ("จำนวนบริษัท", str(cur.company.nunique())), ("ทักษะอันดับ 1", top_skill)])
    return k, [f1, f2, f3, f4]


def register(app, common_inputs):
    outs = [Output("t2-kpis", "children")] + [Output({"type": "g", "name": n}, "figure") for n in FIG_NAMES]

    @app.callback(*outs, *common_inputs)
    def _update(fields, years, countries, sel):
        k, figs = build(data.load(), fields or [], years, countries or [], sel or {})
        return (k, *figs)
