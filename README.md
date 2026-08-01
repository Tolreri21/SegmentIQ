# SegmentIQ

RFM customer segmentation on online retail data.

Every customer gets three numbers: **Recency** (days since the last order),
**Frequency** (number of orders) and **Monetary** (total spend). Customers are
then split into segments twice, first by manual RFM scoring, then by KMeans, and
the two results are compared.

## Results

Four clusters, medians per cluster:

| cluster | recency | frequency | monetary | customers | revenue |
|---------|---------|-----------|----------|-----------|---------|
| Champions         | 8 days   | 10 | £3,542 | 16.2% | 64.2% |
| Average customers | 51 days  | 4  | £1,320 | 27.4% | 24.1% |
| New or small      | 19 days  | 2  | £409   | 20.0% | 5.0%  |
| Churned           | 184 days | 1  | £294   | 36.4% | 6.6%  |

16% of the customers bring 64% of the revenue. What to do with each of them:

* **Champions**: keep them, do not sell harder. Loyalty program, early access, no
  discounts. A Champion silent for a month is a warning sign.
* **Average customers**: the best group to work with. They already buy often and
  they are the closest to the Champions. Remind them every 50 days, cross-sell
  what the Champions buy.
* **New or small**: still active, so they are cheap to reach. Push them to the
  second and the third order.
* **Churned**: the biggest group, but only 6.6% of the money. One cheap email
  campaign, and most of them will not come back.

The manual scoring gives a similar picture, Bronze 33.4% of the customers with
4.8% of the revenue against Gold 23.7% with 71.8%. The two methods agree on the
best and the worst customers and disagree in the middle: what the scoring calls
Silver splits into two clusters that look nothing alike, 4 orders and £1,320
against 2 orders and £409.

## Stack

Python 3.12 · uv · pandas · scikit-learn · matplotlib / seaborn · ruff · pytest

## Setup

```bash
uv sync                     # create .venv, install runtime + dev dependencies
uv run pre-commit install   # enable git hooks
```

## Dataset

[Online Retail](https://archive.ics.uci.edu/dataset/352/online+retail) (UCI
Machine Learning Repository), 541,909 transactions from a UK online retailer,
2010-12-01 to 2011-12-09.

Download `Online Retail.xlsx` into `data/raw/`. Data and models are gitignored,
only the folder structure is kept.

## Layout

```
data/          raw file, parquet cache and processed tables, untracked
notebooks/     the story: EDA, preprocessing, RFM, clustering
src/segmentiq/ the code the notebooks call
tests/         pytest suite
models/        saved pipeline, untracked
```

Notebooks keep only paths, plots and conclusions. Anything worth running twice
lives in the package, one module per step:

```
data.py      load_raw, get_data    read the xlsx, cache it as parquet
clean.py     clean_df              cleaning
rfm.py       create_rfm_table      per customer features
score.py     add_scores            RFM scores and Bronze / Silver / Gold
cluster.py   create_pipe           preprocessing and KMeans in one pipeline
```

## How it works

**Cleaning.** 135,080 rows have no `CustomerID` and are dropped. Service codes
like `POST` and `BANK CHARGES` are not products, duplicates and four outlier
invoices go as well. Cancellations are kept on purpose: their `Revenue` is
negative, so they subtract themselves later instead of being guessed row by row.
541,909 rows in, 399,689 out.

**RFM table.** The snapshot date is the last order plus one day, so the newest
customer gets `Recency = 1` and not 0. Recency and Frequency ignore
cancellations, because a refund is not a visit. Monetary sums everything, so
cancellations net out. Customers with no positive spend are dropped, the
threshold is `> 0.1` and not `> 0` because five of them had values around 1e-15,
pure floating point residue. Result: 4,320 customers.

**Scoring.** Each metric gets a score from 1 to 4. Recency and Monetary use
`qcut`, Frequency uses manual bins, because 34.6% of the customers bought exactly
once and quantiles cannot split a tie that big. The sum gives Bronze, Silver and
Gold.

**Clustering.** `create_pipe(n_clusters)` returns one `Pipeline`: `log1p`, then
`StandardScaler`, then `KMeans` with a fixed `random_state`. Without the
logarithm a few huge spenders pull the centroids onto themselves. Without scaling
Monetary in pounds outweighs Frequency in orders just because of the units.
Keeping the steps in one pipeline is what guarantees the order.

`k = 4` comes from the elbow curve and is checked with silhouette, measured in
the scaled space. The score peaks at `k = 2` and falls all the way down, which is
what a continuum of customers looks like, but from 3 to 4 it drops only by 0.007.
The fitted pipeline is saved with `joblib` to `models/kmeans.joblib`.

## Tests and CI

A 10 row fixture covers every case the cleaning has to handle: a duplicate, a
missing `CustomerID`, a service code, an outlier invoice, a cancellation, a zero
price and a float `CustomerID`. A second fixture with six obvious customers
covers the pipeline. The tests check that cleaning drops the right rows, that a
cancellation changes Monetary but not Recency and Frequency, and that loyal
customers never land in the same cluster as churned ones.

CI runs on every pull request: `ruff check`, `ruff format --check` and `pytest`.

## Limitations

* There is no date of the first order, so one segment stays ambiguous: new
  customers and small ones look the same in the table.
* The segments are not validated on a later period, so it is unknown whether they
  predict anything.
* The saved pipeline is not loaded back anywhere yet, the analysis runs from the
  notebooks.

## Development

```bash
uv run ruff check .          # lint
uv run ruff format .         # format
uv run pytest                # tests
uv run pre-commit run --all-files
```

`nbstripout` clears notebook outputs on commit, so the repository keeps code and
text only.

## License

MIT, see [LICENSE](LICENSE).
