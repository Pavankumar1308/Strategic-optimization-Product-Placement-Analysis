from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default="analyst")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Product(db.Model):
    __tablename__ = "products"
    product_id = db.Column(db.Integer, primary_key=True)
    product_code = db.Column(db.Integer, nullable=False)
    product_category = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Numeric(8, 2), nullable=False)
    competitor_price = db.Column(db.Numeric(8, 2), nullable=False)
    sales = db.relationship("SalesRecord", backref="product", lazy=True)


class SalesRecord(db.Model):
    __tablename__ = "sales_records"
    record_id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("products.product_id"), nullable=False)
    product_position = db.Column(db.String(50), nullable=False)
    promotion = db.Column(db.String(10), nullable=False)
    foot_traffic = db.Column(db.String(20), nullable=False)
    consumer_demographic = db.Column(db.String(50), nullable=False)
    seasonal = db.Column(db.String(10), nullable=False)
    sales_volume = db.Column(db.Integer, nullable=False)
    record_date = db.Column(db.Date, default=datetime.utcnow)


class Prediction(db.Model):
    __tablename__ = "predictions"
    prediction_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    product_category = db.Column(db.String(50))
    product_position = db.Column(db.String(50))
    promotion = db.Column(db.String(10))
    foot_traffic = db.Column(db.String(20))
    seasonal = db.Column(db.String(10))
    predicted_sales_volume = db.Column(db.Numeric(10, 2))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Feedback(db.Model):
    __tablename__ = "feedback"
    feedback_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
