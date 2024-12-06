from sqlalchemy.orm import configure_mappers

try:
    configure_mappers()
except Exception as e:
    print(f"Mapper configuration error: {e}")
