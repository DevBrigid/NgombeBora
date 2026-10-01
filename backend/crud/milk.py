from backend.extensions import db
from backend.models import MilkRecord


def list_milk_records(limit=200):
    return MilkRecord.query.order_by(MilkRecord.date.desc(), MilkRecord.id.desc()).limit(limit).all()


def create_milk_record(data):
    record = MilkRecord(**data)
    db.session.add(record)
    db.session.commit()
    return record
