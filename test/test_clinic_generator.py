from fastapi.testclient import TestClient
from faker import Faker
from main import app
import random
import pandas as pd
import string
import pytest
import os
import csv

pytest.skip(allow_module_level=True)

client = TestClient(app)
fake = Faker()

def parse_address_simple(full_address):

    city, district = None, None
    address_parts = list(full_address)
    city_keywords = ["縣", "市"]
    district_keywords = ["鄉", "鎮", "市", "區"]
    city_end_index = None
    district_end_index = None

    for i, char in enumerate(address_parts):
        if not city and char in city_keywords:
            city = full_address[:i + 1]
            city_end_index = i + 1
        elif city and not district and char in district_keywords:
            district = full_address[city_end_index:i + 1]
            district_end_index = i + 1
            break

    if district_end_index:
        address = full_address[district_end_index:].strip()
    else:
        address = full_address.strip()

    return city or "未知", district or "未知", address

def generate_clinic_payload(row):

    city, district, address = parse_address_simple(row["地址"])
    acct_name :str =  "".join(random.choices(string.ascii_lowercase, k=5))
    acct_pw: str = "".join(random.choices(string.ascii_letters + string.digits, k=10))
    payload = {
        "cid": "C" + "".join(random.choices(string.digits, k=9)),
        "fee": random.choice([100, 150, 200, 250]),
        "queue_type": random.choice(["S", "I"]),
        "acct_name": acct_name,
        "acct_pw": acct_pw,
        "cname": row["醫事機構名稱"],
        "city": city,
        "district": district,
        "address": address,
        "available": True
    }
    csv_file = "./src/clinic_accounts.csv"
    file_exists = os.path.isfile(csv_file)
    with open(csv_file, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if not file_exists:  # 如果檔案不存在，寫入標題行
            writer.writerow(["acct_name", "acct_pw"])
        writer.writerow([acct_name, acct_pw])  # 追加內容
    
    return payload

def test_clinic_generator():
    file_path = "./src/A21030000I-D21004-009.csv"
    df = pd.read_csv(file_path, encoding="utf-8")

    limit = 3
    limited_df = df.head(limit)

    created_count = 0 
    for _, row in limited_df.iterrows():
        payload = generate_clinic_payload(row)
        response = client.post("/clinics", json=payload)
        assert response.status_code == 201, f"Failed at payload: {payload}"
        created_count += 1


