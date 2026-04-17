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

st.markdown("""
<style>

/* 主内容区域限制宽度 + 居中 */
.block-container {
    max-width: 800px;   /* 👈 控制宽度 */
    padding-top: 2rem;
    padding-bottom: 2rem;
    margin-left: auto;
    margin-right: auto;
}

/* 可选：让header也居中 */
h1, h2, h3 {
    text-align: left;
}

</style>
""", unsafe_allow_html=True)

st.markdown("""
<h1 style='font-size:26px; font-weight:600; margin-bottom:5px;'>
🚀 AI Commercial Decision Engine
</h1>
<p style='color:gray; margin-top:0;'>
Transforming commercial analytics from reporting → decision intelligence
</p>
""", unsafe_allow_html=True)


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

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

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

def card_container(title):
    st.markdown(f"""
    <div class="card" style="
        border:1px solid #e6e6e6;
        border-radius:14px;
        padding:20px;
        margin-bottom:20px;
        background-color:#ffffff;
    ">
        <h3 style="margin-top:0;">{title}</h3>
    """, unsafe_allow_html=True)

def end_card():
    st.markdown("</div>", unsafe_allow_html=True)





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
with st.expander("🎯 Raw Data (click to collapse)", expanded=True):
    st.dataframe(df, use_container_width=True)

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

    card_container("📊 Business Overview")

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

        st.plotly_chart(fig, use_container_width=True, height=600)
        
    except Exception as e:
        st.warning(f"Trend analysis failed: {e}")

    end_card()

# =========================================================
# TAB 2 — Ask AI
# =========================================================
with tab2:

    card_container("💬 Ask AI Assistant")

    MAX_USAGE = 5
    COOLDOWN_SECONDS = 10

    # ------------------------
    # Sample Questions
    # ------------------------
    
    with st.expander("🔍 Help (click to expand)"):

        st.markdown("##### 💡 Try sample questions:")
        st.markdown("""
                        
                To copy-paste and ask AI
                    
                - Give me a summary of Customers and Products Performance in 2026
                - For customer C, have we achieved our goal of year 2026
                - Highlight me the product(s) that with big price erosion issue.
                - What product should be focus in near term for European customers.
                - I'll have a re-negotiation with customer E soon to sell Prod D to the customer, give me some insight on prepping for the customer engagement meeting.
                - I'll have a business review with my leadership team(c-level), give me a summary on what's happening and risk and opportunities.
                - I have a new product Prod F a next gen product of Prod A to sell to the customer A soon, for a successful price positioning, give me some insights to prep for this.

            OR
                    
            """)
        
        st.markdown("##### 💡 Try quick questions:")

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
    user_question = st.text_area(
        "",
        placeholder="Ask about pricing, growth, or customer strategy...",
        height=120
    )

    # ------------------------
    # AI Call
    # ------------------------
    col1, col2 = st.columns([2, 2])  # 👉 Ask bigger, Clear smaller

    with col1:
        ask_clicked = st.button("💻 Ask AI", use_container_width=True)

    with col2:
        clear_clicked = st.button("🗑️ Clear Conversation", use_container_width=True)
    
    if clear_clicked:
        st.session_state.chat_history = []
        st.session_state.usage_count = 0
    
    if ask_clicked:

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

            # 👉 保存用户问题
            st.session_state.chat_history.append({
                "role": "user",
                "content": user_question
            })

            # 👉 AI回答
            answer = generate_chat_response(user_question, df, kpis, intent)

            # 👉 保存AI回答
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": answer
            })

            st.markdown("### 📊 Latest Answer")
            st.markdown(answer)

            st.session_state.usage_count += 1
            st.session_state.last_call_time = now

    

    st.markdown("### 💬 Conversation")

    chat_container = st.container(height=550)

    with chat_container:
        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
    
    end_card()

# =========================================================
# TAB 3 — Persona AI Analysis
# =========================================================
with tab3:

    card_container("🧠 Persona-Based AI Analysis")

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

    end_card()

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
    It well demostrates how we transform commercial analytics from Reporting → Decision Intelligence

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