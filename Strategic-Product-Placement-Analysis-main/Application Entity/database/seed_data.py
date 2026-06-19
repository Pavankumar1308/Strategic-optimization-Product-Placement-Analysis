"""
seed_data.py
Loads the retail placement dataset (CSV/Excel) into the MySQL database.
Usage: python seed_data.py --file data/placement_data.csv
"""
import argparse
import pandas as pd
import mysql.connector
from backend.config.settings import DB_CONFIG


def get_connection():
    return mysql.connector.connect(**DB_CONFIG)


def seed(file_path: str):
    df = pd.read_csv(file_path)

    # Basic cleaning (matches Preprocessing_Steps PDF)
    df.drop_duplicates(inplace=True)
    df.fillna(method="ffill", inplace=True)

    conn = get_connection()
    cursor = conn.cursor()

    for _, row in df.iterrows():
        cursor.execute(
            """INSERT INTO products (product_code, product_category, price, competitor_price)
               VALUES (%s, %s, %s, %s)""",
            (row["Product ID"], row["Product Category"], row["Price"], row["Competitor's Price"]),
        )
        product_id = cursor.lastrowid

        cursor.execute(
            """INSERT INTO sales_records
               (product_id, product_position, promotion, foot_traffic,
                consumer_demographic, seasonal, sales_volume)
               VALUES (%s, %s, %s, %s, %s, %s, %s)""",
            (
                product_id,
                row["Product Position"],
                row["Promotion"],
                row["Foot Traffic"],
                row["Consumer Demographics"],
                row["Seasonal"],
                row["Sales Volume"],
            ),
        )

    conn.commit()
    cursor.close()
    conn.close()
    print(f"Seeded {len(df)} records successfully.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", required=True, help="Path to dataset CSV file")
    args = parser.parse_args()
    seed(args.file)
