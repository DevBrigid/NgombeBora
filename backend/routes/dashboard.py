from flask import jsonify
from backend.crud.dashboard import dashboard_summary
from backend.routes import api


@api.get("/dashboard")
def get_dashboard():
    return jsonify(dashboard_summary())
