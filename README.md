# Sales Intelligence Platform

[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.x-red)](https://streamlit.io)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue)](https://postgresql.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green)](LICENSE)

Automated sales analytics platform that ingests raw sales data, runs ETL transformations, and surfaces actionable insights through an interactive Streamlit dashboard.

---

## What This Does

- **Ingests** multi-source sales data (CSV, database) via a modular ETL pipeline
- **Transforms** raw records into analytics-ready datasets: revenue aggregations, rep performance, product trends, and regional breakdowns
- **Serves** results through a Streamlit dashboard with filters, drill-downs, and auto-generated insight summaries
- **Stores** processed data in a PostgreSQL/SQLite backend for reproducible querying

---

## Architecture

```
Raw Sales Data (CSV / DB)
        │
        ▼
etl-pipeline.py     ← Ingest, clean, normalize, load
        │
        ▼
database/           ← PostgreSQL / SQLite storage layer
        │
        ▼
analysis/           ← Aggregations, KPI calculations, trend detection
        │
        ▼
app.py              ← Streamlit dashboard (filters, charts, insights)
```

---

## Key Features

- Rep performance ranking and quota attainment tracking
- Product-level revenue and margin analysis
- Regional / territory breakdown with time-series trends
- Automated insight generation (top performers, anomalies, YoY delta)
- Filter by date range, region, product category, and rep

---

## Tech Stack

| Tool | Purpose |
|---|---|
| Python 3.11 | Core language |
| Pandas | ETL and data transformation |
| SQLAlchemy | Database ORM |
| PostgreSQL / SQLite | Data storage |
| Streamlit | Interactive dashboard |
| Plotly | Charts and visualizations |

---

## Quick Start

```bash
git clone https://github.com/Nag4535/sales-intelligence-platform
cd sales-intelligence-platform
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run ETL pipeline
python etl-pipeline.py

# Launch dashboard
streamlit run app.py
```

Dashboard will be available at `http://localhost:8501`

---

## Project Structure

```
sales-intelligence-platform/
├── app.py              # Streamlit dashboard
├── etl-pipeline.py     # ETL: ingest → clean → load
├── analysis/           # KPI calculations and aggregations
├── data/               # Raw and sample data
├── database/           # Schema definitions and migrations
└── requirements.txt
```

---

## Related Projects

- [customer360-intelligence](https://github.com/Nag4535/customer360-intelligence) — Customer segmentation and churn prediction
- [market-intel-data-pipeline](https://github.com/Nag4535/market-intel-data-pipeline) — Real-time streaming data infrastructure
