from flask import Flask
from models import db, User
from datetime import datetime
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# สร้าง application context
app.app_context().push()

def check_available_date(customer_date):
    try:
        # แปลงวันที่จาก string เป็น datetime object
        customer_date = datetime.strptime(customer_date, '%Y-%m-%d').date()
    except ValueError:
        return False

    # ค้นหาในฐานข้อมูลว่ามีวันที่ที่ตรงกับวันที่ที่รับเข้ามาหรือไม่
    existing_date = User.query.filter_by(customer_date=customer_date).first()

    if existing_date:
        return True
    else:
        return False

# ใช้โค้ดนี้เพื่อทดสอบฟังก์ชัน check_available_date
customer_date = '2024-07-20'  # วันที่ที่ต้องการตรวจสอบ
result = check_available_date(customer_date)
print(result)
