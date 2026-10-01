from flask import Blueprint

api = Blueprint("api", __name__, url_prefix="/api")

from backend.routes import cows, dashboard, finance, milk  # noqa: E402,F401
