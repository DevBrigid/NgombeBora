from datetime import datetime
from sqlalchemy import CheckConstraint
from backend.extensions import db


class Cow(db.Model):
    __tablename__ = "cows"
    id = db.Column(db.Integer, primary_key=True)
    serial_number = db.Column(db.String(80), unique=True, nullable=False, index=True)
    name = db.Column(db.String(120), nullable=False)
    breed = db.Column(db.String(100))
    sex = db.Column(db.String(10), nullable=False)
    date_of_birth = db.Column(db.Date)
    birth_weight = db.Column(db.Numeric(8, 2))
    acquisition_type = db.Column(db.String(12), nullable=False)
    status = db.Column(db.String(12), nullable=False, default="active")
    mother_id = db.Column(db.Integer, db.ForeignKey("cows.id"))
    sire_id = db.Column(db.Integer, db.ForeignKey("cows.id"))
    sire_external = db.Column(db.String(160))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    mother = db.relationship("Cow", remote_side=[id], foreign_keys=[mother_id], backref="calves")
    sire = db.relationship("Cow", remote_side=[id], foreign_keys=[sire_id])
    __table_args__ = (
        CheckConstraint("sex IN ('male','female')", name="ck_cow_sex"),
        CheckConstraint("acquisition_type IN ('born','purchased')", name="ck_cow_acquisition"),
        CheckConstraint("status IN ('active','sold','deceased')", name="ck_cow_status"),
        CheckConstraint("NOT (sire_id IS NOT NULL AND sire_external IS NOT NULL)", name="ck_cow_single_sire"),
    )

    def to_dict(self):
        return {
            "id": self.id, "serial_number": self.serial_number, "name": self.name,
            "breed": self.breed, "sex": self.sex,
            "date_of_birth": self.date_of_birth.isoformat() if self.date_of_birth else None,
            "birth_weight": float(self.birth_weight) if self.birth_weight is not None else None,
            "acquisition_type": self.acquisition_type, "status": self.status,
            "mother_id": self.mother_id, "mother_name": self.mother.name if self.mother else None,
            "sire_id": self.sire_id, "sire_external": self.sire_external,
            "created_at": self.created_at.isoformat(),
        }
