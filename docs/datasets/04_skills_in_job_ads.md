# 04 สกิลที่ระบุในใบสมัครงาน (job postings)

## 4.1 O*NET Database (หลัก — แนะนำ)
- **License:** CC BY 4.0 (ต้องให้เครดิต US DOL / O*NET Resource Center)
- **เวอร์ชันล่าสุดที่หน้าเว็บระบุ:** 31.0 (1,016 อาชีพ) ; ไฟล์ 30.0 ตรวจแล้วดาวน์โหลดได้
- **ไฟล์สำคัญ:** `Technology Skills.txt` (ซอฟต์แวร์/ภาษา), `Skills.txt`, `Knowledge.txt`, `Abilities.txt`, `Job Zones.txt`, `Education, Training, and Experience.txt`, `Task Statements.txt`
- **อาชีพ:** 15-2051.00 Data Scientists, 15-2041.00 Statisticians, 15-1221.00 Computer & Information Research Scientists
- **ตัวอย่าง "Hot Technologies" ของ Data Scientists:** Scala, Apache Hive, NoSQL, Docker, Linux, Kubernetes, Airflow, Kafka, PostgreSQL, Keras, SPSS, Bash (ที่มา: O*NET Online — ที่มาจากการวิเคราะห์ประกาศงาน)
- **ดาวน์โหลด:** https://www.onetcenter.org/dl_files/database/db_30_0_text.zip ✅ · หน้ารวมรุ่นล่าสุด: https://onetcenter.org/database.html ✅ · หน้าอาชีพ: https://www.onetonline.org/link/summary/15-2051.00

## 4.2 ESCO (EU)
- **License:** เปิดให้ใช้ซ้ำฟรีตามเงื่อนไข ESCO (ตรวจหน้า "use ESCO" ⚠️)
- **ไฟล์ CSV:** `occupations_en`, `skills_en`, `occupationSkillRelations` (แยก essential/optional) — 19 ไฟล์ต่อภาษา
- **ดาวน์โหลด:** https://esco.ec.europa.eu/en/use-esco/download ⚠️ (ต้องกรอก form) · โครงสร้างไฟล์: https://esco.ec.europa.eu/en/structure-esco-downloadable-datasets
- **ประโยชน์:** แยก essential vs optional skill ต่ออาชีพ; มีภาษาไทยไหม ให้ตรวจ

## 4.3 Kaggle: LinkedIn Job Postings (ใช้เป็น dataset ตัวอย่างของประกาศจริง)
- **ชุดที่พบ:** "LinkedIn Job Postings (2023–2024)" ของ arshkon (~124,000 ประกาศ, มีไฟล์ skills/industries/benefits แยก) และ "Data Science Job Postings & Skills (2024)" ของ asaniczka
- **License:** รายงานไม่ตรงกัน (CC BY-SA / ODbL ตามหน้าที่ค้นพบ) → **ต้องเปิดหน้า Kaggle ยืนยัน license ก่อนใช้**; URL ตรงไม่ได้ยืนยัน (ค้นชื่อในกล่องค้นหา Kaggle)
- **ข้อจำกัด:** ข้อมูลมาจาก scraping ของ LinkedIn → ความเสี่ยงด้านเงื่อนไขการใช้; ผมจัดเป็น "optional/ตรวจ license ก่อน"

## 4.4 Stack Overflow Survey (ทักษะที่ใช้จริง)
- `LanguageHaveWorkedWith`, `DatabaseHaveWorkedWith`, `PlatformHaveWorkedWith` กรองเฉพาะ DevType = data scientist/ML ดู 02 ข้อ 2.3

## 4.5 OECD.AI
- การกระจายทักษะ AI ในประกาศงาน 16 ประเทศ (Adzuna/LinkedIn): https://oecd.ai ⚠️ (เงื่อนไขดาวน์โหลดต้องตรวจ)

## แนวทางสกัดทักษะ (สำหรับ AI ตัวถัดไป)
1. เริ่มจาก O*NET Technology Skills ของ 3 อาชีพ → กลุ่ม: ภาษา (Python, R, SQL), ML/DL (scikit-learn, TensorFlow, PyTorch), Data eng (Spark, Airflow, Kafka), BI (Tableau, Power BI), Cloud (AWS/GCP/Azure), สถิติ (SPSS, SAS, Stata)
2. เทียบกับ ESCO essential/optional
3. ใช้ประกาศงาน (4.3) ตรวจความถี่จริง แล้ว map ไปที่ระดับใน 05
