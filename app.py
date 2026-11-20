import io
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="Northstar | Sales Intelligence", page_icon="✦", layout="wide")

# ---------- Theme ----------
NAVY = "#14243A"
BLUE = "#3978F6"
TEAL = "#1AAE9F"
AMBER = "#F2A93B"
MUTED = "#718096"
PLOT_TEMPLATE = "plotly_white"

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@500;600;700;800&display=swap');
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
.stApp { background: #F5F7FB; color: #14243A; }
.block-container { padding-top: 1.5rem; padding-bottom: 2.5rem; max-width: 1500px; }
[data-testid="stSidebar"] { background: #14243A; }
[data-testid="stSidebar"] * { color: #F5F7FB !important; }
[data-testid="stSidebar"] [data-baseweb="select"] * { color: #14243A !important; }
[data-testid="stMetric"] { background: white; border: 1px solid #E8EDF5; padding: 17px 18px; border-radius: 14px; box-shadow: 0 3px 12px rgba(20,36,58,.035); }
[data-testid="stMetricLabel"] { color: #718096 !important; font-weight: 600; }
[data-testid="stMetricValue"] { color: #14243A !important; font-family: 'Manrope', sans-serif; }
h1,h2,h3 { font-family: 'Manrope', sans-serif !important; color: #14243A; }
.hero { background: linear-gradient(115deg,#14243A 0%,#203F67 65%,#3978F6 100%); padding: 26px 30px; border-radius: 18px; color: white; margin-bottom: 18px; }
.hero h1 { color: white !important; font-size: 2rem; margin: 0; }
.hero p { color: #D8E5F6; margin: 6px 0 0 0; }
.section-kicker { color: #3978F6; text-transform: uppercase; letter-spacing: .12em; font-size: .72rem; font-weight: 700; margin-bottom: 2px; }
.insight { background: white; border: 1px solid #E8EDF5; border-left: 4px solid #3978F6; border-radius: 10px; padding: 13px 16px; margin: 7px 0; }
.small-note { color: #718096; font-size: .84rem; }
hr { border-color: #E8EDF5; }
</style>
""", unsafe_allow_html=True)

# ---------- Data ----------

@st.cache_data
def load_csv(file_or_path):
    try:
        data = pd.read_csv(file_or_path, encoding="utf-8-sig")
    except UnicodeDecodeError:
        try:
            data = pd.read_csv(file_or_path, encoding="cp1252")
        except UnicodeDecodeError:
            data = pd.read_csv(file_or_path, encoding="latin1")
    return data

def normalize_data(data):
    data = data.copy()
    required = ["Order Date", "Sales", "Profit", "Order ID", "Region", "Category"]
    missing = [c for c in required if c not in data.columns]
    if missing:
        raise ValueError("Missing required columns: " + ", ".join(missing))
    data["Order Date"] = pd.to_datetime(data["Order Date"], errors="coerce")
    for col in ["Sales", "Profit", "Quantity", "Discount"]:
        if col in data.columns:
            data[col] = pd.to_numeric(data[col], errors="coerce")
    data = data.dropna(subset=["Order Date", "Sales", "Profit", "Order ID"])
    if "Quantity" not in data.columns:
        data["Quantity"] = 1
    if "State" not in data.columns:
        data["State"] = "Not specified"
    if "Sub-Category" not in data.columns:
        data["Sub-Category"] = data["Category"]
    if "Segment" not in data.columns:
        data["Segment"] = "Not specified"
    if "Channel" not in data.columns:
        data["Channel"] = "Not specified"
    if "Discount" not in data.columns:
        data["Discount"] = 0
    return data

st.sidebar.markdown("## ✦ NORTHSTAR")
st.sidebar.caption("SALES INTELLIGENCE")
st.sidebar.markdown("---")
uploaded = st.sidebar.file_uploader("Upload your own CSV", type=["csv"], help="Expected fields: Order Date, Sales, Profit, Order ID, Region and Category.")
source_label = "Uploaded dataset" if uploaded else "Included demonstration dataset"

try:
    raw = load_csv(uploaded) if uploaded else load_csv(Path(__file__).parent / "sample_superstore.csv")
    data = normalize_data(raw)
except Exception as exc:
    st.error(f"Could not load the dataset: {exc}")
    st.info("Upload a CSV with the required columns, or restore sample_superstore.csv beside app.py.")
    st.stop()

st.sidebar.markdown("---")
st.sidebar.markdown("### FILTERS")
regions = sorted(data["Region"].dropna().astype(str).unique())
categories = sorted(data["Category"].dropna().astype(str).unique())
segments = sorted(data["Segment"].dropna().astype(str).unique())
selected_regions = st.sidebar.multiselect("Region", regions, default=regions)
selected_categories = st.sidebar.multiselect("Category", categories, default=categories)
selected_segments = st.sidebar.multiselect("Customer segment", segments, default=segments)
date_min = data["Order Date"].min().date()
date_max = data["Order Date"].max().date()
date_range = st.sidebar.date_input("Order date range", value=(date_min, date_max), min_value=date_min, max_value=date_max)
if not isinstance(date_range, (tuple, list)) or len(date_range) != 2:
    date_range = (date_min, date_max)

filtered = data[
    data["Region"].astype(str).isin(selected_regions)
    & data["Category"].astype(str).isin(selected_categories)
    & data["Segment"].astype(str).isin(selected_segments)
    & data["Order Date"].dt.date.between(date_range[0], date_range[1])
].copy()

# ---------- Header ----------
st.markdown("""
<div class="hero">
  <div style="font-size:.72rem;letter-spacing:.16em;font-weight:700;color:#AFC9F4;">BUSINESS PERFORMANCE • INTERACTIVE REPORT</div>
  <h1>Sales, at a glance.</h1>
  <p>One clear view of revenue, profitability, customer demand and geographic performance.</p>
</div>
""", unsafe_allow_html=True)
st.caption(f"DATA SOURCE  ·  {source_label}  ·  {len(filtered):,} transaction rows in current view")

if filtered.empty:
    st.warning("No records match these filters. Widen the date range or select additional regions/categories.")
    st.stop()

# ---------- KPIs ----------
sales = filtered["Sales"].sum()
profit = filtered["Profit"].sum()
orders = filtered["Order ID"].nunique()
aov = sales / orders if orders else 0
margin = profit / sales * 100 if sales else 0
units = filtered["Quantity"].sum()

st.markdown('<div class="section-kicker">01 / Executive overview</div>', unsafe_allow_html=True)
k1,k2,k3,k4,k5 = st.columns(5)
k1.metric("Total sales", f"${sales:,.0f}")
k2.metric("Total profit", f"${profit:,.0f}")
k3.metric("Orders", f"{orders:,}")
k4.metric("Average order value", f"${aov:,.2f}")
k5.metric("Profit margin", f"{margin:.1f}%")
st.markdown("<br>", unsafe_allow_html=True)

# ---------- Trend ----------
st.markdown('<div class="section-kicker">02 / Performance over time</div>', unsafe_allow_html=True)
monthly = (filtered.set_index("Order Date").resample("MS")
           .agg(Sales=("Sales","sum"), Profit=("Profit","sum"), Orders=("Order ID","nunique"))
           .reset_index())
fig_trend = go.Figure()
fig_trend.add_trace(go.Scatter(x=monthly["Order Date"], y=monthly["Sales"], name="Sales",
                               mode="lines+markers", line=dict(color=BLUE,width=3),
                               fill="tozeroy", fillcolor="rgba(57,120,246,.08)"))
fig_trend.add_trace(go.Scatter(x=monthly["Order Date"], y=monthly["Profit"], name="Profit",
                               mode="lines", line=dict(color=TEAL,width=2,dash="dot"), yaxis="y2"))
fig_trend.update_layout(template=PLOT_TEMPLATE, height=340, margin=dict(l=10,r=15,t=25,b=10),
                        legend=dict(orientation="h",y=1.12), hovermode="x unified",
                        yaxis=dict(title="Sales ($)", gridcolor="#EDF1F7"),
                        yaxis2=dict(title="Profit ($)", overlaying="y", side="right", showgrid=False),
                        xaxis=dict(title="", gridcolor="#EDF1F7"))
st.plotly_chart(fig_trend, use_container_width=True)

# ---------- Breakdown charts ----------
st.markdown('<div class="section-kicker">03 / What drives performance</div>', unsafe_allow_html=True)
left,right = st.columns([1.05,1])
region_sales = filtered.groupby("Region",as_index=False).agg(Sales=("Sales","sum"),Profit=("Profit","sum"))
region_sales = region_sales.sort_values("Sales")
with left:
    st.markdown("#### Sales by region")
    fig_region = px.bar(region_sales, x="Sales", y="Region", orientation="h", color="Sales",
                        color_continuous_scale=["#BFD5FF",BLUE], text_auto=".2s")
    fig_region.update_layout(template=PLOT_TEMPLATE,height=310,margin=dict(l=5,r=5,t=5,b=5),
                             coloraxis_showscale=False,xaxis_title="Sales ($)",yaxis_title="")
    st.plotly_chart(fig_region,use_container_width=True)

with right:
    st.markdown("#### Category mix")
    cat = filtered.groupby("Category",as_index=False).agg(Sales=("Sales","sum"),Profit=("Profit","sum"))
    fig_tree = px.treemap(filtered,path=["Category","Sub-Category"],values="Sales",color="Profit",
                          color_continuous_scale=["#E98A8A","#F7D98A","#49B7A5"],
                          hover_data={"Sales":":$,.0f","Profit":":$,.0f"})
    fig_tree.update_layout(template=PLOT_TEMPLATE,height=310,margin=dict(l=5,r=5,t=5,b=5),
                           coloraxis_colorbar_title="Profit ($)")
    st.plotly_chart(fig_tree,use_container_width=True)

# ---------- Geography ----------
st.markdown('<div class="section-kicker">04 / Geographic footprint</div>', unsafe_allow_html=True)
if {"Latitude","Longitude"}.issubset(filtered.columns):
    geo = filtered.dropna(subset=["Latitude","Longitude"]).copy()
    if not geo.empty:
        state_geo = geo.groupby(["State","Latitude","Longitude"],as_index=False).agg(
            Sales=("Sales","sum"),Profit=("Profit","sum"),Orders=("Order ID","nunique"))
        fig_map = px.scatter_geo(state_geo,lat="Latitude",lon="Longitude",size="Sales",
                                 color="Profit",hover_name="State",
                                 hover_data={"Sales":":$,.0f","Profit":":$,.0f","Orders":True,
                                             "Latitude":False,"Longitude":False},
                                 scope="usa",projection="albers usa",
                                 color_continuous_scale="RdYlGn",size_max=32)
        fig_map.update_layout(template=PLOT_TEMPLATE,height=390,margin=dict(l=0,r=0,t=5,b=0))
        st.plotly_chart(fig_map,use_container_width=True)
    else:
        st.info("No valid coordinates in the current selection.")
else:
    st.info("A map needs Latitude and Longitude columns. The included sample dataset contains both.")

# ---------- Insights ----------
st.markdown('<div class="section-kicker">05 / Quick business readout</div>', unsafe_allow_html=True)
top_region = region_sales.sort_values("Sales",ascending=False).iloc[0]
top_cat = cat.sort_values("Sales",ascending=False).iloc[0]
best_month = monthly.loc[monthly["Sales"].idxmax()] if not monthly.empty else None
loss_rows = filtered[filtered["Profit"] < 0]
insights = [
    f"**{top_region['Region']}** is the leading region, contributing **${top_region['Sales']:,.0f}** in sales.",
    f"**{top_cat['Category']}** is the largest category by sales, contributing **${top_cat['Sales']:,.0f}**.",
    f"Overall profit margin for the selected view is **{margin:.1f}%**.",
]
if best_month is not None:
    insights.append(f"The strongest month in the selected period is **{best_month['Order Date']:%B %Y}**, with **${best_month['Sales']:,.0f}** in sales.")
if not loss_rows.empty:
    insights.append(f"**{len(loss_rows):,}** transaction rows have negative profit; review discounts, product mix and fulfilment costs.")
for item in insights:
    st.markdown(f'<div class="insight">{item}</div>',unsafe_allow_html=True)

# ---------- Detail table and export ----------
with st.expander("Explore transaction-level data",expanded=False):
    show_cols = [c for c in ["Order ID","Order Date","Region","State","Segment","Category","Sub-Category","Product Name","Sales","Profit","Quantity","Discount","Channel"] if c in filtered.columns]
    st.dataframe(filtered[show_cols].sort_values("Order Date",ascending=False),use_container_width=True,height=330)
    csv_bytes = filtered.to_csv(index=False).encode("utf-8")
    st.download_button("Download filtered records (CSV)",csv_bytes,"filtered_sales_data.csv","text/csv")

st.markdown("---")
st.markdown('<p class="small-note">NORTHSTAR SALES INTELLIGENCE  ·  Built with Streamlit, Pandas and Plotly  ·  Demonstration data is synthetic and intended for academic/dashboard demonstration.</p>',unsafe_allow_html=True)
