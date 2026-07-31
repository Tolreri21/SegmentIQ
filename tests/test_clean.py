from segmentiq.clean import clean_df


def test_clean_df_drops_bad_rows(raw_df):
    cleaned = clean_df(raw_df)
    assert len(cleaned) == 6
    assert cleaned["CustomerID"].isna().sum() == 0
    assert cleaned["CustomerID"].dtype == "int64"
    assert "POST" not in cleaned["StockCode"].values
    assert "581483" not in cleaned["InvoiceNo"].values
    assert cleaned.duplicated().sum() == 0


def test_clean_df_keeps_cancellations_and_adds_revenue(raw_df):
    cleaned = clean_df(raw_df)
    assert "C536379" in cleaned["InvoiceNo"].values
    assert (cleaned["UnitPrice"] == 0).sum() == 1
    assert (cleaned["Revenue"] == cleaned["Quantity"] * cleaned["UnitPrice"]).all()
    assert "Revenue" not in raw_df.columns
