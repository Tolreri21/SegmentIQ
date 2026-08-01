import numpy as np
import pandas as pd

CATEGORY_LABELS = ["Bronze", "Silver", "Gold"]
CATEGORY_BINS = [0, 5, 9, 12]


def add_scores(rfm):
    scored = rfm.copy()
    scored["R"] = pd.qcut(scored["Recency"], q=4, labels=range(4, 0, -1)).astype(int)
    scored["F"] = pd.cut(
        scored["Frequency"], bins=[1, 2, 4, 9, np.inf], labels=range(1, 5), right=False
    ).astype(int)
    scored["M"] = pd.qcut(scored["Monetary"], q=4, labels=range(1, 5)).astype(int)
    scored["RFM_score"] = scored["R"] + scored["F"] + scored["M"]
    scored["Category"] = pd.cut(
        scored["RFM_score"], bins=CATEGORY_BINS, labels=CATEGORY_LABELS
    )
    return scored
