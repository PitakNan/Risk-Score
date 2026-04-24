# Risk Scoring Dashboard

ระบบ Dashboard วิเคราะห์ความเสี่ยงทางการเงินของโรงพยาบาล (Full-stack Version)

## 🚀 วิธีการติดตั้งและใช้งาน

1. **ติดตั้ง Python:** ตรวจสอบว่าเครื่องคอมพิวเตอร์ติดตั้ง Python เรียบร้อยแล้ว
2. **ติดตั้ง Library ที่จำเป็น:**
   เปิด Terminal หรือ Command Prompt แล้วรันคำสั่ง:
   ```bash
   pip install -r requirements.txt
   ```
3. **รันระบบ Server:**
   ```bash
   python app.py
   ```
4. **เข้าใช้งาน:**
   เปิด Browser แล้วไปที่: **http://localhost:5000**

## 📂 โครงสร้างไฟล์ที่สำคัญ
- `app.py`: ระบบหลังบ้าน (API) จัดการการดึงข้อมูลและการนำเข้าไฟล์ Excel
- `Risk_Score_Dashboard.html`: ระบบหน้าบ้าน (UI) แสดงผลกราฟและตารางวิเคราะห์
- `dashboard.db`: ฐานข้อมูล SQLite เก็บข้อมูลโรงพยาบาลและผลวิเคราะห์
- `requirements.txt`: รายการ Library ที่ต้องใช้ในโปรเจกต์

## 🛡️ ระบบความปลอดภัย (Admin)
- การนำเข้าข้อมูลใหม่ต้องใช้รหัสผ่าน (Admin Code)
- ข้อมูลจะถูกบันทึกลงฐานข้อมูลโดยตรง (Persistent Storage)
