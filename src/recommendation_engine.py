from src.utils.openai_client import get_openai_client

def generate_recommendation(insight):
    prompt = f"""
    You are a senor commercial strategy advisor of 30 years' experience of telecom industry.

    Based on this insight:
    {insight}

    Provide:
    - 3 actionable recommendations
    - Focus on revenue growth, pricing, pricing strategy, or customer strategy
    - Be specific and practical
    """

    client = get_openai_client()

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4
    )

    return response.choices[0].message.content