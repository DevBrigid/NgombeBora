from datetime import date, datetime, timedelta
from decimal import Decimal, InvalidOperation
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint, func, or_
from config import Config


db = SQLAlchemy()
FINANCE_CATEGORIES = {"milk_sales", "livestock_sales", "feed", "vet", "breeding_cost", "labor", "equipment", "other"}


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

    def json(self):
        return {"id": self.id, "serial_number": self.serial_number, "name": self.name, "breed": self.breed,
                "sex": self.sex, "date_of_birth": self.date_of_birth.isoformat() if self.date_of_birth else None,
                "birth_weight": float(self.birth_weight) if self.birth_weight is not None else None,
                "acquisition_type": self.acquisition_type, "status": self.status, "mother_id": self.mother_id,
                "mother_name": self.mother.name if self.mother else None, "sire_id": self.sire_id,
                "sire_external": self.sire_external, "created_at": self.created_at.isoformat()}


class MilkRecord(db.Model):
    __tablename__ = "milk_records"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False, index=True)
    quantity = db.Column(db.Numeric(10, 2), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    # Herd-wide today; an optional cow_id can be added later without changing this contract.
    def json(self):
        return {"id": self.id, "date": self.date.isoformat(), "quantity": float(self.quantity), "created_at": self.created_at.isoformat()}


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
    def json(self):
        return {"id": self.id, "date": self.date.isoformat(), "type": self.type, "category": self.category,
                "amount": float(self.amount), "note": self.note, "created_at": self.created_at.isoformat()}


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    CORS(app)

    def error(message, status=400):
        return jsonify({"error": message}), status

    def parse_day(raw, field="date", required=True):
        if not raw:
            if required: raise ValueError(f"{field} is required")
            return None
        try: return date.fromisoformat(raw)
        except (TypeError, ValueError): raise ValueError(f"{field} must use YYYY-MM-DD")

    def parse_amount(raw, field, required=True):
        if raw in (None, "") and not required: return None
        try: value = Decimal(str(raw))
        except (InvalidOperation, ValueError): raise ValueError(f"{field} must be a valid number")
        if not value.is_finite() or value < 0: raise ValueError(f"{field} must be zero or greater")
        return value

    def body(): return request.get_json(silent=True) or {}

    @app.get("/")
    def index(): return {"message": "NgombeBora API is running", "version": 1}

    @app.get("/api/health")
    def health(): return {"status": "ok"}

    @app.get("/api/cows")
    def cows_list():
        query = Cow.query
        status = request.args.get("status")
        if status: query = query.filter_by(status=status)
        return jsonify([cow.json() for cow in query.order_by(Cow.created_at.desc()).all()])

    def root_serial():
        rows = db.session.query(Cow.serial_number).filter(Cow.mother_id.is_(None), Cow.serial_number.like("COW-%")).all()
        nums = [int(row[0][4:]) for row in rows if row[0][4:].isdigit()]
        return f"COW-{max(nums, default=0) + 1:04d}"

    @app.post("/api/cows/purchased")
    def create_purchased():
        data = body()
        try:
            name = str(data.get("name", "")).strip()
            sex = data.get("sex")
            dob = parse_day(data.get("date_of_birth"), "date_of_birth", False)
            if not name: return error("name is required")
            if sex not in ("male", "female"): return error("sex must be male or female")
            cow = Cow(serial_number=root_serial(), name=name, breed=(data.get("breed") or "").strip() or None,
                      sex=sex, date_of_birth=dob, acquisition_type="purchased")
            db.session.add(cow); db.session.commit()
            return jsonify(cow.json()), 201
        except ValueError as exc: db.session.rollback(); return error(str(exc))

    @app.post("/api/cows/newborn")
    def create_newborn():
        data = body()
        try:
            name = str(data.get("name", "")).strip(); sex = data.get("sex")
            if not name: return error("name is required")
            if sex not in ("male", "female"): return error("sex must be male or female")
            mother = db.session.get(Cow, data.get("mother_id"))
            if not mother: return error("Select a mother from the herd")
            if mother.sex != "female": return error("Mother must be female")
            sire_id = data.get("sire_id") or None
            sire_external = (data.get("sire_external") or "").strip() or None
            if sire_id and sire_external: return error("Choose an existing sire or an outside bull, not both")
            sire = db.session.get(Cow, sire_id) if sire_id else None
            if sire_id and not sire: return error("Selected sire was not found")
            if sire and sire.sex != "male": return error("Sire must be male")
            dob = parse_day(data.get("date_of_birth"), "date_of_birth")
            weight = parse_amount(data.get("birth_weight"), "birth_weight", False)
            serials = [row[0] for row in db.session.query(Cow.serial_number).filter(Cow.mother_id == mother.id).all()]
            sequence = max([int(s.rsplit("-", 1)[1]) for s in serials if s.rsplit("-", 1)[-1].isdigit()] or [0]) + 1
            cow = Cow(serial_number=f"{mother.serial_number}-{sequence:02d}", name=name,
                      breed=(data.get("breed") or mother.breed or "").strip() or None, sex=sex,
                      date_of_birth=dob, birth_weight=weight, acquisition_type="born", mother_id=mother.id,
                      sire_id=sire.id if sire else None, sire_external=sire_external)
            db.session.add(cow); db.session.commit()
            return jsonify(cow.json()), 201
        except ValueError as exc: db.session.rollback(); return error(str(exc))

    @app.patch("/api/cows/<int:cow_id>/status")
    def update_cow_status(cow_id):
        cow = db.session.get(Cow, cow_id)
        if not cow: return error("Cow not found", 404)
        status = body().get("status")
        if status not in ("active", "sold", "deceased"): return error("status must be active, sold, or deceased")
        cow.status = status; db.session.commit(); return jsonify(cow.json())

    @app.get("/api/milk")
    def milk_list():
        return jsonify([entry.json() for entry in MilkRecord.query.order_by(MilkRecord.date.desc(), MilkRecord.id.desc()).limit(200).all()])

    @app.post("/api/milk")
    def milk_create():
        data = body()
        try:
            day = parse_day(data.get("date")); qty = parse_amount(data.get("quantity"), "quantity")
            if qty <= 0: return error("quantity must be greater than zero")
            entry = MilkRecord(date=day, quantity=qty); db.session.add(entry); db.session.commit()
            return jsonify(entry.json()), 201
        except ValueError as exc: db.session.rollback(); return error(str(exc))

    @app.get("/api/finance/categories")
    def categories(): return jsonify(sorted(FINANCE_CATEGORIES))

    @app.get("/api/finance")
    def finance_list():
        query = FinanceEntry.query
        try:
            start = parse_day(request.args.get("start"), "start", False)
            end = parse_day(request.args.get("end"), "end", False)
        except ValueError as exc: return error(str(exc))
        kind = request.args.get("type")
        if start: query = query.filter(FinanceEntry.date >= start)
        if end: query = query.filter(FinanceEntry.date <= end)
        if kind in ("income", "expenditure"): query = query.filter_by(type=kind)
        rows = query.order_by(FinanceEntry.date.desc(), FinanceEntry.id.desc()).all()
        income = sum((row.amount for row in rows if row.type == "income"), Decimal("0"))
        expenditure = sum((row.amount for row in rows if row.type == "expenditure"), Decimal("0"))
        return jsonify({"entries": [row.json() for row in rows], "totals": {"income": float(income), "expenditure": float(expenditure), "net": float(income-expenditure)}})

    @app.post("/api/finance")
    def finance_create():
        data = body()
        try:
            day = parse_day(data.get("date")); kind = data.get("type")
            if kind not in ("income", "expenditure"): return error("type must be income or expenditure")
            category = str(data.get("category", "")).strip()
            if category not in FINANCE_CATEGORIES: return error("Choose a valid finance category")
            amount = parse_amount(data.get("amount"), "amount")
            if amount <= 0: return error("amount must be greater than zero")
            entry = FinanceEntry(date=day, type=kind, category=category, amount=amount, note=(data.get("note") or "").strip() or None)
            db.session.add(entry); db.session.commit(); return jsonify(entry.json()), 201
        except ValueError as exc: db.session.rollback(); return error(str(exc))

    @app.get("/api/dashboard")
    def dashboard():
        today = date.today(); month_start = today.replace(day=1)
        active = Cow.query.filter_by(status="active")
        active_count = active.count()
        by_sex = {sex: active.filter_by(sex=sex).count() for sex in ("female", "male")}
        by_acquisition = {kind: active.filter_by(acquisition_type=kind).count() for kind in ("born", "purchased")}
        cutoff = today - timedelta(days=30)
        newborns = Cow.query.filter(Cow.acquisition_type == "born", Cow.date_of_birth >= cutoff, Cow.date_of_birth <= today).order_by(Cow.date_of_birth.desc()).all()
        milk = db.session.query(func.coalesce(func.sum(MilkRecord.quantity), 0)).filter(MilkRecord.date >= month_start, MilkRecord.date <= today).scalar()
        income = db.session.query(func.coalesce(func.sum(FinanceEntry.amount), 0)).filter(FinanceEntry.type == "income", FinanceEntry.date >= month_start, FinanceEntry.date <= today).scalar()
        expenses = db.session.query(func.coalesce(func.sum(FinanceEntry.amount), 0)).filter(FinanceEntry.type == "expenditure", FinanceEntry.date >= month_start, FinanceEntry.date <= today).scalar()
        return jsonify({"active_cows": active_count, "by_sex": by_sex, "by_acquisition": by_acquisition,
                        "recent_newborns": [cow.json() for cow in newborns],
                        "inactive_historical": {"sold": Cow.query.filter_by(status="sold").count(), "deceased": Cow.query.filter_by(status="deceased").count()},
                        "milk_this_month": float(milk), "net_income_this_month": float(Decimal(str(income))-Decimal(str(expenses)))})

    @app.errorhandler(404)
    def not_found(_): return error("Route not found", 404)

    with app.app_context(): db.create_all()
    return app


app = create_app()
if __name__ == "__main__": app.run(debug=app.config.get("DEBUG", False))
