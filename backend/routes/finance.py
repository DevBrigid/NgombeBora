from flask import jsonify, request
from flask_jwt_extended import jwt_required
from backend.crud.finance import create_finance_entry, finance_totals, list_finance_entries
from backend.routes import api
from backend.schemas.common import parse_date
from backend.schemas.finance import FINANCE_CATEGORIES, validate_finance_entry


@api.get("/finance/categories")
@jwt_required()
def get_finance_categories():
    return jsonify(sorted(FINANCE_CATEGORIES))


@api.get("/finance")
@jwt_required()
def get_finance_entries():
    try:
        start = parse_date(request.args.get("start"), "start", False)
        end = parse_date(request.args.get("end"), "end", False)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    entries = list_finance_entries(start, end, request.args.get("type"))
    return jsonify({"entries": [entry.to_dict() for entry in entries], "totals": finance_totals(entries)})


@api.post("/finance")
@jwt_required()
def add_finance_entry():
    try:
        entry = create_finance_entry(validate_finance_entry(request.get_json(silent=True) or {}))
        return jsonify(entry.to_dict()), 201
    except ValueError as exc:
        from backend.extensions import db
        db.session.rollback()
        return jsonify({"error": str(exc)}), 400
