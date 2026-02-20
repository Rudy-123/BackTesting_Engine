import pandas as pd
import glob
import os

# CONFIG
BOOTSTRAP_PATH = "data/raw/bootstrap/*.csv"
LIVE_PATH = "data/raw/symbol=BTCUSDT/*.csv"
OUTPUT_DIR = "data/processed"

os.makedirs(OUTPUT_DIR, exist_ok=True)

columns = [
    "open_time", "open", "high", "low", "close", "volume",
    "close_time", "quote_asset_volume", "number_of_trades",
    "taker_buy_base_volume", "taker_buy_quote_volume", "ignore"
]

# LOAD BOOTSTRAP 

bootstrap_files = glob.glob(BOOTSTRAP_PATH)
bootstrap_list = []

for file in bootstrap_files:
    df = pd.read_csv(file, header=None, names=columns)
    df = df[["open_time", "open", "high", "low", "close", "volume"]]

    # Convert microseconds → datetime
    df["open_time"] = pd.to_datetime(df["open_time"], unit="us", utc=True)

    bootstrap_list.append(df)

bootstrap_df = pd.concat(bootstrap_list, ignore_index=True) if bootstrap_list else pd.DataFrame()

print("Bootstrap rows:", len(bootstrap_df))

# ------------------ LOAD LIVE ------------------

live_files = glob.glob(LIVE_PATH)
live_list = []

for file in live_files:
    df = pd.read_csv(file)

    if "timestamp" in df.columns:
        df.rename(columns={"timestamp": "open_time"}, inplace=True)

    df = df[["open_time", "open", "high", "low", "close", "volume"]]

    # Convert string → datetime
    df["open_time"] = pd.to_datetime(df["open_time"], utc=True)

    live_list.append(df)

live_df = pd.concat(live_list, ignore_index=True) if live_list else pd.DataFrame()

print("Live rows:", len(live_df))

# ------------------ MERGE ------------------

combined = pd.concat([bootstrap_df, live_df], ignore_index=True)

# Convert numeric columns properly
for col in ["open","high","low","close","volume"]:
    combined[col] = pd.to_numeric(combined[col], errors="coerce")

combined.dropna(inplace=True)

combined.drop_duplicates(subset=["open_time"], inplace=True)

combined.sort_values("open_time", inplace=True)

print("Total merged rows:", len(combined))

# ------------------ SAVE ------------------

parquet_path = os.path.join(OUTPUT_DIR, "final_dataset.parquet")
csv_path = os.path.join(OUTPUT_DIR, "final_dataset.csv")

combined.to_parquet(parquet_path, index=False)
combined.to_csv(csv_path, index=False)

print("Final dataset overwritten successfully")