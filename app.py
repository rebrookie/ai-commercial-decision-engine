import streamlit as st
import pandas as pd
import plotly.graph_objects as go


from src.data_loader import load_data
from src.kpi_calculator import calculate_kpis
from src.insight_generator import generate_insight
from src.recommendation_engine import generate_recommendation
from src.insight_generator import generate_insight, generate_chat_response

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
# 轻量版 RAG（Data-aware Chat）
# ------------------------
st.header("💬 Ask AI about your data")

user_question = st.text_input(
    "Ask a question about your business data:",
    value="Potential reasons why Prod C with higher price for customer D than customer A."
)

if st.button("Analyze pricing difference (Prod C)"):
    answer = generate_chat_response(
        "Why is Product C priced higher for Customer D compared to Customer A?",
        df,
        kpis
    )
    st.write(answer)




# ------------------------
# Layout - Business Overview
# ------------------------
st.header("📊 Business Overview")

col1, col2, col3 = st.columns(3)

col1.metric("Tot Revenue", f"{kpis.get('total_revenue', 'N/A')}")
col2.metric("Tot Volume", f"{kpis.get('total_volume', 'N/A')}")
col3.metric("Avg Price", f"{kpis.get('avg_price', 'N/A')}")


# ------------------------
# Trend Analysis (Monthly Combo Chart)
# ------------------------
st.header("📈 Trend Analysis")

try:
    # ------------------------
    # Data preparation
    # ------------------------
    df["date"] = pd.to_datetime(df["date"])

    df["month_num"] = df["date"].dt.month
    df["month"] = df["date"].dt.strftime("%b")

    monthly = df.groupby(["month_num", "month"]).agg(
        revenue=("revenue", "sum"),
        volume=("volume", "sum"),
        price=("price", "mean")
    ).reset_index()

    monthly = monthly.sort_values("month_num")

    # ------------------------
    # Figure
    # ------------------------
    fig = go.Figure()

    # 💰 Revenue (PRIMARY - bar)
    fig.add_trace(
        go.Bar(
            x=monthly["month"],
            y=monthly["revenue"],
            name="Revenue"
        )
    )

    # 📦 Volume (SECONDARY - line)
    fig.add_trace(
        go.Scatter(
            x=monthly["month"],
            y=monthly["volume"],
            mode="lines+markers",
            name="Volume",
            yaxis="y2"
        )
    )

    # 💲 Price (SECONDARY - line)
    fig.add_trace(
        go.Scatter(
            x=monthly["month"],
            y=monthly["price"],
            mode="lines+markers",
            name="Avg Price",
            yaxis="y2"
        )
    )

    # ------------------------
    # Layout (BI-style)
    # ------------------------
    fig.update_layout(
        title="Monthly Revenue with Key Drivers (Volume & Price)",
        xaxis_title="Month",
        yaxis_title="Revenue",
        yaxis2=dict(
            title="Volume / Price",
            overlaying="y",
            side="right"
        ),
        barmode="group",
        legend=dict(x=0, y=1.15, orientation="h"),
        template="plotly_white"
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




