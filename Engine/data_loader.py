import pandas as pd

class DataLoader:
    def load_data(self, path):
        if path.endswith(".parquet"):
            return pd.read_parquet(path)
        elif path.endswith(".csv"):
            return pd.read_csv(path)
        else:
            raise ValueError("Unsupported file format")
