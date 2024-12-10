import pytest
from fastapi.testclient import TestClient
from main import app  # 假設你的 FastAPI 應用位於 main.py

pytest.skip(allow_module_level=True)

client = TestClient(app)

names = ['家庭醫學科', '內科', '外科', '兒科', '婦產科', '骨科', '神經科', '神經外科', '泌尿科', '耳鼻喉科', '眼科', '皮膚科', '精神科', '復健科', '麻醉科', '放射診斷科', '放射腫瘤科', '解剖病理科', '臨床病理科', '核子醫學科', '急診醫學科', '整形外科', '職業醫學科', '西醫一般科', '牙醫一般科', '口腔病理科', '口腔顎面外科', '齒顎矯正科', '牙周病科', '兒童牙科', '牙髓病科', '復補綴牙科', '牙體復形科', '家庭牙醫科', '特殊需求者口腔醫學科', '中醫一般科', '中醫內科', '中醫外科', '中醫眼科', '中醫兒科', '中醫婦科', '中醫傷科', '中醫針灸科', '中醫痔科']


def test_generate_division():
    for idx, name in enumerate(names, start=1):
        payload = {
            "divid": f"D{idx:02d}",
            "divname": name
        }
        response = client.post("/divisions", json=payload)
        assert response.status_code == 201
        assert response.json()["divname"] == payload["divname"]