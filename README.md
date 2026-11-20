# Northstar — Sales Intelligence Dashboard

A polished, interactive Streamlit dashboard for exploring sales, profitability, product mix and geographic performance.

## Included
- `app.py` — complete Streamlit application
- `sample_superstore.csv` — reproducible synthetic transaction dataset (1,800 rows)
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

Streamlit will print a local URL, usually http://localhost:8501.

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

## 4. Metric definitions

- **Total Sales:** Sum of transaction sales.
- **Total Profit:** Sum of transaction profit.
- **Orders:** Distinct count of Order ID.
- **Average Order Value:** Total Sales / Distinct Orders.
- **Profit Margin:** Total Profit / Total Sales × 100.

The dataset is transaction-line level. If an order contains multiple product lines, the order count remains distinct while sales and profit sum across all lines.

## 5. Publish with Streamlit Community Cloud

1. Create a GitHub repository.
2. Upload `app.py`, `requirements.txt`, and `sample_superstore.csv`.
3. Visit https://share.streamlit.io/ and sign in with GitHub.
4. Choose **Create app**, select your repository and `app.py`.
5. Deploy. The app will be assigned a shareable URL.

Keep the CSV in the repository beside `app.py` for the bundled demo data to load. For a private or large dataset, use Streamlit secrets or an approved data source rather than committing sensitive data.

## 6. Suggested academic submission

Submit:
- The source ZIP or GitHub repository
- Screenshots of the dashboard with all visuals visible
- A short PDF/document containing the objective, dataset description, KPI definitions, filters, and 4–5 insights observed from the running dashboard

When writing insights, use the actual figures displayed by the app. Do not present the synthetic demo results as findings from a real company.

## 7. Data dictionary

| Field | Type | Description |
|---|---|---|
| Order ID | Text | Unique order identifier |
| Order Date | Date | Date of order |
| Ship Mode | Text | Delivery service level |
| Segment | Text | Customer segment |
| Country | Text | Country |
| State | Text | State |
| Region | Text | Broad sales region |
| Category | Text | Product category |
| Sub-Category | Text | Product subcategory |
| Product Name | Text | Product label |
| Sales | Number | Revenue |
| Quantity | Integer | Units |
| Discount | Number | Discount rate |
| Profit | Number | Profit |
| Latitude / Longitude | Number | Approximate state coordinates for map |
| Channel | Text | Sales channel |
