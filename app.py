"""Dash entrypoint: header filters, shared click-selection store, 3 tabs."""
from dash import ALL, Dash, Input, Output, State, ctx, dcc, html

from dashboard import data
from dashboard.config import FIELDS, REAL_NOTE, SAMPLE_BANNER
from dashboard.filters import SEL_KEYS, describe
from dashboard.tabs import tab1, tab2, tab3
from dashboard.ui import CLICK_MAP

app = Dash(__name__, suppress_callback_exceptions=True, title="AI/DS/Stat Workforce Dashboard")
server = app.server

d = data.load()
countries = d.postings.country.value_counts().index.tolist()
y_lo, y_hi = int(d.graduates.year.min()), int(d.graduates.year.max())

app.layout = html.Div([
    html.H2("Dashboard: อุปทาน–อุปสงค์กำลังคน AI / Data Science / Statistics"),
    html.Div(SAMPLE_BANNER if data.IS_SAMPLE else REAL_NOTE, className="banner" if data.IS_SAMPLE else "note-bar"),
    html.Div([
        html.Div([html.Label("สาย"), dcc.Dropdown(id="f-field", multi=True, options=[{"label": v, "value": k} for k, v in FIELDS.items()],
                                                  value=list(FIELDS), clearable=False)], className="fcol"),
        html.Div([html.Label("ช่วงปี"), dcc.RangeSlider(id="f-years", min=y_lo, max=y_hi, step=1, value=[y_lo, y_hi],
                                                       marks={y: str(y) for y in range(y_lo, y_hi + 1)})], className="fcol wide"),
        html.Div([html.Label("ประเทศ (ตลาดงาน)"), dcc.Dropdown(id="f-country", multi=True, options=countries, value=countries,
                                                              clearable=False)], className="fcol"),
    ], className="filters"),
    html.Div([html.Span(id="chips"), html.Button("ล้างการเลือก", id="reset", n_clicks=0)], className="chiprow"),
    dcc.Tabs(id="tabs", value="t1", children=[
        dcc.Tab(label="1 บัณฑิตและทักษะที่เรียน", value="t1"),
        dcc.Tab(label="2 ตลาดงานและทักษะที่ต้องการ", value="t2"),
        dcc.Tab(label="3 Skill Mismatch", value="t3"),
    ]),
    html.Div(id="tab-content"),
    dcc.Store(id="sel", data={}),
], className="page")


@app.callback(Output("tab-content", "children"), Input("tabs", "value"))
def render(tab):
    return {"t1": tab1, "t2": tab2, "t3": tab3}[tab].layout()


@app.callback(Output("sel", "data"), Input({"type": "g", "name": ALL}, "clickData"), Input("reset", "n_clicks"),
              State("sel", "data"), prevent_initial_call=True)
def update_selection(_clicks, _reset, sel):
    """Click on a mark = select it (click again = unselect). Selection is shared by every graph and tab."""
    sel = dict(sel or {})
    trig = ctx.triggered_id
    if trig == "reset":
        return {}
    if not isinstance(trig, dict):
        return sel
    value = ctx.triggered[0]["value"]
    if not value or trig["name"] not in CLICK_MAP:
        return sel
    key, extract = CLICK_MAP[trig["name"]]
    v = extract(value["points"][0])
    if v is None:
        return sel
    if sel.get(key) == v:
        sel.pop(key)
    else:
        sel[key] = v
    return sel


@app.callback(Output("chips", "children"), Input("sel", "data"))
def chips(sel):
    items = describe(sel or {})
    return [html.Span(c, className="chip") for c in items] if items else html.Span("ไม่มีการเลือก — คลิกกราฟเพื่อกรอง", className="hint")


COMMON = [Input("f-field", "value"), Input("f-years", "value"), Input("f-country", "value"), Input("sel", "data")]
for t in (tab1, tab2, tab3):
    t.register(app, COMMON)

if __name__ == "__main__":
    app.run(debug=False, port=8050)
