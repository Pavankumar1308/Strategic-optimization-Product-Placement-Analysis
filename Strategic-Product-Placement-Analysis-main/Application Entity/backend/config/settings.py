import os
from datetime import timedelta

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", "password"),
    "database": os.getenv("DB_NAME", "sppa_db"),
}

SQLALCHEMY_DATABASE_URI = (
    f"mysql+pymysql://{DB_CONFIG['user']}:{DB_CONFIG['password']}"
    f"@{DB_CONFIG['host']}/{DB_CONFIG['database']}"
)

SECRET_KEY = os.getenv("SECRET_KEY", "change-this-secret-key")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "change-this-jwt-secret")
JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=8)

MODEL_PATH = os.path.join(BASE_DIR, "app", "ml", "sales_model.pkl")
ENCODER_PATH = os.path.join(BASE_DIR, "app", "ml", "encoders.pkl")
