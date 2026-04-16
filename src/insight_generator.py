import pandas as pd
from src.utils.openai_client import get_openai_client
from openai import OpenAI
import streamlit as st

def generate_insight(df):
    client = get_openai_client()

    # ✅ Step 1: 构造数据摘要（关键！）
    data_summary = df.describe().to_string()

    # ✅ Step 2: prompt
    prompt = f"""
    You are a senior commercial strategy consultant of Telecom industry to provide insights only from telecom equipment providers' perspectives.

    Given the following business data summary:
    {data_summary}

    Provide:
    1. Key business insight (what is happening)
    2. Root cause (why it is happening)
    3. Risk or opportunity

    Be concise and business-focused.
    """

    # ✅ Step 3: 调用模型
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content

from openai import OpenAI
import os

def generate_chat_response(question, df, kpis, intent):

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    sample_data = df.head(20).to_dict(orient="records")

    # -------------------------
    # Intent-based system prompt
    # -------------------------
    if intent == "pricing_erosion":
        system_prompt = """
        You are a pricing strategy expert.
        Analyze price erosion, identify drivers, and recommend actions.

        Output format:
        - Key Issue
        - Root Cause
        - Recommendation
        """

    elif intent == "executive_summary":
        system_prompt = """
        You are advising a C-level executive.

        Provide:
        - Performance summary
        - Risks
        - Opportunities
        - Actions
        """

    elif intent == "customer_strategy":
        system_prompt = """
        You are a key account strategist.
        Provide negotiation insights and recommended approach.
        """

    else:
        system_prompt = """
        You are a senior commercial analyst with deep telecom experience.
        Provide structured and actionable business insights.
        """

    # -------------------------
    # Build user prompt (FIXED)
    # -------------------------
    prompt = f"""
    Business KPIs:
    {kpis}

    Sample Data:
    {sample_data}

    User Question:
    {question}

    Please provide:
    - Clear answer
    - Business insight
    """

    # -------------------------
    # Call OpenAI
    # -------------------------
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content