import streamlit as st
import os

from src.data_loader import load_data
from src.kpi_calculator import calculate_kpis
from src.insight_generator import generate_insight
from src.recommendation_engine import generate_recommendation

st.title("AI-driven Commercial Decision Engine")

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