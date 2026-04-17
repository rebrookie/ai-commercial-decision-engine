import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import time
import os

from src.data_loader import load_data
from src.kpi_calculator import calculate_kpis
from src.insight_generator import generate_insight, generate_chat_response
from src.recommendation_engine import generate_recommendation

# ------------------------
# Page Config (ONLY ONCE)
# ------------------------
st.set_page_config(
    page_title="AI Commercial Decision Engine",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ------------------------
# Session State Init
# ------------------------
if "usage_count" not in st.session_state:
    st.session_state.usage_count = 0

if "last_call_time" not in st.session_state:
    st.session_state.last_call_time = 0

if "intent" not in st.session_state:
    st.session_state.intent = None

if "user_question" not in st.session_state:
    st.session_state.user_question = ""

# ------------------------
# Intent Definitions
# ------------------------
INTENTS = {
    "price_erosion": "Analyze pricing erosion",
    "portfolio_strategy": "Product focus",
    "customer_strategy": "Customer engagement",
    "executive_summary": "Leadership summary",
    "new_product_priceing_strategy": "New product pricing"
}

# ------------------------
# Intent Detection
# ------------------------
def detect_intent(question: str):
    q = question.lower()

    if "erosion" in q:
        return "price_erosion"
    elif "focus" in q or "which product" in q:
        return "portfolio_strategy"
    elif "customer" in q or "negotiation" in q:
        return "customer_strategy"
    elif "summary" in q or "leadership" in q:
        return "executive_summary"
    elif "new product" in q or "new pricing strategy" in q:
        return "new_product_pricing_strategy"
    else:
        return "general"

# ------------------------
# Title
# ------------------------
st.title("🚀 AI Commercial Decision Engine")
st.markdown("Transforming commercial analytics from **reporting → decision intelligence**")
st.info("⚠️ Demo version with limited AI usage")

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
    "💬 Ask AI",
    "🧠 Persona Analysis"
])

# =========================================================
# TAB 1 — Business Overview
# =========================================================
with tab1:

    st.header("📊 Business Overview")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Revenue", f"{kpis.get('total_revenue', 'N/A')}")
    col2.metric("Total Volume", f"{kpis.get('total_volume', 'N/A')}")
    col3.metric("Avg Price", f"{kpis.get('avg_price', 'N/A')}")

    st.subheader("📈 Trend Analysis")

    try:
        df["date"] = pd.to_datetime(df["date"])
        df["month_num"] = df["date"].dt.month
        df["month"] = df["date"].dt.strftime("%b")

        monthly = df.groupby(["month_num", "month"]).agg(
            revenue=("revenue", "sum"),
            volume=("volume", "sum"),
            price=("price", "mean")
        ).reset_index().sort_values("month_num")

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
            legend=dict(x=0, y=1.1, orientation="h"),
            template="plotly_white"
        )

        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.warning(f"Trend analysis failed: {e}")

# =========================================================
# TAB 2 — Ask AI
# =========================================================
with tab2:

    st.header("💬 Ask AI about your data")

    MAX_USAGE = 5
    COOLDOWN_SECONDS = 10

    # ------------------------
    # Sample Questions
    # ------------------------
    
    st.markdown("# 💡 Sample questions to copy-paste and ask AI:")
    st.markdown("""                    
            - give me a summary of Customers and Products Performance in 2026
            - for customer C, have we achieved our goal of year 2026
            - highlight me the product(s) that with big price erosion issue.
            - what product should be focus in near term for European customers.
            - I'll have a re-negotiation with customer E soon to sell Prod D to the customer, give me some insight on prepping for the customer engagement meeting.
            - I'll have a business review with my leadership team(c-level), give me a summary on what's happening and risk and opportunities.
            - I have a new product Prod F a next gen product of Prod A to sell to the customer A soon, for a successful price positioning, give me some insights to prep for this.

        OR
                
        """)
    
    st.markdown("# 💡 Try simple questions:")

    sample_questions = [
        {"intent": "price_erosion", "text": "Price erosion analysis"},
        {"intent": "portfolio_strategy", "text": "Product focus in Europe"},
        {"intent": "customer_strategy", "text": "Prepare negotiation"},
        {"intent": "executive_summary", "text": "C-level summary"},
        {"intent": "new_product_pricing_strategy", "text": "New product pricing"}
    ]

    
    
    cols = st.columns(2)

    for i, item in enumerate(sample_questions):
        with cols[i % 2]:
            if st.button(item["text"], key=f"q_{i}", use_container_width=True):
                st.session_state.user_question = item["text"]
                st.session_state.intent = item["intent"]

    # ------------------------
    # Input Box
    # ------------------------
    user_question = st.text_input(
        "Ask your question:",
        value=st.session_state.get("user_question", "")
    )

    # ------------------------
    # AI Call
    # ------------------------
    if st.button("Ask AI"):

        now = time.time()

        if now - st.session_state.last_call_time < COOLDOWN_SECONDS:
            st.warning("Please wait before next query.")
            st.stop()

        if st.session_state.usage_count >= MAX_USAGE:
            st.error("Demo limit reached.")
            st.stop()

        with st.spinner("Analyzing..."):

            intent = st.session_state.get("intent") or detect_intent(user_question)

            st.caption(f"🧠 Detected intent: {intent}")

            answer = generate_chat_response(user_question, df, kpis, intent)

            st.markdown("### 📊 Answer")
            st.markdown(answer)

            st.session_state.usage_count += 1
            st.session_state.last_call_time = now

# =========================================================
# TAB 3 — Persona AI Analysis
# =========================================================
with tab3:

    st.header("🧠 Persona-Based AI Analysis")

    persona = st.selectbox(
        "Choose perspective:",
        ["Commercial Manager", "Head of Sales", "Pricing Strategist", "Key Account Manager"]
    )

    if st.button("Run AI Analysis"):

        with st.spinner("Generating insights..."):

            try:
                insight = generate_insight(df)
                recommendation = generate_recommendation(insight)

                st.subheader(f"🧠 Insight ({persona})")
                st.markdown(insight)

                st.divider()

                st.subheader("💡 Recommendation")
                st.markdown(recommendation)

            except Exception as e:
                st.error(f"Error: {e}")

        
# =========================================================
# Sidebar — Contact
# =========================================================
st.set_page_config(
    page_title="AI Commercial Decision Engine",
    layout="wide",
    initial_sidebar_state="collapsed"
)

with st.sidebar:

    st.markdown("""
    ### 🚀 AI Commercial Decision Engine
    Hi, I’m **Lin Liu**, a Commercial Analytics & AI Strategy professional with 15+ years of experience across R&D, Project Management, and Data-driven Commercial Strategy.

    I specialize in:
    - Turning data into business decisions  
    - Bridging strategy and analytics  
    - Building AI-powered decision tools  

    ---

    ### 💡 About This Project

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
    - Feedback, opportunities, collaboration etc.
    - AI & Commercial Strategy discussions  
    """)