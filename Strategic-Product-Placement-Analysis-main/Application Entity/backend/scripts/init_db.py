"""
init_db.py
Creates all database tables using SQLAlchemy models (alternative to schema.sql).
Usage: python init_db.py
"""
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from app.models.models import db

app = create_app()
with app.app_context():
    db.create_all()
    print("All tables created successfully.")
