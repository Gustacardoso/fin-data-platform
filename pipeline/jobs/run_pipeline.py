import logging

from backend.db.create_tables import init_db
from pipeline.extract.extract_erp import extract_data
from pipeline.load.load_raw import load_data

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("pipeline")


def run():
    init_db()
    data = extract_data()
    inserted = load_data(data)
    log.info("Pipeline executado: %d extraídos, %d novos inseridos.", len(data), inserted)


if __name__ == "__main__":
    try:
        run()
    except Exception:
        log.exception("Falha na execução do pipeline")
        raise SystemExit(1)
