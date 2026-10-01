from decimal import Decimal
from backend.extensions import db
from backend.models import FinanceEntry


def list_finance_entries(start=None, end=None, entry_type=None):
    query = FinanceEntry.query
    if start:
        query = query.filter(FinanceEntry.date >= start)
    if end:
        query = query.filter(FinanceEntry.date <= end)
    if entry_type in ("income", "expenditure"):
        query = query.filter_by(type=entry_type)
    return query.order_by(FinanceEntry.date.desc(), FinanceEntry.id.desc()).all()


def finance_totals(entries):
    income = sum((row.amount for row in entries if row.type == "income"), Decimal("0"))
    expenditure = sum((row.amount for row in entries if row.type == "expenditure"), Decimal("0"))
    return {"income": float(income), "expenditure": float(expenditure), "net": float(income - expenditure)}


def create_finance_entry(data):
    entry = FinanceEntry(**data)
    db.session.add(entry)
    db.session.commit()
    return entry
