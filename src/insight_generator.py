import os
from src.utils.openai_client import get_openai_client

client = get_openai_client()


def generate_insight(kpis):
    prompt = f"""
    You are a senior commercial strategy analyst.

    Given the following KPIs and trends:
    {kpis}

    Analyze:
    1. Revenue trend over time
    2. Key growth drivers or declines
    3. Any pricing or volume impact

    Provide a structured business insight.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    return response.choices[0].message.content