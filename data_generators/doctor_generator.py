import sys
import os

from faker import Faker
from sqlalchemy.orm import Session
from services.doctor_service import create_doctor
from schemas.doctor import DoctorCreate
from utils.id_validation import id_generator, id_check
from utils.db import get_db
from sqlalchemy.orm import configure_mappers
import models  # 確保所有模型都已被導入

# 顯式地配置映射器以發現配置錯誤
try:
    configure_mappers()
except Exception as e:
    print(f"Mapper configuration error: {e}")

# 將項目根目錄添加到 Python 的模塊查找路徑中
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.append(project_root)

# 設置工作目錄為項目根目錄
os.chdir(project_root)

fake = Faker()

def generate_doctors(db: Session, num_records: int = 10):
    for _ in range(num_records):
        # 生成合法的 docid
        docid = id_generator()
        while not id_check(docid):
            docid = id_generator()

        # 使用 Faker 生成醫生名字
        docname = fake.name()

        # 使用 create_doctor 函數來創建醫生資料
        try:
            create_doctor(db=db, doctor_data=DoctorCreate(docid=docid, docname=docname))
        except Exception as e:
            print(f"Failed to create doctor: {e}")

    print(f"{num_records} doctors generated successfully.")

if __name__ == "__main__":
    # 使用資料庫連接來生成資料
    db = next(get_db())
    generate_doctors(db, num_records=15)
