"""
predict.py
Loads trained model + encoders, and exposes a predict_sales() function
used by the Flask API to forecast sales volume for a given placement scenario.
"""
import pickle
import os
import pandas as pd

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(CURRENT_DIR, "sales_model.pkl")
ENCODER_PATH = os.path.join(CURRENT_DIR, "encoders.pkl")

_model = None
_encoders = None


def _load():
    global _model, _encoders
    if _model is None:
        with open(MODEL_PATH, "rb") as f:
            _model = pickle.load(f)
        with open(ENCODER_PATH, "rb") as f:
            _encoders = pickle.load(f)
    return _model, _encoders


def predict_sales(payload: dict) -> float:
    """
    payload keys required:
    Product Position, Promotion, Foot Traffic,
    Consumer Demographics, Product Category, Seasonal,
    Price, Competitor's Price
    """
    model, encoders = _load()

    row = {}
    for col in [
        "Product Position",
        "Promotion",
        "Foot Traffic",
        "Consumer Demographics",
        "Product Category",
        "Seasonal",
    ]:
        le = encoders[col]
        value = payload[col]
        if value not in le.classes_:
            value = le.classes_[0]
        row[col] = le.transform([value])[0]

    row["Price"] = payload["Price"]
    row["Competitor's Price"] = payload["Competitor's Price"]

    df = pd.DataFrame([row])
    prediction = model.predict(df)[0]
    return round(float(prediction), 2)
