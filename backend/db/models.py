from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Integer, Numeric, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


def _now():
    return datetime.now(timezone.utc)


class RawFinancial(Base):
    __tablename__ = "raw_financial"

    id = Column(Integer, primary_key=True, index=True)
    external_id = Column(String, unique=True, nullable=False)
    source = Column(String, nullable=False)
    description = Column(String)
    amount = Column(Numeric(14, 2), nullable=False)
    date = Column(DateTime(timezone=True), default=_now)
