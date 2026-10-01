from flask import jsonify
from flask_jwt_extended import jwt_required
from backend.crud.dashboard import dashboard_summary
from backend.routes import api


@api.get("/dashboard")
@jwt_required()
def get_dashboard():
    return jsonify(dashboard_summary())
