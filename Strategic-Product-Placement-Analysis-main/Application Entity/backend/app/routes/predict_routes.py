from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.models import db, Prediction
from app.ml.predict import predict_sales

predict_bp = Blueprint("predict", __name__, url_prefix="/api/predict")


@predict_bp.route("/sales", methods=["POST"])
@jwt_required()
def predict_sales_route():
    data = request.get_json()
    required = [
        "Product Position", "Promotion", "Foot Traffic",
        "Consumer Demographics", "Product Category", "Seasonal",
        "Price", "Competitor's Price",
    ]
    missing = [k for k in required if k not in data]
    if missing:
        return jsonify({"error": f"Missing fields: {missing}"}), 400

    predicted_value = predict_sales(data)

    user_id = get_jwt_identity()
    record = Prediction(
        user_id=user_id,
        product_category=data["Product Category"],
        product_position=data["Product Position"],
        promotion=data["Promotion"],
        foot_traffic=data["Foot Traffic"],
        seasonal=data["Seasonal"],
        predicted_sales_volume=predicted_value,
    )
    db.session.add(record)
    db.session.commit()

    return jsonify({"predicted_sales_volume": predicted_value})


@predict_bp.route("/history", methods=["GET"])
@jwt_required()
def history():
    user_id = get_jwt_identity()
    records = (
        Prediction.query.filter_by(user_id=user_id)
        .order_by(Prediction.created_at.desc())
        .limit(20)
        .all()
    )
    return jsonify([
        {
            "category": r.product_category,
            "position": r.product_position,
            "predicted_sales_volume": float(r.predicted_sales_volume),
            "created_at": r.created_at.isoformat(),
        }
        for r in records
    ])
