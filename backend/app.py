from flask import Flask, jsonify
from flask_cors import CORS
from backend.config import Config
from backend.extensions import db, migrate, jwt
from backend import models  # noqa: F401 - register model metadata for Alembic
from backend.routes import api


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    CORS(app)

    @app.get("/")
    def index():
        return {"message": "NgombeBora API is running", "version": 1}

    @app.get("/api/health")
    def health():
        return {"status": "ok"}

    @app.errorhandler(404)
    def not_found(_error):
        return jsonify({"error": "Route not found"}), 404

    app.register_blueprint(api)
    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=app.config.get("DEBUG", False))
