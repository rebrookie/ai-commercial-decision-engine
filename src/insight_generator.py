import os
from src.utils.openai_client import get_openai_client

client = get_openai_client()


def generate_insight(kpis):
    prompt = f"""
    You are a senior commercial strategy consultant.

    Given the following business data:
    {data_summary}

    Provide:
    1. Key business insight (what is happening)
    2. Root cause (why it is happening)
    3. Risk or opportunity

    Be concise and business-focused.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    return response.choices[0].message.content