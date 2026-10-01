from datetime import datetime
from backend.extensions import db


class MilkRecord(db.Model):
    __tablename__ = "milk_records"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False, index=True)
    quantity = db.Column(db.Numeric(10, 2), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    # Keep herd-wide records independent so nullable cow_id can be added later.

    def to_dict(self):
        return {"id": self.id, "date": self.date.isoformat(), "quantity": float(self.quantity),
                "created_at": self.created_at.isoformat()}
