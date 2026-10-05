import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "etl"))
from skills import map_course, map_posting_skill  # noqa: E402


def test_course_mapping():
    assert "Statistics" in map_course("Probability and Statistics I")
    assert "Statistics" in map_course("Applied Regression Analysis")
    assert {"R", "Data Visualization", "Statistics"} <= set(map_course("Statistical Computing and Data Visualization in R"))
    assert "Machine Learning" in map_course("Data Mining and Machine Learning")
    assert "SQL/Databases" in map_course("Relational Database Systems")
    assert "Mathematics" in map_course("Calculus II")
    assert map_course("Capstone in Statistics") == ["Statistics"]
    assert map_course("Ethics of Data Science") == []


def test_posting_mapping():
    assert map_posting_skill("Python") == ["Python"]
    assert "Deep Learning" in map_posting_skill("pytorch")
    assert set(map_posting_skill("Snowflake")) == {"SQL/Databases", "Cloud"}
    assert map_posting_skill("unknown-tool-xyz") == []
