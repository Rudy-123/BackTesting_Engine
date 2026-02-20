import pandas as pd
def convert(csv_path,parquet_path):
    df=pd.read_csv(csv_path)
    df["timestamp"] = pd.to_datetime(
        df["timestamp"],
        format="%Y-%m-%d %H:%M:%S",
        utc=True
    )
    df.to_parquet(
        parquet_path,
        engine="pyarrow",
        compression="snappy", #compressor for fast compression
        index=False
    )
if __name__ == "__main__":
    convert(
        "data/raw/sample_data.csv",
        "data/parquet/sample_data.parquet"
    )