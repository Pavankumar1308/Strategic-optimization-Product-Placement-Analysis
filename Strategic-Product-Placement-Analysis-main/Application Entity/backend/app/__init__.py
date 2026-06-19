from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from app.models.models import db
from config import settings


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = settings.SQLALCHEMY_DATABASE_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = settings.JWT_SECRET_KEY
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = settings.JWT_ACCESS_TOKEN_EXPIRES
    app.config["SECRET_KEY"] = settings.SECRET_KEY

    CORS(app)
    db.init_app(app)
    JWTManager(app)

    from app.routes.auth_routes import auth_bp
    from app.routes.data_routes import data_bp
    from app.routes.predict_routes import predict_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(data_bp)
    app.register_blueprint(predict_bp)

    @app.route("/api/health")
    def health():
        return {"status": "ok", "service": "SPPA backend"}

    return app
