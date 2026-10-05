# 01 จำนวนผู้สำเร็จการศึกษา AI / Data Science / Statistics

สถานะลิงก์: ✅ = ตรวจแล้วว่าเข้าถึงได้ (2026-10-05) · ⚠️ = ต้องตรวจเองก่อนใช้ (บอทถูกบล็อก/ไม่ได้ตรวจ)

## 1.1 ไทย: จำนวนผู้สำเร็จการศึกษา จำแนกกลุ่มสาขา 10 กลุ่ม (ISCED)
- **แหล่ง:** สป.อว. (MHESI) ผ่าน Open Government Data of Thailand
- **ครอบคลุม:** ปีการศึกษา 2561–2566, ทุกระดับ, สถาบันรัฐ/เอกชน/ต่างประเทศ, มี % เปลี่ยนแปลงรายปี
- **ใช้ทำอะไร:** ดูแนวโน้มภาพรวมกลุ่ม "ICT" / "Natural sciences, mathematics and statistics" (ไม่แยกสาขา AI/DS โดยตรง)
- **License:** Creative Commons Attribution
- **อัปเดตล่าสุด:** 15 ส.ค. 2567
- **หน้าชุดข้อมูล (CSV + data dictionary XLSX):** https://data.go.th/en/dataset/education-creative1 ✅
- **พอร์ทัลต้นทาง (ละเอียดกว่า ตามสถาบัน/สาขา):** https://info.mhesi.go.th/stat_graduate.php ✅ (ตรวจ license เอง)
- **ชุดข้อมูลเสริม (กระทรวงศึกษาธิการ):** https://catalog.moe.go.th/en/dataset/dataset-15_41 ⚠️ (ผู้สำเร็จการศึกษาจำแนกเพศ/สถานศึกษา/ระดับ/จังหวัด)
- **ข้อจำกัด:** ระดับสาขาย่อย (วิทยาการข้อมูล, AI) ต้องไปดูในพอร์ทัล MHESI หรือขอข้อมูลจาก สกสว./อว.

## 1.2 สหรัฐฯ: IPEDS Completions (รายสาขา CIP)
- **แหล่ง:** NCES / US Dept. of Education (ข้อมูลภาครัฐสหรัฐฯ — public domain)
- **รหัส CIP ที่ต้องกรอง:** `30.7001` Data Science · `27.0501` Statistics · `11.0102` Artificial Intelligence · `30.7101` Data Analytics (ตรวจรายการ CIP 2020 อีกครั้ง)
- **ไฟล์:** `C20XX_A` = จำนวนผู้จบจำแนก CIP × ระดับรางวัล × เพศ × เชื้อชาติ
- **ดาวน์โหลดตรง:**
  - https://nces.ed.gov/ipeds/datacenter/data/C2023_A.zip ✅
  - https://nces.ed.gov/ipeds/datacenter/data/C2024_A.zip ✅
  - เปลี่ยนปีใน URL (C2019_A … ) เพื่อดึงอนุกรมเวลา; dictionary อยู่ที่ https://nces.ed.gov/ipeds/datacenter/DataFiles.aspx
- **ระดับ (AWLEVEL):** 3 = associate, 5 = bachelor, 7 = master, 17/18/19 = doctorate

## 1.3 ยุโรป: Eurostat
- **ชุดข้อมูล:** `educ_uoe_grad02` (ผู้จบ tertiary จำแนก ISCED-F), `isoc_sks_itspe` (ICT specialists จำแนกวุฒิ), `isoc_ski_itemp` (ผู้มีการศึกษา ICT ที่ทำงาน)
- **License:** CC BY 4.0 (นโยบาย reuse ของ Eurostat)
- **ลิงก์:** https://ec.europa.eu/eurostat/databrowser/view/educ_uoe_grad02 ⚠️ · https://db.nomics.world/Eurostat/isoc_sks_itspe ✅(ผ่านการค้นหา)
- **หมายเหตุ:** ISCED-F 0613 = software/apps, 0611 = computer use; ไม่มี code เฉพาะ "data science" ให้ใช้ ISCED-F 0541 (mathematics & statistics) + 06 (ICT)

## 1.4 รายงานรวม: Stanford AI Index
- มีข้อมูลผู้จบ CS/AI ระดับโลก แต่รายงานเป็น CC BY-ND (ห้ามดัดแปลง) — ใช้เป็นแหล่งอ้างอิง ไม่ใช่ raw dataset
- https://hai.stanford.edu/ai-index ✅ (ตรวจหน้า "Public Data" เองเพื่อดูเงื่อนไขล่าสุด)

## ข้อควรระวัง
- นิยามสาขาต่างกันระหว่างประเทศ (CIP vs ISCED vs รหัส สกอ.) ต้อง crosswalk ก่อนเปรียบเทียบ
- Data Science เป็นหลักสูตรใหม่ ปี 2018 ก่อนหน้านี้แทบไม่มีรหัสเฉพาะ
