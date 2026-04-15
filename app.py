
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import time

from src.data_loader import load_data
from src.kpi_calculator import calculate_kpis
from src.insight_generator import generate_insight, generate_chat_response
from src.recommendation_engine import generate_recommendation


if "usage_count" not in st.session_state:
    st.session_state.usage_count = 0

if "last_call_time" not in st.session_state:
    st.session_state.last_call_time = 0


# ------------------------
# Page Config
# ------------------------
st.set_page_config(page_title="AI Commercial Decision Engine", layout="wide")

st.title("🚀 AI Commercial Decision Engine")
st.markdown("Transforming commercial analytics from **reporting → decision intelligence**")
st.info("⚠️ This is a demo version of an AI-powered commercial decision system.")

# ------------------------
# Load Data
# ------------------------
df = load_data("data/sales_data.csv")

# ------------------------
# KPI Calculation
# ------------------------
kpis = calculate_kpis(df)

# ------------------------
# Raw Data
# ------------------------
with st.expander("🔍 View Raw Data"):
    st.dataframe(df)

# ------------------------
# Tabs
# ------------------------
tab1, tab2, tab3 = st.tabs([
    "📊 Business Overview",
    "💬 Ask AI about your data",
    "🧠 Persona Based AI Analysis"
    
])

# =========================================================
# TAB 1 — Business Overview
# =========================================================
with tab1:

    st.header("📊 Business Overview")

    col1, col2, col3 = st.columns(3)

    col1.metric("Tot Revenue", f"{kpis.get('total_revenue', 'N/A')}")
    col2.metric("Tot Volume", f"{kpis.get('total_volume', 'N/A')}")
    col3.metric("Avg Price", f"{kpis.get('avg_price', 'N/A')}")

    # ------------------------
    # Trend Analysis
    # ------------------------
    st.subheader("📈 Trend Analysis")

    try:
        df["date"] = pd.to_datetime(df["date"])

        df["month_num"] = df["date"].dt.month
        df["month"] = df["date"].dt.strftime("%b")

        monthly = df.groupby(["month_num", "month"]).agg(
            revenue=("revenue", "sum"),
            volume=("volume", "sum"),
            price=("price", "mean")
        ).reset_index()

        monthly = monthly.sort_values("month_num")

        fig = go.Figure()

        fig.add_trace(go.Bar(
            x=monthly["month"],
            y=monthly["revenue"],
            name="Revenue"
        ))

        fig.add_trace(go.Scatter(
            x=monthly["month"],
            y=monthly["volume"],
            mode="lines+markers",
            name="Volume",
            yaxis="y2"
        ))

        fig.add_trace(go.Scatter(
            x=monthly["month"],
            y=monthly["price"],
            mode="lines+markers",
            name="Avg Price",
            yaxis="y2"
        ))

        fig.update_layout(
            title="Monthly Revenue with Key Drivers",
            xaxis_title="Month",
            yaxis_title="Revenue",
            yaxis2=dict(
                title="Volume / Price",
                overlaying="y",
                side="right"
            ),
            legend=dict(x=0, y=1.15, orientation="h"),
            template="plotly_white"
        )

        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.warning(f"Trend analysis failed: {e}")

# =========================================================
# TAB 2 — Ask AI
# =========================================================
with tab2:
    
    MAX_USAGE = 5
    COOLDOWN_SECONDS = 10

    st.header("💬 Ask AI about your data")

    user_question = st.text_input(
        "Ask questions about pricing, revenue, or customer behavior:",
        value="Why is Product C priced higher for Customer D compared to Customer A?"
    )

    if st.button("Ask AI"):

        now = time.time()

        # -------------------------
        # Cooldown control (anti spam)
        # -------------------------
        if now - st.session_state.last_call_time < COOLDOWN_SECONDS:
            st.warning("Please wait a few seconds before next query.")
            st.stop()

        # -------------------------
        # Usage limit control
        # -------------------------
        if st.session_state.usage_count >= MAX_USAGE:
            st.error("Demo limit reached. Please contact me for full access.")
            st.stop()

        # -------------------------
        # Call AI
        # -------------------------
        with st.spinner("Analyzing..."):
            answer = generate_chat_response(user_question, df, kpis)
            st.markdown(answer)

            # update usage
            st.session_state.usage_count += 1
            st.session_state.last_call_time = now

# =========================================================
# TAB 3 — Persona AI Analysis
# =========================================================
with tab3:

    st.header("🧠 Persona-Based AI Analysis")

    persona = st.selectbox(
        "Choose a perspective:",
        ["Commercial Manager", "Head of Sales", "Pricing Strategist", "Key Account Manager"]
    )

    if st.button("Run AI Analysis"):

        with st.spinner("Generating insights..."):

            try:
                insight = generate_insight(df)
                recommendation = generate_recommendation(insight)

                st.subheader(f"🧠 Insight ({persona})")
                st.markdown(insight)

                st.subheader("💡 Recommendation")
                st.markdown(recommendation)

            except Exception as e:
                st.error(f"Error generating AI output: {e}")


# =========================================================
# Sidebar — Contact
# =========================================================
st.set_page_config(
    page_title="AI Commercial Decision Engine",
    layout="wide",
    initial_sidebar_state="collapsed"
)

with st.sidebar:

    st.title("🚀 AI Commercial Decision Engine")

    st.markdown("""
    Hi, I’m **Lin Liu**, a Commercial Analytics & AI Strategy professional with 15+ years of experience across R&D, Project Management, and Data-driven Commercial Strategy.

    I specialize in:
    - Turning data into business decisions  
    - Bridging strategy and analytics  
    - Building AI-powered decision tools  

    ---

    ### 🚀 About This Project

    I built this AI-powered commercial decision engine that allows business users to query data in natural language and receive strategy-level insights.
    It well demostrates how we convert and eable from data Reporting → Decision Intelligence

    ---
                
    ### ⚙️ Demo Limits
                
    - Max queries: 5
    - Cooldown: 10s
    
    ---

    ### 📬 Contact

    - 💼 LinkedIn: https://www.linkedin.com/in/linl1/  
    - 📧 Email: lin7.liu@gmail.com  

    Feel free to reach out for:
    - Feedback, opportunities, collabration etc.
    - AI & Commercial Strategy discussions  
    """)