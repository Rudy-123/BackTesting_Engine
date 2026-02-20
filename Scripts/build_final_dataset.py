import pandas as pd
import glob
import os

# PATH CONFIG

BOOTSTRAP_PATH = "data/raw/bootstrap/*.csv"
LIVE_PATH = "data/raw/symbol=BTCUSDT/*.csv"
OUTPUT_DIR = "data/processed"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Binance bootstrap column format
columns = [
    "open_time", "open", "high", "low", "close", "volume",
    "close_time", "quote_asset_volume", "number_of_trades",
    "taker_buy_base_volume", "taker_buy_quote_volume", "ignore"
]

# LOAD BOOTSTRAP FILES

bootstrap_files = glob.glob(BOOTSTRAP_PATH)
bootstrap_list = []

for file in bootstrap_files:
    df = pd.read_csv(file, header=None, names=columns)
    df = df[["open_time", "open", "high", "low", "close", "volume"]]
    bootstrap_list.append(df)

if bootstrap_list:
    bootstrap_df = pd.concat(bootstrap_list, ignore_index=True)
else:
    bootstrap_df = pd.DataFrame(columns=["open_time","open","high","low","close","volume"])

print("Bootstrap rows:", len(bootstrap_df))

# LOAD LIVE FILES

live_files = glob.glob(LIVE_PATH)
live_list = []

for file in live_files:
    df = pd.read_csv(file)

    if "timestamp" in df.columns:
        df.rename(columns={"timestamp": "open_time"}, inplace=True)

    df = df[["open_time", "open", "high", "low", "close", "volume"]]
    live_list.append(df)

if live_list:
    live_df = pd.concat(live_list, ignore_index=True)
else:
    live_df = pd.DataFrame(columns=["open_time","open","high","low","close","volume"])

print("Live rows:", len(live_df))

# FIX TIMESTAMPS PROPERLY


# Bootstrap timestamps (16-digit microseconds → ms → datetime)
bootstrap_df["open_time"] = pd.to_numeric(bootstrap_df["open_time"], errors="coerce")
bootstrap_df["open_time"] = bootstrap_df["open_time"] // 1000
bootstrap_df["open_time"] = pd.to_datetime(bootstrap_df["open_time"], unit="ms")

# Live timestamps (already datetime string)
live_df["open_time"] = pd.to_datetime(live_df["open_time"], errors="coerce")

# MERGE AFTER BOTH ARE DATETIME

combined = pd.concat([bootstrap_df, live_df], ignore_index=True)

# Clean numeric columns
for col in ["open", "high", "low", "close", "volume"]:
    combined[col] = pd.to_numeric(combined[col], errors="coerce")

combined = combined.dropna(subset=["open_time"])
combined = combined.dropna()

# Remove duplicates properly
combined = combined.drop_duplicates(subset=["open_time"])

# Sort correctly
combined = combined.sort_values(by="open_time")

print("Total merged rows:", len(combined))
print("Min date:", combined["open_time"].min())
print("Max date:", combined["open_time"].max())

# SAVE FINAL FILES

parquet_path = os.path.join(OUTPUT_DIR, "final_dataset.parquet")
csv_path = os.path.join(OUTPUT_DIR, "final_dataset.csv")

combined.to_parquet(parquet_path, index=False)
combined.to_csv(csv_path, index=False)

print("Final dataset overwritten successfully ✅")