"""Tab 3 – skill mismatch between what is taught (Tab 1) and what is demanded (Tab 2)."""
import pandas as pd
import plotly.graph_objects as go
from dash import Input, Output, html

from .. import data, filters, metrics
from ..config import ALL_SKILLS, LEVELS, SKILL_TO_CATEGORY
from ..ui import COLORWAY, DIM, HIGHLIGHT, card, empty, graph, kpis, style

FIG_NAMES = ["t3-gap", "t3-heat", "t3-quad", "t3-programs"]
QUAD_COLORS = {"ขาดแคลน": "#c0392b", "สมดุล": "#3a9d6e", "ผลิตเกิน": "#2a5d9f", "ความต้องการต่ำ": "#aab0b8"}


def layout():
    return html.Div([
        html.Div(id="t3-kpis"),
        html.Div([
            card("Supply vs Demand ต่อทักษะ", graph("t3-gap", 440),
                 "Demand = % ประกาศที่ต้องการ · Supply = % บัณฑิตที่หลักสูตรมีวิชาบังคับในทักษะนั้น · คลิกเพื่อเลือกทักษะ"),
            card("Gap (Demand − Supply) ทักษะ × ระดับงาน", graph("t3-heat", 440), "แดง = ขาดแคลน · น้ำเงิน = ผลิตเกิน"),
            card("Quadrant: ความครอบคลุมในหลักสูตร vs ความต้องการตลาด", graph("t3-quad"), "เส้นแบ่ง = ค่ามัธยฐาน"),
            card("Mismatch score รายหลักสูตร", graph("t3-programs"),
                 "สัดส่วนความต้องการตลาดที่หลักสูตรไม่ครอบคลุม (0 = ครอบคลุมหมด) · คลิกเพื่อเลือกหลักสูตร"),
        ], className="grid2"),
        html.Div(id="t3-table", className="card"),
    ])


def build(d: data.Data, fields, years, countries, sel):
    pfields = list(fields)
    efields = filters.effective_fields(d.programs, fields, sel)
    p_sup = filters.select_programs(d.programs, d.courses, pfields, sel, exclude=("skill",))
    g_sup = d.graduates[d.graduates.year.between(*years)]
    p_all = filters.select_programs(d.programs, d.courses, pfields, sel, exclude=("skill", "program"))

    def posts(exclude=()):
        return filters.select_postings(d.postings, d.posting_skills, efields, years, countries, sel, exclude)

    demand_posts = posts(("skill",))
    D = metrics.demand_share(demand_posts, d.posting_skills, ALL_SKILLS)
    S = metrics.supply_coverage(p_sup.program_id, g_sup, d.courses, ALL_SKILLS)
    gt = metrics.gap_table(D, S)
    sk = sel.get("skill")

    if demand_posts.empty or p_sup.empty:
        empty_f = empty("ไม่มีข้อมูลตามตัวกรอง (ประกาศงานหรือหลักสูตรว่าง)")
        return kpis([("หลักสูตรที่เลือก", str(len(p_sup))), ("ประกาศ", str(len(demand_posts)))]), [empty_f] * 4, html.Div("—")

    # C1 diverging: demand vs supply per skill, sorted by gap
    g = gt.sort_values("gap")
    f1 = go.Figure()
    hl = dict(color="#000", width=[3 if x == sk else 0 for x in g.skill])
    f1.add_bar(y=g.skill, x=g.demand * 100, orientation="h", name="Demand (ตลาด)", marker=dict(color=COLORWAY[1], line=hl))
    f1.add_bar(y=g.skill, x=-g.supply * 100, orientation="h", name="Supply (หลักสูตร)", marker=dict(color=COLORWAY[0], line=hl),
               customdata=(g.supply * 100).round(1), hovertemplate="%{y}: supply %{customdata}%<extra></extra>")
    f1.update_layout(barmode="relative", xaxis=dict(title="← Supply %   |   Demand % →", tickformat="~s"), yaxis=dict(dtick=1))
    style(f1)

    # C2 heatmap gap by level
    z = pd.DataFrame({lv: metrics.demand_share(
        filters.select_postings(d.postings, d.posting_skills, efields, years, countries, {**sel, "level": lv}, ("skill",)),
        d.posting_skills, ALL_SKILLS) - S for lv in LEVELS})
    order = list(g.skill)
    f2 = go.Figure(go.Heatmap(z=z.loc[order].values, x=LEVELS, y=order, zmid=0, colorscale="RdBu_r",
                              colorbar=dict(title="gap", tickformat=".0%"),
                              hovertemplate="%{y} / %{x}: gap %{z:.1%}<extra></extra>"))
    f2.update_yaxes(dtick=1)
    style(f2)

    # C3 quadrant
    d_cut, s_cut = gt.demand.median(), gt.supply.median()
    gt["quadrant"] = gt.apply(metrics.quadrant, axis=1, d_cut=d_cut, s_cut=s_cut)
    f3 = go.Figure()
    for qn, sub in gt.groupby("quadrant"):
        f3.add_scatter(x=sub.supply * 100, y=sub.demand * 100, mode="markers+text", text=sub.skill, textposition="top center",
                       name=qn, customdata=sub[["skill"]].values, marker=dict(size=[16 if s == sk else 10 for s in sub.skill],
                       color=QUAD_COLORS[qn], line=dict(width=[3 if s == sk else 0 for s in sub.skill], color="#000")))
    f3.add_vline(x=s_cut * 100, line_dash="dot", line_color=DIM)
    f3.add_hline(y=d_cut * 100, line_dash="dot", line_color=DIM)
    f3.update_layout(xaxis_title="Supply % (ครอบคลุมในหลักสูตร)", yaxis_title="Demand % (ตลาดต้องการ)")
    style(f3)

    # C4 program mismatch (all programs in field filter; selected highlighted)
    mm = metrics.program_mismatch(D, d.courses, p_all.program_id).sort_values()
    names = p_all.set_index("program_id").program_name
    f4 = go.Figure(go.Bar(y=[names[i] for i in mm.index], x=mm.values, orientation="h", customdata=[[i] for i in mm.index],
                          marker_color=[HIGHLIGHT if i == sel.get("program") else (COLORWAY[0] if not sel.get("program") else DIM) for i in mm.index],
                          hovertemplate="%{y}<br>mismatch %{x:.1%}<extra></extra>"))
    f4.update_xaxes(tickformat=".0%")
    f4.update_yaxes(showticklabels=False)
    style(f4)

    # table: top shortages with related courses
    top = gt.sort_values("gap", ascending=False).head(8)
    cc = d.courses[d.courses.program_id.isin(p_sup.program_id)]
    npost = d.posting_skills[d.posting_skills.posting_id.isin(demand_posts.posting_id)].drop_duplicates().groupby("skill").size()
    rows = []
    for _, r in top.iterrows():
        rel = cc[cc.skill == r.skill].course.drop_duplicates().head(3).tolist()
        rows.append(html.Tr([html.Td(r.skill), html.Td(f"{r.demand:.0%}"), html.Td(f"{r.supply:.0%}"), html.Td(f"{r.gap:+.0%}"),
                             html.Td(int(npost.get(r.skill, 0))), html.Td(", ".join(rel) if rel else "— ไม่มีวิชาบังคับ")]))
    table = html.Div([html.H4("ทักษะที่ขาดแคลนสูงสุด และวิชาที่เกี่ยวข้อง"),
                      html.Table([html.Thead(html.Tr([html.Th(h) for h in ["ทักษะ", "Demand", "Supply", "Gap", "# ประกาศ", "วิชาที่เกี่ยวข้อง (ตัวอย่าง)"]])),
                                  html.Tbody(rows)])])

    worst = gt.sort_values("gap", ascending=False).iloc[0]
    k = kpis([("หลักสูตรที่เลือก", str(len(p_sup))), ("ประกาศที่เทียบ", f"{len(demand_posts):,}"),
              ("ทักษะขาดแคลนสุด", worst.skill), ("Mismatch เฉลี่ย", f"{mm.mean():.0%}" if len(mm) else "n/a")])
    return k, [f1, f2, f3, f4], table


def register(app, common_inputs):
    outs = [Output("t3-kpis", "children")] + [Output({"type": "g", "name": n}, "figure") for n in FIG_NAMES] + [Output("t3-table", "children")]

    @app.callback(*outs, *common_inputs)
    def _update(fields, years, countries, sel):
        k, figs, table = build(data.load(), fields or [], years, countries or [], sel or {})
        return (k, *figs, table)
