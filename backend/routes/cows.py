from flask import jsonify, request
from flask_jwt_extended import jwt_required
from backend.crud.cows import add_newborn, add_purchased, list_cows, update_status
from backend.routes import api
from backend.schemas.cow import validate_newborn, validate_purchased_cow


@api.get("/cows")
@jwt_required()
def get_cows():
    return jsonify([cow.to_dict() for cow in list_cows(request.args.get("status"))])


@api.post("/cows/purchased")
@jwt_required()
def create_purchased_cow():
    try:
        cow = add_purchased(validate_purchased_cow(request.get_json(silent=True) or {}))
        return jsonify(cow.to_dict()), 201
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400


@api.post("/cows/newborn")
@jwt_required()
def create_newborn_cow():
    try:
        cow = add_newborn(validate_newborn(request.get_json(silent=True) or {}))
        return jsonify(cow.to_dict()), 201
    except ValueError as exc:
        from backend.extensions import db
        db.session.rollback()
        return jsonify({"error": str(exc)}), 400


@api.patch("/cows/<int:cow_id>/status")
@jwt_required()
def change_cow_status(cow_id):
    try:
        cow = update_status(cow_id, (request.get_json(silent=True) or {}).get("status"))
        if not cow:
            return jsonify({"error": "Cow not found"}), 404
        return jsonify(cow.to_dict())
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
