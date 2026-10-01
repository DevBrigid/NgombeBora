from flask import jsonify, request
from flask_jwt_extended import jwt_required
from backend.crud.milk import create_milk_record, list_milk_records
from backend.routes import api
from backend.schemas.milk import validate_milk_record


@api.get("/milk")
@jwt_required()
def get_milk_records():
    return jsonify([entry.to_dict() for entry in list_milk_records()])


@api.post("/milk")
@jwt_required()
def add_milk_record():
    try:
        entry = create_milk_record(validate_milk_record(request.get_json(silent=True) or {}))
        return jsonify(entry.to_dict()), 201
    except ValueError as exc:
        from backend.extensions import db
        db.session.rollback()
        return jsonify({"error": str(exc)}), 400
