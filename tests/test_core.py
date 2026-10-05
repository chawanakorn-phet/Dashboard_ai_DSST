import pandas as pd
import pytest

from dashboard import filters, metrics


@pytest.fixture
def frames():
    programs = pd.DataFrame({"program_id": ["P1", "P2"], "field": ["DS", "AI"], "program_name": ["a", "b"]})
    courses = pd.DataFrame({"program_id": ["P1", "P1", "P2"], "skill": ["SQL", "R", "Python"],
                            "course": ["c1", "c2", "c3"], "credits": [3, 3, 3]})
    grads = pd.DataFrame({"program_id": ["P1", "P2"], "year": [2024, 2024], "count": [30, 10]})
    post = pd.DataFrame({"posting_id": ["a", "b", "c", "d"], "field": ["DS", "DS", "AI", "AI"],
                         "year": [2024] * 4, "country": ["TH", "US", "US", "US"],
                         "level": ["เริ่มต้น", "ปานกลาง", "ปานกลาง", "เชี่ยวชาญ"], "company": ["X", "X", "Y", "Y"]})
    ps = pd.DataFrame({"posting_id": ["a", "a", "b", "c", "d"], "skill": ["SQL", "Python", "SQL", "Python", "Python"]})
    return programs, courses, grads, post, ps


def test_demand_share(frames):
    _, _, _, post, ps = frames
    d = metrics.demand_share(post, ps, ["SQL", "Python", "R"])
    assert d["SQL"] == 0.5 and d["Python"] == 0.75 and d["R"] == 0


def test_demand_share_empty(frames):
    _, _, _, post, ps = frames
    assert metrics.demand_share(post.iloc[0:0], ps, ["SQL"]).sum() == 0


def test_supply_coverage_weighted_by_graduates(frames):
    _, courses, grads, _, _ = frames
    s = metrics.supply_coverage(["P1", "P2"], grads, courses, ["SQL", "R", "Python", "Spark"])
    assert s["SQL"] == pytest.approx(0.75) and s["Python"] == pytest.approx(0.25) and s["Spark"] == 0


def test_supply_equal_weights_when_no_graduates(frames):
    _, courses, grads, _, _ = frames
    s = metrics.supply_coverage(["P1", "P2"], grads.iloc[0:0], courses, ["SQL"])
    assert s["SQL"] == pytest.approx(0.5)


def test_gap_and_program_mismatch(frames):
    _, courses, grads, post, ps = frames
    skills = ["SQL", "Python", "R"]
    D = metrics.demand_share(post, ps, skills)
    gt = metrics.gap_table(D, metrics.supply_coverage(["P1", "P2"], grads, courses, skills))
    assert gt.set_index("skill").gap["Python"] == pytest.approx(0.75 - 0.25)
    mm = metrics.program_mismatch(D, courses, ["P1", "P2"])
    assert mm["P1"] == pytest.approx(0.75 / 1.25)  # P1 lacks Python (0.75) of total demand 1.25
    assert mm["P2"] == pytest.approx(0.5 / 1.25)   # P2 lacks SQL (0.5)


def test_select_postings_cross_filter(frames):
    _, _, _, post, ps = frames
    args = (post, ps, ["DS", "AI"], (2024, 2024), ["TH", "US"])
    assert len(filters.select_postings(*args, {})) == 4
    assert set(filters.select_postings(*args, {"skill": "SQL"}).posting_id) == {"a", "b"}
    both = filters.select_postings(*args, {"skill": "SQL", "level": "ปานกลาง"})
    assert set(both.posting_id) == {"b"}
    # excluded key is ignored so the chart keeps showing all options
    assert len(filters.select_postings(*args, {"skill": "SQL"}, exclude=("skill",))) == 4
    assert len(filters.select_postings(post, ps, [], (2024, 2024), ["US"], {})) == 0


def test_select_programs_and_effective_fields(frames):
    programs, courses, *_ = frames
    assert list(filters.select_programs(programs, courses, ["DS", "AI"], {"skill": "Python"}).program_id) == ["P2"]
    assert list(filters.select_programs(programs, courses, ["DS"], {}).program_id) == ["P1"]
    assert filters.effective_fields(programs, ["DS", "AI"], {"program": "P2"}) == ["AI"]
    assert filters.effective_fields(programs, ["DS", "AI"], {}) == ["DS", "AI"]
