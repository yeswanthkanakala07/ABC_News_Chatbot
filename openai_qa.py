import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def ask_openai(query, articles):
    context_blocks = []
    for i, doc in enumerate(articles):
        context_blocks.append(
            f"""Article {i+1}:
Title: {doc['title']}
Summary: {doc['description']}
Details: {doc['spell']}
URL: {doc['url']}"""
        )
    context = "\n\n".join(context_blocks)

    prompt = f"""Answer the question below based only on the news context provided.

Question: {query}

Context:
{context}
"""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes and answers questions using news data."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    return response.choices[0].message.content
