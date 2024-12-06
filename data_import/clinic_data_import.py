import pandas as pd
from sqlalchemy.orm import Session
from utils.db import get_db
from models.clinic import Clinic

# 加載 CSV 文件
file_path = r'C:\Users\User\Downloads\A21030000I-D21004-009.csv'  # 請調整這個路徑為實際的文件位置
df = pd.read_csv(file_path, encoding='utf-8')  # 根據需要設置 encoding

# 檢查數據
print(df.head())  # 確認「醫事機構代碼」列的名稱

# 使用 SQLAlchemy 連接資料庫
db: Session = next(get_db())

# 遍歷每一行並插入到 clinic 表中
for _, row in df.iterrows():
    # 獲取醫事機構代碼，假設列名為 "醫事機構代碼"
    clinic_code = row['醫事機構代碼']

    # 創建 Clinic 對象
    new_clinic = Clinic(cid=clinic_code)

    # 添加到數據庫會話
    try:
        db.add(new_clinic)
        db.commit()
    except Exception as e:
        db.rollback()  # 如果出錯，回滾事務
        print(f"Failed to insert clinic {clinic_code}: {e}")

print("Clinic data insertion complete.")
