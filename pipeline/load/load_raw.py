from backend.db.connection import SessionLocal
from backend.db.models import RawFinancial


def load_data(data):
    """Insere os registros novos; os já carregados (external_id) são ignorados."""
    db = SessionLocal()
    try:
        ids = [item["external_id"] for item in data]
        existing = {
            row[0]
            for row in db.query(RawFinancial.external_id)
            .filter(RawFinancial.external_id.in_(ids))
            .all()
        }
        new = [item for item in data if item["external_id"] not in existing]
        for item in new:
            db.add(
                RawFinancial(
                    external_id=item["external_id"],
                    source="ERP_SIMULADO",
                    description=item["description"],
                    amount=item["amount"],
                )
            )
        db.commit()
        return len(new)
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
