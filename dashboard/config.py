"""Shared constants: fields, career levels, skill taxonomy."""

FIELDS = {"AI": "AI", "DS": "Data Science", "STAT": "Statistics"}

# experience_level code (ai-jobs.net style) -> dashboard level label
LEVELS = ["เริ่มต้น", "ปานกลาง", "เชี่ยวชาญ"]
LEVEL_FROM_CODE = {"EN": "เริ่มต้น", "MI": "ปานกลาง", "SE": "เชี่ยวชาญ", "EX": "เชี่ยวชาญ"}

SKILL_CATEGORIES = {
    "Languages & Programming": ["Python", "R", "SQL/Databases", "Software Engineering"],
    "ML/AI": ["Machine Learning", "Deep Learning", "NLP", "GenAI/LLM"],
    "Statistics": ["Statistics"],
    "Data Eng & Cloud": ["Big Data/Data Eng", "Cloud", "DevOps/Containers"],
    "BI & Viz": ["BI Tools", "Data Visualization", "Spreadsheets"],
}
SKILL_TO_CATEGORY = {s: c for c, ss in SKILL_CATEGORIES.items() for s in ss}
ALL_SKILLS = list(SKILL_TO_CATEGORY)       # skills compared in the mismatch analysis
FOUNDATION_SKILLS = ["Mathematics"]       # taught but not a posting skill -> shown in Tab 1 only

SAMPLE_BANNER = (
    "⚠️ ข้อมูลที่แสดงเป็นข้อมูลตัวอย่าง (SYNTHETIC) เพื่อพัฒนา UI และตรรกะ — ไม่ใช่ตัวเลขจริง"
)
REAL_NOTE = (
    "ข้อมูลจริง (สหรัฐฯ): ผู้จบ = NCES IPEDS · รายได้/การมีงานทำ = College Scorecard · ค่าเล่าเรียน = IPEDS IC · "
    "ประกาศงาน = Luke Barousse data_jobs (ปี 2023, Apache-2.0) · รายวิชา = แค็ตตาล็อกหลักสูตร 9 แห่งที่รวบรวมเอง"
)

MIN_N = 10  # below this, outcome rates are suppressed (BRD §7 privacy)
