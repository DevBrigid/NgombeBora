from flask import Blueprint

api = Blueprint("api", __name__, url_prefix="/api")

from backend.routes import auth, cows, dashboard, finance, milk  # noqa: E402,F401
