# Project Status

อัปเดตล่าสุด: 2026-10-05 · เวอร์ชัน: 0.1 (prototype บนข้อมูลตัวอย่าง)

## สรุป
Dashboard 3 tab ทำงานได้ครบบน **ข้อมูลตัวอย่าง (synthetic)** — ยังไม่มีข้อมูลจริง ตัวเลขทุกตัวที่แสดงจึงไม่ใช่ข้อเท็จจริง (มีป้ายเตือนบนหน้าจอ)

## ความคืบหน้าตาม Milestone (BRD §10)
| เฟส | งาน | สถานะ |
|---|---|---|
| 0 | เอกสาร: README, BRD, handoff spec, dataset docs | ✅ เสร็จ |
| 1 | ETL ข้อมูลจริง (IPEDS, MHESI, BLS, ai-jobs.net, O*NET, Epoch, Companies House) | ⬜ ยังไม่เริ่ม — ตอนนี้มีเฉพาะตัวสร้างข้อมูลตัวอย่าง `etl/make_sample_data.py` |
| 2 | Skill taxonomy + mapping | 🟡 มี taxonomy 5 หมวด/21 ทักษะใน `dashboard/config.py`; ยังไม่มี mapping จากข้อความจริง (ชื่อวิชา/ประกาศงาน → ทักษะ) |
| 3 | Tab 2 + cross-filter | ✅ ทำงานบนข้อมูลตัวอย่าง |
| 4 | Tab 1 | ✅ ทำงานบนข้อมูลตัวอย่าง (หลักสูตรจริงยังไม่มี) |
| 5 | Tab 3 Skill Mismatch | ✅ ทำงานบนข้อมูลตัวอย่าง (สูตรเป็นร่างตาม BRD §5.4) |
| 6 | NFR, deploy, เอกสารผู้ใช้ | ⬜ ยังไม่เริ่ม |

## สิ่งที่ทำเสร็จแล้ว
- Dash app (`app.py`) 3 tab + ตัวกรองส่วนกลาง (สาย, ช่วงปี, ประเทศ) + ปุ่มล้างการเลือก
- **Cross-filter:** คลิกกราฟ → เก็บการเลือกใน `dcc.Store` กลาง (program / skill / level / company) → ทุกกราฟใน tab อัปเดต; คลิกซ้ำเพื่อยกเลิก; การเลือกข้าม tab ได้ (FR-G5); ทดสอบในเบราว์เซอร์แล้ว (คลิกทักษะ Statistics → หลักสูตร 12→10, KPI เปลี่ยน, chip แสดง)
- Tab 1: หลักสูตร×บัณฑิตต่อปี, หน่วยกิตวิชาบังคับตามทักษะ, มีงานทำปี 1/2/3 (ซ่อนเมื่อ n < 10), ค่าเทอม, KPI
- Tab 2: ประกาศงานตามปี/ระดับ, Top ทักษะ, Top บริษัท, เงินเดือน box ตามระดับ, KPI
- Tab 3: Supply vs Demand, gap heatmap ทักษะ×ระดับ, quadrant, mismatch รายหลักสูตร, ตารางทักษะขาดแคลน+วิชาที่เกี่ยวข้อง
- ตรรกะแกนกลางแยกเป็นฟังก์ชันล้วน: `dashboard/filters.py`, `dashboard/metrics.py`
- Unit test 7 รายการ (`tests/test_core.py`) ผ่านทั้งหมด; smoke test ทุก tab กับ 5 ชุดการเลือก + ตัวกรองว่างผ่าน

## ส่วนที่ต่างจาก BRD / ยังไม่ทำ
| รายการ | สถานะ |
|---|---|
| T1-C4 ค่าเทอม | ทำเป็น bar chart (BRD เสนอ bubble ค่าเทอม vs อัตรามีงานทำ) — ยังไม่ทำ scatter |
| T2-C1 ตำแหน่งว่าง | มีกราฟตามปี×ระดับ; ยังไม่มีแผนที่ choropleth ตามประเทศ |
| ปีของการ cross-filter | ใช้ slider ส่วนกลาง; ยังไม่เลือกปีจากการคลิกกราฟ |
| Export CSV/PNG, หน้า "About data" (FR-G6) | PNG มีใน modebar ของ Plotly; CSV และ About ยังไม่ทำ |
| สลับภาษา TH/EN (FR-G7) | ยังไม่ทำ (Could) |
| Callback test อัตโนมัติสำหรับ cross-filter (AC2) | ทดสอบด้วยมือในเบราว์เซอร์ + unit test ของตรรกะกรอง; ยังไม่มี test อัตโนมัติระดับ callback |
| ต่อ DuckDB | ยังอ่านจาก CSV ใน `data/sample/` |

## ความเสี่ยง/ประเด็นค้าง (ดู BRD §4.2, §9, §11)
1. **ข้อมูลจริงของไทยยังขาด:** รายหลักสูตร, รายวิชาบังคับ, ค่าเทอม, บัณฑิตมีงานทำปี 1–3 — ต้องตัดสินใจแหล่ง/วิธีรวบรวม
2. ประกาศงานไทยแบบเปิดแทบไม่มี; license ชุด Kaggle LinkedIn ยังไม่ยืนยัน
3. ลิงก์ที่ทำเครื่องหมาย ⚠️ ใน `docs/datasets/` ต้องตรวจก่อนเขียน loader
4. ตัวเลขใน sample อาจ "ดูสมเหตุสมผล" — ห้ามนำไปอ้างอิงเป็นข้อมูลจริง

## ขั้นต่อไป (เสนอ)
1. ตอบคำถามเปิดใน BRD §11 โดยเฉพาะแหล่งข้อมูลหลักสูตรไทยและการมีงานทำ
2. เขียน loader ข้อมูลจริงที่ลิงก์ ✅ แล้ว: ai-jobs.net → `postings`/เงินเดือน, O*NET → taxonomy ทักษะ, IPEDS → graduates (เทียบเคียง), แล้วสลับ `DATA_DIR`/`IS_SAMPLE`
3. สร้าง skill mapping (keyword → skill) + ชุดทดสอบที่ติดป้ายมือ
4. เพิ่ม callback test, หน้า About data และ export CSV

## วิธีรัน
```bash
pip install -r requirements.txt
python etl/make_sample_data.py
python app.py     # http://127.0.0.1:8050
pytest
```
