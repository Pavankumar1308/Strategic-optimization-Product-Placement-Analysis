"""
train_model.py
Data preprocessing + ML training pipeline for predicting Sales Volume
based on product placement attributes (Strategic Product Placement Analysis).

Model: RandomForestRegressor
Pipeline: Label Encoding (categoricals) -> Train/Test Split -> Model Fit -> Evaluation -> Save (pickle)
"""
import argparse
import pickle
import os
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_absolute_error, r2_score

CATEGORICAL_COLS = [
    "Product Position",
    "Promotion",
    "Foot Traffic",
    "Consumer Demographics",
    "Product Category",
    "Seasonal",
]
NUMERIC_COLS = ["Price", "Competitor's Price"]
TARGET_COL = "Sales Volume"

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(CURRENT_DIR, "sales_model.pkl")
ENCODER_PATH = os.path.join(CURRENT_DIR, "encoders.pkl")


def preprocess(df: pd.DataFrame):
    df = df.copy()
    df.drop_duplicates(inplace=True)
    df.fillna(method="ffill", inplace=True)

    encoders = {}
    for col in CATEGORICAL_COLS:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col].astype(str))
        encoders[col] = le

    X = df[CATEGORICAL_COLS + NUMERIC_COLS]
    y = df[TARGET_COL]
    return X, y, encoders


def train(file_path: str):
    df = pd.read_csv(file_path)
    X, y, encoders = preprocess(df)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = RandomForestRegressor(n_estimators=200, max_depth=10, random_state=42)
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    mae = mean_absolute_error(y_test, preds)
    r2 = r2_score(y_test, preds)
    print(f"Model trained. MAE={mae:.2f}, R2={r2:.3f}")

    with open(MODEL_PATH, "wb") as f:
        pickle.dump(model, f)
    with open(ENCODER_PATH, "wb") as f:
        pickle.dump(encoders, f)

    print(f"Saved model to {MODEL_PATH}")
    print(f"Saved encoders to {ENCODER_PATH}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", required=True, help="Path to training CSV")
    args = parser.parse_args()
    train(args.file)
