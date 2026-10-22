from fastapi import Depends, FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import case, func
from sqlalchemy.orm import Session

from backend.db.connection import get_db
from backend.db.models import RawFinancial

app = FastAPI(title="Fin Data Platform")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["GET"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/financial")
def get_financial(
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    items = (
        db.query(RawFinancial)
        .order_by(RawFinancial.id)
        .offset(offset)
        .limit(limit)
        .all()
    )
    return [
        {
            "id": item.id,
            "source": item.source,
            "description": item.description,
            "amount": float(item.amount),
            "date": item.date,
        }
        for item in items
    ]


@app.get("/financial/summary")
def get_summary(db: Session = Depends(get_db)):
    income, expenses, count = db.query(
        func.coalesce(func.sum(case((RawFinancial.amount > 0, RawFinancial.amount), else_=0)), 0),
        func.coalesce(func.sum(case((RawFinancial.amount < 0, RawFinancial.amount), else_=0)), 0),
        func.count(RawFinancial.id),
    ).one()
    income, expenses = float(income), float(expenses)
    return {
        "income": income,
        "expenses": expenses,
        "balance": income + expenses,
        "count": count,
    }
