"""Tab 1 – graduates and the skills they were taught (BQ1)."""
import plotly.graph_objects as go
from dash import Input, Output

from .. import data, filters
from ..config import MIN_N
from ..ui import HIGHLIGHT, DIM, card, colors_for, empty, graph, kpis, style

FIG_NAMES = ["t1-programs", "t1-skills", "t1-outcomes", "t1-tuition"]


def layout():
    from dash import html
    return html.Div([
        html.Div(id="t1-kpis"),
        html.Div([
            card("หลักสูตรที่ผลิตบัณฑิตสาย AI/DS/Stat และจำนวนต่อปี", graph("t1-programs"), "คลิกแท่งเพื่อเลือกหลักสูตร"),
            card("รายวิชาบังคับ จัดกลุ่มตามทักษะ (หน่วยกิต)", graph("t1-skills"), "คลิกทักษะเพื่อกรองหลักสูตรที่สอนทักษะนั้น"),
            card("บัณฑิตมีงานทำ ปีที่ 1 / 2 / 3 หลังจบ", graph("t1-outcomes"),
                 f"แสดงเมื่อ n ≥ {MIN_N} เท่านั้น"),
            card("ค่าเทอมตลอดหลักสูตร (บาท)", graph("t1-tuition"), "คลิกแท่งเพื่อเลือกหลักสูตร"),
        ], className="grid2"),
    ])


def build(d: data.Data, fields, years, sel):
    """Return (kpi component, [4 figures]) for the given global filters + selection."""
    # charts that *offer* the selection (program) use the set without it, and highlight the chosen one
    p_all = filters.select_programs(d.programs, d.courses, fields, sel, exclude=("program",))
    p_sel = filters.select_programs(d.programs, d.courses, fields, sel)
    g_all = d.graduates[d.graduates.program_id.isin(p_all.program_id) & d.graduates.year.between(*years)]
    sel_prog = sel.get("program")

    # C1 graduates per year per program
    if g_all.empty:
        f1 = empty()
    else:
        f1 = go.Figure()
        for _, p in p_all.iterrows():
            g = g_all[g_all.program_id == p.program_id].sort_values("year")
            if g.empty:
                continue
            dim = sel_prog and p.program_id != sel_prog
            f1.add_bar(x=g.year, y=g["count"], name=p.program_name, customdata=[[p.program_id]] * len(g),
                       marker_color=DIM if dim else None, opacity=1,
                       marker_line=dict(color=HIGHLIGHT, width=2) if sel_prog == p.program_id else None,
                       hovertemplate=f"{p.program_name}<br>%{{x}}: %{{y}} คน<extra></extra>")
        f1.update_layout(barmode="stack", showlegend=False, xaxis=dict(dtick=1), yaxis_title="จำนวนบัณฑิต")
        style(f1)

    # C2 required-course credits by skill (programs after all filters except skill → so skill options stay visible)
    p_for_skills = filters.select_programs(d.programs, d.courses, fields, sel, exclude=("skill",))
    c = d.courses[d.courses.program_id.isin(p_for_skills.program_id)]
    if c.empty:
        f2 = empty()
    else:
        s = c.groupby("skill").credits.sum().sort_values()
        f2 = go.Figure(go.Bar(y=s.index, x=s.values, orientation="h",
                              marker_color=colors_for(list(s.index), sel.get("skill")),
                              hovertemplate="%{y}: %{x} หน่วยกิต<extra></extra>"))
        f2.update_layout(xaxis_title="หน่วยกิตรวม (ทุกหลักสูตรที่เลือก)", yaxis=dict(dtick=1))
        style(f2)

    # C3 employment after 1/2/3 years (pooled over selected programs and cohorts)
    o = d.outcomes[d.outcomes.program_id.isin(p_sel.program_id)]
    agg = o.groupby("years_after")[["n_total", "n_employed", "n_in_field"]].sum()
    agg = agg[agg.n_total >= MIN_N]
    if agg.empty:
        f3 = empty(f"ข้อมูลน้อยกว่า {MIN_N} ราย")
    else:
        f3 = go.Figure()
        f3.add_bar(x=[f"ปีที่ {i}" for i in agg.index], y=agg.n_employed / agg.n_total * 100, name="มีงานทำ",
                   text=(agg.n_employed / agg.n_total * 100).round(1).astype(str) + "%")
        f3.add_bar(x=[f"ปีที่ {i}" for i in agg.index], y=agg.n_in_field / agg.n_total * 100, name="งานตรงสาย",
                   text=(agg.n_in_field / agg.n_total * 100).round(1).astype(str) + "%")
        f3.update_layout(barmode="group", yaxis=dict(title="% ของบัณฑิต", range=[0, 100]))
        style(f3)

    # C4 tuition
    if p_all.empty:
        f4 = empty()
    else:
        t = p_all.sort_values("tuition_total")
        f4 = go.Figure(go.Bar(y=t.program_name, x=t.tuition_total, orientation="h", customdata=t[["program_id"]].values,
                              marker_color=colors_for(list(t.program_id), sel_prog),
                              hovertemplate="%{y}<br>%{x:,.0f} บาท<extra></extra>"))
        f4.update_yaxes(showticklabels=False)
        style(f4)

    n_grad = int(g_all[g_all.program_id.isin(p_sel.program_id)]["count"].sum())
    emp1 = o[o.years_after == 1]
    r1 = f"{emp1.n_employed.sum() / emp1.n_total.sum() * 100:.0f}%" if emp1.n_total.sum() >= MIN_N else "n/a"
    med_t = f"{p_sel.tuition_total.median():,.0f}" if len(p_sel) else "n/a"
    k = kpis([("หลักสูตร", str(len(p_sel))), ("บัณฑิตรวม (ช่วงปีที่เลือก)", f"{n_grad:,}"),
              ("มีงานทำภายใน 1 ปี", r1), ("ค่าเทอมตลอดหลักสูตร (มัธยฐาน, บาท)", med_t)])
    return k, [f1, f2, f3, f4]


def register(app, common_inputs):
    outs = [Output("t1-kpis", "children")] + [Output({"type": "g", "name": n}, "figure") for n in FIG_NAMES]

    @app.callback(*outs, *common_inputs)
    def _update(fields, years, countries, sel):
        k, figs = build(data.load(), fields or [], years, sel or {})
        return (k, *figs)
