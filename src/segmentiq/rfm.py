import pandas as pd


def create_rfm_table(df):
    snapshot_date = df["InvoiceDate"].max() + pd.DateOffset(days=1)
    monetary = df.groupby("CustomerID").agg(Monetary=("Revenue", "sum"))
    # not > 0 because of the approximation some values are very low but not zero. >0.1 delete all these problems
    monetary = monetary[monetary["Monetary"] > 0.1]
    df_without_cancellations = df[df["InvoiceNo"].str[0] != "C"]
    rf = df_without_cancellations.groupby("CustomerID").agg(
        Recency=("InvoiceDate", lambda x: (snapshot_date - x.max()).days),
        Frequency=("InvoiceNo", "nunique"),
    )
    rfm = rf.merge(monetary, on="CustomerID", how="inner")
    return rfm
