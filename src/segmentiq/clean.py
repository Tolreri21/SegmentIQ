CODES = ["POST", "M", "DOT", "D", "CRUK", "C2", "BANK CHARGES"]
OUTLIERS = ["C581484", "C541433", "581483", "541431"]


def clean_df(df):
    new_df = df.dropna(subset=["CustomerID"])
    new_df["CustomerID"] = new_df["CustomerID"].astype(int)
    new_df = new_df[~new_df["StockCode"].isin(CODES)]
    new_df.drop_duplicates(inplace=True)
    new_df = new_df[~new_df["InvoiceNo"].astype(str).isin(OUTLIERS)]
    new_df["Revenue"] = new_df["UnitPrice"] * new_df["Quantity"]
    return new_df
