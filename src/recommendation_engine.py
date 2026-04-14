def generate_recommendation(insight):
    prompt = f"""
    Based on the following business insight:

    {insight}

    Provide 2-3 actionable recommendations for:
    - pricing strategy
    - revenue growth
    - regional optimization
    """

    from openai import OpenAI

    client = OpenAI(api_key=OPENAI_API_KEY)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4
    )

    return response.choices[0].message.content