from passlib.context import CryptContext

# 定義加密上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """對密碼進行哈希處理"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """驗證明文密碼與哈希密碼是否匹配"""
    return pwd_context.verify(plain_password, hashed_password)