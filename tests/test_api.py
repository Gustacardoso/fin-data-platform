from fastapi.testclient import TestClient

from backend.app.main import app
from pipeline.extract.extract_erp import extract_data
from pipeline.load.load_raw import load_data

client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_financial_empty():
    assert client.get("/financial").json() == []


def test_financial_lists_loaded_records():
    data = extract_data()
    load_data(data)
    body = client.get("/financial").json()
    assert len(body) == len(data)
    assert {"id", "source", "description", "amount", "date"} <= body[0].keys()
    assert body[0]["amount"] == data[0]["amount"]


def test_financial_pagination():
    load_data(extract_data())
    assert len(client.get("/financial?limit=2").json()) == 2
    assert len(client.get("/financial?limit=2&offset=2").json()) == 1


def test_financial_rejects_invalid_limit():
    assert client.get("/financial?limit=0").status_code == 422


def test_summary_empty():
    assert client.get("/financial/summary").json() == {
        "income": 0.0,
        "expenses": 0.0,
        "balance": 0.0,
        "count": 0,
    }


def test_summary_totals():
    load_data(extract_data())
    assert client.get("/financial/summary").json() == {
        "income": 1500.0,
        "expenses": -300.0,
        "balance": 1200.0,
        "count": 3,
    }
