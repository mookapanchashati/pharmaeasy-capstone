import pandas as pd
import streamlit as st
import plotly.express as px

# ---------------------------------------------------------
# PAGE SETUP
# ---------------------------------------------------------

st.set_page_config(
    page_title="PharmEasy Regional Pulse",
    layout="wide"
)

st.title("PharmEasy Regional Pulse")
st.caption("Regional Performance Intelligence Dashboard")


# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------

@st.cache_data
def load_data():
    df = pd.read_csv("orders_clean.csv")

    df["order_date"] = pd.to_datetime(df["order_date"])
    df["month"] = df["order_date"].dt.strftime("%Y-%m")

    return df


df = load_data()


# ---------------------------------------------------------
# REGION FILTER
# ---------------------------------------------------------

regions = sorted(df["region"].unique())

selected_region = st.selectbox(
    "Select Region",
    ["All Regions"] + regions
)


if selected_region == "All Regions":
    filtered_df = df.copy()
else:
    filtered_df = df[
        df["region"] == selected_region
    ].copy()


# ---------------------------------------------------------
# EXECUTIVE SUMMARY DATA
# ---------------------------------------------------------

total_sales = filtered_df["sales_inr"].sum()
total_profit = filtered_df["profit_inr"].sum()

# DISTINCT order count - required by the capstone
total_orders = filtered_df["order_id"].nunique()


monthly_summary = (
    filtered_df
    .groupby("month")
    .agg(
        sales=("sales_inr", "sum")
    )
    .reset_index()
)


top_month_row = monthly_summary.loc[
    monthly_summary["sales"].idxmax()
]

top_month = top_month_row["month"]
top_month_sales = top_month_row["sales"]


category_summary = (
    filtered_df
    .groupby("category")
    .agg(
        sales=("sales_inr", "sum")
    )
    .reset_index()
)


top_category_row = category_summary.loc[
    category_summary["sales"].idxmax()
]

top_category = top_category_row["category"]


# ---------------------------------------------------------
# EXECUTIVE SUMMARY
# ---------------------------------------------------------

st.subheader("Executive Summary")

summary_text = f"""
The selected view generated **₹{total_sales:,.2f} in sales**, 
**₹{total_profit:,.2f} in profit**, across **{total_orders:,} distinct orders**.  
The strongest sales month in this view was **{top_month}**, with sales of **₹{top_month_sales:,.2f}**.  
**{top_category}** was the largest category contributor to sales.  
The month-to-month movements should be reviewed alongside the operational alerts before any business action is taken.  
Use the category, trend and regional detail sections below to investigate the underlying performance.
"""

st.markdown(summary_text)


# ---------------------------------------------------------
# OVERVIEW LEVEL
# ---------------------------------------------------------

st.header("1. Overview")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Total Sales (INR)",
    f"₹{total_sales:,.2f}"
)

col2.metric(
    "Total Profit (INR)",
    f"₹{total_profit:,.2f}"
)

col3.metric(
    "Distinct Orders",
    f"{total_orders:,}"
)


# ---------------------------------------------------------
# MONTHLY TREND CHART
# ---------------------------------------------------------

trend_data = (
    filtered_df
    .groupby(["month", "region"])
    ["sales_inr"]
    .sum()
    .reset_index()
)

trend_max = trend_data["sales_inr"].max()

fig_line = px.line(
    trend_data,
    x="month",
    y="sales_inr",
    color="region",
    markers=True,
    title="How have monthly sales changed across regions?"
)

fig_line.update_layout(
    xaxis_title="Month",
    yaxis_title="Sales (INR)"
)

fig_line.update_yaxes(
    range=[0, trend_max * 1.10]
)

st.plotly_chart(
    fig_line,
    use_container_width=True
)


# ---------------------------------------------------------
# REGION COMPARISON BAR CHART
# ---------------------------------------------------------

region_sales = (
    filtered_df
    .groupby("region")
    ["sales_inr"]
    .sum()
    .reset_index()
    .sort_values(
        "sales_inr",
        ascending=False
    )
)

bar_max = region_sales["sales_inr"].max()

fig_bar = px.bar(
    region_sales,
    x="region",
    y="sales_inr",
    title="Which region generated the most sales?"
)

fig_bar.update_layout(
    xaxis_title="Region",
    yaxis_title="Total Sales (INR)"
)

fig_bar.update_yaxes(
    range=[0, bar_max * 1.10]
)

st.plotly_chart(
    fig_bar,
    use_container_width=True
)


# ---------------------------------------------------------
# CATEGORY LEVEL
# ---------------------------------------------------------

st.header("2. Category Breakdown")

category_detail = (
    filtered_df
    .groupby("category")
    .agg(
        total_sales=("sales_inr", "sum"),
        total_profit=("profit_inr", "sum"),
        order_count=("order_id", "nunique")
    )
    .reset_index()
    .sort_values(
        "total_sales",
        ascending=False
    )
)

st.dataframe(
    category_detail,
    use_container_width=True
)


# ---------------------------------------------------------
# CATEGORY DONUT CHART
# ---------------------------------------------------------

fig_pie = px.pie(
    category_detail,
    names="category",
    values="total_sales",
    hole=0.45,
    title="Which medicine categories contribute most to sales?"
)

fig_pie.update_traces(
    textinfo="percent+label"
)

st.plotly_chart(
    fig_pie,
    use_container_width=True
)


# ---------------------------------------------------------
# DETAIL LEVEL
# ---------------------------------------------------------

st.header("3. Region × Month Detail")

detail_table = (
    filtered_df
    .groupby(
        ["region", "month"]
    )
    .agg(
        total_sales=("sales_inr", "sum"),
        total_profit=("profit_inr", "sum"),
        order_count=("order_id", "nunique")
    )
    .reset_index()
    .sort_values(
        ["region", "month"]
    )
)

detail_table["total_sales"] = (
    detail_table["total_sales"].round(2)
)

detail_table["total_profit"] = (
    detail_table["total_profit"].round(2)
)

st.dataframe(
    detail_table,
    use_container_width=True
)