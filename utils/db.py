from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from dotenv import load_dotenv
import os

# 加載 .env 文件
load_dotenv(dotenv_path="secrets/.env")

# 從環境變數讀取配置
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "iclinic")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")

# 檢查是否讀取成功
if not DB_PASSWORD:
    raise Exception("Database password not found. Check your secrets/.env file.")

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