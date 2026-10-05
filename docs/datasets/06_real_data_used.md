# 06 ข้อมูลจริงที่ใช้ใน Dashboard (ตรวจและดาวน์โหลดแล้ว 2026-10-05)

เจ้าของโปรเจกต์ยืนยันว่าข้อมูลจริง **ไม่จำเป็นต้องเป็นของไทย** จึงใช้ข้อมูลสหรัฐฯ เป็นหลัก ดาวน์โหลดอัตโนมัติด้วย `python etl/download_raw.py` (~290 MB) แล้วสร้างตารางด้วย `python etl/build_real_data.py`

| ใช้ทำอะไร | ชุดข้อมูล | License | ลิงก์ที่ใช้ | ขนาด |
|---|---|---|---|---|
| บัณฑิตรายหลักสูตร/ปี (CIP 11.0102 AI; 30.70xx/30.71xx Data Science/Analytics; 27.05xx Statistics; ระดับ ตรี/โท/เอก; ปีรางวัล 2019–2024) | NCES IPEDS Completions `C2019_A`–`C2024_A` | ข้อมูลรัฐบาลสหรัฐฯ (public domain) | https://nces.ed.gov/ipeds/datacenter/data/C2024_A.zip (เปลี่ยนปีในชื่อไฟล์) | 4–9 MB/ปี |
| ชื่อสถาบัน | IPEDS Institutional Characteristics `HD2024` | public domain | https://nces.ed.gov/ipeds/datacenter/data/HD2024.zip | 1 MB |
| ค่าเล่าเรียน+ค่าธรรมเนียมต่อปี (in-state; ปีการศึกษา 2023-24) | IPEDS `IC2023_AY` | public domain | https://nces.ed.gov/ipeds/datacenter/data/IC2023_AY.zip | 0.3 MB |
| จำนวนบัณฑิตที่มีรายได้และรายได้มัธยฐาน 1/3/4/5 ปีหลังจบ (ระดับสาขา CIP 4 หลัก) | College Scorecard Field of Study (Most-Recent-Cohorts, 2026-06-10) | ข้อมูลสาธารณะของ US Dept. of Education | https://ed-public-download.scorecard.network/downloads/Most-Recent-Cohorts-Field-of-Study_06102026.zip (หน้า: https://collegescorecard.ed.gov/data/) | 17 MB |
| ประกาศงาน 2023 + ทักษะ + บริษัท + ประเทศ + เงินเดือน | Luke Barousse `data_jobs` (Hugging Face) | Apache-2.0 (ตาม dataset card) | https://huggingface.co/datasets/lukebarousse/data_jobs/resolve/main/data_jobs.csv | 231 MB |
| รายวิชาบังคับ 9 หลักสูตร | รวบรวมเองจากแค็ตตาล็อกสาธารณะของมหาวิทยาลัย (ชื่อวิชา/หน่วยกิต) | ข้อเท็จจริงจากเว็บมหาวิทยาลัย — URL ต้นทางทุกแถวใน `data/curated/courses_curated.csv` | ดูไฟล์ | — |

## ข้อจำกัดที่ต้องรู้
- **Scorecard:** ชุดนี้ไม่มีปีที่ 2 (มี 1, 3, 4, 5); จำนวน "ไม่ได้ทำงาน" ถูกปกปิดเกือบทั้งหมด จึงรายงาน **จำนวนผู้มีรายได้ + รายได้มัธยฐาน** ไม่ใช่อัตราการมีงานทำ; ไม่มีรหัส AI แยก (AI อยู่ใน CIP 11.01 รวม) และหลักสูตรใหม่ยังไม่มีข้อมูล
- **ประกาศงาน:** snapshot ปี 2023 ปีเดียว; ข้อมูลระบุ "เครื่องมือ" (python, sql, tensorflow ฯลฯ) ไม่ใช่แนวคิด (statistics, regression) ความต้องการทักษะเชิงแนวคิดจึงถูกประเมินต่ำ; เงินเดือนมีในประกาศเพียง ~4% (ส่วนใหญ่สหรัฐฯ); ระดับงาน (เริ่มต้น/ปานกลาง/เชี่ยวชาญ) จัดจากคำในชื่อตำแหน่ง; ประเทศ "Sudan" มี ~10k ประกาศ ซึ่งผิดปกติ — เป็นค่าตามที่ชุดข้อมูลระบุ ยังไม่ได้ตรวจสาเหตุ
- **รายวิชา:** มีเพียง 9 หลักสูตรปริญญาตรี (AI 3, DS 3, Stat 3) และจับคู่ทักษะจาก **ชื่อวิชา** ด้วยกฎคำสำคัญ (ไม่ได้อ่านคำอธิบายรายวิชา); หลักสูตรใหม่ 5 แห่งยังไม่มีบัณฑิตใน IPEDS 2019–24; Baylor ดึงจากข้อความผลการค้นหา หน่วยกิตเป็นค่าสมมติ 3
- ค่าเล่าเรียนรวม = ค่าต่อปี × (ตรี 4 / โท 2 / เอก 5 ปี) เป็นค่าประมาณ ไม่รวมค่าครองชีพ
