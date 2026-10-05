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
Python 3.11+, Dash (Flask + Plotly), pandas, DuckDB (ใช้ภายหลัง), pytest

## โครงสร้าง
```
app.py                 Dash entrypoint (3 tabs)
dashboard/
  config.py            ระดับงาน, หมวดทักษะ, สี
  data.py              โหลดข้อมูล (sample หรือ processed)
  filters.py           apply_filters — ตรรกะ cross-filter ที่ทดสอบได้
  metrics.py           Demand / Supply / Gap / Mismatch score
  tabs/{tab1,tab2,tab3}.py
etl/make_sample_data.py  สร้างข้อมูลตัวอย่าง (SYNTHETIC)
tests/
```

## เริ่มใช้งาน
```bash
pip install -r requirements.txt
python etl/make_sample_data.py   # สร้าง data/sample/*.csv
python app.py                    # เปิด http://127.0.0.1:8050
pytest
```

## หมายเหตุสำคัญเรื่องข้อมูล
ข้อมูลที่ dashboard แสดงตอนนี้เป็น **ข้อมูลตัวอย่าง (synthetic)** เพื่อพัฒนา UI และตรรกะ — ไม่ใช่ตัวเลขจริง และมีป้ายเตือนบนหน้าจอ
ช่องว่างข้อมูลจริงของไทย (หลักสูตร รายวิชา ค่าเทอม การมีงานทำปี 1–3) ดู BRD §4.2

## License ข้อมูล
แต่ละแหล่งมี license ต่างกัน (CC0, CC BY, OGL, ODbL ฯลฯ) ดูรายละเอียดใน `docs/datasets/`
