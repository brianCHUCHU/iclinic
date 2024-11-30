# Virtual Environment

Please install the virtual environment via `requirements.txt` file.

```bash
conda create --name fastapi_postgres_env python=3.11
conda activate fastapi_postgres_env
pip install -r requirements.txt
```

# Database

Add `secrets/db_password.txt` file with the password of the database.

```bash
echo "your_password" > secrets/db_password.txt
```

# Run the FastAPI server

```bash
conda activate fastapi_postgres_env
uvicorn main:app --reload
```

# pytest

```bash
conda activate fastapi_postgres_env
set PYTHONPATH="your_root_repo_path"
pytest
```
