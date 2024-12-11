# Virtual Environment

Please install the virtual environment via `requirements.txt` file.

```bash
conda create --name fastapi_postgres_env python=3.11
conda activate fastapi_postgres_env
pip install -r requirements.txt
```

# Database

1. Backup via .backup file on the repo
2. Add `secrets/.env` file with the correct environment variables.

Example:
```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=iclinic
DB_USER=postgres
DB_PASSWORD="your_password"
```

# Run the FastAPI server

```bash
conda activate fastapi_postgres_env
uvicorn main:app --reload
```

# Valid Account and Password

clinic帳號
```
tdbjf
Q67kXtqyTW
```

patient帳號1
```
I121674754
UlBVd5CjHK
```

patient帳號2
```
T143060794
r7D3QwuvqH
```
