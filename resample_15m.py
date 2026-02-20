import pandas as pd
import glob

files = glob.glob("data/raw/bootstrap/*.csv")
print("Found files:", len(files))

cols = [
    "open_time","open","high","low","close","volume",
    "close_time","quote_asset_volume","num_trades",
    "taker_buy_base","taker_buy_quote","ignore"
]

dfs = []

for f in files:
    df_temp = pd.read_csv(f, header=None, names=cols)
    dfs.append(df_temp)

df = pd.concat(dfs)

# Convert numeric first
df["open_time"] = pd.to_numeric(df["open_time"])

# Convert microseconds → datetime
df["open_time"] = pd.to_datetime(df["open_time"], unit="us", utc=True)

# Convert to readable format (DD-MM-YYYY HH:MM:SS)
df["open_time"] = df["open_time"].dt.strftime("%d-%m-%Y %H:%M:%S")

# Keep only required columns
df = df[["open_time","open","high","low","close","volume"]]

df.sort_values("open_time", inplace=True)
df.drop_duplicates(subset=["open_time"], inplace=True)

df.to_csv("data/Processed/final_15m_1year.csv", index=False)

print("Final Rows:", len(df))