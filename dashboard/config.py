"""Shared constants: fields, career levels, skill taxonomy."""

FIELDS = {"AI": "AI", "DS": "Data Science", "STAT": "Statistics"}

# experience_level code (ai-jobs.net style) -> dashboard level label
LEVELS = ["เริ่มต้น", "ปานกลาง", "เชี่ยวชาญ"]
LEVEL_FROM_CODE = {"EN": "เริ่มต้น", "MI": "ปานกลาง", "SE": "เชี่ยวชาญ", "EX": "เชี่ยวชาญ"}

SKILL_CATEGORIES = {
    "Languages": ["Python", "R", "SQL"],
    "ML/AI": ["Machine Learning", "Deep Learning", "NLP", "Computer Vision", "GenAI/LLM"],
    "Statistics": ["Statistics", "Regression", "A/B Testing", "Bayesian", "Time Series"],
    "Data Eng/MLOps": ["Spark", "Airflow", "Docker", "Cloud", "MLOps"],
    "BI/Viz": ["Tableau", "Power BI", "Data Visualization"],
}
SKILL_TO_CATEGORY = {s: c for c, ss in SKILL_CATEGORIES.items() for s in ss}
ALL_SKILLS = list(SKILL_TO_CATEGORY)

SAMPLE_BANNER = (
    "⚠️ ข้อมูลที่แสดงเป็นข้อมูลตัวอย่าง (SYNTHETIC) เพื่อพัฒนา UI และตรรกะ — ไม่ใช่ตัวเลขจริง"
)

MIN_N = 10  # below this, outcome rates are suppressed (BRD §7 privacy)
