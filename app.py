import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from src.data_loader import load_data
from src.kpi_calculator import calculate_kpis
from src.insight_generator import generate_insight
from src.recommendation_engine import generate_recommendation

# ------------------------
# Page Config
# ------------------------
st.set_page_config(page_title="AI Commercial Decision Engine", layout="wide")

st.title("🚀 AI Commercial Decision Engine")
st.markdown(
        "Transforming commercial analytics from **reporting → decision intelligence**"
)


# ------------------------
# Load Data
# ------------------------
df = load_data("data/sales_data.csv")


# ------------------------
# Optional: Raw Data (collapsed)
# ------------------------
with st.expander("🔍 View Raw Data"):
    st.dataframe(df)

# ------------------------
# KPI Calculation
# ------------------------
kpis = calculate_kpis(df)



# ------------------------
# Layout - Business Overview
# ------------------------
st.header("📊 Business Overview")

col1, col2, col3 = st.columns(3)

col1.metric("Revenue", f"{kpis.get('revenue', 'N/A')}")
col2.metric("Volume", f"{kpis.get('volume', 'N/A')}")
col3.metric("Price", f"{kpis.get('price', 'N/A')}")




# ------------------------
# Trend Analysis (Monthly Combo Chart)
# ------------------------
st.header("📈 Trend Analysis")

try:
    df["date"] = pd.to_datetime(df["date"])

    # 👉 按月聚合（关键）
    df["month"] = df["date"].dt.to_period("M").astype(str)

    monthly = df.groupby("month").agg(
        revenue=("revenue", "sum"),
        volume=("volume", "sum"),
        price=("price", "mean")
    ).reset_index()

    fig = go.Figure()

    # 📦 Volume (stacked bar)
    fig.add_bar(
        x=monthly["month"],
        y=monthly["volume"],
        name="Volume"
    )

    # 💰 Revenue (bar)
    fig.add_bar(
        x=monthly["month"],
        y=monthly["revenue"],
        name="Revenue"
    )

    # 💲 Price (line)
    fig.add_trace(
        go.Scatter(
            x=monthly["month"],
            y=monthly["price"],
            mode="lines+markers",
            name="Avg Price",
            yaxis="y2"
        )
    )

    # 🎯 Layout (dual axis + titles)
    fig.update_layout(
        title="Monthly Revenue, Volume & Price Trend",
        xaxis_title="Month",
        yaxis_title="Revenue / Volume",
        yaxis2=dict(
            title="Avg Price",
            overlaying="y",
            side="right"
        ),
        barmode="stack",
        legend=dict(x=0, y=1.1, orientation="h")
    )

    st.plotly_chart(fig, use_container_width=True)

except Exception as e:
    st.warning(f"Trend analysis failed: {e}")


# ------------------------
# Run AI Analysis Button
# ------------------------
st.header("🧠 AI Analysis")

if st.button("Run AI Analysis"):

    with st.spinner("Generating insights..."):

        try:
            insight = generate_insight(df)
            recommendation = generate_recommendation(insight)

            # Insight
            st.subheader("🧠 Insight")
            st.write(insight)

            # Recommendation
            st.subheader("💡 Recommendation")
            st.write(recommendation)

        except Exception as e:
            st.error(f"Error generating AI output: {e}")

