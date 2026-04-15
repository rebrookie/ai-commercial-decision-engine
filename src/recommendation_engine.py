def generate_recommendation(insight):
    prompt = f"""
    Based on the following business insight:

    {insight}

    Provide 2-3 actionable recommendations for:
    - pricing strategy
    - revenue growth
    - regional optimization
    """

    from src.utils.openai_client import get_openai_client

    client = get_openai_client()

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4
    )

    return response.choices[0].message.content