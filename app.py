import streamlit as st
import pandas as pd

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
# Trend Analysis
# ------------------------
st.header("📈 Trend Analysis")

try:
    df["date"] = pd.to_datetime(df["date"])
    df_sorted = df.sort_values("date")
    st.line_chart(df_sorted.set_index("date")["revenue"])
except Exception:
    st.warning("No valid 'date' column found for trend analysis.")

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

# ------------------------
# Optional: Raw Data (collapsed)
# ------------------------
with st.expander("🔍 View Raw Data"):
    st.dataframe(df)