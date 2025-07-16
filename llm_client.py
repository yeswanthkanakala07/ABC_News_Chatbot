import openai

client = openai.OpenAI(api_key="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")

def get_openai_response(prompt, model="gpt-4o"):
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content