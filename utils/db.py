from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from contextlib import contextmanager

# 資料庫配置
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "db_project"
DB_USER = "user"

# 讀取密碼
PASSWORD_FILE = "secrets/db_password.txt"
try:
    with open(PASSWORD_FILE, "r") as file:
        DB_PASSWORD = file.read().strip()
except FileNotFoundError:
    raise Exception(f"Password file not found at {PASSWORD_FILE}. Ensure it exists and contains the correct password.")

# 建立資料庫連接字串
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# 建立 SQLAlchemy 引擎與 SessionLocal
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 簡單的資料庫連接測試函式
def test_db_connection():
    try:
        with engine.connect() as connection:
            print("Database connected successfully!")
    except Exception as e:
        print(f"Database connection failed: {e}")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()