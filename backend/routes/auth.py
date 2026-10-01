from flask import jsonify, request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from backend.extensions import db
from backend.models import User
from backend.routes import api
from backend.schemas.auth import validate_login, validate_registration


@api.post("/auth/register")
def register():
    try:
        data = validate_registration(request.get_json(silent=True) or {})
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "An account with this email already exists"}), 409
    user = User(name=data["name"], email=data["email"])
    user.set_password(data["password"])
    db.session.add(user)
    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        return jsonify({"error": "Could not create account. Please try again."}), 409
    token = create_access_token(identity=str(user.id))
    return jsonify({"access_token": token, "user": user.to_dict()}), 201


@api.post("/auth/login")
def login():
    try:
        data = validate_login(request.get_json(silent=True) or {})
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    user = User.query.filter_by(email=data["email"]).first()
    if not user or not user.check_password(data["password"]):
        return jsonify({"error": "Email or password is incorrect"}), 401
    token = create_access_token(identity=str(user.id))
    return jsonify({"access_token": token, "user": user.to_dict()})


@api.get("/auth/me")
@jwt_required()
def current_user():
    user = db.session.get(User, int(get_jwt_identity()))
    if not user:
        return jsonify({"error": "Account not found"}), 404
    return jsonify(user.to_dict())


@api.patch("/auth/me")
@jwt_required()
def update_current_user():
    from backend.schemas.auth import validate_profile_update

    user = db.session.get(User, int(get_jwt_identity()))
    if not user:
        return jsonify({"error": "Account not found"}), 404
    try:
        updates = validate_profile_update(request.get_json(silent=True) or {})
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    duplicate = User.query.filter(User.email == updates["email"], User.id != user.id).first()
    if duplicate:
        return jsonify({"error": "That email address is already in use"}), 409
    user.name = updates["name"]
    user.email = updates["email"]
    db.session.commit()
    return jsonify(user.to_dict())


@api.post("/auth/change-password")
@jwt_required()
def change_password():
    from backend.schemas.auth import validate_password_update

    user = db.session.get(User, int(get_jwt_identity()))
    if not user:
        return jsonify({"error": "Account not found"}), 404
    try:
        data = validate_password_update(request.get_json(silent=True) or {})
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    if not user.check_password(data["current_password"]):
        return jsonify({"error": "Current password is incorrect"}), 400
    user.set_password(data["new_password"])
    db.session.commit()
    return jsonify({"message": "Password updated successfully"})
