# Sales Intelligence Dashboard — Project Documentation

## Objective
To develop an interactive dashboard that summarizes sales performance and helps users explore revenue, profitability, product mix, regional performance and changes over time.

## Tools and Technologies
- Python
- Streamlit
- Pandas and NumPy
- Plotly

## Dataset
The project includes a synthetic Superstore-style transaction dataset with 1,800 records. It contains order dates, order IDs, region, state, product category/sub-category, sales, profit, quantity, discount, customer segment and sales channel. Synthetic data is supplied so the project runs immediately; a real CSV can be uploaded through the sidebar.

## Dashboard Features
- Five KPI cards: Total Sales, Total Profit, Orders, Average Order Value and Profit Margin.
- Monthly sales and profit trend.
- Regional sales comparison.
- Category/sub-category treemap.
- Geographic sales and profit map.
- Region, category, customer segment and date filters.
- Filtered transaction table and CSV export.
- Automatically generated insights.

## KPI Calculations
- Total Sales = Sum of Sales
- Total Profit = Sum of Profit
- Orders = Distinct count of Order ID
- Average Order Value = Total Sales / Distinct Orders
- Profit Margin = (Total Profit / Total Sales) × 100

## Key Insights
Fill these in after running the dashboard and selecting the required filters:
1. Highest-sales region: ______________________________
2. Highest-sales category: ____________________________
3. Highest-sales month: _______________________________
4. Overall profit margin: _____________________________
5. Notable loss-making transactions or product areas: __

## Conclusion
The dashboard combines KPI summaries, trend analysis, categorical comparisons, geographic exploration and interactive filters in one interface. It allows users to move from a high-level overview to transaction-level records and export the filtered data for further analysis.
