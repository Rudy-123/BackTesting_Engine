import pandas as pd
import os

def convert_partitioned(csv_path, out_dir):
    df = pd.read_csv(csv_path)
    df.columns = df.columns.str.strip().str.lower()
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
    # partition key
    df["year"] = df["timestamp"].dt.year
    os.makedirs(out_dir, exist_ok=True)
    # write partitioned parquet
    df.to_parquet(
        out_dir,
        engine="pyarrow",
        partition_cols=["year"],
        compression="snappy",
        index=False
    )
if __name__ == "__main__":
    convert_partitioned(
        "data/raw/sample_data.csv",
        "data/parquet/market_data/"
    )
