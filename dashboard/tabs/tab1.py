"""Tab 1 – graduates and the skills they were taught (BQ1)."""
import pandas as pd
import plotly.graph_objects as go
from dash import Input, Output, html

from .. import data, filters
from ..config import MIN_N
from ..ui import DIM, HIGHLIGHT, card, colors_for, empty, graph, kpis, style

FIG_NAMES = ["t1-programs", "t1-skills", "t1-outcomes", "t1-tuition"]
TOP_N = 15


def layout():
    return html.Div([
        html.Div(id="t1-kpis"),
        html.Div([
            card(f"หลักสูตรที่ผลิตบัณฑิตมากที่สุด Top {TOP_N} และจำนวนต่อปี", graph("t1-programs"),
                 "คลิกแท่งเพื่อเลือกหลักสูตร · สีเทา = หลักสูตรที่เหลือรวมกัน"),
            card("รายวิชาบังคับ จัดกลุ่มตามทักษะ (หน่วยกิต)", graph("t1-skills"),
                 "มีข้อมูลรายวิชาเฉพาะหลักสูตรที่รวบรวมไว้ (ดู STATUS.md) · คลิกทักษะเพื่อกรองหลักสูตรที่สอนทักษะนั้น"),
            card("บัณฑิตที่มีงานทำ (มีรายได้) และรายได้มัธยฐาน หลังจบ 1 / 3 / 4 / 5 ปี", graph("t1-outcomes"),
                 f"College Scorecard ระดับสาขา (DS, Statistics; ไม่มี AI แยก) · 'มีงานทำ' = มีรายได้และไม่ได้เรียนต่อ · ชุดนี้ไม่มีปีที่ 2 · แสดงเมื่อ n ≥ {MIN_N}"),
            card(f"ค่าเล่าเรียนตลอดหลักสูตร (USD, in-state) Top {TOP_N}", graph("t1-tuition"),
                 "ประมาณจากค่าเล่าเรียน+ค่าธรรมเนียมต่อปี × จำนวนปีของหลักสูตร (IPEDS 2023-24) · คลิกแท่งเพื่อเลือกหลักสูตร"),
        ], className="grid2"),
    ])


def _top(p: pd.DataFrame, g: pd.DataFrame, keep=None, n=TOP_N) -> list:
    tot = g.groupby("program_id")["count"].sum().sort_values(ascending=False)
    allowed = set(p.program_id)
    ids = tot.index[tot.index.isin(allowed)][:n].tolist()
    if keep and keep in allowed and keep not in ids:
        ids.append(keep)
    return ids


def build(d: data.Data, fields, years, sel):
    """Return (kpi component, [4 figures]) for the given global filters + selection."""
    # charts that *offer* the selection (program) use the set without it, and highlight the chosen one
    p_all = filters.select_programs(d.programs, d.courses, fields, sel, exclude=("program",))
    p_sel = filters.select_programs(d.programs, d.courses, fields, sel)
    g_all = d.graduates[d.graduates.program_id.isin(p_all.program_id) & d.graduates.year.between(*years)]
    sel_prog = sel.get("program")
    names = p_all.set_index("program_id").program_name

    # C1 graduates per year: top programs + "others"
    if g_all.empty:
        f1 = empty()
    else:
        top = _top(p_all, g_all, sel_prog)
        f1 = go.Figure()
        rest = g_all[~g_all.program_id.isin(top)].groupby("year")["count"].sum()
        if len(rest):
            f1.add_bar(x=rest.index, y=rest.values, name=f"อื่นๆ ({g_all[~g_all.program_id.isin(top)].program_id.nunique()} หลักสูตร)",
                       marker_color="#e3e6ea", hovertemplate="อื่นๆ<br>%{x}: %{y:,} คน<extra></extra>")
        for pid in reversed(top):
            g = g_all[g_all.program_id == pid].sort_values("year")
            dim = sel_prog and pid != sel_prog
            f1.add_bar(x=g.year, y=g["count"], name=names[pid], customdata=[[pid]] * len(g),
                       marker_color=DIM if dim else None,
                       marker_line=dict(color=HIGHLIGHT, width=2) if sel_prog == pid else None,
                       hovertemplate=f"{names[pid]}<br>%{{x}}: %{{y:,}} คน<extra></extra>")
        f1.update_layout(barmode="stack", showlegend=False, xaxis=dict(dtick=1), yaxis_title="จำนวนบัณฑิต (ทุกระดับที่เลือก)")
        style(f1)

    # C2 required-course credits by skill (all filters except skill, so every skill stays clickable)
    p_for_skills = filters.select_programs(d.programs, d.courses, fields, sel, exclude=("skill",))
    c = d.courses[d.courses.program_id.isin(p_for_skills.program_id)]
    if c.empty:
        f2 = empty("ไม่มีข้อมูลรายวิชาสำหรับหลักสูตรที่เลือก")
    else:
        s = c.groupby("skill").credits.sum().sort_values()
        f2 = go.Figure(go.Bar(y=s.index, x=s.values, orientation="h",
                              marker_color=colors_for(list(s.index), sel.get("skill")),
                              hovertemplate="%{y}: %{x} หน่วยกิต<extra></extra>"))
        f2.update_layout(xaxis_title=f"หน่วยกิตรวม ({c.program_id.nunique()} หลักสูตรที่มีข้อมูลรายวิชา)", yaxis=dict(dtick=1))
        style(f2)

    # C3 earnings + number of graduates with earnings, 1/3/4/5 years after completion (pooled)
    o = d.outcomes[d.outcomes.program_id.isin(p_sel.program_id)]
    o2 = o.assign(w=o.n_employed.where(o.median_earnings.notna(), 0), we=o.median_earnings.fillna(0) * o.n_employed)
    agg = o2.groupby("years_after").agg(n=("n_employed", "sum"), we=("we", "sum"), w=("w", "sum"))
    agg["earn"] = agg.we / agg.w.where(agg.w > 0)  # employer-count-weighted mean of program medians
    agg = agg[agg.n >= MIN_N]
    if agg.empty:
        f3 = empty(f"ไม่มีข้อมูลผลลัพธ์ (n < {MIN_N}) — Scorecard ไม่มีรหัสแยกสาย AI และไม่ครอบคลุมหลักสูตรใหม่")
    else:
        x = [f"ปีที่ {i}" for i in agg.index]
        f3 = go.Figure()
        f3.add_bar(x=x, y=agg.earn, name="รายได้มัธยฐาน (USD)", marker_color="#2a5d9f", text=agg.earn.round(-2).map("${:,.0f}".format))
        f3.add_scatter(x=x, y=agg.n, name="# บัณฑิตที่มีรายได้", yaxis="y2", mode="lines+markers", line_color="#e07b39")
        f3.update_layout(yaxis=dict(title="รายได้มัธยฐาน (USD)", rangemode="tozero"),
                         yaxis2=dict(title="# บัณฑิตที่มีรายได้", overlaying="y", side="right", rangemode="tozero"))
        style(f3)

    # C4 tuition (top programs by graduates, with tuition data)
    pt = p_all.dropna(subset=["tuition_total"])
    if pt.empty:
        f4 = empty()
    else:
        top = _top(pt, g_all, sel_prog)
        t = pt[pt.program_id.isin(top)].sort_values("tuition_total")
        f4 = go.Figure(go.Bar(y=t.program_name, x=t.tuition_total, orientation="h", customdata=t[["program_id"]].values,
                              marker_color=colors_for(list(t.program_id), sel_prog),
                              hovertemplate="%{y}<br>%{x:,.0f} USD<extra></extra>"))
        f4.update_yaxes(showticklabels=False)
        f4.update_layout(xaxis_title="USD")
        style(f4)

    n_grad = int(g_all[g_all.program_id.isin(p_sel.program_id)]["count"].sum())
    e1 = o[o.years_after == 1]
    r1 = f"{int(e1.n_employed.sum()):,}" if e1.n_employed.sum() >= MIN_N else "n/a"
    med_t = f"${p_sel.tuition_total.median():,.0f}" if p_sel.tuition_total.notna().any() else "n/a"
    k = kpis([("หลักสูตร", f"{len(p_sel):,}"), ("บัณฑิตรวม (ช่วงปีที่เลือก)", f"{n_grad:,}"),
              ("บัณฑิตที่มีรายได้ภายใน 1 ปี (คน, Scorecard)", r1), ("ค่าเล่าเรียนตลอดหลักสูตร (มัธยฐาน)", med_t)])
    return k, [f1, f2, f3, f4]


def register(app, common_inputs):
    outs = [Output("t1-kpis", "children")] + [Output({"type": "g", "name": n}, "figure") for n in FIG_NAMES]

    @app.callback(*outs, *common_inputs)
    def _update(fields, years, countries, sel):
        k, figs = build(data.load(), fields or [], years, sel or {})
        return (k, *figs)
