import pandas as pd
from src.utils.openai_client import get_openai_client
from openai import OpenAI

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

def generate_chat_response(question, df, kpis):

    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

    sample_data = df.head(20).to_dict()

    prompt = f"""
    You are a commercial strategy analyst.

    Business KPIs:
    {kpis}

    Sample data:
    {sample_data}

    User question:
    {question}

    Please provide:
    - Clear answer
    - Business insight
    - Actionable recommendation
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content