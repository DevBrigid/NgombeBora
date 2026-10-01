from datetime import date, timedelta
from backend.extensions import db
from backend.models import Cow


def list_cows(status=None):
    query = Cow.query
    if status:
        query = query.filter_by(status=status)
    return query.order_by(Cow.created_at.desc()).all()


def next_root_serial():
    rows = db.session.query(Cow.serial_number).filter(
        Cow.mother_id.is_(None), Cow.serial_number.like("COW-%")
    ).all()
    numbers = [int(row[0][4:]) for row in rows if row[0][4:].isdigit()]
    return f"COW-{max(numbers, default=0) + 1:04d}"


def add_purchased(data):
    cow = Cow(serial_number=next_root_serial(), acquisition_type="purchased", **data)
    db.session.add(cow)
    db.session.commit()
    return cow


def add_newborn(data):
    mother = db.session.get(Cow, data["mother_id"])
    if not mother:
        raise ValueError("Select a mother from the herd")
    if mother.sex != "female":
        raise ValueError("Mother must be female")
    sire = db.session.get(Cow, data["sire_id"]) if data["sire_id"] else None
    if data["sire_id"] and not sire:
        raise ValueError("Selected sire was not found")
    if sire and sire.sex != "male":
        raise ValueError("Sire must be male")
    serials = db.session.query(Cow.serial_number).filter(Cow.mother_id == mother.id).all()
    sequence = max([int(row[0].rsplit("-", 1)[1]) for row in serials
                    if row[0].rsplit("-", 1)[-1].isdigit()] or [0]) + 1
    cow = Cow(serial_number=f"{mother.serial_number}-{sequence:02d}",
              name=data["name"], sex=data["sex"], breed=data["breed"] or mother.breed,
              date_of_birth=data["date_of_birth"], birth_weight=data["birth_weight"],
              acquisition_type="born", mother_id=mother.id, sire_id=sire.id if sire else None,
              sire_external=data["sire_external"])
    db.session.add(cow)
    db.session.commit()
    return cow


def update_status(cow_id, status):
    cow = db.session.get(Cow, cow_id)
    if not cow:
        return None
    if status not in ("active", "sold", "deceased"):
        raise ValueError("status must be active, sold, or deceased")
    cow.status = status
    db.session.commit()
    return cow


def recent_newborns(days=30):
    today = date.today()
    return Cow.query.filter(Cow.acquisition_type == "born", Cow.date_of_birth >= today - timedelta(days=days),
                            Cow.date_of_birth <= today).order_by(Cow.date_of_birth.desc()).all()
