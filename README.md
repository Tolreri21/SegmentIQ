# SegmentIQ

RFM customer segmentation on online retail transaction data.

The project derives three per-customer metrics — **Recency** (days since last
purchase), **Frequency** (number of purchases) and **Monetary** (total spend) —
and groups customers into actionable segments, first by manual RFM scoring and
then by KMeans clustering.

## Stack

Python 3.12 · uv · pandas · scikit-learn · matplotlib / seaborn · ruff · pytest

## Setup

```bash
uv sync                     # create .venv, install runtime + dev dependencies
uv run pre-commit install   # enable git hooks
```

## Dataset

[Online Retail](https://archive.ics.uci.edu/dataset/352/online+retail) (UCI
Machine Learning Repository) — 541,909 transactions from a UK-based online
retailer, 2010-12-01 to 2011-12-09.

Download `Online Retail.xlsx` and place it in `data/raw/`. Datasets are **not
tracked in git** — `data/` and `models/` are gitignored, only their structure is
kept via `.gitkeep`.

Reading `.xlsx` requires `openpyxl` (a dev dependency, installed by `uv sync`).

## Layout

```
data/raw/          source dataset, untracked
data/cache/        parquet cache of the raw file, untracked
data/processed/    cleaned data and RFM tables, untracked
notebooks/         exploration and analysis
src/segmentiq/     reusable package code
tests/             pytest suite
models/            serialized models, untracked
```

Every notebook keeps only the narrative: paths, plots and conclusions. Anything
worth running twice lives in `src/segmentiq/`, one module per pipeline stage:

```
data.py      load_raw, get_data         reading the xlsx and caching to parquet
clean.py     clean_df                   cleaning
rfm.py       create_rfm_table           per-customer features
cluster.py   create_pipe                preprocessing + KMeans in one pipeline
```

## Analysis

The work is split by pull request, each one adds a stage of the pipeline.

### EDA (PR #2)

`notebooks/eda.ipynb`. First look at the raw file: 541,909 rows and 8 columns.
Findings that shaped everything downstream:

* 135,080 rows have no `CustomerID`, so they cannot be attributed to anyone
* 9,288 rows are cancellations: their invoice number starts with `C` and the
  `Quantity` is negative
* some `StockCode` values are not products at all (`POST`, `M`, `DOT`, `D`,
  `CRUK`, `C2`, `BANK CHARGES`)
* four invoices are extreme outliers, including one order of 80,995 units and
  its cancellation

### Preprocessing (PR #3)

`src/segmentiq/clean.py`, `notebooks/preprocessing.ipynb`.

`clean_df` drops rows without `CustomerID` and casts it to `int`, removes the
service stock codes, drops full duplicates, removes the four outlier invoices
and adds a `Revenue` column equal to `UnitPrice * Quantity`. Cancellations are
deliberately **kept**: their `Revenue` is negative, so they subtract themselves
later at aggregation instead of being guessed at row level.

Result: 541,909 rows in, 399,689 rows and 9 columns out.

### RFM table (PR #4)

`src/segmentiq/rfm.py`, `notebooks/rfm.ipynb`.

`create_rfm_table` takes the snapshot date as the last `InvoiceDate` plus one
day, so the most recent customer gets `Recency = 1` instead of 0. Recency and
Frequency are computed on non-cancellation invoices only, because a refund is
not a visit and not a purchase. Monetary sums `Revenue` over all rows, so
cancellations net out. Customers whose net spend is not positive are dropped,
with a `> 0.1` threshold rather than `> 0`: five of them survived a plain `> 0`
filter with values around 1e-15, pure floating point residue from netting.

Result: 4,320 customers with `Recency`, `Frequency` and `Monetary`.

The notebook scores each metric from 1 to 4. Recency and Monetary use `qcut`,
Frequency uses manual bins, because 34.6% of the customers bought exactly once
and quantiles cannot split a tie that large. The sum of the three scores gives
Bronze, Silver and Gold:

| segment | customers | revenue |
|---------|-----------|---------|
| Gold    | 23.7%     | 71.8%   |
| Silver  | 42.9%     | 23.4%   |
| Bronze  | 33.4%     | 4.8%    |

### Tests and CI (PR #5)

`tests/`, `.github/workflows/cicd.yml`.

A 10 row fixture in `conftest.py` reproduces every case the cleaning has to
handle: a duplicate row, a missing `CustomerID`, a service stock code, an
outlier invoice, a cancellation, a zero price and a float `CustomerID`. Four
tests cover `clean_df` and `create_rfm_table`, including the rule that a
cancellation changes Monetary but leaves Recency and Frequency alone.

CI runs on every pull request in two jobs, `ruff check` plus `ruff format
--check`, and `pytest`.

### Clustering (PR #6)

`src/segmentiq/cluster.py`, `notebooks/clustering.ipynb`.

`create_pipe(n_clusters)` returns a single `Pipeline`: `log1p`, then
`StandardScaler`, then `KMeans` with a fixed `random_state`. The order matters
and chaining the steps is what guarantees it. All three RFM distributions are
heavily right skewed, and KMeans minimises squared distances, so without the
logarithm a handful of customers with six figure spend pull the centroids onto
themselves. Without scaling, Monetary in pounds outweighs Frequency in orders
purely because of units.

`k = 4` was chosen from the elbow curve and confirmed with silhouette. The
score is highest at `k = 2` and falls monotonically, which is expected: RFM data
is a continuum, not a set of separated blobs. From 3 to 4 it drops by 0.007, so
the fourth cluster costs almost nothing in cohesion and buys a much more useful
picture.

Medians per cluster, because the tails survive even inside the clusters:

| cluster | recency | frequency | monetary | customers | revenue |
|---------|---------|-----------|----------|-----------|---------|
| Champions          | 8 days   | 10 | £3,542 | 16.2% | 64.2% |
| Average customers  | 51 days  | 4  | £1,320 | 27.4% | 24.1% |
| New or small       | 19 days  | 2  | £409   | 20.0% | 5.0%  |
| Churned            | 184 days | 1  | £294   | 36.4% | 6.6%  |

16% of the customers bring 64% of the revenue.

## Development

```bash
uv run ruff check .          # lint
uv run ruff format .         # format
uv run pytest                # tests
uv run pre-commit run --all-files
```

Notebook outputs are stripped by `nbstripout` on commit, so the repository keeps
code and prose only.

## License

MIT — see [LICENSE](LICENSE).
