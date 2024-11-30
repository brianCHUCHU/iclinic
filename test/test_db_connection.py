import pytest
from sqlalchemy.exc import OperationalError
from sqlalchemy.sql import text  # 必须导入 text 函数
from utils.db import get_db  # Adjust import based on your project structure


def test_database_connection():
    """
    Test if the database connection is successful.
    """
    # Get a database session
    db = next(get_db())
    
    try:
        # Test the connection by executing a simple query
        db.execute(text("SELECT 1"))
        assert True, "Database connection successful"
    except OperationalError as e:
        pytest.fail(f"Database connection failed: {e}")
    finally:
        # Ensure the session is properly closed
        db.close()
