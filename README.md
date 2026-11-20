# Northstar — Sales Intelligence Dashboard

A polished, interactive Streamlit dashboard for exploring sales, profitability, product mix and geographic performance.

## Included
- `app.py` — complete Streamlit application
- `sample_superstore.csv` — transaction dataset
- `requirements.txt` — Python dependencies
- `README.md` — setup, usage, data dictionary and deployment notes

> **Dataset note:** The included CSV is synthetic demonstration data, not the official Kaggle Sample Superstore dataset. It is designed to make the app runnable immediately. You can upload a real Superstore CSV from the sidebar.

## 1. Run locally

Python 3.9+ is recommended.

```bash
# Create and activate a virtual environment (optional but recommended)
python -m venv .venv

# Windows PowerShell
.venv\Scripts\Activate.ps1

# macOS / Linux
source .venv/bin/activate

# Install packages
pip install -r requirements.txt

# Launch
streamlit run app.py
```

## 2. Use your own dataset

Use the sidebar's **Upload your own CSV** control. Required columns:

| Column | Meaning |
|---|---|
| `Order Date` | Transaction date |
| `Order ID` | Unique order identifier |
| `Sales` | Revenue amount |
| `Profit` | Profit amount |
| `Region` | Geographic sales region |
| `Category` | Product category |

Optional columns used by the visuals: `State`, `Sub-Category`, `Segment`, `Quantity`, `Discount`, `Channel`, `Latitude`, `Longitude`.

The app handles missing optional columns by filling safe defaults. A map is shown when latitude and longitude columns are available.

## 3. Dashboard contents

1. **Executive KPIs:** Total Sales, Total Profit, Orders, Average Order Value and Profit Margin.
2. **Time series:** Monthly Sales and Profit.
3. **Regional comparison:** Horizontal bar chart of sales by region.
4. **Product mix:** Treemap grouped by Category and Sub-Category, coloured by Profit.
5. **Geography:** US map sized by sales and coloured by profit.
6. **Interactive filters:** Region, Category, Customer Segment and Order Date range.
7. **Business readout:** Automatically generated insights for the current filtered selection.
8. **Data exploration:** Expandable transaction table and CSV download.
