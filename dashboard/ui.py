"""Shared UI helpers: graph ids, KPI cards, empty figures, click -> selection mapping."""
import plotly.graph_objects as go
from dash import dcc, html

COLORWAY = ["#2a5d9f", "#e07b39", "#3a9d6e", "#9b59b6", "#c0392b", "#16a2b8", "#8d6e63", "#7f8c8d",
            "#d4a017", "#5c6bc0", "#26a69a", "#ec407a"]
DIM = "#c9ced6"
HIGHLIGHT = "#e07b39"

# graph name -> (selection key, how to read the value from a Plotly clickData point)
_cd = lambda p: (p.get("customdata") or [None])[0]  # noqa: E731
_y = lambda p: p.get("y")  # noqa: E731
_x = lambda p: p.get("x")  # noqa: E731
CLICK_MAP = {
    "t1-programs": ("program", _cd),
    "t1-skills": ("skill", _y),
    "t1-tuition": ("program", _cd),
    "t2-skills": ("skill", _y),
    "t2-companies": ("company", _y),
    "t2-salary": ("level", _x),
    "t3-gap": ("skill", _y),
    "t3-quad": ("skill", _cd),
    "t3-heat": ("skill", _y),
    "t3-programs": ("program", _cd),
}


def graph(name: str, height: int = 340):
    return dcc.Graph(id={"type": "g", "name": name}, style={"height": f"{height}px"},
                     config={"displaylogo": False, "toImageButtonOptions": {"filename": name}})


def card(title: str, child, note: str | None = None):
    kids = [html.H4(title), child]
    if note:
        kids.append(html.Div(note, className="note"))
    return html.Div(kids, className="card")


def kpis(items):
    return html.Div([html.Div([html.Div(v, className="kv"), html.Div(k, className="kk")], className="kpi")
                     for k, v in items], className="kpis")


def style(fig: go.Figure, title: str | None = None, **kw) -> go.Figure:
    fig.update_layout(template="plotly_white", colorway=COLORWAY, margin=dict(l=10, r=10, t=30, b=10),
                      font=dict(family="system-ui, 'Noto Sans Thai', sans-serif", size=12),
                      legend=dict(orientation="h", y=-0.2), title=dict(text=title, x=0, font_size=13), **kw)
    return fig


def empty(msg="ไม่มีข้อมูลตามตัวกรองที่เลือก") -> go.Figure:
    fig = go.Figure()
    fig.add_annotation(text=msg, showarrow=False, font=dict(size=14, color="#888"))
    fig.update_xaxes(visible=False)
    fig.update_yaxes(visible=False)
    return style(fig)


def colors_for(values, selected):
    """Dim everything except the selected value (if any)."""
    if not selected:
        return [COLORWAY[0]] * len(values)
    return [HIGHLIGHT if v == selected else DIM for v in values]
