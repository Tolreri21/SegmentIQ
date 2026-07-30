import pandas as pd


def load_raw(path):
    return pd.read_excel(
        io=path,
        sheet_name="Online Retail",
        dtype={"InvoiceNo": str, "StockCode": str, "Description": str},
    )


def get_data(raw_path, cache_path):
    if cache_path.exists():
        return pd.read_parquet(cache_path)

    df = load_raw(raw_path)
    df.to_parquet(cache_path)
    return df
