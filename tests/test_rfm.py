import pytest

from segmentiq.clean import clean_df
from segmentiq.rfm import create_rfm_table


def test_rfm_table_has_only_paying_customers(raw_df):
    rfm = create_rfm_table(clean_df(raw_df))
    assert list(rfm.columns) == ["Recency", "Frequency", "Monetary"]
    assert rfm.index.name == "CustomerID"
    assert list(rfm.index) == [13748, 17850]
    assert rfm.isna().sum().sum() == 0


def test_cancellations_change_money_but_not_recency_and_frequency(raw_df):
    df = raw_df.copy()
    df.loc[df["InvoiceNo"] == "C536379", "CustomerID"] = 17850.0
    rfm = create_rfm_table(clean_df(df))
    assert rfm.loc[17850, "Recency"] == 1
    assert rfm.loc[17850, "Frequency"] == 2
    assert rfm.loc[17850, "Monetary"] == pytest.approx(46.74 - 4.25)
    assert rfm.loc[13748, "Recency"] == 360
