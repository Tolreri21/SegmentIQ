import pandas as pd
import pytest

COLUMNS = [
    "InvoiceNo",
    "StockCode",
    "Description",
    "Quantity",
    "InvoiceDate",
    "UnitPrice",
    "CustomerID",
    "Country",
]

ROWS = [
    ("536365", "85123A", "HEART HOLDER", 6, "2010-12-01", 2.55, 17850.0, "UK"),
    ("536365", "71053", "METAL LANTERN", 6, "2010-12-01", 3.39, 17850.0, "UK"),
    # duplicate of the first row
    ("536365", "85123A", "HEART HOLDER", 6, "2010-12-01", 2.55, 17850.0, "UK"),
    # guest purchase, no CustomerID
    ("536366", "22633", "HAND WARMER", 6, "2010-12-02", 1.85, None, "UK"),
    # service stock code
    ("536367", "POST", "POSTAGE", 1, "2010-12-03", 18.00, 12583.0, "France"),
    # invoice from OUTLIERS
    ("581483", "23843", "PAPER CRAFT", 80995, "2011-12-09", 2.08, 16446.0, "UK"),
    # cancellation, has to stay
    ("C536379", "22960", "JAM MAKING SET", -1, "2010-12-04", 4.25, 14527.0, "UK"),
    # zero price, has to stay
    ("536370", "22913", "RED COAT RACK", 1, "2010-12-05", 0.00, 12583.0, "France"),
    ("536371", "21756", "BATH BUILDING", 12, "2010-12-06", 1.65, 13748.0, "UK"),
    ("536372", "22632", "HAND WARMER RED", 6, "2011-11-30", 1.85, 17850.0, "UK"),
]


@pytest.fixture
def raw_df():
    df = pd.DataFrame(ROWS, columns=COLUMNS)
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
    return df
