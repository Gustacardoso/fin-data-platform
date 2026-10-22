from pipeline.extract.extract_erp import extract_data


def test_extract_returns_records_with_unique_ids():
    data = extract_data()
    assert data
    ids = [d["external_id"] for d in data]
    assert len(ids) == len(set(ids))
    assert all({"description", "amount"} <= d.keys() for d in data)
