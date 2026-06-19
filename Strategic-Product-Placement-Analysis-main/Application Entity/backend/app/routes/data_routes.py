from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from sqlalchemy import func
from app.models.models import db, Product, SalesRecord

data_bp = Blueprint("data", __name__, url_prefix="/api/data")


@data_bp.route("/products", methods=["GET"])
@jwt_required()
def list_products():
    products = Product.query.limit(100).all()
    return jsonify([
        {
            "product_id": p.product_id,
            "product_code": p.product_code,
            "category": p.product_category,
            "price": float(p.price),
            "competitor_price": float(p.competitor_price),
        }
        for p in products
    ])


@data_bp.route("/sales", methods=["GET"])
@jwt_required()
def list_sales():
    category = request.args.get("category")
    position = request.args.get("position")

    query = db.session.query(SalesRecord, Product).join(
        Product, SalesRecord.product_id == Product.product_id
    )
    if category:
        query = query.filter(Product.product_category == category)
    if position:
        query = query.filter(SalesRecord.product_position == position)

    results = query.limit(200).all()
    return jsonify([
        {
            "record_id": s.record_id,
            "category": p.product_category,
            "position": s.product_position,
            "promotion": s.promotion,
            "foot_traffic": s.foot_traffic,
            "demographic": s.consumer_demographic,
            "seasonal": s.seasonal,
            "sales_volume": s.sales_volume,
            "price": float(p.price),
        }
        for s, p in results
    ])


@data_bp.route("/analytics/summary", methods=["GET"])
@jwt_required()
def summary():
    """Avg sales volume by product category - powers dashboard charts"""
    rows = (
        db.session.query(
            Product.product_category,
            func.avg(SalesRecord.sales_volume).label("avg_sales"),
            func.count(SalesRecord.record_id).label("count"),
        )
        .join(SalesRecord, SalesRecord.product_id == Product.product_id)
        .group_by(Product.product_category)
        .all()
    )
    return jsonify([
        {"category": r.product_category, "avg_sales": round(float(r.avg_sales), 1), "count": r.count}
        for r in rows
    ])


@data_bp.route("/analytics/by-position", methods=["GET"])
@jwt_required()
def by_position():
    rows = (
        db.session.query(
            SalesRecord.product_position,
            func.avg(SalesRecord.sales_volume).label("avg_sales"),
        )
        .group_by(SalesRecord.product_position)
        .all()
    )
    return jsonify([
        {"position": r.product_position, "avg_sales": round(float(r.avg_sales), 1)}
        for r in rows
    ])


@data_bp.route("/analytics/foot-traffic", methods=["GET"])
@jwt_required()
def by_foot_traffic():
    rows = (
        db.session.query(
            SalesRecord.foot_traffic,
            func.avg(SalesRecord.sales_volume).label("avg_sales"),
        )
        .group_by(SalesRecord.foot_traffic)
        .all()
    )
    return jsonify([
        {"foot_traffic": r.foot_traffic, "avg_sales": round(float(r.avg_sales), 1)}
        for r in rows
    ])
