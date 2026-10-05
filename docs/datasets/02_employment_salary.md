# 02 การจ้างงาน วุฒิ เงินเดือน (ทั่วโลก)

สถานะลิงก์: ✅ ตรวจแล้ว · ⚠️ ต้องตรวจเอง (บอทถูกบล็อก/ไม่ได้ตรวจ)

## 2.1 BLS OEWS + Employment Projections (สหรัฐฯ)
- **License:** ข้อมูลรัฐบาลสหรัฐฯ (public domain, อ้างอิงแหล่ง)
- **อาชีพ SOC:** 15-2051 Data Scientists · 15-2041 Statisticians · 15-2021 Mathematicians
- **ข้อเท็จจริงที่พบ (BLS OOH, พ.ค. 2024):** Data scientist median $112,590 (P10 $63,650 / P90 $194,410); Statistician median $103,300; คาดการณ์การจ้างงาน data scientist โต 34% ช่วง 2024–2034
- **วุฒิขั้นต่ำ:** ดูหน้า OOH (โดยทั่วไป Bachelor's สำหรับ DS, Master's สำหรับ statistician)
- **ดาวน์โหลด (national, ทุก SOC):**
  - พ.ค. 2025: https://www.bls.gov/oes/special-requests/oesm25nat.zip ⚠️
  - พ.ค. 2024: https://www.bls.gov/oes/special-requests/oesm24nat.zip ⚠️ (curl ถูก 403 แต่หน้า BLS ระบุลิงก์นี้ — เปิดผ่านเบราว์เซอร์)
  - หน้ารวม: https://www.bls.gov/oes/tables.htm · OOH: https://www.bls.gov/ooh/math/data-scientists.htm ✅
- **เงินเดือนเริ่มต้น (proxy):** ใช้ P10/P25 ของ OEWS (ไม่มีตัวเลข "starting salary" ตรง ๆ)

## 2.2 ai-jobs.net Salaries (global, รายงานโดยผู้ใช้)
- **License:** CC0 (public domain)
- **ฟิลด์:** work_year, experience_level (EN/MI/SE/EX), employment_type, job_title, salary, salary_currency, salary_in_usd, employee_residence, remote_ratio, company_location, company_size
- **ประเทศ:** ทั่วโลก (มีไทยจำนวนน้อย — ตรวจจำนวนแถว)
- **ดาวน์โหลด:** https://ai-jobs.net/salaries/download/ (redirect ไป foorilla.com — ตรวจหน้าเพื่อหาปุ่ม CSV ล่าสุด) ⚠️; สำเนา Kaggle: ค้น "Data Science Job Salaries" โดย ruchi798 (ตรวจ license บนหน้า)
- **ข้อจำกัด:** self-reported, bias ไปทาง US/ทักษะสูง

## 2.3 Stack Overflow Developer Survey
- **License:** ODbL 1.0
- **ฟิลด์ที่ใช้:** Country, EdLevel, DevType (data scientist/ML), YearsCodePro, ConvertedCompYearly, LanguageHaveWorkedWith
- **ผลปี 2025:** ผู้ตอบ ~49,000 จาก 177 ประเทศ; DS median ที่รายงานในบล็อกบุคคลที่สาม ~$60k (ต้องยืนยันจากข้อมูลดิบ)
- **ดาวน์โหลด:** https://survey.stackoverflow.co/ (ปุ่ม "Download Full Data Set (CSV)") ✅ — URL zip ตรงเดาไม่ได้ ให้คลิกจากหน้า

## 2.4 Kaggle Machine Learning & Data Science Survey
- **ฟิลด์:** อายุ, ประเทศ (รวมไทย), วุฒิ, ตำแหน่ง, ประสบการณ์, ช่วงเงินเดือน (Q ปีละ), เครื่องมือ
- **License:** Creative Commons (ต้องตรวจชนิด CC บนหน้าแต่ละปี ⚠️)
- **ลิงก์:** ค้นหา "Kaggle Machine Learning & Data Science Survey" บน https://www.kaggle.com (URL เฉพาะปีไม่ได้ยืนยัน; ต้องล็อกอินเพื่อดาวน์โหลด)

## 2.5 อังกฤษ ONS ASHE (OGL)
- เงินเดือนตาม SOC (เช่น 2135 Data scientists — ตรวจรหัสใน SOC 2020) https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/earningsandworkinghours ⚠️

## 2.6 ไทย
- **สำรวจภาวะการทำงานของประชากร (NSO):** ผู้มีงานทำตามอาชีพ (ISCO)/การศึกษา/ค่าจ้าง — microdata ต้องขออนุญาต, ตารางสรุปเปิด: https://www.nso.go.th ⚠️ ; ตรวจ data.go.th เพิ่ม
- **ข้อจำกัด:** ไม่มีรหัสอาชีพ "นักวิทยาการข้อมูล" แยกใน ISCO-08 (อยู่ใต้ 2511/2120) → ต้องใช้ proxy

## 2.7 Eurostat
- ICT specialists จำแนกวุฒิ `isoc_sks_itspe` (ISCED 2011): https://db.nomics.world/Eurostat/isoc_sks_itspe ✅

## 2.8 OECD.AI live data
- สัดส่วนประกาศงาน/ทักษะ AI ใน 16 ประเทศ (Adzuna, LinkedIn) — เงื่อนไข reuse ต้องตรวจ: https://oecd.ai ⚠️
