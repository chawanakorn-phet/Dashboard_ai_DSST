# 03 บริษัทที่รับทำงาน AI / Data Science / Statistics

ไม่มีทะเบียนเปิดที่ระบุ "บริษัท AI" โดยตรง ใช้การกรองจากรหัสประเภทธุรกิจ (SIC/TSIC) + ชุดข้อมูลเฉพาะทาง

## 3.1 ไทย: DBD ทะเบียนนิติบุคคล (Open Data)
- **แหล่ง:** กรมพัฒนาธุรกิจการค้า (DBD) ผ่าน Open Government Data
- **เนื้อหา:** นิติบุคคลใหม่/คงอยู่ และทุนจดทะเบียน จำแนกประเภทธุรกิจ — CSV/XLSX รายปี (ระดับสรุป ไม่ใช่รายชื่อบริษัท)
- **ลิงก์:** https://opendata.dbd.go.th/en/dataset/dataset_12_01 ✅ · https://gdcc.data.go.th/en/dataset/new-corporate-registration · https://gdcc.data.go.th/en/dataset/registration-type (ลิงก์หลังพบจากค้นหา ⚠️)
- **รายชื่อรายบริษัท:** DBD DataWarehouse+ (https://datawarehouse.dbd.go.th) — ค้นได้ฟรีแต่ไม่ใช่ bulk open dataset; ตรวจเงื่อนไขก่อนดึงอัตโนมัติ
- **รหัส TSIC ที่เกี่ยว:** 62xx (เขียนโปรแกรม/ที่ปรึกษา IT), 63111 (ประมวลผลข้อมูล), 72xx (R&D), 70200 (ที่ปรึกษาการจัดการ)

## 3.2 UK Companies House — Free Company Data Product
- **License:** Open Government Licence v3.0
- **เนื้อหา:** บริษัท live ทั้งหมด (~3.4M แถว แบ่ง 4 zip CSV ~60MB) มี SIC สูงสุด 4 รหัส
- **SIC เป้าหมาย:** 62012, 62020, 63110 (data processing/hosting), 72190, 73200, 70229
- **ดาวน์โหลด:** https://download.companieshouse.gov.uk/en_output.html ✅ (อัปเดตรายเดือน)

## 3.3 Epoch AI — Notable AI Models
- **License:** CC BY 4.0
- **เนื้อหา:** โมเดล AI ~21,600 (notable ~7,400) พร้อมองค์กรผู้พัฒนา (Google, OpenAI ฯลฯ) ปี 1950–ปัจจุบัน; ใช้ระบุองค์กรวิจัย/บริษัทที่ทำ AI จริง
- **ดาวน์โหลด:** https://epoch.ai/data/notable_ai_models.csv ✅ · หน้า: https://epoch.ai/data/notable-ai-models

## 3.4 สหรัฐฯ SEC EDGAR (public domain)
- ค้นบริษัทตาม SIC 7370–7374 (computer services/software): https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&SIC=7374 ⚠️ (ต้องใส่ User-Agent ตามเงื่อนไข SEC)

## 3.5 Wikidata (CC0)
- Query SPARQL หาบริษัทที่ industry = artificial intelligence / data analysis: https://query.wikidata.org ⚠️

## ข้อจำกัด
- ทะเบียนบอกแค่รหัส ไม่บอกว่าทำ AI จริง → ต้องกรองซ้ำด้วยชื่อ/เว็บไซต์/ประกาศงาน
- ไม่ควรใช้ชุดที่ไม่ใช่ open (Crunchbase, LinkedIn Company, OpenCorporates bulk) ใน deliverable นี้
