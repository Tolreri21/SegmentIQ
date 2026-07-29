# SegmentIQ

RFM customer segmentation on online retail transaction data.

The project derives three per-customer metrics — **Recency** (days since last
purchase), **Frequency** (number of purchases) and **Monetary** (total spend) —
and groups customers into actionable segments.

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
data/processed/    cleaned data and RFM tables, untracked
notebooks/         exploration and analysis
src/segmentiq/     reusable package code
tests/             pytest suite
models/            serialized models, untracked
```

## Development

```bash
uv run ruff check .          # lint
uv run ruff format .         # format
uv run pytest                # tests
uv run pre-commit run --all-files
```

## License

MIT — see [LICENSE](LICENSE).
