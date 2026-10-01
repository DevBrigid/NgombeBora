from datetime import date
from decimal import Decimal
from sqlalchemy import func
from backend.extensions import db
from backend.models import Cow, FinanceEntry, MilkRecord
from backend.crud.cows import recent_newborns


def dashboard_summary():
    today = date.today()
    month_start = today.replace(day=1)
    active = Cow.query.filter_by(status="active")
    by_sex = {sex: active.filter_by(sex=sex).count() for sex in ("female", "male")}
    by_acquisition = {kind: active.filter_by(acquisition_type=kind).count() for kind in ("born", "purchased")}
    milk = db.session.query(func.coalesce(func.sum(MilkRecord.quantity), 0)).filter(
        MilkRecord.date >= month_start, MilkRecord.date <= today).scalar()
    income = db.session.query(func.coalesce(func.sum(FinanceEntry.amount), 0)).filter(
        FinanceEntry.type == "income", FinanceEntry.date >= month_start, FinanceEntry.date <= today).scalar()
    expenses = db.session.query(func.coalesce(func.sum(FinanceEntry.amount), 0)).filter(
        FinanceEntry.type == "expenditure", FinanceEntry.date >= month_start, FinanceEntry.date <= today).scalar()
    return {
        "active_cows": active.count(), "by_sex": by_sex, "by_acquisition": by_acquisition,
        "recent_newborns": [cow.to_dict() for cow in recent_newborns()],
        "inactive_historical": {"sold": Cow.query.filter_by(status="sold").count(),
                                 "deceased": Cow.query.filter_by(status="deceased").count()},
        "milk_this_month": float(milk),
        "net_income_this_month": float(Decimal(str(income)) - Decimal(str(expenses))),
    }
