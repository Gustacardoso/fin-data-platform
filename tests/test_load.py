from backend.db.connection import SessionLocal
from backend.db.models import RawFinancial
from pipeline.extract.extract_erp import extract_data
from pipeline.load.load_raw import load_data


def _count():
    db = SessionLocal()
    try:
        return db.query(RawFinancial).count()
    finally:
        db.close()


def test_load_inserts_records():
    data = extract_data()
    assert load_data(data) == len(data)
    assert _count() == len(data)


def test_load_is_idempotent():
    data = extract_data()
    load_data(data)
    assert load_data(data) == 0
    assert _count() == len(data)


def test_load_inserts_only_new_records():
    data = extract_data()
    load_data(data[:1])
    assert load_data(data) == len(data) - 1
    assert _count() == len(data)
