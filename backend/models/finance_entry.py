from datetime import datetime
from sqlalchemy import CheckConstraint
from backend.extensions import db


class FinanceEntry(db.Model):
    __tablename__ = "finance_entries"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False, index=True)
    type = db.Column(db.String(12), nullable=False)
    category = db.Column(db.String(40), nullable=False)
    amount = db.Column(db.Numeric(12, 2), nullable=False)
    note = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    __table_args__ = (CheckConstraint("type IN ('income','expenditure')", name="ck_finance_type"),)

    def to_dict(self):
        return {"id": self.id, "date": self.date.isoformat(), "type": self.type,
                "category": self.category, "amount": float(self.amount), "note": self.note,
                "created_at": self.created_at.isoformat()}
