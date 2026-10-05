# Dashboard_ai_DSST

Dashboard วิเคราะห์อุปทาน–อุปสงค์กำลังคนสาย **AI / Data Science / Statistics** และ **Skill Mismatch** สร้างด้วย Python + Plotly (Dash)

สถานะโครงการ: ดู [`STATUS.md`](STATUS.md)

## วัตถุประสงค์
ตอบ 3 คำถามทางธุรกิจ (รายละเอียดใน [`docs/BRD_Dashboard_AI_DSST.md`](docs/BRD_Dashboard_AI_DSST.md)):

| Tab | คำถาม | กราฟหลัก |
|---|---|---|
| 1 บัณฑิตและทักษะที่เรียน | คนจบเท่าไร จากหลักสูตรไหน เรียนทักษะอะไร | หลักสูตร × จำนวนบัณฑิตต่อปี, รายวิชาบังคับ, บัณฑิตมีงานทำปี 1/2/3, ค่าเทอม |
| 2 ตลาดงานและทักษะที่ต้องการ | จ้างเท่าไร ต้องการทักษะอะไร บริษัทไหน เงินเดือนเท่าไร | ตำแหน่งว่าง, ทักษะที่ต้องการ, บริษัท, เงินเดือนตามระดับ |
| 3 Skill Mismatch | ที่เรียนกับที่ตลาดต้องการต่างกันตรงไหน | Supply vs Demand, gap matrix, quadrant, เปรียบเทียบหลักสูตร |

ทุกกราฟใน tab เดียวกัน **เชื่อมกัน (cross-filter)** — คลิกกราฟหนึ่ง กราฟอื่นอัปเดตตาม

## เอกสารในโปรเจกต์
| ไฟล์ | เนื้อหา |
|---|---|
| [`docs/BRD_Dashboard_AI_DSST.md`](docs/BRD_Dashboard_AI_DSST.md) | Business Requirements: ขอบเขต, FR/NFR, นิยามตัวชี้วัด, ความเสี่ยง |
| [`docs/ai_handoff_specification_document.md`](docs/ai_handoff_specification_document.md) | Handoff spec: schema เป้าหมาย 3 ชุดข้อมูล, taxonomy ระดับงาน/ทักษะ, งานวิเคราะห์ |
| [`docs/datasets/`](docs/datasets) | รายการแหล่งข้อมูลเปิด 5 หมวด พร้อม license และลิงก์ (✅ ตรวจแล้ว / ⚠️ ต้องตรวจเอง) |
| [`docs/handoff.html`](docs/handoff.html) | หน้า handoff แบบแก้ไขได้ |

## เทคโนโลยี
Python 3.11+, Dash (Flask + Plotly), pandas, pytest

## โครงสร้าง
```
app.py                  Dash entrypoint (3 tabs)
dashboard/              config, data loader, filters (cross-filter), metrics (Gap/Mismatch), ui, tabs/
etl/download_raw.py     ดาวน์โหลดข้อมูลเปิด (~290 MB) -> data/raw/
etl/build_real_data.py  สร้างตาราง -> data/processed/
etl/skills.py           กฎจับคู่ชื่อวิชา / ทักษะในประกาศงาน -> taxonomy กลาง
data/curated/           รายวิชาบังคับ 9 หลักสูตร (รวบรวมเอง พร้อม URL ต้นทาง)
tests/
```

## เริ่มใช้งาน
```bash
pip install -r requirements.txt
python etl/download_raw.py       # ครั้งแรกเท่านั้น
python etl/build_real_data.py    # สร้าง data/processed/*.csv
python app.py                    # เปิด http://127.0.0.1:8050
pytest
```

## ข้อมูล
ใช้ **ข้อมูลจริงเปิด (สหรัฐฯ เป็นหลัก)**: NCES IPEDS, College Scorecard, Luke Barousse `data_jobs` (Apache-2.0) และรายวิชาที่รวบรวมเอง — รายละเอียด license ลิงก์ และข้อจำกัดอยู่ใน [`docs/datasets/06_real_data_used.md`](docs/datasets/06_real_data_used.md)
ข้อมูลไทยยังไม่ได้ใช้ (ไม่จำเป็นตามที่เจ้าของโปรเจกต์ระบุ) — แหล่งไทยที่รวบรวมไว้ดู `docs/datasets/01–05`

## License ข้อมูล
แต่ละแหล่งมี license ต่างกัน (CC0, CC BY, OGL, ODbL ฯลฯ) ดูรายละเอียดใน `docs/datasets/`
