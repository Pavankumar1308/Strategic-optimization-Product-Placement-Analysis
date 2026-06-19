"""
eda.py
Exploratory Data Analysis script for the retail placement dataset.
Generates business insight summaries matching the project documentation.
Usage: python eda.py --file data/placement_data.csv
"""
import argparse
import pandas as pd


def run_eda(file_path: str):
    df = pd.read_csv(file_path)
    df.drop_duplicates(inplace=True)
    df.fillna(method="ffill", inplace=True)

    print("Shape:", df.shape)
    print("\n--- Avg Sales Volume by Product Category ---")
    print(df.groupby("Product Category")["Sales Volume"].mean().round(1))

    print("\n--- Avg Sales Volume by Product Position ---")
    print(df.groupby("Product Position")["Sales Volume"].mean().round(1))

    print("\n--- Avg Sales Volume by Foot Traffic ---")
    print(df.groupby("Foot Traffic")["Sales Volume"].mean().round(1))

    print("\n--- Promotion Impact on Sales ---")
    print(df.groupby("Promotion")["Sales Volume"].mean().round(1))

    print("\n--- Seasonal Impact on Sales ---")
    print(df.groupby("Seasonal")["Sales Volume"].mean().round(1))

    print("\n--- Top Combination: Category x Position ---")
    print(
        df.groupby(["Product Category", "Product Position"])["Sales Volume"]
        .mean()
        .sort_values(ascending=False)
        .head(5)
        .round(1)
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", required=True)
    args = parser.parse_args()
    run_eda(args.file)
