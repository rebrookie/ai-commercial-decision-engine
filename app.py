import streamlit as st
import os

from src.data_loader import load_data
from src.kpi_calculator import calculate_kpis
from src.insight_generator import generate_insight
from src.recommendation_engine import generate_recommendation
import pandas as pd

st.title("🚀 AI Commercial Decision Engine")
st.markdown("This tool demonstrates how commercial analytics can evolve from static reporting into AI-driven decision intelligence, enabling faster and more actionable business insights.")

# --- Load data ---
df = pd.read_csv("data/sales_data.csv")

# --- Generate insight ---
insight = ""
recommendation = ""

try:
    insight = generate_insight(df)
    recommendation = generate_recommendation(insight)
except Exception as e:
    st.error(f"Error generating AI output: {e}")

# --- UI ---
st.header("📊 Business Overview")

col1, col2, col3 = st.columns(3)
col1.metric("Revenue", "€12.5M", "+5%")
col2.metric("Volume", "1.2M units", "-2%")
col3.metric("Price", "€10.4", "+7%")

st.header("📈 Trend Analysis")
st.line_chart(df.set_index("date")["revenue"])

st.header("🧠 AI Insight")
st.write(insight)

st.header("💡 Recommendation")
st.write(recommendation)

# ✅ 读取数据（必须相对路径）
df = load_data("data/sales_data.csv")

st.subheader("Raw Data")
st.dataframe(df)

if st.button("Run Analysis"):

    kpis = calculate_kpis(df)
    st.subheader("KPIs")
    st.write(kpis)

    # ✅ 从环境变量读取 key（关键）
    api_key = None
    if "OPENAI_API_KEY" in st.secrets:
        api_key = st.secrets["OPENAI_API_KEY"]
    elif "OPENAI_API_KEY" in os.environ:
        api_key = os.environ["OPENAI_API_KEY"]

    if api_key:
        os.environ["OPENAI_API_KEY"] = api_key
    else:
        st.error("No API key found.")

    insight = generate_insight(kpis)
    st.subheader("AI Insight")
    st.write(insight)

    recommendation = generate_recommendation(insight)
    st.subheader("Recommendations")
    st.write(recommendation)